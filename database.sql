-- ============================================================
-- Event Registration System — Database Setup Script
-- RDBMS Lab Module 5
-- ============================================================
-- Run this file to set up the complete database with sample data.
--
-- Command line  : mysql -u root -p < database.sql
-- MySQL Workbench: File → Open SQL Script → Run (⚡)
-- ============================================================

-- Step 1: Create and select the database
CREATE DATABASE IF NOT EXISTS event_registration_db;
USE event_registration_db;

-- ============================================================
-- Step 2: Drop tables in reverse dependency order (safe re-run)
-- ============================================================
DROP TABLE IF EXISTS registrations;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS participants;

-- ============================================================
-- Step 3: CREATE TABLE — events
-- ============================================================
CREATE TABLE events (
    event_id      INT           AUTO_INCREMENT PRIMARY KEY,
    event_name    VARCHAR(150)  NOT NULL,
    event_date    DATE          NOT NULL,
    venue         VARCHAR(200)  NOT NULL,
    description   TEXT
);

-- ============================================================
-- Step 4: CREATE TABLE — participants
-- ============================================================
CREATE TABLE participants (
    participant_id INT          AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    email          VARCHAR(150) NOT NULL UNIQUE,
    phone          VARCHAR(15)  NOT NULL
);

-- ============================================================
-- Step 5: CREATE TABLE — registrations
-- Junction table linking participants to events.
-- status ENUM: Registered | Confirmed | Attended | Cancelled
-- ============================================================
CREATE TABLE registrations (
    registration_id   INT  AUTO_INCREMENT PRIMARY KEY,
    event_id          INT  NOT NULL,
    participant_id    INT  NOT NULL,
    registration_date DATE NOT NULL,
    status            ENUM('Registered', 'Confirmed', 'Attended', 'Cancelled')
                      NOT NULL DEFAULT 'Registered',

    -- FK: registrations.event_id → events.event_id
    CONSTRAINT fk_reg_event
        FOREIGN KEY (event_id) REFERENCES events(event_id),

    -- FK: registrations.participant_id → participants.participant_id
    CONSTRAINT fk_reg_participant
        FOREIGN KEY (participant_id) REFERENCES participants(participant_id),

    -- A participant cannot be registered for the same event twice
    CONSTRAINT uq_event_participant
        UNIQUE (event_id, participant_id)
);

-- ============================================================
-- Step 6: INSERT sample EVENTS (6 events)
-- ============================================================
INSERT INTO events (event_name, event_date, venue, description) VALUES
('Python Programming Workshop',  '2026-10-05', 'Computer Lab 1',   'Introduction to Python programming and practical development.'),
('Web Development Bootcamp',     '2026-10-10', 'Seminar Hall',      'Hands-on introduction to modern web development.'),
('AI & Technology Seminar',      '2026-10-15', 'Main Auditorium',   'Seminar covering current developments in artificial intelligence and technology.'),
('UI/UX Design Workshop',        '2026-10-20', 'Innovation Lab',    'Practical introduction to user interface and user experience design.'),
('Interclass Football Tournament','2026-10-25', 'College Ground',    'Football tournament conducted for students.'),
('Tech Quiz Challenge',          '2026-10-30', 'Seminar Hall',      'Technical quiz covering programming, databases, networking and emerging technologies.');

-- ============================================================
-- Step 7: INSERT sample PARTICIPANTS (19 participants)
-- Names are preserved EXACTLY as provided.
-- Emails and phones are fictional/demo values only.
-- ============================================================
INSERT INTO participants (name, email, phone) VALUES
('ADARSH S',               'adarsh.s@example.com',           '9876500001'),
('ADARSH TOM',             'adarsh.tom@example.com',         '9876500002'),
('ADHITHYAN K BIJU',       'adhithyan.biju@example.com',     '9876500003'),
('ALBERT SONI',            'albert.soni@example.com',        '9876500004'),
('ALLEN JOE CHERIAMADOM',  'allen.joe@example.com',          '9876500005'),
('ALPHONSA THOMAS',        'alphonsa.thomas@example.com',    '9876500006'),
('ANUGRAH ANIL',           'anugrah.anil@example.com',       '9876500007'),
('CHRIS P JOHN',           'chris.john@example.com',         '9876500008'),
('DEVANANDHA P S',         'devanandha.ps@example.com',      '9876500009'),
('DEVIKA SANOJ',           'devika.sanoj@example.com',       '9876500010'),
('FASILA SATHAR',          'fasila.sathar@example.com',      '9876500011'),
('JAKE J MATHEW',          'jake.mathew@example.com',        '9876500012'),
('JISS CHERIAN',           'jiss.cherian@example.com',       '9876500013'),
('MARIA SANTY',            'maria.santy@example.com',        '9876500014'),
('NIKHIL S KUMAR',         'nikhil.kumar@example.com',       '9876500015'),
('RICHAN JOSE',            'richan.jose@example.com',        '9876500016'),
('RICHU FRANCY SEBASTIAN', 'richu.sebastian@example.com',   '9876500017'),
('SAYOOJYA P.',            'sayoojya.p@example.com',         '9876500018'),
('THERESSA ROSE MATHEW',   'theressa.mathew@example.com',    '9876500019');

