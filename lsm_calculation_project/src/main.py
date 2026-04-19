from pathlib import Path
from lsm_solver import binh_phuong_toi_thieu

def main():
    # Xac dinh cac duong dan dua tren vi tri cua main.py
    base_dir = Path(__file__).resolve().parent.parent
    out_file = base_dir / "output" / "equation_result.txt"
    out_file.parent.mkdir(exist_ok=True)
    
    # Chay thuat toan
    kq = binh_phuong_toi_thieu(base_dir / "data" / "du_lieu_sau_xu_ly.csv")
    
    # In ra man hinh
    print(f"=== KET QUA BINH PHUONG TOI THIEU ===\n  a = {kq['a']}\n  b = {kq['b']}\n  c = {kq['c']}\n"
          f"  Phuong trinh: {kq['phuong_trinh']}\n  R^2 = {kq['R2']}\n  SSE = {kq['SSE']}")
    
    # Tao chuoi bang so sanh cac dong
    table_rows = "".join(f"   {x:8.2f}  {y:10.4f}  {yp:10.4f}  {e:12.6e}\n" 
                         for x, y, yp, e in zip(kq['x_data'], kq['y_data'], kq['y_du_doan'], kq['sai_so']))
    
    # Ghi toan bo noi dung vao file cuc ky ngan gon bang f-string nhieu dong
    out_file.write_text(f"""============================================================
  KET QUA BINH PHUONG TOI THIEU (LEAST SQUARES METHOD)
  Phuong trinh: y = a*x^2 + b*x + c
============================================================

1. CAC HE SO TIM DUOC:
   a = {kq['a']}
   b = {kq['b']}
   c = {kq['c']}

2. PHUONG TRINH:
   {kq['phuong_trinh']}

3. DANH GIA:
   SSE = {kq['SSE']}
   R^2 = {kq['R2']}

4. BANG SO SANH:
   {'x':>8}  {'y_thuc':>10}  {'y_pred':>10}  {'sai_so':>12}
   --------------------------------------------
{table_rows}
============================================================
""", encoding="utf-8")
    
    print(f"\nDa luu ket qua vao: {out_file}")

if __name__ == "__main__":
    main()
