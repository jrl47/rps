# String Bots vs Predators
# How does a bot that just loops through a fixed string of moves (a poor man's randomness) fare against predators?
# At each length it compares two kinds of string:
#   de Bruijn: simple to describe (low kolmogorov complexity), but every run of `order` moves appears exactly once per loop
#   arbitrary: drawn at random once (high complexity), with no special structure
# Each number is the string bot's margin (rounds won minus rounds lost) in a game of NUM_ROUNDS rounds, averaged over
# both seats. The bots are all deterministic, so every result is exact; the arbitrary column averages NUM_ARBITRARY strings.
import random
from rps import NUM_ROUNDS, de_bruijn, string_bot, exact_game, favorite_bot, habit_bot, deja_vu_bot

PREDATORS = [favorite_bot, habit_bot, deja_vu_bot]
ORDERS = range(1, 9) # string lengths 3, 9, 27, ..., 6561
NUM_ARBITRARY = 10 # arbitrary strings per length
arbitrary = random.Random(20260929) # fixed seed, so the "arbitrary" strings are the same every run

def margin(moves, predator): # the string bot's margin against predator, averaged over both seats
    bot = string_bot(moves, "string_bot")
    as_p1 = exact_game(bot, predator)[0] # {margin: probability}
    as_p2 = exact_game(predator, bot)[0]
    return (sum(m * chance for m, chance in as_p1.items()) - sum(m * chance for m, chance in as_p2.items())) / 2

print(f"String bot's margin over {NUM_ROUNDS} rounds (negative means the predator wins)")
names = [p.__name__.replace("_bot", "") for p in PREDATORS]
print("LENGTH".ljust(8) + "DE BRUIJN".ljust(12 * len(PREDATORS)) + f"ARBITRARY (AVERAGE OF {NUM_ARBITRARY})")
print("".ljust(8) + "".join(f"vs {name}".ljust(12) for name in names) * 2)
for order in ORDERS:
    length = 3 ** order
    de_bruijn_margins = [margin(de_bruijn(order), p) for p in PREDATORS]
    strings = [[arbitrary.randint(0, 2) for _ in range(length)] for _ in range(NUM_ARBITRARY)]
    arbitrary_margins = [sum(margin(s, p) for s in strings) / NUM_ARBITRARY for p in PREDATORS]
    print(f"{length}".ljust(8) + "".join(f"{float(m):.0f}".ljust(12) for m in de_bruijn_margins + arbitrary_margins))
