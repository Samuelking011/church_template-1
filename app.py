from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
