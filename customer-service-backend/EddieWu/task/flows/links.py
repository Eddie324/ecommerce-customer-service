"""
边数据模型
顺序边： next: ask_order_number
条件边 ：  - if: "条件1" then "clarification_rejected"    - if: "条件2" then "no_relevant_answer"
默认兜底边: - else: ask_rephrase
基类思想
"""

from dataclasses import  dataclass

@dataclass(slots=True)
class   FlowStepLink:
    """
    三种边的基类
    """
    target:str        # 下一个节点的节点ID(顺序边的next内容、条件边的then内容、兜底边的else内容)


@dataclass(slots=True)
class  FlowStepStaticLink(FlowStepLink):
    pass


@dataclass(slots=True)
class FlowStepConditionLink(FlowStepLink):
    condition:str        # 条件



@dataclass(slots=True)
class FlowStepFallbackLink(FlowStepLink):
    pass













