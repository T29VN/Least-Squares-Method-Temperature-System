# Test Coverage Evidence

> Nguồn sự thật: nội dung file local tại `f:\BPTT` đọc ngày 2026-07-16.
> Test framework: **bộ kiểm thử tự viết** (custom test runner), không phải pytest hoặc unittest.

---

## Tổng quan test suite

| Thuộc tính | Giá trị |
|------------|---------|
| **File** | `tests/test_algorithm.py` (245 dòng) |
| **Framework** | Custom test runner (không pytest, không unittest) |
| **Entry point** | `if __name__ == "__main__": sys.exit(main())` (dòng 243–244) |
| **Số test functions** | 4 |
| **Số sub-tests** | 3 (bên trong `test_validation`) |
| **Custom assertion** | `assert_gan_bang(a, b, epsilon, thong_bao)` — raise `AssertionError` |
| **Output helper** | `in_ket_qua_test(ten, thanh_cong)` — print [PASS]/[FAIL] |
| **Exit code** | 0 = tất cả pass, 1 = có fail |
| **Import từ lsm_solver** | `binh_phuong_toi_thieu`, `doc_du_lieu_csv`, `kiem_tra_du_lieu`, `tinh_cac_tong`, `lap_he_phuong_trinh_chuan_tac`, `giai_he_gauss` (dòng 24–31) |

---

## Ma trận Test Coverage

### TC-01 · `test_du_lieu_da_biet()` (dòng 58–81)

| Trường | Giá trị |
|--------|---------|
| **Test ID** | TC-01 |
| **Mô tả** | Kiểm tra với dữ liệu đã biết: y = 2x² + 3x + 1 |
| **Hàm được gọi** | `tinh_cac_tong` (68), `lap_he_phuong_trinh_chuan_tac` (69), `giai_he_gauss` (70) |
| **Hành vi được kiểm tra** | Nghiệm chính xác: a=2, b=3, c=1 |
| **Trường hợp thành công** | 3 assertions pass (a≈2, b≈3, c≈1, epsilon=1e-6) |
| **Trường hợp lỗi** | `AssertionError` nếu sai lệch > 1e-6. Bất kỳ `Exception` → return False |
| **Assertion/helper** | `assert_gan_bang(nghiem[0], 2.0)`, `assert_gan_bang(nghiem[1], 3.0)`, `assert_gan_bang(nghiem[2], 1.0)` |
| **Trạng thái** | **CONFIRMED** |

#### Hàm được test trực tiếp bởi TC-01

| Hàm | Vai trò trong test | Evidence |
|-----|---------------------|---------|
| `tinh_cac_tong` | Tính 7 tổng từ x=[0,1,2,3,4], y sinh từ y=2x²+3x+1 | ARCH-06 |
| `lap_he_phuong_trinh_chuan_tac` | Lập ma trận 3×3 từ các tổng | ARCH-07 |
| `giai_he_gauss` | Giải hệ → [a, b, c] | ARCH-08 |

#### Hàm KHÔNG được test bởi TC-01

- `doc_du_lieu_csv` — dữ liệu tạo inline, không đọc CSV
- `kiem_tra_du_lieu` — không được gọi
- `nghich_dao_ma_tran` — không được gọi
- `tinh_thong_ke` — không được gọi
- `binh_phuong_toi_thieu` — không được gọi (test gọi từng bước riêng)

---

### TC-02 · `test_du_lieu_csv()` (dòng 88–122)

| Trường | Giá trị |
|--------|---------|
| **Test ID** | TC-02 |
| **Mô tả** | Chạy pipeline đầy đủ với file CSV thực tế (`du_lieu_sau_xu_ly.csv`) |
| **Hàm được gọi** | `binh_phuong_toi_thieu` (95) — gọi gián tiếp toàn bộ pipeline |
| **Hành vi được kiểm tra** | (1) Kết quả có đủ 9 required keys, (2) R² > 0.99, (3) Thống kê có đủ 7 keys |
| **Trường hợp thành công** | Tất cả keys tồn tại, R² ≥ 0.99 |
| **Trường hợp lỗi** | `ValueError` nếu thiếu key hoặc R² < 0.99. Bất kỳ `Exception` → return False |
| **Assertion/helper** | Trực tiếp: `if key not in kq: raise ValueError(...)`, `if kq['R2'] < 0.99: raise ValueError(...)` |
| **Trạng thái** | **CONFIRMED** |

#### Hàm được test gián tiếp bởi TC-02

