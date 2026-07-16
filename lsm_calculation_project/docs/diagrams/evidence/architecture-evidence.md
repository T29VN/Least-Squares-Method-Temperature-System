# Architecture Evidence

> Nguồn sự thật: nội dung file local tại `f:\BPTT` đọc ngày 2026-07-16.
> Đếm hàm trực tiếp từ mã nguồn, không sử dụng số liệu tổng hợp từ báo cáo trước.

---

## Tổng quan số hàm (đếm trực tiếp)

| Module | File | Số hàm top-level | Hàm lồng (nested) |
|--------|------|------------------:|--------------------|
| lsm_solver | `src/lsm_solver.py` (550 dòng) | 10 | 1 (`fmt` bên trong `dinh_dang_phuong_trinh`) |
| main | `src/main.py` (303 dòng) | 6 | 0 |
| visualizer | `src/visualizer.py` (221 dòng) | 4 | 0 |
| test_algorithm | `tests/test_algorithm.py` (245 dòng) | 7 | 0 |
| tinh_phuong_trinh_bac_2 | `tests/tinh_phuong_trinh_bac_2.py` (11 dòng) | 0 (script thuần) | 0 |
| **Tổng** | | **27 top-level** | **1 nested** |

---

## Nhóm 1: Entry Point CLI

### ARCH-01 · `main.py` (module)

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-01 |
| **File** | `src/main.py` |
| **Phạm vi** | Toàn bộ file, 303 dòng |
| **Vai trò** | Entry point CLI — orchestrator chạy pipeline đầy đủ |
| **Đầu vào** | CLI arguments (`--data`, `--output-dir`, `--no-chart`) |
| **Đầu ra** | Console stdout, `equation_result.txt`, `bieu_do_fit.png` |
| **Thành phần gọi** | Không — được gọi bởi `python main.py` |
| **Thành phần được gọi** | `parse_args`, `binh_phuong_toi_thieu`, `in_tom_tat`, `tao_bao_cao`, `tao_bieu_do_tong_hop` |
| **Kiểu dữ liệu chính** | `argparse.Namespace`, `dict` (kq), `Path` |
| **Import từ module khác** | `binh_phuong_toi_thieu`, `fraction_sang_decimal` (từ lsm_solver); `tao_bieu_do_tong_hop` (từ visualizer) |
| **Trạng thái** | **CONFIRMED** — dòng 27–28 import, dòng 301–302 `if __name__` guard |
| **Giải thích** | Module-level code thiết lập `BASE_DIR`, `DEFAULT_DATA`, `OUTPUT_DIR` tại dòng 38–40. `sys.path.insert` tại dòng 25 thêm thư mục `src`. |

### ARCH-02 · `parse_args()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-02 |
| **File** | `src/main.py` |
| **Phạm vi** | Dòng 227–253 |
| **Vai trò** | Phân tích tham số dòng lệnh |
| **Đầu vào** | `sys.argv` (implicit) |
| **Đầu ra** | `argparse.Namespace` với attributes `data`, `output_dir`, `no_chart` |
| **Thành phần gọi** | `main()` tại dòng 262 |
| **Thành phần được gọi** | `argparse.ArgumentParser` (stdlib) |
| **Kiểu dữ liệu chính** | `str` (data, output_dir), `bool` (no_chart) |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 227–253 |
| **Giải thích** | 3 arguments: `--data` (default `du_lieu_sau_xu_ly.csv`), `--output-dir` (default `output/`), `--no-chart` (store_true). |

