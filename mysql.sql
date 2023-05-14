CREATE TABLE Users
(
    userID INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name   VARCHAR(255) NOT NULL,
    age    INT          NOT NULL,
    gender VARCHAR(255) NOT NULL,
    email  VARCHAR(255) NOT NULL
);

CREATE TABLE Meetings
(
    meetingID   INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    isPublic    BOOLEAN      NOT NULL
);


CREATE TABLE meeting_instances
(
    meetingID    INT      NOT NULL REFERENCES Meetings (meetingID) ON DELETE CASCADE ON UPDATE CASCADE,
    orderID      INT      NOT NULL,
    fromDatetime DATETIME NOT NULL,
    toDatetime   DATETIME NOT NULL,
    PRIMARY KEY (meetingID, orderID)
);


CREATE TABLE Meeting_Audience
(
    meetingID  INT          NOT NULL REFERENCES Meetings (meetingID) ON DELETE CASCADE ON UPDATE CASCADE,
    user_email VARCHAR(255) NOT NULL REFERENCES Users (email) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (meetingID, user_email)
);

CREATE TABLE events_log
(
    event_id   VARCHAR(255) NOT NULL PRIMARY KEY,
    userID     INT          NOT NULL REFERENCES Users (userID) ON DELETE CASCADE ON UPDATE CASCADE,
    event_type INT          NOT NULL,
    timestamp  DATETIME     NOT NULL
);