import threading

import redis
import json
import time
from datetime import datetime
import random
from objects import User, MeetingInstance
from mysql_handler import MySQLHandler
import pandas as pd

r = redis.StrictRedis(host='localhost', port=6379, db=0)


# 1
def join_meeting(user, meeting_instance, audience=None):
    if audience is None or user.email in audience:
        r.sadd(f'participants_{meeting_instance.meetingID}_{meeting_instance.orderID}', user.userID)
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
def leave_meeting(user_id, meetingID, meeting_instance_orderID):
    if r.srem(f'participants_{meetingID}_{meeting_instance_orderID}', user_id):
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
def get_current_participants(meetingID, meeting_instance_orderID):
    return list(r.smembers(f'participants_{meetingID}_{meeting_instance_orderID}'))


# 4
def get_active_meetings_instances():
    active_meetings = {}
    for key in r.scan_iter('meeting_instance_*_*'):
        # meeting_instance = json.loads(r.get(key))
        hash_table_contents = r.hgetall(key.decode("utf-8"))
        # Decode the byte strings returned by the hgetall method
        meeting_instance = {k.decode("utf-8"): v.decode("utf-8") for k, v in hash_table_contents.items()}
        if str2datetime(meeting_instance['fromDatetime']) <= datetime.now() <= str2datetime(
                meeting_instance['toDatetime']):
            active_meetings[f"{meeting_instance['meetingID']}_{meeting_instance['orderID']}"] = meeting_instance
    return active_meetings


# 5
def end_meeting(meetingID, meeting_instance_orderID):
    participants = r.smembers(f'participants_{meetingID}_{meeting_instance_orderID}')
    for user_id in participants:
        leave_meeting(user_id.decode('utf-8'), meetingID, meeting_instance_orderID)
    r.delete(f'meeting_instance_{meetingID}_{meeting_instance_orderID}')


# 6
def post_chat_message(user_id, meetingID, meeting_instance_orderID, message):
    chat_message = {
        'user_id': user_id,
        'message': message,
        'timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    }
    r.rpush(f'chat_{meetingID}_{meeting_instance_orderID}', json.dumps(chat_message, default=str))


# 7
def get_chat_messages(meetingID, meeting_instance_orderID):
    messages = []
    for message in r.lrange(f'chat_{meetingID}_{meeting_instance_orderID}', 0, -1):
        messages.append(json.loads(message))
    return messages


# 8
def get_join_timestamps(meetingID, meeting_instance_orderID):
    join_timestamps = {}
    for event in r.lrange('events_log', 0, -1):
        event_data = json.loads(event)
        if event_data['event_type'] == 1 and event_data['user_id'] in r.smembers(
                f'participants_{meetingID}_{meeting_instance_orderID}'):
            join_timestamps[event_data['user_id']] = event_data['timestamp']
    return join_timestamps


# 9
def get_user_chat_messages(meetingID, meeting_instance_orderID, user_id):
    user_messages = []
    for message in r.lrange(f'chat_{meetingID}_{meeting_instance_orderID}', 0, -1):
        message_data = json.loads(message)
        if message_data['user_id'] == user_id:
            user_messages.append(message_data)
    return user_messages


def generateRandomMessage():
    return "Random Message " + str(random.randint(-10000, 1000000))


def controller():
    start_time = time.time()
    while main.is_alive():
        print(time.time() - start_time)
        # Check for active meetings if not active then deactivate them
        active_meetings_instances = get_active_meetings_instances()
        for key in r.scan_iter('meeting_instance_*_*'):
            # meeting_instance = json.loads(r.get(key))
            hash_table_contents = r.hgetall(key.decode("utf-8"))
            # Decode the byte strings returned by the hgetall method
            meeting_instance = {k.decode("utf-8"): v.decode("utf-8") for k, v in hash_table_contents.items()}

            # Deactivate meeting if it is not active
            if str2datetime(meeting_instance['toDatetime']) < datetime.now():
                end_meeting(meeting_instance['meetingID'], meeting_instance['orderID'])
                # del active_meetings_instances[f"{meeting_instance['meetingID']}_{meeting_instance['orderID']}"]
            # Activate meeting if it is not active
            # elif str2datetime(meeting_instance['fromDatetime']) <= datetime.now() <= str2datetime(
            #        meeting_instance['toDatetime']):

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
        print(time.time() - start_time)
        choice = random.randint(0, 8)
        user_num = random.randint(0, 3)
        meeting_num = random.randint(0, 3)
        user = User(**users[user_num])
        meeting_instance = MeetingInstance(**meeting_instances[meeting_num])
        if choice == 0:
            if meetings[meeting_instance.meetingID]['is_public']:
                join_meeting(user, meeting_instance)
            else:
                print('Meeting is private')
                print(join_meeting(user, meeting_instance,
                                   meeting_audience[meeting_audience['meetingID'] == meeting_num + 1]['email'].values))
        elif choice == 1:
            leave_meeting(user.userID, meeting_instance.meetingID, meeting_instance.orderID)
        elif choice == 2:
            get_current_participants(meeting_instance.meetingID, meeting_instance.orderID)
        elif choice == 3:
            get_active_meetings_instances()
        elif choice == 4:
            end_meeting(meeting_instance.meetingID, meeting_instance.orderID)
        elif choice == 5:
            post_chat_message(user.userID, meeting_instance.meetingID, meeting_instance.orderID,
                              generateRandomMessage())
        elif choice == 6:
            get_chat_messages(meeting_instance.meetingID, meeting_instance.orderID)
        elif choice == 7:
            get_join_timestamps(meeting_instance.meetingID, meeting_instance.orderID)
        elif choice == 8:
            get_user_chat_messages(meeting_instance.meetingID, meeting_instance.orderID, user.userID)
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
    meeting_instances = json.loads(meeting_instances.to_json(orient='records', date_format='iso'))
    # Insert active meeting_instances to redis
    with r.pipeline() as pipe:
        for meeting_instance in meeting_instances:
            # if str2datetime(meeting_instance['fromDatetime']) <= datetime.now() <= str2datetime(
            #        meeting_instance['toDatetime']):
            for field, value in meeting_instance.items():
                pipe.hset(f'meeting_instance_{meeting_instance["meetingID"]}_{meeting_instance["orderID"]}', field,
                          value)
        pipe.execute()

    main = threading.Thread(target=run)
    main.start()

    scheduler = threading.Thread(target=controller)
    scheduler.start()

    # Wait for the continuous thread to finish
    main.join()

    # Terminate the periodic thread after the continuous thread is done
    scheduler.join(timeout=1)  # Give it a chance to finish the current iteration

    # Load the event_log data from redis to mysql
    while r.llen('events_log') > 0:
        # Pop a JSON document from the Redis list
        json_document = r.lpop('event_log').decode("utf-8")
        event_log = json.loads(json_document)
        sql_query = "INSERT INTO events_log (event_id, userID, event_type, timestamp) VALUES (%s, %s, %s, %s)"
        values = (
            event_log['event_id'], event_log['user_id'], event_log['event_type'],
            str2datetime(event_log['timestamp']))
        # values = **event_log
        db.execute(sql_query, values)

    db.close()
