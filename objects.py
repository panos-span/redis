from datetime import datetime


class User:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('username')
        self.age = kwargs.get('age')
        self.gender = kwargs.get('gender')
        self.email = kwargs.get('email')

    def __getattr__(self, item):
        return self.__dict__[item]


class Meeting:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.isPublic = kwargs.get('isPublic')

    def __getattr__(self, item):
        return self.__dict__[item]


class MeetingInstance:

    def __init__(self, **kwargs):
        self.isActive = None
        self.meeting_id = kwargs.get('meeting_id')
        self.order_id = kwargs.get('order_id')
        self.fromDatetime = kwargs.get('fromDatetime')
        self.toDatetime = kwargs.get('toDatetime')
        self.checkActivity()

    def __getattr__(self, item):
        return self.__dict__[item]

    def checkActivity(self):
        self.isActive = self.fromDatetime < datetime.now() < self.toDatetime


class EventLog:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.user_id = kwargs.get('user_id')
        self.event_type = kwargs.get('event_type')  # 1 if user joined, 2 if user left , 3 if user timed out
        self.timestamp = kwargs.get('timestamp')

    def __getattr__(self, item):
        return self.__dict__[item]
