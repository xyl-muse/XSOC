from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from typing import Optional, List, Dict, Any
from .alert import Alert
class Event(BaseModel):
    """全链路事件数据模型，贯穿整个处理流程"""
    # 基础信息
    event_id: str = Field(default_factory=lambda: f"EVENT-{uuid4().hex[:16]}", description="事件唯一ID")
    event_name: str = Field(description="事件名称")
    event_type: str = Field(description="事件类型")
    alert: Alert = Field(description="关联的原始告警信息")
    create_time: datetime = Field(default_factory=datetime.now, description="事件创建时间")
    # 研判阶段信息
    is_real_event: Optional[bool] = Field(default=None, description="是否真实事件：True真实/False误报")
    judge_time: Optional[datetime] = Field(default=None, description="研判完成时间")
    judge_evidence: Optional[str] = Field(default=None, description="研判依据")
    judge_tool_calls: List[str] = Field(default_factory=list, description="研判阶段调用工具列表")
    # 溯源阶段信息（仅真实事件有）
    trace_time: Optional[datetime] = Field(default=None, description="溯源完成时间")
    trace_attack_chain: Optional[str] = Field(default=None, description="攻击链分析结果")
    trace_impact_scope: Optional[str] = Field(default=None, description="影响范围")
    trace_root_cause: Optional[str] = Field(default=None, description="根因分析")
    trace_tool_calls: List[str] = Field(default_factory=list, description="溯源阶段调用工具列表")
    # 处置阶段信息（仅真实事件有）
    risk_score: int = Field(default=0, ge=0, le=10, description="风险度评分：0-10分")
    hitl_required: bool = Field(default=False, description="是否需要人工确认")
    hitl_confirmed: bool = Field(default=False, description="人工确认是否通过")
    hitl_confirmed_by: Optional[str] = Field(default=None, description="人工确认人")
    hitl_confirmed_time: Optional[datetime] = Field(default=None, description="人工确认时间")
    response_time: Optional[datetime] = Field(default=None, description="处置完成时间")
    response_actions: List[str] = Field(default_factory=list, description="执行的处置动作列表")
    response_result: Optional[str] = Field(default=None, description="处置结果")
    response_tool_calls: List[str] = Field(default_factory=list, description="处置阶段调用工具列表")
    # 归档阶段信息
    xdr_archived: bool = Field(default=False, description="是否已回写到XDR中心")
    dingtalk_archived: bool = Field(default=False, description="是否已同步到钉钉AI表格")
    report_path: Optional[str] = Field(default=None, description="事件报告文件路径")
    archive_time: Optional[datetime] = Field(default=None, description="归档完成时间")
    model_config = {
        "extra": "allow"
    }
