from flask import Flask, json, views, request

import sqlite3
conn = sqlite3.connect('game.db')
app = Flask(__name__)



class GameAPI(views.MethodView):

    def get(self, session):
        c = conn.cursor()
        c.execute('SELECT * FROM game_state WHERE session=?', (session,))
        result = c.fetchone()
        if result:
            (_, state) = result
            return json.jsonify(json.loads(state))
        else:
            return json.jsonify({})

    def post(self, session):
        state = request.get_data()
        c = conn.cursor()
        c.execute('SELECT * FROM game_state WHERE session=?', (session,))
        session_exists = c.fetchone()
        if session_exists:
            c.execute('UPDATE game_state SET state=? WHERE session=?', (state,session,))
        else:
            c.execute('INSERT INTO game_state VALUES (?, ?)', (session, state,))
        conn.commit()
        return self.get(session)

app.add_url_rule('/game/<string:session>', view_func=GameAPI.as_view('game'))