### ARCH-03 · `main()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-03 |
| **File** | `src/main.py` |
| **Phạm vi** | Dòng 260–298 |
| **Vai trò** | Hàm chính — chạy pipeline 5 bước |
| **Đầu vào** | `args` từ `parse_args()` |
| **Đầu ra** | Side effects: console, file TXT, file PNG |
| **Thành phần gọi** | `__main__` guard dòng 301–302 |
| **Thành phần được gọi** | `parse_args` (dòng 262), `binh_phuong_toi_thieu` (dòng 276), `in_tom_tat` (dòng 284), `tao_bao_cao` (dòng 289), `tao_bieu_do_tong_hop` (dòng 294) |
| **Kiểu dữ liệu chính** | `dict` (kq), `Path` (data_path, output_dir, txt_file, chart_file) |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 260–298 |
| **Giải thích** | Try/except bắt `FileNotFoundError`, `ValueError` từ `binh_phuong_toi_thieu` → `sys.exit(1)` tại dòng 275–279. `time.perf_counter` đo thời gian tính toán. Nhánh `--no-chart` tại dòng 292–296. |

---

## Nhóm 2: Core Solver

### ARCH-04 · `doc_du_lieu_csv()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-04 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 60–125 |
| **Vai trò** | Đọc dữ liệu (x, y) từ file CSV, chuyển string → Fraction |
| **Đầu vào** | `duong_dan_file: str | Path` |
| **Đầu ra** | `(x_data: list[Fraction], y_data: list[Fraction])` |
| **Thành phần gọi** | `binh_phuong_toi_thieu` (dòng 505), `test_validation` (dòng 152) |
| **Thành phần được gọi** | `csv.DictReader`, `Path.exists`, `Fraction` (stdlib) |
| **Kiểu dữ liệu chính** | `Path`, `csv.DictReader`, `Fraction`, `str`, `float` (validation only) |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 60–125 |
| **Giải thích** | Chuyển string → Fraction (dòng 119–120) không qua float để giữ precision. Validate: file tồn tại (79), header (88), cột x/y (92), parse float (103–107), NaN/Inf (109–116), dữ liệu rỗng (122). |

### ARCH-05 · `kiem_tra_du_lieu()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-05 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 128–155 |
| **Vai trò** | Validate dữ liệu trước khi fit |
| **Đầu vào** | `x_data: list[Fraction]`, `y_data: list[Fraction]`, `bac_da_thuc: int` |
| **Đầu ra** | Không (raise ValueError nếu không hợp lệ) |
| **Thành phần gọi** | `binh_phuong_toi_thieu` (dòng 508), `test_validation` (dòng 136, 144) |
| **Thành phần được gọi** | Không |
| **Kiểu dữ liệu chính** | `list`, `int`, `set` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 128–155 |
| **Giải thích** | 3 validation: len(x)≠len(y) (140), n < bậc+1 (145), giá trị x phân biệt < bậc+1 (151). |

### ARCH-06 · `tinh_cac_tong()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-06 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 162–201 |
| **Vai trò** | Tính 7 tổng thống kê (Σx, Σx², Σx³, Σx⁴, Σy, Σxy, Σx²y) |
| **Đầu vào** | `x_data: list[Fraction]`, `y_data: list[Fraction]` |
| **Đầu ra** | `dict` với keys: `n`, `Sx`, `Sx2`, `Sx3`, `Sx4`, `Sy`, `Sxy`, `Sx2y` (tất cả Fraction) |
| **Thành phần gọi** | `binh_phuong_toi_thieu` (dòng 511), `test_du_lieu_da_biet` (dòng 68) |
| **Thành phần được gọi** | Không |
| **Kiểu dữ liệu chính** | `Fraction` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 162–201 |
| **Giải thích** | Vòng lặp đơn qua n điểm dữ liệu, tích luỹ 7 tổng bằng Fraction. |

### ARCH-07 · `lap_he_phuong_trinh_chuan_tac()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-07 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 208–243 |
| **Vai trò** | Lập ma trận 3×3 và vector vế phải từ các tổng |
| **Đầu vào** | `cac_tong: dict` (Fraction values) |
| **Đầu ra** | `(A: list[list[Fraction]], B: list[Fraction])` — hệ phương trình chuẩn tắc |
| **Thành phần gọi** | `binh_phuong_toi_thieu` (dòng 514), `test_du_lieu_da_biet` (dòng 69) |
| **Thành phần được gọi** | Không |
| **Kiểu dữ liệu chính** | `Fraction`, `list[list[Fraction]]` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 208–243 |
| **Giải thích** | Ma trận đối xứng: [[Sx4,Sx3,Sx2],[Sx3,Sx2,Sx],[Sx2,Sx,n]]. Vector: [Sx2y,Sxy,Sy]. |

