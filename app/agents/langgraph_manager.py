import yaml
import random
from app.utils.embeddings import find_similarity

class InterviewAgent:
    def __init__(self):
        with open("app/agents/interview_graph.yaml", "r") as f:
            self.graph = yaml.safe_load(f)

    def init_state(self):
        return {"phase": "start", "turns": 0, "score": 0}

    def process(self, text, state):
        phase = state.get("phase", "start")
        state["turns"] += 1

        # Move through graph
        if phase == "start":
            next_phase = self.graph[phase]["next"]
            question = random.choice(self.graph[next_phase]["questions"])
            state["phase"] = next_phase
            return question, state

        elif phase in ["behavioral", "technical", "system_design"]:
            # scoring:
            score = self.score_answer(text)
            state["score"] += score

            # next question or next phase:
            next_phase = self.graph[phase]["next"]
            if state["turns"] >= 2:
                state["phase"] = next_phase
                if next_phase != "end":
                    question = random.choice(self.graph[next_phase]["questions"])
                else:
                    question = self.graph["end"]["message"]
            else:
                question = random.choice(self.graph[phase]["questions"])

            return question, state

        elif phase == "end":
            return self.graph["end"]["message"], state

        return "Something went wrong.", state
    
    def score_answer(self, text):
        similarity = find_similarity(text)
        if similarity > 0.8:
            return 1
        else:
            return 0