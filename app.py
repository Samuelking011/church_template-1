from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Added for database migrations

app = Flask(__name__)
#app.secret_key = 'your_secret_key'  # Change this to a random, secure string
app.config['SECRET_KEY'] = 'abc110@516!!k89' # Change this to a random, secure string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://your_mysql_user:your_mysql_password@your_mysql_host/your_mysql_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize migration engine

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

#MySQL Configuration
'''mysql_db = mysql.connector.connect(
    host="your_mysql_host",
    user="your_mysql_user",
    password="your_mysql_password",
    database="your_mysql_database"

)
mysql_cursor = mysql_db.cursor()

#Create a table for prayer requests
mysql_cursor.execute("""
    CREATE TABLE IF NOT EXISTS prayer_requests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        request_text TEXT NOT NULL
    )
""")
mysql_db.commit()
'''

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)

# Callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the PrayerRequst model
class PrayerRequest(db.Model):
    __tablename__ = 'prayer_requests'  # Specify the actual table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    request_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Added foreign key relationship

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/about_us')
def about_us():
    return render_template('html/about_us.html')

@app.route('/contact_us')
def contact_us():
    return render_template('html/contact_us.html')

@app.route('/events')
def events():
    return render_template('html/events.html')

# Route for fetching prayer requests
@app.route('/prayer_request')
@login_required
def prayer_request():
    # Fetch prayer requests of the logged-in user from the database
    prayer_requests = PrayerRequest.query.filter_by(user_id=current_user.id).all()
   
    # Print debug information
    print("Current User ID:", current_user.id)
    print("Prayer Requests:", prayer_requests)

    return render_template('html/prayer_request.html', prayer_requests=prayer_requests, current_user=current_user)
    #prayer_requests = PrayerRequest.query.all()
    #return render_template('html/prayer_request.html', prayer_requests=prayer_requests, current_user=current_user)



# Route for submitting a prayer request
@app.route('/submit_prayer_request', methods=['POST'])
@login_required
def submit_prayer_request():
        name = request.form['name']
        request_text = request.form['request_text']

        # Input validation
        if not name or not request_text:
            flash('Please fill in all field.', 'error')
            return redirect(url_for('prayer_request'))
        
        try:
            #Insert the prayer request into the database
            new_prayer_request = PrayerRequest(name=name, request_text=request_text, user_id=current_user.id)
            db.session.add(new_prayer_request)
            db.session.commit()

            flash('Prayer request submitted successfully!', 'success')
        except Exception as e:
            flash(f"Error: {str(e)}", 'error')

        return redirect(url_for('prayer_request'))
    
<<<<<<< HEAD

# Additional routes for authentication
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Use a different variable name for the query result
        queried_user = User.query.filter_by(username=username).first()

        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash('You are now logged in. Welcome back!', 'success')
            return redirect(url_for('prayer_request'))
        else:
            flash('Login failed. Please check your username and password.', 'error')
    
    return render_template('html/login.html')
        
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))

# Route for user registration
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Input validation
        if not username or not password:
            flash('All fields must be filled out.','error')
            return redirect(url_for('register'))
        
        # Check that the username is taken or unique
        if User.query.filter_by(username=username).first():
            flash('Username already taken. Please choose a different one.', 'error')
            return redirect(url_for('register'))
        
        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user and add to the database
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful: You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('html/register.html')

# Custom error handler for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message='Page not found', error=e), 404

# Custom error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message="Internal server error", error=e), 500
=======
>>>>>>> 5803338651d10e6bf5aa2182230722978c6e5c06

        # Insert the prayer request into the database
        #cursor.execute("INSERT INTO prayer_requests (name, request_text) VALUES (%s, %s)", (name, request_text))
        #db.commit()

        #return redirect(url_for('prayer_request'))
#Run the application
if __name__ == '__main__':
    app.run(debug=True)
