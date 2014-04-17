# -*- coding: utf-8 -*-

import datetime

def getDate(unixTime=None, format="%Y-%m-%d %H:%M:%S"):
  if unixTime == None:
    date = datetime.datetime.today()
  else:
    date = datetime.fromtimestamp(unixTime)

  return date.strftime(format)
