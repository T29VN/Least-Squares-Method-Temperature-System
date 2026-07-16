from __future__ import annotations

import os
import re
import xml.etree.ElementTree as ET
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "source"
DRAWIO = SOURCE / "BPTT_system_diagrams.drawio"
TMP = SOURCE / "BPTT_system_diagrams.tmp.drawio"
RESUME = BASE / "resume_state.md"
REPORT = BASE / "completion_report.md"
TZ = timezone(timedelta(hours=7))

SOURCE.mkdir(parents=True, exist_ok=True)
(BASE / "export" / "svg").mkdir(parents=True, exist_ok=True)
(BASE / "export" / "png").mkdir(parents=True, exist_ok=True)

PAGES = [
    ("01 — Kiến trúc tổng quan", "Trang 1 — Kiến trúc tổng quan"),
    ("02 — Luồng thực thi chính", "Trang 2 — Luồng thực thi chính"),
    ("03 — Bình phương tối thiểu và thống kê", "Trang 3 — Bình phương tối thiểu và thống kê"),
    ("04 — Khử Gauss", "Trang 4 — Khử Gauss"),
    ("05 — Phạm vi kiểm thử", "Trang 5 — Phạm vi kiểm thử"),
]

FONT = "fontFamily=Arial;fontSize=12;"
BASE_STYLE = f"whiteSpace=wrap;html=1;{FONT}align=center;verticalAlign=middle;"
STYLES = {
    "title": "text;html=1;strokeColor=none;fillColor=none;fontFamily=Arial;fontSize=22;fontStyle=1;align=center;",
    "note": "text;html=1;strokeColor=none;fillColor=none;fontFamily=Arial;fontSize=11;align=left;verticalAlign=top;",
    "container": f"swimlane;html=1;whiteSpace=wrap;startSize=30;container=1;collapsible=0;recursiveResize=0;{FONT}fontStyle=1;fillColor=#f8f9fa;strokeColor=#666666;",
    "process": "rounded=1;arcSize=8;" + BASE_STYLE + "fillColor=#dae8fc;strokeColor=#6c8ebf;",
    "module": "rounded=1;arcSize=8;" + BASE_STYLE + "fillColor=#ffe6cc;strokeColor=#d79b00;",
    "result": "rounded=1;arcSize=8;" + BASE_STYLE + "fillColor=#d5e8d4;strokeColor=#82b366;",
    "grey": "rounded=1;arcSize=8;" + BASE_STYLE + "fillColor=#f5f5f5;strokeColor=#666666;",
    "term": "rounded=1;arcSize=50;" + BASE_STYLE + "fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;",
    "error": "rounded=1;arcSize=12;" + BASE_STYLE + "fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;",
    "decision": "rhombus;" + BASE_STYLE + "fillColor=#fff2cc;strokeColor=#d6b656;",
    "data": "shape=document;boundedLbl=1;" + BASE_STYLE + "fillColor=#e1d5e7;strokeColor=#9673a6;",
    "output": "shape=document;boundedLbl=1;" + BASE_STYLE + "fillColor=#d5e8d4;strokeColor=#82b366;",
    "dashed": "rounded=1;arcSize=8;dashed=1;dashPattern=8 4;" + BASE_STYLE + "fillColor=#f5f5f5;strokeColor=#666666;",
}
EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;fontFamily=Arial;fontSize=11;labelBackgroundColor=#ffffff;endArrow=block;endFill=1;strokeColor=#666666;"
EDGE_DASHED = EDGE + "dashed=1;dashPattern=8 4;"
EDGE_ERROR = EDGE + "strokeColor=#b85450;fontColor=#b85450;"
EDGE_OK = EDGE + "strokeColor=#82b366;fontColor=#2d7600;"


def graph() -> ET.Element:
    model = ET.Element("mxGraphModel", {
        "dx": "1100", "dy": "780", "grid": "1", "gridSize": "10", "guides": "1",
        "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1",
        "pageScale": "1", "pageWidth": "1169", "pageHeight": "827", "math": "0", "shadow": "0",
    })
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    return model


