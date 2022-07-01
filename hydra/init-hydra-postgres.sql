DROP TABLE IF EXISTS catalog;
DROP TABLE IF EXISTS checks;
CREATE TABLE IF NOT EXISTS catalog(
    id serial PRIMARY KEY,
    dataset_id VARCHAR(24),
    resource_id UUID,
    url VARCHAR,
    deleted BOOLEAN NOT NULL,
    last_check INT,
    priority BOOLEAN NOT NULL,
    initialization BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE(dataset_id, resource_id, url)
);
CREATE TABLE IF NOT EXISTS checks(
    id serial PRIMARY KEY,
    url VARCHAR,
    domain VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    status INT,
    headers JSONB,
    timeout BOOLEAN NOT NULL,
    response_time FLOAT,
    error VARCHAR
);
