#!/usr/bin/env python3
"""Regenerate the Track-2 hero image with the CORRECT Carnot bound.

Paper 10 (Phonon Extraction Bound) fix: the efficiency bound is the textbook
Carnot form  eta <= 1 - T/T_res , NOT the super-Carnot  1/(1 + T/T_res).
At r = T/T_res = 0.2 the ceiling is 0.80 (a 20% suppression), and at T = T_res
Carnot gives eta -> 0 (no work between equal temperatures).
Outputs both SVG (vector) and PNG.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

BG      = "#0a0a0b"
PURPLE  = "#8b6dff"
PURPSUB = "#9184ef"
ORANGE  = "#f5a623"
GOLD    = "#ffc23c"
GREYDOT = "#c4c4cc"
GREYLBL = "#8a8a97"
WHITE   = "#f6f6f9"
AXIS    = "#d3d3db"
GRID    = "#20202b"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "svg.fonttype": "path",
})

fig = plt.figure(figsize=(12.13, 7.33), dpi=100)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0.075, 0.14, 0.845, 0.63])
ax.set_facecolor(BG)

# ---- the Carnot bound ----
r = np.logspace(-25.4, 0.0, 3000)      # T/T_res in (0, 1]
eta = 1.0 - r                          # Carnot

ax.set_xscale("log")
ax.set_xlim(3e-26, 1.35)
ax.set_ylim(-0.02, 1.06)

# faint naive reference + shaded "it bites" regime
ax.axhline(1.0, color=GREYLBL, lw=1.0, ls=(0, (6, 5)), alpha=0.55)
ax.axvspan(0.03, 1.0, color=PURPLE, alpha=0.065, lw=0)

# thin verticals under the astrophysical anchor points
for rx in (1e-23, 1e-15, 2e-9):
    ax.plot([rx, rx], [0.0, 1.0], color=GRID, lw=1.0, zorder=1)

# the bound
ax.plot(r, eta, color=PURPLE, lw=3.6, solid_capstyle="round", zorder=5)

# anchor points (all vacuous at eta~1) + trivial limit at eta=0
for rx in (1e-23, 1e-15, 2e-9):
    ax.plot(rx, 1.0, "o", ms=11, mfc=GREYDOT, mec=BG, mew=2.0, zorder=6)
ax.plot(1.0, 0.0, "o", ms=11, mfc=GREYDOT, mec=BG, mew=2.0, zorder=6)

# the BEC operating point: r = 0.2 -> eta = 0.80
r_bec = 0.2
ax.plot(r_bec, 1 - r_bec, marker="*", ms=30, mfc=GOLD, mec=ORANGE, mew=1.6, zorder=8)

# ---- axes cosmetics ----
ax.set_xticks([1e-25, 1e-20, 1e-15, 1e-10, 1e-5, 1e-2, 1])
ax.set_xticklabels([r"$10^{-25}$", r"$10^{-20}$", r"$10^{-15}$", r"$10^{-10}$",
                    r"$10^{-5}$", r"$10^{-2}$", r"$1$"])
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.tick_params(colors=AXIS, labelsize=13, length=5, width=1.0)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("bottom", "left"):
    ax.spines[s].set_color("#3a3a48")
ax.set_xlabel(r"$T/T_{\rm res}$  (local Unruh / reservoir temperature ratio, log scale)",
              color=AXIS, fontsize=14.5, labelpad=10)
ax.set_ylabel(r"Maximum extraction efficiency  $\eta_{\max}$",
              color=AXIS, fontsize=14.5, labelpad=8)

# ---- title / subtitle ----
fig.text(0.05, 0.945, "When the Entropic-Gravity Bound Becomes Empirically Discriminating",
         color=WHITE, fontsize=21, fontweight="bold", ha="left", va="center")
fig.text(0.05, 0.892,
         r"$\eta \leq 1 - T/T_{\rm res}$   (Carnot)  —  same equation, ~25 orders of magnitude, only one regime where it bites",
         color=PURPSUB, fontsize=13.5, fontstyle="italic", ha="left", va="center")

# ---- annotations ----
ax.text(6e-25, 1.028, r"naive: $\eta = 1$  (vacuous)", color=GREYLBL,
        fontsize=12.5, fontstyle="italic", va="bottom")

ax.text(2e-13, 0.905, "BEC analog gravity\n(this paper)", color=PURPLE,
        fontsize=15.5, fontweight="bold", ha="left", va="center", linespacing=1.25)
ax.add_patch(FancyArrowPatch((0.028, 0.90), (r_bec*0.72, 1 - r_bec + 0.015),
        connectionstyle="arc3,rad=-0.28", color=PURPLE, lw=2.0,
        arrowstyle="-|>", mutation_scale=18, zorder=7))

ax.text(2e-13, 0.44, r"$\eta \leq 0.80$   $\rightarrow$   20% efficiency suppression",
        color=ORANGE, fontsize=15.5, fontweight="bold", fontstyle="italic",
        ha="left", va="center")
ax.add_patch(FancyArrowPatch((0.03, 0.42), (r_bec*0.82, 1 - r_bec - 0.02),
        connectionstyle="arc3,rad=0.30", color=ORANGE, lw=2.0,
        arrowstyle="-|>", mutation_scale=18, zorder=7))

# grey anchor labels
ax.text(1e-23, 0.64, "Saturn V\n(surface gravity)", color=GREYLBL, fontsize=12,
        ha="center", va="top", linespacing=1.3)
ax.text(1e-15, 0.64, "Hot-Jupiter\natmospheric escape", color=GREYLBL, fontsize=12,
        ha="center", va="top", linespacing=1.3)
ax.text(2e-9, 0.64, "Stellar wind /\nbinary inspiral", color=GREYLBL, fontsize=12,
        ha="center", va="top", linespacing=1.3)
ax.text(0.32, 0.115, r"trivial heat-engine limit  ($T = T_{\rm res}$):" + "\n"
        r"Carnot $\eta \rightarrow 0$", color=GREYLBL, fontsize=12,
        ha="right", va="bottom", linespacing=1.3)

for ext, dpi in (("svg", 100), ("png", 280)):
    fig.savefig(f"{OUT}/web_hero_track2_bound.{ext}", facecolor=BG, dpi=dpi)
    print(f"wrote {OUT}/web_hero_track2_bound.{ext}")
plt.close(fig)
