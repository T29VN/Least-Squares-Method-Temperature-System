"""
main.py -- Chuong trinh chinh: Binh phuong toi thieu (Least Squares Method)

Chay full pipeline:
    1. Doc du lieu tu file CSV
    2. Thuc hien hoi quy da thuc bac 2:  y = a*x^2 + b*x + c
    3. Tinh day du cac chi so thong ke (Fraction — chinh xac tuyet doi)
    4. Xuat bao cao chi tiet ra file TXT
    5. Tao bieu do chuyen nghiep (PNG)

Cach su dung:
    python main.py
    python main.py --data "duong/dan/file.csv"
    python main.py --help
"""

import argparse
import sys
import time
from pathlib import Path
from decimal import Decimal, getcontext
from fractions import Fraction

# Them thu muc src vao sys.path de import duoc cac module
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lsm_solver import binh_phuong_toi_thieu, fraction_sang_decimal
from visualizer import tao_bieu_do_tong_hop

# Do chinh xac hien thi
getcontext().prec = 50


# ============================================================
#  1. CAU HINH DUONG DAN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATA = BASE_DIR / "data" / "du_lieu_sau_xu_ly.csv"
OUTPUT_DIR = BASE_DIR / "output"


# ============================================================
#  TIEN ICH: DINH DANG SO
# ============================================================

def fmt_frac(val, chu_so=30):
    """Dinh dang Fraction thanh chuoi Decimal voi nhieu chu so."""
    if isinstance(val, Fraction):
        d = fraction_sang_decimal(val, chu_so + 5)
    elif isinstance(val, Decimal):
        d = val
    else:
        d = Decimal(str(val))
    return format(d, f'.{chu_so}g')


def fmt_phan_tram(val, chu_so=6):
    """Dinh dang gia tri phan tram."""
    if isinstance(val, Fraction):
        return format(float(val), f'.{chu_so}f')
    return format(val, f'.{chu_so}f')


# ============================================================
#  2. TAO BAO CAO VAN BAN
# ============================================================

