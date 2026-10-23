from flask import Flask, reder_template, session, redirect, url_for
from game_engine improt FinancialGameEngine, PlayerProfile
import simulation

app = Flask(__name__)
app.secret_key = "financial-game-secret-key"

engines = {}

def get_engine():
    eid = session.get("engine_id")
    return engines.get(eid) if eid else None

@app.route("/",methods=["GET"])
def index():
    session.clear()
    return render_template("index.html",step=1)

@app.route("/goals", methods=["POST"])
def goals():
    try:
        session["age"]      = int(request.form["age"])
        session["income"]   = float(request.form["income"])
        session["expenses"] = float(request.form["expenses"])
        session["savings"]  = float(request.form["savings"])
        session["debt"]     = float(request.form["debt"])
    except (ValueError, KeyError):
        return render_template("index.html", step=1,error="กรุณากรอกข้อมูลตัวเลขให้ครบถ้วน")
    return render_template("index.html", step=2)