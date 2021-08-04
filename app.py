from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

#initial route
@app.route('/')
def index():
    #show all to-dos
    todo_list = todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)

#adding route
@app.route('/add', methods=['GET', 'POST'])
def add():
    #add a new to-do note
    title = request.form.get('Title')
    new_todo = todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

#route to update a particular note
@app.route('/update/<int:todo_id>')
def update(todo_id):
    #update status of to-do note from incomplete to complete
    Todo = todo.query.filter_by(id=todo_id).first()
    Todo.complete = not Todo.complete
    db.session.commit()
    return redirect(url_for('index'))

#route to delete a particular note
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    #delete a to-do note
    Todo = todo.query.filter_by(id=todo_id).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect(url_for('index'))

#main function
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
