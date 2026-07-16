# Preexisting State — Baseline Record

## Thời điểm tạo baseline

- **Timestamp:** 2026-07-16T09:59:00+07:00 (giờ địa phương)
- **UTC:** 2026-07-16T02:59:00Z

## Project root

- **Đường dẫn:** `f:\BPTT`
- **Corpus:** `T29VN/BPTT`

## Các file đã bẩn từ trước (staged hoặc modified)

| Trạng thái | File | Giải thích |
|------------|------|------------|
| ` D` | `Screenshot 2026-04-18 153612.png` | Đã xoá trong working tree, chưa staged |
| `A ` | `lsm_calculation_project/README.md` | Mới thêm, đã staged |
| `MM` | `lsm_calculation_project/data/du_lieu_sau_xu_ly.csv` | Modified cả staged lẫn working tree |
| `AM` | `lsm_calculation_project/output/bieu_do_fit.png` | Added và staged, rồi modified thêm trong working tree |
| `MM` | `lsm_calculation_project/output/equation_result.txt` | Modified cả staged lẫn working tree |
| `A ` | `lsm_calculation_project/requirements.txt` | Mới thêm, đã staged |
| `M ` | `lsm_calculation_project/src/__pycache__/lsm_solver.cpython-314.pyc` | Bytecode modified, đã staged |
| `A ` | `lsm_calculation_project/src/__pycache__/visualizer.cpython-314.pyc` | Bytecode mới thêm, đã staged |
| `M ` | `lsm_calculation_project/src/lsm_solver.py` | Modified, đã staged |
| `M ` | `lsm_calculation_project/src/main.py` | Modified, đã staged |
| `A ` | `lsm_calculation_project/src/visualizer.py` | Mới thêm, đã staged |
| `M ` | `lsm_calculation_project/tests/test_algorithm.py` | Modified, đã staged |

## Các file untracked từ trước

| File | Ghi chú |
|------|---------|
| `.agents/` | Thư mục cấu hình agent skills |
| `analysis_report.md` | Báo cáo phân tích tạo trước đó |
| `lsm_calculation_project/data/Du_lieu_moi.csv` | Dữ liệu đầu vào thay thế |
| `lsm_calculation_project/tests/tinh_phuong_trinh_bac_2.py` | Script tính toán phụ trợ |

## Các file được bảo vệ bằng SHA-256

Toàn bộ 13 file sau đã được ghi nhận SHA-256 tại thời điểm baseline:

1. `lsm_calculation_project/src/lsm_solver.py`
2. `lsm_calculation_project/src/main.py`
3. `lsm_calculation_project/src/visualizer.py`
4. `lsm_calculation_project/tests/test_algorithm.py`
5. `lsm_calculation_project/tests/tinh_phuong_trinh_bac_2.py`
6. `lsm_calculation_project/data/du_lieu_sau_xu_ly.csv`
7. `lsm_calculation_project/data/Du_lieu_moi.csv`
8. `lsm_calculation_project/output/equation_result.txt`
9. `lsm_calculation_project/output/bieu_do_fit.png`
10. `lsm_calculation_project/README.md`
11. `lsm_calculation_project/requirements.txt`
12. `AGENTS.md`
13. `CLAUDE.md`

Chi tiết SHA-256 xem tại: `preexisting-protected-files.sha256`

## Lưu ý quan trọng

> Working tree không sạch **không đồng nghĩa** phiên hiện tại gây ra thay đổi.
>
> Tất cả trạng thái bẩn được liệt kê ở trên đều **tồn tại từ trước** khi phiên
> làm việc hiện tại bắt đầu. Phiên hiện tại chỉ tạo file mới trong thư mục
> `lsm_calculation_project/docs/diagrams/` và không sửa bất kỳ file nào bên ngoài
> thư mục đó.
>
> SHA-256 manifest cho phép xác minh rằng không có file bảo vệ nào bị thay đổi
> bởi phiên hiện tại.
