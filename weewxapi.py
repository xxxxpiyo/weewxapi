from flask import Flask, render_template, g
from ConfigParser import SafeConfigParser
import util

app = Flask(__name__)
app.debug = True

@app.before_request
def before_request():
  g.conf = SafeConfigParser()
  g.conf.read("config.ini")


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

if __name__ == "__main__":
    app.run()