### ARCH-08 · `giai_he_gauss()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-08 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 250–305 |
| **Vai trò** | Giải hệ phương trình tuyến tính bằng khử Gauss với partial pivoting |
| **Đầu vào** | `A: list[list[Fraction]]`, `B: list[Fraction]` |
| **Đầu ra** | `list[Fraction]` — nghiệm chính xác [a, b, c] |
| **Thành phần gọi** | `binh_phuong_toi_thieu` (dòng 517), `test_du_lieu_da_biet` (dòng 70) |
| **Thành phần được gọi** | Không |
| **Kiểu dữ liệu chính** | `Fraction`, `list[list[Fraction]]` (augmented matrix M) |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 250–305 |
| **Giải thích** | Tạo augmented matrix (266–270), forward elimination với partial pivoting (273–294), back substitution (297–305). Pivot = 0 → ValueError (286–289). |

### ARCH-09 · `nghich_dao_ma_tran()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-09 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 312–362 |
| **Vai trò** | Nghịch đảo ma trận NxN bằng Gauss-Jordan |
| **Đầu vào** | `A: list[list[Fraction]]` |
| **Đầu ra** | `list[list[Fraction]]` hoặc `None` (nếu singular) |
| **Thành phần gọi** | `tinh_thong_ke` (dòng 416) |
| **Thành phần được gọi** | Không |
| **Kiểu dữ liệu chính** | `Fraction`, `list[list[Fraction]]` (augmented [A|I]) |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 312–362 |
| **Giải thích** | Gauss-Jordan với partial pivoting. Pivot = 0 → return None (345–346). Không raise, khác với `giai_he_gauss`. |

### ARCH-10 · `tinh_thong_ke()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-10 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 369–454 |
| **Vai trò** | Tính đầy đủ các chỉ số thống kê hồi quy |
| **Đầu vào** | `x_data`, `y_data`, `y_du_doan: list[Fraction]`, `he_so: list[Fraction]`, `A_matrix: list[list[Fraction]]` |
| **Đầu ra** | `dict` (19 keys: SSE, SSR, SST, R2, R2_adj, MSE, MSR, F_stat, SE_estimate, SE_he_so, t_stats, sai_so, sai_so_phan_tram, df_*, sai_so_tb, sai_so_abs_max, sai_so_abs_tb, sai_so_pt_max, sai_so_pt_tb) |
| **Thành phần gọi** | `binh_phuong_toi_thieu` (dòng 524) |
| **Thành phần được gọi** | `nghich_dao_ma_tran` (dòng 416) |
| **Kiểu dữ liệu chính** | `Fraction` (SSE, SSR, SST, R2, …), `float` (SE_estimate, SE_he_so, t_stats) |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 369–454 |
| **Giải thích** | Fraction cho hầu hết phép tính. Chuyển sang float tại `math.sqrt` (413, 420) và `float(he_so[i])` (425). Nhiều nhánh edge case (SST=0, df_res≤0, MSE≤0, A_inv=None, SE nhỏ, y=0). |

### ARCH-11 · `dinh_dang_phuong_trinh()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-11 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 461–484 |
| **Vai trò** | Tạo chuỗi phương trình dạng `y = ...` với precision cao |
| **Đầu vào** | `a, b, c: Fraction`, `so_chu_so: int` |
| **Đầu ra** | `str` — chuỗi phương trình |
| **Thành phần gọi** | `binh_phuong_toi_thieu` (dòng 531) |
| **Thành phần được gọi** | `fraction_sang_decimal` (qua hàm lồng `fmt` tại dòng 467) |
| **Kiểu dữ liệu chính** | `Fraction`, `Decimal`, `str` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 461–484 |
| **Giải thích** | Chứa hàm lồng `def fmt(val)` tại dòng 466–470. Nhánh b≥0/b<0 (474–477) và c≥0/c<0 (479–482) quyết định dấu `+` hay `-`. |

