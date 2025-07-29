import os.path
import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def get_gmail_service():
    """
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as e:
                print(f"Error refreshing token: {e}")
                # If refresh fails, force re-authentication
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def create_gmail_draft(service, to: str, subject: str, body: str) -> str:
    """Create and insert a draft email.
    
    Args:
        service: Authorized Gmail API service instance.
        to: Email address of the receiver.
        subject: The subject of the email.
        body: The body of the email.

    Returns:
        A string indicating success or failure.
    """
    try:
        message = EmailMessage()
        message.set_content(body)
        message["To"] = to
        message["Subject"] = subject

        # Encode the message in base64url
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"message": {"raw": encoded_message}}
        
        draft = (
            service.users()
            .drafts()
            .create(userId="me", body=create_message)
            .execute()
        )

        return f"Draft created successfully. Draft ID: {draft['id']}"

    except HttpError as error:
        return f"An error occurred while creating the draft: {error}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    # This is for testing the functions directly
    # 1. Make sure you have your credentials.json in the same directory.
    # 2. Run this file: python multi_agent_cli/gmail_tools.py
    # 3. It will open a browser for you to authenticate.
    # 4. After authentication, it will create a draft in your Gmail.
    gmail_service = get_gmail_service()
    if gmail_service:
        result = create_gmail_draft(
            gmail_service,
            to="test@example.com",
            subject="Test Draft from Gmail API",
            body="This is a test email draft created by the Python script."
        )
        print(result)
