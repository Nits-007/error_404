from flask import Flask, render_template,redirect,url_for,flash,request
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import Length, EqualTo, Email, DataRequired,ValidationError
from flask_login import login_user,LoginManager,logout_user,login_required
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config["SECRET_KEY"] = '47ee737f08449eaa9be9b532'
db = SQLAlchemy(app)
app.app_context().push()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #value = db.Column(db.String(100))
    distance_travelled = db.Column(db.Integer())
    CO2_emmission = db.Column(db.Integer())
    Fuel_Efficiency = db.Column(db.Integer())
    result = db.Column(db.Integer())
    
class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #value = db.Column(db.String(100))
    distance_travelled = db.Column(db.Integer())
    CO2_emmission = db.Column(db.Integer())
    Fuel_Efficiency = db.Column(db.Integer())
    No_passenger=db.Column(db.Integer())
    result = db.Column(db.Integer())   

    
class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    result = db.Column(db.Integer())    
    

@app.route('/car' , methods=['GET' , 'POST'])
def car_page():
    result = None
    if request.method == 'POST' :
        num1 =float(request.form.get('distance_travelled'))
        num2 = float(request.form.get('Mileage'))
        operation = request.form.get('operation')

        if operation=="petrol":
            result = num1*num2*8.87/1000
                 
        elif operation=="diesel":
            result = num1*num2*10.16/1000
                
        elif operation=="electric":
            result = num1*num2*0.54/1000
            
        elif operation=="CNG":
            result = num1*num2*5.38/1000
        
        return redirect(url_for('result',result=result))
        
    return render_template('car.html')



@app.route('/bus' , methods=['GET' , 'POST'])
def bus_page():
    result = None
    if request.method == 'POST' :
        num1 = float(request.form.get('distance_travelled'))
        num2 = float(request.form.get('Mileage'))
        num3 = float(request.form.get('No_Passenger'))
        
        operation = request.form.get('operation')

        if operation=="petrol":
        
            result = num1*num2*8.87/(num3*1000)
                 
            
        elif operation=="diesel":
            result = num1*num2*10.16/(num3*1000)
                
        elif operation=="electric":
            result = num1*num2*0.54/(num3*1000)
            
        elif operation=="CNG":
            result = num1*num2*5.38/(num3*1000)
                
        return redirect(url_for('result',result=result))       
            
    return render_template('bus.html')

@app.route('/train' , methods=['GET' , 'POST'])
def train_page():
    result = None
    if request.method == 'POST' :
        num1 = float(request.form.get('distance_travelled'))
        num2 = float(request.form.get('No_Passenger'))
        result = num1*num2*0.035/1000       
        return redirect(url_for('result',result=result))             
    return render_template('train.html')

@app.route('/aeroplane' , methods=['GET' , 'POST'])
def aeroplane_page():
    result = None
    if request.method == 'POST' :
        num1 = float(request.form.get('distance_travelled'))
        num2 = float(request.form.get('No_Passenger'))
        result = num1*num2*0.035*3/1000    
        return redirect(url_for('result',result=result))             
    return render_template('aeroplane.html')
@app.route('/animal' , methods=['GET' , 'POST'])
def animal_page():
    result = None
    if request.method == 'POST' :
        num1 = float(request.form.get('Non-Veg'))
       
        result = num1*31/1000      
        return redirect(url_for('result',result=result))             
    return render_template('animal.html')

@app.route('/household' , methods=['GET' , 'POST'])
def household_page():
    result = None
    if request.method == 'POST' :
        num1 = float(request.form.get('distance_travelled'))
        num2 = float(request.form.get('Waste_production'))
        result = num1*num2*0.7*58.8/100
                
        return redirect(url_for('result',result=result))       
            
    return render_template('hosehold.html')




@app.route('/result', methods=['GET'])
def result():
    result = request.args.get('result')
    return render_template('res1.html', result=result)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash= db.Column(db.String(length=60), nullable=False)
  
   
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)      
        



class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account') 


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in') 

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/carbon')
def carbon_page():
    return render_template('carbon.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            #print(f'There was an error with creating a user: {err_msg}')
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
            

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))



if __name__ == "__main__" :
    app.run(debug=True)