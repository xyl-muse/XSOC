import pytest
from src.models.event import Event
from src.models.alert import Alert, AlertSourceEnum
def test_event_model_defaults():
    """测试Event模型默认值"""
    alert = Alert(
        alert_id="test-001",
        alert_type="测试告警",
        alert_time="2026-03-26T12:00:00+08:00",
        raw_content="测试内容",
        source=AlertSourceEnum.MANUAL
    )
    event = Event(
        event_name="测试事件",
        event_type="测试类型",
        alert=alert
    )
    assert event.event_id.startswith("EVENT-")
    assert event.create_time is not None
    assert event.is_real_event is None
    assert event.risk_score == 0
    assert event.judge_tool_calls == []
def test_event_risk_score_validation():
    """测试风险评分范围校验"""
    alert = Alert(
        alert_id="test-001",
        alert_type="测试告警",
        alert_time="2026-03-26T12:00:00+08:00",
        raw_content="测试内容",
        source=AlertSourceEnum.MANUAL
    )
    # 合法值
    event = Event(event_name="测试", event_type="测试", alert=alert, risk_score=7)
    assert event.risk_score ==7
    # 非法值应该抛出异常
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        Event(event_name="测试", event_type="测试", alert=alert, risk_score=11)
    with pytest.raises(ValidationError):
        Event(event_name="测试", event_type="测试", alert=alert, risk_score=-1)