def tao_bao_cao(kq, duong_dan_luu):
    """
    Tao bao cao ket qua chi tiet va luu vao file TXT.
    Hien thi cac he so voi do chinh xac cao (30 chu so co nghia).
    """
    tk = kq['thong_ke']
    n = kq['so_diem']
    sep = "=" * 72

    lines = []
    lines.append(sep)
    lines.append("  KET QUA BINH PHUONG TOI THIEU (LEAST SQUARES METHOD)")
    lines.append("  Mo hinh:  y = a*x^2 + b*x + c")
    lines.append("  Tinh toan: fractions.Fraction (chinh xac tuyet doi)")
    lines.append(sep)
    lines.append("")

    # --- 1. HE SO (DO CHINH XAC CAO) ---
    lines.append("1. CAC HE SO HOI QUY (DO CHINH XAC CAO - 30 CHU SO):")
    lines.append("")
    lines.append(f"   a (x^2) = {kq['a_decimal']}")
    lines.append(f"   b (x)   = {kq['b_decimal']}")
    lines.append(f"   c       = {kq['c_decimal']}")
    lines.append("")
    lines.append("   Phan so chinh xac (tu/mau):")
    lines.append(f"   a = {kq['a_fraction']}")
    lines.append(f"   b = {kq['b_fraction']}")
    lines.append(f"   c = {kq['c_fraction']}")
    lines.append("")

    # --- 2. HE SO KEM SAI SO CHUAN ---
    lines.append("2. HE SO KEM SAI SO CHUAN:")
    lines.append("")
    lines.append(f"   {'He so':<10} {'Gia tri':>22} {'Sai so chuan':>16} {'t-stat':>12}")
    lines.append(f"   {'_' * 10} {'_' * 22} {'_' * 16} {'_' * 12}")

    ten = ['a (x^2)', 'b (x)', 'c']
    he_so = [kq['a'], kq['b'], kq['c']]
    for i in range(3):
        val_str = fmt_frac(he_so[i], 15)
        lines.append(
            f"   {ten[i]:<10} {val_str:>22} "
            f"{tk['SE_he_so'][i]:>16.6e} {tk['t_stats'][i]:>12.4f}"
        )
    lines.append("")

    # --- 3. PHUONG TRINH ---
    lines.append("3. PHUONG TRINH HOI QUY:")
    lines.append(f"   {kq['phuong_trinh']}")
    lines.append("")

    # --- 4. ANOVA ---
    lines.append("4. BANG PHAN TICH PHUONG SAI (ANOVA):")
    lines.append("")
    lines.append(
        f"   {'Nguon':<14} {'df':>4} {'SS':>22} {'MS':>22} {'F':>14}"
    )
    lines.append(f"   {'_' * 14} {'_' * 4} {'_' * 22} {'_' * 22} {'_' * 14}")

    ssr_str = fmt_frac(tk['SSR'], 15)
    sse_str = fmt_frac(tk['SSE'], 15)
    sst_str = fmt_frac(tk['SST'], 15)
    msr_str = fmt_frac(tk['MSR'], 15)
    mse_str = fmt_frac(tk['MSE'], 15)
    f_str = fmt_frac(tk['F_stat'], 10) if tk['F_stat'] is not None else "N/A"

    lines.append(f"   {'Hoi quy':<14} {tk['df_reg']:>4d} {ssr_str:>22} {msr_str:>22} {f_str:>14}")
    lines.append(f"   {'Sai so':<14} {tk['df_res']:>4d} {sse_str:>22} {mse_str:>22}")
    lines.append(f"   {'Tong':<14} {tk['df_total']:>4d} {sst_str:>22}")
    lines.append("")

    # --- 5. CHI SO CHAT LUONG ---
    r2_str = fmt_frac(tk['R2'], 20)
    r2a_str = fmt_frac(tk['R2_adj'], 20)
    lines.append("5. CHI SO CHAT LUONG MO HINH:")
    lines.append(f"   R^2                     = {r2_str}")
    lines.append(f"   Adjusted R^2            = {r2a_str}")
    lines.append(f"   Standard Error (SE)     = {tk['SE_estimate']:.10e}")
    lines.append(f"   F-statistic             = {f_str}")
    lines.append(f"   So diem du lieu (n)     = {n}")
    lines.append("")

    # --- 6. PHAN TICH PHAN DU ---
    lines.append("6. PHAN TICH PHAN DU:")
    lines.append(f"   Trung binh phan du        = {fmt_frac(tk['sai_so_tb'], 15)}")
    lines.append(f"   Sai so tuyet doi TB       = {fmt_frac(tk['sai_so_abs_tb'], 15)}")
    lines.append(f"   Sai so tuyet doi MAX      = {fmt_frac(tk['sai_so_abs_max'], 15)}")
    lines.append(f"   Sai so % trung binh       = {fmt_phan_tram(tk['sai_so_pt_tb'])}%")
    lines.append(f"   Sai so % lon nhat         = {fmt_phan_tram(tk['sai_so_pt_max'])}%")
    lines.append("")

    # --- 7. BANG SO SANH ---
    lines.append("7. BANG SO SANH CHI TIET:")
    lines.append("")
    lines.append(
        f"   {'STT':>3}  {'x':>8}  {'y_thuc':>14}  "
        f"{'y_fit':>14}  {'phan_du':>16}  {'sai_so_%':>12}"
    )
    lines.append(f"   {'_' * 3}  {'_' * 8}  {'_' * 14}  {'_' * 14}  {'_' * 16}  {'_' * 12}")

    for i in range(n):
        x_str = fmt_frac(kq['x_data'][i], 6)
        y_str = fmt_frac(kq['y_data'][i], 10)
        yf_str = fmt_frac(kq['y_du_doan'][i], 10)
        e_str = fmt_frac(tk['sai_so'][i], 10)
        pct = fmt_phan_tram(tk['sai_so_phan_tram'][i], 6)
        lines.append(
            f"   {i+1:>3}  {x_str:>8}  {y_str:>14}  "
            f"{yf_str:>14}  {e_str:>16}  {pct:>11}%"
        )
    lines.append("")
    lines.append(sep)

    noi_dung = "\n".join(lines) + "\n"
    duong_dan_luu.parent.mkdir(parents=True, exist_ok=True)
    duong_dan_luu.write_text(noi_dung, encoding="utf-8")


