# 05 — Test Coverage Diagram Specification

## 1. Mục đích

Sơ đồ thể hiện bộ kiểm thử tự viết: 4 test cases, các hàm chúng gọi, branches được test/chưa test, và gaps.

## 2. Câu hỏi mà sơ đồ trả lời

- Mỗi test kiểm tra hàm nào?
- Test nào trực tiếp, test nào gián tiếp?
- Branches nào đã được test, branches nào chưa?
- Module nào hoàn toàn chưa test?

## 3. Phạm vi

- `test_algorithm.py` — 4 test functions + 2 helpers + runner
- Coverage map tới tất cả hàm trong `lsm_solver.py`, `main.py`, `visualizer.py`

## 4. Thành phần cố ý không đưa vào

- Chi tiết thuật toán (đã thể hiện trong spec 03, 04)
- `tinh_phuong_trinh_bac_2.py` (không có test, nhưng ghi annotation)
- Nội dung assertion (chỉ ghi tên assertion)

## 5. Danh sách node

### Test nodes

| Node ID | Tên | Loại | Evidence ID | Trạng thái |
|---------|-----|------|-------------|------------|
| T01 | `test_du_lieu_da_biet()` | Test node | ARCH-25 | CONFIRMED |
| T02 | `test_du_lieu_csv()` | Test node | ARCH-26 | CONFIRMED |
| T03 | `test_validation()` (3 sub-tests) | Test node | ARCH-27 | CONFIRMED |
| T04 | `test_thong_ke()` | Test node | ARCH-28 | CONFIRMED |
| T05 | `main()` (test runner) | Runner node | ARCH-29 | CONFIRMED |
| T06 | `assert_gan_bang()` | Helper node | ARCH-23 | CONFIRMED |
| T07 | `in_ket_qua_test()` | Helper node | ARCH-24 | CONFIRMED |

### Target function nodes (lsm_solver.py)

| Node ID | Tên | Evidence ID | Trạng thái |
|---------|-----|-------------|------------|
| F01 | `fraction_sang_decimal()` | ARCH-13 | CONFIRMED |
| F02 | `doc_du_lieu_csv()` | ARCH-04 | CONFIRMED |
| F03 | `kiem_tra_du_lieu()` | ARCH-05 | CONFIRMED |
| F04 | `tinh_cac_tong()` | ARCH-06 | CONFIRMED |
| F05 | `lap_he_phuong_trinh_chuan_tac()` | ARCH-07 | CONFIRMED |
| F06 | `giai_he_gauss()` | ARCH-08 | CONFIRMED |
| F07 | `nghich_dao_ma_tran()` | ARCH-09 | CONFIRMED |
| F08 | `tinh_thong_ke()` | ARCH-10 | CONFIRMED |
| F09 | `dinh_dang_phuong_trinh()` | ARCH-11 | CONFIRMED |
| F10 | `binh_phuong_toi_thieu()` | ARCH-12 | CONFIRMED |

### Untested module nodes

| Node ID | Tên | Evidence ID | Trạng thái |
|---------|-----|-------------|------------|
| U01 | `main.py` (6 hàm) | ARCH-01 | CONFIRMED |
| U02 | `visualizer.py` (4 hàm) | ARCH-18 | CONFIRMED |

### Branch coverage nodes

| Node ID | Tên | Evidence | Trạng thái |
|---------|-----|----------|------------|
| B01 | BR-01 (FileNotFoundError) — TESTED | BR-01, TC-03c | CONFIRMED |
| B02 | BR-08 (len mismatch) — TESTED | BR-08, TC-03b | CONFIRMED |
| B03 | BR-09 (n < 3) — TESTED | BR-09, TC-03a | CONFIRMED |
| B04 | BR-02..BR-07, BR-10..BR-21 — NOT TESTED | BR-* | CONFIRMED |

## 6. Danh sách edge

