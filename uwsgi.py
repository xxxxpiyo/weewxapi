# -*- coding:utf-8 -*-
# Updated: 2014/04/17
 
# Flaskアプリケーショントップのパスをpathに追加
import sys, os
sys.path.append('/usr/local/webapp/weewxapi') 
 
from weewxapi import app as application