| Hàm | Lý do | Evidence |
|-----|-------|---------|
| `doc_du_lieu_csv` | Được gọi bởi `binh_phuong_toi_thieu` | ARCH-04 |
| `kiem_tra_du_lieu` | Được gọi bởi `binh_phuong_toi_thieu` | ARCH-05 |
| `tinh_cac_tong` | Được gọi bởi `binh_phuong_toi_thieu` | ARCH-06 |
| `lap_he_phuong_trinh_chuan_tac` | Được gọi bởi `binh_phuong_toi_thieu` | ARCH-07 |
| `giai_he_gauss` | Được gọi bởi `binh_phuong_toi_thieu` | ARCH-08 |
| `tinh_thong_ke` | Được gọi bởi `binh_phuong_toi_thieu` | ARCH-10 |
| `nghich_dao_ma_tran` | Được gọi bởi `tinh_thong_ke` | ARCH-09 |
| `fraction_sang_decimal` | Được gọi bởi `binh_phuong_toi_thieu` | ARCH-13 |
| `dinh_dang_phuong_trinh` | Được gọi bởi `binh_phuong_toi_thieu` | ARCH-11 |

#### Kiểm tra required keys (dòng 98–104)

```python
required_keys = [
    'a', 'b', 'c', 'phuong_trinh', 'x_data', 'y_data',
    'y_du_doan', 'thong_ke', 'so_diem',
]
```

#### Kiểm tra thống kê keys (dòng 112–115)

```python
tk_keys = ['SSE', 'SSR', 'SST', 'R2', 'R2_adj', 'SE_he_so', 'F_stat']
```

---

### TC-03 · `test_validation()` (dòng 129–159)

| Trường | Giá trị |
|--------|---------|
| **Test ID** | TC-03 |
| **Mô tả** | Kiểm tra xử lý lỗi khi dữ liệu không hợp lệ (3 sub-tests) |
| **Trạng thái** | **CONFIRMED** |

#### TC-03a · Dữ liệu quá ít (dòng 134–140)

| Trường | Giá trị |
|--------|---------|
| **Sub-test ID** | TC-03a |
| **Hàm được gọi** | `kiem_tra_du_lieu([1, 2], [3, 4], bac_da_thuc=2)` |
| **Hành vi được kiểm tra** | 2 điểm < 3 (bậc 2 + 1) → phải raise ValueError |
| **Trường hợp thành công** | Bắt được `ValueError` |
| **Trường hợp lỗi** | Nếu KHÔNG raise → `tat_ca_pass = False` |
| **Branch liên quan** | BR-09 |

#### TC-03b · x và y không khớp kích thước (dòng 142–148)

| Trường | Giá trị |
|--------|---------|
| **Sub-test ID** | TC-03b |
| **Hàm được gọi** | `kiem_tra_du_lieu([1, 2, 3], [4, 5], bac_da_thuc=2)` |
| **Hành vi được kiểm tra** | len(x)=3 ≠ len(y)=2 → phải raise ValueError |
| **Trường hợp thành công** | Bắt được `ValueError` |
| **Trường hợp lỗi** | Nếu KHÔNG raise → `tat_ca_pass = False` |
| **Branch liên quan** | BR-08 |

#### TC-03c · File không tồn tại (dòng 150–156)

| Trường | Giá trị |
|--------|---------|
| **Sub-test ID** | TC-03c |
| **Hàm được gọi** | `doc_du_lieu_csv("khong_ton_tai.csv")` |
| **Hành vi được kiểm tra** | File không tồn tại → phải raise FileNotFoundError |
| **Trường hợp thành công** | Bắt được `FileNotFoundError` |
| **Trường hợp lỗi** | Nếu KHÔNG raise → `tat_ca_pass = False` |
| **Branch liên quan** | BR-01 |

---

### TC-04 · `test_thong_ke()` (dòng 166–204)

| Trường | Giá trị |
|--------|---------|
| **Test ID** | TC-04 |
| **Mô tả** | Kiểm tra tính nhất quán thống kê |
| **Hàm được gọi** | `binh_phuong_toi_thieu` (172) — gọi gián tiếp toàn bộ pipeline |
| **Trạng thái** | **CONFIRMED** |

#### Assertions trong TC-04

| # | Assertion | epsilon | Dòng | Ý nghĩa |
|---|-----------|---------|------|---------|
| 1 | `SSR + SSE ≈ SST` | 1e-10 | 176–180 | Phân tách phương sai |
| 2 | `SSR / SST ≈ R²` | 1e-10 | 182–187 | Định nghĩa R² |
| 3 | `mean(residuals) ≈ 0` | 1e-10 | 189–193 | Tính chất phân dư |
| 4 | `0 ≤ R² ≤ 1` | exact | 196–197 | Ràng buộc lý thuyết |

---

## Tổng hợp coverage — Ma trận hàm × test

