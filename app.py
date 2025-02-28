from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired

app = Flask(__name__)

# Initialize the database and migration tools
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plant.db'
app.config['SECRET_KEY'] = 'Iphone99'
csrf = CSRFProtect(app)

# Initialize the database
db = SQLAlchemy(app)

# Initialize the migration tool
migrate = Migrate(app, db)

# Initialize other tools
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Load user session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

# Plant Model
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Register User
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        role = request.form['role']

        new_user = User(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration Successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Login User
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login Successful!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid Credentials!', 'danger')

    return render_template('login.html', form=form)

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    plants = Plant.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard.html', plants=plants)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

# Admin: Manage Users
@app.route('/manage_users')
@login_required
def manage_users():
    if current_user.role != "admin":
        flash("Unauthorized Access!", "danger")
        return redirect(url_for('user_dashboard'))
    
    users = User.query.all()
    return render_template('manage_users.html', users=users)

# Plant Form for Adding a New Plant
class PlantForm(FlaskForm):
    name = StringField('Plant Name', validators=[DataRequired()])
    submit = SubmitField('Add Plant')

# Add Plant
@app.route('/add_plant', methods=['GET', 'POST'])
@login_required
def add_plant():
    form = PlantForm()

    if form.validate_on_submit():
        name = form.name.data
        description = request.form['description']

        new_plant = Plant(name=name, description=description, user_id=current_user.id)
        db.session.add(new_plant)
        db.session.commit()

        flash("Plant added successfully!", "success")
        return redirect(url_for('plant_list'))

    return render_template('add_plant.html', form=form)

# List Plants
@app.route('/plant_list')
@login_required
def plant_list():
    plants = Plant.query.all()
    print("Plants:", plants)  # Debugging: Check console output
    return render_template('plant_list.html', plants=plants)


# Profile Page
@app.route('/profile')
def profile():
    return render_template('profile.html', current_user=current_user)

# Edit Profile
class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.role = form.role.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form=form)

# Delete Plant
@app.route('/delete_plant/<int:plant_id>')
@login_required
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    db.session.delete(plant)
    db.session.commit()
    flash("Plant deleted successfully!", "success")
    return redirect(url_for('plant_list'))

# View Plant Details
@app.route('/plant/<int:plant_id>')
def view_plant(plant_id):
    plant = Plant.query.get(plant_id)
    if not plant:
        return "Plant not found", 404
    return render_template('plant_details.html', plant=plant)

@app.route('/saved_plants')
def saved_plants():
    # Your code to handle saved plants
    return render_template('saved_plants.html')

@app.route('/edit_plant/<int:plant_id>', methods=['GET', 'POST'])
def edit_plant(plant_id):
    form = PlantForm()
    if form.validate_on_submit():
        # Process form data for plant_id
        name = form.name.data
        description = form.description.data
        return f'Form submitted successfully for plant {plant_id}'
    return render_template('edit_plant.html', form=form, plant_id=plant_id)


# Main entry point for the app
if __name__ == '__main__':
    app.run(debug=True)