### ARCH-12 · `binh_phuong_toi_thieu()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-12 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 491–549 |
| **Vai trò** | Orchestrator — chạy toàn bộ pipeline tính bình phương tối thiểu |
| **Đầu vào** | `duong_dan_csv: str | Path` |
| **Đầu ra** | `dict` — kết quả tổng hợp (17 keys: a, b, c, a_decimal, b_decimal, c_decimal, a_fraction, b_fraction, c_fraction, phuong_trinh, x_data, y_data, y_du_doan, thong_ke, so_diem, sai_so, SSE, R2) |
| **Thành phần gọi** | `main.main()` (dòng 276), `test_du_lieu_csv` (dòng 95), `test_thong_ke` (dòng 172) |
| **Thành phần được gọi** | `doc_du_lieu_csv` (505), `kiem_tra_du_lieu` (508), `tinh_cac_tong` (511), `lap_he_phuong_trinh_chuan_tac` (514), `giai_he_gauss` (517), `tinh_thong_ke` (524), `fraction_sang_decimal` (527–529), `dinh_dang_phuong_trinh` (531) |
| **Kiểu dữ liệu chính** | `Fraction`, `Decimal`, `list`, `dict`, `str` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 491–549 |
| **Giải thích** | 8 bước tuần tự. Backward compatibility keys `sai_so`, `SSE`, `R2` tại dòng 546–548 tham chiếu tới `thong_ke` dict. List comprehension `y_du_doan` tại dòng 521. |

### ARCH-13 · `fraction_sang_decimal()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-13 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 33–53 |
| **Vai trò** | Chuyển đổi Fraction → Decimal với precision tuỳ chọn |
| **Đầu vào** | `phan_so: Fraction`, `so_chu_so: int | None` |
| **Đầu ra** | `Decimal` |
| **Thành phần gọi** | `binh_phuong_toi_thieu` (527–529), `dinh_dang_phuong_trinh.fmt` (467), `main.fmt_frac` (50) |
| **Thành phần được gọi** | `Decimal`, `getcontext` (stdlib) |
| **Kiểu dữ liệu chính** | `Fraction`, `Decimal`, `int` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 33–53 |
| **Giải thích** | Tạm tăng `getcontext().prec` thêm 10 (dòng 50), tính `Decimal(num)/Decimal(den)`, rồi restore precision (52). |

---

## Nhóm 3: Output Formatting

### ARCH-14 · `fmt_frac()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-14 |
| **File** | `src/main.py` |
| **Phạm vi** | Dòng 47–55 |
| **Vai trò** | Định dạng Fraction/Decimal/số thành chuỗi Decimal |
| **Đầu vào** | `val: Fraction | Decimal | any`, `chu_so: int = 30` |
| **Đầu ra** | `str` |
| **Thành phần gọi** | `tao_bao_cao` (nhiều lần: 108, 128–133, 141–142, 153–155, 170–173), `in_tom_tat` (210–212) |
| **Thành phần được gọi** | `fraction_sang_decimal` (từ lsm_solver, dòng 50) |
| **Kiểu dữ liệu chính** | `Fraction`, `Decimal`, `str` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 47–55 |
| **Giải thích** | 3 nhánh isinstance: Fraction → gọi `fraction_sang_decimal`, Decimal → giữ nguyên, other → `Decimal(str(val))`. |

### ARCH-15 · `fmt_phan_tram()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-15 |
| **File** | `src/main.py` |
| **Phạm vi** | Dòng 58–62 |
| **Vai trò** | Định dạng giá trị phần trăm |
| **Đầu vào** | `val: Fraction | float`, `chu_so: int = 6` |
| **Đầu ra** | `str` |
| **Thành phần gọi** | `tao_bao_cao` (156–157, 174), `in_tom_tat` (217–218) |
| **Thành phần được gọi** | Không |
| **Kiểu dữ liệu chính** | `Fraction`, `float`, `str` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 58–62 |
| **Giải thích** | Nhánh isinstance: Fraction → `float(val)` trước format. |

