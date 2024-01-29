import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def main():
  """
  Modified basic API example
  Retrieves wanted values from our target spreadsheet and 
  Uses them to update the csv usable from other scripts
  """
  creds = None
  secrets_file = os.path.join(os.getcwd(), "client_secret.json")
  if os.path.exists(secrets_file):
    creds = service_account.Credentials.from_service_account_file(secrets_file, scopes=SCOPES)

  sheet_id = ""
  cell_range = "" 
  with open("sheet_id.json", "r") as f:    
    decoded = json.loads(f.read())
    sheet_id = decoded['id']
    cell_range = decoded['range']

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=sheet_id, range=cell_range)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return
    users = []
    for user in values[0]:
        if (user.strip() == ""):
            continue
        users.append(user)

    with open("preferences.csv", "a") as f:    
        for row in values:
            while len(row) < len(users) + 1:
                row.append("")
            print(";".join(row), file=f)

  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()
