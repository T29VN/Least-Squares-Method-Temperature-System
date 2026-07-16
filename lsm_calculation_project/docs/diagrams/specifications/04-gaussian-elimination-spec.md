# 04 — Gaussian Elimination Diagram Specification

## 1. Mục đích

Sơ đồ chi tiết thuật toán khử Gauss (`giai_he_gauss`) và nghịch đảo ma trận (`nghich_dao_ma_tran`).

## 2. Câu hỏi mà sơ đồ trả lời

- Thuật toán khử Gauss hoạt động ra sao (forward elimination + back substitution)?
- Partial pivoting thực hiện ở bước nào?
- Khi nào pivot = 0 và xử lý thế nào (raise vs return None)?
- Sự khác biệt giữa `giai_he_gauss` và `nghich_dao_ma_tran` là gì?

## 3. Phạm vi

- `giai_he_gauss()` (dòng 250–305)
- `nghich_dao_ma_tran()` (dòng 312–362)

## 4. Thành phần cố ý không đưa vào

- Hệ phương trình chuẩn tắc (đã thể hiện trong spec 03)
- `tinh_thong_ke` (caller — đã thể hiện trong spec 03)
- Các hàm không liên quan

## 5. Danh sách node

### Panel A: `giai_he_gauss()`

| Node ID | Tên | Loại | Evidence ID | Trạng thái |
|---------|-----|------|-------------|------------|
| G01 | START: nhận A (3×3), B (3-vec) | Terminal | ARCH-08 dòng 250 | CONFIRMED |
| G02 | Tạo augmented matrix M = [A|B] | Process | ARCH-08 dòng 266–270 | CONFIRMED |
| G03 | Vòng lặp cột (cot = 0..n-1) | Process (loop) | ARCH-08 dòng 273 | CONFIRMED |
| G04 | Tìm hàng có |M[hang][cot]| max (partial pivoting) | Process | ARCH-08 dòng 274–280 | CONFIRMED |
| G05 | hang_max ≠ cot? | Decision | ARCH-08 dòng 282 | CONFIRMED |
| G06 | Hoán vị hàng M[cot] ↔ M[hang_max] | Process | ARCH-08 dòng 283 | CONFIRMED |
| G07 | M[cot][cot] == 0? | Decision | BR-11 | CONFIRMED |
| G08 | RAISE ValueError("det = 0") | Terminal (error) | BR-11 dòng 287–289 | CONFIRMED |
| G09 | Khử xuôi: trừ hàng bên dưới | Process (loop) | ARCH-08 dòng 291–294 | CONFIRMED |
| G10 | Thay ngược (Back Substitution) | Process (loop) | ARCH-08 dòng 297–303 | CONFIRMED |
| G11 | RETURN: nghiem [a,b,c] Fraction | Terminal | ARCH-08 dòng 305 | CONFIRMED |

### Panel B: `nghich_dao_ma_tran()`

| Node ID | Tên | Loại | Evidence ID | Trạng thái |
|---------|-----|------|-------------|------------|
| I01 | START: nhận A (NxN) | Terminal | ARCH-09 dòng 312 | CONFIRMED |
| I02 | Tạo augmented matrix M = [A|I] | Process | ARCH-09 dòng 326–331 | CONFIRMED |
| I03 | Vòng lặp cột (cot = 0..n-1) | Process (loop) | ARCH-09 dòng 333 | CONFIRMED |
| I04 | Tìm hàng pivot max (partial pivoting) | Process | ARCH-09 dòng 334–339 | CONFIRMED |
| I05 | hang_max ≠ cot? | Decision | ARCH-09 dòng 341 | CONFIRMED |
| I06 | Hoán vị hàng | Process | ARCH-09 dòng 342 | CONFIRMED |
| I07 | pivot == 0? | Decision | BR-12 | CONFIRMED |
| I08 | RETURN None | Terminal (soft error) | BR-12 dòng 346 | CONFIRMED |
| I09 | Chia hàng pivot cho pivot value | Process | ARCH-09 dòng 348–349 | CONFIRMED |
| I10 | Khử tất cả hàng khác (Gauss-Jordan) | Process (loop) | ARCH-09 dòng 351–356 | CONFIRMED |
| I11 | Trích xuất A_inv từ phần phải | Process | ARCH-09 dòng 358–360 | CONFIRMED |
| I12 | RETURN A_inv | Terminal | ARCH-09 dòng 362 | CONFIRMED |

## 6. Danh sách edge

### Panel A edges