def root(model: ET.Element) -> ET.Element:
    return model.find("root")


def meta(source: str, scope: str, role: str, confidence: str = "CONFIRMED") -> dict[str, str]:
    return {
        "source_file": source,
        "function_or_scope": scope,
        "confidence": confidence,
        "diagram_role": role,
    }


def add_node(parent: ET.Element, item: tuple) -> None:
    node_id, label, kind, x, y, w, h, source, scope, role, *rest = item
    confidence = rest[0] if rest else "CONFIRMED"
    obj = ET.SubElement(parent, "object", {
        "id": node_id,
        "label": label,
        **meta(source, scope, role, confidence),
    })
    mx = ET.SubElement(obj, "mxCell", {"style": STYLES[kind], "vertex": "1", "parent": "1"})
    ET.SubElement(mx, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})


def add_text(parent: ET.Element, node_id: str, label: str, x: int, y: int, w: int, h: int, title: bool = False) -> None:
    mx = ET.SubElement(parent, "mxCell", {
        "id": node_id, "value": label, "style": STYLES["title" if title else "note"], "vertex": "1", "parent": "1",
    })
    ET.SubElement(mx, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})


def add_edge(parent: ET.Element, item: tuple) -> None:
    edge_id, src, dst, label, *rest = item
    flavor = rest[0] if rest else ""
    style = {"dashed": EDGE_DASHED, "error": EDGE_ERROR, "ok": EDGE_OK}.get(flavor, EDGE)
    mx = ET.SubElement(parent, "mxCell", {
        "id": edge_id, "value": label, "style": style, "edge": "1", "parent": "1", "source": src, "target": dst,
    })
    ET.SubElement(mx, "mxGeometry", {"relative": "1", "as": "geometry"})


def legend(parent: ET.Element, prefix: str, entries: list[tuple[str, str]]) -> None:
    add_text(parent, prefix + "_legend_title", "Chú giải: màu/viền chỉ hỗ trợ đọc nhanh; nhãn và edge mới là nguồn ý nghĩa.", 40, 745, 520, 25)
    x = 40
    for idx, (label, kind) in enumerate(entries):
        add_node(parent, (f"{prefix}_leg_{idx}", label, kind, x, 775, 150, 28, "docs/diagrams", "legend", "legend"))
        x += 165


def make_page(name: str, subtitle: str, nodes: list[tuple], edges: list[tuple], legends: list[tuple[str, str]]) -> ET.Element:
    model = graph()
    r = root(model)
    prefix = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
    add_text(r, prefix + "_title", name, 50, 20, 1060, 32, True)
    add_text(r, prefix + "_subtitle", subtitle, 65, 60, 1040, 35)
    for item in nodes:
        add_node(r, item)
    for item in edges:
        add_edge(r, item)
    legend(r, prefix, legends)
    return model