### ARCH-16 · `tao_bao_cao()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-16 |
| **File** | `src/main.py` |
| **Phạm vi** | Dòng 69–184 |
| **Vai trò** | Tạo báo cáo văn bản chi tiết, ghi ra file TXT |
| **Đầu vào** | `kq: dict`, `duong_dan_luu: Path` |
| **Đầu ra** | Side effect: ghi file `equation_result.txt` (UTF-8) |
| **Thành phần gọi** | `main()` (dòng 289) |
| **Thành phần được gọi** | `fmt_frac` (nhiều lần), `fmt_phan_tram` (156–157, 174) |
| **Kiểu dữ liệu chính** | `dict`, `Path`, `list[str]`, `str` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 69–184 |
| **Giải thích** | 7 sections: hệ số, hệ số kèm SE, phương trình, ANOVA, chỉ số chất lượng, phân dư, bảng so sánh. Ghi file tại dòng 183–184. F_stat=None → "N/A" (133). |

### ARCH-17 · `in_tom_tat()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-17 |
| **File** | `src/main.py` |
| **Phạm vi** | Dòng 191–220 |
| **Vai trò** | In tóm tắt kết quả ra console (stdout) |
| **Đầu vào** | `kq: dict` |
| **Đầu ra** | Side effect: `print()` ra console |
| **Thành phần gọi** | `main()` (dòng 284) |
| **Thành phần được gọi** | `fmt_frac` (210–212), `fmt_phan_tram` (217–218) |
| **Kiểu dữ liệu chính** | `dict` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 191–220 |
| **Giải thích** | Hiển thị: phương trình, a/b/c ± SE, R², R²_adj, F, SE estimate, n, sai số % TB/MAX. F_stat=None → "N/A" (212). |

---

## Nhóm 4: Visualization

### ARCH-18 · `tao_bieu_do_tong_hop()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-18 |
| **File** | `src/visualizer.py` |
| **Phạm vi** | Dòng 159–219 |
| **Vai trò** | Tạo biểu đồ tổng hợp 2-panel (fit + residual) và lưu PNG |
| **Đầu vào** | `kq: dict`, `duong_dan_luu: str | Path` |
| **Đầu ra** | `Path` — đường dẫn file ảnh đã lưu. Side effect: ghi file PNG |
| **Thành phần gọi** | `main.main()` (dòng 294) |
| **Thành phần được gọi** | `_cau_hinh_style` (177), `ve_bieu_do_fit` (200), `ve_bieu_do_phan_du` (211) |
| **Kiểu dữ liệu chính** | `dict`, `list[float]`, `Path`, `matplotlib.Figure`, `matplotlib.Axes` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 159–219 |
| **Giải thích** | Convert Fraction→float (192–197). 2 panels: height ratio 3:2 (182). Lấy `sai_so` từ `kq['thong_ke']['sai_so']` với fallback `kq['sai_so']` (209). Lưu dpi=150, bbox_inches='tight' (216). |

### ARCH-19 · `_cau_hinh_style()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-19 |
| **File** | `src/visualizer.py` |
| **Phạm vi** | Dòng 43–48 |
| **Vai trò** | Áp dụng cấu hình style chung cho matplotlib |
| **Đầu vào** | Không |
| **Đầu ra** | Side effect: cập nhật `plt.rcParams` |
| **Thành phần gọi** | `tao_bieu_do_tong_hop` (dòng 177) |
| **Thành phần được gọi** | `plt.rcParams.update` |
| **Kiểu dữ liệu chính** | `dict` (FONT_CONFIG) |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 43–48 |
| **Giải thích** | Thiết lập grid (alpha=0.3, linestyle='--'), font sizes (11 default, 13 title). |

