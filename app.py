import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.url import URL
from flask_migrate import Migrate

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
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'),  nullable=False)
    list = db.relationship('TodoList', back_populates='todos')

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', back_populates='list', lazy=True)

@app.route('/lists/create', methods=['POST'])
def create_list():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['name'] = todolist.name
        body['id'] = todolist.id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
        body['id'] = todo.id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)
    
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        redirect(url_for('index'))
    return jsonify({ 'success': True })

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', 
    lists=TodoList.query.all(), 
    active_list=TodoList.query.get(list_id), 
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
    )

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

if __name__ == '__main__':
    with app.app_context():
        app.debug = True
        #db.create_all()
        app.run(host="0.0.0.0", port=5000)