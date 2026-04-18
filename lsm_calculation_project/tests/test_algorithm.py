"""
Test: test_algorithm.py
Chay thuat toan binh phuong toi thieu tu lsm_solver.py
Doc du lieu tu du_lieu_sau_xu_ly.csv
Luu ket qua he so a, b, c vao equation_result.txt
"""

import os
import sys

# Them duong dan src vao sys.path de import duoc lsm_solver
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from lsm_solver import binh_phuong_toi_thieu


def chay_va_luu_ket_qua():
    """Chay thuat toan LSM va luu ket qua vao file."""

    # Duong dan file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "data", "du_lieu_sau_xu_ly.csv")
    output_file = os.path.join(base_dir, "output", "equation_result.txt")

    # Dam bao thu muc output ton tai
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Chay thuat toan
    kq = binh_phuong_toi_thieu(data_file)

    # In ket qua ra man hinh
    print("=== KET QUA BINH PHUONG TOI THIEU ===")
    print(f"  a = {kq['a']}")
    print(f"  b = {kq['b']}")
    print(f"  c = {kq['c']}")
    print(f"  Phuong trinh: {kq['phuong_trinh']}")
    print(f"  R^2 = {kq['R2']}")
    print(f"  SSE = {kq['SSE']}")

    # Luu ket qua vao file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("============================================================\n")
        f.write("  KET QUA BINH PHUONG TOI THIEU (LEAST SQUARES METHOD)\n")
        f.write("  Phuong trinh: y = a*x^2 + b*x + c\n")
        f.write("============================================================\n\n")

        f.write("1. CAC HE SO TIM DUOC:\n")
        f.write(f"   a = {kq['a']}\n")
        f.write(f"   b = {kq['b']}\n")
        f.write(f"   c = {kq['c']}\n\n")

        f.write("2. PHUONG TRINH:\n")
        f.write(f"   {kq['phuong_trinh']}\n\n")

        f.write("3. DANH GIA:\n")
        f.write(f"   SSE = {kq['SSE']}\n")
        f.write(f"   R^2 = {kq['R2']}\n\n")

        f.write("4. BANG SO SANH:\n")
        f.write(f"   {'x':>8}  {'y_thuc':>10}  {'y_pred':>10}  {'sai_so':>12}\n")
        f.write("   " + "-" * 44 + "\n")
        for i in range(len(kq['x_data'])):
            f.write(f"   {kq['x_data'][i]:8.2f}  {kq['y_data'][i]:10.4f}  "
                    f"{kq['y_du_doan'][i]:10.4f}  {kq['sai_so'][i]:12.6e}\n")

        f.write("\n============================================================\n")

    print(f"\nDa luu ket qua vao: {output_file}")


if __name__ == "__main__":
    chay_va_luu_ket_qua()
