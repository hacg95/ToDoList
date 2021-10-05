import unittest
from flask import request, make_response, redirect, render_template, session, url_for, flash
from app import create_app
from app.forms import ToDoForm
from app.firestore_service import get_toDo, put_todo, delete_todo, update_todo
from flask_login import login_required, current_user


app = create_app()


@app.cli.command()
def test():
    loader = unittest.TestLoader()
    tests= loader.discover('tests')
    u=unittest.TextTestRunner()
    u.run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)


@app.errorhandler(500)
def not_found(error):
    return render_template("500.html", error=error)


@app.route("/")
def index():
    response = make_response(redirect("/hello"))
    return response


@app.route("/hello", methods=['GET', 'POST'])
@login_required
def hello():
    username = current_user.id
    todo_form = ToDoForm()

    context = {
        'todo': get_toDo(user_id=username),
        'username': username,
        'todo_form': todo_form
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)
        flash('ToDo created succesfully')
        return redirect(url_for('hello'))

    return render_template("hello.html", **context)


@app.route('/todos/delete/<todo_id>', methods=['GET', 'POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id, todo_id)

    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['GET', 'POST'])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id, todo_id, done)

    return redirect(url_for('hello'))


if __name__ == "__main__":
    app.run()