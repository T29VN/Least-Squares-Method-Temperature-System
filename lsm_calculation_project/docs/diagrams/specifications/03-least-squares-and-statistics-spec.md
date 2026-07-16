# 03 — Least Squares and Statistics Diagram Specification

## 1. Mục đích

Sơ đồ chi tiết bên trong hàm `binh_phuong_toi_thieu()`: 8 bước tính toán từ đọc CSV đến trả về kết quả, bao gồm các kiểu dữ liệu và nhánh lỗi.

## 2. Câu hỏi mà sơ đồ trả lời

- `binh_phuong_toi_thieu()` gồm bao nhiêu bước?
- Kiểu dữ liệu nào được truyền giữa các bước?
- Ở bước nào có thể xảy ra lỗi?
- Tại sao dùng Fraction thay vì float?
- Các chỉ số thống kê nào được tính?

## 3. Phạm vi

Nội dung hàm `binh_phuong_toi_thieu()` (dòng 491–549) và các hàm nó gọi trong `lsm_solver.py`.

## 4. Thành phần cố ý không đưa vào

- `main.py` (caller — đã thể hiện trong spec 02)
- `visualizer.py` (downstream — đã thể hiện trong spec 02)
- Tests
- Chi tiết thuật toán Gauss (sẽ thể hiện trong spec 04)

## 5. Danh sách node

| Node ID | Tên | Loại | Evidence ID | Trạng thái |
|---------|-----|------|-------------|------------|
| S01 | START: nhận `duong_dan_csv` | Terminal | ARCH-12 dòng 491 | CONFIRMED |
| S02 | Bước 1: `doc_du_lieu_csv()` | Process | ARCH-04 | CONFIRMED |
| S03 | File tồn tại? | Decision | BR-01 | CONFIRMED |
| S04 | Header hợp lệ? | Decision | BR-02, BR-03 | CONFIRMED |
| S05 | Mỗi dòng: parse + validate | Process (loop) | BR-04, BR-05, BR-06 | CONFIRMED |
| S06 | Dữ liệu rỗng? | Decision | BR-07 | CONFIRMED |
| S07 | Bước 2: `kiem_tra_du_lieu()` | Process | ARCH-05 | CONFIRMED |
| S08 | n ≥ 3? x phân biệt ≥ 3? | Decision | BR-08, BR-09, BR-10 | CONFIRMED |
| S09 | Bước 3: `tinh_cac_tong()` | Process | ARCH-06 | CONFIRMED |
| S10 | Bước 4: `lap_he_phuong_trinh_chuan_tac()` | Process | ARCH-07 | CONFIRMED |
| S11 | Bước 5: `giai_he_gauss(A, B)` | Process (sub-process → spec 04) | ARCH-08 | CONFIRMED |
| S12 | Bước 6: Tính `y_du_doan` | Process | ARCH-12 dòng 521 | CONFIRMED |
| S13 | Bước 7: `tinh_thong_ke()` | Process | ARCH-10 | CONFIRMED |
| S14 | SST > 0? | Decision | BR-13 | CONFIRMED |
| S15 | df_res > 0? | Decision | BR-14 | CONFIRMED |
| S16 | MSE > 0? | Decision | BR-15 | CONFIRMED |
| S17 | `nghich_dao_ma_tran(A)` | Process | ARCH-09 | CONFIRMED |
| S18 | A_inv is None? | Decision | BR-16 | CONFIRMED |
| S19 | SE_he_so[i] > 1e-30? | Decision | BR-17 | CONFIRMED |
| S20 | y_data[i] = 0? | Decision | BR-18 | CONFIRMED |
| S21 | Bước 8a: `fraction_sang_decimal(a,b,c)` | Process | ARCH-13 | CONFIRMED |
| S22 | Bước 8b: `dinh_dang_phuong_trinh(a,b,c)` | Process | ARCH-11 | CONFIRMED |
| S23 | Đóng gói kq dict | Process | ARCH-12 dòng 533–549 | CONFIRMED |
| S24 | RETURN: kq dict | Terminal | ARCH-12 dòng 533 | CONFIRMED |
| S25 | RAISE: ValueError / FileNotFoundError | Terminal (error) | BR-01–BR-11 | CONFIRMED |

## 6. Danh sách edge

