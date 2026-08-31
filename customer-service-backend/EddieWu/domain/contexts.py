"""
定义两个数据模型
业务流程
系统流程
上下文概念:
把动态的信息，封装成上下文对象，传递给引擎
承载动态可变的内容

TaskContext未来给引擎使用(运行流程以及执行流程的步骤)
引擎未来执行哪一个流程和哪一步(信息数据)[不固定]----TaskContext(flow_id,step_id)
"""
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(slots=True)
class TaskContext:
    """
    业务流程上下文：
    flow_id:业务流程ID:确认业务流是哪一个的唯一标识：比如order_status_query
    step_id: 业务流程的步骤ID.确认业务流程的步骤。已经走了哪些不，该走哪一步
    slots: 业务流程缺少的槽位信息
    """

    flow_id: str
    step_id: str
    slots: dict[str, Any] = field(default_factory=dict)  # 槽位的信息

    def to_dict(self) -> dict[str, Any]:
        return {
            "flow_id": self.flow_id,
            "step_id": self.step_id,
            "slots": self.slots
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskContext":
        return cls(
            flow_id=data['flow_id'],
            step_id=data['step_id'],
            slots=data['slots']
        )


@dataclass(slots=True)
class SystemContext:
    """
    系统流程上下文的基类(模版)
    flow_id: 系统流程ID: system_task_started
    step_id: 系统流程的步骤ID:start
    flow_id/step_id一定要是这两个名字【在流程推进器的时候，解释原因】
    """

    flow_id: str
    step_id: str

    def to_dict(self) -> dict[str, Any]:
        """将具体的子类对象转成字典"""
        return asdict(self)  # type: ignore

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "SystemContext":
        """将字典转成对应的子类对象"""
        flow_id = data['flow_id']
        clz = SYSTEM_CONTEXT_TO_CLASS[flow_id]
        return clz(**data)


@dataclass(slots=True)
class SystemTaskStartedContext(SystemContext):
    """
    触发时机 开启业务流程的时候(先触发)
    """
    started_flow_id: str  # 开启的业务流程的流程ID
    started_flow_name: str  # 开启的业务流程的流程名字(根据业务流程ID获取)


@dataclass(slots=True)
class SystemTaskInterruptedContext(SystemContext):
    """
    触发时机 中断某一个业务流程的时候(场景:之前正在进行A业务流程 接着开启B业务流程 底层:先把之前的业务流程存储起来,然后再开启新的业务流程: 中断的开场白:)
    """
    interrupted_flow_id: str        # 中断的业务流程的流程ID
    interrupted_flow_name: str      # 中断的业务流程的流程名字
    started_flow_id: str            # 开启新的业务流程ID
    started_flow_name: str          # 开启新的业务流程的流程名字


@dataclass(slots=True)
class SystemTaskResumedContext(SystemContext):
    """
    触发时机 恢复一个中断的业务流程的时候
    """
    resumed_flow_id: str        # 中断的业务流程ID
    resumed_flow_name: str      # 中断的业务流程名字


@dataclass(slots=True)
class SystemTaskResumeFailedContext(SystemContext):
    """没有找到可恢复的业务流程时使用。"""


@dataclass(slots=True)
class SystemTaskCanceledContext(SystemContext):
    """
    触发时机 取消一个已经开启的业务流程
    """
    canceled_flow_id: str        # 取消的业务流程ID
    canceled_flow_name: str      # 取消的业务流程名字


@dataclass(slots=True)
class SystemCollectInformationContext(SystemContext):
    """
    触发时机 当某个业务流程要补充信息的时候
    1. 告诉用户槽位要填写什么
    2. 收集用户填写这个槽位的信息{"order_number":"A10001"}---下游如果有逻辑 继续使用
    """
    response: dict[str, Any]  # 要告诉用户业务流程槽位缺少什么 {"text":"请告诉我你的订单号"}
    slot_name: str  # 缺少槽位名字【槽位信息：槽位名字 槽位值】 TODO 主要是为了判断


SYSTEM_CONTEXT_TO_CLASS: dict[str, type[SystemContext]] = {
    """
    映射
    """
    "system_task_started": SystemTaskStartedContext,
    "system_task_interrupted": SystemTaskInterruptedContext,
    "system_task_resumed": SystemTaskResumedContext,
    "system_task_canceled": SystemTaskCanceledContext,
    "system_collect_information": SystemCollectInformationContext,
    "system_task_resume_failed": SystemTaskResumeFailedContext
}