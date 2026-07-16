# Diagram Rules

## Quy tắc chung

1. **Mỗi sơ đồ phải có specification** trước khi vẽ.
   Specification nằm trong `specifications/` và mô tả đầy đủ nodes, edges, layout.

2. **Mỗi node và edge phải có Evidence ID** trỏ tới file `evidence/`.
   Không thêm thành phần nào không có bằng chứng từ mã nguồn local.

3. **Trạng thái xác nhận**: mỗi thành phần phải được phân loại:
   - `CONFIRMED` — có bằng chứng trực tiếp trong mã local
   - `INFERRED` — suy ra hợp lý nhưng không thể hiện hoàn toàn trực tiếp
   - `UNKNOWN` — chưa đủ bằng chứng

4. **Không đặt giả định về ngữ nghĩa dữ liệu.**
   - Chỉ gọi hai cột là `x` và `y`.
   - Không gọi x là nhiệt độ, y là hệ số hiệu chỉnh.
   - Không gọi TO là nhiệt độ đo hoặc TA là nhiệt độ thực.

5. **Thành phần untracked** (như `tinh_phuong_trinh_bac_2.py`) phải được
   phân biệt bằng nét đứt trong sơ đồ.

6. **Thành phần `__pycache__`** không được đưa vào sơ đồ.

## Quy trình tạo sơ đồ

1. Tạo/cập nhật evidence trong `evidence/`.
2. Tạo/cập nhật specification trong `specifications/`.
3. Đợi duyệt specification.
4. Tạo file `.drawio` trong `source/`.
5. Export sang `export/svg/` và `export/png/`.

## Cấu trúc thư mục

```
docs/diagrams/
├── DIAGRAM_RULES.md          ← File này
├── audit/                    ← Baseline và kiểm tra tính toàn vẹn
├── evidence/                 ← Bằng chứng từ mã nguồn
├── specifications/           ← Đặc tả sơ đồ (duyệt trước khi vẽ)
├── source/                   ← File .drawio gốc
└── export/
    ├── svg/                  ← Xuất SVG
    └── png/                  ← Xuất PNG
```

## Quy tắc đặt tên file

- Evidence: `{chủ-đề}-evidence.md`
- Specification: `{số thứ tự}-{tên-sơ-đồ}-spec.md`
- Source: `{số thứ tự}-{tên-sơ-đồ}.drawio`
- Export: `{số thứ tự}-{tên-sơ-đồ}.{svg|png}`
