"""
Module: visualizer.py
Tao bieu do chuyen nghiep cho ket qua binh phuong toi thieu.

Bieu do bao gom:
    1. Bieu do fit: scatter du lieu thuc + duong cong hoi quy
    2. Bieu do phan du (residuals): phan tich sai so
    3. Bieu do tong hop: ket hop ca hai tren cung mot figure

Su dung: matplotlib (backend Agg de luu file, khong can GUI)
"""

import math
import matplotlib
matplotlib.use('Agg')  # Backend khong can GUI, chi luu file
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pathlib import Path


# ============================================================
#  CAU HINH MAC DINH
# ============================================================

# Cau hinh chung cho moi bieu do
FONT_CONFIG = {
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
}

# Mau sac chuyen nghiep
MAU_DU_LIEU = '#2563EB'       # Xanh duong dam — diem du lieu
MAU_DUONG_FIT = '#DC2626'     # Do — duong fit
MAU_PHAN_DU = '#059669'       # Xanh la — thanh phan du
MAU_ZERO_LINE = '#6B7280'     # Xam — duong zero


def _cau_hinh_style():
    """Ap dung cau hinh style chung cho matplotlib."""
    plt.rcParams.update(FONT_CONFIG)
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'


# ============================================================
#  1. BIEU DO FIT (Du lieu + Duong cong hoi quy)
# ============================================================

def ve_bieu_do_fit(ax, x_data, y_data, a, b, c, phuong_trinh, R2):
    """
    Ve bieu do scatter du lieu thuc va duong cong hoi quy len axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    x_data, y_data : list[float]
    a, b, c : float
    phuong_trinh : str
    R2 : float
    """
    # Tao cac diem mịn cho duong cong
    x_min = min(x_data)
    x_max = max(x_data)
    margin = (x_max - x_min) * 0.05
    so_diem_muot = 200
    x_muot = []
    y_muot = []
    for i in range(so_diem_muot + 1):
        xi = (x_min - margin) + i * (x_max - x_min + 2 * margin) / so_diem_muot
        x_muot.append(xi)
        y_muot.append(a * xi * xi + b * xi + c)

    # Ve duong cong fit truoc (de nam duoi)
    ax.plot(
        x_muot, y_muot,
        color=MAU_DUONG_FIT,
        linewidth=2.0,
        label=f'Fit: {phuong_trinh}',
        zorder=2,
    )

    # Ve scatter du lieu thuc (nam tren)
    ax.scatter(
        x_data, y_data,
        color=MAU_DU_LIEU,
        s=60,
        edgecolors='white',
        linewidths=1.0,
        label=f'Du lieu thuc (n={len(x_data)})',
        zorder=3,
    )

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Binh phuong toi thieu — R² = {R2:.6f}')
    ax.legend(loc='best', framealpha=0.9)


# ============================================================
#  2. BIEU DO PHAN DU (Residuals)
# ============================================================

def ve_bieu_do_phan_du(ax, x_data, sai_so):
    """
    Ve bieu do phan du (residual plot) len axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    x_data : list[float]
    sai_so : list[float]
    """
    # Duong zero
    ax.axhline(
        y=0,
        color=MAU_ZERO_LINE,
        linestyle='-',
        linewidth=1.0,
        zorder=1,
    )

    # Ve thanh (stem plot bang tay)
    for i in range(len(x_data)):
        ax.plot(
            [x_data[i], x_data[i]], [0, sai_so[i]],
            color=MAU_PHAN_DU,
            linewidth=1.5,
            zorder=2,
        )

    # Ve cac diem
    ax.scatter(
        x_data, sai_so,
        color=MAU_PHAN_DU,
        s=50,
        edgecolors='white',
        linewidths=1.0,
        zorder=3,
    )

    ax.set_xlabel('x')
    ax.set_ylabel('Phan du (y_thuc - y_fit)')
    ax.set_title('Phan tich phan du (Residual Analysis)')

    # Dinh dang truc y — su dung scientific notation neu sai so nho
    ax.ticklabel_format(axis='y', style='scientific', scilimits=(-3, 3))


# ============================================================
#  3. BIEU DO TONG HOP
# ============================================================

def tao_bieu_do_tong_hop(kq, duong_dan_luu):
    """
    Tao bieu do tong hop gom 2 panel:
        - Panel tren: du lieu + duong fit
        - Panel duoi: phan du

    Parameters
    ----------
    kq : dict
        Ket qua tu ham binh_phuong_toi_thieu().
    duong_dan_luu : str hoac Path
        Duong dan luu file anh (PNG).

    Returns
    -------
    Path
        Duong dan file anh da luu.
    """
    _cau_hinh_style()

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(9, 8),
        gridspec_kw={'height_ratios': [3, 2], 'hspace': 0.35},
    )

    fig.suptitle(
        'KET QUA BINH PHUONG TOI THIEU (Least Squares Method)',
        fontweight='bold',
        y=0.97,
    )

    # Convert Fraction -> float cho matplotlib
    x_float = [float(x) for x in kq['x_data']]
    y_float = [float(y) for y in kq['y_data']]
    a_f = float(kq['a'])
    b_f = float(kq['b'])
    c_f = float(kq['c'])
    r2_f = float(kq['R2'])

    # Panel tren: bieu do fit
    ve_bieu_do_fit(
        ax1,
        x_float, y_float,
        a_f, b_f, c_f,
        kq['phuong_trinh'],
        r2_f,
    )

    # Panel duoi: bieu do phan du
    sai_so = kq.get('thong_ke', {}).get('sai_so', kq.get('sai_so', []))
    sai_so_float = [float(e) for e in sai_so]
    ve_bieu_do_phan_du(ax=ax2, x_data=x_float, sai_so=sai_so_float)

    # Luu file
    duong_dan = Path(duong_dan_luu)
    duong_dan.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(duong_dan), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    return duong_dan