def page1() -> ET.Element:
    nodes = [
        ("p1_in", "Đầu vào", "container", 35, 110, 250, 210, "data", "CSV inputs", "container"),
        ("p1_pipe", "Pipeline chính", "container", 325, 100, 500, 320, "src", "main pipeline", "container"),
        ("p1_out", "Đầu ra", "container", 865, 110, 260, 250, "output", "runtime outputs", "container"),
        ("p1_np", "Kiểm thử và script phụ, tách khỏi production", "container", 250, 470, 690, 165, "tests", "non-production", "container"),
        ("p1_default", "du_lieu_sau_xu_ly.csv\ndữ liệu mặc định", "data", 60, 160, 200, 60, "data/du_lieu_sau_xu_ly.csv", "CSV x,y", "default input"),
        ("p1_alt", "Du_lieu_moi.csv\ndữ liệu thay thế qua --data", "data", 60, 245, 200, 60, "data/Du_lieu_moi.csv", "CSV x,y", "alternate input"),
        ("p1_main", "main.py\nCLI orchestrator", "module", 360, 160, 120, 65, "src/main.py", "main(), parse_args()", "orchestrator"),
        ("p1_solver", "lsm_solver.py\ncore solver", "process", 535, 160, 130, 65, "src/lsm_solver.py", "binh_phuong_toi_thieu()", "solver"),
        ("p1_kq", "kq\ndictionary kết quả", "result", 700, 160, 105, 65, "src/lsm_solver.py", "return dict", "result"),
        ("p1_summary", "in_tom_tat(kq)", "grey", 410, 300, 125, 55, "src/main.py", "in_tom_tat()", "console formatter"),
        ("p1_report", "tao_bao_cao(kq)", "grey", 570, 300, 130, 55, "src/main.py", "tao_bao_cao()", "text writer"),
        ("p1_viz", "visualizer.py\ntao_bieu_do_tong_hop(kq)", "process", 720, 300, 150, 65, "src/visualizer.py", "tao_bieu_do_tong_hop()", "chart renderer"),
        ("p1_stdout", "Console stdout", "output", 890, 160, 210, 55, "src/main.py", "print()", "console output"),
        ("p1_txt", "output/equation_result.txt", "output", 890, 230, 210, 55, "output/equation_result.txt", "written by tao_bao_cao()", "text output"),
        ("p1_png", "output/bieu_do_fit.png", "output", 890, 300, 210, 55, "output/bieu_do_fit.png", "written by visualizer", "image output"),
        ("p1_test", "tests/test_algorithm.py\ncustom test runner", "dashed", 300, 535, 255, 70, "tests/test_algorithm.py", "main(), four test functions", "test runner"),
        ("p1_aux", "tests/tinh_phuong_trinh_bac_2.py\nscript phụ, untracked", "dashed", 635, 535, 255, 70, "tests/tinh_phuong_trinh_bac_2.py", "standalone input()/print()", "auxiliary script"),
    ]
    edges = [
        ("p1e1", "p1_default", "p1_main", "CSV"),
        ("p1e2", "p1_alt", "p1_main", "--data", "dashed"),
        ("p1e3", "p1_main", "p1_solver", "gọi solver"),
        ("p1e4", "p1_solver", "p1_kq", "trả kq"),
        ("p1e5", "p1_kq", "p1_summary", "kq"),
        ("p1e6", "p1_summary", "p1_stdout", "print"),
        ("p1e7", "p1_kq", "p1_report", "kq"),
        ("p1e8", "p1_report", "p1_txt", "ghi TXT"),
        ("p1e9", "p1_kq", "p1_viz", "kq"),
        ("p1e10", "p1_viz", "p1_png", "ghi PNG"),
    ]
    return make_page(PAGES[0][0], "Tổng quan project local. Không suy diễn ý nghĩa vật lý của x, y, TO hoặc TA.", nodes, edges, [("Module/xử lý", "process"), ("File dữ liệu", "data"), ("Đầu ra", "output"), ("Tách khỏi production", "dashed")])


