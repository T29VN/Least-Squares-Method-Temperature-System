# Branch and Error Evidence

> Nguồn sự thật: nội dung file local tại `f:\BPTT` đọc ngày 2026-07-16.

---

## Tổng quan

| Nhóm | Số nhánh |
|------|---------|
| Validation đầu vào (`doc_du_lieu_csv`) | 7 |
| Validation dữ liệu (`kiem_tra_du_lieu`) | 3 |
| Giải hệ (`giai_he_gauss`) | 1 |
| Nghịch đảo (`nghich_dao_ma_tran`) | 1 |
| Thống kê (`tinh_thong_ke`) | 6 |
| Định dạng (`dinh_dang_phuong_trinh`) | 2 (sign formatting, non-error) |
| Định dạng (`tao_bao_cao`, `in_tom_tat`) | 1 (F_stat None check) |
| CLI (`main`) | 2 |
| **Tổng** | **23** |

---

## BR-01 · FileNotFoundError

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-01 |
| **Điều kiện** | `not duong_dan.exists()` |
| **Xử lý** | `raise FileNotFoundError(f"Khong tim thay file: {duong_dan}")` |
| **Hàm** | `doc_du_lieu_csv()` |
| **File** | `src/lsm_solver.py` dòng 79–80 |
| **Loại kết thúc** | Exception propagation — bắt bởi `main()` dòng 277 |
| **Sơ đồ** | 02-main-execution-pipeline, 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-02 · CSV không có header

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-02 |
| **Điều kiện** | `reader.fieldnames is None` |
| **Xử lý** | `raise ValueError("File CSV khong co header!")` |
| **Hàm** | `doc_du_lieu_csv()` |
| **File** | `src/lsm_solver.py` dòng 88–89 |
| **Loại kết thúc** | Exception propagation — bắt bởi `main()` dòng 277 |
| **Sơ đồ** | 02-main-execution-pipeline, 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-03 · Thiếu cột x hoặc y

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-03 |
| **Điều kiện** | `"x" not in ten_cot or "y" not in ten_cot` |
| **Xử lý** | `raise ValueError(f"File CSV phai co cac cot 'x' va 'y', nhung chi co {reader.fieldnames}")` |
| **Hàm** | `doc_du_lieu_csv()` |
| **File** | `src/lsm_solver.py` dòng 92–96 |
| **Loại kết thúc** | Exception propagation |
| **Sơ đồ** | 02-main-execution-pipeline, 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-04 · Giá trị không chuyển đổi được

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-04 |
| **Điều kiện** | `float(x_str)` hoặc `float(y_str)` raise `ValueError` |
| **Xử lý** | `raise ValueError(f"Loi du lieu tai dong {so_dong}: {e}")` |
| **Hàm** | `doc_du_lieu_csv()` |
| **File** | `src/lsm_solver.py` dòng 103–107 |
| **Loại kết thúc** | Exception propagation |
| **Sơ đồ** | 02-main-execution-pipeline, 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-05 · x là NaN hoặc Inf

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-05 |
| **Điều kiện** | `math.isnan(x_float) or math.isinf(x_float)` |
| **Xử lý** | `raise ValueError(f"Gia tri x khong hop le tai dong {so_dong}: {x_str}")` |
| **Hàm** | `doc_du_lieu_csv()` |
| **File** | `src/lsm_solver.py` dòng 109–112 |
| **Loại kết thúc** | Exception propagation |
| **Sơ đồ** | 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-06 · y là NaN hoặc Inf

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-06 |
| **Điều kiện** | `math.isnan(y_float) or math.isinf(y_float)` |
| **Xử lý** | `raise ValueError(f"Gia tri y khong hop le tai dong {so_dong}: {y_str}")` |
| **Hàm** | `doc_du_lieu_csv()` |
| **File** | `src/lsm_solver.py` dòng 113–116 |
| **Loại kết thúc** | Exception propagation |
| **Sơ đồ** | 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-07 · CSV rỗng

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-07 |
| **Điều kiện** | `len(x_data) == 0` |
| **Xử lý** | `raise ValueError("File CSV khong co du lieu!")` |
| **Hàm** | `doc_du_lieu_csv()` |
| **File** | `src/lsm_solver.py` dòng 122–123 |
| **Loại kết thúc** | Exception propagation |
| **Sơ đồ** | 02-main-execution-pipeline, 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-08 · len(x) != len(y)

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-08 |
| **Điều kiện** | `len(x_data) != len(y_data)` |
| **Xử lý** | `raise ValueError(f"So luong x ({len(x_data)}) va y ({len(y_data)}) khong khop!")` |
| **Hàm** | `kiem_tra_du_lieu()` |
| **File** | `src/lsm_solver.py` dòng 140–143 |
| **Loại kết thúc** | Exception propagation |
| **Sơ đồ** | 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-09 · Số điểm < 3

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-09 |
| **Điều kiện** | `len(x_data) < so_he_so` (so_he_so = bac_da_thuc + 1 = 3) |
| **Xử lý** | `raise ValueError(f"Can it nhat {so_he_so} diem du lieu ...")` |
| **Hàm** | `kiem_tra_du_lieu()` |
| **File** | `src/lsm_solver.py` dòng 145–149 |
| **Loại kết thúc** | Exception propagation |
| **Sơ đồ** | 03-least-squares-and-statistics, 05-test-coverage |
| **Trạng thái** | **CONFIRMED** |

