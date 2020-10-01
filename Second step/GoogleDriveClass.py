from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from apiclient import errors
import io
from typing import Optional


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
TYPE2MIME_DICT = {'txt': 'text/plain',
                  'folder': 'application/vnd.google-apps.folder'}


class GoogleClient:
    def __init__(self):
        self.default_page_size = 1000
        self.service = self.login()
        self.files = []
        self.folders = []

    def login(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        return service

    def list_files(self, file_num: int=100, query='', verbose: bool =False):
        # Call the Drive v3 API
        results = self.service.files().list(pageSize=file_num, q=query, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            if verbose:
                print('Files:')
                for item in items:
                    print(u'Got {0} ({1} - {2})'.format(item['name'], item['id'], item['mimeType']))
            print(f"Loaded {len(items)} files into `client.files`")

    def get_all_files(self, file_type: str='', folder_name: str=None, substring: Optional[str]=None,
                      save: bool=True):
        params = {
            'pageSize': self.default_page_size,
            'fields': "nextPageToken, files(id, name)"
        }
        if file_type:
            params['q'] = f"mimeType='{TYPE2MIME_DICT[file_type]}'"
        if folder_name:
            folder_id = self.get_folder_id(folder_name)
            if params.get('q'):
                params['q'] = params['q']+f" and parents in '{folder_id}'"
            else:
                params['q'] = f"parents in '{folder_id}'"
        if substring:
            if params.get('q'):
                params['q'] = params['q'] + f" and fullText contains '{substring}'"
            else:
                params['q'] = f"fullText contains '{substring}'"
        page_token = None

        results = []
        while True:
            try:
                if page_token:
                    params['pageToken'] = page_token
                files = self.service.files().list(**params).execute()

                results.extend(files['files'])
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except errors.HttpError as  error:
                print('An error occurred: %s' % error)
                break
        if save:
            self.files = results
        return results

    def get_all_folders(self, to_print: bool=False):
        folders = self.get_all_files(file_type='folder', save=False)
        if to_print:
            for folder in folders:
                print(folder)
        self.folders=folders
        return folders

    def get_folder_id(self, folder_name: str) -> Optional[str]:
        """
        Finds the folder name by folder id
        Args:
            folder_name: The name of the folder

        Returns:
            a string of the folder id
        """
        if not self.folders:
            self.get_all_folders()
        for folder_dict in self.folders:
            if folder_dict.get('name') == folder_name:
                return folder_dict.get('id')
        raise ValueError(f"Could not find Folder {folder_name}.")

    def download_file(self, file_id: str):
        # If read more than once make sure to run `file.seek(0)`
        # before in order to move head of file descriptor to the begining of the file
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            # print("Download %d%%." % int(status.progress() * 100))
        fh.seek(0)
        # DONT FORGET TO CLOSE fh!!
        return fh

    # `Normalized and scaled data` folder id: 1OSOnj9XW5JuwC0V_WSJqidreD-NSD6U0
    def upload_BytesIO_file(self, file_data: io.BytesIO, file_type: str, file_name: str,
                    parent_folder: str='1OSOnj9XW5JuwC0V_WSJqidreD-NSD6U0', to_close: bool=True):
        file_metadata = {
            'name': file_name,
            'mimeType': TYPE2MIME_DICT[file_type],
            'parents': [parent_folder]
        }
        media = MediaIoBaseUpload(file_data,
                                mimetype=TYPE2MIME_DICT[file_type],
                                resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        if to_close:
            file_data.close()
        print('File ID: %s' % file.get('id'))


if __name__ == '__main__':
    client = GoogleClient()
    client.get_all_folders(to_print=True)
    
