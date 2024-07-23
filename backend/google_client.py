import requests
import datetime

# Replace with your actual access token
ACCESS_TOKEN = "ya29.a0AXooCgsThHqnUYevh_BS-XhYSIe_akhHojUdWcz2BgELtvb0MtNbVGTfNdpTVkjEusoVeVYfbnnNOx6qWF9fRA1WJv3-Pj4swBP59CY9xqT1k8FvEzIXFypwKezyUWvgyy3lNd5quZnB4Mry-hw6ieTKGewA4dCB7TxFaCgYKAVsSARASFQHGX2Mi4YhSqzG_duy5ulpPvVkj1w0171"

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/calendar.events']

def get_token():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
                return token


def get_upcoming_events(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    
    params = {
        "calendarId": "primary",
        "timeMin": now,
        "maxResults": 10,
        "singleEvents": True,
        "orderBy": "startTime"
    }
    
    response = requests.get(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        events = response.json().get("items", [])
        if not events:
            print("No upcoming events found.")
        else:
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])
    else:
        print(f"An error occurred: {response.status_code}")
        print(response.text)

def create_event(token, summary, location, description, start_date_time:str, end_date_time:str, attendee_emails:list, timezone_region:str ="America/Los_Angeles", email_reminder_minutes_ahead: int = 1440, freq: str="DAILY", count: int="1"):
    # date_time has to be in ISO 8601 "2015-05-28T09:00:00-07:00"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Define the event details
    event = {
        "summary": summary,
        "location": location,
        "description": description,
        "start": {
            "dateTime": start_date_time,
            "timeZone": timezone_region,
        },
        "end": {
            "dateTime": end_date_time,
            "timeZone": timezone_region,
        },
        "recurrence": [
            f"RRULE:FREQ={freq};COUNT={count}"
        ],
        "attendees": [ 
            [{"email" : email} for email in attendee_emails]
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": email_reminder_minutes_ahead},
                {"method": "popup", "minutes": 10},
            ],
        },
    }

    # Make the API request
    response = requests.post(
        "https://www.googleapis.com/calendar/v3/calendars/primary/events",
        headers=headers,
        json=event
    )

    if response.status_code == 200:
        print("Event created: %s" % response.json()["htmlLink"])
    else:
        print(f"An error occurred: {response.status_code}")
        print(response.text)

# if __name__ == "__main__":

if __name__ == "__main__":
    # token = get_token()
    # print(f"Access Token: {token}")

    get_upcoming_events(token=ACCESS_TOKEN)
    create_event(
        token=ACCESS_TOKEN,
        summary="Team Meeting",
        location="123 Main St, Anytown, USA",
        description="Monthly team meeting to discuss project updates.",
        start_date_time="2024-08-01T10:00:00-07:00",
        end_date_time="2024-08-01T11:00:00-07:00",
        attendee_emails=["alice@example.com", "bob@example.com"]
    )
    get_upcoming_events(token=ACCESS_TOKEN)


