"""
Fault Tolerance and Auto-Recovery System
Inspired by claude-flow's Dynamic Agent Architecture (DAA)

Core capabilities:
- Automatic retry with exponential backoff
- Graceful degradation
- Health monitoring and heartbeat
- Self-healing mechanisms
"""

import time
import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timedelta
from enum import Enum


class RecoveryStrategy(Enum):
    """Recovery strategies for different failure types"""
    RETRY = "retry"
    GRACEFUL_DEGRADE = "graceful_degrade"
    FALLBACK = "fallback"
    SKIP = "skip"
    ABORT = "abort"


class HealthStatus(Enum):
    """Health status of skills"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class RecoveryManager:
    """Manages fault tolerance and auto-recovery for skill execution"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.max_retries = self.config.get('max_retries', 3)
        self.retry_backoff = self.config.get('retry_backoff', 'exponential')
        self.base_delay = self.config.get('base_delay_ms', 2000) / 1000  # Convert to seconds
        self.timeout = self.config.get('timeout_ms', 300000) / 1000

        # Health monitoring
        self.skill_health: Dict[str, HealthStatus] = {}
        self.skill_failures: Dict[str, List[datetime]] = {}
        self.heartbeat_interval = self.config.get('heartbeat_interval', 30)

        # Circuit breaker
        self.circuit_breaker_threshold = self.config.get('circuit_breaker_threshold', 5)
        self.circuit_breaker_timeout = self.config.get('circuit_breaker_timeout', 60)
        self.open_circuits: Dict[str, datetime] = {}

    def execute_with_retry(
        self,
        skill_name: str,
        skill_func: Callable,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute skill with automatic retry and recovery
        Returns: {'success': bool, 'result': Any, 'attempts': int, 'strategy': str}
        """
        # Check circuit breaker
        if self._is_circuit_open(skill_name):
            return {
                'success': False,
                'error': 'Circuit breaker open',
                'strategy': 'circuit_breaker',
                'attempts': 0
            }

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                # Execute skill
                start_time = time.time()
                result = skill_func(*args, **kwargs)
                execution_time = time.time() - start_time

                # Mark as healthy
                self._record_success(skill_name)

                return {
                    'success': True,
                    'result': result,
                    'attempts': attempt + 1,
                    'execution_time_ms': execution_time * 1000,
                    'strategy': 'direct' if attempt == 0 else 'retry'
                }

            except TimeoutError as e:
                last_error = e
                self.logger.warning(
                    f"Skill {skill_name} timed out on attempt {attempt + 1}"
                )
                self._record_failure(skill_name, 'timeout')

                # Timeout typically needs different handling
                if attempt >= self.max_retries:
                    return self._handle_timeout(skill_name, last_error)

            except Exception as e:
                last_error = e
                self.logger.warning(
                    f"Skill {skill_name} failed on attempt {attempt + 1}: {str(e)}"
                )
                self._record_failure(skill_name, 'error')

                # Check if we should retry
                if attempt < self.max_retries:
                    delay = self._calculate_backoff(attempt)
                    self.logger.info(f"Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    # Max retries reached
                    return self._handle_failure(skill_name, last_error)

        # Should not reach here, but just in case
        return {
            'success': False,
            'error': str(last_error),
            'attempts': self.max_retries + 1,
            'strategy': 'failed_all_retries'
        }

    def _calculate_backoff(self, attempt: int) -> float:
        """Calculate backoff delay based on strategy"""
        if self.retry_backoff == 'exponential':
            return self.base_delay * (2 ** attempt)
        elif self.retry_backoff == 'linear':
            return self.base_delay * (attempt + 1)
        else:  # constant
            return self.base_delay

    def _handle_timeout(self, skill_name: str, error: Exception) -> Dict[str, Any]:
        """Handle timeout with graceful degradation"""
        self.logger.error(f"Skill {skill_name} timed out: {str(error)}")

        # Check if there's a fallback
        fallback_result = self._try_fallback(skill_name)
        if fallback_result:
            return {
                'success': True,
                'result': fallback_result,
                'strategy': 'fallback',
                'warning': 'Used fallback due to timeout'
            }

        return {
            'success': False,
            'error': str(error),
            'strategy': 'timeout_no_fallback'
        }

    def _handle_failure(self, skill_name: str, error: Exception) -> Dict[str, Any]:
        """Handle permanent failure with degradation strategies"""
        self.logger.error(f"Skill {skill_name} failed permanently: {str(error)}")

        # Try graceful degradation
        degraded_result = self._graceful_degrade(skill_name, error)
        if degraded_result:
            return {
                'success': True,
                'result': degraded_result,
                'strategy': 'graceful_degradation',
                'warning': 'Returned degraded result'
            }

        # Try fallback
        fallback_result = self._try_fallback(skill_name)
        if fallback_result:
            return {
                'success': True,
                'result': fallback_result,
                'strategy': 'fallback',
                'warning': 'Used fallback skill'
            }

        # No recovery possible
        return {
            'success': False,
            'error': str(error),
            'strategy': 'no_recovery'
        }

    def _graceful_degrade(self, skill_name: str, error: Exception) -> Optional[Any]:
        """Attempt graceful degradation"""
        # Return partial results or safe defaults
        # This should be customized per skill
        self.logger.info(f"Attempting graceful degradation for {skill_name}")

        # Mark skill as degraded
        self.skill_health[skill_name] = HealthStatus.DEGRADED

        # Return None to indicate no degraded result available
        return None

    def _try_fallback(self, skill_name: str) -> Optional[Any]:
        """Try fallback skill if configured"""
        fallback_config = self.config.get('fallback_skills', {})
        fallback_skill = fallback_config.get(skill_name)

        if fallback_skill:
            self.logger.info(f"Using fallback skill: {fallback_skill}")
            # This would need integration with skill execution system
            # For now, return None
            return None

        return None

    def _record_success(self, skill_name: str):
        """Record successful execution"""
        self.skill_health[skill_name] = HealthStatus.HEALTHY

        # Clear failures
        if skill_name in self.skill_failures:
            self.skill_failures[skill_name] = []

        # Close circuit if open
        if skill_name in self.open_circuits:
            del self.open_circuits[skill_name]
            self.logger.info(f"Circuit breaker closed for {skill_name}")

    def _record_failure(self, skill_name: str, failure_type: str):
        """Record failure and update health status"""
        now = datetime.now()

        if skill_name not in self.skill_failures:
            self.skill_failures[skill_name] = []

        self.skill_failures[skill_name].append(now)

        # Clean old failures (only count recent ones)
        cutoff = now - timedelta(seconds=self.circuit_breaker_timeout)
        self.skill_failures[skill_name] = [
            f for f in self.skill_failures[skill_name] if f > cutoff
        ]

        # Check if circuit should open
        recent_failures = len(self.skill_failures[skill_name])
        if recent_failures >= self.circuit_breaker_threshold:
            self.open_circuits[skill_name] = now
            self.skill_health[skill_name] = HealthStatus.UNHEALTHY
            self.logger.warning(
                f"Circuit breaker opened for {skill_name} "
                f"({recent_failures} failures in {self.circuit_breaker_timeout}s)"
            )
        elif recent_failures > 0:
            self.skill_health[skill_name] = HealthStatus.DEGRADED

    def _is_circuit_open(self, skill_name: str) -> bool:
        """Check if circuit breaker is open for skill"""
        if skill_name not in self.open_circuits:
            return False

        # Check if timeout has passed
        opened_at = self.open_circuits[skill_name]
        now = datetime.now()

        if (now - opened_at).total_seconds() > self.circuit_breaker_timeout:
            # Try half-open state
            del self.open_circuits[skill_name]
            self.skill_health[skill_name] = HealthStatus.DEGRADED
            self.logger.info(f"Circuit breaker half-open for {skill_name}")
            return False

        return True

    def get_health_status(self, skill_name: str) -> HealthStatus:
        """Get current health status of a skill"""
        return self.skill_health.get(skill_name, HealthStatus.UNKNOWN)

    def get_all_health_statuses(self) -> Dict[str, str]:
        """Get health status of all monitored skills"""
        return {
            skill: status.value
            for skill, status in self.skill_health.items()
        }

    def heartbeat_check(self, skill_name: str, status: HealthStatus = HealthStatus.HEALTHY):
        """Record heartbeat from a skill"""
        self.skill_health[skill_name] = status

    def reset_skill_health(self, skill_name: str):
        """Reset health status for a skill"""
        self.skill_health[skill_name] = HealthStatus.HEALTHY
        if skill_name in self.skill_failures:
            self.skill_failures[skill_name] = []
        if skill_name in self.open_circuits:
            del self.open_circuits[skill_name]


class PartialResultCommitter:
    """Commits partial results to avoid losing work on failure"""

    def __init__(self):
        self.partial_results: Dict[str, List[Any]] = {}

    def commit_partial(self, workflow_id: str, skill_name: str, result: Any):
        """Commit partial result"""
        if workflow_id not in self.partial_results:
            self.partial_results[workflow_id] = []

        self.partial_results[workflow_id].append({
            'skill': skill_name,
            'result': result,
            'timestamp': datetime.now()
        })

    def get_partial_results(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Retrieve partial results for a workflow"""
        return self.partial_results.get(workflow_id, [])

    def clear_workflow(self, workflow_id: str):
        """Clear partial results for completed workflow"""
        if workflow_id in self.partial_results:
            del self.partial_results[workflow_id]


class HealthMonitor:
    """Monitors system health with heartbeat mechanism"""

    def __init__(self, interval: int = 30):
        self.interval = interval
        self.last_heartbeats: Dict[str, datetime] = {}

    def record_heartbeat(self, component: str):
        """Record heartbeat from component"""
        self.last_heartbeats[component] = datetime.now()

    def check_health(self) -> Dict[str, bool]:
        """Check which components are healthy based on heartbeats"""
        now = datetime.now()
        health_status = {}

        for component, last_heartbeat in self.last_heartbeats.items():
            time_since_heartbeat = (now - last_heartbeat).total_seconds()
            health_status[component] = time_since_heartbeat < (self.interval * 2)

        return health_status

    def get_unhealthy_components(self) -> List[str]:
        """Get list of components that haven't sent heartbeat"""
        health = self.check_health()
        return [comp for comp, healthy in health.items() if not healthy]
