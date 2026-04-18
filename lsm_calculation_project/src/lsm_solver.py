"""
Module: lsm_solver.py
Phuong phap Binh phuong toi thieu (Least Squares Method)

Tim cac he so a, b, c trong phuong trinh:
    y = a*x^2 + b*x + c

Huong tiep can: Tim cuc tri ham nhieu bien
    - Xay dung ham sai so: S(a,b,c) = Sum[ (yi - a*xi^2 - b*xi - c)^2 ]
    - Lay dao ham rieng theo a, b, c va cho bang 0:
        dS/da = 0  =>  a*Sum(x^4) + b*Sum(x^3) + c*Sum(x^2) = Sum(x^2 * y)
        dS/db = 0  =>  a*Sum(x^3) + b*Sum(x^2) + c*Sum(x)   = Sum(x * y)
        dS/dc = 0  =>  a*Sum(x^2) + b*Sum(x)   + c*n        = Sum(y)
    - Giai he 3 phuong trinh 3 an bang phuong phap khu Gauss
"""

import csv


def doc_du_lieu_csv(duong_dan_file):
    """
    Doc du lieu (x, y) tu file CSV.

    File CSV can co header voi 2 cot: x, y
    Cac dong du lieu la cac gia tri so thuc phan tach boi dau phay.

    Parameters:
        duong_dan_file : str - duong dan tuyet doi den file CSV

    Returns:
        x_data : list[float] - danh sach gia tri x
        y_data : list[float] - danh sach gia tri y
    """
    x_data = []
    y_data = []

    with open(duong_dan_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x_data.append(float(row["x"]))
            y_data.append(float(row["y"]))

    return x_data, y_data


def tinh_cac_tong(x_data, y_data):
    """
    Tinh tat ca cac tong can thiet de xay dung he phuong trinh chuan tac.

    Tu dieu kien cuc tri (dao ham rieng = 0), ta can cac tong:
        Sum(x^k) voi k = 1..4  va  Sum(x^k * y) voi k = 0..2

    Parameters:
        x_data : list[float]
        y_data : list[float]

    Returns:
        dict chua cac gia tri tong:
            'n', 'Sx', 'Sx2', 'Sx3', 'Sx4', 'Sy', 'Sxy', 'Sx2y'
    """
    n = len(x_data)

    Sx   = 0.0   # Sum(x)
    Sx2  = 0.0   # Sum(x^2)
    Sx3  = 0.0   # Sum(x^3)
    Sx4  = 0.0   # Sum(x^4)
    Sy   = 0.0   # Sum(y)
    Sxy  = 0.0   # Sum(x * y)
    Sx2y = 0.0   # Sum(x^2 * y)

    for i in range(n):
        xi = x_data[i]
        yi = y_data[i]

        xi2 = xi * xi       # x^2
        xi3 = xi2 * xi      # x^3
        xi4 = xi3 * xi      # x^4

        Sx   += xi
        Sx2  += xi2
        Sx3  += xi3
        Sx4  += xi4
        Sy   += yi
        Sxy  += xi * yi
        Sx2y += xi2 * yi

    return {
        'n': n,
        'Sx': Sx, 'Sx2': Sx2, 'Sx3': Sx3, 'Sx4': Sx4,
        'Sy': Sy, 'Sxy': Sxy, 'Sx2y': Sx2y
    }


def lap_he_phuong_trinh_chuan_tac(cac_tong):
    """
    Lap he phuong trinh chuan tac tu dieu kien cuc tri.

    Dat S(a,b,c) = Sum[ (yi - a*xi^2 - b*xi - c)^2 ]
    Dieu kien cuc tri (cuc tieu):
        dS/da = -2 * Sum[ (yi - a*xi^2 - b*xi - c) * xi^2 ] = 0
        dS/db = -2 * Sum[ (yi - a*xi^2 - b*xi - c) * xi   ] = 0
        dS/dc = -2 * Sum[ (yi - a*xi^2 - b*xi - c)         ] = 0

    Khai trien va sap xep lai, ta duoc he:
        | Sx4   Sx3   Sx2 | |a|   | Sx2y |
        | Sx3   Sx2   Sx  | |b| = | Sxy  |
        | Sx2   Sx    n   | |c|   | Sy   |

    Parameters:
        cac_tong : dict - ket qua tu ham tinh_cac_tong()

    Returns:
        A : list[list[float]] - ma tran he so 3x3
        B : list[float]       - vecto ve phai 3x1
    """
    n    = cac_tong['n']
    Sx   = cac_tong['Sx']
    Sx2  = cac_tong['Sx2']
    Sx3  = cac_tong['Sx3']
    Sx4  = cac_tong['Sx4']
    Sy   = cac_tong['Sy']
    Sxy  = cac_tong['Sxy']
    Sx2y = cac_tong['Sx2y']

    # Ma tran he so (tu dao ham rieng = 0)
    A = [
        [Sx4, Sx3, Sx2],   # tu dS/da = 0
        [Sx3, Sx2, Sx ],   # tu dS/db = 0
        [Sx2, Sx,  n  ],   # tu dS/dc = 0
    ]

    # Vecto ve phai
    B = [Sx2y, Sxy, Sy]

    return A, B


def giai_he_gauss(A, B):
    """
    Giai he phuong trinh tuyen tinh A * x = B
    bang phuong phap khu Gauss voi chon phan tu chinh (partial pivoting).

    Parameters:
        A : list[list[float]] - ma tran he so NxN
        B : list[float]       - vecto ve phai Nx1

    Returns:
        x : list[float] - nghiem [a, b, c]

    Raises:
        ValueError: khi ma tran suy bien
    """
    n = len(B)

    # Tao ban sao ma tran mo rong [A|B] de khong lam thay doi du lieu goc
    M = []
    for i in range(n):
        hang = []
        for j in range(n):
            hang.append(A[i][j])
        hang.append(B[i])
        M.append(hang)

    # ===== BUOC 1: Khu xuoi (Forward Elimination) =====
    for cot in range(n):
        # Chon phan tu chinh (pivot): tim hang co |M[hang][cot]| lon nhat
        gia_tri_max = abs(M[cot][cot])
        hang_max = cot

        for hang in range(cot + 1, n):
            if abs(M[hang][cot]) > gia_tri_max:
                gia_tri_max = abs(M[hang][cot])
                hang_max = hang

        # Doi cho 2 hang neu can thiet
        if hang_max != cot:
            M[cot], M[hang_max] = M[hang_max], M[cot]

        # Kiem tra ma tran suy bien
        if abs(M[cot][cot]) < 1e-12:
            raise ValueError(
                "Ma tran he so suy bien (det ~ 0), khong the giai he!"
            )

        # Khu cac phan tu phia duoi phan tu chinh
        for hang in range(cot + 1, n):
            he_so = M[hang][cot] / M[cot][cot]
            for j in range(cot, n + 1):
                M[hang][j] = M[hang][j] - he_so * M[cot][j]

    # ===== BUOC 2: Thay nguoc (Back Substitution) =====
    nghiem = [0.0] * n

    for i in range(n - 1, -1, -1):
        nghiem[i] = M[i][n]  # bat dau tu ve phai
        for j in range(i + 1, n):
            nghiem[i] = nghiem[i] - M[i][j] * nghiem[j]
        nghiem[i] = nghiem[i] / M[i][i]

    return nghiem


def binh_phuong_toi_thieu(duong_dan_csv):
    """
    Ham chinh: Doc du lieu tu file CSV va tim cac he so a, b, c
    cua phuong trinh  y = a*x^2 + b*x + c
    bang phuong phap binh phuong toi thieu (cuc tri ham nhieu bien).

    Cac buoc thuc hien:
        1. Doc du lieu (x, y) tu file CSV
        2. Tinh cac tong Sx, Sx2, ..., Sx2y
        3. Lap he phuong trinh chuan tac tu dieu kien dao ham rieng = 0
        4. Giai he bang phuong phap khu Gauss
        5. Tra ve ket qua

    Parameters:
        duong_dan_csv : str - duong dan den file CSV chua du lieu (x, y)

    Returns:
        dict voi cac khoa:
            'a'          : float - he so cua x^2
            'b'          : float - he so cua x
            'c'          : float - he so tu do
            'phuong_trinh' : str - chuoi bieu dien phuong trinh
            'y_du_doan'  : list  - gia tri y tinh tu phuong trinh tim duoc
            'sai_so'     : list  - hieu giua y thuc te va y du doan
            'SSE'        : float - tong binh phuong sai so
            'R2'         : float - he so xac dinh R^2
    """
    # Buoc 1: Doc du lieu
    x_data, y_data = doc_du_lieu_csv(duong_dan_csv)

    if len(x_data) < 3:
        raise ValueError("Can it nhat 3 diem du lieu de fit da thuc bac 2!")

    # Buoc 2: Tinh cac tong
    cac_tong = tinh_cac_tong(x_data, y_data)

    # Buoc 3: Lap he phuong trinh chuan tac (tu dieu kien cuc tri)
    A, B = lap_he_phuong_trinh_chuan_tac(cac_tong)

    # Buoc 4: Giai he phuong trinh
    nghiem = giai_he_gauss(A, B)
    a = nghiem[0]   # he so cua x^2
    b = nghiem[1]   # he so cua x
    c = nghiem[2]   # he so tu do

    # Buoc 5: Tinh gia tri du doan va cac chi so danh gia
    y_du_doan = []
    for xi in x_data:
        yi_pred = a * xi * xi + b * xi + c
        y_du_doan.append(yi_pred)

    sai_so = []
    for i in range(len(y_data)):
        sai_so.append(y_data[i] - y_du_doan[i])

    # SSE: Sum of Squared Errors
    SSE = 0.0
    for e in sai_so:
        SSE += e * e

    # R^2: He so xac dinh
    y_trung_binh = sum(y_data) / len(y_data)
    SST = 0.0
    for yi in y_data:
        SST += (yi - y_trung_binh) ** 2

    R2 = 1.0 - (SSE / SST) if SST != 0 else 0.0

    # Tao chuoi phuong trinh
    phuong_trinh = f"y = ({a})*x^2 + ({b})*x + ({c})"

    return {
        'a': a,
        'b': b,
        'c': c,
        'phuong_trinh': phuong_trinh,
        'x_data': x_data,
        'y_data': y_data,
        'y_du_doan': y_du_doan,
        'sai_so': sai_so,
        'SSE': SSE,
        'R2': R2,
    }