-- ============================================================
-- Step 8: INSERT sample REGISTRATIONS
--
-- Participant ID reference:
--  1  ADARSH S               11 FASILA SATHAR
--  2  ADARSH TOM             12 JAKE J MATHEW
--  3  ADHITHYAN K BIJU       13 JISS CHERIAN
--  4  ALBERT SONI            14 MARIA SANTY
--  5  ALLEN JOE CHERIAMADOM  15 NIKHIL S KUMAR
--  6  ALPHONSA THOMAS        16 RICHAN JOSE
--  7  ANUGRAH ANIL           17 RICHU FRANCY SEBASTIAN
--  8  CHRIS P JOHN           18 SAYOOJYA P.
--  9  DEVANANDHA P S         19 THERESSA ROSE MATHEW
-- 10  DEVIKA SANOJ
--
-- Event ID reference:
--  1  Python Programming Workshop   (2026-10-05)
--  2  Web Development Bootcamp      (2026-10-10)
--  3  AI & Technology Seminar       (2026-10-15)
--  4  UI/UX Design Workshop         (2026-10-20)
--  5  Interclass Football Tournament(2026-10-25)
--  6  Tech Quiz Challenge           (2026-10-30)
--
-- Every participant is registered for at least one event.
-- Total registrations: 45
-- ============================================================
INSERT INTO registrations (event_id, participant_id, registration_date, status) VALUES

-- ── Event 1: Python Programming Workshop ──────────────────
(1,  1,  '2026-09-20', 'Confirmed'),   -- ADARSH S
(1,  2,  '2026-09-20', 'Confirmed'),   -- ADARSH TOM
(1,  3,  '2026-09-21', 'Registered'),  -- ADHITHYAN K BIJU
(1,  4,  '2026-09-21', 'Confirmed'),   -- ALBERT SONI
(1,  5,  '2026-09-22', 'Attended'),    -- ALLEN JOE CHERIAMADOM
(1,  7,  '2026-09-22', 'Attended'),    -- ANUGRAH ANIL
(1,  8,  '2026-09-23', 'Confirmed'),   -- CHRIS P JOHN
(1,  9,  '2026-09-23', 'Registered'),  -- DEVANANDHA P S

-- ── Event 2: Web Development Bootcamp ─────────────────────
(2,  6,  '2026-09-22', 'Confirmed'),   -- ALPHONSA THOMAS
(2,  10, '2026-09-22', 'Registered'),  -- DEVIKA SANOJ
(2,  11, '2026-09-23', 'Confirmed'),   -- FASILA SATHAR
(2,  12, '2026-09-23', 'Attended'),    -- JAKE J MATHEW
(2,  13, '2026-09-24', 'Confirmed'),   -- JISS CHERIAN
(2,  14, '2026-09-24', 'Attended'),    -- MARIA SANTY
(2,  15, '2026-09-25', 'Registered'),  -- NIKHIL S KUMAR

-- ── Event 3: AI & Technology Seminar ──────────────────────
(3,  1,  '2026-09-25', 'Registered'),  -- ADARSH S
(3,  3,  '2026-09-25', 'Confirmed'),   -- ADHITHYAN K BIJU
(3,  5,  '2026-09-26', 'Registered'),  -- ALLEN JOE CHERIAMADOM
(3,  7,  '2026-09-26', 'Confirmed'),   -- ANUGRAH ANIL
(3,  9,  '2026-09-26', 'Registered'),  -- DEVANANDHA P S
(3,  11, '2026-09-27', 'Confirmed'),   -- FASILA SATHAR
(3,  13, '2026-09-27', 'Registered'),  -- JISS CHERIAN
(3,  17, '2026-09-27', 'Confirmed'),   -- RICHU FRANCY SEBASTIAN
(3,  19, '2026-09-28', 'Registered'),  -- THERESSA ROSE MATHEW

-- ── Event 4: UI/UX Design Workshop ────────────────────────
(4,  2,  '2026-09-28', 'Registered'),  -- ADARSH TOM
(4,  4,  '2026-09-28', 'Confirmed'),   -- ALBERT SONI
(4,  6,  '2026-09-29', 'Registered'),  -- ALPHONSA THOMAS
(4,  8,  '2026-09-29', 'Confirmed'),   -- CHRIS P JOHN
(4,  10, '2026-09-29', 'Registered'),  -- DEVIKA SANOJ
(4,  12, '2026-09-30', 'Confirmed'),   -- JAKE J MATHEW
(4,  14, '2026-09-30', 'Registered'),  -- MARIA SANTY
(4,  16, '2026-09-30', 'Confirmed'),   -- RICHAN JOSE
(4,  18, '2026-10-01', 'Registered'),  -- SAYOOJYA P.

-- ── Event 5: Interclass Football Tournament ────────────────
(5,  15, '2026-10-01', 'Confirmed'),   -- NIKHIL S KUMAR
(5,  16, '2026-10-01', 'Confirmed'),   -- RICHAN JOSE
(5,  17, '2026-10-02', 'Confirmed'),   -- RICHU FRANCY SEBASTIAN
(5,  18, '2026-10-02', 'Confirmed'),   -- SAYOOJYA P.
(5,  19, '2026-10-02', 'Confirmed'),   -- THERESSA ROSE MATHEW

-- ── Event 6: Tech Quiz Challenge ──────────────────────────
(6,  1,  '2026-10-03', 'Registered'),  -- ADARSH S
(6,  2,  '2026-10-03', 'Registered'),  -- ADARSH TOM
(6,  5,  '2026-10-03', 'Registered'),  -- ALLEN JOE CHERIAMADOM
(6,  8,  '2026-10-04', 'Registered'),  -- CHRIS P JOHN
(6,  11, '2026-10-04', 'Registered'),  -- FASILA SATHAR
(6,  14, '2026-10-04', 'Registered'),  -- MARIA SANTY
(6,  17, '2026-10-05', 'Registered');  -- RICHU FRANCY SEBASTIAN

-- ============================================================
-- Step 9: Verification — row counts after import
-- ============================================================
SELECT 'Database setup complete!' AS Status;
SELECT COUNT(*) AS total_events        FROM events;
SELECT COUNT(*) AS total_participants  FROM participants;
SELECT COUNT(*) AS total_registrations FROM registrations;
