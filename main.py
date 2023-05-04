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
    # Get meeting instance status from redis
    key = f'meeting_{meeting.meetingID}'
    if r.hget(key, 'isActive') is None:
        return False
    meeting_status = int(r.hget(key, 'isActive').decode('utf-8'))
    if not meeting_status:
        return False
    if audience is None or user.email in audience:
        r.sadd(f'participants_{meeting.meetingID}', user.userID)
        event = {
            'event_id': f'event_{(time.time())}',
            'user_id': user.userID,
            'event_type': 1,  # join_meeting
            'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        print(event)
        r.rpush('events_log', json.dumps(event, default=str))
        return True
    return False


# 2
def leave_meeting(user_id, meetingID):
    key = f'meeting_{meetingID}'
    if r.hget(key, 'isActive') is None:
        return False
    meeting_status = int(r.hget(key, 'isActive').decode('utf-8'))
    if not meeting_status:
        return False
    if r.srem(f'participants_{meetingID}', user_id):
        event = {
            'event_id': f'event_{(time.time())}',
            'user_id': user_id,
            'event_type': 2,  # leave_meeting
            'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        r.rpush('events_log', json.dumps(event, default=str))
        return True
    return False


# 3
def get_current_participants(meetingID):
    return list(r.smembers(f'participants_{meetingID}'))


# 4
def get_active_meetings():
    active_meetings = {}
    for key in r.scan_iter('meeting_*'):
        # meeting_instance = json.loads(r.get(key))
        hash_table_contents = r.hgetall(key.decode("utf-8"))
        # Decode the byte strings returned by the hgetall method
        meeting = {k.decode("utf-8"): v.decode("utf-8") for k, v in hash_table_contents.items()}
        print(meeting)
        if meeting['isActive']:
            active_meetings[meeting['meetingID']] = meeting
    return active_meetings


# 5
def end_meeting(meetingID):
    participants = r.smembers(f'participants_{meetingID}')
    for user_id in participants:
        leave_meeting(user_id.decode('utf-8'), meetingID)
    r.delete(f'meeting_{meetingID}')


# 6
def post_chat_message(user_id, meetingID, message):
    chat_message = {
        'user_id': user_id,
        'message': message,
        'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    r.rpush(f'chat_{meetingID}', json.dumps(chat_message, default=str))


# 7
def get_chat_messages(meetingID):
    messages = []
    for message in r.lrange(f'chat_{meetingID}', 0, -1):
        messages.append(json.loads(message))
    return messages


def get_join_timestamps(meetingID):
    join_timestamps = {}
    for event in r.lrange('events_log', 0, -1):
        event_data = json.loads(event)
        if event_data['event_type'] == 1 and event_data['user_id'] in r.smembers(
                f'participants_{meetingID}'):
            join_timestamps[event_data['user_id']] = event_data['timestamp']
    return join_timestamps


# 8
def get_active_meeting_timestamps():
    active_meetings = get_active_meetings()
    active_meeting_timestamps = {}
    for meetingID in active_meetings:
        active_meeting_timestamps[meetingID] = get_join_timestamps(meetingID)
    return active_meeting_timestamps


# 9
def get_user_chat_messages(meetingID, user_id):
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
    return "Random Message " + str(datetime.now())


def controller():
    start_time = time.time()
    while main.is_alive():
        print(time.time() - start_time)
        for key in r.scan_iter('meeting_*'):
            # meeting_instance = json.loads(r.get(key))
            hash_table_contents = r.hgetall(key.decode("utf-8"))
            # Decode the byte strings returned by the hgetall method
            meeting = {k.decode("utf-8"): v.decode("utf-8") for k, v in hash_table_contents.items()}
            print(meeting)
            print(meeting['meetingID'])
            meeting_inst = json.loads(
                meeting_instances[meeting_instances['meetingID'] == int(meeting['meetingID'])].
                to_json(orient='records', date_format='iso'))
            isOnceActive = False
            for meeting_instance in meeting_inst:
                # Activate meeting if it is not active
                print("!"*50)
                print(str2datetime(meeting_instance['fromDatetime']))
                current_datetime = datetime.now()
                formatted_datetime = str(current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
                print(formatted_datetime)
                print(str2datetime(meeting_instance['toDatetime']))
                print("!"*50)
                if str2datetime(meeting_instance['fromDatetime']) <= str2datetime(formatted_datetime) <= str2datetime(
                        meeting_instance['toDatetime']):
                    r.hset(f'meeting_{meeting_instance["meetingID"]}', 'isActive',
                           1)
                    isOnceActive = True
                    break
            # Deactivate meeting if it is not active
            if not isOnceActive:
                r.hset(f'meeting_{meeting["meetingID"]}', 'isActive',
                       0)

        time.sleep(60)


def str2datetime(date_str):
    return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')


def initialise_columns():
    user_columns = ['userID', 'username', 'age', 'gender', 'email']
    meeting_columns = ['meetingID', 'title', 'description', 'is_public']
    meeting_audience_columns = ['meetingID', 'email']
    meeting_instance_columns = ['meetingID', 'orderID', 'fromDatetime', 'toDatetime']
    return user_columns, meeting_columns, meeting_audience_columns, meeting_instance_columns


def run():
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


if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    user_columns, meeting_columns, meeting_audience_columns, meeting_instance_columns = initialise_columns()
    db = MySQLHandler()
    db.connect()
    users = pd.DataFrame(db.select('SELECT * FROM users'), columns=user_columns)
    meetings = pd.DataFrame(db.select('SELECT * FROM meetings'), columns=meeting_columns)
    meeting_instances = pd.DataFrame(db.select('SELECT * FROM meeting_instances'), columns=meeting_instance_columns)
    meeting_audience = pd.DataFrame(db.select('SELECT * FROM meeting_audience'), columns=meeting_audience_columns)
    users = json.loads(users.to_json(orient='records'))
    meetings = json.loads(meetings.to_json(orient='records'))

    # Insert meetings to redis
    with r.pipeline() as pipe:
        for meeting in meetings:
            for field, value in meeting.items():
                pipe.hset(f'meeting_{meeting["meetingID"]}', field, value)
        pipe.execute()

    meetings = {entry['meetingID']: entry for entry in meetings}
    user = User(**users[0])
    meeting = Meeting(**meetings[1])
    join_meeting(user, meeting)

    main = threading.Thread(target=run)
    main.start()

    scheduler = threading.Thread(target=controller)
    scheduler.start()

    # Wait for the continuous thread to finish
    main.join()

    # Terminate the periodic thread after the continuous thread is done
    scheduler.join(timeout=1)  # Give it a chance to finish the current iteration

    # Load the event_log data from redis to mysql
    #while r.llen('events_log') > 0:
    #    # Pop a JSON document from the Redis list
    #    json_document = r.lpop('events_log').decode("utf-8")
    #    event_log = json.loads(json_document)
    #    sql_query = "INSERT INTO events_log (event_id, userID, event_type, timestamp) VALUES (%s, %s, %s, %s)"
    #    values = (
    #        event_log['event_id'], event_log['user_id'], event_log['event_type'],
    #        str2datetime(event_log['timestamp']))
    #    db.execute(sql_query, values)

    db.close()