# ============================================================
#  3. IN KET QUA RA MAN HINH (TOM TAT)
# ============================================================

def in_tom_tat(kq):
    """In tom tat ket qua ra man hinh (console)."""
    tk = kq['thong_ke']
    sep = "=" * 60

    print()
    print(sep)
    print("  KET QUA BINH PHUONG TOI THIEU (Fraction — chinh xac)")
    print(sep)
    print(f"  Phuong trinh:")
    print(f"    {kq['phuong_trinh']}")
    print("-" * 60)
    print(f"  a (x^2) = {kq['a_decimal']}")
    print(f"             +/- {tk['SE_he_so'][0]:.6e}")
    print(f"  b (x)   = {kq['b_decimal']}")
    print(f"             +/- {tk['SE_he_so'][1]:.6e}")
    print(f"  c       = {kq['c_decimal']}")
    print(f"             +/- {tk['SE_he_so'][2]:.6e}")
    print("-" * 60)
    print(f"  R^2          = {fmt_frac(tk['R2'], 20)}")
    print(f"  Adjusted R^2 = {fmt_frac(tk['R2_adj'], 20)}")
    f_str = fmt_frac(tk['F_stat'], 10) if tk['F_stat'] is not None else "N/A"
    print(f"  F-statistic  = {f_str}")
    print(f"  SE Estimate  = {tk['SE_estimate']:.10e}")
    print(f"  So diem (n)  = {kq['so_diem']}")
    print("-" * 60)
    print(f"  Sai so % TB  = {fmt_phan_tram(tk['sai_so_pt_tb'])}%")
    print(f"  Sai so % MAX = {fmt_phan_tram(tk['sai_so_pt_max'])}%")
    print(sep)
    print()


# ============================================================
#  4. PARSE COMMAND LINE ARGUMENTS
# ============================================================

def parse_args():
    """Parse tham so dong lenh."""
    parser = argparse.ArgumentParser(
        description="Binh phuong toi thieu - Fit da thuc bac 2: y = a*x^2 + b*x + c",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Vi du su dung:\n"
            "  python main.py\n"
            "  python main.py --data ../data/du_lieu.csv\n"
            "  python main.py --no-chart\n"
        ),
    )

    parser.add_argument(
        "--data", type=str, default=str(DEFAULT_DATA),
        help=f"Duong dan file CSV (mac dinh: {DEFAULT_DATA.name})",
    )
    parser.add_argument(
        "--output-dir", type=str, default=str(OUTPUT_DIR),
        help=f"Thu muc xuat ket qua (mac dinh: {OUTPUT_DIR})",
    )
    parser.add_argument(
        "--no-chart", action="store_true",
        help="Khong tao bieu do (chi xuat file TXT)",
    )

    return parser.parse_args()


# ============================================================
#  5. HAM MAIN
# ============================================================

def main():
    """Chay full pipeline."""
    args = parse_args()

    data_path = Path(args.data)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    txt_file = output_dir / "equation_result.txt"
    chart_file = output_dir / "bieu_do_fit.png"

    # Buoc 1: Chay thuat toan
    print(f"[1/3] Doc du lieu tu: {data_path.name}")
    bat_dau = time.perf_counter()

    try:
        kq = binh_phuong_toi_thieu(data_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n  LOI: {e}")
        sys.exit(1)

    thoi_gian = (time.perf_counter() - bat_dau) * 1000

    # Buoc 2: In ket qua
    in_tom_tat(kq)
    print(f"  Thoi gian tinh toan: {thoi_gian:.2f} ms")

    # Buoc 3: Luu bao cao
    print(f"\n[2/3] Luu bao cao: {txt_file}")
    tao_bao_cao(kq, txt_file)

    # Buoc 4: Tao bieu do
    if not args.no_chart:
        print(f"[3/3] Tao bieu do:  {chart_file}")
        tao_bieu_do_tong_hop(kq, chart_file)
    else:
        print("[3/3] Bo qua bieu do (--no-chart)")

    print("\n  HOAN TAT!")


if __name__ == "__main__":
    main()