| Edge ID | Source | Target | Flow type | Dữ liệu | Hướng | Evidence | Trạng thái |
|---------|--------|--------|-----------|----------|-------|----------|------------|
| GE01 | G01 | G02 | control+data | A, B → M | → | dòng 266–270 | CONFIRMED |
| GE02 | G02 | G03 | control | M | → | dòng 273 | CONFIRMED |
| GE03 | G03 | G04 | control (for each cot) | cot index | → | dòng 273–274 | CONFIRMED |
| GE04 | G04 | G05 | control | hang_max | → | dòng 282 | CONFIRMED |
| GE05 | G05 | G06 | control (yes: swap) | — | → | dòng 283 | CONFIRMED |
| GE06 | G05 | G07 | control (no: no swap) | — | → | dòng 286 | CONFIRMED |
| GE07 | G06 | G07 | control | — | → | dòng 286 | CONFIRMED |
| GE08 | G07 | G08 | control (yes: zero pivot) | — | → | BR-11 | CONFIRMED |
| GE09 | G07 | G09 | control (no: non-zero) | — | → | dòng 291 | CONFIRMED |
| GE10 | G09 | G03 | control (next cot) | — | ↑ loop | dòng 273 | CONFIRMED |
| GE11 | G03 | G10 | control (loop done) | upper triangular M | → | dòng 297 | CONFIRMED |
| GE12 | G10 | G11 | control+data | nghiem list[Fraction] | → | dòng 305 | CONFIRMED |

### Panel B edges

| Edge ID | Source | Target | Flow type | Dữ liệu | Hướng | Evidence | Trạng thái |
|---------|--------|--------|-----------|----------|-------|----------|------------|
| IE01 | I01 | I02 | control+data | A → M=[A|I] | → | dòng 326–331 | CONFIRMED |
| IE02 | I02 | I03 | control | M | → | dòng 333 | CONFIRMED |
| IE03 | I03 | I04 | control (for each cot) | cot index | → | dòng 334 | CONFIRMED |
| IE04 | I04 | I05 | control | hang_max | → | dòng 341 | CONFIRMED |
| IE05 | I05 | I06 | control (yes: swap) | — | → | dòng 342 | CONFIRMED |
| IE06 | I05 | I07 | control (no) | — | → | dòng 344 | CONFIRMED |
| IE07 | I06 | I07 | control | — | → | dòng 344 | CONFIRMED |
| IE08 | I07 | I08 | control (yes: zero pivot) | — | → | BR-12 | CONFIRMED |
| IE09 | I07 | I09 | control (no) | pivot value | → | dòng 348 | CONFIRMED |
| IE10 | I09 | I10 | control | — | → | dòng 351 | CONFIRMED |
| IE11 | I10 | I03 | control (next cot) | — | ↑ loop | dòng 333 | CONFIRMED |
| IE12 | I03 | I11 | control (loop done) | [I|A_inv] | → | dòng 358 | CONFIRMED |
| IE13 | I11 | I12 | control+data | A_inv | → | dòng 362 | CONFIRMED |

## 7. Loại node

| Loại | Hình dạng | Nodes |
|------|-----------|-------|
| Terminal (start) | Rounded rectangle | G01, I01 |
| Terminal (return) | Rounded rectangle (green) | G11, I12 |
| Terminal (error — raise) | Rounded rectangle (red) | G08 |
| Terminal (error — return None) | Rounded rectangle (orange) | I08 |
| Process | Rectangle | G02, G04, G06, G09, G10, I02, I04, I06, I09, I10, I11 |
| Process (loop) | Rectangle with loop indicator | G03, I03 |
| Decision | Diamond | G05, G07, I05, I07 |

## 8. Nhãn edge

- Loop-back edges (GE10, IE11): nhãn "next cot"
- Error edges (GE08, IE08): nhãn "pivot = 0"

## 9. Trạng thái xác nhận

- Nodes: 23/23 CONFIRMED
- Edges: 25/25 CONFIRMED

## 10. Bố cục dự kiến

- **Hai panel song song** (Panel A bên trái, Panel B bên phải)
- Top-down flowchart cho mỗi panel
- Annotation giải thích sự khác biệt:
  - Panel A: forward elimination + back substitution, raise ValueError nếu pivot=0
  - Panel B: Gauss-Jordan (full elimination), return None nếu pivot=0

## 11. Những điểm cần duyệt trước khi vẽ

1. **Hai panel** hay **hai sơ đồ riêng**? Vì cả hai thuật toán rất tương đồng, đặt song song giúp so sánh.
2. **Mức chi tiết loop**: Có cần thể hiện biến `he_so = M[hang][cot] / M[cot][cot]` không? Hay chỉ cần box "khử xuôi"?
3. **Annotation toán học**: Có thêm công thức toán (M_ij = M_ij - factor * M_cot_j)?
