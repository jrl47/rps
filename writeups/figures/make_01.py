# Figures for writeup 01. Run from the repository root: python3 writeups/figures/make_01.py
# (needs matplotlib: pip install matplotlib)
import math
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.getcwd())
import rps

HERE = os.path.dirname(os.path.abspath(__file__))
SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e1e0d9"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK_2,
                     "xtick.color": INK_2, "ytick.color": INK_2, "axes.facecolor": SURFACE, "figure.facecolor": SURFACE})

def style(ax):
    ax.grid(True, color = GRID, linewidth = 0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"): ax.spines[side].set_visible(False)
    ax.tick_params(length = 0)

# 1. what one draw of n options can buy in 10 rounds against the perfect counter-bot
ns = [2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 27, 32, 36, 48, 54, 64, 72, 81]
bits = [math.log2(n) for n in ns]
ceiling = 2 / (3 * math.log2(3) - 2)
series = [("0.726 × bits: the ceiling for any bot", [ceiling * b for b in bits], AQUA, None),
          ("best possible (Lopsided Bot's kind of plans)", [rps.best_split(n, 10)[0] / n for n in ns], ORANGE, "o"),
          ("spent on fully unpredictable rounds", [math.log(n, 3) for n in ns], BLUE, None)]
fig, ax = plt.subplots(figsize = (7, 4.2))
for label, ys, color, marker in series:
    ax.plot(bits, ys, color = color, linewidth = 2, marker = marker, markersize = 5, label = label)
    ax.annotate(label.split(":")[0].split(" (")[0], (bits[-1], ys[-1]), xytext = (6, 0), textcoords = "offset points",
                va = "center", color = INK_2, fontsize = 9)
style(ax)
ax.set_xlabel("bits of randomness drawn (log2 of the number of options)")
ax.set_ylabel("margin bought per 10 rounds")
ax.set_title("What one draw can buy against the perfect counter-bot", loc = "left", color = INK, fontsize = 12)
ax.legend(frameon = False, loc = "upper left", labelcolor = INK_2)
ax.set_xlim(0.8, 8.4)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "01-what-one-draw-buys.png"), dpi = 200)

# 2. protection against the perfect counter-bot vs robustness against predators that don't know how the bot works
# (numbers from section 4 of rationing_experiment.py, which is seeded, so rerunning it prints these exact values)
bots = [("burst_bot", -7.000, [-0.169, -0.405, -5.869]), ("jumpy_de_bruijn_bot", -7.000, [0.120, 0.255, -5.934]),
        ("lopsided_bot", -6.778, [-1.986, -5.150, -6.059]), ("masked_lopsided_bot", -6.778, [-0.071, -0.003, -0.006]),
        ("sprinkled_pi_bot", -7.000, [-0.060, 0.007, 0.009]), ("moody_predator_bot", -9.132, [3.759, -1.221, -1.392])]
offsets = {"burst_bot": (-8, 8), "jumpy_de_bruijn_bot": (-8, -16), "lopsided_bot": (8, -4), "masked_lopsided_bot": (8, 6),
           "sprinkled_pi_bot": (-8, -16), "moody_predator_bot": (8, -4)}
fig, ax = plt.subplots(figsize = (7, 4.2))
for name, counter, predators in bots:
    color = ORANGE if name == "masked_lopsided_bot" else BLUE
    ax.scatter([counter], [min(predators)], s = 64, color = color, edgecolors = SURFACE, linewidths = 2, zorder = 3)
    dx, dy = offsets[name]
    ax.annotate(name, (counter, min(predators)), xytext = (dx, dy), textcoords = "offset points", color = INK,
                fontsize = 9, ha = "right" if dx < 0 else "left")
style(ax)
ax.set_xlim(-10, -6)
ax.set_ylim(-7, 1)
ax.set_xlabel("margin per 10 rounds against its perfect counter-bot  (-10 = losing every round; better →)")
ax.set_ylabel("margin per 10 rounds against its\nworst cheap predator  (better →)")
ax.set_title("Protection vs. balance (one draw every 10 rounds)", loc = "left", color = INK, fontsize = 12)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "01-protection-vs-balance.png"), dpi = 200)
print("wrote", os.listdir(HERE))
