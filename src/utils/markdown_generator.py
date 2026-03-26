from datetime import datetime
from typing import Dict, Any, Optional
from src.models.event import Event
from src.utils.logger import get_logger
logger = get_logger("markdown_generator")
class MarkdownGenerator:
    """事件报告生成器，按照blueprint要求生成标准化md文档"""
    @classmethod
    def generate_event_report(cls, event: Event) -> str:
        """
        生成完整事件运营脉络报告
        :param event: 完整事件对象
        :return: markdown格式的报告内容
        """
        report = [
            f"# 安全事件报告：{event.event_name}",
            f"## 基本信息",
            f"- 事件ID: `{event.event_id}`",
            f"- 告警ID: `{event.alert.alert_id}`",
            f"- 事件类型: {event.event_type}",
            f"- 告警时间: {event.alert.alert_time}",
            f"- 事件完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- 风险评分: {event.risk_score}/10",
            f"- 事件状态: {'真实事件' if event.is_real_event else '误报'}",
            "",
            f"## 原始告警信息",
            f"- 告警来源: {event.alert.source}",
            f"- 告警类型: {event.alert.alert_type}",
            f"- 源IP: {event.alert.src_ip or '无'}",
            f"- 目的IP: {event.alert.dst_ip or '无'}",
            f"- 目的端口: {event.alert.dst_port or '无'}",
            f"- 告警详情: {event.alert.raw_content}",
            ""
        ]
        # 研判过程
        report.extend([
            f"## 事件研判过程",
            f"- 研判专家: 事件研判智能体",
            f"- 研判时间: {event.judge_time.strftime('%Y-%m-%d %H:%M:%S') if event.judge_time else '未记录'}",
            f"- 研判结论: {'真实事件，进入溯源流程' if event.is_real_event else '误报，事件结束'}",
            f"- 研判依据: {event.judge_evidence or '无'}",
            f"- 调用工具记录: {', '.join(event.judge_tool_calls) if event.judge_tool_calls else '无'}",
            ""
        ])
        # 真实事件的溯源和处置内容
        if event.is_real_event:
            # 溯源分析
            report.extend([
                f"## 溯源分析结果",
                f"- 溯源专家: 溯源分析智能体",
                f"- 溯源时间: {event.trace_time.strftime('%Y-%m-%d %H:%M:%S') if event.trace_time else '未记录'}",
                f"- 攻击链分析: {event.trace_attack_chain or '无'}",
                f"- 影响范围: {event.trace_impact_scope or '无'}",
                f"- 根因分析: {event.trace_root_cause or '无'}",
                f"- 调用工具记录: {', '.join(event.trace_tool_calls) if event.trace_tool_calls else '无'}",
                ""
            ])
            # 风险处置
            report.extend([
                f"## 风险处置记录",
                f"- 处置专家: 风险处置智能体",
                f"- 处置时间: {event.response_time.strftime('%Y-%m-%d %H:%M:%S') if event.response_time else '未记录'}",
                f"- 风险评分: {event.risk_score}/10",
                f"- HITL人工确认: {'已通过' if event.hitl_confirmed else '未触发'}",
                f"- 人工确认人: {event.hitl_confirmed_by or '无'}",
                f"- 处置动作: {event.response_actions or '无'}",
                f"- 处置结果: {event.response_result or '无'}",
                f"- 调用工具记录: {', '.join(event.response_tool_calls) if event.response_tool_calls else '无'}",
                ""
            ])
        # 归档信息
        report.extend([
            f"## 归档信息",
            f"- 归档专家: 数据可视化智能体",
            f"- 归档时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- XDR归档状态: {'已同步' if event.xdr_archived else '未同步'}",
            f"- 钉钉表格状态: {'已同步' if event.dingtalk_archived else '未同步'}",
            f"- 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ])
        return "\n".join(report)
    @classmethod
    def save_event_report(cls, event: Event, save_path: Optional[str] = None) -> str:
        """
        生成并保存事件报告到文件
        :param event: 完整事件对象
        :param save_path: 保存路径，默认使用./reports/{event_id}.md
        :return: 保存的文件路径
        """
        import os
        if not save_path:
            os.makedirs("./reports", exist_ok=True)
            save_path = f"./reports/{event.event_id}.md"

        content = cls.generate_event_report(event)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info("事件报告已保存", event_id=event.event_id, path=save_path)
        return save_path
