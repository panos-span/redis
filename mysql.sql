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
    isPublic    BOOLEAN      NOT NULL,
    audience    VARCHAR(255)
);

CREATE TABLE MeetingInstances
(
    meetingID    INT      NOT NULL REFERENCES Meetings (meetingID) ON DELETE CASCADE ON UPDATE CASCADE,
    orderID      INT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fromDatetime DATETIME NOT NULL,
    toDatetime   DATETIME NOT NULL
);

INSERT INTO Users
VALUES ('nolis', 69, 'Male', 'nolis@dellatollis.gr'),
       ('panos', 420, 'Male', 'panos@span.gr'),
       ('mallo', 420, 'Male', 'teo@mallo.gr'),
       ('spyros', 5, 'Male', 'g@artop.gr');


INSERT INTO Meetings
VALUES ('Dellatollis', 'Dellatollis is a Greek word meaning "the place where the toll is paid".', TRUE,
        'mallo;spyros;nolis'),
       ('Span', 'Span is a Greek word meaning "the place where the span is paid".', FALSE, NULL),
       ('Mallo', 'Mallo is a Greek word meaning "the place where the mallo is paid".', TRUE, 'panos;spyros;nolis'),
       ('Artop', 'Artop is a Greek word meaning "the place where the artop is paid".', FALSE, NULL);

INSERT INTO MeetingInstances (meetingID, orderID, fromDatetime, toDatetime)
VALUES (1, 1, '2019-01-01 00:00:00', '2019-01-01 01:00:00'),
       (1, 2, '2019-01-01 01:00:00', '2019-01-01 02:00:00'),
       (1, 3, '2019-01-01 02:00:00', '2019-01-01 03:00:00'),
       (2, 1, '2019-01-01 00:00:00', '2019-01-01 01:00:00'),
       (2, 2, '2019-01-01 01:00:00', '2019-01-01 02:00:00'),
       (2, 3, '2019-01-01 02:00:00', '2019-01-01 03:00:00'),
       (3, 1, '2019-01-01 00:00:00', '2019-01-01 01:00:00'),
       (3, 2, '2019-01-01 01:00:00', '2019-01-01 02:00:00'),
       (3, 3, '2019-01-01 02:00:00', '2019-01-01 03:00:00'),
       (4, 1, '2019-01-01 00:00:00', '2019-01-01 01:00:00'),
       (4, 2, '2019-01-01 01:00:00', '2019-01-01 02:00:00'),
       (4, 3, '2019-01-01 02:00:00', '2019-01-01 03:00:00');


