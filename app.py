from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

#MySQL Configuration
db = mysql.connector.connect(
    host="your_mysql_host",
    user="your_mysql_user",
    password="your_mysql_password",
    database="your_mysql_database"
)
cursor = db.cursor()

#Create a table for prayer requests
cursor.execute("""
    CREATE TABLE IF NOT EXISTS prayer_requests (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        request_text TEXT NOT NULL
    )
""")
db.commit()


# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_us')
def about_us():
    return render_template('html/about_us.html')

@app.route('/contact_us')
def contact_us():
    return render_template('html/contact_us.html')

@app.route('/events')
def events():
    return render_template('html/events.html')

@app.route('/prayer_request')
def prayer_request():
    #Fetch prayer requests from the database
    cursor.execute("SELECT * FROM prayer_requests")
    prayer_requests = cursor.fetchall()
    return render_template('html/prayer_request.html', prayer_requests=prayer_requests)

# Route for submitting a prayer request
@app.route('/submit_prayer_request', methods=['POST'])
def submit_prayer_request():
    if request.method == 'POST':
        name = request.form['name']
        request_text = request.form['request_text']

        # Insert the prayer request into the database
        cursor.execute("INSERT INTO prayer_requests (name, request_text) VALUES (%s, %s)", (name, request_text))
        db.commit()

        return redirect(url_for('prayer_request'))

if __name__ == '__main__':
    app.run(debug=True)
