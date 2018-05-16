from sqlalchemy import create_engine


class Engine:

    def __init__(self):
            self.engine = create_engine('sqlite:///batoru.db')

    def get_engine(self):
        return self.engine
