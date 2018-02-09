
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d | %H:%M:%S'
    )
logger = logging.getLogger(__name__)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials(reset=False):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')


    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')
    if reset:
        try:
            os.remove(credential_path)
        except:
            logger.info("Error in resetting credentials")
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main(date=None, period_days=7, reset=False):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    logger.info('Get credentials.')
    credentials = get_credentials(reset)
    logger.info('Authorizing credentials at google.')
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http, cache_discovery=False)

    if not date:
        date = datetime.datetime.utcnow()
        date = date.replace(hour=1)
    else:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    iso_now = date.isoformat() + 'Z' # 'Z' indicates UTC time
    week = date + datetime.timedelta(days=period_days)
    iso_week = week.isoformat() + 'Z'
    logger.info('Getting the events from {} to {}.'.format(date, week))
    eventsResult = service.events().list(
        calendarId='primary', timeMin=iso_now, timeMax=iso_week, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    classes = []
    if not events:
        logger.debug('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        description = event.get('description')
        subject = event.get('summary')
        logger.info(event.get("creator"))
        classes.append({
            'start':start,
            'end':end,
            'description':description,
            'subject':subject
        })
    logger.info('Done.')
    return classes



if __name__ == '__main__':
    print(main(reset=True))
