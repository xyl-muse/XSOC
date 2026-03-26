from typing import Dict, Any, Optional, Union
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError
from src.models.alert import Alert, AlertSourceEnum
from src.utils.logger import get_logger
logger = get_logger("alert_adapter")
class AlertAdapter:
    """告警适配器，统一两种输入源格式"""
    @classmethod
    def adapt(cls, alert_input: Union[Dict[str, Any], str], source: Optional[AlertSourceEnum] = None) -> Alert:
        """
        适配不同来源的告警输入，转换为统一Alert结构
        :param alert_input: 告警输入，支持两种格式：
            1. Dict: XDR推送的结构化告警
            2. str: 用户手动输入的告警文本
        :param source: 告警来源，不传的话自动识别
        """
        try:
            # 处理字符串输入（用户手动输入）
            if isinstance(alert_input, str):
                return cls._adapt_manual_input(alert_input)

            # 处理结构化输入（XDR推送）
            if isinstance(alert_input, dict):
                if source == AlertSourceEnum.MANUAL or alert_input.get("source") == "MANUAL":
                    return cls._adapt_manual_input(str(alert_input.get("raw_content", str(alert_input))))
                return cls._adapt_xdr_input(alert_input)

            raise ValueError(f"不支持的告警输入类型: {type(alert_input)}")
        except Exception as e:
            logger.error("告警格式适配失败", error=str(e), alert_input=str(alert_input))
            raise
    @classmethod
    def _adapt_xdr_input(cls, xdr_alert: Dict[str, Any]) -> Alert:
        """适配XDR推送的结构化告警"""
        try:
            return Alert(**xdr_alert)
        except ValidationError as e:
            # XDR字段不全时自动补全默认值
            logger.warning("XDR告警字段不全，自动补全", errors=e.errors())
            alert_id = xdr_alert.get("alert_id", f"XDR-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:8]}")
            return Alert(
                alert_id=alert_id,
                alert_type=xdr_alert.get("alert_type", "未知告警类型"),
                src_ip=xdr_alert.get("src_ip"),
                dst_ip=xdr_alert.get("dst_ip"),
                dst_port=xdr_alert.get("dst_port"),
                alert_time=xdr_alert.get("alert_time", datetime.now().isoformat()),
                severity=xdr_alert.get("severity", "中"),
                raw_content=str(xdr_alert),
                source=AlertSourceEnum.XDR
            )
    @classmethod
    def _adapt_manual_input(cls, alert_text: str) -> Alert:
        """适配用户手动输入的文本告警"""
        alert_id = f"MANUAL-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:8]}"
        return Alert(
            alert_id=alert_id,
            alert_type="手动提交告警",
            alert_time=datetime.now().isoformat(),
            raw_content=alert_text,
            source=AlertSourceEnum.MANUAL
        )
