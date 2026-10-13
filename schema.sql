
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    gstin VARCHAR(15),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255)
);

CREATE TABLE projects (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    client_id INT REFERENCES clients(id),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    estimated_revenue NUMERIC(12,2) NOT NULL,
    CONSTRAINT check_project_dates
        CHECK (start_date < end_date)
);

CREATE TABLE transactions (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    type VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    project_id INT REFERENCES projects(id),
    CONSTRAINT check_transaction_type
        CHECK (type IN ('income', 'expense')),
    CONSTRAINT check_transaction_amount
        CHECK (amount >= 0)
);
