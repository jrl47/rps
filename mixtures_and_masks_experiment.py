# Mixtures and Masks
# 1. Does a far-sighted counter-bot, which plans its own moves ahead, do better against mixture bots than a greedy one?
# 2. Can a mixture bot choose how its strategies disagree? (Variations on one strategy, rather than several strategies.)
# 3. How many bits does a mask's secret start need, against bots that happen to share the mask, and against a bot that
#    knows the whole scheme?
# "Margin bought" is how much better a bot does against its perfect counter-bot than losing every round.
import math
import random
import rps
from rps import (mixture_bot, mixture_counter_bot, lookahead_counter_bot, fixed_start, plan_bot, plan_counter_bot, best_plans,
                 exact_game, play_game, pi_digit, youll_remain_bot, youll_change_bot, youll_remain_if_won_else_change_bot,
                 historian_bot, constant_bot, three_cycle_bot, pattern_bot_2)

NUM_ROUNDS = rps.NUM_ROUNDS
NUM_GAMES = 10 # sampled games in each seat
random.seed(20260930)

def exact_bought(bot, counter, rounds): # margin bot buys per 10 rounds against counter, exactly, over a game of `rounds` rounds
    rps.NUM_ROUNDS = rounds
    as_p1 = exact_game(bot, counter)[0]; as_p2 = exact_game(counter, bot)[0]
    rps.NUM_ROUNDS = NUM_ROUNDS
    margin = (sum(m * chance for m, chance in as_p1.items()) - sum(m * chance for m, chance in as_p2.items())) / 2
    return float(10 + margin * 10 / rounds)

def sampled_margin(bot, rival, games = NUM_GAMES): # bot's average margin per 10 rounds against rival, over `games` games in each seat
    total = sum(play_game(bot, rival)[0] - play_game(rival, bot)[0] for _ in range(games))
    return total / (2 * games) / (rps.NUM_ROUNDS / 10)

print("1. GREEDY VS FAR-SIGHTED COUNTER-BOTS against mixtures of the original reactive bots (each starting with rock)")
print("   Margin the mixture buys per 10 rounds, exact over 30 rounds. The far-sighted counter-bot plans to the end of each")
print("   block, or 1 or 2 rounds into the next.")
POOL = {"remain": fixed_start(youll_remain_bot), "change": fixed_start(youll_change_bot), "if_won": fixed_start(youll_remain_if_won_else_change_bot),
        "historian": fixed_start(historian_bot), "constant": fixed_start(constant_bot), "three_cycle": fixed_start(three_cycle_bot),
        "pattern_2": fixed_start(pattern_bot_2), "remain_from_paper": fixed_start(youll_remain_bot, 1)}
MIXTURES = [("remain", "change", "if_won"), ("remain", "change", "constant"), ("remain", "if_won", "historian"), ("change", "if_won", "constant"),
            ("change", "constant", "pattern_2"), ("change", "constant", "remain_from_paper"), ("if_won", "three_cycle", "remain_from_paper")]
print("MIXTURE".ljust(38) + "GREEDY".ljust(10) + "TO BLOCK END".ljust(14) + "+1 ROUND".ljust(10) + "+2 ROUNDS")
for names in MIXTURES:
    mix = mixture_bot([POOL[n] for n in names], "mix")
    row = [exact_bought(mix, mixture_counter_bot(mix, "greedy"), 30)]
    row += [exact_bought(mix, lookahead_counter_bot(mix, "far-sighted", into_next_block = k), 30) for k in (0, 1, 2)]
    print("+".join(names).ljust(38) + "".join(f"{v:.4f}".ljust(v_width) for v, v_width in zip(row, (10, 14, 10, 10))))

print()
print("   What the counter-bots faced each round (sampled): how often they knew which strategy was active, how often several")
print("   were still possible but would all play the same move, and how often the possible strategies disagreed")
print("MIXTURE".ljust(38) + "COUNTER-BOT".ljust(13) + "KNOWN".ljust(8) + "SEVERAL, AGREEING".ljust(20) + "DISAGREEING")
rps.NUM_ROUNDS = 1000
for names in MIXTURES[1:]:
    mix = mixture_bot([POOL[n] for n in names], "mix")
    for label in ("greedy", "far-sighted"):
        log = []
        counter = mixture_counter_bot(mix, label, log = log) if label == "greedy" else lookahead_counter_bot(mix, label, log = log)
        for _ in range(4):
            play_game(mix, counter); play_game(counter, mix)
        known = sum(1 for chances in log if sum(chances) == 1) / len(log)
        agreeing = sum(1 for chances in log if sum(chances) > 1 and max(chances) == sum(chances)) / len(log)
        print(("+".join(names) if label == "greedy" else "").ljust(38) + label.ljust(13) + f"{known:.1%}".ljust(8) + f"{agreeing:.1%}".ljust(20) + f"{1 - known - agreeing:.1%}")
