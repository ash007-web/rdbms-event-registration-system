CREATE DATABASE IF NOT EXISTS event_registration_db;
USE event_registration_db;

-- ==========================================
-- 1. CREATE TABLES
-- ==========================================

-- Create Events Table
CREATE TABLE IF NOT EXISTS events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    venue VARCHAR(255) NOT NULL,
    description TEXT
) ENGINE=InnoDB;

-- Create Participants Table
CREATE TABLE IF NOT EXISTS participants (
    participant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

-- Create Registrations Table (with Foreign Keys)
CREATE TABLE IF NOT EXISTS registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    participant_id INT NOT NULL,
    registration_date DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'Registered',
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id)
) ENGINE=InnoDB;

-- ==========================================
-- 2. INSERT SAMPLE DATA
-- ==========================================

-- Insert Sample Events
INSERT INTO events (event_name, event_date, venue, description) VALUES
('Python Programming Workshop', '2023-11-15', 'Lab 1', 'Introduction to Python programming for beginners.'),
('Web Development Bootcamp', '2023-11-20', 'Lab 2', 'Learn HTML, CSS, and basic JavaScript.'),
('AI & Technology Seminar', '2023-11-25', 'Auditorium', 'Seminar on the future of Artificial Intelligence.'),
('UI/UX Design Workshop', '2023-12-01', 'Design Studio', 'Basics of user interface and user experience design.'),
('Interclass Football Tournament', '2023-12-10', 'Main Ground', 'Annual football tournament.'),
('Tech Quiz Challenge', '2023-12-15', 'Seminar Hall', 'Quiz competition covering various tech topics.');

-- Insert Sample Participants
INSERT INTO participants (name, email, phone) VALUES
('ADARSH S', 'adarsh.s@example.com', '9876543210'),
('ADARSH TOM', 'adarsh.tom@example.com', '9876543211'),
('ADHITHYAN K BIJU', 'adhithyan.biju@example.com', '9876543212'),
('ALBERT SONI', 'albert.soni@example.com', '9876543213'),
('ALLEN JOE CHERIAMADOM', 'allen.joe@example.com', '9876543214'),
('ALPHONSA THOMAS', 'alphonsa.thomas@example.com', '9876543215'),
('ANUGRAH ANIL', 'anugrah.anil@example.com', '9876543216'),
('CHRIS P JOHN', 'chris.john@example.com', '9876543217'),
('DEVANANDHA P S', 'devanandha.ps@example.com', '9876543218'),
('DEVIKA SANOJ', 'devika.sanoj@example.com', '9876543219'),
('FASILA SATHAR', 'fasila.sathar@example.com', '9876543220'),
('JAKE J MATHEW', 'jake.mathew@example.com', '9876543221'),
('JISS CHERIAN', 'jiss.cherian@example.com', '9876543222'),
('MARIA SANTY', 'maria.santy@example.com', '9876543223'),
('NIKHIL S KUMAR', 'nikhil.kumar@example.com', '9876543224'),
('RICHAN JOSE', 'richan.jose@example.com', '9876543225'),
('RICHU FRANCY SEBASTIAN', 'richu.sebastian@example.com', '9876543226'),
('SAYOOJYA P.', 'sayoojya.p@example.com', '9876543227'),
('THERESSA ROSE MATHEW', 'theressa.mathew@example.com', '9876543228');

-- Insert Sample Registrations
-- Event 1: Python Programming Workshop
INSERT INTO registrations (event_id, participant_id, registration_date, status) VALUES
(1, 1, '2023-11-01', 'Registered'),
(1, 2, '2023-11-02', 'Registered'),
(1, 3, '2023-11-03', 'Registered');

-- Event 2: Web Development Bootcamp
INSERT INTO registrations (event_id, participant_id, registration_date, status) VALUES
(2, 4, '2023-11-04', 'Registered'),
(2, 5, '2023-11-05', 'Registered');

-- Event 5: Interclass Football Tournament
INSERT INTO registrations (event_id, participant_id, registration_date, status) VALUES
(5, 6, '2023-11-06', 'Registered'),
(5, 7, '2023-11-07', 'Registered'),
(5, 8, '2023-11-08', 'Registered');
