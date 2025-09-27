from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # ✅ Correct import

app = Flask(__name__)
app.secret_key = "secret_key"  # Needed for flash messages

# Initialize extensions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # ✅ Initialize Flask-Bcrypt

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')  # ✅ Correct usage

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)  # ✅ Correct usage

# Create DB
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    return "hi"

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

       

        # Check if user exists
        # existing_user = User.query.filter_by(email=email).first()
        # if existing_user:
        #     flash("Email already registered!")
        #     return redirect(url_for('register'))

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        # flash("Registration successful!")
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # flash("Login successful!")
            # return redirect(url_for('home'))
            session['name'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/dashboard')

        else:
            return render_template('login.html',error="Invalid credentials!")
           

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if session.get('name'):
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)