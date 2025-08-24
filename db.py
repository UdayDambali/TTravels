from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.exception import AppwriteException
import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv("APPWRITE_ENDPOINT")
PROJECT_ID = os.getenv("APPWRITE_PROJECT_ID")
API_KEY = os.getenv("APPWRITE_API_KEY")
DATABASE_ID = os.getenv("APPWRITE_DATABASE_ID")
COLLECTION_ID = os.getenv("APPWRITE_COLLECTION_ID")

def create_user_document(fname, lname, email, mobile):
    client = Client()
    client.set_endpoint(ENDPOINT)
    client.set_project(PROJECT_ID)
    client.set_key(API_KEY)

    databases = Databases(client)

    try:
        response = databases.create_document(
            database_id=DATABASE_ID,
            collection_id=COLLECTION_ID,
            document_id=ID.unique(),
            data={
                "fname": fname,
                "lname": lname,
                "email": email,
                "mobile": mobile
            }
        )
        print("Document created successfully:")
        print(response)
    except AppwriteException as e:
        print(f"AppwriteException: {e.message} (Code: {e.code})")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Example usage
    create_user_document(
        fname="John",
        lname="Doe",
        email="john.doe@example.com",
        mobile="1234567890"
    )
