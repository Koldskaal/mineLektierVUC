try:
    from modules import login2
    from modules import loginGoogle
except ImportError:
    import login2
    import loginGoogle
import dateutil.parser
import datetime
import calendar
import re
from pprint import pprint
import logging

logger = logging.getLogger(__name__)

translate = {
    'Monday':'Mandag',
    'Tuesday':'Tirsdag',
    'Wednesday': 'Onsdag',
    'Thursday': 'Torsdag',
    'Friday': 'Fredag',
    'Saturday':'Lørdag',
    'Sunday': 'Søndag'
}

class Samler():
    """ A class to collect info and organize it. """
    def __init__(self, username, password):
        self.usr = username
        self.pwd = password
        self.gdata = None
        self.assignments = None
        self.period_days = 7
        self.google_date = None

    def get_google_info(self, reset=False):
        if not self.gdata or reset:
            self.gdata = loginGoogle.main(date=self.google_date, period_days=self.period_days)
            return self.gdata
        return self.gdata

    def get_assignments(self, reset=False):
        if not self.assignments or reset:
            self.assignments = login2.assignment_scraper(self.usr, self.pwd)
            return self.assignments
        return self.assignments

    def box_ordered(self, ginfo=True, ainfo=False, reset=False):
        """ Taking the data and ordering into a dictionary that the html-page
            can read to makes the boxes.
        """
        box = {}
        later_date = []
        old_day = ""
        if ginfo:
            # Calling the data from google's calendar API
            gdata = self.get_google_info(reset)
            for d in gdata:
                # Converting date string to datetime objcet
                date = dateutil.parser.parse(d['start'])
                # Saving some variables that I need in the box
                current_date = str(date.date())
                current_day = date.day

                # Add the current date and the properties of it to box
                # Only need to do this once
                if current_date not in box.keys():
                    box[current_date] = {}
                    box[current_date]['Ugedag'] = translate[calendar.day_name[date.weekday()]]

                    test_date = datetime.datetime.today().date() + datetime.timedelta(days=15)
                    #logger.info(test_date + current_date)
                    if str(test_date) == current_date:

                        box[current_date]['Today'] = True

                    # For adding "gap" between weekends
                    # if old_day is needed because I don't have an old_day on first item
                    if old_day:
                        gap = int(current_day) - int(old_day)
                        if gap > 1:
                            box[current_date]['Dag'] = date.day
                            box[current_date]['gap'] = True
                        else:
                            box[current_date]['Dag'] = date.day
                            box[current_date]['gap'] = False
                    else:
                            box[current_date]['Dag'] = date.day
                            box[current_date]['gap'] = False

                # Getting the subject name and cutting the worthless bits off
                subject = d.get('subject')
                subject = subject.replace('1801', '')
                subject = subject[8:]

                des = d.get('description')

                # Flitering and replacing urls for html links
                if des:
                    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', des)
                    for url in urls:
                        des = des.replace(url, '<a href="{}" target="_blank">Klik her</a>'.format(url))

                # Adding homework to dict. None is added if there is none.
                if subject in box[current_date].keys():
                    if des:
                        box[current_date][subject] += " | " + des

                else:
                    box[current_date][subject] = des

                old_day = date.day

        return box

if __name__ == "__main__":
    pprint(Samler("", "").box_ordered())
