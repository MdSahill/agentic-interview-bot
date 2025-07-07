class InterviewAgent:
    def __init__(self):
        pass

    def process(self, text, state):
        # dummy agent logic
        phase = state.get("phase", "behavioral")
        reply = f"(phase: {phase}) Thanks for your answer: {text}"
        state["turns"] += 1
        if state["turns"] > 2 and phase == "behavioral":
            state["phase"] = "technical"
        return reply, state

