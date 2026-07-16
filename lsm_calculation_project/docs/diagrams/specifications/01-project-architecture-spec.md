# 01 — Project Architecture Diagram Specification

## 1. Mục đích

Sơ đồ tổng quan kiến trúc project: các module, file, hàm, dữ liệu và quan hệ giữa chúng.

## 2. Câu hỏi mà sơ đồ trả lời

- Project gồm những module nào?
- Mỗi module chứa những hàm nào?
- Module nào phụ thuộc module nào (import)?
- Dữ liệu đầu vào đi vào từ đâu và đầu ra xuất ra đâu?
- Thành phần nào là auxiliary (không thuộc pipeline chính)?

## 3. Phạm vi

Toàn bộ project `lsm_calculation_project/` bao gồm:
- 3 source modules (`main.py`, `lsm_solver.py`, `visualizer.py`)
- 1 test module (`test_algorithm.py`)
- 1 auxiliary script (`tinh_phuong_trinh_bac_2.py`)
- 2 data files, 2 output files

## 4. Thành phần cố ý không đưa vào

- `__pycache__/` và bytecode files
- `.git/`, `.agents/`, `.gitnexus/`
- `AGENTS.md`, `CLAUDE.md` (cấu hình agent, không phải code)
- `requirements.txt` (manifest, không phải executable)
- Hàm lồng `fmt` bên trong `dinh_dang_phuong_trinh`
- Module-level imports và constants (trừ khi thể hiện dependency)

## 5. Danh sách node

| Node ID | Tên | Loại node | Evidence ID | Trạng thái |
|---------|-----|-----------|-------------|------------|
| N01 | `main.py` | Module (container) | ARCH-01 | CONFIRMED |
| N02 | `parse_args()` | Function | ARCH-02 | CONFIRMED |
| N03 | `main()` | Function (entry) | ARCH-03 | CONFIRMED |
| N04 | `fmt_frac()` | Function | ARCH-14 | CONFIRMED |
| N05 | `fmt_phan_tram()` | Function | ARCH-15 | CONFIRMED |
| N06 | `tao_bao_cao()` | Function | ARCH-16 | CONFIRMED |
| N07 | `in_tom_tat()` | Function | ARCH-17 | CONFIRMED |
| N08 | `lsm_solver.py` | Module (container) | ARCH-12 | CONFIRMED |
| N09 | `fraction_sang_decimal()` | Function | ARCH-13 | CONFIRMED |
| N10 | `doc_du_lieu_csv()` | Function | ARCH-04 | CONFIRMED |
| N11 | `kiem_tra_du_lieu()` | Function | ARCH-05 | CONFIRMED |
| N12 | `tinh_cac_tong()` | Function | ARCH-06 | CONFIRMED |
| N13 | `lap_he_phuong_trinh_chuan_tac()` | Function | ARCH-07 | CONFIRMED |
| N14 | `giai_he_gauss()` | Function | ARCH-08 | CONFIRMED |
| N15 | `nghich_dao_ma_tran()` | Function | ARCH-09 | CONFIRMED |
| N16 | `tinh_thong_ke()` | Function | ARCH-10 | CONFIRMED |
| N17 | `dinh_dang_phuong_trinh()` | Function | ARCH-11 | CONFIRMED |
| N18 | `binh_phuong_toi_thieu()` | Function (orchestrator) | ARCH-12 | CONFIRMED |
| N19 | `visualizer.py` | Module (container) | ARCH-18 | CONFIRMED |
| N20 | `_cau_hinh_style()` | Function | ARCH-19 | CONFIRMED |
| N21 | `ve_bieu_do_fit()` | Function | ARCH-20 | CONFIRMED |
| N22 | `ve_bieu_do_phan_du()` | Function | ARCH-21 | CONFIRMED |
| N23 | `tao_bieu_do_tong_hop()` | Function | ARCH-18 | CONFIRMED |
| N24 | `test_algorithm.py` | Module (container) | ARCH-22 | CONFIRMED |
| N25 | `tinh_phuong_trinh_bac_2.py` | Script (auxiliary, dashed) | ARCH-30 | CONFIRMED |
| N26 | `du_lieu_sau_xu_ly.csv` | Data file | ARCH-31 | CONFIRMED |
| N27 | `Du_lieu_moi.csv` | Data file (dashed — untracked) | ARCH-32 | CONFIRMED |
| N28 | `equation_result.txt` | Output file | ARCH-33 | CONFIRMED |
| N29 | `bieu_do_fit.png` | Output file | ARCH-34 | CONFIRMED |

