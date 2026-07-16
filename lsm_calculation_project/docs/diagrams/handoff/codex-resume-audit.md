# Codex Resume Audit

Nguon su that: working tree local tai `F:\BPTT`, doc truc tiep ngay 2026-07-16. Khong dung GitHub, khong dung GitNexus, khong chay `main.py`, `test_algorithm.py`, hay script ghi output.

## 1. Checkpoint Git dang su dung

- `git log -1 --oneline`: `2eb19ec nang cap xong`
- Checkpoint kiem soat thay doi thay the: commit `2eb19ec`.
- Baseline pre-handoff tu phien truoc co ton tai trong `docs/diagrams/audit/` va duoc kiem tra lai bang SHA-256. Cac hash trong `preexisting-protected-files.sha256` khop voi file local hien tai.

## 2. Working tree khi Codex bat dau

`git status --short` tai thoi diem bat dau:

```text
 D "Screenshot 2026-04-18 153612.png"
A  lsm_calculation_project/README.md
MM lsm_calculation_project/data/du_lieu_sau_xu_ly.csv
AM lsm_calculation_project/output/bieu_do_fit.png
MM lsm_calculation_project/output/equation_result.txt
A  lsm_calculation_project/requirements.txt
M  lsm_calculation_project/src/__pycache__/lsm_solver.cpython-314.pyc
A  lsm_calculation_project/src/__pycache__/visualizer.cpython-314.pyc
M  lsm_calculation_project/src/lsm_solver.py
M  lsm_calculation_project/src/main.py
A  lsm_calculation_project/src/visualizer.py
M  lsm_calculation_project/tests/test_algorithm.py
?? .agents/
?? analysis_report.md
?? lsm_calculation_project/data/Du_lieu_moi.csv
?? lsm_calculation_project/docs/
?? lsm_calculation_project/tests/tinh_phuong_trinh_bac_2.py
```

Khac biet chinh so voi baseline `preexisting-git-status.txt`: baseline khong co `?? lsm_calculation_project/docs/`. Do do toan bo `docs/diagrams/` la cong viec da xuat hien sau baseline pre-handoff, nhung hien tai van untracked.

## 3. Danh sach file da co trong `docs/diagrams/`

- `DIAGRAM_RULES.md`
- `audit/preexisting-git-status.txt`
- `audit/preexisting-protected-files.sha256`
- `audit/preexisting-state.md`
- `evidence/architecture-evidence.md`
- `evidence/branch-and-error-evidence.md`
- `evidence/test-coverage-evidence.md`
- `specifications/01-project-architecture-spec.md`
- `specifications/02-main-execution-pipeline-spec.md`
- `specifications/03-least-squares-and-statistics-spec.md`
- `specifications/04-gaussian-elimination-spec.md`
- `specifications/05-test-coverage-spec.md`
- `source/` ton tai nhung rong
- `export/svg/` ton tai nhung rong
- `export/png/` ton tai nhung rong

## 4. Ma tran trang thai

| Muc | Trang thai | Ghi chu ngan |
|---|---|---|
| `DIAGRAM_RULES.md` | COMPLETE | Co quy tac evidence/status/layout/ten file; phu hop voi noi dung Prompt 2. |
| `audit/preexisting-git-status.txt` | COMPLETE | Baseline co ton tai; phan anh trang thai truoc khi `docs/` xuat hien. |
| `audit/preexisting-protected-files.sha256` | COMPLETE | Hash khop voi file local hien tai cho cac file protected. |
| `audit/preexisting-state.md` | COMPLETE | Mo ta baseline, file ban, file untracked va pham vi bao ve. |
| `evidence/architecture-evidence.md` | COMPLETE | Khop voi code local: modules, functions, CSV, output, auxiliary script. |
| `evidence/branch-and-error-evidence.md` | COMPLETE | Khop voi cac nhanh trong `lsm_solver.py` va `main.py`. |
| `evidence/test-coverage-evidence.md` | COMPLETE | Khop voi custom runner trong `tests/test_algorithm.py`; khong khang dinh da chay test. |
| `specifications/01-project-architecture-spec.md` | PARTIAL | Noi dung chinh dung, nhung con muc "Nhung diem can duyet truoc khi ve". |
| `specifications/02-main-execution-pipeline-spec.md` | PARTIAL | Nodes/edges dung, nhung con cau hoi duyet ve sub-process/timing. |
| `specifications/03-least-squares-and-statistics-spec.md` | PARTIAL | Bao phu pipeline solver, nhung con quyet dinh layout/annotation. |
| `specifications/04-gaussian-elimination-spec.md` | PARTIAL | Bao phu Gauss va inverse, nhung con cau hoi ve panel/loop/detail math. |
| `specifications/05-test-coverage-spec.md` | PARTIAL | Bao phu test coverage, nhung con cau hoi ve indirect edges/branch badges/sub-tests. |
| `source/` | MISSING | Thu muc ton tai nhung khong co file `.drawio`. |
| `export/svg/` | MISSING | Thu muc ton tai nhung khong co SVG export. |
| `export/png/` | MISSING | Thu muc ton tai nhung khong co PNG export. |

Khong co muc nao duoc phan loai `INCORRECT` hay `NOT_APPLICABLE`.

## 5. Chi tiet cac muc PARTIAL hoac MISSING

### Specification files

Phan da dung:
- Moi spec da co muc dich, pham vi, nodes, edges, node types, edge labels, layout du kien va trang thai xac nhan.
- Evidence ID trong spec tro ve cac file evidence va khop voi code local doc duoc: `main.py`, `lsm_solver.py`, `visualizer.py`, `test_algorithm.py`, `tinh_phuong_trinh_bac_2.py`, hai CSV.

