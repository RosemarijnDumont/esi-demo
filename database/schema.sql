-- SQL schema for the ideas table

CREATE TABLE IF NOT EXISTS ideas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    submitter_name VARCHAR(255),
    submitter_email VARCHAR(255),
    submission_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster retrieval of recently submitted ideas (optional, but good for performance)
CREATE INDEX idx_submission_timestamp ON ideas(submission_timestamp);