from modules import login2
from modules import loginGoogle
#import login2
#import loginGoogle
import dateutil.parser
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
        """
        TODO: Put data into day boxes for the html.
        example - monday, has date, subjects, homeworks, maybe classroom,

        """

    def get_assignments(self, reset=False):
        if not self.assignments or reset:
            self.assignments = login2.assignment_scraper(self.usr, self.pwd)
            return self.assignments
        return self.assignments

    def box_ordered(self, ginfo=True, assinfo=False, reset=False):
        box = {}
        later_date = []
        old_day = ""
        if ginfo:
            gdata = self.get_google_info(reset)
            for d in gdata:
                date = dateutil.parser.parse(d['start'])
                current_date = str(date.date())
                current_day = date.day
                if current_date not in box.keys():
                    box[current_date] = []
                    box[current_date].append({'Ugedag':translate[calendar.day_name[date.weekday()]]})

                    if old_day:
                        gap = int(current_day) - int(old_day)
                        if gap > 1:
                            box[current_date].append({'Dag':date.day,
                                                      'gap':True})
                        else:
                            box[current_date].append({'Dag':date.day,
                                                      'gap':False})
                    else:
                        box[current_date].append({'Dag':date.day})

                subject = d.get('subject')
                subject = subject.replace('1801', '')
                subject = subject[8:]
                #print(subject)
                des = d.get('description')
                if des:
                    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', des)
                    for url in urls:
                        des = des.replace(url, '<a href="{}" target="_blank">Klik her</a>'.format(url))

                huh = next((item for item in box[current_date] if subject in item.keys()), None)
                if huh:
                    for n, i in enumerate(box[current_date]):
                        if subject in i.keys():
                            if des:
                                i[subject].append(des)
                else:
                    box[current_date].append({subject:[des]})

                old_day = date.day

            # Adding line break between gaps
            for index, dag in enumerate(later_date):
                try:
                    gap = int(later_date[index+1]) - int(dag)
                except IndexError:
                    logger.info("Reached end of list")
                if gap > 1:
                    logger.info("{} and {} is above 1".format(dag, later_date[index+1]))


        return box


#pprint(Samler('aviv0001', 'qwe123qwe').box_ordered())
