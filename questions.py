from flask import Flask
from flask import request
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect(':memory:')


@app.route('/question', methods=['POST'])
def ask_question():
    json = request.get_json()
    question = json['question']
    c = conn.cursor()
    for row in c.execute('SELECT MAX(question_id) FROM questions'):
        row_id = 0 if row[0] is None else row[0]
        row_id += 1
        c.execute('INSERT INTO questions VALUES (?, ?, 0, 0, 0)', (row_id, question,))
        conn.commit()
    return str(row_id)


@app.route('/yes/<int:question_id>', methods=['POST'])
def vote_yes(question_id):
    c = conn.cursor()
    c.execute('UPDATE questions SET yes = yes + 1 where question_id = ?', (question_id,))
    conn.commit()
    return ""


@app.route('/no/<int:question_id>', methods=['POST'])
def vote_no(question_id):
    c = conn.cursor()
    c.execute('UPDATE questions SET no = no + 1 where question_id = ?', (question_id,))
    conn.commit()
    return ""


@app.route('/maybe/<int:question_id>', methods=['POST'])
def vote_maybe(question_id):
    c = conn.cursor()
    c.execute('UPDATE questions SET maybe = maybe + 1 where question_id = ?', (question_id,))
    conn.commit()
    return ""


@app.route('/results/<int:question_id>')
def get_results(question_id):
    c = conn.cursor()
    for row in c.execute('SELECT question, yes, no, maybe FROM questions where question_id = ?', (question_id,)):
        return '''
        Question    Yes No  Maybe
        {}  {}  {}  {}
        '''.format(row[0], row[1], row[2], row[3])


if __name__ == "__main__":
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (question_id integer, question text, yes integer, no integer, maybe integer)''')
    try:
        app.run()
    finally:
        conn.close()