rps.NUM_ROUNDS = NUM_ROUNDS

print()
print("2. VARIATIONS ON A THEME: a mixture of different strategies (Moody Predator Bot) vs. one strategy with designed variations")
print("   (Deja Vu Bot varied by Lopsided Bot's plans). Margin per 10 rounds; against the counter-bot it's exact for the plan bots.")
three_plans = plan_bot(best_plans(3, 10, rest = 0), "lopsided_predator_3", base = rps.deja_vu_bot) # (3 plans: the same randomness as Moody Predator Bot)
RIVALS = [rps.favorite_bot, rps.habit_bot, rps.deja_vu_bot, rps.youll_remain_bot, rps.historian_bot]
print("BOT".ljust(24) + "BITS/10 ROUNDS".ljust(16) + "VS COUNTER-BOT".ljust(16) + "".join(f"VS {r.__name__.replace('_bot', '').upper()}".ljust(15) for r in RIVALS))
for bot in [rps.moody_predator_bot, three_plans, rps.lopsided_predator_bot]:
    if hasattr(bot, "plans"):
        bits = math.log2(len(bot.plans)); against_counter = exact_bought(bot, plan_counter_bot(bot.plans, "counter", base = bot.base), 10) - 10
    else:
        bits = math.log2(len(bot.strategies)); against_counter = sampled_margin(bot, mixture_counter_bot(bot, "counter"))
    print(bot.__name__.ljust(24) + f"{bits:.2f}".ljust(16) + f"{against_counter:+.3f}".ljust(16)
          + "".join(f"{sampled_margin(bot, r, 5):+.3f}".ljust(15) for r in RIVALS))
plans = best_plans(27, 10, rest = 0)
theme = fixed_start(youll_remain_bot)
def varied(plan): # You'll Remain Bot's move, varied by one plan (a strategy with no memory, so the far-sighted counter-bot can plan against it)
    return lambda p1hist, p2hist, whoAmI, rng: (theme(p1hist, p2hist, whoAmI, None) + plan[len(p1hist) % 10]) % 3
designed = mixture_bot([varied(plan) for plan in plans], "designed")
print(f"   (Designed variations can't be steered into agreeing: You'll Remain Bot varied by the same plans buys "
      f"{exact_bought(designed, mixture_counter_bot(designed, 'greedy'), 10):.4f} per 10 rounds against the greedy counter-bot")
print(f"   and {exact_bought(designed, lookahead_counter_bot(designed, 'far-sighted', into_next_block = 0), 10):.4f} against the far-sighted one.)")

print()
print("3. SECRET MASKS: Masked Lopsided Bot's plans, masked by pi, starting at a secret place (one of 2**bits, drawn once per game)")
print(f"   A. margin per 10 rounds against bots that happen to play pi (average of {4 * NUM_GAMES} games)")
PLANS = best_plans(27, 10)
for bits in (0, 1, 2, 4, 8, 16):
    bot = plan_bot(PLANS, "secret_mask", mask = pi_digit, mask_bits = bits)
    print(f"   {bits:2} secret bits: vs pi_bot {sampled_margin(bot, rps.pi_bot, 2 * NUM_GAMES):+.3f}   vs sprinkled_pi_bot {sampled_margin(bot, rps.sprinkled_pi_bot, 2 * NUM_GAMES):+.3f}")
print("   B. against the perfect counter-bot, which knows pi and the plans but not the start: margin bought in the first 10 rounds, exactly")
without = exact_bought(plan_bot(PLANS, "s", mask = pi_digit), plan_counter_bot(PLANS, "c", mask = pi_digit), 10)
for bits in range(1, 8):
    bought = exact_bought(plan_bot(PLANS, "s", mask = pi_digit, mask_bits = bits), plan_counter_bot(PLANS, "c", mask = pi_digit, mask_bits = bits), 10)
    print(f"   {bits} secret bits: {bought:.4f}, {bought - without:+.4f} more than with no secret (at most {0.726 * bits:.2f} over a whole game, however it's spent)")
print("   C. how many rounds it takes the counter-bot to pin down the start (5 sampled games each)")
rps.NUM_ROUNDS = 300
for bits in (4, 8, 12, 16):
    rounds = []
    for _ in range(5):
        log = []
        play_game(plan_bot(PLANS, "s", mask = pi_digit, mask_bits = bits), plan_counter_bot(PLANS, "c", mask = pi_digit, mask_bits = bits, log = log))
        rounds.append(next((i for i, starts_left in enumerate(log) if starts_left == 1), None))
    print(f"   {bits:2} secret bits ({2 ** bits} possible starts): {rounds}")
rps.NUM_ROUNDS = NUM_ROUNDS
