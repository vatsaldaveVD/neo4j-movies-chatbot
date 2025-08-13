from graph import create_session, add_message


class ChatAgent:
    def __init__(self, session_id=None):
        self.session_id = session_id or create_session()

    def add_user_message(self, content):
        add_message(self.session_id, "human", content)

    def add_bot_message(self, content):
        add_message(self.session_id, "ai", content)
