import pytest
from src.models.alert import Alert, AlertSourceEnum
def test_alert_model():
    """测试Alert模型正常创建"""
    alert = Alert(
        alert_id="test-001",
        alert_type="测试告警",
        alert_time="2026-03-26T12:00:00+08:00",
        raw_content="测试告警内容",
        source=AlertSourceEnum.XDR
    )
    assert alert.alert_id == "test-001"
    assert alert.source == AlertSourceEnum.XDR
    assert alert.severity == "中"  # 默认值
def test_alert_extra_fields():
    """测试Alert模型允许额外字段（适配XDR推送的自定义字段）"""
    alert = Alert(
        alert_id="test-001",
        alert_type="测试告警",
        alert_time="2026-03-26T12:00:00+08:00",
        raw_content="测试告警内容",
        source=AlertSourceEnum.XDR,
        extra_field="自定义字段值",
        another_field=123
    )
    assert alert.extra_field == "自定义字段值"
    assert alert.another_field == 123
