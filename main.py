import sys
from game_engine import FinancialGameEngine, PlayerProfile
from simulation import format_currency

def run_cli():
    print("-" * 100)
    print("          เริ่มต้นระบบจำลองการเงิน (CLI Mode)")
    print("-" * 100)

    try:
        age = int(input("อายุของผู้เล่น (ปี): "))
        income = float(input("รายได้ต่อเดือน (บาท): "))
        expenses = float(input("ค่าใช้จ่ายต่อเดือน (บาท): "))
        savings = float(input("เงินออมปัจจุบัน (บาท): "))
        debt = float(input("หนี้สินปัจจุบัน (บาท): "))
        
        sim_duration = int(input("ระยะเวลาจำลอง (ปี): "))
        retirement_age = int(input("อายุที่ต้องการเกษียณ (ปี): "))
        target_wealth = float(input("เป้าหมายความมั่งคั่ง (บาท): "))
    except ValueError:
        print("กรุณากรอกข้อมูลตัวเลขให้ถูกต้อง")
        return

    profile = PlayerProfile(
        age=age, income_monthly=income, expenses_monthly=expenses,
        savings=savings, debt=debt, sim_duration=sim_duration,
        retirement_age=retirement_age, target_wealth=target_wealth
    )

    engine = FinancialGameEngine(profile)
    print("\n" + "-" * 100)
    print("           ประมวลผลข้อมูลเริ่มต้น")
    print("-" * 100)
    print(f"• กระแสเงินสดสุทธิรายเดือน: {format_currency(engine.net_cashflow_monthly)}")
    print(f"• กระแสเงินสดสุทธิรายปี: {format_currency(engine.net_cashflow_annual)}")
    print(f"• จำนวนเดือนที่รองรับค่าใช้จ่ายฉุกเฉิน: {engine.emergency_fund_months:.1f} เดือน")
    print(f"• อัตราส่วนหนี้สินต่อรายได้ (DTI): {engine.dti:.1f}%")
    print(f"• ระดับความเสี่ยงที่เหมาะสม: {engine.risk_level}")
    print(f"• ผลตอบแทนคาดหวังเฉลี่ย: {engine.base_return_rate * 100:.1f}% ต่อปี")
    print(f"• ความสามารถในการลงทุนต่อปี: {format_currency(engine.annual_invest_capacity)}")

    input("\nกด Enter เพื่อเริ่มจำลองรายปี...")
    engine.start_game()

    while not engine.is_finished():
        snap = engine.step_year()
        print("\n" + "-" * 100)
        print(f"          >>> เข้าสู่ปีที่ {snap.year} (อายุ {snap.age} ปี) <<<")
        print("-" * 100)
        print(f"  1. เงินสด (Cash)        : {format_currency(snap.cash)}")
        print(f"  2. เงินออม (Savings)    : {format_currency(snap.savings)}")
        print(f"  3. เงินลงทุน (Invest)   : {format_currency(snap.investments)}")
        print(f"  4. ทรัพย์สินรวม (Assets): {format_currency(snap.assets)}")
        print(f"  5. หนี้สิน (Debt)       : {format_currency(snap.debt)}")
        print(f"  --> มูลค่าความมั่งคั่งสุทธิ: {format_currency(snap.net_worth)}")
        print(f"  --> ความคืบหน้าสู่เป้าหมาย : {snap.progress:.2f}% (เป้าหมาย {format_currency(profile.target_wealth)})")
        
        if snap.is_retired:
            print(f"  [แจ้งเตือน] คุณถึงอายุเกษียณ ({profile.retirement_age} ปี) ในปีนี้แล้ว!")

        if not engine.is_finished():
            choice = input("\nต้องการไปต่อปีถัดไปหรือไม่? (Enter ไปต่อ / 'q' เพื่อหยุด): ").strip().lower()
            if choice == 'q':
                break

    print("\n" + "=" * 100)
    print("               จบการจำลองสถานะทางการเงิน")
    print("=" * 100)

def run_streamlit():
    try:
        import streamlit as st
    except ImportError:
        print("ยังไม่ได้ติดตั้ง Streamlit กรุณารันด้วย CLI หรือติดตั้ง streamlit ด้วย pip install streamlit")
        return

    st.set_page_config(page_title="Financial Simulation Game", layout="wide")
    st.title("🎮 เกมจำลองการเงินและการลงทุนเพื่อเสริมสร้างทักษะทางการเงิน")
    # Streamlit UI implementation logic...

if __name__ == "__main__":
    if "streamlit" in sys.modules:
        run_streamlit()
    else:
        run_cli()