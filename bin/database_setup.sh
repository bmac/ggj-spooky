!#/bin/sh

touch game.db
sqlite3 game.db -cmd "create table game_state(session TEXT PRIMARY KEY, state TEXT)"
