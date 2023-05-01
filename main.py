import redis
import json
import time
from datetime import datetime
import random
import schedule as schedule
from objects import User, Meeting, MeetingInstance, EventLog
from mysql_handler import MySQLHandler
import pandas as pd
import threading

r = redis.StrictRedis(host='localhost', port=6379, db=0)


# 1
def join_meeting(user, meeting_instance):
    # user = json.loads(r.get(f'user_{user_id}'))
    # meeting_instance = json.loads(r.get(f'meeting_instance_{meeting_id}_{meeting_instance_order_id}'))

    if meeting_instance['is_public'] or user['email'] in meeting_instance['audience']:
        r.sadd(f'participants_{meeting_id}', user_id)
        event = {
            'event_id': f'event_{int(time.time())}',
            'user_id': user_id,
            'event_type': 1,  # join_meeting
            'timestamp': time.time()
        }
        r.rpush('events_log', json.dumps(event))
        return True
    return False


# 2
def leave_meeting(user_id, meeting_id):
    if r.srem(f'participants_{meeting_id}', user_id):
        event = {
            'event_id': f'event_{int(time.time())}',
            'user_id': user_id,
            'event_type': 2,  # leave_meeting
            'timestamp': time.time()
        }
        r.rpush('events_log', json.dumps(event))
        return True
    return False


# 3
def get_current_participants(meeting_id, meeting_instance_order_id):
    return list(r.smembers(f'participants_{meeting_id}_{meeting_instance_order_id}'))


# 4
def get_active_meetings():
    now = datetime.now()
    active_meetings = []
    for key in r.scan_iter('meeting_instance_*_*'):
        meeting_instance = json.loads(r.get(key))
        if meeting_instance['fromDatetime'] <= now <= meeting_instance['toDatetime']:
            active_meetings.append(meeting_instance)
    return active_meetings


# 5
def end_meeting(meeting_id, meeting_instance_order_id):
    participants = r.smembers(f'participants_{meeting_id}_{meeting_instance_order_id}')
    for user_id in participants:
        leave_meeting(user_id, meeting_id)


# 6
def post_chat_message(user_id, meeting_id, message):
    chat_message = {
        'user_id': user_id,
        'message': message,
        'timestamp': time.time()
    }
    r.rpush(f'chat_{meeting_id}', json.dumps(chat_message))


# 7
def get_chat_messages(meeting_id):
    messages = []
    for message in r.lrange(f'chat_{meeting_id}', 0, -1):
        messages.append(json.loads(message))
    return messages


# 8
def get_join_timestamps(meeting_id):
    join_timestamps = {}
    for event in r.lrange('events_log', 0, -1):
        event_data = json.loads(event)
        if event_data['event_type'] == 1 and event_data['user_id'] in r.smembers(f'participants_{meeting_id}'):
            join_timestamps[event_data['user_id']] = event_data['timestamp']
    return join_timestamps


# 9
def get_user_chat_messages(meeting_id, meeting_instance_order_id, user_id):
    user_messages = []
    for message in r.lrange(f'chat_{meeting_id}_{meeting_instance_order_id}', 0, -1):
        message_data = json.loads(message)
        if message_data['user_id'] == user_id:
            user_messages.append(message_data)
    return user_messages


def controller():
    # Check for active meetings if not active then deactivate them
    print('Checking for active meetings')
    active_meetings = get_active_meetings()
    for meeting in active_meetings:
        if meeting['toDatetime'] < datetime.now():
            end_meeting(meeting['meetingID'])



def initialise_columns():
    user_columns = ['id', 'username', 'age', 'gender', 'email']
    meeting_columns = ['id', 'title', 'description', 'is_public']
    meeting_audience_columns = ['meetingID', 'email']
    meeting_instance_columns = ['meetingID', 'orderID', 'fromDatetime', 'toDatetime']
    return user_columns, meeting_columns, meeting_audience_columns, meeting_instance_columns


def initialise_redis():
    r = redis.Redis(host='localhost', port=6379, db=0)


if __name__ == '__main__':
    user_columns, meeting_columns, meeting_audience_columns, meeting_instance_columns = initialise_columns()
    db = MySQLHandler()
    db.connect()
    users = pd.DataFrame(db.select('SELECT * FROM users'), columns=user_columns)
    meetings = pd.DataFrame(db.select('SELECT * FROM meetings'), columns=meeting_columns)
    meeting_instances = pd.DataFrame(db.select('SELECT * FROM meeting_instances'), columns=meeting_instance_columns)
    users = json.loads(users.to_json(orient='records'))
    meetings = json.loads(meetings.to_json(orient='records'))
    meeting_instances = json.loads(meeting_instances.to_json(orient='records'))
    schedule.every(60).seconds.do(controller)
    # Run loop for 120 seconds continuously
    t_end = time.time() + 60 * 2
    while time.time() < t_end:
        schedule.run_pending()
        choice = random.randint(0, 10)
        if choice == 0:
            join_meeting(random.choice(users['id'].values), random.choice(meetings['id'].values))
        elif choice == 1:
            leave_meeting(random.choice(users['id'].values), random.choice(meetings['id'].values))
        elif choice == 2:
            get_current_participants(random.choice(meetings['id'].values))
        elif choice == 3:
            get_active_meetings()
        elif choice == 4:
            end_meeting(random.choice(meetings['id'].values))
        elif choice == 5:
            post_chat_message(random.choice(users['id'].values), random.choice(meetings['id'].values), 'Hello')
        elif choice == 6:
            get_chat_messages(random.choice(meetings['id'].values))
        elif choice == 7:
            get_join_timestamps(random.choice(meetings['id'].values))
        elif choice == 8:
            get_user_chat_messages(random.choice(meetings['id'].values), random.choice(users['id'].values))
        time.sleep(1)
