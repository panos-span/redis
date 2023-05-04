class User:
    def __init__(self, **kwargs):
        self.userID = kwargs.get('userID')
        self.name = kwargs.get('username')
        self.age = kwargs.get('age')
        self.gender = kwargs.get('gender')
        self.email = kwargs.get('email')

    def __getattr__(self, item):
        return self.__dict__[item]


class Meeting:

    def __init__(self, **kwargs):
        self.meetingID = kwargs.get('meetingID')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.isPublic = kwargs.get('isPublic')

    def __getattr__(self, item):
        return self.__dict__[item]