## 6. Danh sách edge

| Edge ID | Source | Target | Flow type | Dữ liệu | Hướng | Evidence | Trạng thái |
|---------|--------|--------|-----------|----------|-------|----------|------------|
| E01 | N03 (main) | N02 (parse_args) | control | args | → | ARCH-03 dòng 262 | CONFIRMED |
| E02 | N03 (main) | N18 (binh_phuong_toi_thieu) | control+data | data_path → kq dict | → | ARCH-03 dòng 276 | CONFIRMED |
| E03 | N03 (main) | N07 (in_tom_tat) | control+data | kq dict | → | ARCH-03 dòng 284 | CONFIRMED |
| E04 | N03 (main) | N06 (tao_bao_cao) | control+data | kq dict + txt_file path | → | ARCH-03 dòng 289 | CONFIRMED |
| E05 | N03 (main) | N23 (tao_bieu_do_tong_hop) | control+data | kq dict + chart_file path | → | ARCH-03 dòng 294 | CONFIRMED |
| E06 | N18 (binh_phuong_toi_thieu) | N10 (doc_du_lieu_csv) | control+data | duong_dan_csv → (x_data, y_data) | → | ARCH-12 dòng 505 | CONFIRMED |
| E07 | N18 | N11 (kiem_tra_du_lieu) | control+data | x_data, y_data, bac=2 | → | ARCH-12 dòng 508 | CONFIRMED |
| E08 | N18 | N12 (tinh_cac_tong) | control+data | x_data, y_data → cac_tong dict | → | ARCH-12 dòng 511 | CONFIRMED |
| E09 | N18 | N13 (lap_he_phuong_trinh_chuan_tac) | control+data | cac_tong → (A, B) | → | ARCH-12 dòng 514 | CONFIRMED |
| E10 | N18 | N14 (giai_he_gauss) | control+data | A, B → nghiem [a,b,c] | → | ARCH-12 dòng 517 | CONFIRMED |
| E11 | N18 | N16 (tinh_thong_ke) | control+data | x_data, y_data, y_du_doan, nghiem, A → thong_ke dict | → | ARCH-12 dòng 524 | CONFIRMED |
| E12 | N18 | N09 (fraction_sang_decimal) | control+data | a,b,c Fraction → a_dec,b_dec,c_dec Decimal | → | ARCH-12 dòng 527–529 | CONFIRMED |
| E13 | N18 | N17 (dinh_dang_phuong_trinh) | control+data | a,b,c Fraction → phuong_trinh str | → | ARCH-12 dòng 531 | CONFIRMED |
| E14 | N16 (tinh_thong_ke) | N15 (nghich_dao_ma_tran) | control+data | A_matrix → A_inv | → | ARCH-10 dòng 416 | CONFIRMED |
| E15 | N17 (dinh_dang_phuong_trinh) | N09 (fraction_sang_decimal) | control+data | Fraction → Decimal (qua nested fmt) | → | ARCH-11 dòng 467 | CONFIRMED |
| E16 | N07 (in_tom_tat) | N04 (fmt_frac) | control+data | Fraction/Decimal → str | → | ARCH-17 dòng 210–212 | CONFIRMED |
| E17 | N07 (in_tom_tat) | N05 (fmt_phan_tram) | control+data | Fraction/float → str | → | ARCH-17 dòng 217–218 | CONFIRMED |
| E18 | N06 (tao_bao_cao) | N04 (fmt_frac) | control+data | Fraction/Decimal → str | → | ARCH-16 nhiều dòng | CONFIRMED |
| E19 | N06 (tao_bao_cao) | N05 (fmt_phan_tram) | control+data | Fraction/float → str | → | ARCH-16 dòng 156–157, 174 | CONFIRMED |
| E20 | N04 (fmt_frac) | N09 (fraction_sang_decimal) | control+data | Fraction → Decimal | → | ARCH-14 dòng 50 | CONFIRMED |
| E21 | N23 (tao_bieu_do_tong_hop) | N20 (_cau_hinh_style) | control | — | → | ARCH-18 dòng 177 | CONFIRMED |
| E22 | N23 | N21 (ve_bieu_do_fit) | control+data | ax, x/y float, a/b/c float, str, R2 | → | ARCH-18 dòng 200 | CONFIRMED |
| E23 | N23 | N22 (ve_bieu_do_phan_du) | control+data | ax, x float, sai_so float | → | ARCH-18 dòng 211 | CONFIRMED |
| E24 | N10 (doc_du_lieu_csv) | N26 (du_lieu_sau_xu_ly.csv) | data | Đọc CSV → Fraction | ← | ARCH-04 dòng 85 | CONFIRMED |
| E25 | N10 (doc_du_lieu_csv) | N27 (Du_lieu_moi.csv) | data | Đọc CSV → Fraction (qua --data) | ← | ARCH-04 (gián tiếp qua --data) | INFERRED |
| E26 | N06 (tao_bao_cao) | N28 (equation_result.txt) | data | Ghi file TXT | → | ARCH-16 dòng 184 | CONFIRMED |
| E27 | N23 (tao_bieu_do_tong_hop) | N29 (bieu_do_fit.png) | data | Ghi file PNG | → | ARCH-18 dòng 216 | CONFIRMED |
| E28 | N01 (main.py) | N08 (lsm_solver.py) | import | `from lsm_solver import ...` | → | ARCH-01 dòng 27 | CONFIRMED |
| E29 | N01 (main.py) | N19 (visualizer.py) | import | `from visualizer import ...` | → | ARCH-01 dòng 28 | CONFIRMED |
| E30 | N24 (test_algorithm.py) | N08 (lsm_solver.py) | import | `from lsm_solver import ...` | → | ARCH-22 dòng 24–31 | CONFIRMED |

