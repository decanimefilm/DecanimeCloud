import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # 🚨 Ini WAJIB kalau deploy di Zeabur/Replit

from flask import Flask, redirect, request, session, url_for
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import os

app = Flask(__name__)
app.secret_key = 'rahasia-bro'  # ganti di production

# GANTI SESUAI DATA KAMU
CLIENT_ID = '129791644041-km8ro654n14blt1dboqdi37o3ju92bhf.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'https://decanimecloud.zeabur.app/oauth2callback'
FILE_ID_TO_COPY = '1hPI1l9cXJw5CGTMuV2P2dvHneAXz-gqW'

SCOPES = ['https://www.googleapis.com/auth/drive.file']

@app.route('/')
def index():
    return '<a href="/auth">Login with Google & Copy File</a>'

@app.route('/auth')
def auth():
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
        state=state
    )
    flow.redirect_uri = REDIRECT_URI
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    service = build('drive', 'v3', credentials=credentials)

    copied_file = service.files().copy(
        fileId=FILE_ID_TO_COPY,
        body={"name": "Copy dari Bot"}
    ).execute()

    return f'✅ File berhasil dicopy! <br>ID: {copied_file["id"]}'

if __name__ == '__main__':
    app.run(debug=True)
