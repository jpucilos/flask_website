from flask import Flask, request, flash, url_for, redirect, render_template
from flask import session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thoughts.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

class entries(db.Model):
	id = db.Column('entry_id', db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	thought = db.Column(db.String(200))
	time = db.Column(db.String(100))

	def __init__(self, name, thought, time):
		self.name = name
		self.thought = thought
		self.time = time	
@app.route('/')
def index():	
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/photos')
def photos():
	return render_template('photos.html')
'''
@app.route('/your-thoughts')
def index():
	if 'name' not in session:
		return redirect(url_for('login'))
	else:
		return render_template('show_yours.html', entries = reversed(entries.query.filter_by(name = session['name']).all()))
'''

'''
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		if 'name' in request.values:
			session['name'] = request.form['name']
		else:
			session['name'] = 'Anonymous'
		return redirect(url_for('show_all'))
'''



@app.route('/new', methods = ['GET', 'POST'])
def new():
	if request.method == 'POST':
		if not request.form['thought']:
			flash('Please enter all the fields', 'error')
		else:
			entry = entries(session['name'], request.form['thought'], datetime.now().strftime('%Y-%m-%d at %H:%M'))
 
			db.session.add(entry)
			db.session.commit()
			flash('Record was successfully added')
			return redirect(url_for('show_all'))
	return render_template('new.html')

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)

