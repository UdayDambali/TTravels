from appwrite.client import Client
from appwrite.services.account import Account
from appwrite.exception import AppwriteException
import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
API_KEY = os.getenv("APPWRITE_API_KEY")

class Auth:
    def __init__(self):
        self.client = Client()
        self.client.set_endpoint(ENDPOINT)
        self.client.set_project(PROJECT_ID)
        self.client.set_key(API_KEY)
        self.account = Account(self.client)

    def login(self, email, password):
        try:
            session = self.account.create_email_password_session(email, password)
            return session
        except AppwriteException as e:
            return {"error": e.message}
        except Exception as e:
            return {"error": str(e)}