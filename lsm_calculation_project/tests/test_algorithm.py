"""
Test: test_algorithm.py
Kiem tra tinh dung dan cua thuat toan binh phuong toi thieu.

Bao gom:
    - Test voi du lieu da biet (kiem chung ket qua)
    - Test voi du lieu thuc tu file CSV
    - Test xu ly loi (validation)
"""

import os
import sys
import math

# Them duong dan src vao sys.path de import duoc lsm_solver
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src",
    ),
)

from lsm_solver import (
    binh_phuong_toi_thieu,
    doc_du_lieu_csv,
    kiem_tra_du_lieu,
    tinh_cac_tong,
    lap_he_phuong_trinh_chuan_tac,
    giai_he_gauss,
)


# ============================================================
#  HAM HO TRO
# ============================================================

def assert_gan_bang(a, b, epsilon=1e-6, thong_bao=""):
    """Kiem tra 2 gia tri gan bang nhau."""
    if abs(a - b) > epsilon:
        raise AssertionError(
            f"THAT BAI: {a} != {b} (sai lech = {abs(a - b):.2e}) {thong_bao}"
        )


def in_ket_qua_test(ten, thanh_cong):
    """In ket qua 1 test case."""
    if thanh_cong:
        print(f"  [PASS] {ten}")
    else:
        print(f"  [FAIL] {ten}")


# ============================================================
#  TEST 1: DU LIEU DA BIET
# ============================================================

def test_du_lieu_da_biet():
    """
    Kiem tra voi du lieu don gian:  y = 2*x^2 + 3*x + 1
    Ket qua phai la a=2, b=3, c=1 (chinh xac).
    """
    ten = "Du lieu da biet: y = 2x² + 3x + 1"
    try:
        x = [0, 1, 2, 3, 4]
        y = [2 * xi * xi + 3 * xi + 1 for xi in x]

        cac_tong = tinh_cac_tong(x, y)
        A, B = lap_he_phuong_trinh_chuan_tac(cac_tong)
        nghiem = giai_he_gauss(A, B)

        assert_gan_bang(nghiem[0], 2.0, thong_bao="a != 2")
        assert_gan_bang(nghiem[1], 3.0, thong_bao="b != 3")
        assert_gan_bang(nghiem[2], 1.0, thong_bao="c != 1")

        in_ket_qua_test(ten, True)
        return True
    except Exception as e:
        in_ket_qua_test(ten, False)
        print(f"         {e}")
        return False


# ============================================================
#  TEST 2: DU LIEU TU FILE CSV
# ============================================================

def test_du_lieu_csv():
    """Chay pipeline day du voi file CSV thuc te."""
    ten = "Doc va xu ly file CSV"
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_file = os.path.join(base_dir, "data", "du_lieu_sau_xu_ly.csv")

        kq = binh_phuong_toi_thieu(data_file)

        # Kiem tra ket qua co day du cac key
        required_keys = [
            'a', 'b', 'c', 'phuong_trinh', 'x_data', 'y_data',
            'y_du_doan', 'thong_ke', 'so_diem',
        ]
        for key in required_keys:
            if key not in kq:
                raise ValueError(f"Thieu key '{key}' trong ket qua!")

        # Kiem tra R^2 > 0.99 (mo hinh tot)
        if kq['R2'] < 0.99:
            raise ValueError(f"R² = {kq['R2']:.6f} qua thap!")

        # Kiem tra thong ke co day du
        tk = kq['thong_ke']
        tk_keys = ['SSE', 'SSR', 'SST', 'R2', 'R2_adj', 'SE_he_so', 'F_stat']
        for key in tk_keys:
            if key not in tk:
                raise ValueError(f"Thieu key thong ke '{key}'!")

        in_ket_qua_test(ten, True)
        return True
    except Exception as e:
        in_ket_qua_test(ten, False)
        print(f"         {e}")
        return False


# ============================================================
#  TEST 3: KIEM TRA VALIDATION
# ============================================================

def test_validation():
    """Kiem tra xu ly loi khi du lieu khong hop le."""
    ten = "Xu ly loi (validation)"
    tat_ca_pass = True

    # Test 3a: Du lieu qua it
    try:
        kiem_tra_du_lieu([1, 2], [3, 4], bac_da_thuc=2)
        in_ket_qua_test("  3a. Phat hien du lieu qua it", False)
        tat_ca_pass = False
    except ValueError:
        in_ket_qua_test("  3a. Phat hien du lieu qua it", True)

    # Test 3b: x va y khong cung kich thuoc
    try:
        kiem_tra_du_lieu([1, 2, 3], [4, 5], bac_da_thuc=2)
        in_ket_qua_test("  3b. Phat hien x, y khong khop", False)
        tat_ca_pass = False
    except ValueError:
        in_ket_qua_test("  3b. Phat hien x, y khong khop", True)

    # Test 3c: File khong ton tai
    try:
        doc_du_lieu_csv("khong_ton_tai.csv")
        in_ket_qua_test("  3c. Phat hien file khong ton tai", False)
        tat_ca_pass = False
    except FileNotFoundError:
        in_ket_qua_test("  3c. Phat hien file khong ton tai", True)

    in_ket_qua_test(ten, tat_ca_pass)
    return tat_ca_pass


# ============================================================
#  TEST 4: KIEM TRA THONG KE
# ============================================================

def test_thong_ke():
    """Kiem tra cac chi so thong ke co nhat quan."""
    ten = "Tinh nhat quan thong ke"
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_file = os.path.join(base_dir, "data", "du_lieu_sau_xu_ly.csv")
        kq = binh_phuong_toi_thieu(data_file)
        tk = kq['thong_ke']

        # SST = SSR + SSE (phai bang nhau)
        sst_check = tk['SSR'] + tk['SSE']
        assert_gan_bang(
            sst_check, tk['SST'], epsilon=1e-10,
            thong_bao="SSR + SSE != SST"
        )

        # R² = SSR / SST
        r2_check = tk['SSR'] / tk['SST']
        assert_gan_bang(
            r2_check, tk['R2'], epsilon=1e-10,
            thong_bao="R² != SSR/SST"
        )

        # Trung binh phan du gan 0
        assert_gan_bang(
            tk['sai_so_tb'], 0.0, epsilon=1e-10,
            thong_bao="Trung binh phan du != 0"
        )

        # 0 <= R² <= 1
        if not (0 <= tk['R2'] <= 1):
            raise ValueError(f"R² = {tk['R2']} nam ngoai [0, 1]!")

        in_ket_qua_test(ten, True)
        return True
    except Exception as e:
        in_ket_qua_test(ten, False)
        print(f"         {e}")
        return False


# ============================================================
#  CHAY TAT CA TEST
# ============================================================

def main():
    """Chay toan bo test suite."""
    print()
    print("=" * 50)
    print("  TEST SUITE — Binh phuong toi thieu")
    print("=" * 50)
    print()

    ket_qua = []
    ket_qua.append(test_du_lieu_da_biet())
    ket_qua.append(test_du_lieu_csv())
    ket_qua.append(test_validation())
    ket_qua.append(test_thong_ke())

    so_pass = sum(ket_qua)
    tong = len(ket_qua)

    print()
    print("-" * 50)
    print(f"  Ket qua: {so_pass}/{tong} tests PASSED")

    if so_pass == tong:
        print("  TRANG THAI: TAT CA THANH CONG!")
    else:
        print("  TRANG THAI: CO LOI — Xem chi tiet o tren.")

    print("-" * 50)
    print()

    return 0 if so_pass == tong else 1


if __name__ == "__main__":
    sys.exit(main())
