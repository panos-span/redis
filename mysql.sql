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

DROP TABLE IF EXISTS Meetings;

CREATE TABLE meeting_instances
(
    meetingID    INT      NOT NULL REFERENCES Meetings (meetingID) ON DELETE CASCADE ON UPDATE CASCADE,
    orderID      INT      NOT NULL,
    fromDatetime DATETIME NOT NULL,
    toDatetime   DATETIME NOT NULL,
    PRIMARY KEY (meetingID, orderID)
);

DROP TABLE IF EXISTS meetinginstances;

CREATE TABLE Meeting_Audience
(
    meetingID  INT          NOT NULL REFERENCES Meetings (meetingID) ON DELETE CASCADE ON UPDATE CASCADE,
    user_email VARCHAR(255) NOT NULL REFERENCES Users (email) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (meetingID, user_email)
);

DROP TABLE IF EXISTS Meeting_Audience;

INSERT INTO Users
VALUES (1, 'nolis', 69, 'Male', 'nolis@dellatollis.gr'),
       (2, 'panos', 420, 'Male', 'panos@span.gr'),
       (3, 'mallo', 420, 'Male', 'teo@mallo.gr'),
       (4, 'spyros', 5, '@', 'g@artop.gr');


INSERT INTO Meetings
VALUES (1, 'Dellatollis', 'Dellatollis is a Greek word meaning "the place where the toll is paid".', TRUE),
       (2, 'Span', 'Span is a Greek word meaning "the place where the span is paid".', FALSE),
       (3, 'Mallo', 'Mallo is a Greek word meaning "the place where the mallo is paid".', TRUE),
       (4, 'Artop', 'Artop is a Greek word meaning "the place where the artop is paid".', FALSE);

INSERT INTO Meeting_Audience (meetingID, user_email)
VALUES (1, 'nolis@dellatollis.gr'),
       (1, 'g@artop.gr'),
       (2, 'panos@span.gr'),
       (2, 'teo@mallo.gr'),
       (3, 'nolis@dellatollis.gr'),
       (3, 'panos@span.gr'),
       (4, 'teo@mallo.gr'),
       (4, 'g@artop.gr');

INSERT INTO meeting_instances (meetingID, orderID, fromDatetime, toDatetime)
VALUES (1, 1, '2023-05-03 00:00:00', '2023-05-06 01:00:00'),
       (1, 2, '2023-05-03 01:00:00', '2023-05-06 02:00:00'),
       (1, 3, '2023-05-03 02:00:00', '2023-05-06 03:00:00'),
       (2, 1, '2023-05-03 00:00:00', '2023-05-06 01:00:00'),
       (2, 2, '2023-05-03 01:00:00', '2023-05-06 02:00:00'),
       (2, 3, '2023-05-03 02:00:00', '2023-05-06 03:00:00'),
       (3, 1, '2023-05-03 00:00:00', '2023-05-03 01:00:00'),
       (3, 2, '2023-05-03 01:00:00', '2023-05-03 02:00:00'),
       (3, 3, '2023-05-03 02:00:00', '2023-05-04 03:00:00'),
       (4, 1, '2023-05-03 00:00:00', '2023-05-04 01:00:00'),
       (4, 2, '2023-05-03 01:00:00', '2023-05-04 02:00:00'),
       (4, 3, '2023-05-03 02:00:00', '2023-05-04 03:00:00');

DELETE FROM meeting_instances;

DROP TABLE IF EXISTS meeting_instances;

CREATE TABLE events_log
(
    event_id   VARCHAR(255) NOT NULL PRIMARY KEY,
    userID     INT          NOT NULL REFERENCES Users (userID) ON DELETE CASCADE ON UPDATE CASCADE,
    event_type INT          NOT NULL,
    timestamp  DATETIME     NOT NULL
);