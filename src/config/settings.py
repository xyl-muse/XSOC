from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
class Settings(BaseSettings):
    """全局配置类，支持环境变量注入"""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    # 项目基础配置
    PROJECT_NAME: str = Field(default="XSOC 智能安全运营平台", description="项目名称")
    VERSION: str = Field(default="1.0.0", description="版本号")
    DEBUG: bool = Field(default=False, description="调试模式")
    LOG_LEVEL: str = Field(default="INFO", description="日志级别: DEBUG/INFO/WARNING/ERROR/CRITICAL")
    LOG_PATH: str = Field(default="./logs", description="日志存储路径")
    # HITL 机制配置
    HITL_RISK_THRESHOLD: int = Field(default=7, ge=0, le=10, description="HITL人工确认风险阈值，0-10分，高于此值需要人工确认")
    HITL_TIMEOUT: int = Field(default=3600, description="人工确认超时时间(秒)，超时则事件挂起")
    # MCP 配置
    MCP_THREAT_INTEL_URL: Optional[str] = Field(default=None, description="微步威胁情报MCP服务地址")
    MCP_THREAT_INTEL_API_KEY: Optional[str] = Field(default=None, description="微步威胁情报MCP API密钥")
    # Skill 接口通用配置
    SKILL_TIMEOUT: int = Field(default=30, description="Skill接口调用超时时间(秒)")
    SKILL_MAX_RETRIES: int = Field(default=3, description="Skill接口调用最大重试次数")
    SKILL_RETRY_DELAY: int = Field(default=1, description="Skill接口重试间隔(秒)")
    # XDR 配置
    XDR_API_URL: Optional[str] = Field(default=None, description="XDR中心API地址")
    XDR_API_KEY: Optional[str] = Field(default=None, description="XDR中心API密钥")
    XDR_EVENT_ARCHIVE_PATH: Optional[str] = Field(default=None, description="XDR事件归档回写接口路径")
    # 钉钉AI表格配置
    DINGTALK_API_URL: Optional[str] = Field(default=None, description="钉钉API地址")
    DINGTALK_APP_KEY: Optional[str] = Field(default=None, description="钉钉应用Key")
    DINGTALK_APP_SECRET: Optional[str] = Field(default=None, description="钉钉应用密钥")
    DINGTALK_AI_TABLE_ID: Optional[str] = Field(default=None, description="钉钉AI表格ID")
    # 工作流配置
    WORKFLOW_MAX_PARALLEL_TASKS: int = Field(default=10, description="最大并行处理事件数")
    WORKFLOW_EVENT_EXPIRE_TIME: int = Field(default=86400, description="事件处理超时时间(秒)，超时自动关闭")
settings = Settings()
