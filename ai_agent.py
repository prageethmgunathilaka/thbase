class EchoAgent:
    def __init__(self):
        self.name = "Echo Agent"
    
    def respond(self, user_input):
        """
        Simply echoes back the user's input
        """
        return f"{self.name} says: {user_input}" 