"""باب الترابط — Inter-proposition linking (Articles 45–47).

Pure functions that link propositions via particles and validate
the resulting links.
"""

from __future__ import annotations

from arabic_engine.core.enums import InterPropositionLinkType
from arabic_engine.core.types import CompositionProposition, InterPropositionLink

# Known linking particles → link types
_PARTICLE_MAP: dict[str, InterPropositionLinkType] = {
    "و": InterPropositionLinkType.CONJUNCTION,
    "ف": InterPropositionLinkType.CONJUNCTION,
    "ثم": InterPropositionLinkType.TEMPORAL,
    "إذا": InterPropositionLinkType.CONDITION,
    "إن": InterPropositionLinkType.CONDITION,
    "لو": InterPropositionLinkType.CONDITION,
    "لأن": InterPropositionLinkType.CAUSATION,
    "بسبب": InterPropositionLinkType.CAUSATION,
    "لكن": InterPropositionLinkType.ADVERSATIVE,
    "بل": InterPropositionLinkType.ADVERSATIVE,
    "قبل": InterPropositionLinkType.TEMPORAL,
    "بعد": InterPropositionLinkType.TEMPORAL,
}


def link_propositions(
    source: CompositionProposition,
    target: CompositionProposition,
    particle: str,
) -> InterPropositionLink:
    """Link two propositions via a particle.

    Parameters
    ----------
    source:
        The source proposition.
    target:
        The target proposition.
    particle:
        The linking particle (e.g. و، لأن، إذا).
    """
    link_type = _PARTICLE_MAP.get(particle, InterPropositionLinkType.OTHER)
    valid = source.closed and target.closed

    return InterPropositionLink(
        source_prop_id=source.proposition_id,
        target_prop_id=target.proposition_id,
        link_type=link_type,
        particle=particle,
        valid=valid,
    )


def validate_link(link: InterPropositionLink) -> bool:
    """Return whether an inter-proposition link is valid."""
    return link.valid and link.particle != ""
