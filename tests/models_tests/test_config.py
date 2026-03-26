import os
import pytest
from src.config.settings import settings
def test_default_settings():
    """测试默认配置值"""
    assert settings.PROJECT_NAME == "XSOC 智能安全运营平台"
    assert settings.VERSION == "1.0.0"
    assert settings.DEBUG is False
    assert settings.LOG_LEVEL == "INFO"
    assert settings.HITL_RISK_THRESHOLD == 7
    assert settings.HITL_TIMEOUT == 3600
    assert settings.SKILL_TIMEOUT == 30
    assert settings.SKILL_MAX_RETRIES == 3
def test_env_variable_override(monkeypatch):
    """测试环境变量覆盖配置"""
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("HITL_RISK_THRESHOLD", "8")
    monkeypatch.setenv("XDR_API_KEY", "test_xdr_key")

    # 重新加载配置
    from importlib import reload
    from src.config import settings
    reload(settings)

    assert settings.settings.DEBUG is True
    assert settings.settings.LOG_LEVEL == "DEBUG"
    assert settings.settings.HITL_RISK_THRESHOLD == 8
    assert settings.settings.XDR_API_KEY == "test_xdr_key"
def test_risk_threshold_range():
    """测试风险阈值范围校验"""
    from pydantic import ValidationError
    from src.config.settings import Settings

    with pytest.raises(ValidationError):
        Settings(HITL_RISK_THRESHOLD=11)

    with pytest.raises(ValidationError):
        Settings(HITL_RISK_THRESHOLD=-1)

    # 合法值应该通过
    assert Settings(HITL_RISK_THRESHOLD=0)
    assert Settings(HITL_RISK_THRESHOLD=10)
