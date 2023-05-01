from datetime import datetime


class User:
    def __init__(self, **kwargs):
        self.id = kwargs.get('userID')
        self.name = kwargs.get('username')
        self.age = kwargs.get('age')
        self.gender = kwargs.get('gender')
        self.email = kwargs.get('email')

    def __getattr__(self, item):
        return self.__dict__[item]


class Meeting:

    def __init__(self, **kwargs):
        self.id = kwargs.get('meetingID')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.isPublic = kwargs.get('isPublic')

    def __getattr__(self, item):
        return self.__dict__[item]


class MeetingInstance:

    def __init__(self, **kwargs):
        self.isActive = None
        self.meeting_id: int = kwargs.get('meetingID')
        self.order_id: int = kwargs.get('orderID')
        self.fromDatetime: datetime = self.str2datetime(kwargs.get('fromDatetime'))
        self.toDatetime: datetime = self.str2datetime(kwargs.get('toDatetime'))
        self.checkActivity()

    def str2datetime(self, date_str):
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

    def __getattr__(self, item):
        return self.__dict__[item]

    def checkActivity(self):
        self.isActive = self.fromDatetime < datetime.now() < self.toDatetime


class EventLog:

    def __init__(self, **kwargs):
        self.id = kwargs.get('event_id')
        self.user_id = kwargs.get('userID')
        self.event_type = kwargs.get('event_type')  # 1 if user joined, 2 if user left , 3 if user timed out
        self.timestamp = kwargs.get('timestamp')

    def __getattr__(self, item):
        return self.__dict__[item]
