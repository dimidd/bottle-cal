#!/usr/bin/env python3
from bottle import route, run, template, redirect, static_file
import calendar
import time
import os
import pathlib

CAL = calendar.HTMLCalendar(calendar.SUNDAY)
Y, M = time.strftime('%Y %m').split()
BASE_PATH = pathlib.Path(__file__).parent
PORT = int(os.environ.get("PORT", 5000))
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
@route('/<year>/<month:re:\d{1,2}/>')
def mcal(year=Y, month=M):
    year = int(year)
    month = int(month[:-1])
    n_y, n_m = get_next(year, month)
    p_y, p_m = get_prev(year, month)
    ad = [p_y, p_m, n_y, n_m]
    return template('cal', cal=CAL.formatmonth(year, month, True), adjacent=ad)


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


run(host='localhost', port=PORT, debug=True)