def page2() -> ET.Element:
    nodes = [
        ("p2_start", "Bắt đầu\npython main.py", "term", 60, 110, 150, 55, "src/main.py", "__main__ guard", "start"),
        ("p2_parse", "parse_args()", "process", 60, 200, 150, 55, "src/main.py", "parse_args()", "CLI parsing"),
        ("p2_paths", "Xác định data path,\noutput directory và --no-chart", "process", 45, 290, 185, 70, "src/main.py", "main(): path setup", "path setup"),
        ("p2_solver", "binh_phuong_toi_thieu(data_path)", "process", 45, 405, 185, 65, "src/main.py", "main() calls solver", "solver call"),
        ("p2_err_dec", "FileNotFoundError\nhoặc ValueError?", "decision", 70, 510, 140, 90, "src/main.py", "except block", "error decision"),
        ("p2_print_err", "In thông báo lỗi", "error", 300, 520, 145, 55, "src/main.py", "print error", "error handling"),
        ("p2_exit1", "sys.exit(1)\nkết thúc lỗi", "error", 525, 520, 145, 60, "src/main.py", "sys.exit(1)", "error end"),
        ("p2_summary", "in_tom_tat(kq)\n+ in thời gian", "grey", 300, 650, 155, 65, "src/main.py", "in_tom_tat()", "summary output"),
        ("p2_report", "tao_bao_cao(kq, txt_file)\nlưu equation_result.txt", "grey", 510, 650, 185, 65, "src/main.py", "tao_bao_cao()", "text report"),
        ("p2_dec_chart", "--no-chart?", "decision", 760, 635, 130, 95, "src/main.py", "if not args.no_chart", "chart decision"),
        ("p2_skip", "Bỏ qua biểu đồ", "module", 960, 610, 135, 55, "src/main.py", "else branch", "skip chart"),
        ("p2_chart", "tao_bieu_do_tong_hop(kq, chart_file)\nlưu bieu_do_fit.png", "process", 935, 725, 190, 70, "src/main.py; src/visualizer.py", "chart branch", "chart output"),
        ("p2_done", "HOÀN TẤT\nexit code 0", "term", 760, 760, 140, 55, "src/main.py", "normal completion", "success end"),
    ]
    edges = [
        ("p2e1", "p2_start", "p2_parse", ""), ("p2e2", "p2_parse", "p2_paths", "args"),
        ("p2e3", "p2_paths", "p2_solver", "data_path"), ("p2e4", "p2_solver", "p2_err_dec", "kq hoặc exception"),
        ("p2e5", "p2_err_dec", "p2_print_err", "Có", "error"), ("p2e6", "p2_print_err", "p2_exit1", ""),
        ("p2e7", "p2_err_dec", "p2_summary", "Không", "ok"), ("p2e8", "p2_summary", "p2_report", "kq"),
        ("p2e9", "p2_report", "p2_dec_chart", ""), ("p2e10", "p2_dec_chart", "p2_skip", "Có"),
        ("p2e11", "p2_dec_chart", "p2_chart", "Không", "ok"), ("p2e12", "p2_skip", "p2_done", "hoàn tất"),
        ("p2e13", "p2_chart", "p2_done", "hoàn tất"),
    ]
    return make_page(PAGES[1][0], "Luồng chính của main.py, gồm nhánh lỗi và nhánh --no-chart với nhãn Có/Không trên edge.", nodes, edges, [("Bắt đầu/kết thúc", "term"), ("Xử lý", "process"), ("Điều kiện", "decision"), ("Ngoại lệ", "error")])


