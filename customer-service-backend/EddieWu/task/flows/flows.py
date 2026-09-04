from dataclasses import dataclass, field

from EddieWu.task.flows.steps import FlowStep

@dataclass(slots=True)
class FlowSlot:
    slot_name:str
    type:str
    label:str
    description:str



@dataclass(slots=True)
class Flow:
    """
    流程对象（不区分系统流程、业务流程）
    作用：
    作用一：后续流程推进器使用流程（steps）
    作用二：后续LLM作为参考，选择开启哪一个业务流程、取消、恢复、填写槽位信息[slots]

    """
    id: str  # 流程ID
    name: str  # 流程名字
    description: str  # 流程描述
    steps: list[FlowStep]  # 流程步骤
    slots: dict[str,FlowSlot]=field(default_factory=dict)   # slots 是后续给LLM来帮助我们填写槽位的时候，作为参考


    def get_step_by_id(self,step_id:str)->FlowStep | None:
        for step in self.steps:
            if step.id==step_id:
                return  step

        return  None





@dataclass(slots=True)
class FlowList:
    """
    职责：承载yaml文件中的顶层元素（slots：user_flows.yml中/flows:两份yml文件都有）
    """
    flows: list[Flow]
    slots: dict[str, FlowSlot] = field(default_factory=dict)     # 字典key是槽位的名字


    def  get_flow_by_id(self,flow_id)->Flow | None:

        for flow in self.flows:
            if flow.id==flow_id:
                return  flow

        return  None



