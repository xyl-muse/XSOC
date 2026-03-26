import os
import tempfile
from src.utils.logger import get_logger, bind_event_id
def test_get_logger():
    """测试获取日志实例"""
    logger = get_logger("test_module")
    assert logger is not None
def test_logger_with_event_id():
    """测试绑定事件ID的日志"""
    logger = get_logger("test_module", event_id="test-event-123")
    assert logger is not None
    logger = bind_event_id(logger, "test-event-456")
    assert logger is not None
def test_log_output():
    """测试日志输出功能"""
    logger = get_logger("test")
    # 测试各级别日志输出不报错
    logger.debug("debug test")
    logger.info("info test")
    logger.warning("warning test")
    logger.error("error test")
