"""
Performance Monitoring and Optimization System
Track and optimize skill execution performance

Core capabilities:
- Real-time performance tracking
- Latency monitoring (target P95 < 500ms)
- Memory usage profiling
- Success rate tracking
- Automatic benchmarking
"""

import time
import psutil
import statistics
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque


class PerformanceMonitor:
    """Monitor and track performance metrics"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

        # Metrics storage
        self.latencies: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.memory_usage: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.success_counts: Dict[str, int] = defaultdict(int)
        self.failure_counts: Dict[str, int] = defaultdict(int)

        # Targets
        self.target_p95_latency = self.config.get('target_p95_latency_ms', 500)
        self.target_success_rate = self.config.get('target_success_rate', 0.95)

        # System process for memory tracking
        self.process = psutil.Process()

    def record_execution(
        self,
        skill_name: str,
        execution_time_ms: float,
        success: bool,
        memory_delta_mb: float = None
    ):
        """Record a skill execution"""
        # Record latency
        self.latencies[skill_name].append(execution_time_ms)

        # Record success/failure
        if success:
            self.success_counts[skill_name] += 1
        else:
            self.failure_counts[skill_name] += 1

        # Record memory if provided
        if memory_delta_mb is not None:
            self.memory_usage[skill_name].append(memory_delta_mb)

    def get_metrics(self, skill_name: str) -> Dict[str, Any]:
        """Get comprehensive metrics for a skill"""
        latencies = list(self.latencies.get(skill_name, []))
        memory = list(self.memory_usage.get(skill_name, []))

        if not latencies:
            return {
                'skill_name': skill_name,
                'total_executions': 0,
                'success_rate': 0.0,
                'avg_latency_ms': 0.0,
                'p50_latency_ms': 0.0,
                'p95_latency_ms': 0.0,
                'p99_latency_ms': 0.0,
                'avg_memory_mb': 0.0
            }

        # Calculate latency percentiles
        sorted_latencies = sorted(latencies)
        total = len(sorted_latencies)

        p50_idx = int(total * 0.50)
        p95_idx = int(total * 0.95)
        p99_idx = int(total * 0.99)

        # Calculate success rate
        success = self.success_counts[skill_name]
        failure = self.failure_counts[skill_name]
        total_executions = success + failure
        success_rate = success / total_executions if total_executions > 0 else 0.0

        metrics = {
            'skill_name': skill_name,
            'total_executions': total_executions,
            'success_rate': success_rate,
            'avg_latency_ms': statistics.mean(latencies),
            'p50_latency_ms': sorted_latencies[p50_idx],
            'p95_latency_ms': sorted_latencies[p95_idx],
            'p99_latency_ms': sorted_latencies[p99_idx],
            'min_latency_ms': min(latencies),
            'max_latency_ms': max(latencies)
        }

        # Memory metrics
        if memory:
            metrics['avg_memory_mb'] = statistics.mean(memory)
            metrics['peak_memory_mb'] = max(memory)

        # Performance status
        metrics['performance_status'] = self._evaluate_performance(
            success_rate,
            sorted_latencies[p95_idx]
        )

        return metrics

    def _evaluate_performance(
        self,
        success_rate: float,
        p95_latency: float
    ) -> str:
        """Evaluate performance status"""
        if (success_rate >= self.target_success_rate and
                p95_latency <= self.target_p95_latency):
            return 'excellent'
        elif success_rate >= 0.85 and p95_latency <= self.target_p95_latency * 1.5:
            return 'good'
        elif success_rate >= 0.70:
            return 'degraded'
        else:
            return 'poor'

    def get_all_metrics(self) -> List[Dict[str, Any]]:
        """Get metrics for all skills"""
        all_skills = set(self.latencies.keys()) | set(self.success_counts.keys())
        return [self.get_metrics(skill) for skill in all_skills]

    def get_slow_skills(self, threshold_ms: float = None) -> List[Dict[str, Any]]:
        """Get skills that are slower than threshold"""
        threshold = threshold_ms or self.target_p95_latency
        slow_skills = []

        for skill in self.latencies.keys():
            metrics = self.get_metrics(skill)
            if metrics['p95_latency_ms'] > threshold:
                slow_skills.append({
                    'skill_name': skill,
                    'p95_latency_ms': metrics['p95_latency_ms'],
                    'target_ms': threshold,
                    'slowdown_factor': metrics['p95_latency_ms'] / threshold
                })

        slow_skills.sort(key=lambda x: x['slowdown_factor'], reverse=True)
        return slow_skills

    def get_failing_skills(self, threshold: float = None) -> List[Dict[str, Any]]:
        """Get skills with success rate below threshold"""
        threshold = threshold or self.target_success_rate
        failing_skills = []

        for skill in set(self.success_counts.keys()) | set(self.failure_counts.keys()):
            metrics = self.get_metrics(skill)
            if metrics['success_rate'] < threshold:
                failing_skills.append({
                    'skill_name': skill,
                    'success_rate': metrics['success_rate'],
                    'target_rate': threshold,
                    'total_executions': metrics['total_executions']
                })

        failing_skills.sort(key=lambda x: x['success_rate'])
        return failing_skills

    def generate_report(self) -> str:
        """Generate performance report"""
        all_metrics = self.get_all_metrics()

        if not all_metrics:
            return "No performance data collected yet."

        # Summary statistics
        total_executions = sum(m['total_executions'] for m in all_metrics)
        avg_success_rate = statistics.mean(m['success_rate'] for m in all_metrics)

        report = f"""
