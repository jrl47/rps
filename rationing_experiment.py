# Rationed Randomness
# How much can a bot protect itself against the perfect counter-bot (which knows everything about it except its random
# draws) when its randomness is rationed? "Margin bought" is how much better the bot does than losing every round.
# Everything here is exact.
import math
import random
from collections import Counter
import rps
from rps import best_split, plan_counter_bot, mixture_counter_bot, exact_game, play_game, round_gain

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
def plan_bought(bot): # margin a plan bot buys per 10 rounds against its perfect counter-bot, exactly
    # (every block is the same, with fresh randomness, so one block tells the whole story)
    rps.NUM_ROUNDS = 10
    outcomes = exact_game(bot, plan_counter_bot(bot.plans, "counter", mask = bot.mask))[0]
    rps.NUM_ROUNDS = NUM_ROUNDS
    return 10 + float(sum(m * chance for m, chance in outcomes.items()))

NUM_ROUNDS = rps.NUM_ROUNDS
for bot in [rps.burst_bot, rps.jumpy_de_bruijn_bot, rps.lopsided_bot]:
    bought = plan_bought(bot)
    print(f"  {bot.__name__}: buys {bought:.4f} per 10 rounds ({bought / 10:.1%} of the way from losing every round to breaking even)")

NUM_GAMES = 10 # sampled games in each seat
random.seed(20260929)
def sampled_margin(bot, rival): # bot's average margin per 10 rounds against rival, over NUM_GAMES games in each seat
    total = sum(play_game(bot, rival)[0] - play_game(rival, bot)[0] for _ in range(NUM_GAMES))
    return total / (2 * NUM_GAMES) / (NUM_ROUNDS / 10)

print()
print("4. BALANCE: rationed bots against their perfect counter-bot and against three predators that don't know how they work")
print(f"Margin per 10 rounds (-10 means losing every round). Against the counter-bot it's exact for the plan bots; everything")
print(f"else is the average of {2 * NUM_GAMES} games of {NUM_ROUNDS} rounds.")
PREDATORS = [rps.favorite_bot, rps.habit_bot, rps.deja_vu_bot]
print("BOT".ljust(22) + "BITS PER 10 ROUNDS".ljust(20) + "VS COUNTER-BOT".ljust(16) + "".join(f"VS {p.__name__.replace('_bot', '').upper()}".ljust(14) for p in PREDATORS))
for bot in [rps.burst_bot, rps.jumpy_de_bruijn_bot, rps.lopsided_bot, rps.masked_lopsided_bot, rps.sprinkled_pi_bot, rps.moody_predator_bot]:
    if hasattr(bot, "plans"):
        bits = math.log2(len(bot.plans)); against_counter = plan_bought(bot) - 10
    else:
        bits = math.log2(len(bot.strategies)); against_counter = sampled_margin(bot, mixture_counter_bot(bot, "counter"))
    print(bot.__name__.ljust(22) + f"{bits:.2f}".ljust(20) + f"{against_counter:+.3f}".ljust(16) + "".join(f"{sampled_margin(bot, p):+.3f}".ljust(14) for p in PREDATORS))

print()
print("5. WHERE MOODY PREDATOR BOT'S RANDOMNESS GOES: each round, how the moves its possible strategies would play split up")
print("   (as its perfect counter-bot sees it), and the margin bought in rounds like that")
log = []
counter = mixture_counter_bot(rps.moody_predator_bot, "counter", log = log)
for _ in range(NUM_GAMES):
    play_game(rps.moody_predator_bot, counter); play_game(counter, rps.moody_predator_bot)
kinds = Counter(); bought = Counter()
for chances in log:
    kind = f"{sum(chances)} possible, moves split {sorted([c for c in chances if c], reverse = True)}"
    kinds[kind] += 1; bought[kind] += round_gain(chances)
for kind, count in kinds.most_common():
    print(f"  {count / len(log):6.1%} of rounds: {kind}".ljust(58) + f"buys {bought[kind] / count:.3f} per round")
print(f"  in all: {10 * sum(bought.values()) / len(log):.3f} per 10 rounds, from {math.log2(3):.2f} bits (a fully unpredictable round would buy 1)")

print()
print("6. A MASK IS A SHARED SECRET: Masked Lopsided Bot hides behind pi's digits, so bots that play pi can see through it")
print("   (take the mask off and Pi Bot is just 'always rock', which beats the plans' scissors). Masked with sqrt(2)'s digits instead:")
def ternary_sqrt2(n): # the first n digits of sqrt(2) in base 3 (1.10201122122... in base 3)
    root = math.isqrt(2 * 3 ** (2 * (n - 1)))
    digits = []
    for _ in range(n):
        root, digit = divmod(root, 3)
        digits.append(digit)
    return digits[::-1]
SQRT2_DIGITS = ternary_sqrt2(NUM_ROUNDS)
sqrt2_masked_bot = rps.plan_bot(rps.best_plans(27, 10), "sqrt2_masked_lopsided_bot", mask = lambda t: SQRT2_DIGITS[t])
RIVALS = [rps.pi_bot, rps.sprinkled_pi_bot] + PREDATORS
print("BOT".ljust(28) + "".join(f"VS {r.__name__.replace('_bot', '').upper()}".ljust(18) for r in RIVALS))
for bot in [rps.masked_lopsided_bot, sqrt2_masked_bot]:
    print(bot.__name__.ljust(28) + "".join(f"{sampled_margin(bot, r):+.3f}".ljust(18) for r in RIVALS))
