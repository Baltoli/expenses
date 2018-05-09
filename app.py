import sqlite3
import json
from flask import g, Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

DATABASE = './expenses.db'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    get_db().commit()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def all_expenses():
    return query_db('select * from expenses')

def expense(exp_id):
    return query_db('select * from expenses where id = ?', exp_id, True)

class Expense(Resource):
    def get(self, exp_id=None):
        if exp_id is None:
            return jsonify(all_expenses())
        else:
            result = expense(exp_id)
            if result is not None:
                return jsonify(result)
            else:
                return "", 404

api.add_resource(Expense, 
        '/expense',
        '/expense/<string:exp_id>')

if __name__ == '__main__':
    app.run(debug=True)
