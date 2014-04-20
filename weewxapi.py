from flask import Flask, render_template, g
from ConfigParser import SafeConfigParser
import util, db

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

@app.route("/")
def index():
  data = {}
  data["name"] = g.conf.get("station", "name")
  data["years"] = []
  year = int(util.getDate(None, "%Y"))
  while year >= int(g.conf.get("station", "firstyear")):
    data["years"].append(str(year))
    year = year - 1

  return render_template("index.html", data=data)

@app.route("/api/<path:route>")
def api(route):
  return route

if __name__ == "__main__":
    app.run()
