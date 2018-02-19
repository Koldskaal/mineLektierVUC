import os
import requests
from flask import Flask, render_template, request
from modules.login2 import assignment_scraper
from modules.dataGatherer import Samler
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d | %H:%M:%S'
    )
logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
print(app.config['SECRET_KEY'])

@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    c = Samler('', '')
    sdata = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            formdate = request.form['date']
            formdays = request.form['days']
            logger.info(formdate)
            c.google_date = formdate
            c.period_days = int(formdays)
            logger.info(formdays)
            sdata = c.box_ordered()



        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    else:
        sdata = c.box_ordered()
    return render_template('index.html', errors=errors, results=results, sdata=sdata)

if __name__ == '__main__':
    app.run()
