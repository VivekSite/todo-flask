from datetime import datetime 
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Todo(db.Model) :
  sno= db.Column(db.Integer, primary_key=True)
  title= db.Column(db.String(200), nullable=False)
  desc= db.Column(db.String(500), nullable=False)
  data_created= db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self) -> str:
    return f"{self.sno} - {self.title}"



@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == "POST":
    title = request.form['title']
    desc = request.form['desc']
    newTodo = Todo(title=title, desc=desc)
    db.session.add(newTodo)
    db.session.commit()

  allTodo = Todo.query.all()
  return render_template('index.html', allTodo=allTodo)



###### The route for updating a Todo  ######
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
  todo = Todo.query.filter_by(sno=sno).first()
  if request.method == "POST":
    title = request.form['title']
    desc = request.form['desc']
    todo.title = title
    todo.desc = desc
    db.session.add(todo)
    db.session.commit()
    return redirect('/')
  
  return render_template('update.html', todo=todo)



###### The route for deleting a Todo  ######
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

