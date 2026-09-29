# Rationed Randomness
# How much can a bot protect itself against the perfect counter-bot (which knows everything about it except its random
# draws) when its randomness is rationed? "Margin bought" is how much better the bot does than losing every round.
# Everything here is exact.
import math
import rps
from rps import best_split, plan_counter_bot, exact_game, round_gain

def entropy(counts): # bits of uncertainty in a round where the next move is rock, paper or scissors in these proportions
    n = sum(counts)
    return -sum(c / n * math.log2(c / n) for c in counts if c)

print("1. ONE ROUND: margin bought per bit of the counter-bot's uncertainty about the bot's next move")
for label, counts in [("fully unpredictable (1/3 each)", (1, 1, 1)), ("coin flip between two moves (1/2 each)", (1, 1, 0)),
                      ("lopsided (2/3 rock, 1/3 scissors)", (2, 0, 1))]:
    print(f"  {label}: buys {round_gain(counts):.3f} for {entropy(counts):.3f} bits = {round_gain(counts) / entropy(counts):.3f} per bit")
N = 600
best = max(((round_gain(c) / entropy(c), c) for c in ((a, b, N - a - b) for a in range(N + 1) for b in range(N + 1 - a)) if max(c) < N))
print(f"  the best of every split (in steps of 1/{N}): {best[0]:.4f} per bit, at {tuple(round(x / N, 3) for x in best[1])} (rock, paper, scissors)")
print(f"  (that's lopsided exactly: (2/3) / (log2(3) - 2/3) = {(2 / 3) / (math.log2(3) - 2 / 3):.4f})")
CEILING = best[0]
print("  The counter-bot only learns about a bot's draws through the moves it sees, so each bit can only be used up once:")
print(f"  over a whole game, margin bought <= {CEILING:.3f} * bits drawn, however the bot spreads them out.")

print()
print("2. ONE DRAW OF n OPTIONS, SPREAD OVER 10 ROUNDS: the most margin it can buy (by checking every way to split the options)")
print("OPTIONS".ljust(9) + "BITS".ljust(7) + "FULLY UNPREDICTABLE ROUNDS".ljust(28) + "BEST".ljust(9) + f"CEILING ({CEILING:.3f} * BITS)")
for n in [2, 3, 4, 6, 8, 9, 12, 18, 27, 36, 54, 81]:
    print(f"{n}".ljust(9) + f"{math.log2(n):.2f}".ljust(7) + f"{math.log(n, 3):.3f}".ljust(28) + f"{best_split(n, 10)[0] / n:.4f}".ljust(9) + f"{CEILING * math.log2(n):.4f}")
print("(fully unpredictable rounds: log3(n), what the draw buys if it's spent making whole rounds completely unpredictable)")
print("(making all 10 rounds completely unpredictable takes 3**10 = 59049 options, 15.85 bits)")

print()
print("3. RATIONED BOTS VS THE PERFECT COUNTER-BOT: one draw of 27 options (4.75 bits) every 10 rounds")
rps.NUM_ROUNDS = 10 # every block is the same, with fresh randomness, so one block tells the whole story
for bot in [rps.burst_bot, rps.jumpy_de_bruijn_bot, rps.lopsided_bot]:
    outcomes = exact_game(bot, plan_counter_bot(bot.plans, "counter"))[0]
    bought = 10 + float(sum(m * chance for m, chance in outcomes.items()))
    print(f"  {bot.__name__}: buys {bought:.4f} per 10 rounds ({bought / 10:.1%} of the way from losing every round to breaking even)")