| Edge ID | Source | Target | Flow type | Dữ liệu | Hướng | Evidence | Trạng thái |
|---------|--------|--------|-----------|----------|-------|----------|------------|
| SE01 | S01 | S02 | control+data | duong_dan_csv: str/Path | → | ARCH-12 dòng 505 | CONFIRMED |
| SE02 | S02 | S03 | control | — | → | ARCH-04 dòng 79 | CONFIRMED |
| SE03 | S03 | S25 | control (no: file missing) | FileNotFoundError | → | BR-01 | CONFIRMED |
| SE04 | S03 | S04 | control (yes: exists) | file handle | → | ARCH-04 dòng 85 | CONFIRMED |
| SE05 | S04 | S25 | control (no: bad header) | ValueError | → | BR-02, BR-03 | CONFIRMED |
| SE06 | S04 | S05 | control (yes: valid) | DictReader | → | ARCH-04 dòng 98 | CONFIRMED |
| SE07 | S05 | S25 | control (error in row) | ValueError | → | BR-04, BR-05, BR-06 | CONFIRMED |
| SE08 | S05 | S06 | control (all rows ok) | x_data, y_data: list[Fraction] | → | ARCH-04 dòng 122 | CONFIRMED |
| SE09 | S06 | S25 | control (yes: empty) | ValueError | → | BR-07 | CONFIRMED |
| SE10 | S06 | S07 | control (no: has data) | x_data, y_data | → | ARCH-12 dòng 508 | CONFIRMED |
| SE11 | S07 | S08 | control | — | → | ARCH-05 | CONFIRMED |
| SE12 | S08 | S25 | control (fail) | ValueError | → | BR-08, BR-09, BR-10 | CONFIRMED |
| SE13 | S08 | S09 | control (pass) | x_data, y_data | → | ARCH-12 dòng 511 | CONFIRMED |
| SE14 | S09 | S10 | control+data | cac_tong: dict{n,Sx,Sx2,Sx3,Sx4,Sy,Sxy,Sx2y} | → | ARCH-12 dòng 514 | CONFIRMED |
| SE15 | S10 | S11 | control+data | A: 3×3 Fraction, B: 3 Fraction | → | ARCH-12 dòng 517 | CONFIRMED |
| SE16 | S11 | S25 | control (pivot=0) | ValueError | → | BR-11 | CONFIRMED |
| SE17 | S11 | S12 | control+data (ok) | nghiem: [a,b,c] Fraction | → | ARCH-12 dòng 518–521 | CONFIRMED |
| SE18 | S12 | S13 | control+data | y_du_doan: list[Fraction] | → | ARCH-12 dòng 524 | CONFIRMED |
| SE19 | S13 | S17 | control+data | A_matrix | → | ARCH-10 dòng 416 | CONFIRMED |
| SE20 | S17 | S18 | control+data | A_inv hoặc None | → | ARCH-09 | CONFIRMED |
| SE21 | S18 | S19 | control | SE_he_so (computed hoặc [0,0,0]) | → | BR-16 | CONFIRMED |
| SE22 | S13 → S14 | — | control | SST | → | BR-13 dòng 399 | CONFIRMED |
| SE23 | S13 → S15 | — | control | df_res | → | BR-14 dòng 401 | CONFIRMED |
| SE24 | S13 → S16 | — | control | MSE | → | BR-15 dòng 410 | CONFIRMED |
| SE25 | S13 → S19 | — | control | SE_he_so | → | BR-17 dòng 424 | CONFIRMED |
| SE26 | S13 → S20 | — | control | y_data[i] | → | BR-18 dòng 433 | CONFIRMED |
| SE27 | S13 | S21 | control+data | thong_ke dict + a,b,c Fraction | → | ARCH-12 dòng 527 | CONFIRMED |
| SE28 | S21 | S22 | control+data | a_dec, b_dec, c_dec Decimal | → | ARCH-12 dòng 531 | CONFIRMED |
| SE29 | S22 | S23 | control+data | phuong_trinh str | → | ARCH-12 dòng 533 | CONFIRMED |
| SE30 | S23 | S24 | control+data | kq dict (17 keys) | → | ARCH-12 dòng 533–549 | CONFIRMED |

## 7. Loại node

| Loại | Hình dạng | Nodes |
|------|-----------|-------|
| Terminal (start) | Rounded rectangle | S01 |
| Terminal (return) | Rounded rectangle (green) | S24 |
| Terminal (error) | Rounded rectangle (red) | S25 |
| Process | Rectangle | S02, S05, S07, S09, S10, S11, S12, S13, S17, S21, S22, S23 |
| Decision | Diamond | S03, S04, S06, S08, S14, S15, S16, S18, S19, S20 |

## 8. Nhãn edge

| Nhãn quan trọng |
|-----------------|
| "list[Fraction]" trên SE08, SE10, SE13, SE18 |
| "dict{n,Sx,...}" trên SE14 |
| "A 3×3, B 3-vec" trên SE15 |
| "[a,b,c] Fraction" trên SE17 |
| "thong_ke dict" trên SE27 |
| "ValueError" / "FileNotFoundError" trên error edges |

## 9. Trạng thái xác nhận

- Nodes: 25/25 CONFIRMED
- Edges: 30/30 CONFIRMED

## 10. Bố cục dự kiến

- **Top-down flowchart** (vertical)
- Error exits (S25) collected on left side with multiple incoming edges
- Decision nodes (S14–S20) within S13 có thể cần sub-group hoặc annotation
- Chú thích kiểu dữ liệu trên các edge chính

## 11. Những điểm cần duyệt trước khi vẽ

1. **S14–S20** (6 decision nodes bên trong `tinh_thong_ke`): có nên inline vào S13 hay tách thành sub-process?
2. **S11** (`giai_he_gauss`): thể hiện như sub-process với link tới spec 04?
3. **Annotation "Fraction chính xác"**: Có cần thêm annotation giải thích tại sao dùng Fraction?