def page3() -> ET.Element:
    labels = [
        ("p3_start", "binh_phuong_toi_thieu()"), ("p3_read", "doc_du_lieu_csv()"), ("p3_val", "kiem_tra_du_lieu()"),
        ("p3_sum", "tinh_cac_tong()"), ("p3_norm", "lap_he_phuong_trinh_chuan_tac()"), ("p3_gauss", "giai_he_gauss()"),
        ("p3_abc", "nghiệm\n[a, b, c]"), ("p3_yhat", "tính y_du_doan"),
    ]
    nodes = [(id_, label, "process" if id_ != "p3_abc" else "result", 25 + i * 142, 110, 125, 60, "src/lsm_solver.py", label, "solver step") for i, (id_, label) in enumerate(labels)]
    nodes += [
        ("p3_stats", "tinh_thong_ke()\nnhóm thống kê", "container", 135, 250, 760, 270, "src/lsm_solver.py", "tinh_thong_ke()", "statistics group"),
        ("p3_res", "residuals", "grey", 165, 310, 120, 45, "src/lsm_solver.py", "sai_so", "statistic"),
        ("p3_ss", "SSE, SSR, SST", "grey", 315, 310, 120, 45, "src/lsm_solver.py", "SSE/SSR/SST", "statistic"),
        ("p3_r2", "R² và R²_adj", "grey", 465, 310, 120, 45, "src/lsm_solver.py", "R2/R2_adj", "statistic"),
        ("p3_ms", "MSE và MSR", "grey", 615, 310, 120, 45, "src/lsm_solver.py", "MSE/MSR", "statistic"),
        ("p3_f", "F statistic", "grey", 165, 405, 120, 45, "src/lsm_solver.py", "F_stat", "statistic"),
        ("p3_inv", "nghich_dao_ma_tran(A)", "grey", 315, 405, 150, 45, "src/lsm_solver.py", "nghich_dao_ma_tran()", "statistic"),
        ("p3_se", "SE hệ số", "grey", 505, 405, 120, 45, "src/lsm_solver.py", "SE_he_so", "statistic"),
        ("p3_t", "t-statistics\nsai số phần trăm", "grey", 655, 405, 150, 50, "src/lsm_solver.py", "t_stats/sai_so_phan_tram", "statistic"),
        ("p3_special", "Nhánh đặc biệt\nSST = 0\ndf_res <= 0\nMSE <= 0\nA_inv is None\nSE quá nhỏ\ny_data[i] = 0", "decision", 940, 270, 170, 210, "src/lsm_solver.py", "tinh_thong_ke() branches", "special branches"),
        ("p3_errors", "Nhóm ngoại lệ đọc/validation\nFileNotFoundError, ValueError,\npivot = 0", "error", 25, 315, 100, 150, "src/lsm_solver.py", "read/validation/gauss exceptions", "exceptions"),
        ("p3_fmt", "dinh_dang_phuong_trinh()", "process", 310, 590, 180, 60, "src/lsm_solver.py", "dinh_dang_phuong_trinh()", "format equation"),
        ("p3_pack", "đóng gói dictionary kq", "result", 545, 590, 170, 60, "src/lsm_solver.py", "return dict", "package result"),
        ("p3_return", "trả kết quả kq", "term", 770, 590, 150, 60, "src/lsm_solver.py", "return", "return"),
    ]
    chain = [x[0] for x in labels]
    edges = [(f"p3e{i}", chain[i], chain[i + 1], "") for i in range(len(chain) - 1)]
    edges += [
        ("p3e_stats", "p3_yhat", "p3_stats", "x_data, y_data, y_du_doan, A"),
        ("p3e_sp", "p3_stats", "p3_special", "edge cases", "dashed"),
        ("p3e_fmt", "p3_stats", "p3_fmt", "thong_ke"),
        ("p3e_pack", "p3_fmt", "p3_pack", "phuong_trinh"),
        ("p3e_ret", "p3_pack", "p3_return", "kq"),
        ("p3e_err1", "p3_read", "p3_errors", "lỗi đọc CSV", "error"),
        ("p3e_err2", "p3_val", "p3_errors", "lỗi validation", "error"),
        ("p3e_err3", "p3_gauss", "p3_errors", "pivot 0", "error"),
    ]
    return make_page(PAGES[2][0], "Pipeline solver dùng Fraction cho tính toán chính; các lỗi đọc và validation được gom để giữ sơ đồ dễ đọc.", nodes, edges, [("Bước tính toán", "process"), ("Nhóm thống kê", "container"), ("Nhánh đặc biệt", "decision"), ("Ngoại lệ", "error")])


