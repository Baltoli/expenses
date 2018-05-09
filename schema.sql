CREATE TABLE IF NOT EXISTS 
expenses (
  id      INTEGER PRIMARY KEY,
  info    TEXT    NOT NULL,
  amount  INTEGER NOT NULL,
  time    INTEGER NOT NULL
);
