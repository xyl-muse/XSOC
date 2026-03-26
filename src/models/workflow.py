from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from src.config.settings import settings
class WorkflowStatusEnum(str, Enum):
    """工作流状态枚举，完全匹配blueprint流程"""
    PENDING_JUDGE = "待研判"
    PENDING_TRACE = "待溯源"
    PENDING_HITL_CONFIRM = "待人工确认"
    PENDING_RESPONSE = "待处置"
    PENDING_ARCHIVE = "待归档"
    COMPLETED = "已完成"
    SUSPENDED = "已挂起"
class WorkflowState(BaseModel):
    """工作流状态模型"""
    event_id: str = Field(description="关联事件ID")
    current_status: WorkflowStatusEnum = Field(default=WorkflowStatusEnum.PENDING_JUDGE, description="当前状态")
    previous_status: Optional[WorkflowStatusEnum] = Field(default=None, description="上一个状态")
    status_updated_time: float = Field(default_factory=lambda: __import__('time').time(), description="状态更新时间戳")
    error_msg: Optional[str] = Field(default=None, description="错误信息")
    def transition(self, next_status: WorkflowStatusEnum, error_msg: Optional[str] = None) -> None:
        """
        状态流转，严格遵循blueprint流程，非法流转会抛出异常
        :param next_status: 下一个状态
        :param error_msg: 错误信息，状态为挂起时需要提供
        """
        allowed_transitions = {
            # 待研判可以流转到：待归档（误报）、待溯源（真实事件）、挂起
            WorkflowStatusEnum.PENDING_JUDGE: [
                WorkflowStatusEnum.PENDING_ARCHIVE,
                WorkflowStatusEnum.PENDING_TRACE,
                WorkflowStatusEnum.SUSPENDED
            ],
            # 待溯源可以流转到：待处置、挂起
            WorkflowStatusEnum.PENDING_TRACE: [
                WorkflowStatusEnum.PENDING_RESPONSE,
                WorkflowStatusEnum.SUSPENDED
            ],
            # 待处置可以流转到：待人工确认（风险高于阈值）、待归档、挂起
            WorkflowStatusEnum.PENDING_RESPONSE: [
                WorkflowStatusEnum.PENDING_HITL_CONFIRM,
                WorkflowStatusEnum.PENDING_ARCHIVE,
                WorkflowStatusEnum.SUSPENDED
            ],
            # 待人工确认可以流转到：待处置（确认通过）、待归档（确认拒绝）、挂起
            WorkflowStatusEnum.PENDING_HITL_CONFIRM: [
                WorkflowStatusEnum.PENDING_RESPONSE,
                WorkflowStatusEnum.PENDING_ARCHIVE,
                WorkflowStatusEnum.SUSPENDED
            ],
            # 待归档可以流转到：已完成、挂起
            WorkflowStatusEnum.PENDING_ARCHIVE: [
                WorkflowStatusEnum.COMPLETED,
                WorkflowStatusEnum.SUSPENDED
            ],
            # 已完成是终态，挂起可以流转回之前的状态
            WorkflowStatusEnum.COMPLETED: [],
            WorkflowStatusEnum.SUSPENDED: [
                WorkflowStatusEnum.PENDING_JUDGE,
                WorkflowStatusEnum.PENDING_TRACE,
                WorkflowStatusEnum.PENDING_RESPONSE,
                WorkflowStatusEnum.PENDING_HITL_CONFIRM,
                WorkflowStatusEnum.PENDING_ARCHIVE
            ]
        }
        if next_status not in allowed_transitions[self.current_status]:
            raise ValueError(f"非法状态流转：{self.current_status} → {next_status}，不在允许的流转列表中")
        if next_status == WorkflowStatusEnum.SUSPENDED and not error_msg:
            raise ValueError("状态设置为挂起时必须提供错误信息")
        self.previous_status = self.current_status
        self.current_status = next_status
        self.status_updated_time = __import__('time').time()
        self.error_msg = error_msg
    def check_hitl_required(self, risk_score: int) -> bool:
        """
        检查是否需要触发HITL人工确认
        :param risk_score: 风险评分0-10
        :return: 是否需要人工确认
        """
        return risk_score >= settings.HITL_RISK_THRESHOLD