# MindSymphony Performance Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Skills Monitored: {len(all_metrics)}
- Total Executions: {total_executions}
- Average Success Rate: {avg_success_rate:.2%}

## Top Performing Skills
"""
        # Top performers
        top_skills = sorted(
            all_metrics,
            key=lambda x: (x['success_rate'], -x['p95_latency_ms']),
            reverse=True
        )[:5]

        for skill in top_skills:
            report += f"\n- {skill['skill_name']}: "
            report += f"{skill['success_rate']:.1%} success, "
            report += f"P95={skill['p95_latency_ms']:.0f}ms"

        # Performance issues
        slow_skills = self.get_slow_skills()
        failing_skills = self.get_failing_skills()

        if slow_skills:
            report += "\n\n## ⚠️ Slow Skills (P95 > target)"
            for skill in slow_skills[:5]:
                report += f"\n- {skill['skill_name']}: "
                report += f"{skill['p95_latency_ms']:.0f}ms "
                report += f"({skill['slowdown_factor']:.1f}x target)"

        if failing_skills:
            report += "\n\n## ❌ Failing Skills (Success < target)"
            for skill in failing_skills[:5]:
                report += f"\n- {skill['skill_name']}: "
                report += f"{skill['success_rate']:.1%} "
                report += f"({skill['total_executions']} executions)"

        report += "\n"
        return report


class ExecutionTimer:
    """Context manager for timing execution"""

    def __init__(self, monitor: PerformanceMonitor, skill_name: str):
        self.monitor = monitor
        self.skill_name = skill_name
        self.start_time = None
        self.start_memory = None
        self.success = True

    def __enter__(self):
        self.start_time = time.time()
        self.start_memory = self.monitor.process.memory_info().rss / 1024 / 1024
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        end_memory = self.monitor.process.memory_info().rss / 1024 / 1024

        execution_time_ms = (end_time - self.start_time) * 1000
        memory_delta_mb = end_memory - self.start_memory

        # Mark as failed if exception occurred
        if exc_type is not None:
            self.success = False

        self.monitor.record_execution(
            self.skill_name,
            execution_time_ms,
            self.success,
            memory_delta_mb
        )

        # Don't suppress exceptions
        return False

    def mark_failed(self):
        """Manually mark execution as failed"""
        self.success = False


class SkillProfiler:
    """Profile skill execution for optimization"""

    def __init__(self):
        self.profiles: Dict[str, Dict[str, Any]] = {}

    def profile_skill(self, skill_name: str, func, *args, **kwargs) -> Dict[str, Any]:
        """Profile a skill execution"""
        import cProfile
        import pstats
        from io import StringIO

        profiler = cProfile.Profile()

        start_time = time.time()
        profiler.enable()

        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = None
            success = False

        profiler.disable()
        end_time = time.time()

        # Get profiling stats
        s = StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats(20)  # Top 20 functions

        profile_data = {
            'skill_name': skill_name,
            'execution_time_ms': (end_time - start_time) * 1000,
            'success': success,
            'result': result,
            'profile_stats': s.getvalue(),
            'timestamp': datetime.now()
        }

        self.profiles[skill_name] = profile_data
        return profile_data

    def get_hotspots(self, skill_name: str) -> Optional[str]:
        """Get performance hotspots for a skill"""
        if skill_name in self.profiles:
            return self.profiles[skill_name]['profile_stats']
        return None


class BenchmarkRunner:
    """Run benchmarks to establish performance baselines"""

    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self.baselines: Dict[str, Dict[str, float]] = {}

    def benchmark_skill(
        self,
        skill_name: str,
        skill_func,
        test_inputs: List[Any],
        iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Run benchmark for a skill
        Returns baseline performance metrics
        """
        latencies = []
        successes = 0

        for _ in range(iterations):
            for test_input in test_inputs:
                with ExecutionTimer(self.monitor, skill_name) as timer:
                    try:
                        skill_func(test_input)
                        successes += 1
                    except Exception:
                        timer.mark_failed()

        # Get metrics after benchmark
        metrics = self.monitor.get_metrics(skill_name)

        # Store baseline
        self.baselines[skill_name] = {
            'p95_latency_ms': metrics['p95_latency_ms'],
            'success_rate': metrics['success_rate'],
            'timestamp': datetime.now()
        }

        return metrics

    def compare_to_baseline(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Compare current performance to baseline"""
        if skill_name not in self.baselines:
            return None

        baseline = self.baselines[skill_name]
        current = self.monitor.get_metrics(skill_name)

        return {
            'skill_name': skill_name,
            'baseline_p95_ms': baseline['p95_latency_ms'],
            'current_p95_ms': current['p95_latency_ms'],
            'latency_change': (
                    (current['p95_latency_ms'] - baseline['p95_latency_ms']) /
                    baseline['p95_latency_ms']
            ),
            'baseline_success_rate': baseline['success_rate'],
            'current_success_rate': current['success_rate'],
            'success_rate_change': current['success_rate'] - baseline['success_rate']
        }


class OptimizationAdvisor:
    """Provide optimization recommendations"""

    @staticmethod
    def analyze_and_recommend(metrics: Dict[str, Any]) -> List[str]:
        """Analyze metrics and provide recommendations"""
        recommendations = []

        # High latency
        if metrics['p95_latency_ms'] > 500:
            recommendations.append(
                f"⚡ High latency detected (P95={metrics['p95_latency_ms']:.0f}ms). "
                "Consider: connection pooling, caching, or async execution."
            )

        # Low success rate
        if metrics['success_rate'] < 0.90:
            recommendations.append(
                f"❌ Low success rate ({metrics['success_rate']:.1%}). "
                "Consider: adding retry logic, improving error handling, or input validation."
            )

        # High memory usage
        if 'peak_memory_mb' in metrics and metrics['peak_memory_mb'] > 500:
            recommendations.append(
                f"💾 High memory usage (peak={metrics['peak_memory_mb']:.0f}MB). "
                "Consider: streaming processing, garbage collection, or data structure optimization."
            )

        # High variance in latency
        if 'max_latency_ms' in metrics and 'min_latency_ms' in metrics:
            variance = metrics['max_latency_ms'] / metrics['min_latency_ms']
            if variance > 10:
                recommendations.append(
                    f"📊 High latency variance ({variance:.1f}x). "
                    "Consider: preloading resources, reducing cold starts, or optimizing worst-case paths."
                )

        if not recommendations:
            recommendations.append("✅ Performance looks good! No immediate optimizations needed.")

        return recommendations
