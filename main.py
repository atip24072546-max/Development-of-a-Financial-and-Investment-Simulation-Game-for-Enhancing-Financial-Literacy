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
    print("-" *30)
    print("          เริ่มต้นระบบจำลองการเงิน")
    print("-" *30)

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

    print("\n" + "-" *30)
    print("           ระบบกำลังประมวลผลข้อมูล...")
    print("-" *30 + "\n")

    net_cashflow_monthly = income_monthly - expenses_monthly
    net_cashflow_annual = net_cashflow_monthly * 12
    emergency_fund_months = (savings / expenses_monthly) if expenses_monthly > 0 else 0
    dti = (debt / (income_monthly *12)) * 100 if income_monthly > 0 else 0

    print(f"• กระแสเงินสดสุทธิรายเดือน: {format_currency(net_cashflow_monthly)}")
    print(f"• กระแสเงินสดสุทธิรายปี: {format_currency(net_cashflow_annual)}")
    print(f"• จำนวนเดือนที่สามารถรองรับค่าใช้จ่ายฉุกเฉิน: {emergency_fund_months:.1f} เดือน")
    print(f"• อัตราส่วนหนี้สินต่อรายได้: {dti:.1f}%")

    