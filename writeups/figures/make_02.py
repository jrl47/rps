# Figures for writeup 02. Run from the repository root: python3 writeups/figures/make_02.py
# (needs matplotlib: pip install matplotlib). The numbers are from mixtures_and_masks_experiment.py, which is seeded, so
# rerunning it prints these exact values.
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
SURFACE, INK, INK_2, GRID, NEUTRAL = "#fcfcfb", "#0b0b0b", "#52514e", "#e1e0d9", "#c9c8c1"
BLUE, ORANGE = "#2a78d6", "#eb6834"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK_2,
                     "xtick.color": INK_2, "ytick.color": INK_2, "axes.facecolor": SURFACE, "figure.facecolor": SURFACE})

def style(ax, grid_axis = "both"):
    ax.grid(True, axis = grid_axis, color = GRID, linewidth = 0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"): ax.spines[side].set_visible(False)
    ax.tick_params(length = 0)

# 1. what the counter-bots faced each round (section 1 of the experiment): known / several but agreeing / disagreeing
HERDING = [("remain+change+constant", [("greedy", .872, .001, .127), ("far-sighted", .302, .598, .100)]),
           ("remain+if_won+historian", [("greedy", .456, .423, .122), ("far-sighted", .284, .616, .100)]),
           ("change+if_won+constant", [("greedy", .866, .001, .133), ("far-sighted", .419, .464, .117)]),
           ("change+constant+pattern_2", [("greedy", .691, .164, .145), ("far-sighted", .542, .330, .128)]),
           ("change+constant+remain_from_paper", [("greedy", .866, .008, .126), ("far-sighted", .301, .599, .100)]),
           ("if_won+three_cycle+remain_from_paper", [("greedy", .487, .389, .124), ("far-sighted", .306, .594, .101)])]
fig, ax = plt.subplots(figsize = (7, 4.6))
labels, y = [], 0
for mixture, rows in HERDING:
    for counter, known, agreeing, disagreeing in rows:
        left = 0
        for value, color in ((known, NEUTRAL), (agreeing, BLUE), (disagreeing, ORANGE)):
            ax.barh(y, value, left = left, color = color, height = 0.72, edgecolor = SURFACE, linewidth = 2)
            left += value
        labels.append((y, f"{mixture}   {counter}" if counter == "greedy" else counter))
        y -= 1
    y -= 0.6
ax.set_yticks([p for p, _ in labels])
ax.set_yticklabels([text for _, text in labels], fontsize = 8)
ax.set_xlim(0, 1)
ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
style(ax, "x")
ax.set_xlabel("share of rounds")
ax.set_title("What each counter-bot faced, round by round", loc = "left", color = INK, fontsize = 12)
handles = [matplotlib.patches.Patch(color = c, label = l) for c, l in
           ((NEUTRAL, "knew the strategy"), (BLUE, "several possible, agreeing"), (ORANGE, "several possible, disagreeing"))]
fig.legend(handles = handles, frameon = False, loc = "lower center", ncol = 3, fontsize = 8.5, labelcolor = INK_2)
fig.tight_layout(rect = (0, 0.05, 1, 1))
fig.savefig(os.path.join(HERE, "02-herding.png"), dpi = 200)

# 2. secret bits vs. damage from bots that happen to play pi (section 3A of the experiment)
BITS = [0, 1, 2, 4, 8, 16]
VS_PI = [-1.433, -0.775, -0.186, -0.221, 0.012, 0.006]
VS_SPRINKLED = [-0.800, -0.482, -0.168, -0.041, -0.004, -0.013]
fig, ax = plt.subplots(figsize = (7, 3.8))
ax.axhline(0, color = INK_2, linewidth = 0.8)
halving = [x / 10 for x in range(0, 161)]
ax.plot(halving, [VS_PI[0] / 2 ** b for b in halving], color = NEUTRAL, linewidth = 1.5, label = "vs pi_bot if each bit halved the risk")
for values, color, label in ((VS_PI, BLUE, "vs pi_bot"), (VS_SPRINKLED, ORANGE, "vs sprinkled_pi_bot")):
    ax.plot(BITS, values, color = color, linewidth = 2, marker = "o", markersize = 5, label = label)
    ax.annotate(label, (BITS[0], values[0]), xytext = (-8, 0), textcoords = "offset points", va = "center", ha = "right", color = INK_2, fontsize = 9)
style(ax)
ax.set_xticks(BITS)
ax.set_xlim(-5.6, 16.6)
ax.set_xlabel("bits spent on a secret start for the mask (drawn once per game)")
ax.set_ylabel("margin per 10 rounds")
ax.set_title("A few secret bits end accidental collisions", loc = "left", color = INK, fontsize = 12)
ax.legend(frameon = False, loc = "lower right", labelcolor = INK_2)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "02-secret-bits.png"), dpi = 200)
print("wrote", sorted(os.listdir(HERE)))
