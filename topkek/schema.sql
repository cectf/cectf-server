
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

INSERT INTO users (username, password, admin) VALUES ("a", "b", 0);
INSERT INTO users (username, password, admin) VALUES ("abc", "123", 1);
INSERT INTO challenges (title, category, body, hint, solution) VALUES ("The First Challenge", "crypto", "Just think really hard!", "CTF{l0l}", "CTF{l0l}");
INSERT INTO challenges (title, category, body, hint, solution) VALUES ("The Second Challenge", "reversing", "Just think really harder!", "not so easy now huh", "CTF{1337}");
