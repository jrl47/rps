# String Bots: Predators, Random Starts, and the Perfect Counter-Bot
# How does a bot that just loops through a fixed string of moves (a poor man's randomness) fare?
# At each length it compares two kinds of string:
#   de Bruijn: simple to describe (low kolmogorov complexity), but every run of `order` moves appears exactly once per loop
#   arbitrary: drawn at random once (high complexity), with no special structure
# All the bots here are deterministic apart from a random start, so every result is exact; the arbitrary column
# averages NUM_ARBITRARY strings.
import itertools
import math
import random
import rps
from rps import de_bruijn, string_bot, string_counter_bot, exact_game, favorite_bot, habit_bot, deja_vu_bot, overdue_bot, pi_bot

PREDATORS = [favorite_bot, habit_bot, deja_vu_bot, overdue_bot]
ORDERS = range(1, 9) # string lengths 3, 9, 27, ..., 6561
NUM_ARBITRARY = 10 # arbitrary strings per length
arbitrary = random.Random(20260929) # fixed seed, so the "arbitrary" strings are the same every run
ARBITRARY_STRINGS = {order: [[arbitrary.randint(0, 2) for _ in range(3 ** order)] for _ in range(NUM_ARBITRARY)] for order in ORDERS}

def margin(bot, rival): # bot's expected margin (rounds won minus rounds lost) against rival, averaged over both seats
    as_p1 = exact_game(bot, rival)[0] # {p1's margin: probability}
    as_p2 = exact_game(rival, bot)[0]
    return float(sum(m * chance for m, chance in as_p1.items()) - sum(m * chance for m, chance in as_p2.items())) / 2

def rounds_to_figure_out(moves): # after this many moves, the string bot's moves so far always show where in the string it is
    doubled = moves * 2
    rotations = [tuple(doubled[s:s + len(moves)]) for s in range(len(moves))]
    for n in range(1, len(moves) + 1):
        seen = {} # first n moves -> the rotation they came from
        if all(seen.setdefault(tuple(doubled[s:s + n]), rotations[s]) == rotations[s] for s in range(len(moves))):
            return n
    return len(moves)

def margin_bought(moves): # how much margin a random start buys a string bot against its perfect counter-bot
    # (with a fixed start the counter-bot wins every round, so the margin would be -rounds; once the counter-bot has
    # figured out where the string bot is it wins every round, so any game at least that long gives the same answer)
    rounds = rounds_to_figure_out(moves) + 1
    rps.NUM_ROUNDS = rounds
    bought = rounds + margin(string_bot(moves, "string_bot", random_start = True), string_counter_bot(moves, "counter_bot", random_start = True))
    rps.NUM_ROUNDS = NUM_ROUNDS
    return bought

NUM_ROUNDS = rps.NUM_ROUNDS
names = [p.__name__.replace("_bot", "") for p in PREDATORS]

print(f"1. STRING BOTS VS PREDATORS: the string bot's margin over {NUM_ROUNDS} rounds (negative means the predator wins)")
print("LENGTH".ljust(8) + "DE BRUIJN".ljust(12 * len(PREDATORS)) + f"ARBITRARY (AVERAGE OF {NUM_ARBITRARY})")
print("".ljust(8) + "".join(f"vs {name}".ljust(12) for name in names) * 2)
for order in ORDERS:
    de_bruijn_margins = [margin(string_bot(de_bruijn(order), "string_bot"), p) for p in PREDATORS]
    arbitrary_margins = [sum(margin(string_bot(s, "string_bot"), p) for s in ARBITRARY_STRINGS[order]) / NUM_ARBITRARY for p in PREDATORS]
    print(f"{3 ** order}".ljust(8) + "".join(f"{m:.0f}".ljust(12) for m in de_bruijn_margins + arbitrary_margins))
print("pi bot (never loops): " + ", ".join(f"vs {name} {margin(pi_bot, p):.0f}" for name, p in zip(names, PREDATORS)))

print()
print("2. RANDOM START VS THE PERFECT COUNTER-BOT (it knows the string, and that the start is random)")
print("A fixed start loses every round; this is the margin a random start buys back. log2(length) bits of randomness")
print("could make log3(length) rounds completely unpredictable, each worth 1.")
print("LENGTH".ljust(8) + "BITS".ljust(8) + "log3(LENGTH)".ljust(14) + "DE BRUIJN".ljust(11) + f"ARBITRARY (AVERAGE OF {NUM_ARBITRARY})")
for order in range(1, 8):
    length = 3 ** order
    de_bruijn_bought = margin_bought(de_bruijn(order))
    arbitrary_bought = sum(margin_bought(s) for s in ARBITRARY_STRINGS[order]) / NUM_ARBITRARY
    print(f"{length}".ljust(8) + f"{math.log2(length):.2f}".ljust(8) + f"{order}".ljust(14) + f"{de_bruijn_bought:.3f}".ljust(11) + f"{arbitrary_bought:.3f}")

# Rotating a string, or relabeling its moves rock -> paper -> scissors -> rock, doesn't change the margin a random start
# buys, so it's enough to try one string from each such family.
print()
print("3. THE BEST STRING OF EACH LENGTH AGAINST THE PERFECT COUNTER-BOT (checking every string)")
for length in [3, 6, 9]:
    families = {min(tuple((move + shift) % 3 for move in s[r:] + s[:r]) for r in range(length) for shift in range(3))
                for s in itertools.product(range(3), repeat = length)}
    best = max(families, key = lambda s: margin_bought(list(s)))
    print(f"length {length}: best buys {margin_bought(list(best)):.4f} (log3({length}) = {math.log(length, 3):.4f}): "
          + "".join("RPS"[move] for move in best))