### ARCH-20 · `ve_bieu_do_fit()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-20 |
| **File** | `src/visualizer.py` |
| **Phạm vi** | Dòng 55–102 |
| **Vai trò** | Vẽ scatter dữ liệu thực + đường cong hồi quy |
| **Đầu vào** | `ax: Axes`, `x_data, y_data: list[float]`, `a, b, c: float`, `phuong_trinh: str`, `R2: float` |
| **Đầu ra** | Side effect: vẽ lên `ax` |
| **Thành phần gọi** | `tao_bieu_do_tong_hop` (dòng 200) |
| **Thành phần được gọi** | `ax.plot`, `ax.scatter`, `ax.set_xlabel`, `ax.set_ylabel`, `ax.set_title`, `ax.legend` |
| **Kiểu dữ liệu chính** | `list[float]`, `matplotlib.Axes` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 55–102 |
| **Giải thích** | Tạo 201 điểm mịn (so_diem_muot=200, range 0..200 inclusive, dòng 71–77). Margin 5% mỗi bên (70). Đường fit zorder=2, scatter zorder=3. |

### ARCH-21 · `ve_bieu_do_phan_du()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-21 |
| **File** | `src/visualizer.py` |
| **Phạm vi** | Dòng 109–152 |
| **Vai trò** | Vẽ biểu đồ phân dư (residual stem plot) |
| **Đầu vào** | `ax: Axes`, `x_data: list[float]`, `sai_so: list[float]` |
| **Đầu ra** | Side effect: vẽ lên `ax` |
| **Thành phần gọi** | `tao_bieu_do_tong_hop` (dòng 211) |
| **Thành phần được gọi** | `ax.axhline`, `ax.plot`, `ax.scatter`, `ax.ticklabel_format` |
| **Kiểu dữ liệu chính** | `list[float]`, `matplotlib.Axes` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 109–152 |
| **Giải thích** | Đường zero (120–126). Stem bằng tay: từng cặp [x,x],[0,e] (129–135). Scientific notation y-axis (152). |

---

## Nhóm 5: Tests

### ARCH-22 · `test_algorithm.py` (module)

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-22 |
| **File** | `tests/test_algorithm.py` |
| **Phạm vi** | Toàn bộ file, 245 dòng |
| **Vai trò** | Bộ kiểm thử tự viết (custom test runner), 4 test cases |
| **Đầu vào** | Không (chạy trực tiếp) |
| **Đầu ra** | Console stdout, exit code 0 (pass) hoặc 1 (fail) |
| **Thành phần gọi** | `python test_algorithm.py` |
| **Thành phần được gọi** | `tinh_cac_tong`, `lap_he_phuong_trinh_chuan_tac`, `giai_he_gauss`, `binh_phuong_toi_thieu`, `kiem_tra_du_lieu`, `doc_du_lieu_csv` (import dòng 24–31) |
| **Kiểu dữ liệu chính** | `list[bool]` (ket_qua), `int` (exit code) |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 1–245 |
| **Giải thích** | Không dùng unittest/pytest. `sys.path.insert` tại 16–22. Custom runner `main()` tại 211–240 với `sys.exit(main())` tại 244. |

### ARCH-23 · `assert_gan_bang()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-23 |
| **File** | `tests/test_algorithm.py` |
| **Phạm vi** | Dòng 38–43 |
| **Vai trò** | Helper — kiểm tra 2 giá trị gần bằng nhau |
| **Đầu vào** | `a, b: number`, `epsilon: float = 1e-6`, `thong_bao: str = ""` |
| **Đầu ra** | Không (raise `AssertionError` nếu sai lệch > epsilon) |
| **Thành phần gọi** | `test_du_lieu_da_biet` (72–74), `test_thong_ke` (177–178, 184–185, 190–191) |
| **Thành phần được gọi** | Không |
| **Kiểu dữ liệu chính** | `float`, `Fraction` (qua operator overload) |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 38–43 |
| **Giải thích** | Raise `AssertionError` (tên class Python chuẩn). |

### ARCH-24 · `in_ket_qua_test()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-24 |
| **File** | `tests/test_algorithm.py` |
| **Phạm vi** | Dòng 46–51 |
| **Vai trò** | Helper — in [PASS] hoặc [FAIL] cho test case |
| **Đầu vào** | `ten: str`, `thanh_cong: bool` |
| **Đầu ra** | Side effect: `print()` |
| **Thành phần gọi** | Tất cả 4 test functions và sub-tests |
| **Thành phần được gọi** | Không |
| **Kiểu dữ liệu chính** | `str`, `bool` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 46–51 |