## BR-10 · Số giá trị x phân biệt < 3

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-10 |
| **Điều kiện** | `len(set(x_data)) < so_he_so` |
| **Xử lý** | `raise ValueError(f"Can it nhat {so_he_so} gia tri x khac nhau ...")` |
| **Hàm** | `kiem_tra_du_lieu()` |
| **File** | `src/lsm_solver.py` dòng 151–155 |
| **Loại kết thúc** | Exception propagation |
| **Sơ đồ** | 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-11 · Pivot = 0 trong giai_he_gauss()

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-11 |
| **Điều kiện** | `M[cot][cot] == 0` (sau partial pivoting) |
| **Xử lý** | `raise ValueError("Ma tran he so suy bien (det = 0), khong the giai he!")` |
| **Hàm** | `giai_he_gauss()` |
| **File** | `src/lsm_solver.py` dòng 286–289 |
| **Loại kết thúc** | Exception propagation — bắt bởi `main()` dòng 277 |
| **Sơ đồ** | 04-gaussian-elimination |
| **Trạng thái** | **CONFIRMED** |

## BR-12 · Pivot = 0 trong nghich_dao_ma_tran()

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-12 |
| **Điều kiện** | `pivot == 0` (sau partial pivoting) |
| **Xử lý** | `return None` (không raise exception) |
| **Hàm** | `nghich_dao_ma_tran()` |
| **File** | `src/lsm_solver.py` dòng 345–346 |
| **Loại kết thúc** | Trả giá trị None — xử lý bởi caller `tinh_thong_ke` tại BR-15 |
| **Sơ đồ** | 04-gaussian-elimination |
| **Trạng thái** | **CONFIRMED** |

## BR-13 · SST = 0

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-13 |
| **Điều kiện** | `SST > 0` (else branch: SST ≤ 0) |
| **Xử lý** | Nếu SST ≤ 0: `R2 = Fraction(0)` |
| **Hàm** | `tinh_thong_ke()` |
| **File** | `src/lsm_solver.py` dòng 399 |
| **Loại kết thúc** | Tiếp tục thực thi (giá trị mặc định) |
| **Sơ đồ** | 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-14 · df_res ≤ 0

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-14 |
| **Điều kiện** | `df_res > 0 and df_total > 0 and SST > 0` (else branch) |
| **Xử lý** | Nếu bất kỳ điều kiện nào false: `R2_adj = Fraction(0)`. Riêng `MSE = Fraction(0)` nếu `df_res ≤ 0` (dòng 406) |
| **Hàm** | `tinh_thong_ke()` |
| **File** | `src/lsm_solver.py` dòng 401–404, 406 |
| **Loại kết thúc** | Tiếp tục thực thi (giá trị mặc định) |
| **Sơ đồ** | 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-15 · MSE ≤ 0

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-15 |
| **Điều kiện** | `MSE > 0` (else branch) |
| **Xử lý** | `F_stat = None` |
| **Hàm** | `tinh_thong_ke()` |
| **File** | `src/lsm_solver.py` dòng 410 |
| **Loại kết thúc** | Tiếp tục thực thi (None value) |
| **Sơ đồ** | 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-16 · A_inv is None

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-16 |
| **Điều kiện** | `A_inv is not None` (else branch: A_inv is None) |
| **Xử lý** | SE_he_so giữ nguyên `[0.0] * p` (dòng 415) |
| **Hàm** | `tinh_thong_ke()` |
| **File** | `src/lsm_solver.py` dòng 417 |
| **Loại kết thúc** | Tiếp tục thực thi (giá trị mặc định) |
| **Sơ đồ** | 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-17 · SE quá nhỏ

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-17 |
| **Điều kiện** | `SE_he_so[i] > 1e-30` (else branch) |
| **Xử lý** | `t_stats.append(float('inf'))` |
| **Hàm** | `tinh_thong_ke()` |
| **File** | `src/lsm_solver.py` dòng 424–427 |
| **Loại kết thúc** | Tiếp tục thực thi (inf value) |
| **Sơ đồ** | 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-18 · y_data[i] = 0

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-18 |
| **Điều kiện** | `abs(y_data[i]) > 0` (else branch) |
| **Xử lý** | `sai_so_phan_tram.append(Fraction(0))` (tránh chia cho 0) |
| **Hàm** | `tinh_thong_ke()` |
| **File** | `src/lsm_solver.py` dòng 433–436 |
| **Loại kết thúc** | Tiếp tục thực thi (giá trị mặc định) |
| **Sơ đồ** | 03-least-squares-and-statistics |
| **Trạng thái** | **CONFIRMED** |