def page4() -> ET.Element:
    nodes = [
        ("p4_start", "Nhận A và B", "term", 80, 100, 150, 55, "src/lsm_solver.py", "giai_he_gauss(A, B)", "start"),
        ("p4_aug", "Tạo ma trận mở rộng\nM = [A|B]", "process", 80, 195, 170, 60, "src/lsm_solver.py", "augmented matrix", "setup"),
        ("p4_loop", "Lặp theo từng cột pivot", "module", 80, 305, 170, 60, "src/lsm_solver.py", "for cot in range(n)", "loop"),
        ("p4_find", "Tìm hàng có trị tuyệt đối\npivot lớn nhất", "process", 330, 305, 190, 60, "src/lsm_solver.py", "partial pivoting", "pivot selection"),
        ("p4_swap_dec", "Cần đổi hàng?", "decision", 585, 290, 130, 90, "src/lsm_solver.py", "if hang_max != cot", "swap decision"),
        ("p4_swap", "Đổi hàng", "module", 790, 245, 120, 50, "src/lsm_solver.py", "row swap", "row swap"),
        ("p4_pivot_dec", "Pivot bằng 0?", "decision", 790, 350, 130, 90, "src/lsm_solver.py", "if M[cot][cot] == 0", "zero pivot decision"),
        ("p4_error", "ValueError:\nma trận suy biến", "error", 980, 365, 145, 65, "src/lsm_solver.py", "raise ValueError", "error end"),
        ("p4_elim", "Khử các phần tử\nphía dưới pivot", "process", 560, 500, 180, 60, "src/lsm_solver.py", "forward elimination", "eliminate below"),
        ("p4_more", "Còn cột pivot?", "decision", 330, 485, 130, 90, "src/lsm_solver.py", "loop continuation", "loop decision"),
        ("p4_back", "Thế ngược", "process", 330, 640, 150, 55, "src/lsm_solver.py", "back substitution", "back substitution"),
        ("p4_return", "Trả [a, b, c]", "term", 580, 640, 150, 55, "src/lsm_solver.py", "return nghiem", "return"),
        ("p4_end", "Kết thúc", "term", 830, 640, 130, 55, "src/lsm_solver.py", "normal end", "end"),
    ]
    edges = [
        ("p4e1", "p4_start", "p4_aug", ""), ("p4e2", "p4_aug", "p4_loop", ""),
        ("p4e3", "p4_loop", "p4_find", ""), ("p4e4", "p4_find", "p4_swap_dec", ""),
        ("p4e5", "p4_swap_dec", "p4_swap", "Có"), ("p4e6", "p4_swap", "p4_pivot_dec", ""),
        ("p4e7", "p4_swap_dec", "p4_pivot_dec", "Không", "ok"),
        ("p4e8", "p4_pivot_dec", "p4_error", "Có", "error"),
        ("p4e9", "p4_pivot_dec", "p4_elim", "Không", "ok"),
        ("p4e10", "p4_elim", "p4_more", ""), ("p4e11", "p4_more", "p4_loop", "Có"),
        ("p4e12", "p4_more", "p4_back", "Không", "ok"), ("p4e13", "p4_back", "p4_return", ""),
        ("p4e14", "p4_return", "p4_end", ""),
    ]
    return make_page(PAGES[3][0], "Không ghi determinant vì mã chỉ kiểm tra pivot bằng 0 sau partial pivoting.", nodes, edges, [("Vòng lặp pivot", "module"), ("Điều kiện", "decision"), ("Ngoại lệ", "error"), ("Kết thúc", "term")])


