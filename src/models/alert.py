from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime
class AlertSourceEnum(str, Enum):
    """告警来源枚举"""
    XDR = "XDR"
    MANUAL = "MANUAL"
class Alert(BaseModel):
    """统一告警数据模型，适配两种输入源"""
    alert_id: str = Field(description="告警唯一ID")
    alert_type: str = Field(description="告警类型")
    src_ip: Optional[str] = Field(default=None, description="源IP")
    dst_ip: Optional[str] = Field(default=None, description="目的IP")
    dst_port: Optional[int] = Field(default=None, description="目的端口")
    alert_time: str = Field(description="告警时间，ISO格式")
    severity: str = Field(default="中", description="告警严重程度：高/中/低")
    raw_content: str = Field(description="原始告警内容")
    source: AlertSourceEnum = Field(description="告警来源：XDR/MANUAL")
    model_config = {
        "use_enum_values": True,
        "extra": "allow"  # 允许XDR推送额外字段
    }
