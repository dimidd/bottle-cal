#!/usr/bin/env python3
from bottle import route, run, template, redirect, static_file
import calendar
import time
import os
import pathlib
import xmltodict
from urllib.request import urlopen

CAL = calendar.HTMLCalendar(calendar.SUNDAY)
Y, M = time.strftime('%Y %m').split()
BASE_PATH = pathlib.Path(__file__).parent
PORT = int(os.environ.get("PORT", 49229))
HIST_PREF = "http://www.vizgr.org/historical-events/search.php?"
HIST_SUFF = "&html=true&format=xml"
MIN_YEAR = 2
MAX_YEAR = 9999


def get_next(year, month=None):
    next_y = year + 1 if year < MAX_YEAR else None
    next_m = None
    if month:
        next_m = month + 1
        if month == 12:
            next_m = 1
        else:
            next_y = year

    return next_y, next_m


def get_prev(year, month=None):
    prev_y = year - 1 if year > MIN_YEAR else None
    prev_m = None
    if month:
        prev_m = month - 1
        if month == 1:
            prev_m = 12
        else:
            prev_y = year

    return prev_y, prev_m


@route('/')
@route('/<year_s>/<month_s:re:\d{1,2}/>')
def mcal(year_s=Y, month_s=M):
    month_s = month_s if month_s[-1] != '/' else month_s[:-1]
    year = int(year_s)
    month = int(month_s)
    cal = CAL.formatmonth(year, month, True)
    n_y, n_m = get_next(year, month)
    p_y, p_m = get_prev(year, month)
    ad = [p_y, p_m, n_y, n_m]
    pad_y = ((4 - len(year_s)) * '0') + year_s
    pad_m = ((2 - len(month_s)) * '0') + month_s
    url_mid = "begin_date={}{}01&end_date={}{}31".format(pad_y, pad_m, pad_y, pad_m)
    ev_file = urlopen(HIST_PREF + url_mid + HIST_SUFF)
    data = ev_file.read()
    ev_file.close()
    events = []
    if data != b'No events found for this query.':
        events_xml = xmltodict.parse(data)
        events = events_xml["result"]["event"]
        events = [events] if type(events) != list else events
    return template('cal', cal=cal, adjacent=ad, events=events)


@route('/<year:re:\d{4}/>')
def ycal(year):
    year = int(year[:-1])
    n_y, n_m = get_next(year)
    p_y, p_m = get_prev(year)
    ad = [p_y, p_m, n_y, n_m]
    return template('cal', cal=CAL.formatyear(year, 5), adjacent=ad)


@route('<path:re:.+[^/]$>')
def add_slash(path):
    return redirect(path + "/")


@route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=str(BASE_PATH / 'assets'))


run(host='0.0.0.0', port=PORT, debug=False)