| Edge ID | Source | Target | Flow type | Dữ liệu | Hướng | Evidence | Trạng thái |
|---------|--------|--------|-----------|----------|-------|----------|------------|
| TE01 | T05 | T01 | control | invoke | → | ARCH-29 dòng 220 | CONFIRMED |
| TE02 | T05 | T02 | control | invoke | → | ARCH-29 dòng 221 | CONFIRMED |
| TE03 | T05 | T03 | control | invoke | → | ARCH-29 dòng 222 | CONFIRMED |
| TE04 | T05 | T04 | control | invoke | → | ARCH-29 dòng 223 | CONFIRMED |
| TE05 | T01 | F04 | control (direct) | x,y lists → cac_tong | → | ARCH-25 dòng 68 | CONFIRMED |
| TE06 | T01 | F05 | control (direct) | cac_tong → A,B | → | ARCH-25 dòng 69 | CONFIRMED |
| TE07 | T01 | F06 | control (direct) | A,B → nghiem | → | ARCH-25 dòng 70 | CONFIRMED |
| TE08 | T01 | T06 | control | nghiem[i], expected | → | ARCH-25 dòng 72–74 | CONFIRMED |
| TE09 | T02 | F10 | control (direct) | data_file → kq | → | ARCH-26 dòng 95 | CONFIRMED |
| TE10 | T02 | F02 | control (indirect) | via binh_phuong_toi_thieu | → | ARCH-12 dòng 505 | INFERRED |
| TE11 | T02 | F03 | control (indirect) | via binh_phuong_toi_thieu | → | ARCH-12 dòng 508 | INFERRED |
| TE12 | T02 | F04 | control (indirect) | via binh_phuong_toi_thieu | → | ARCH-12 dòng 511 | INFERRED |
| TE13 | T02 | F05 | control (indirect) | via binh_phuong_toi_thieu | → | ARCH-12 dòng 514 | INFERRED |
| TE14 | T02 | F06 | control (indirect) | via binh_phuong_toi_thieu | → | ARCH-12 dòng 517 | INFERRED |
| TE15 | T02 | F08 | control (indirect) | via binh_phuong_toi_thieu | → | ARCH-12 dòng 524 | INFERRED |
| TE16 | T02 | F07 | control (indirect) | via tinh_thong_ke | → | ARCH-10 dòng 416 | INFERRED |
| TE17 | T03 | F03 | control (direct — 3a,3b) | invalid data → ValueError | → | ARCH-27 dòng 136,144 | CONFIRMED |
| TE18 | T03 | F02 | control (direct — 3c) | missing file → FileNotFoundError | → | ARCH-27 dòng 152 | CONFIRMED |
| TE19 | T03 | B01 | coverage | — | → | TC-03c | CONFIRMED |
| TE20 | T03 | B02 | coverage | — | → | TC-03b | CONFIRMED |
| TE21 | T03 | B03 | coverage | — | → | TC-03a | CONFIRMED |
| TE22 | T04 | F10 | control (direct) | data_file → kq | → | ARCH-28 dòng 172 | CONFIRMED |
| TE23 | T04 | T06 | control | SSR+SSE vs SST etc. | → | ARCH-28 dòng 177,184,190 | CONFIRMED |
| TE24 | — | U01 | gap | Không có edge — hoàn toàn chưa test | ✗ | — | CONFIRMED |
| TE25 | — | U02 | gap | Không có edge — hoàn toàn chưa test | ✗ | — | CONFIRMED |

## 7. Loại node

| Loại | Hình dạng | Style | Nodes |
|------|-----------|-------|-------|
| Test function | Rectangle (rounded) | Blue/test colour | T01, T02, T03, T04 |
| Test runner | Rectangle (rounded, bold) | Blue/test colour | T05 |
| Test helper | Rectangle (small) | Light blue | T06, T07 |
| Target function (tested) | Rectangle | Green background | F01–F10 |
| Untested module | Rectangle | **Red/orange background, dashed** | U01, U02 |
| Branch (tested) | Small circle/badge | Green | B01, B02, B03 |
| Branch (untested) | Small circle/badge | **Red** | B04 |

## 8. Nhãn edge

| Edge type | Style | Ví dụ |
|-----------|-------|-------|
| Direct test call | Solid arrow (green) | T01 → F04 |
| Indirect test (via pipeline) | Dashed arrow (light green) | T02 ··> F02 |
| Helper call | Thin arrow | T01 → T06 |
| Coverage link | Dotted arrow | T03 ··> B01 |
| Gap (no test) | Red X or no edge | — ✗ U01 |

## 9. Trạng thái xác nhận

- Nodes: 24/24 CONFIRMED
- Edges: 18/25 CONFIRMED, 7/25 INFERRED (indirect test edges TE10–TE16)

## 10. Bố cục dự kiến

- **Left column**: Test runner + 4 test functions (vertical)
- **Center**: Target functions (lsm_solver.py) grouped vertically
- **Right column**: Untested modules (red), branch badges
- **Arrows**: solid (direct), dashed (indirect), no arrow (gap)

## 11. Những điểm cần duyệt trước khi vẽ

1. **Indirect edges** (TE10–TE16): Hiển thị riêng hay chỉ ghi annotation "gián tiếp qua binh_phuong_toi_thieu"?
2. **Branch badges**: Hiển thị tất cả 23 branches hay chỉ tóm tắt "3 tested / 20 untested"?
3. **Sub-tests** (3a, 3b, 3c): Hiển thị riêng hay gộp vào T03?
4. **Annotation cho `tinh_phuong_trinh_bac_2.py`**: Thêm ghi chú "standalone, untracked, no tests"?