### ARCH-25 · `test_du_lieu_da_biet()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-25 |
| **File** | `tests/test_algorithm.py` |
| **Phạm vi** | Dòng 58–81 |
| **Vai trò** | Test 1 — kiểm tra với dữ liệu đã biết y=2x²+3x+1 |
| **Thành phần được gọi** | `tinh_cac_tong` (68), `lap_he_phuong_trinh_chuan_tac` (69), `giai_he_gauss` (70), `assert_gan_bang` (72–74) |
| **Trạng thái** | **CONFIRMED** |

### ARCH-26 · `test_du_lieu_csv()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-26 |
| **File** | `tests/test_algorithm.py` |
| **Phạm vi** | Dòng 88–122 |
| **Vai trò** | Test 2 — chạy pipeline đầy đủ với CSV thực tế |
| **Thành phần được gọi** | `binh_phuong_toi_thieu` (95) |
| **Trạng thái** | **CONFIRMED** |
| **Giải thích** | Kiểm tra 9 required keys (98–104), R² > 0.99 (107), 7 thong ke keys (112–115). |

### ARCH-27 · `test_validation()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-27 |
| **File** | `tests/test_algorithm.py` |
| **Phạm vi** | Dòng 129–159 |
| **Vai trò** | Test 3 — kiểm tra xử lý lỗi (3 sub-tests: 3a, 3b, 3c) |
| **Thành phần được gọi** | `kiem_tra_du_lieu` (136, 144), `doc_du_lieu_csv` (152) |
| **Trạng thái** | **CONFIRMED** |
| **Giải thích** | 3a: dữ liệu quá ít (2 điểm). 3b: len(x)≠len(y). 3c: file không tồn tại. Expect `ValueError` (3a, 3b) hoặc `FileNotFoundError` (3c). |

### ARCH-28 · `test_thong_ke()`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-28 |
| **File** | `tests/test_algorithm.py` |
| **Phạm vi** | Dòng 166–204 |
| **Vai trò** | Test 4 — kiểm tra tính nhất quán thống kê |
| **Thành phần được gọi** | `binh_phuong_toi_thieu` (172), `assert_gan_bang` (177, 184, 190) |
| **Trạng thái** | **CONFIRMED** |
| **Giải thích** | 4 assertions: SSR+SSE=SST (epsilon 1e-10), R²=SSR/SST (epsilon 1e-10), mean residual≈0 (epsilon 1e-10), 0≤R²≤1. |

### ARCH-29 · test runner `main()` (trong test_algorithm.py)

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-29 |
| **File** | `tests/test_algorithm.py` |
| **Phạm vi** | Dòng 211–240 |
| **Vai trò** | Custom test runner — chạy 4 tests, tính kết quả, exit code |
| **Đầu vào** | Không |
| **Đầu ra** | `int` (0 nếu tất cả pass, 1 nếu có fail) |
| **Thành phần gọi** | `__main__` guard dòng 243–244 |
| **Thành phần được gọi** | `test_du_lieu_da_biet` (220), `test_du_lieu_csv` (221), `test_validation` (222), `test_thong_ke` (223) |
| **Trạng thái** | **CONFIRMED** |

---

## Nhóm 6: Auxiliary Script