## 7. Loại node

| Loại | Hình dạng | Màu/style | Nodes |
|------|-----------|-----------|-------|
| Module (container) | Rectangle with rounded corners, containment | Light background | N01, N08, N19, N24 |
| Function (normal) | Rectangle | Default | N02, N04–N07, N09–N17, N20–N22 |
| Function (entry) | Rectangle, bold border | Highlighted | N03 |
| Function (orchestrator) | Rectangle, double border | Highlighted | N18 |
| Function (tạo output) | Rectangle | Highlighted output | N06, N23 |
| Script (auxiliary) | Rectangle, **dashed border** | Grayed/dashed | N25 |
| Data file (default) | Cylinder/document | Data color | N26 |
| Data file (untracked) | Cylinder/document, **dashed border** | Grayed/dashed | N27 |
| Output file | Cylinder/document | Output color | N28, N29 |

## 8. Nhãn edge

| Loại | Style | Ví dụ |
|------|-------|-------|
| control flow | Solid arrow | → |
| data flow | Solid arrow with label | "kq dict" → |
| import | Dashed arrow | ---> |
| data read | Thin arrow, from data to function | ← |
| data write | Thin arrow, from function to data | → |

## 9. Trạng thái xác nhận tổng hợp

- Nodes: 29/29 CONFIRMED
- Edges: 29/30 CONFIRMED, 1/30 INFERRED (E25 — Du_lieu_moi.csv qua --data flag)

## 10. Bố cục dự kiến

- **Top-down**: main.py → lsm_solver.py → visualizer.py
- **Trái**: data files (input)
- **Phải**: output files
- **Dưới cùng, tách biệt**: test_algorithm.py, tinh_phuong_trinh_bac_2.py (dashed)
- Containment: các hàm nằm bên trong module container

## 11. Những điểm cần duyệt trước khi vẽ

1. **N25 (tinh_phuong_trinh_bac_2.py)** nên nằm ở vị trí nào? Hiện tại đặt riêng, dashed, không có edge vào pipeline. Có cần thêm annotation ghi chú "hardcode hệ số từ output"?
2. **E25** là INFERRED — có chấp nhận edge này trong sơ đồ không?
3. **Mức chi tiết hàm**: Có cần hiển thị tất cả 27 hàm hay chỉ nhóm theo module?
4. **Constants** (ARCH-35, 36, 37): có cần hiển thị `DO_CHINH_XAC`, `BASE_DIR`, `FONT_CONFIG` không?