def page5() -> ET.Element:
    nodes = [
        ("p5_runner", "main()\ncustom test runner", "module", 55, 130, 170, 65, "tests/test_algorithm.py", "main()", "test runner"),
        ("p5_assert", "assert_gan_bang()", "grey", 55, 260, 170, 50, "tests/test_algorithm.py", "assert_gan_bang()", "helper"),
        ("p5_print", "in_ket_qua_test()", "grey", 55, 330, 170, 50, "tests/test_algorithm.py", "in_ket_qua_test()", "helper"),
        ("p5_exit", "Thu pass/fail\nexit code 0 hoặc 1", "term", 55, 610, 170, 65, "tests/test_algorithm.py", "return code", "test result"),
        ("p5_t1", "test_du_lieu_da_biet()", "process", 315, 105, 185, 60, "tests/test_algorithm.py", "test_du_lieu_da_biet()", "test"),
        ("p5_t2", "test_du_lieu_csv()", "process", 315, 225, 185, 60, "tests/test_algorithm.py", "test_du_lieu_csv()", "test"),
        ("p5_t3", "test_validation()", "process", 315, 345, 185, 60, "tests/test_algorithm.py", "test_validation()", "test"),
        ("p5_t4", "test_thong_ke()", "process", 315, 465, 185, 60, "tests/test_algorithm.py", "test_thong_ke()", "test"),
        ("p5_sum", "tinh_cac_tong()", "result", 610, 70, 210, 52, "src/lsm_solver.py", "tinh_cac_tong()", "production"),
        ("p5_norm", "lap_he_phuong_trinh_chuan_tac()", "result", 610, 145, 210, 52, "src/lsm_solver.py", "lap_he_phuong_trinh_chuan_tac()", "production"),
        ("p5_gauss", "giai_he_gauss()", "result", 610, 220, 210, 52, "src/lsm_solver.py", "giai_he_gauss()", "production"),
        ("p5_pipeline", "binh_phuong_toi_thieu()", "result", 610, 310, 210, 52, "src/lsm_solver.py", "binh_phuong_toi_thieu()", "production"),
        ("p5_check", "kiem_tra_du_lieu()", "result", 610, 400, 210, 52, "src/lsm_solver.py", "kiem_tra_du_lieu()", "production"),
        ("p5_read", "doc_du_lieu_csv()", "result", 610, 475, 210, 52, "src/lsm_solver.py", "doc_du_lieu_csv()", "production"),
        ("p5_gap", "Chưa test trực tiếp\nmain.py: fmt/report/CLI/main\nvisualizer.py: vẽ và lưu PNG", "dashed", 875, 170, 235, 155, "src/main.py; src/visualizer.py", "not directly tested", "coverage gap"),
    ]
    edges = [
        ("p5e1", "p5_runner", "p5_t1", "chạy"), ("p5e2", "p5_runner", "p5_t2", "chạy"),
        ("p5e3", "p5_runner", "p5_t3", "chạy"), ("p5e4", "p5_runner", "p5_t4", "chạy"),
        ("p5e5", "p5_runner", "p5_exit", "tổng hợp"), ("p5e6", "p5_t1", "p5_sum", "trực tiếp"),
        ("p5e7", "p5_t1", "p5_norm", "trực tiếp"), ("p5e8", "p5_t1", "p5_gauss", "trực tiếp"),
        ("p5e9", "p5_t1", "p5_assert", "so sánh", "dashed"), ("p5e10", "p5_t2", "p5_pipeline", "trực tiếp"),
        ("p5e11", "p5_t3", "p5_check", "3a, 3b"), ("p5e12", "p5_t3", "p5_read", "3c"),
        ("p5e13", "p5_t4", "p5_pipeline", "trực tiếp"), ("p5e14", "p5_t4", "p5_assert", "thống kê", "dashed"),
        ("p5e15", "p5_pipeline", "p5_gap", "không test trực tiếp", "dashed"),
    ]
    return make_page(PAGES[4][0], "Custom test runner tự viết: chạy bốn test, thu pass/fail, trả exit code 0 hoặc 1.", nodes, edges, [("Test/runner", "process"), ("Helper", "grey"), ("Production được gọi", "result"), ("Coverage gap", "dashed")])


BUILDERS = {
    PAGES[0][0]: page1,
    PAGES[1][0]: page2,
    PAGES[2][0]: page3,
    PAGES[3][0]: page4,
    PAGES[4][0]: page5,
}


def mxfile() -> ET.Element:
    return ET.Element("mxfile", {
        "host": "drawio", "modified": datetime.now(TZ).isoformat(),
        "agent": "Codex", "version": "26.0.0", "type": "device",
    })


def load() -> ET.Element:
    if DRAWIO.exists():
        try:
            root_el = ET.parse(DRAWIO).getroot()
            if root_el.tag == "mxfile":
                return root_el
        except ET.ParseError:
            pass
    return mxfile()


def names(mx: ET.Element) -> set[str]:
    return {d.get("name", "") for d in mx.findall("diagram")}


