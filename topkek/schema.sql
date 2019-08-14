
DROP TABLE IF EXISTS solves;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS challenges;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  admin BOOLEAN
);

CREATE TABLE challenges (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  title TEXT UNIQUE NOT NULL,
  category TEXT NOT NULL,
  body TEXT NOT NULL,
  hint TEXT NOT NULL,
  solution TEXT NOT NULL
);

CREATE TABLE solves (
  user_id INTEGER,
  challenge_id INTEGER,
  hinted BOOLEAN,
  solved BOOLEAN,
  PRIMARY KEY (user_id, challenge_id),
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (challenge_id) REFERENCES challenges (id)
);
