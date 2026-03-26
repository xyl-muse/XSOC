import pytest
from src.utils.alert_adapter import AlertAdapter
from src.models.alert import AlertSourceEnum
def test_adapt_manual_input():
    """测试适配用户手动输入的字符串告警"""
    alert_text = "服务器10.0.0.5CPU占用率100%，疑似挖矿"
    alert = AlertAdapter.adapt(alert_text)
    assert alert.alert_id.startswith("MANUAL-")
    assert alert.alert_type == "手动提交告警"
    assert alert.source == AlertSourceEnum.MANUAL
    assert alert.raw_content == alert_text
def test_adapt_xdr_input():
    """测试适配XDR推送的结构化告警"""
    xdr_alert = {
        "alert_id": "ALERT-20260326-00001",
        "alert_type": "暴力破解",
        "src_ip": "192.168.1.100",
        "dst_ip": "10.0.0.5",
        "dst_port": 22,
        "alert_time": "2026-03-26T12:00:00+08:00",
        "severity": "高",
        "raw_content": "SSH暴力破解尝试127次",
        "source": "XDR"
    }
    alert = AlertAdapter.adapt(xdr_alert)
    assert alert.alert_id == "ALERT-20260326-00001"
    assert alert.alert_type == "暴力破解"
    assert alert.src_ip == "192.168.1.100"
    assert alert.source == AlertSourceEnum.XDR
def test_adapt_xdr_input_missing_fields():
    """测试XDR告警字段不全时的自动补全"""
    xdr_alert = {
        "raw_content": "未知告警，字段不全"
    }
    alert = AlertAdapter.adapt(xdr_alert)
    assert alert.alert_id.startswith("XDR-")
    assert alert.alert_type == "未知告警类型"
    assert alert.raw_content == str(xdr_alert)
    assert alert.source == AlertSourceEnum.XDR
def test_adapt_manual_dict_input():
    """测试手动输入的字典格式告警"""
    manual_alert = {
        "source": "MANUAL",
        "raw_content": "手动提交的挖矿告警"
    }
    alert = AlertAdapter.adapt(manual_alert)
    assert alert.alert_id.startswith("MANUAL-")
    assert alert.source == AlertSourceEnum.MANUAL
    assert alert.raw_content == "手动提交的挖矿告警"
