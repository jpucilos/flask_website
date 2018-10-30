import os
import sys
#Avoid TCL error
import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, flash, url_for, redirect, render_template
#from flask import session
#from flask_sqlalchemy import SQLAlchemy
import dalton_method
import signal_fading_sim

UPLOAD_FOLDER = '/home/jpucilos/flask_website/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 0.5 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



'''
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

'''
@app.route('/', endpoint='index')
def index():
	return render_template('index.html')

@app.route('/projects', endpoint='projects')
def projects():
	return render_template('projects.html')

@app.route('/books', endpoint='books')
def contact():
	return render_template('books.html')

@app.route('/photos', endpoint='photos')
def photos():
	return render_template('photos.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/projects/dalton_method', endpoint='dalton method', methods = ['GET', 'POST'])
def project462():
    if request.method == 'GET':
	    return render_template('dalton_method.html')
    else:
        # check if the post request has the file part
        file = request.files['file']
        if 'file' not in request.files or file == '':
            flash('No file inputted')
            return render_template('dalton_method.html')
        # if user does not select file, browser also
        # submit a empty part without filename
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'test2.jpg'))
            dalton_method.dalton_run('/home/jpucilos/flask_website/static/test2.jpg')
            return render_template('dalton_method2.html')
        return render_template('dalton_method.html')


@app.route('/projects/rayleigh_fading', endpoint='rayleigh fading', methods = ['GET', 'POST'])
def project441():
    if request.method == 'GET':
	    return render_template('rayleigh_fading.html')
    else:
        # check if the post request has the file part
        try:
            f0 = int(request.form['f0'])
            v = int(request.form['v'])
            n = int(request.form['n'])
            fs = int(request.form['fs'])
            signal_fading_sim.rayleigh_fade(f0,v,n,fs)
        except ValueError as verr:
            print >> sys.stderr, str(verr)
        except Exception as ex:
            print >> sys.stderr, str(ex)

        return render_template('rayleigh_fading.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


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
'''
if __name__ == '__main__':
#	db.create_all()
	app.run(debug = False)

