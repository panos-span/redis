"""
This program is designed to manage meetings using Redis and MySQL databases.
It allows users to join and leave meetings, view the participants in a meeting,
view active meetings, end meetings, send chat messages, and view chat messages.
The program simulates these actions using random selections and user inputs.
The main logic of the program is broken down into several functions,
and a controller function is used to manage the state of active meetings.
"""

__authors__ = 'Panagiotis Spanakis, Emmanouil Dellatolas'

import json
import random
import threading
import time
from datetime import datetime

import pandas as pd
import redis

from mysql_handler import MySQLHandler
from objects import User, Meeting


# 1
def join_meeting(user, meeting, audience=None):
    """
    Allows a user to join a meeting if the meeting is active and the user is allowed to join.

    :param user: the user that wants to join a meeting
    :param meeting: the meeting that the user wants to join
    :param audience: the list of users that are allowed to join the meeting
    :return: true if the user joined the meeting, false otherwise
    """

    # Get meeting instance status from redis
    key = f'meeting_{meeting.meetingID}'
    if r.hget(key, 'isActive') is None:
        return False
    meeting_status = int(r.hget(key, 'isActive').decode('utf-8'))
    if not meeting_status:
        return False
    # If the user is allowed to join, add them to the participants list
    if audience is None or user.email in audience:
        r.sadd(f'participants_{meeting.meetingID}', user.userID)
        event = {
            'event_id': f'event_{(time.time())}',
            'user_id': user.userID,
            'event_type': 1,  # join_meeting
            'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        r.rpush('events_log', json.dumps(event, default=str))
        return True
    return False


# 2
def leave_meeting(user_id, meetingID, timeOut=False):
    """
    Allows a user to leave a meeting if the meeting is active and the user is part of the participants.

    :param user_id: the id of the user that wants to leave the meeting
    :param meetingID: the id of the meeting that the user wants to leave
    :param timeOut: true if the user left the meeting due to a timeout, false otherwise
    :return: true if the user left the meeting, false otherwise
    """
    key = f'meeting_{meetingID}'
    if r.hget(key, 'isActive') is None:
        return False
    meeting_status = int(r.hget(key, 'isActive').decode('utf-8'))
    if not meeting_status:
        return False
    if r.srem(f'participants_{meetingID}', user_id):
        # Check if the user left the meeting due to a timeout or not
        if timeOut:
            event_type = 3  # timeout
        else:
            event_type = 2  # leave_meeting
        event = {
            'event_id': f'event_{(time.time())}',
            'user_id': user_id,
            'event_type': event_type,
            'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        r.rpush('events_log', json.dumps(event, default=str))
        return True
    return False


# 3
def get_current_participants(meetingID):
    """
    Retrieves a list of the current participants in a meeting.

    :param meetingID: the id of the meeting
    :return: a list of the current participants in a meeting
    """
    return list(r.smembers(f'participants_{meetingID}'))


# 4
def get_active_meetings():
    """
    Retrieves a list of active meetings.

    :return: A list of active meetings.
    """
    active_meetings = {}
    for key in r.scan_iter('meeting_*'):
        # meeting_instance = json.loads(r.get(key))
        hash_table_contents = r.hgetall(key.decode("utf-8"))
        # Decode the byte strings returned by the hgetall method
        meeting = {k.decode("utf-8"): v.decode("utf-8") for k, v in hash_table_contents.items()}
        if meeting['isActive']:
            active_meetings[meeting['meetingID']] = meeting
    return active_meetings


# 5
def end_meeting(meetingID):
    """
    Ends a meeting by removing all participants from the meeting.

    :param meetingID: the id of the meeting that will be ended
    :return: nothing
    """
    participants = r.smembers(f'participants_{meetingID}')
    for user_id in participants:
        leave_meeting(user_id.decode('utf-8'), meetingID, True)
    # Clear the participants
    r.delete(f'participants_{meetingID}')


# 6
def post_chat_message(user_id, meetingID, message):
    """
    Posts a chat message to a meeting.

    :param user_id: the id of the user that posted the message
    :param meetingID: the id of the meeting that the message was posted to
    :param message: the message that was posted
    :return: nothing
    """
    chat_message = {
        'user_id': user_id,
        'message': message,
        'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    r.rpush(f'chat_{meetingID}', json.dumps(chat_message, default=str))


# 7
def get_chat_messages(meetingID):
    """
    Retrieves all chat messages from a meeting.

    :param meetingID: the id of the meeting
    :return: list of chat messages
    """
    messages = []
    for message in r.lrange(f'chat_{meetingID}', 0, -1):
        messages.append(json.loads(message))
    return messages


def get_join_timestamps(meetingID):
    """
    Retrieves the join timestamps of all participants in a meeting.

    :param meetingID: the id of the meeting
    :return: dictionary of join timestamps
    """
    join_timestamps = {}
    for event in r.lrange('events_log', 0, -1):
        event_data = json.loads(event)
        if event_data['event_type'] == 1 and event_data['user_id'] in r.smembers(
                f'participants_{meetingID}'):
            join_timestamps[event_data['user_id']] = event_data['timestamp']
    return join_timestamps


# 8
def get_active_meeting_timestamps():
    """
    Retrieves the join timestamps of all participants in all active meetings.

    :return: dictionary of join timestamps
    """
    active_meetings = get_active_meetings()
    active_meeting_timestamps = {}
    for meetingID in active_meetings:
        active_meeting_timestamps[meetingID] = get_join_timestamps(meetingID)
    return active_meeting_timestamps


# 9
def get_user_chat_messages(meetingID, user_id):
    """
    Retrieves all chat messages from a meeting for a specific user.

    :param meetingID: the id of the meeting
    :param user_id: the id of the user
    :return: list of chat messages
    """
    key = f'meeting_{meetingID}'
    if r.hget(key, 'isActive') is None:
        return False
    meeting_status = int(r.hget(key, 'isActive').decode('utf-8'))
    if not meeting_status:
        return False
    user_messages = []
    for message in r.lrange(f'chat_{meetingID}', 0, -1):
        message_data = json.loads(message)
        if message_data['user_id'] == user_id:
            user_messages.append(message_data)
    return user_messages


def generateRandomMessage():
    """
    Generates a random message for testing purposes.

    :return: random message
    """
    return "Random Message " + str(datetime.now())


def controller():
    """
    Controller method that runs every 60 seconds and checks for active meetings.
    In the start of the program this method instantiates the field isActive (True/False)
    for all the meetings in the redis database.

    :return: nothing
    """
    start_time = time.time()
    while main.is_alive():
        print(time.time() - start_time)
        for key in r.scan_iter('meeting_*'):
            hash_table_contents = r.hgetall(key.decode("utf-8"))
            # Decode the byte strings returned by the hgetall method
            meeting = {k.decode("utf-8"): v.decode("utf-8") for k, v in hash_table_contents.items()}
            meeting_inst = meeting_instances[meeting_instances['meetingID'] == int(meeting['meetingID'])]
            # Check for meeting instances where the current time is between the start and end time
            meeting_inst_active = meeting_inst[
                (meeting_inst['fromDatetime'] <= datetime.now()) & (meeting_inst['toDatetime'] >= datetime.now())]
            meeting_inst_active = json.loads(meeting_inst_active.to_json(orient='records', date_format='iso'))[0]

            if meeting_inst_active is not None:
                r.hset(f'meeting_{meeting_inst_active["meetingID"]}', 'isActive',
                       1)
                continue

            meetingID = int(meeting['meetingID'])
            # Check if meeting was active in the previous iteration
            if int(meeting['isActive']):
                end_meeting(meetingID)

            # If there are no active meeting instances, make the meeting inactive
            r.hset(f'meeting_{meetingID}', 'isActive',
                   0)
        time.sleep(60)


def str2datetime(date_str):
    """
    Converts a string to a datetime object.
    :param date_str: the string to be converted
    :return: datetime object
    """
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')


def initialise_columns():
    """
    Initialises the columns of the dataframes.
    :return: dataframe columns
    """
    user_columns = ['userID', 'email']
    meeting_columns = ['meetingID', 'is_public']
    meeting_audience_columns = ['meetingID', 'email']
    meeting_instance_columns = ['meetingID', 'orderID', 'fromDatetime', 'toDatetime']
    return user_columns, meeting_columns, meeting_audience_columns, meeting_instance_columns


def run():
    """
    Runs the program.

    :return: nothing
    """
    # Wait for the controller to run first
    time.sleep(1)
    start_time = time.time()
    while time.time() - start_time < 120:  # Run for 2 minutes
        # print(time.time() - start_time)
        choice = random.randint(0, 8)
        user_num = random.randint(0, 3)
        meeting_num = random.randint(1, 4)
        user = User(**users[user_num])
        meeting = Meeting(**meetings[meeting_num])
        if choice == 0:
            if meetings[meeting.meetingID]['is_public']:
                join_meeting(user, meeting)
            else:
                print('Meeting is private')
                print(join_meeting(user, meeting,
                                   meeting_audience[meeting_audience['meetingID'] == meeting_num]['email'].values))
        elif choice == 1:
            leave_meeting(user.userID, meeting.meetingID)
        elif choice == 2:
            get_current_participants(meeting.meetingID)
        elif choice == 3:
            get_active_meetings()
        elif choice == 4:
            end_meeting(meeting.meetingID)
        elif choice == 5:
            post_chat_message(user.userID, meeting.meetingID,
                              generateRandomMessage())
        elif choice == 6:
            get_chat_messages(meeting.meetingID)
        elif choice == 7:
            get_join_timestamps(meeting.meetingID)
        elif choice == 8:
            get_user_chat_messages(meeting.meetingID, user.userID)
        time.sleep(1)  # Sleep for 1 second


def migrateEventsLog():
    """
    Migrates the events_log from redis to mysql.

    :return: nothing
    """
    # Load the event_log data from redis to mysql
    while r.llen('events_log') > 0:
        # Pop a JSON document from the Redis list
        json_document = r.lpop('events_log').decode("utf-8")
        event_log = json.loads(json_document)
        sql_query = "INSERT INTO events_log (event_id, userID, event_type, timestamp) VALUES (%s, %s, %s, %s)"
        values = (
            event_log['event_id'], event_log['user_id'], event_log['event_type'],
            str2datetime(event_log['timestamp']))
        db.execute(sql_query, values)


if __name__ == '__main__':
    """
    Main method.
    """
    # Connect to redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    password = input('Enter mysql password: ')

    # Load dataframe columns
    user_columns, meeting_columns, meeting_audience_columns, meeting_instance_columns = initialise_columns()

    # Connect to mysql
    db = MySQLHandler(password=password)
    db.connect()

    # Load data from mysql to pandas dataframes
    users = pd.DataFrame(db.select('SELECT userID,email FROM users'), columns=user_columns)
    meetings = pd.DataFrame(db.select('SELECT meetingID,isPublic FROM meetings'), columns=meeting_columns)
    meeting_instances = pd.DataFrame(db.select('SELECT * FROM meeting_instances'), columns=meeting_instance_columns)
    meeting_audience = pd.DataFrame(db.select('SELECT * FROM meeting_audience'), columns=meeting_audience_columns)

    # Convert the dataframes to json
    users = json.loads(users.to_json(orient='records'))
    meetings = json.loads(meetings.to_json(orient='records'))

    # Insert meetings to redis
    with r.pipeline() as pipe:
        for meeting in meetings:
            for field, value in meeting.items():
                pipe.hset(f'meeting_{meeting["meetingID"]}', field, value)
        pipe.execute()

    # Make keys of the meetings dictionary the meetingID for faster access
    meetings = {meeting['meetingID']: meeting for meeting in meetings}

    # Start the continuous thread
    main = threading.Thread(target=run)
    main.start()

    # Start the periodic thread (scheduler)
    scheduler = threading.Thread(target=controller)
    scheduler.start()

    # Wait for the continuous thread to finish
    main.join()

    # Terminate the scheduler after the continuous thread is done
    scheduler.join(timeout=1)  # Give it a chance to finish the current iteration

    # Migrate the events_log from redis to mysql
    migrateEventsLog()

    # Clear the participants sets if they exist
    for key in r.scan_iter('participants_*'):
        r.delete(key.decode("utf-8"))

    # Close the connection to mysql
    db.close()
