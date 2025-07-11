from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from functools import wraps
import pickle
import numpy as np
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')

# MongoDB Configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/career_guidance')
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Load ML Model
try:
    with open("careerlast.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ Error: careerlast.pkl not found. Ensure it's in the project directory.")
    model = None
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Job Titles Dictionary
jobs_dict = {
    0: 'AI ML Specialist', 1: 'API Integration Specialist',
    2: 'Application Support Engineer', 3: 'Business Analyst',
    4: 'Customer Service Executive', 5: 'Cyber Security Specialist',
    6: 'Data Scientist', 7: 'Database Administrator',
    8: 'Graphics Designer', 9: 'Hardware Engineer',
    10: 'Helpdesk Engineer', 11: 'Information Security Specialist',
    12: 'Networking Engineer', 13: 'Project Manager',
    14: 'Software Developer', 15: 'Software Tester',
    16: 'Technical Writer'
}

career_links = {
    "AI ML Specialist": "https://www.ibm.com/topics/machine-learning",
    "API Integration Specialist": "https://roadmap.sh/backend",
    "Application Support Engineer": "https://roadmap.sh/product-manager",
    "Business Analyst": "https://www.iiba.org/",
    "Cyber Security Specialist": "https://roadmap.sh/cyber-security",
    "Data Scientist": "https://www.datasciencecentral.com/",
    "Database Administrator": "https://roadmap.sh/sql",
    "Graphics Designer": "https://www.coursera.org/courses?query=graphic%20design",
    "Hardware Engineer": "https://www.comptia.org/certifications/a",
    "Helpdesk Engineer": "https://roadmap.sh/best-practices/code-review",
    "Information Security Specialist": "https://roadmap.sh/cyber-security",
    "Networking Engineer": "https://roadmap.sh/r/system-engineer",
    "Project Manager": "https://www.pmi.org/certifications/project-management-pmp",
    "Software Developer": "https://roadmap.sh/software-architect",
    "Software Tester": "https://roadmap.sh/qa",
    "Technical Writer": "https://www.techtarget.com/whatis/definition/technical-writing"
}

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("You need to log in first!", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Redirect `/` to `/login`
@app.route('/')
def home_redirect():
    return redirect(url_for('login'))

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']

        # Check if the email is already registered
        existing_email = mongo.db.users.find_one({'email': email})

        if existing_email:
            flash("An account with this email already exists.Please sign in", "info")
            return redirect(url_for('login'))  # Redirect to login page

        # Check if the username is taken
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            flash("Username already taken. Try another.", "error")
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert user into the database
        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })

        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')




# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        username = request.form['username'].strip()
        password = request.form['password']

        # Find user with matching email and username
        user = mongo.db.users.find_one({'email': email, 'username': username})

        if user and bcrypt.check_password_hash(user['password'], password):
            # Store user session
            session['email'] = email
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username, email, or password. Please try again.", "error")

    return render_template('login.html')

#homeroute
@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=session.get('username'))


# About Page Route
@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

# Profile Page Route
@app.route('/profile')
@login_required
def profile():
    user = mongo.db.users.find_one({'username': session['username']})
    return render_template('profile.html', user=user)

# Career Test Route
@app.route('/career_test', methods=['GET', 'POST'])
@login_required
def career_test():
    if request.method == 'POST':
        if model is None:
            flash("Error: Career prediction model is not available.", "danger")
            return redirect(url_for('home'))

        form_data = [int(request.form[key]) for key in request.form.keys()]
        data = np.array(form_data).reshape(1, -1)

        predictions = model.predict(data)
        pred_probs = model.predict_proba(data)

        pred_probs = pred_probs > 0.05
        final_res = {i: j for i, j in enumerate(np.where(pred_probs[0])[0]) if j != predictions[0]}
        job_title = jobs_dict.get(int(predictions[0]), "Unknown Job Role")

        return render_template("testafter.html", final_res=final_res, job_dict=jobs_dict, job0=job_title, career_links=career_links)

    return render_template('career_test.html')

# Chatbot Route (OpenAI)
# Chatbot Response Route
@app.route('/chatbot_response', methods=['POST'])
@login_required
def chatbot_response():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    try:
        client = OpenAI(api_key=openai_api_key)  # Ensure API key is correct
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career guidance assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content  # Extract chatbot response
        return jsonify({"response": bot_reply})

    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        return jsonify({"response": "Sorry, there was an issue with the chatbot. Please try again later."})

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
