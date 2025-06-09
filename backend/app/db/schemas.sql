CREATE TABLE IF NOT EXISTS container_tracking (
    id SERIAL PRIMARY KEY,
    container_number VARCHAR(20) NOT NULL,
    carrier VARCHAR(20),
    status VARCHAR(50),
    location VARCHAR(100),
    eta TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);