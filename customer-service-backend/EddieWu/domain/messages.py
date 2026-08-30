"""
用消息机器消息数据
"""
from enum import Enum
from dataclasses import dataclass,field
from typing import Any, Literal


class MessageType(Enum):
    TEXT = "text"
    OBJECT = "object"


@dataclass(slots=True)  # 内存占用空间少 访问速度快 对象的属性个数是固定的
class FocusedObject:
    """
    消息类型是对象
    """
    id: str  # 商品编号 or  订单编号
    title: str  # 商品标题 or  订单标题
    type: str  # 点击的商品卡片 type:"product" 点击的是订单卡片 type:"order"
    attributes: dict = field(default_factory=dict)  # 商品or订单的额外信息

    def to_dict(self) -> dict[str, Any]:
        """
        将self的实例对象转换为字典对象：
        对象：业务代码使用的
        字典---json格式字符串--->数据库写操作的时候使用的
        :return:
        """

        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "attributes": dict(self.attributes)  # 浅拷贝
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FocusedObject":
        """
        将字典对象转成实例对象
        :param data:
        :return:
        """
        return cls(
            id=data['id'],
            type=data['type'],
            title=data.get('title'),
            attributes=dict(data.get('attributes',))
        )

@dataclass(slots=True) # 1. 访问速度快__slots__ __dict__() 2.占用内存空间更小 3.对象的属性个数固定住
class UserMessage:
    """
    用户角色的消息
    """
    sender_id: str          # 必填参数(用户id) 前端传过来
    message_id: str         # 必填参数(消息id) 前端没传(扩展) 自己生成自己传入(uuid)
    type: MessageType       # 消息类型(文本以及对象类型)
    text: str | None = None  # 文本类型消息的内容
    object: FocusedObject | None = None  # 对象类型消息的内容

    def to_dict(self) -> dict[str, Any]:
        return {
            "sender_id": self.sender_id,
            "message_id": self.message_id,
            "type": self.type.value,
            "text": self.text,
            "object": FocusedObject.to_dict(self.object) if self.object is not None else None
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserMessage":
        return cls(
            sender_id=data['sender_id'],
            message_id=data['message_id'],
            type=MessageType(data['type']),
            text=data['text'],
            object=FocusedObject.from_dict(data['object']) if data['object'] is not None else None
        )



@dataclass(slots=True)
class BotMessage:
    """
    机器人回复的消息
    """
    text: str  # 机器人回复的内容（当下用的属性）
    object: FocusedObject | None = None  # 后续扩展集成的属性

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "object": FocusedObject.to_dict(self.object) if self.object is not None else None
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BotMessage":
        return cls(
            text=data['text'],
            object=FocusedObject.from_dict(data['object']) if data['object'] is not None else None
        )


@dataclass(slots=True)
class ProcessedResult:
    message_id: str
    messages: list[BotMessage]


@dataclass(slots=True)
class ChatHistoryMessage:
    session_id: str
    role: Literal["user", "bot"]
    text: str | None = None
    object: FocusedObject | None = None