"""Tests for the generic state-machine engine."""

from __future__ import annotations

from enum import Enum, auto
from typing import Any, Dict

from arabic_engine.core.state_machine import (
    StateMachine,
    StateMachineConfig,
    StateTransition,
)

# ── tiny test machine ───────────────────────────────────────────────


class St(Enum):
    A = auto()
    B = auto()
    C = auto()
    FAIL = auto()


class Ev(Enum):
    GO = auto()
    SKIP = auto()
    DIE = auto()


def _guard_ok(ctx: Dict[str, Any]) -> bool:
    return ctx.get("ok", False)


def _guard_fail(ctx: Dict[str, Any]) -> bool:
    return ctx.get("fail", False)


TINY_CONFIG = StateMachineConfig(
    name="Tiny",
    initial_state=St.A,
    transitions=(
        StateTransition(St.A, Ev.GO, St.B, guard=_guard_ok, guard_name="ok", priority=1),
        StateTransition(St.B, Ev.GO, St.C, priority=1),
        StateTransition(St.A, Ev.DIE, St.FAIL, guard=_guard_fail, guard_name="fail", priority=0),
        StateTransition(St.B, Ev.DIE, St.FAIL, guard=_guard_fail, guard_name="fail", priority=0),
    ),
    accept_states=frozenset({St.C}),
    reject_states=frozenset({St.FAIL}),
)


# ── tests ───────────────────────────────────────────────────────────


class TestStateMachineBasics:
    def test_initial_state(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.start()
        assert snap.current_state == St.A

    def test_guard_blocks_transition(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.start({"ok": False})
        snap = sm.send(snap, Ev.GO)
        assert snap.current_state == St.A  # did not advance

    def test_guard_allows_transition(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.start({"ok": True})
        snap = sm.send(snap, Ev.GO)
        assert snap.current_state == St.B

    def test_unconditional_transition(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.start({"ok": True})
        snap = sm.send(snap, Ev.GO)  # A→B
        snap = sm.send(snap, Ev.GO)  # B→C (no guard)
        assert snap.current_state == St.C

    def test_terminal_state_no_further_events(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.start({"ok": True})
        snap = sm.send(snap, Ev.GO)
        snap = sm.send(snap, Ev.GO)  # now at C (accept)
        assert sm.is_accepted(snap.current_state)
        snap = sm.send(snap, Ev.GO)  # should stay at C
        assert snap.current_state == St.C

    def test_reject_state(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.start({"ok": True, "fail": True})
        snap = sm.send(snap, Ev.GO)  # A→B (ok guard passes)
        snap = sm.send(snap, Ev.DIE)  # B→FAIL
        assert sm.is_rejected(snap.current_state)

    def test_is_terminal(self):
        sm = StateMachine(TINY_CONFIG)
        assert sm.is_terminal(St.C)
        assert sm.is_terminal(St.FAIL)
        assert not sm.is_terminal(St.A)

    def test_run_to_completion_accepts(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.run_to_completion(
            [(Ev.GO, None), (Ev.GO, None)],
            initial_context={"ok": True},
        )
        assert snap.current_state == St.C
        assert len(snap.history) == 2

    def test_run_to_completion_stops_at_reject(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.run_to_completion(
            [(Ev.DIE, None), (Ev.GO, None)],
            initial_context={"fail": True},
        )
        assert snap.current_state == St.FAIL
        assert len(snap.history) == 1  # stopped after first

    def test_context_update_on_send(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.start()
        snap = sm.send(snap, Ev.GO, {"ok": True})
        assert snap.current_state == St.B

    def test_history_records_transitions(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.start({"ok": True})
        snap = sm.send(snap, Ev.GO)
        snap = sm.send(snap, Ev.GO)
        assert snap.history == [(St.A, Ev.GO, St.B), (St.B, Ev.GO, St.C)]

    def test_transition_table_serialisation(self):
        sm = StateMachine(TINY_CONFIG)
        table = sm.transition_table()
        assert len(table) == 4
        assert table[0]["source"] == "A"
        assert table[0]["event"] == "GO"

    def test_unmatched_event_is_noop(self):
        sm = StateMachine(TINY_CONFIG)
        snap = sm.start()
        snap = sm.send(snap, Ev.SKIP)  # no transitions for SKIP from A
        assert snap.current_state == St.A


class TestPriorityOrdering:
    """Verify that lower-priority-number transitions fire first."""

    def test_low_priority_wins(self):
        """When two transitions match the same (state, event), the one
        with the lower priority number should fire."""

        class X(Enum):
            START = auto()
            LOW = auto()
            HIGH = auto()

        cfg = StateMachineConfig(
            name="Priority",
            initial_state=X.START,
            transitions=(
                StateTransition(X.START, Ev.GO, X.HIGH, priority=2),
                StateTransition(X.START, Ev.GO, X.LOW, priority=1),
            ),
            accept_states=frozenset({X.LOW, X.HIGH}),
        )
        sm = StateMachine(cfg)
        snap = sm.start()
        snap = sm.send(snap, Ev.GO)
        assert snap.current_state == X.LOW  # priority=1 wins


class TestSelectTransition:
    def test_returns_none_when_no_match(self):
        sm = StateMachine(TINY_CONFIG)
        assert sm.select_transition(St.A, Ev.SKIP, {}) is None

    def test_returns_transition_when_guard_passes(self):
        sm = StateMachine(TINY_CONFIG)
        tr = sm.select_transition(St.A, Ev.GO, {"ok": True})
        assert tr is not None
        assert tr.target == St.B
