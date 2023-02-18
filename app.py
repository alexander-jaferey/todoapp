from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL

postgres_db = {
    'drivername': 'postgresql',
    'username': 'vagrant',
    'password': 'password',
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'todoapp'
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URL.create(**postgres_db)
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description': todo.description
    })


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all()
    )

if __name__ == '__main__':
    with app.app_context():
        app.debug = True
        db.create_all()
        app.run(host="0.0.0.0", port=5000)