import os
import io
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# 1. Scopes define permissions (read-only access here)
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# 2. Global metadata store
metadata_list = []

# 3. Authenticate user and store token
def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# 4. Create local folder if needed
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_file(service, file_id, file_name, save_path):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(os.path.join(save_path, file_name), 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Downloading {file_name}: {int(status.progress() * 100)}%")

def crawl_and_download(service, folder_id, local_path):
    ensure_dir(local_path)
    query = f"'{folder_id}' in parents and trashed = false"
    response = service.files().list(
        q=query,
        fields='files(id, name, mimeType, size, createdTime, modifiedTime, webViewLink, owners)',
    ).execute()

    for file in response.get('files', []):
        file_id = file['id']
        name = file['name']
        mime_type = file.get('mimeType', '')
        size = file.get('size', 'Unknown')
        created_time = file.get('createdTime', '')
        modified_time = file.get('modifiedTime', '')
        web_view_link = file.get('webViewLink', '')
        owner_email = file.get('owners', [{}])[0].get('emailAddress', 'Unknown')

        metadata_list.append({
            'File Name': name,
            'File ID': file_id,
            'MIME Type': mime_type,
            'Size (Bytes)': size,
            'Created Time': created_time,
            'Modified Time': modified_time,
            'Owner Email': owner_email,
            'Download/View Link': web_view_link
        })

        if mime_type == 'application/vnd.google-apps.folder':
            print(f"Entering folder: {name}")
            crawl_and_download(service, file_id, os.path.join(local_path, name))
        else:
            print(f"Downloading file: {name}")
            try:
                download_file(service, file_id, name, local_path)
            except Exception as e:
                print(f"Failed to download {name}: {e}")

# 7. Write metadata to Excel
def save_metadata_to_excel(file_path='drive_metadata.xlsx'):
    df = pd.DataFrame(metadata_list)
    df.to_excel(file_path, index=False)
    print(f"\n✅ Metadata written to: {file_path}")

# 8. Main function
def main():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    folder_id = '100EiwDTz41Z5rqLSfbk0PtjKZVGnLO4t'  # 🔁 Replace with your folder ID
    download_root = 'drive_downloads'
    crawl_and_download(service, folder_id, download_root)
    save_metadata_to_excel()

if __name__ == '__main__':
    main()