Phan con thieu hoac can xu ly:
- Ca 5 spec van co section "Nhung diem can duyet truoc khi ve", nen chua phai spec da khoa de render draw.io.
- `01` con can chot cach the hien auxiliary script, edge `Du_lieu_moi.csv` qua `--data`, muc chi tiet ham/constants.
- `02` con can chot `binh_phuong_toi_thieu()` la box don hay sub-process, co tach timing hay khong.
- `03` con can chot cac decision trong `tinh_thong_ke`, lien ket spec 04, annotation `Fraction`.
- `04` con can chot hai panel hay hai so do rieng, muc chi tiet loop va cong thuc.
- `05` con can chot indirect edges, branch badges, sub-tests va annotation cho auxiliary script.

Bang chung trong ma local:
- `src/main.py`: CLI co `--data`, `--output-dir`, `--no-chart`; `main()` goi solver, report writer va visualizer.
- `src/lsm_solver.py`: solver dung `Fraction`, tao normal equations, giai Gauss, tinh statistics va format equation.
- `src/visualizer.py`: Matplotlib `Agg`, bieu do fit va residual, ghi PNG.
- `tests/test_algorithm.py`: custom runner, 4 test functions, khong dung pytest/unittest.
- `tests/tinh_phuong_trinh_bac_2.py`: script standalone, untracked, hardcode he so va doc `input()`.

### `source/`, `export/svg/`, `export/png/`

Phan da dung:
- Thu muc da duoc tao dung vi tri theo `DIAGRAM_RULES.md`.

Phan con thieu:
- Chua co file `.drawio` trong `source/`.
- Chua co SVG trong `export/svg/`.
- Chua co PNG trong `export/png/`.

Bang chung:
- `Get-ChildItem -Recurse -File lsm_calculation_project\docs\diagrams\source, ...\export\svg, ...\export\png` khong tra ve file nao.

## 6. Khac biet giua tai lieu va ma local

- Khong thay mau thuan noi dung nghiem trong evidence/spec voi ma local.
- Tai lieu hien tai dung line references theo `rg -n` cho cac dinh nghia ham chinh. Luu y: `Measure-Object -Line` trong PowerShell cho ket qua thap hon do cach dem, khong nen dung de ket luan evidence sai.
- `README.md` chi liet ke `du_lieu_sau_xu_ly.csv`; evidence/spec co them `Du_lieu_moi.csv` la file untracked va chi dung duoc qua `--data`. Cach ghi nay phu hop voi code local.
- Cac file tai lieu va source co tieng Viet/ky tu dac biet; terminal `Get-Content` co the hien mojibake tuy `rg` doc dung. Can than trong lan sua tiep de khong lam hong encoding.

## 7. Hanh dong toi thieu de hoan thanh Prompt 2

1. Chot 5 specification bang cach xu ly cac muc "Nhung diem can duyet truoc khi ve"; khong can viet lai neu noi dung da dung.
2. Tao 5 file `.drawio` tu cac spec da chot trong `source/`.
3. Export 5 SVG vao `export/svg/`.
4. Export 5 PNG vao `export/png/`.
5. Kiem tra lai khong sua file ngoai `lsm_calculation_project/docs/diagrams/`.
6. Neu can bao ve baseline, khong tao baseline moi voi ten "preexisting"; dung baseline da co va checkpoint `2eb19ec`.

## 8. File du kien se sua hoac tao de hoan thanh tiep

Du kien sua:
- `specifications/01-project-architecture-spec.md`
- `specifications/02-main-execution-pipeline-spec.md`
- `specifications/03-least-squares-and-statistics-spec.md`
- `specifications/04-gaussian-elimination-spec.md`
- `specifications/05-test-coverage-spec.md`

Du kien tao:
- `source/01-project-architecture.drawio`
- `source/02-main-execution-pipeline.drawio`
- `source/03-least-squares-and-statistics.drawio`
- `source/04-gaussian-elimination.drawio`
- `source/05-test-coverage.drawio`
- `export/svg/01-project-architecture.svg`
- `export/svg/02-main-execution-pipeline.svg`
- `export/svg/03-least-squares-and-statistics.svg`
- `export/svg/04-gaussian-elimination.svg`
- `export/svg/05-test-coverage.svg`
- `export/png/01-project-architecture.png`
- `export/png/02-main-execution-pipeline.png`
- `export/png/03-least-squares-and-statistics.png`
- `export/png/04-gaussian-elimination.png`
- `export/png/05-test-coverage.png`

## 9. Rui ro co the lam mat du lieu

- Working tree dang ban va co staged/untracked files tu truoc; khong duoc dung `checkout`, `reset`, `restore`, `clean`, `stash`.
- `docs/diagrams/` dang untracked; lenh don dep Git co the xoa toan bo cong viec Prompt 2.
- Cac output `output/equation_result.txt` va `output/bieu_do_fit.png` dang modified/staged tu truoc; khong chay `main.py` vi co the ghi de.
- `test_algorithm.py` va script phu co the doc/chay code; khong chay theo yeu cau de tranh side effect/ghi output ngoai pham vi.
- Encoding tieng Viet co nguy co bi mojibake neu ghi bang cong cu/shell sai encoding.

## 10. Ket luan

SAFE_TO_RESUME

Ly do: baseline pre-handoff ton tai va hash khop; evidence hien co khop ma local; cac spec da du noi dung co ban de tiep tuc. Viec con lai chu yeu la chot cac cau hoi trong spec, tao `.drawio`, va export anh trong pham vi `lsm_calculation_project/docs/diagrams/`.
