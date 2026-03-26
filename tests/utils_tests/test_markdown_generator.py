from datetime import datetime
from src.utils.markdown_generator import MarkdownGenerator
from src.models.event import Event
from src.models.alert import Alert, AlertSourceEnum
def test_generate_event_report():
    """测试生成事件报告"""
    # 创建测试告警
    alert = Alert(
        alert_id="ALERT-20260326-00001",
        alert_type="暴力破解",
        src_ip="192.168.1.100",
        dst_ip="10.0.0.5",
        dst_port=22,
        alert_time="2026-03-26T12:00:00+08:00",
        severity="高",
        raw_content="SSH暴力破解尝试127次",
        source=AlertSourceEnum.XDR
    )
    # 创建测试事件（误报场景）
    event = Event(
        event_name="SSH暴力破解告警",
        event_type="暴力破解",
        alert=alert,
        is_real_event=False,
        judge_time=datetime.now(),
        judge_evidence="源IP为内部运维IP，属于正常操作",
        judge_tool_calls=["微步情报查询", "资产信息查询"]
    )
    report = MarkdownGenerator.generate_event_report(event)
    # 验证报告包含关键信息
    assert "# 安全事件报告：SSH暴力破解告警" in report
    assert "事件ID: `EVENT-" in report
    assert "告警ID: `ALERT-20260326-00001`" in report
    assert "事件状态: 误报" in report
    assert "研判结论: 误报，事件结束" in report
def test_generate_real_event_report():
    """测试生成真实事件的完整报告"""
    alert = Alert(
        alert_id="ALERT-20260326-00002",
        alert_type="挖矿行为",
        src_ip="192.168.1.200",
        alert_time="2026-03-26T14:00:00+08:00",
        severity="高",
        raw_content="检测到挖矿进程",
        source=AlertSourceEnum.XDR
    )
    event = Event(
        event_name="服务器挖矿事件",
        event_type="挖矿",
        alert=alert,
        is_real_event=True,
        judge_time=datetime.now(),
        judge_evidence="微步情报确认源IP为恶意IP，存在挖矿行为",
        trace_time=datetime.now(),
        trace_attack_chain="端口扫描→弱口令爆破→植入挖矿程序→运行挖矿进程",
        trace_impact_scope="影响服务器192.168.1.200，未扩散",
        trace_root_cause="SSH弱口令被爆破",
        risk_score=8,
        hitl_required=True,
        hitl_confirmed=True,
        hitl_confirmed_by="安全管理员",
        response_time=datetime.now(),
        response_actions=["封禁源IP", "终止挖矿进程", "修改弱口令"],
        response_result="处置完成，风险已闭环",
        xdr_archived=True,
        dingtalk_archived=True
    )
    report = MarkdownGenerator.generate_event_report(event)
    assert "风险评分: 8/10" in report
    assert "事件状态: 真实事件" in report
    assert "## 溯源分析结果" in report
    assert "## 风险处置记录" in report
    assert "HITL人工确认: 已通过" in report
    assert "攻击链分析: 端口扫描→弱口令爆破→植入挖矿程序→运行挖矿进程" in report
