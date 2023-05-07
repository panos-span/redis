__authors__ = 'Panagiotis Spanakis, Emmanouil Dellatolas'

class User:
    """
    User object

    Attributes:
        userID: int
        name: str
        age: int
        gender: str
        email: str
    """

    def __init__(self, **kwargs):
        """
        Constructor of the class

        :param kwargs: dictionary of the attributes
        """
        self.userID: int = kwargs.get('userID')
        self.name = kwargs.get('username')
        self.age: int = kwargs.get('age')
        self.gender = kwargs.get('gender')
        self.email = kwargs.get('email')

    def __getattr__(self, item):
        return self.__dict__[item]


class Meeting:
    """
    Meeting object

    Attributes:
        meetingID: int
        title: str
        description: str
        isPublic: bool
    """

    def __init__(self, **kwargs):
        """
        Constructor of the class

        :param kwargs: dictionary of the attributes
        """
        self.meetingID = kwargs.get('meetingID')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.isPublic = kwargs.get('isPublic')

    def __getattr__(self, item):
        return self.__dict__[item]
