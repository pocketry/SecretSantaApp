-- Enable foreign key enforcement (required in SQLite)
PRAGMA foreign_keys = ON;

-- Table: EXCHANGE
CREATE TABLE exchange (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Table: SANTA
CREATE TABLE santa (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    parentName TEXT
);

-- Table: SANTAEXCHANGEPARTICIPATION
CREATE TABLE santa_exchange_participation (
    id INTEGER PRIMARY KEY,
    exchangeID INTEGER NOT NULL,
    santaID INTEGER NOT NULL,
    isAdmin BOOLEAN,
    FOREIGN KEY (exchangeID) REFERENCES exchange(id),
    FOREIGN KEY (santaID) REFERENCES santa(id)
);

-- Table: SANTARESTRICTION
CREATE TABLE santa_restriction (
    id INTEGER PRIMARY KEY,
    santa1ID INTEGER NOT NULL,
    santa2ID INTEGER NOT NULL,
    CONSTRAINT check_order CHECK (santa1ID < santa2ID),
    CONSTRAINT unique_pair UNIQUE (santa1ID, santa2ID),
    FOREIGN KEY (santa1ID) REFERENCES santa(id),
    FOREIGN KEY (santa2ID) REFERENCES santa(id)
);

-- Table: EXCHANGERUN
CREATE TABLE exchange_run (
    id INTEGER PRIMARY KEY,
    exchangeID INTEGER NOT NULL,
    createdAt TEXT NOT NULL, -- use ISO 8601 string format for datetime
    FOREIGN KEY (exchangeID) REFERENCES exchange(id)
);

-- Table: EXCHANGEASSIGNMENT
CREATE TABLE exchange_assignment (
    id INTEGER PRIMARY KEY,
    exchangeRunID INTEGER NOT NULL,
    santaID INTEGER NOT NULL,
    gifteeSantaID INTEGER NOT NULL,
    FOREIGN KEY (exchangeRunID) REFERENCES exchange_run(id),
    FOREIGN KEY (santaID) REFERENCES santa(id),
    FOREIGN KEY (gifteeSantaID) REFERENCES santa(id)
);