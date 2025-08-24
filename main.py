from flask import Flask, render_template, request, jsonify, session, redirect
from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.services.databases import Databases
from appwrite.id import ID
from db import create_user_document
from auth import Auth
from appwrite.exception import AppwriteException
import secrets
import os
from dotenv import load_dotenv

app = Flask(__name__)
# You can generate a secret key using Python's secrets module:
# import secrets
# print(secrets.token_hex(32))
# Replace 'your-secret-key-here' with the generated value.
app.secret_key = secrets.token_hex(32)  # Required for sessions


# # ---- Appwrite Setup ----
client = Client()
load_dotenv()

client.set_endpoint(os.getenv("APPWRITE_ENDPOINT"))
client.set_project(os.getenv("APPWRITE_PROJECT_ID"))
client.set_key(os.getenv("APPWRITE_API_KEY"))

account = Account(client)
databases = Databases(client)


@app.route("/")
def index():
    return redirect("/index.html")

@app.route("/index.html")
def index_html():
    return render_template("index.html")

# # Signup page route
# @app.route("/signup", methods=["GET"])
# def signup():
#     return render_template("signup.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fname = request.form.get("firstName", "").strip()
        lname = request.form.get("lastName", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirmPassword", "")
        mobile = request.form.get("mobile", "").strip()

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match")
        
        # user = account.create(ID.unique(), email, password, f"{fname} {lname}")

        # # You do NOT need to create the Appwrite user here since you are using create_user_document from db.py.
        # # Remove the following block if you are not using Appwrite Account API directly:
        # # user = account.create(
        # #     ID.unique(),
        # #     email,
        # #     password,
        # #     f"{fname} {lname}"
        # # )

        # # Store profile data in DB using db.py
        # create_user_document(fname, lname, email, mobile)

        # # Log user in by storing user ID in session
        # session['user_id'] = user['$id']

        # return redirect("/hotel3.html")
    
        try:
            user = account.create(ID.unique(), email, password, f"{fname} {lname}")
            create_user_document(fname, lname, email, mobile)
            session['user_id'] = user['$id']
            return redirect("/login")
        except AppwriteException as e:
            # Show Appwrite error (like invalid password) on the signup page
            return render_template("signup.html", error=f"Signup failed: {e.message}")
        except Exception as e:
            # Show any other error
            return render_template("signup.html", error=f"Signup failed: {str(e)}")

    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            error = 'Please enter email and password.'
            return render_template('login.html', error=error)

        auth = Auth()
        result = auth.login(email, password)
        print('Login result:', result)  # Debug print
        if isinstance(result, dict) and 'error' in result:
            error = result['error']
            print('Login error:', error)  # Debug print
        else:
            session['user_id'] = result['userId'] if 'userId' in result else None
            print('Login successful, redirecting to index.html')  # Debug print
            return redirect("/index.html")

    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run(debug=True)