## Meeting Manager

This program is designed to manage meetings using Redis and MySQL databases. It allows users to join and leave meetings,
view the participants in a meeting, view active meetings, end meetings, send chat messages, and view chat messages. The
program simulates these actions using random selections and user inputs. The main logic of the program is broken down
into several functions, and a controller function is used to manage the state of active meetings.

### Authors: Panagiotis Spanakis, Emmanouil Dellatolas

## Features

- Join and leave meetings
- View participants in a meeting
- View active meetings
- End meetings
- Send and view chat messages

## Dependencies

- Python 3
- Redis
- MySQL
- Pandas

## Installation

- Clone this repository
- Install the required Python packages: `pip install pandas redis`
- Set up a Redis server on your local machine
- Set up a MySQL server on your local machine

## Usage

- Run the program using `python main.py`
- The program will simulate various actions, such as joining and leaving meetings, viewing participants, and sending
  chat messages
- The program will run for 2 minutes and then terminate
- After the program has finished, the events_log will be migrated from Redis to MySQL

## Functions

- `join_meeting(user, meeting, audience=None):` Allows a user to join a meeting if the meeting is active and the user is
  allowed to join.
- `leave_meeting(user_id, meetingID, timeOut=False):` Allows a user to leave a meeting if the meeting is active and the
  user is part of the participants.
- `get_current_participants(meetingID):` Retrieves a list of the current participants in a meeting.
- `get_active_meetings():` Retrieves a list of active meetings.
- `end_meeting(meetingID):` Ends a meeting by removing all participants from the meeting.
- `post_chat_message(user_id, meetingID, message):` Posts a chat message to a meeting.
- `get_chat_messages(meetingID):` Retrieves all chat messages from a meeting.
- `get_join_timestamps(meetingID):` Retrieves the join timestamps of all participants in a meeting.
- `get_active_meeting_timestamps():` Retrieves the join timestamps of all participants in all active meetings.
- `get_user_chat_messages(meetingID, user_id):` Retrieves all chat messages from a meeting for a specific user.

