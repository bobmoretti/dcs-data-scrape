#%%
import numpy as np
import matplotlib.pyplot as pl
import matplotlib
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import pandas as pd

# import scipy.signal as sigР

MPS_PER_KNOT = 0.514444
MPS2_PER_G = 9.82
M_PER_FT = 0.3048


def make_doghouse_grid():
    speeds = np.linspace(100, 1000, 1024 * 16, endpoint=False) * MPS_PER_KNOT
    x = speeds / MPS_PER_KNOT

    matplotlib.style.use("seaborn-ticks")
    pl.rcParams["font.size"] = 10

    MAX_TRT = 34

    GRID_COLOR = (.1, .1, .1)

    pl.figure(dpi=128, figsize=[12, 10])
    for load_factor in range(1, 11):
        y = np.rad2deg((load_factor * MPS2_PER_G) / speeds)
        where_is_visible = np.where(y < MAX_TRT)
        x1 = x[where_is_visible]
        y1 = y[where_is_visible]
        pl.plot(x1, y1, color="gray", ls="--", lw=0.6)
        ylabel_pos = min(y1[0], MAX_TRT-0.5)
        pl.annotate(f"{load_factor}", (x1[0] - 10, ylabel_pos), fontsize=8, color=GRID_COLOR)

    radii = np.array(
        [
            1000,
            1500,
            2000,
            2500,
            3000,
            4000,
            5000,
            6000,
            8000,
            10000,
            15000,
            20000,
            25000,
            30000,
            40000,
            50000,
            60000,
        ]
    )

    for r0_ft in radii:
        r0 = r0_ft * M_PER_FT
        accel = (speeds ** 2 / r0) / MPS2_PER_G
        where_is_in_limits = np.where(np.logical_and(1 <= accel, accel <= 10))
        y = np.rad2deg(speeds / r0)
        x2 = x[where_is_in_limits]
        y2 = y[where_is_in_limits]
        pl.plot(x2, y2, color="gray", ls="--", lw=0.6)
        pl.annotate(f"{r0_ft}", (x2[0] - 30, y2[0] - 0.5), fontsize=6, color=GRID_COLOR)

    pl.annotate('Turn radius (feet)', (100, 2.5), fontsize=9, color=GRID_COLOR)
    pl.annotate('Load factor (g)', (340, MAX_TRT-.4), fontsize=9, color=GRID_COLOR)

    ax = pl.gca()
    ax.xaxis.set_minor_locator(MultipleLocator(20))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.axes.xaxis.set_visible(True)
    ax.axes.yaxis.set_visible(True)

    pl.grid(True)

    pl.ylim(0, MAX_TRT)
    pl.xlabel("TAS (knots)")
    pl.ylabel("TRT (°/s)")
    return ax

ax = make_doghouse_grid()    

airframe_data_log = pd.read_csv('data/f16_em00.csv')
load_factor = airframe_data_log['ny']
tas = airframe_data_log['tas']

trt = np.rad2deg((load_factor * MPS2_PER_G) / tas)
# ax.plot(tas/MPS_PER_KNOT, trt, 'x')

vvi = airframe_data_log['vvi']
nx = airframe_data_log['nx']
dv = np.array(np.diff(tas)/np.diff(airframe_data_log['time']))
dv_smoothed = np.fft.irfft(np.fft.rfft(dv)[:len(dv)//40], len(dv))

Ps = vvi[1:] + tas[1:]*dv_smoothed
im = ax.scatter(tas[1:]/MPS_PER_KNOT, trt[1:], c=Ps*196.85, cmap='viridis')
cbar = pl.gcf().colorbar(im, ax=ax)
cbar.ax.set_title('P_s\n(ft/min)')

pl.title('DCS F-16 turn performance at ~1000ft (clean, 50% fuel)')
pl.tight_layout()
pl.savefig("doghouse.png", transparent=False)


# # %%
# l2 = pd.read_csv('log.csv')
# pl.plot(l2['nx'])

# #%%
# fig, (p1, p2) = pl.subplots(2, 1, sharex=True, dpi=128, figsize=[10, 10])
# p1.plot(tas)
# p2.plot(nx)

# #%%
# pl.figure(dpi=128, figsize=[8, 8])

# dv = np.array(np.diff(tas)/np.diff(airframe_data_log['time']))
# dv_smoothed = np.fft.irfft(np.fft.rfft(dv)[:len(dv)//40], len(dv))
# pl.plot(dv,'o')
# pl.plot(dv_smoothed, 'o')
# # %%
# %matplotlib qt