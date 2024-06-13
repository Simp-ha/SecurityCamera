import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'C:/Users/bdouk/Security_Camera/client_secret_333182355234-f17n8hrrobs9tp6cbirbq6q351p00e8t.apps.googleusercontent.com.json'  # Path to your OAuth 2.0 credentials JSON file
TOKEN_FILE = 'token.json'  # File to store the user's access and refresh tokens

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_video_to_drive(filename):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': filename}
    media = MediaFileUpload(filename, mimetype='video/mp4')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')

    # Generate shareable link
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=file_id, body=permission).execute()
    url = f"https://drive.google.com/file/d/%7Bfile_id%7D/view?usp=sharing"
    return url
