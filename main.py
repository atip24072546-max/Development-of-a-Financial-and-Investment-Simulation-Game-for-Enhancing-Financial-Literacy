"""
main.py - Web Server (Flask) สำหรับเกมจำลองการเงินและการลงทุน
เชื่อมต่อ UI (HTML/CSS) กับ Game Engine และแบบจำลองการเงิน
"""
import uuid
import sys
from flask import Flask, render_template, request, session, redirect, url_for
from game_engine import FinancialGameEngine, PlayerProfile
import simulation

app = Flask(__name__)
app.secret_key = "financial-simulation-game-secret-key-2026"

# บันทึก Engine ของแต่ละเซสชันผู้เล่น
engines = {}

def get_engine():
    eid = session.get("engine_id")
    return engines.get(eid) if eid else None

@app.route("/", methods=["GET"])
def index():
    """หน้า 1: กรอกข้อมูลผู้เล่น"""
    return render_template("index.html", step=1)

@app.route("/goals", methods=["POST"])
def goals():
    """หน้า 2: รับข้อมูลผู้เล่นจากหน้า 1 -> แสดงหน้ากำหนดเป้าหมาย"""
    try:
        session["age"] = int(request.form.get("age", 25))
        session["income"] = float(request.form.get("income", 30000))
        session["expenses"] = float(request.form.get("expenses", 18000))
        session["savings"] = float(request.form.get("savings", 50000))
        session["debt"] = float(request.form.get("debt", 0))
    except (ValueError, TypeError):
        return render_template("index.html", step=1, error="กรุณากรอกข้อมูลตัวเลขให้ถูกต้องครบถ้วน")

    return render_template("index.html", step=2)

@app.route("/analyze", methods=["POST"])
def analyze():
    """หน้า 3: รับข้อมูลเป้าหมาย -> ประมวลผลและแสดงสถานะทางการเงิน"""
    try:
        retirement_age = int(request.form.get("retirement_age", 60))
        duration = int(request.form.get("duration", 20))
        target_wealth_raw = request.form.get("target_wealth", "5000000")
        target_wealth = float(target_wealth_raw) if target_wealth_raw else 5000000.0
        target_text = request.form.get("target_wealth_text", "").strip() or "มีเงินเก็บเพื่อการเกษียณและมีอิสรภาพทางการเงิน"

        session["retirement_age"] = retirement_age
        session["duration"] = duration
        session["target_wealth"] = target_wealth
        session["target_text"] = target_text
    except (ValueError, TypeError):
        return render_template("index.html", step=2, error="กรุณากรอกข้อมูลเป้าหมายให้ถูกต้อง")

    # สร้าง PlayerProfile และ Engine
    profile = PlayerProfile(
        age=session.get("age", 25),
        income_monthly=session.get("income", 30000.0),
        expenses_monthly=session.get("expenses", 18000.0),
        savings=session.get("savings", 50000.0),
        debt=session.get("debt", 0.0),
        sim_duration=duration,
        retirement_age=retirement_age,
        target_wealth=target_wealth
    )

    engine = FinancialGameEngine(profile, use_dynamic_economy=True)
    engine.start_game()

    eid = str(uuid.uuid4())
    session["engine_id"] = eid
    engines[eid] = engine

    # จัดเตรียมข้อมูลสรุปสถานะการเงินสำหรับแสดงในหน้า 3
    net_monthly = engine.net_cashflow_monthly
    savings = profile.savings
    debt = profile.debt
    savings_to_debt = (savings / debt) if debt > 0 else (savings if savings > 0 else 0.0)
    readiness_pct = min(100.0, (savings / (profile.expenses_monthly * 6.0)) * 100.0) if profile.expenses_monthly > 0 else 100.0

    health_data = {
        "income": simulation.format_currency(profile.income_monthly),
        "expenses": simulation.format_currency(profile.expenses_monthly),
        "net_monthly": simulation.format_currency(net_monthly),
        "savings": simulation.format_currency(savings),
        "debt": simulation.format_currency(debt),
        "duration": f"{duration} ปี",
        "retirement_age": f"{retirement_age} ปี",
        "target_text": target_text,
        "savings_to_debt": f"{savings_to_debt:.1f} เท่า" if debt > 0 else "ไม่มีหนี้สิน",
        "readiness_pct": f"{readiness_pct:.1f}%",
        "dti": f"{engine.dti:.1f}%",
        "emergency_months": f"{engine.emergency_fund_months:.1f} เดือน",
        "risk_level": engine.risk_level,
        "invest_capacity": simulation.format_currency(engine.annual_invest_capacity),
        "is_negative": net_monthly <= 0
    }

    return render_template("index.html", step=3, health=health_data)

@app.route("/step", methods=["POST", "GET"])
def step_year():
    """หน้า 4: ก้าวไปปีถัดไป และแสดงแดชบอร์ดการเงินรายปี"""
    engine = get_engine()
    if not engine:
        return redirect(url_for("index"))

    snap = None
    if not engine.is_finished():
        snap = engine.step_year()
    elif len(engine.history) > 0:
        snap = engine.history[-1]

    if snap:
        snap_data = {
            "year": snap.year,
            "age": snap.age,
            "cash": simulation.format_currency(snap.cash),
            "savings": simulation.format_currency(snap.savings),
            "investments": simulation.format_currency(snap.investments),
            "assets": simulation.format_currency(snap.assets),
            "debt": simulation.format_currency(snap.debt),
            "net_worth": simulation.format_currency(snap.net_worth),
            "progress": f"{snap.progress:.1f}",
            "is_retired": snap.is_retired,
            "is_finished": engine.is_finished()
        }
    else:
        return redirect(url_for("summary"))

    target_wealth = session.get("target_wealth", 5000000.0)
    return render_template("index.html", step=4, snap=snap_data, target=simulation.format_currency(target_wealth))

@app.route("/summary", methods=["POST", "GET"])
def summary():
    """หน้า 5: สรุปผลลัพธ์การจำลองการเงิน"""
    engine = get_engine()
    if not engine or len(engine.history) == 0:
        return redirect(url_for("index"))

    last = engine.history[-1]
    target = session.get("target_wealth", 5000000.0)

    summary_data = {
        "total_years": last.year,
        "final_age": last.age,
        "cash": simulation.format_currency(last.cash),
        "savings": simulation.format_currency(last.savings),
        "investments": simulation.format_currency(last.investments),
        "assets": simulation.format_currency(last.assets),
        "debt": simulation.format_currency(last.debt),
        "net_worth": simulation.format_currency(last.net_worth),
        "target": simulation.format_currency(target),
        "progress": f"{last.progress:.1f}",
        "goal_reached": last.net_worth >= target
    }

    return render_template("index.html", step=5, summary=summary_data)

if __name__ == "__main__":
    print("=" * 65)
    print(" 🎮 เกมจำลองการเงินและการลงทุนเพื่อเสริมสร้างทักษะทางการเงิน")
    print(" 🌐 เปิดใช้งานเว็บเซิร์ฟเวอร์ที่: http://127.0.0.1:5000")
    print("=" * 65)
    app.run(debug=True, port=5000)
