window.SPEAKER_SCRIPT = Object.freeze({
  ...window.SPEAKER_SCRIPT,
  "safe1": "This is the running semantic-exchange case. One checker proves the index is non-negative. Another proves the loop upper bound. A third knows whether the array extent is stable here. The optimizer should ask for the SafeIndex fact, not know every producer implementation.",
  "safe2": "Now the bounds-check specializer consumes that shared meaning.\n\nIt asks one proposition: can we establish SafeIndex(a, i) here? If the semantic layer can combine current-valid evidence into zero is less than or equal to i, and i is less than Length(a), then the checked load can be specialized into an unchecked load.\n\nThis is the payoff: independently produced knowledge enables a global optimization. But it is still conservative. If the evidence is missing, stale, contradictory, or for the wrong path or revision, the specialization must not happen."
});
