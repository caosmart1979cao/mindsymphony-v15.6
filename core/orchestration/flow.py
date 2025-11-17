"""
CrewAI-inspired Flow implementation

事件驱动工作流引擎，支持装饰器语法和条件路由
"""

import time
from typing import Dict, Any, Callable, List, Optional, Union
from .types import FlowState, FlowOutput


# 装饰器辅助函数
def or_(*events: str) -> List[str]:
    """OR 逻辑：监听多个事件之一"""
    return list(events)


def and_(*events: str) -> tuple:
    """AND 逻辑：监听所有事件（简化实现，实际需要更复杂的逻辑）"""
    return tuple(events)


def start():
    """标记工作流起点"""
    def decorator(func: Callable) -> Callable:
        func._flow_start = True
        return func
    return decorator


def listen(event: Union[str, List[str]]):
    """监听事件"""
    def decorator(func: Callable) -> Callable:
        if isinstance(event, list):
            func._flow_events = event
        else:
            func._flow_events = [event]
        return func
    return decorator


def router(event: str):
    """路由器：根据条件选择下一步"""
    def decorator(func: Callable) -> Callable:
        func._flow_router = True
        func._flow_events = [event]
        return func
    return decorator


class Flow:
    """
    CrewAI 风格的事件驱动工作流

    支持特性：
    1. 装饰器语法定义步骤
    2. 事件监听和触发
    3. 条件路由
    4. 状态管理
    5. Crew 集成
    """

    def __init__(self, name: str, verbose: bool = False):
        """
        初始化工作流

        Args:
            name: 工作流名称
            verbose: 是否输出详细日志
        """
        self.name = name
        self.verbose = verbose
        self.state = FlowState()

        # 注册的步骤
        self.steps: Dict[str, Callable] = {}
        self.start_step: Optional[str] = None

        # 运行时状态
        self.execution_history: List[FlowOutput] = []
        self.crews: Dict[str, Any] = {}  # 可集成的 Crew

        # 自动注册装饰的方法
        self._register_decorated_methods()

    def _register_decorated_methods(self):
        """自动注册所有装饰的方法"""
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue

            attr = getattr(self, attr_name)
            if not callable(attr):
                continue

            # 检查是否有流程装饰器
            if hasattr(attr, '_flow_start'):
                self.start_step = attr_name
                self.steps[attr_name] = attr

            elif hasattr(attr, '_flow_events'):
                # 为每个监听的事件注册步骤
                for event in attr._flow_events:
                    self.steps[event] = attr

            elif hasattr(attr, '_flow_router'):
                for event in attr._flow_events:
                    self.steps[event] = attr

    def run(self, inputs: Dict[str, Any]) -> FlowOutput:
        """
        运行工作流

        Args:
            inputs: 输入数据

        Returns:
            FlowOutput: 工作流执行结果
        """
        start_time = time.time()

        if self.verbose:
            print(f"\n{'=' * 60}")
            print(f"Flow '{self.name}' 启动")
            print(f"起点: {self.start_step}")
            print(f"{'=' * 60}\n")

        # 初始化状态
        self.state = FlowState(data=inputs.copy())

        if not self.start_step:
            raise ValueError(f"Flow '{self.name}' 没有定义起点 (@start)")

        try:
            # 执行起点
            current_step = self.start_step
            step_count = 0
            max_steps = 100  # 防止无限循环

            while current_step and current_step != "END" and step_count < max_steps:
                step_count += 1

                if self.verbose:
                    print(f"[Step {step_count}] 执行: {current_step}")

                # 执行当前步骤
                next_step = self._execute_step(current_step)

                # 记录执行路径
                self.state.execution_path.append(current_step)
                self.state.current_step = current_step

                current_step = next_step

            execution_time_ms = int((time.time() - start_time) * 1000)

            success = (current_step == "END" or step_count < max_steps)

            flow_output = FlowOutput(
                flow_name=self.name,
                final_state=self.state,
                execution_path=self.state.execution_path,
                total_steps=step_count,
                success=success,
                execution_time_ms=execution_time_ms,
                metadata={
                    "final_step": current_step,
                    "max_steps_reached": step_count >= max_steps
                }
            )

            self.execution_history.append(flow_output)

            if self.verbose:
                print(f"\n{'=' * 60}")
                print(f"Flow '{self.name}' 完成")
                print(f"总步骤数: {step_count}")
                print(f"总耗时: {execution_time_ms}ms")
                print(f"状态: {'成功' if success else '失败'}")
                print(f"{'=' * 60}\n")

            return flow_output

        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)

            if self.verbose:
                print(f"\n[Flow '{self.name}'] 执行失败: {str(e)}\n")

            return FlowOutput(
                flow_name=self.name,
                final_state=self.state,
                execution_path=self.state.execution_path,
                total_steps=step_count if 'step_count' in locals() else 0,
                success=False,
                execution_time_ms=execution_time_ms,
                metadata={"error": str(e)}
            )

    def _execute_step(self, step_name: str) -> Optional[str]:
        """
        执行单个步骤

        Args:
            step_name: 步骤名称

        Returns:
            Optional[str]: 下一个步骤名称，或 None/END 表示结束
        """
        if step_name not in self.steps:
            raise ValueError(f"步骤 '{step_name}' 未注册")

        step_func = self.steps[step_name]

        try:
            # 执行步骤函数
            result = step_func()

            # 返回值是下一个步骤
            if result is None:
                return "END"

            return result

        except Exception as e:
            if self.verbose:
                print(f"[Flow] 步骤 '{step_name}' 执行失败: {str(e)}")

            # 错误处理：尝试调用错误处理器
            if "error_handler" in self.steps:
                self.state.metadata["last_error"] = str(e)
                return "error_handler"
            else:
                raise

    def register_crew(self, crew_name: str, crew: Any):
        """
        注册 Crew 供 Flow 调用

        Args:
            crew_name: Crew 名称
            crew: Crew 实例
        """
        self.crews[crew_name] = crew

    def call_crew(self, crew_name: str, inputs: Dict[str, Any]) -> Any:
        """
        在 Flow 中调用 Crew

        Args:
            crew_name: Crew 名称
            inputs: 输入数据

        Returns:
            Any: Crew 执行结果
        """
        if crew_name not in self.crews:
            raise ValueError(f"Crew '{crew_name}' 未注册")

        crew = self.crews[crew_name]
        result = crew.kickoff(inputs)

        return result

    def get_flow_stats(self) -> Dict[str, Any]:
        """获取工作流统计信息"""
        if not self.execution_history:
            return {
                "total_executions": 0,
                "success_rate": 0.0,
                "avg_steps": 0,
                "avg_execution_time_ms": 0
            }

        total = len(self.execution_history)
        successful = sum(1 for e in self.execution_history if e.success)
        avg_steps = sum(e.total_steps for e in self.execution_history) / total
        avg_time = sum(e.execution_time_ms for e in self.execution_history) / total

        return {
            "total_executions": total,
            "success_rate": successful / total,
            "avg_steps": avg_steps,
            "avg_execution_time_ms": int(avg_time),
            "registered_steps": len(self.steps),
            "registered_crews": len(self.crews)
        }


# 示例 Flow 定义
class ExampleFlow(Flow):
    """示例工作流"""

    def __init__(self):
        super().__init__(name="example_flow", verbose=True)

    @start()
    def begin(self) -> str:
        """起点"""
        print("Flow 开始")
        self.state.data["started"] = True
        return "process"

    @listen("process")
    def process_data(self) -> str:
        """处理数据"""
        print("处理数据...")
        self.state.data["processed"] = True
        return "decide"

    @router("decide")
    def make_decision(self) -> str:
        """条件路由"""
        if self.state.data.get("use_path_a", True):
            return "path_a"
        else:
            return "path_b"

    @listen("path_a")
    def handle_path_a(self) -> str:
        """路径 A"""
        print("执行路径 A")
        self.state.data["path"] = "A"
        return "finalize"

    @listen("path_b")
    def handle_path_b(self) -> str:
        """路径 B"""
        print("执行路径 B")
        self.state.data["path"] = "B"
        return "finalize"

    @listen(or_("finalize", "finalize"))
    def finalize(self) -> str:
        """汇聚点"""
        print("完成！")
        self.state.data["completed"] = True
        return "END"