## BR-19 · --no-chart

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-19 |
| **Điều kiện** | `not args.no_chart` (tức `--no-chart` được set) |
| **Xử lý** | Bỏ qua `tao_bieu_do_tong_hop()`, in "Bo qua bieu do (--no-chart)" |
| **Hàm** | `main()` |
| **File** | `src/main.py` dòng 292–296 |
| **Loại kết thúc** | Tiếp tục thực thi (skip visualization) |
| **Sơ đồ** | 02-main-execution-pipeline |
| **Trạng thái** | **CONFIRMED** |

## BR-20 · Exception trong main() → sys.exit(1)

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-20 |
| **Điều kiện** | `binh_phuong_toi_thieu(data_path)` raise `FileNotFoundError` hoặc `ValueError` |
| **Xử lý** | `print(f"\n  LOI: {e}")` + `sys.exit(1)` |
| **Hàm** | `main()` |
| **File** | `src/main.py` dòng 275–279 |
| **Loại kết thúc** | Process exit code 1 |
| **Sơ đồ** | 02-main-execution-pipeline |
| **Trạng thái** | **CONFIRMED** |
| **Giải thích** | Bắt cả exceptions từ `doc_du_lieu_csv` (BR-01 đến BR-07), `kiem_tra_du_lieu` (BR-08 đến BR-10), và `giai_he_gauss` (BR-11). |

## BR-21 · F_stat is None (formatting)

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-21 |
| **Điều kiện** | `tk['F_stat'] is not None` (else branch) |
| **Xử lý** | `f_str = "N/A"` |
| **Hàm** | `tao_bao_cao()` (dòng 133), `in_tom_tat()` (dòng 212) |
| **File** | `src/main.py` dòng 133, 212 |
| **Loại kết thúc** | Tiếp tục thực thi (hiển thị "N/A") |
| **Sơ đồ** | 02-main-execution-pipeline |
| **Trạng thái** | **CONFIRMED** |

## BR-22 · Dấu b trong phương trình

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-22 |
| **Điều kiện** | `b >= 0` |
| **Xử lý** | `+ fmt(b)*x` nếu true, `- fmt(abs(b))*x` nếu false |
| **Hàm** | `dinh_dang_phuong_trinh()` |
| **File** | `src/lsm_solver.py` dòng 474–477 |
| **Loại kết thúc** | Tiếp tục thực thi (formatting) |
| **Sơ đồ** | (không cần sơ đồ riêng — formatting nhỏ) |
| **Trạng thái** | **CONFIRMED** |

## BR-23 · Dấu c trong phương trình

| Trường | Giá trị |
|--------|---------|
| **Branch ID** | BR-23 |
| **Điều kiện** | `c >= 0` |
| **Xử lý** | `+ fmt(c)` nếu true, `- fmt(abs(c))` nếu false |
| **Hàm** | `dinh_dang_phuong_trinh()` |
| **File** | `src/lsm_solver.py` dòng 479–482 |
| **Loại kết thúc** | Tiếp tục thực thi (formatting) |
| **Sơ đồ** | (không cần sơ đồ riêng — formatting nhỏ) |
| **Trạng thái** | **CONFIRMED** |
