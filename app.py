# from flask import Flask, render_template,request,redirect
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# import pytz
# import os
# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class Todo(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     desc = db.Column(db.String(500), nullable=False)
#     # date_created = db.Column(db.DateTime, default=datetime.utcnow)
#     date_created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))


#     def __repr__(self) -> str:
#         return f"{self.sno}-{self.title}"



# @app.route("/",methods = ['GET','POST'])

# def hello_world():
#     if request.method=='POST':
#         titles = request.form['title']
#         descs = request.form["desc"]
#         print(titles,descs)
#         todo = Todo(title=titles, desc=descs)
#         attachment_file = request.files['attachment']  # Get attachment file
#         if attachment_file:
#             filename = attachment_file.filename
#             attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             attachment_file.save(attachment_path)  # Save attachment file
#         else:
#             filename = None
#         todo = Todo(title=titles, desc=descs, attachment=filename)
#         db.session.add(todo)
#         db.session.commit()
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return render_template('index.html',allTodo=allTodo)

# @app.route('/show')
# def show_todo():
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return "this is the database"
# @app.route('/delete/<int:sno>')
# def delete(sno):
#     todo=Todo.query.filter_by(sno=sno).first()
#     db.session.delete(todo)
#     db.session.commit()
#     # allTodo = Todo.query.all(todo)
#     # print(allTodo)
#     return redirect('/')

# @app.route('/update/<int:sno>',methods = ['GET','POST'])
# def update(sno):
#     if request.method=="POST":
#         titles = request.form['title']
#         descs = request.form["desc"]
        
#         todo=Todo.query.filter_by(sno=sno).first()
#         todo.title = titles
#         todo.desc = descs
#         db.session.add(todo)
#         db.session.commit()
#         return redirect('/')
#     todo=Todo.query.filter_by(sno=sno).first()

#     return render_template('update.html',todo=todo)
    

#     # return render_template('show.html', allTodo=allTodo)
# with app.app_context():
#     db.create_all()

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import os
from werkzeug.utils import secure_filename

from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = './Documents'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
    attachment = db.Column(db.String(200)) 

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        titles = request.form['title']
        descs = request.form["desc"]
        todo = Todo(title=titles, desc=descs)
        # Use request.files.get to avoid UnboundLocalError if no file is uploaded
        # attachment_file = request.files.get('attachment')  
        
        # if attachment_file:
        #     filename = secure_filename(attachment_file.filename)
        #     # Check if file format is allowed before saving
        #     if filename.endswith(('.pdf', '.jpg')):
        #         attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #         try:
        #             attachment_file.save(attachment_path)
        #             print("Attachment saved successfully!")
        #             todo.attachment = filename
        #         except Exception as e:
        #             print("Error saving attachment:", e)
        #     else:
        #         print("Invalid file format. Only PDF and JPG files are allowed.")
        
        db.session.add(todo)
        db.session.commit()
        print("Todo added successfully!")

    
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    if todo.attachment:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], todo.attachment))
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == "POST":
        titles = request.form['title']
        descs = request.form["desc"]
        todo.title = titles
        todo.desc = descs
        # attachment_file = request.files['attachment']
        # if attachment_file:
        #     filename = attachment_file.filename
        #     attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #     try:
        #         attachment_file.save(attachment_path)
        #         print("Attachment saved successfully!")
        #         todo.attachment = filename
        #     except Exception as e:
        #         print("Error saving attachment:", e)
        
        db.session.commit()
        return redirect('/')
    
    return render_template('update.html', todo=todo)

@app.route('/show')
def show_todo():
    allTodo = Todo.query.all()
    return render_template('show.html', allTodo=allTodo)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/search', methods=['GET'])
def search_todo():
    query = request.args.get('query', '')
    results = Todo.query.filter(Todo.title.ilike(f'%{query}%')).all()
    return render_template('search_results.html', results=results, query=query)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
