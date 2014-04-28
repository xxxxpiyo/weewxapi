from flask import Flask, render_template, g, request
from ConfigParser import SafeConfigParser
import json
import util, db, method

app = Flask(__name__)
app.debug = True

@app.before_request
def before_request():
  g.conf = SafeConfigParser()
  g.conf.read("config.ini")
  g.con = db.MySQLConnect(
    g.conf.get("db", "host"),
    g.conf.get("db", "database"),
    g.conf.get("db", "user"),
    g.conf.get("db", "password")
  )

#@app.route("/")
#def index():
#  data = {}
#  data["name"] = g.conf.get("station", "name")
#  data["years"] = []
#  year = int(util.getDate(None, "%Y"))
#  while year >= int(g.conf.get("station", "firstyear")):
#    data["years"].append(str(year))
#    year = year - 1
#
#  return render_template("index.html", data=data)

@app.route("/api/<path:route>")
def api(route):
  path = route.split('/')
  result = 'aho'
  
  if path[0] == "max":
    result = method.max(g.con, request)

  elif path[0] == "record":
    result = method.record(g.con, request)

  elif path[0] == "year":
    result = method.year(g.con, request)

  elif path[0] == "now":
    result = method.now(g.con, request)

  elif path[0] == "day":
    result = method.day(g.con, request)

  elif path[0] == "recent":
    result = method.recent(g.con, request)

  elif path[0] == "station":
    result = method.station(g.con, request)

  elif path[0] == "windhist":
    result = method.windhist(g.con, request)

  elif path[0] == "hour":
    result = method.hour(g.con, request)

  elif path[0] == "month":
    result = method.month(g.con, request)

  return json.dumps(result)

if __name__ == "__main__":
    app.run()
