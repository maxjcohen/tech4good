import csv

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_sheet():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('src/client_secret.json', scope)
    client = gspread.authorize(creds)
    # Make sure you use the right name here !
    return client.open("Questionnaire terrain Mouvement du Nid (Responses)").sheet1

def save_csv(sheet):
    # Extract and print all of the values
    with open('src/data.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(sheet.get_all_values())

def load_gspread():
    save_csv(get_sheet())