CREATE SCHEMA IF NOT EXISTS lab;

CREATE TABLE IF NOT EXISTS lab.customers (
    row_id             BIGSERIAL PRIMARY KEY,
    customer_id        TEXT NOT NULL,
    first_name         TEXT NOT NULL,
    last_name          TEXT NOT NULL,
    email               TEXT,
    city                TEXT,
    signup_date         DATE NOT NULL,
    customer_segment    TEXT NOT NULL,
    CONSTRAINT ck_customer_segment_known
        CHECK (customer_segment IN ('Professional', 'Retail', 'SME', 'Student'))
);