DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
  ticket_name TEXT NOT NULL,
  ticket_description TEXT NOT NULL,
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  due_date TIMESTAMP NOT NULL,
  status TEXT NOT NULL,
  department TEXT NOT NULL,
  category TEXT NOT NULL
);

-- #TODO: User table
-- DROP TABLE IF EXISTS users;

-- CREATE TABLE users (
-- );