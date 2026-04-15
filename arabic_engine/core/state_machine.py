"""Generic state-machine engine used by all layer machines.

Each linguistic layer (sound, haraka, syllable, root-rank, transform,
judgment) is modelled as a deterministic finite-state machine with
*numeric guards* and *priority-ordered transitions*.  This module
provides the reusable infrastructure so that individual machines only
need to declare their configuration tables.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
)

# ── transition definition ───────────────────────────────────────────


@dataclass(frozen=True)
class StateTransition:
    """A single row in a state-machine transition table.

    Parameters
    ----------
    source:
        Current state (an Enum member).
    event:
        Event that triggers this transition (an Enum member).
    target:
        State to move to if the guard passes.
    guard:
        Optional callable ``(context) → bool``.  When *None* the
        transition is unconditional.
    guard_name:
        Human-readable label for the guard (used in traces / YAML).
    threshold:
        The numeric threshold the guard checks against.
    priority:
        Lower number = higher priority.  When multiple transitions
        match the same ``(source, event)`` pair, the one with the
        lowest ``priority`` value fires first.
    """

    source: Enum
    event: Enum
    target: Enum
    guard: Optional[Callable[[Dict[str, Any]], bool]] = None
    guard_name: str = ""
    threshold: float = 0.0
    priority: int = 1


# ── machine configuration ──────────────────────────────────────────


@dataclass(frozen=True)
class StateMachineConfig:
    """Declarative specification of a state machine.

    Parameters
    ----------
    name:
        Machine name (e.g. ``"SoundMachine"``).
    initial_state:
        The starting state.
    transitions:
        Ordered sequence of :class:`StateTransition` rows.
    reject_states:
        States that signify a terminal rejection.
    accept_states:
        States that signify a terminal acceptance / output.
    wildcard_source:
        Optional sentinel value representing "any state" transitions
        (e.g. global rejection transitions that can fire from anywhere).
    """

    name: str
    initial_state: Enum
    transitions: Tuple[StateTransition, ...] = ()
    reject_states: FrozenSet[Enum] = field(default_factory=frozenset)
    accept_states: FrozenSet[Enum] = field(default_factory=frozenset)
    wildcard_source: Optional[str] = "ANY"


# Workaround: frozen dataclass cannot use mutable default for FrozenSet
# with field() — redefine with __post_init__ is not allowed on frozen.
# Instead we use a Tuple and convert at usage time.  But the above
# works because ``frozenset`` is already immutable.

from typing import FrozenSet  # noqa: E402 (already imported but re-stated for clarity)

# ── state-machine runtime ──────────────────────────────────────────


@dataclass
class MachineSnapshot:
    """Mutable snapshot of a running state machine."""

    current_state: Enum
    history: List[Tuple[Enum, Enum, Enum]] = field(default_factory=list)
    """List of (source, event, target) tuples for every fired transition."""
    context: Dict[str, Any] = field(default_factory=dict)


class StateMachine:
    """Priority-guarded deterministic state machine.

    Usage::

        machine = StateMachine(config)
        snap = machine.start(initial_context)
        snap = machine.send(snap, event, context_update)
    """

    def __init__(self, config: StateMachineConfig) -> None:
        self._config = config
        # Pre-index transitions by (source,) for O(1) lookup.
        self._by_source: Dict[Enum, List[StateTransition]] = {}
        self._wildcards: List[StateTransition] = []
        for t in config.transitions:
            # Check for wildcard source
            if isinstance(t.source, str) and t.source == config.wildcard_source:
                self._wildcards.append(t)
            else:
                self._by_source.setdefault(t.source, []).append(t)
        # Sort each bucket by priority (ascending = highest priority first).
        for bucket in self._by_source.values():
            bucket.sort(key=lambda tr: tr.priority)
        self._wildcards.sort(key=lambda tr: tr.priority)

    # -- public properties -------------------------------------------

    @property
    def config(self) -> StateMachineConfig:
        return self._config

    @property
    def name(self) -> str:
        return self._config.name

    # -- lifecycle ---------------------------------------------------

    def start(
        self,
        context: Optional[Dict[str, Any]] = None,
    ) -> MachineSnapshot:
        """Create a fresh snapshot at the initial state."""
        return MachineSnapshot(
            current_state=self._config.initial_state,
            context=dict(context) if context else {},
        )

    def send(
        self,
        snapshot: MachineSnapshot,
        event: Enum,
        context_update: Optional[Dict[str, Any]] = None,
    ) -> MachineSnapshot:
        """Attempt to transition *snapshot* via *event*.

        If no transition matches (guard fails or event not applicable),
        the snapshot is returned **unchanged**.

        Parameters
        ----------
        snapshot:
            Current machine snapshot (mutated in-place for efficiency).
        event:
            The event to process.
        context_update:
            Optional key/value pairs merged into the context before
            guard evaluation.

        Returns
        -------
        MachineSnapshot
            The (possibly advanced) snapshot.
        """
        if context_update:
            snapshot.context.update(context_update)

        # Terminal states do not accept further events.
        if self.is_terminal(snapshot.current_state):
            return snapshot

        tr = self.select_transition(snapshot.current_state, event, snapshot.context)
        if tr is not None:
            snapshot.history.append((tr.source, tr.event, tr.target))
            snapshot.current_state = tr.target
        return snapshot

    def run_to_completion(
        self,
        events: Sequence[Tuple[Enum, Optional[Dict[str, Any]]]],
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> MachineSnapshot:
        """Feed a sequence of ``(event, context_update)`` pairs.

        Stops early if a terminal state is reached.
        """
        snap = self.start(initial_context)
        for event, ctx in events:
            snap = self.send(snap, event, ctx)
            if self.is_terminal(snap.current_state):
                break
        return snap

    # -- query helpers -----------------------------------------------

    def is_terminal(self, state: Enum) -> bool:
        """Return True if *state* is an accept or reject terminal."""
        return (
            state in self._config.accept_states
            or state in self._config.reject_states
        )

    def is_accepted(self, state: Enum) -> bool:
        return state in self._config.accept_states

    def is_rejected(self, state: Enum) -> bool:
        return state in self._config.reject_states

    def select_transition(
        self,
        state: Enum,
        event: Enum,
        context: Dict[str, Any],
    ) -> Optional[StateTransition]:
        """Find the highest-priority matching transition.

        Specific-source transitions are evaluated before wildcard ones.
        Within each group, transitions are ordered by ascending
        ``priority`` (lower number = higher priority).
        """
        candidates = self._by_source.get(state, []) + self._wildcards
        for tr in candidates:
            if tr.event != event:
                continue
            if tr.guard is not None and not tr.guard(context):
                continue
            return tr
        return None

    # -- serialisation helpers ---------------------------------------

    def transition_table(self) -> List[Dict[str, Any]]:
        """Return the full transition table as a list of dicts."""
        rows: List[Dict[str, Any]] = []
        for t in self._config.transitions:
            rows.append(
                {
                    "source": t.source.name if isinstance(t.source, Enum) else t.source,
                    "event": t.event.name if isinstance(t.event, Enum) else t.event,
                    "target": t.target.name if isinstance(t.target, Enum) else t.target,
                    "guard": t.guard_name,
                    "threshold": t.threshold,
                    "priority": t.priority,
                }
            )
        return rows
