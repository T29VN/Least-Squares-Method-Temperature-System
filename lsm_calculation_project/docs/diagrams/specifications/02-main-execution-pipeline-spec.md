# 02 — Main Execution Pipeline Diagram Specification

## 1. Mục đích

Sơ đồ luồng thực thi chính (flowchart) khi chạy `python main.py`: từ CLI arguments đến khi tạo xong output.

## 2. Câu hỏi mà sơ đồ trả lời

- Khi chạy `python main.py`, các bước diễn ra theo thứ tự nào?
- Dữ liệu nào được truyền giữa các bước?
- Nhánh nào có thể xảy ra (lỗi, --no-chart)?
- Khi nào chương trình dừng (thành công hay lỗi)?

## 3. Phạm vi

Luồng thực thi từ `if __name__ == "__main__"` trong `main.py` qua `binh_phuong_toi_thieu()` và các hàm output.

## 4. Thành phần cố ý không đưa vào

- Chi tiết bên trong `binh_phuong_toi_thieu()` (sẽ thể hiện trong spec 03)
- Chi tiết thuật toán Gauss (sẽ thể hiện trong spec 04)
- Tests và auxiliary script
- Hàm lồng, constants

## 5. Danh sách node

| Node ID | Tên | Loại | Evidence ID | Trạng thái |
|---------|-----|------|-------------|------------|
| P01 | START: `python main.py` | Terminal | ARCH-01 dòng 301 | CONFIRMED |
| P02 | `parse_args()` | Process | ARCH-02 | CONFIRMED |
| P03 | Tạo Path objects (data_path, output_dir, txt_file, chart_file) | Process | ARCH-03 dòng 264–269 | CONFIRMED |
| P04 | `binh_phuong_toi_thieu(data_path)` | Process (sub-pipeline) | ARCH-12 | CONFIRMED |
| P05 | Exception? | Decision | BR-20 | CONFIRMED |
| P06 | Print LOI + `sys.exit(1)` | Terminal (error) | BR-20 dòng 278–279 | CONFIRMED |
| P07 | `in_tom_tat(kq)` | Process | ARCH-17 | CONFIRMED |
| P08 | Print thời gian tính toán | Process | ARCH-03 dòng 285 | CONFIRMED |
| P09 | `tao_bao_cao(kq, txt_file)` | Process | ARCH-16 | CONFIRMED |
| P10 | `--no-chart`? | Decision | BR-19 | CONFIRMED |
| P11 | `tao_bieu_do_tong_hop(kq, chart_file)` | Process | ARCH-18 | CONFIRMED |
| P12 | Print "Bo qua bieu do" | Process | BR-19 dòng 296 | CONFIRMED |
| P13 | Print "HOAN TAT!" | Process | ARCH-03 dòng 298 | CONFIRMED |
| P14 | END (exit code 0) | Terminal | ARCH-03 | CONFIRMED |
| P15 | `equation_result.txt` | Data output | ARCH-33 | CONFIRMED |
| P16 | `bieu_do_fit.png` | Data output | ARCH-34 | CONFIRMED |
| P17 | Console stdout | Data output | ARCH-17 | CONFIRMED |

## 6. Danh sách edge

| Edge ID | Source | Target | Flow type | Dữ liệu | Hướng | Evidence | Trạng thái |
|---------|--------|--------|-----------|----------|-------|----------|------------|
| PE01 | P01 | P02 | control | sys.argv | → | ARCH-01 dòng 301–302 | CONFIRMED |
| PE02 | P02 | P03 | control+data | args Namespace | → | ARCH-03 dòng 262–269 | CONFIRMED |
| PE03 | P03 | P04 | control+data | data_path | → | ARCH-03 dòng 276 | CONFIRMED |
| PE04 | P04 | P05 | control | kq hoặc exception | → | ARCH-03 dòng 275–279 | CONFIRMED |
| PE05 | P05 | P06 | control (yes: exception) | FileNotFoundError / ValueError | → | BR-20 | CONFIRMED |
| PE06 | P05 | P07 | control (no: success) | kq dict | → | ARCH-03 dòng 284 | CONFIRMED |
| PE07 | P07 | P08 | control | — | → | ARCH-03 dòng 285 | CONFIRMED |
| PE08 | P07 | P17 | data | Console text | → | ARCH-17 | CONFIRMED |
| PE09 | P08 | P09 | control | kq, txt_file | → | ARCH-03 dòng 289 | CONFIRMED |
| PE10 | P09 | P15 | data | File write | → | ARCH-16 dòng 184 | CONFIRMED |
| PE11 | P09 | P10 | control | — | → | ARCH-03 dòng 292 | CONFIRMED |
| PE12 | P10 | P11 | control (no: create chart) | kq, chart_file | → | BR-19 false branch | CONFIRMED |
| PE13 | P10 | P12 | control (yes: skip chart) | — | → | BR-19 true branch | CONFIRMED |
| PE14 | P11 | P16 | data | File write PNG | → | ARCH-18 dòng 216 | CONFIRMED |
| PE15 | P11 | P13 | control | — | → | ARCH-03 dòng 298 | CONFIRMED |
| PE16 | P12 | P13 | control | — | → | ARCH-03 dòng 298 | CONFIRMED |
| PE17 | P13 | P14 | control | — | → | implicit | CONFIRMED |
| PE18 | P06 | — | terminal | exit code 1 | ⊣ | BR-20 | CONFIRMED |

## 7. Loại node

| Loại | Hình dạng | Nodes |
|------|-----------|-------|
| Terminal (start) | Rounded rectangle (green) | P01 |
| Terminal (error) | Rounded rectangle (red) | P06 |
| Terminal (end) | Rounded rectangle (green) | P14 |
| Process | Rectangle | P02, P03, P04, P07, P08, P09, P11, P12, P13 |
| Decision | Diamond | P05, P10 |
| Data output | Parallelogram or document | P15, P16, P17 |

## 8. Nhãn edge

| Edge | Nhãn |
|------|------|
| PE05 | "FileNotFoundError / ValueError" |
| PE06 | "kq dict" |
| PE10 | "ghi equation_result.txt" |
| PE12 | "no (tạo biểu đồ)" |
| PE13 | "yes (--no-chart)" |
| PE14 | "ghi bieu_do_fit.png" |

## 9. Trạng thái xác nhận

- Nodes: 17/17 CONFIRMED
- Edges: 18/18 CONFIRMED

## 10. Bố cục dự kiến

- **Top-down flowchart** (vertical)
- Decision diamonds cho P05 và P10
- Hai nhánh song song từ P10 (chart / no-chart) hội tụ tại P13
- Data output ở bên phải (P15, P16, P17)
- Error terminal P06 tách sang bên trái

## 11. Những điểm cần duyệt trước khi vẽ

1. **P04** ("binh_phuong_toi_thieu") nên là một box đơn hay collapsible sub-process? Nếu là sub-process, cần link tới spec 03.
2. **P08** ("thời gian tính toán") có đáng hiển thị riêng hay gộp vào P07?
3. **Timing**: `time.perf_counter()` bắt đầu trước P04, kết thúc sau P04 — cần thể hiện không?
