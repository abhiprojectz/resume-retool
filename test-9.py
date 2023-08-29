
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

def upload_pdf_to_drive(pdf_file_path, credentials_file_path):
    # Load the credentials from the JSON file
    credentials = service_account.Credentials.from_service_account_file(credentials_file_path, scopes=['https://www.googleapis.com/auth/drive'])

    # Create a Google Drive API client
    drive_service = build('drive', 'v2', credentials=credentials)

    # Set the metadata for the file
    file_metadata = {
        'name': os.path.basename(pdf_file_path),
        'mimeType': 'application/pdf'
    }

    # Create a media object for the file upload
    media = MediaFileUpload(pdf_file_path, mimetype='application/pdf')

    # Upload the file to Google Drive
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Print the file ID of the uploaded file
    print('File ID: %s' % file.get('id'))

# Example usage
pdf_file_path = 'output_result.pdf'
credentials_file_path = 'client_secret_510950996539-ukv54tj6qpemvdm6kf67362588ubrqgn.apps.googleusercontent.com.json'
upload_pdf_to_drive(pdf_file_path, credentials_file_path)
