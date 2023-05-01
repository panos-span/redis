import time
import redis
import json

event = {
    'event_id': f'event_{int(time.time())}',
    'user_id': 2,
    'event_type': 1,  # join_meeting
    'timestamp': time.time()
}
r = redis.Redis(host='localhost', port=6379, db=0)
r.rpush('events_log', json.dumps(event))
serialized_data = r.lrange('events_log', 0, -1)
deserialized_data = [json.loads(item) for item in serialized_data]

# Print the deserialized JSON data
print(deserialized_data)