def set_page(mx: ET.Element, name: str, model: ET.Element) -> None:
    kept = {d.get("name", ""): d for d in mx.findall("diagram") if d.get("name") != name}
    d = ET.Element("diagram", {"id": re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_"), "name": name})
    d.append(model)
    kept[name] = d
    for old in list(mx.findall("diagram")):
        mx.remove(old)
    for page_name, _ in PAGES:
        if page_name in kept:
            mx.append(kept[page_name])
    for page_name, diag in kept.items():
        if page_name not in dict(PAGES):
            mx.append(diag)


def validate(path: Path, expected: set[str]) -> None:
    mx = ET.parse(path).getroot()
    if mx.tag != "mxfile":
        raise ValueError("draw.io XML root must be mxfile")
    found = names(mx)
    missing = expected - found
    if missing:
        raise ValueError(f"Missing pages: {sorted(missing)}")
    for d in mx.findall("diagram"):
        model = d.find("mxGraphModel")
        if model is None or model.find("root") is None:
            raise ValueError(f"Invalid page: {d.get('name')}")
        ids = set()
        for el in model.find("root"):
            cell_id = el.get("id")
            if cell_id in ids:
                raise ValueError(f"Duplicate id {cell_id} on page {d.get('name')}")
            ids.add(cell_id)
            mxcell = el.find("mxCell") if el.tag == "object" else el
            if mxcell is not None and mxcell.get("edge") == "1" and mxcell.find("mxGeometry") is None:
                raise ValueError(f"Edge without geometry: {mxcell.get('id')}")


def save(mx: ET.Element, completed: set[str]) -> None:
    mx.set("modified", datetime.now(TZ).isoformat())
    out = deepcopy(mx)
    ET.indent(out, space="  ")
    ET.ElementTree(out).write(TMP, encoding="UTF-8", xml_declaration=True)
    validate(TMP, completed)
    os.replace(TMP, DRAWIO)


def completed_from_resume() -> set[str]:
    if not RESUME.exists():
        return set()
    text = RESUME.read_text(encoding="utf-8")
    return {name for name, short in PAGES if f"- [x] {short}" in text}


def logs_from_resume() -> list[str]:
    if not RESUME.exists():
        return []
    lines = RESUME.read_text(encoding="utf-8").splitlines()
    if "## Nhật ký" not in lines:
        return []
    return [line for line in lines[lines.index("## Nhật ký") + 1:] if line.strip()]


def write_resume(completed: set[str], logs: list[str]) -> None:
    lines = ["# Resume State", "", "## Tiến độ", ""]
    for name, short in PAGES:
        lines.append(f"- [{'x' if name in completed else ' '}] {short}")
    lines += ["", "## Nhật ký", ""]
    lines.extend(logs)
    RESUME.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    logs = logs_from_resume()
    completed = completed_from_resume()
    if not RESUME.exists():
        write_resume(completed, logs)
    mx = load()
    for name, short in PAGES:
        if name in completed and name in names(mx):
            continue
        set_page(mx, name, BUILDERS[name]())
        completed.add(name)
        save(mx, completed)
        validate(DRAWIO, completed)
        logs.append(f"- {datetime.now(TZ).isoformat(timespec='seconds')}: COMPLETE {short} — đã lưu và validate XML.")
        write_resume(completed, logs)
        mx = load()

    validate(DRAWIO, completed)
    report = [
        "# Completion Report", "",
        "- Đường dẫn file draw.io: `lsm_calculation_project/docs/diagrams/source/BPTT_system_diagrams.drawio`",
        "- Các trang hoàn thành:",
    ]
    for name, short in PAGES:
        if name in completed:
            report.append(f"  - {short}")
    report.append("- Các trang chưa hoàn thành:")
    missing = [short for name, short in PAGES if name not in completed]
    report.extend([f"  - {m}" for m in missing] or ["  - Không có"])
    report += [
        "- Lỗi còn tồn tại: chưa render bằng draw.io CLI tại thời điểm tạo XML; file XML đã parse hợp lệ.",
        "- Xác nhận: không sửa file ngoài `lsm_calculation_project/docs/diagrams/`.",
    ]
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"saved={DRAWIO}")
    print(f"completed={len(completed)}/{len(PAGES)}")


if __name__ == "__main__":
    main()
