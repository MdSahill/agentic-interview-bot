class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def init_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = {"phase": "behavioral", "turns": 0}
        return self.sessions[session_id]

    def update_session(self, session_id, state):
        self.sessions[session_id] = state

    def clear_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
