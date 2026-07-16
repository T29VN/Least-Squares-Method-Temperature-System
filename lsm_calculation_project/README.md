# Binh Phuong Toi Thieu — Least Squares Method

Chuong trinh tinh toan hoi quy da thuc bac 2 bang phuong phap binh phuong toi thieu.

**Mo hinh:**  `y = a·x² + b·x + c`

## Cau truc du an

```
lsm_calculation_project/
├── data/
│   └── du_lieu_sau_xu_ly.csv   # Du lieu dau vao (x, y)
├── output/
│   ├── equation_result.txt     # Bao cao ket qua chi tiet
│   └── bieu_do_fit.png         # Bieu do fit + phan du
├── src/
│   ├── lsm_solver.py           # Thuat toan chinh (core)
│   ├── visualizer.py           # Tao bieu do (matplotlib)
│   └── main.py                 # Chuong trinh chinh (CLI)
├── tests/
│   └── test_algorithm.py       # Test suite
├── requirements.txt
└── README.md
```

## Cai dat

```bash
pip install -r requirements.txt
```

## Su dung

### Chay mac dinh (doc du lieu tu `data/du_lieu_sau_xu_ly.csv`):
```bash
cd src
python main.py
```

### Chi dinh file du lieu khac:
```bash
python main.py --data "duong/dan/file.csv"
```

### Chi xuat file TXT (khong tao bieu do):
```bash
python main.py --no-chart
```

### Chay test:
```bash
python tests/test_algorithm.py
```

## Ket qua dau ra

### File TXT (`output/equation_result.txt`)
- Cac he so hoi quy kem sai so chuan (Standard Error)
- Thong ke t (t-statistic)
- Bang phan tich phuong sai (ANOVA)
- R², Adjusted R², F-statistic
- Phan tich phan du chi tiet
- Bang so sanh: x, y_thuc, y_fit, phan_du, sai_so_%

### Bieu do (`output/bieu_do_fit.png`)
- Panel tren: scatter du lieu thuc + duong cong hoi quy
- Panel duoi: bieu do phan du (residual analysis)

## Dinh dang file du lieu dau vao

File CSV voi 2 cot `x` va `y`:
```csv
x,y
0,1.0021021
10,1.0003003
20,0.9870871
```
