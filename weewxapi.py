from flask import Flask, render_template, g
from ConfigParser import SafeConfigParser
import util

app = Flask(__name__)
app.debug = True

#g.conf = SafeConfigParser().read("config.ini")

@app.route("/")
def index():
    
    return render_template("index.html",)

if __name__ == "__main__":
    app.run()
