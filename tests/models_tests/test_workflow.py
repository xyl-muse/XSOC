import pytest
from src.models.workflow import WorkflowState, WorkflowStatusEnum
def test_workflow_initial_state():
    """测试工作流初始状态"""
    state = WorkflowState(event_id="test-event-123")
    assert state.current_status == WorkflowStatusEnum.PENDING_JUDGE
    assert state.event_id == "test-event-123"
def test_valid_transitions():
    """测试合法的状态流转"""
    state = WorkflowState(event_id="test-event-123")
    # 待研判 → 待溯源（真实事件）
    state.transition(WorkflowStatusEnum.PENDING_TRACE)
    assert state.current_status == WorkflowStatusEnum.PENDING_TRACE
    # 待溯源 → 待处置
    state.transition(WorkflowStatusEnum.PENDING_RESPONSE)
    assert state.current_status == WorkflowStatusEnum.PENDING_RESPONSE
    # 待处置 → 待人工确认
    state.transition(WorkflowStatusEnum.PENDING_HITL_CONFIRM)
    assert state.current_status == WorkflowStatusEnum.PENDING_HITL_CONFIRM
    # 待人工确认 → 待处置（确认通过）
    state.transition(WorkflowStatusEnum.PENDING_RESPONSE)
    assert state.current_status == WorkflowStatusEnum.PENDING_RESPONSE
    # 待处置 → 待归档
    state.transition(WorkflowStatusEnum.PENDING_ARCHIVE)
    assert state.current_status == WorkflowStatusEnum.PENDING_ARCHIVE
    # 待归档 → 已完成
    state.transition(WorkflowStatusEnum.COMPLETED)
    assert state.current_status == WorkflowStatusEnum.COMPLETED
def test_invalid_transition():
    """测试非法状态流转抛出异常"""
    state = WorkflowState(event_id="test-event-123")
    # 待研判不能直接到待处置
    with pytest.raises(ValueError, match="非法状态流转"):
        state.transition(WorkflowStatusEnum.PENDING_RESPONSE)
    # 已完成不能再流转
    state.current_status = WorkflowStatusEnum.COMPLETED
    with pytest.raises(ValueError, match="非法状态流转"):
        state.transition(WorkflowStatusEnum.PENDING_ARCHIVE)
def test_suspend_transition():
    """测试挂起状态流转"""
    state = WorkflowState(event_id="test-event-123")
    # 挂起必须提供错误信息
    with pytest.raises(ValueError, match="状态设置为挂起时必须提供错误信息"):
        state.transition(WorkflowStatusEnum.SUSPENDED)
    # 正常挂起
    state.transition(WorkflowStatusEnum.SUSPENDED, error_msg="工具调用失败，等待人工处理")
    assert state.current_status == WorkflowStatusEnum.SUSPENDED
    assert state.error_msg == "工具调用失败，等待人工处理"
    # 从挂起恢复到待研判
    state.transition(WorkflowStatusEnum.PENDING_JUDGE)
    assert state.current_status == WorkflowStatusEnum.PENDING_JUDGE
def test_hitl_check():
    """测试HITL阈值检查"""
    state = WorkflowState(event_id="test-event-123")
    # 默认阈值7分
    assert state.check_hitl_required(6) is False
    assert state.check_hitl_required(7) is True
    assert state.check_hitl_required(9) is True