| Hàm (lsm_solver) | TC-01 | TC-02 | TC-03 | TC-04 | Coverage |
|---|:---:|:---:|:---:|:---:|---|
| `fraction_sang_decimal` | — | gián tiếp | — | gián tiếp | Gián tiếp qua pipeline |
| `doc_du_lieu_csv` | — | gián tiếp | trực tiếp (3c) | gián tiếp | Trực tiếp (error path) + gián tiếp (happy path) |
| `kiem_tra_du_lieu` | — | gián tiếp | trực tiếp (3a,3b) | gián tiếp | Trực tiếp (error paths) + gián tiếp (happy path) |
| `tinh_cac_tong` | trực tiếp | gián tiếp | — | gián tiếp | Trực tiếp (happy path) |
| `lap_he_phuong_trinh_chuan_tac` | trực tiếp | gián tiếp | — | gián tiếp | Trực tiếp (happy path) |
| `giai_he_gauss` | trực tiếp | gián tiếp | — | gián tiếp | Trực tiếp (happy path) |
| `nghich_dao_ma_tran` | — | gián tiếp | — | gián tiếp | Gián tiếp qua pipeline |
| `tinh_thong_ke` | — | gián tiếp | — | gián tiếp | Gián tiếp qua pipeline |
| `dinh_dang_phuong_trinh` | — | gián tiếp | — | gián tiếp | Gián tiếp qua pipeline |
| `binh_phuong_toi_thieu` | — | trực tiếp | — | trực tiếp | Trực tiếp (integration) |

| Hàm (main.py) | TC-01 | TC-02 | TC-03 | TC-04 | Coverage |
|---|:---:|:---:|:---:|:---:|---|
| `fmt_frac` | — | — | — | — | **Không test** |
| `fmt_phan_tram` | — | — | — | — | **Không test** |
| `tao_bao_cao` | — | — | — | — | **Không test** |
| `in_tom_tat` | — | — | — | — | **Không test** |
| `parse_args` | — | — | — | — | **Không test** |
| `main` (main.py) | — | — | — | — | **Không test** |

| Hàm (visualizer.py) | TC-01 | TC-02 | TC-03 | TC-04 | Coverage |
|---|:---:|:---:|:---:|:---:|---|
| `_cau_hinh_style` | — | — | — | — | **Không test** |
| `ve_bieu_do_fit` | — | — | — | — | **Không test** |
| `ve_bieu_do_phan_du` | — | — | — | — | **Không test** |
| `tao_bieu_do_tong_hop` | — | — | — | — | **Không test** |

---

## Những phần chưa được test

### Hàm chưa có test trực tiếp (chỉ gián tiếp hoặc chưa test)

| Hàm | Lý do | Rủi ro |
|-----|-------|--------|
| `nghich_dao_ma_tran` | Chỉ test gián tiếp qua pipeline. Không test trường hợp singular matrix (return None). | Trung bình — BR-12 chưa được kiểm tra |
| `tinh_thong_ke` | Chỉ test gián tiếp. Không kiểm tra từng edge case (SST=0, df_res≤0, A_inv=None, y=0). | Cao — 6 nhánh edge case chưa test (BR-13 đến BR-18) |
| `fraction_sang_decimal` | Chỉ test gián tiếp. | Thấp — hàm đơn giản |
| `dinh_dang_phuong_trinh` | Chỉ test gián tiếp. | Thấp — formatting |

### Branch chưa được test

| Branch ID | Mô tả | Hàm |
|-----------|-------|-----|
| BR-02 | CSV không có header | `doc_du_lieu_csv` |
| BR-03 | Thiếu cột x hoặc y | `doc_du_lieu_csv` |
| BR-04 | Giá trị không parse được | `doc_du_lieu_csv` |
| BR-05 | x là NaN/Inf | `doc_du_lieu_csv` |
| BR-06 | y là NaN/Inf | `doc_du_lieu_csv` |
| BR-07 | CSV rỗng | `doc_du_lieu_csv` |
| BR-10 | x phân biệt < 3 | `kiem_tra_du_lieu` |
| BR-11 | Pivot = 0 (gauss) | `giai_he_gauss` |
| BR-12 | Pivot = 0 (inverse) | `nghich_dao_ma_tran` |
| BR-13 | SST = 0 | `tinh_thong_ke` |
| BR-14 | df_res ≤ 0 | `tinh_thong_ke` |
| BR-15 | MSE ≤ 0 | `tinh_thong_ke` |
| BR-16 | A_inv is None | `tinh_thong_ke` |
| BR-17 | SE quá nhỏ | `tinh_thong_ke` |
| BR-18 | y_data[i] = 0 | `tinh_thong_ke` |
| BR-19 | --no-chart | `main()` |
| BR-20 | Exception → sys.exit(1) | `main()` |
| BR-21 | F_stat is None formatting | `tao_bao_cao`, `in_tom_tat` |

### Branch ĐÃ được test

| Branch ID | Mô tả | Test |
|-----------|-------|------|
| BR-01 | FileNotFoundError | TC-03c |
| BR-08 | len(x) ≠ len(y) | TC-03b |
| BR-09 | Số điểm < 3 | TC-03a |

### Module hoàn toàn chưa test

- `main.py` — 6 hàm (fmt_frac, fmt_phan_tram, tao_bao_cao, in_tom_tat, parse_args, main)
- `visualizer.py` — 4 hàm (_cau_hinh_style, ve_bieu_do_fit, ve_bieu_do_phan_du, tao_bieu_do_tong_hop)
- `tinh_phuong_trinh_bac_2.py` — script phụ trợ, standalone