### ARCH-30 · `tinh_phuong_trinh_bac_2.py`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-30 |
| **File** | `tests/tinh_phuong_trinh_bac_2.py` |
| **Phạm vi** | Toàn bộ file, 11 dòng |
| **Vai trò** | Script tính nhanh — nhập x, tính y; nhập TO, tính TA=TO/y |
| **Đầu vào** | `input()` từ người dùng: x (float), TO (float) |
| **Đầu ra** | `print()`: y, TA |
| **Thành phần gọi** | Chạy trực tiếp (`python tinh_phuong_trinh_bac_2.py`) |
| **Thành phần được gọi** | Không — standalone, không import từ lsm_solver |
| **Kiểu dữ liệu chính** | `float` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp dòng 1–11 |
| **Giải thích** | Hệ số a, b, c **hardcode** (dòng 3–5) — trùng với kết quả trong `equation_result.txt`. `import numpy as np` (dòng 1) nhưng `np` không được sử dụng. Biến `TO` và `TA` không có tài liệu giải thích ý nghĩa. **Không thuộc pipeline chính.** File đang **untracked** (`??`). Phải phân biệt bằng **nét đứt** trong sơ đồ. |

---

## Nhóm 7: Dữ liệu

### ARCH-31 · `du_lieu_sau_xu_ly.csv`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-31 |
| **File** | `data/du_lieu_sau_xu_ly.csv` |
| **Phạm vi** | 32 dòng (1 header + 31 data rows) |
| **Vai trò** | Dữ liệu đầu vào mặc định |
| **Format** | CSV, 2 cột: `x` (int 0–30), `y` (float 12 chữ số thập phân) |
| **Được đọc bởi** | `doc_du_lieu_csv()` qua `binh_phuong_toi_thieu()` |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp 32 dòng |

### ARCH-32 · `Du_lieu_moi.csv`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-32 |
| **File** | `data/Du_lieu_moi.csv` |
| **Phạm vi** | 32 dòng (1 header + 31 data rows) |
| **Vai trò** | Dữ liệu đầu vào thay thế |
| **Format** | CSV, 2 cột: `x` (int 0–30), `y` (float 15 chữ số thập phân) |
| **Được đọc bởi** | Có thể dùng qua `--data` flag, nhưng không phải default |
| **Trạng thái** | **CONFIRMED** — đọc trực tiếp 32 dòng. File **untracked**. |

### ARCH-33 · `equation_result.txt`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-33 |
| **File** | `output/equation_result.txt` |
| **Vai trò** | Đầu ra — báo cáo kết quả chi tiết |
| **Được ghi bởi** | `tao_bao_cao()` |
| **Trạng thái** | **CONFIRMED** |

### ARCH-34 · `bieu_do_fit.png`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-34 |
| **File** | `output/bieu_do_fit.png` |
| **Vai trò** | Đầu ra — biểu đồ 2-panel (fit + residual) |
| **Được ghi bởi** | `tao_bieu_do_tong_hop()` |
| **Trạng thái** | **CONFIRMED** |

---

## Nhóm 8: Module-level Constants & Config

### ARCH-35 · Constants trong `lsm_solver.py`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-35 |
| **File** | `src/lsm_solver.py` |
| **Phạm vi** | Dòng 25–26 |
| **Nội dung** | `DO_CHINH_XAC = 50`, `getcontext().prec = 50` |
| **Trạng thái** | **CONFIRMED** |

### ARCH-36 · Constants trong `main.py`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-36 |
| **File** | `src/main.py` |
| **Phạm vi** | Dòng 25, 31, 38–40 |
| **Nội dung** | `sys.path.insert(0, ...)`, `getcontext().prec = 50`, `BASE_DIR`, `DEFAULT_DATA`, `OUTPUT_DIR` |
| **Trạng thái** | **CONFIRMED** |

### ARCH-37 · Constants trong `visualizer.py`

| Trường | Giá trị |
|--------|---------|
| **Evidence ID** | ARCH-37 |
| **File** | `src/visualizer.py` |
| **Phạm vi** | Dòng 14–15, 26–40 |
| **Nội dung** | `matplotlib.use('Agg')`, `FONT_CONFIG` dict, 4 colour constants (MAU_DU_LIEU, MAU_DUONG_FIT, MAU_PHAN_DU, MAU_ZERO_LINE) |
| **Trạng thái** | **CONFIRMED** |
| **Giải thích** | `import MaxNLocator` (dòng 17) nhưng không được sử dụng trong bất kỳ hàm nào. `import math` (dòng 13) cũng không được sử dụng. |
