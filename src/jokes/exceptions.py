class JokeBaseException(Exception):
    def __init__(self, msg=''):
        self.msg = msg


class JokeBadUserException(JokeBaseException):
    pass


class JokeBadJokeException(JokeBaseException):
    pass
