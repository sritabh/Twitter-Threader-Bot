import os
from os import environ
def googleCreds():
    creds = {
    "type": "service_account",
    "project_id": "twitter-threader",
    "private_key_id": environ["private_key_id"],
    "private_key": environ["private_key"],
    "client_email": environ["client_email"],
    "client_id": environ["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-rh7d4%40twitter-threader.iam.gserviceaccount.com"
    }
    return creds