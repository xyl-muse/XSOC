import structlog
import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any
from src.config.settings import settings
# 确保日志目录存在
os.makedirs(settings.LOG_PATH, exist_ok=True)
# 日志文件名按日期生成
log_file = os.path.join(settings.LOG_PATH, f"xsoc_{datetime.now().strftime('%Y%m%d')}.log")
# 配置结构化日志
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=False),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.BoundLogger,
    cache_logger_on_first_use=True,
)
# 创建日志输出：控制台+文件
logger = structlog.get_logger()
# 添加文件输出handler
from logging.handlers import RotatingFileHandler
import logging
# 配置标准logging输出，用于structlog的文件写入
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=100*1024*1024,  # 100M
    backupCount=30,
    encoding="utf-8"
)
console_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
root_logger = logging.getLogger()
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)
root_logger.setLevel(settings.LOG_LEVEL.upper())
def get_logger(module_name: str, event_id: Optional[str] = None) -> structlog.BoundLogger:
    """
    获取绑定了模块名和事件ID的日志实例
    :param module_name: 模块名称
    :param event_id: 事件唯一ID，用于全链路追踪
    """
    bind_params: Dict[str, Any] = {"module": module_name}
    if event_id:
        bind_params["event_id"] = event_id
    return logger.bind(**bind_params)
def bind_event_id(logger: structlog.BoundLogger, event_id: str) -> structlog.BoundLogger:
    """
    给已有的日志实例绑定事件ID
    :param logger: 已有的日志实例
    :param event_id: 事件唯一ID
    """
    return logger.bind(event_id=event_id)
