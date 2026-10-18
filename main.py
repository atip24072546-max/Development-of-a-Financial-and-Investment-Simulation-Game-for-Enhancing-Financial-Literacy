def format_currency(amount: float) -> str:
    return f"{amount:,.2f} บาท"

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            val = float(input(prompt))
            if val < 0:
                print("กรุณาใส่จำนวนมากกว่า 0")
                continue
            return val
        except ValueError:
            print("กรุณาใส่ตัวเลขเท่านั้น")

def get_positive_int(prompt: str) -> int:
    while True:
        try:
            val = int(input(prompt))
            if val < 0:
                print("กรุณาใส่จำนวนมากกว่า 0")
                continue
            return val
        except ValueError:
            print("กรุณาใส่ตัวเลขจำนวนเต็มเท่านั้น")

def main():
    print("-" *100)
    print("          เริ่มต้นระบบจำลองการเงิน")
    print("-" *100)

    print("\n--- กรอกข้อมูลผู้เล่น ---")
    age = get_positive_int("อายุของผู้เล่น (ปี): ")
    income_monthly = get_positive_float("รายได้ต่อเดือน (บาท): ")
    expenses_monthly = get_positive_float("ค่าใช้จ่ายต่อเดือน (บาท): ")
    savings = get_positive_float("เงินออมปัจจุบัน (บาท): ")
    debt = get_positive_float("หนี้สินปัจจุบัน (บาท): ")

    print("\n--- กำหนดเป้าหมายทางการเงิน ---")
    sim_duration = get_positive_int("ระยะเวลาจำลอง (เดือน): ")
    retirement_age = get_positive_int("อายุที่ต้องการเกษียณ (ปี): ")
    target_wealth = get_positive_float("เป้าหมายความมั่งคั่ง (บาท): ")

    print("\n" + "-" *100)
    print("           ระบบกำลังประมวลผลข้อมูล...")
    print("-" *100 + "\n")

    net_cashflow_monthly = income_monthly - expenses_monthly
    net_cashflow_annual = net_cashflow_monthly * 12
    emergency_fund_months = (savings / expenses_monthly) if expenses_monthly > 0 else 0
    dti = (debt / (income_monthly *12)) * 100 if income_monthly > 0 else 0

    print(f"• กระแสเงินสดสุทธิรายเดือน: {format_currency(net_cashflow_monthly)}")
    print(f"• กระแสเงินสดสุทธิรายปี: {format_currency(net_cashflow_annual)}")
    print(f"• จำนวนเดือนที่สามารถรองรับค่าใช้จ่ายฉุกเฉิน: {emergency_fund_months:.1f} เดือน")
    print(f"• อัตราส่วนหนี้สินต่อรายได้: {dti:.1f}%")

    if net_cashflow_monthly <= 0:
        print("\n[คำเตือน] คุณมีรายจ่ายมากกว่ารายได้ ควรปรับลดกรายจ่ายก่อนเริ่มลงทุน")

    print("\n"+ "-" *100)
    print("          คำนวณระดับความมเสี่ยงและความสามารถในการลงทุน...")
    print("-" *100 + "\n")

    if age < 35 and debt == 0:
        risk_level = "สูง"
        expected_return_rate = 0.08
    elif age < 50 and dti < 30:
        risk_level = "ปานกลาง"
        expected_return_rate = 0.05
    else:
        risk_level = "ต่ำ"
        expected_return_rate = 0.03

    annual_invest_capacity = max(0.0, net_cashflow_annual * 0.6)

    print(f"• ระดับความเสี่ยงที่เหมาะสม: {risk_level}")
    print(f"• อัตราผลตอบแทนคาดหวังเฉลี่ย: {expected_return_rate * 100:.1f}% ต่อปี")
    print(f"• ความสามารถในการลงทุนต่อปี: {format_currency(annual_invest_capacity)}")

    input("\n          กด Enter เพื่อเริ่มเข้าสู่การจำลองรายปี...")

    cash = max(0.0, net_cashflow_monthly * 3)
    investments = 0.0
    x = 0
    current_age = age

    while x < sim_duration:
        x += 1
        current_age += 1

        print("\n" + "-" *100)
        print(f"          >>> เข้าสู่ปีที่ {x} (อายุ {current_age} ปี) <<<")
        print("-" *100 + "\n")

        if debt > 0:
                repayment = min(debt, net_cashflow_annual * 0.3)
                debt -= repayment
            
        annual_savings_added = max(0.0, net_cashflow_annual * 0.2)
        savings += annual_savings_added

        investments = (investments + annual_invest_capacity) * (1 + expected_return_rate)
            

        assets = cash + savings + investments
        net_worth = assets - debt

        print(f"สถานะทางการเงินปัจจุบัน ณ สิ้นปีที่ {x}:")
        print(f"  1. เงินสด (Cash)        : {format_currency(cash)}")
        print(f"  2. เงินออม (Savings)    : {format_currency(savings)}")
        print(f"  3. เงินลงทุน (Invest)   : {format_currency(investments)}")
        print(f"  4. ทรัพย์สินรวม (Assets): {format_currency(assets)}")
        print(f"  5. หนี้สิน (Debt)       : {format_currency(debt)}")
        print(f"  --> มูลค่าความมั่งคั่งสุทธิ: {format_currency(net_worth)}")

        progress = min(100.0, (net_worth / target_wealth) * 100) if target_wealth > 0 else 0
        print(f"  --> ความคืบหน้าสู่เป้าหมาย : {progress:.2f}% (เป้าหมาย {format_currency(target_wealth)})")
        if current_age == retirement_age:
            print(f"  [แจ้งเตือน] คุณถึงอายุเกษียณ ({retirement_age} ปี) ในปีนี้แล้ว!")
        if x < sim_duration:
            choice = input("\nต้องการไปต่อปีถัดไปหรือไม่? (กด Enter เพื่อไปต่อ หรือพิมพ์ 'q' เพื่อหยุด): ").strip().lower()
        if choice == 'q':
            print("สิ้นสุดการจำลองตามคำสั่งของผู้ใช้")
            break
    print("\n" + "=" * 100)
    print("               จบการจำลองสถานะทางการเงิน")
    print("=" * 100)
if __name__ == "__main__":
    main()