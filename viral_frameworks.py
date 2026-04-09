"""
═══════════════════════════════════════════════════════════════
 VIRAL FRAMEWORKS — THE INTELLIGENCE OS
 
 Codified versions of top-tier content strategist frameworks.
 Frameworks: Alex Hormozi (Hook/Retain/Reward), MrBeast (Pacing).
═══════════════════════════════════════════════════════════════
"""

VIRAL_FRAMEWORKS = {
    "hormozi_unit": {
        "name": "The Hormozi 'Content Unit'",
        "philosophy": "Self-contained value, zero fluff, extreme hook focus.",
        "structure": [
            "HOOK: Stop the scroll with a contrarian or high-stakes statement.",
            "PROBLEM: Call out a specific pain point or desire.",
            "INSIGHT: Share a 'wisdom' piece—a story of what worked, not just advice.",
            "PAYOFF: A clear, actionable reward or transformation vision."
        ],
        "tone": "Authoritative, fast-paced, high-conviction."
    },
    "mrbeast_momentum": {
        "name": "MrBeast Momentum",
        "philosophy": "Audience > Algorithm. Relentless pacing and open loops.",
        "structure": [
            "HOOK: Visual and narrative promise (Setting the stakes).",
            "RE-ENGAGEMENT: Constant pattern interrupts (new info every 3-5s).",
            "OPEN LOOP: Start a challenge or question that only resolves at the end.",
            "PROGRESSION: Fast-forward through friction, only show the 'big wins'."
        ],
        "tone": "Exciting, high-energy, narrative-driven."
    },
    "executive_luxury": {
        "name": "Royalle Executive",
        "philosophy": "Status signaling and premium lifestyle evolution.",
        "structure": [
            "HOOK: Aesthetic pattern interrupt (High-status visual).",
            "ASPIRATION: Showing the 'after' state first.",
            "INTEL: The 'gatekept' secret to elite results.",
            "COMMAND: A direct, high-value CTA (Join the elite)."
        ],
        "tone": "Sleek, sophisticated, premium, exclusive."
    }
}

def get_strategy_prompt(strategy_key):
    strategy = VIRAL_FRAMEWORKS.get(strategy_key, VIRAL_FRAMEWORKS["hormozi_unit"])
    return f"""
    Using the '{strategy['name']}' framework:
    - Philosophy: {strategy['philosophy']}
    - Structure: {', '.join(strategy['structure'])}
    - Tone: {strategy['tone']}
    """
