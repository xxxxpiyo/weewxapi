# -*- coding: utf-8 -*-

import datetime

def getDate(unixTime=None, format="%Y-%m-%d %H:%M:%S"):
  if unixTime == None:
    date = datetime.datetime.today()
  else:
    date = datetime.fromtimestamp(unixTime)

  return date.strftime(format)

def getDate2UT(date=None):
    if date == None:
        d = getDate(None, "%Y-%m-%d")
    else:
        d = date

    dt = datetime.datetime.strptime(d + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    return dt.strftime('%s')