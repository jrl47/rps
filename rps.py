import functools
import math
import random
from fractions import Fraction
numbers_to_moves = {0: "rock", 1:"paper", 2:"scissors"}

# 1 Random Bot
# plays random moves
def random_bot(p1hist, p2hist, whoAmI, rng): # no hist usage
    return rng.randint(0,2)

# 2 Constant Bot
# randomly picks a move to play forever
def constant_bot(p1hist, p2hist, whoAmI, rng): # no hist usage; de se & random just for random first move as root of pattern
    if not p1hist:
        return rng.randint(0,2)
    return(p1hist[0] if whoAmI == 1 else p2hist[0])

# 3 3-Cycle Bot
# plays a random 3-permutation aka 3-cycle; in this case, rock, paper, scissors (where which move comes first is random)
def three_cycle_bot(p1hist, p2hist, whoAmI, rng): # only uses hist length; de se & random just for random first move as root of pattern
    if not p1hist:
        return rng.randint(0,2)
    return((p1hist[0] + len(p1hist)) % 3 if whoAmI == 1 else (p2hist[0] + len(p1hist)) % 3)

# 4 Pattern Bot 1
# plays rock, rock, rock, paper, paper, rock
def pattern_bot_1(p1hist, p2hist, whoAmI, rng): # no hist usage; de se & random just for random first move as root of pattern
    if not p1hist:
        return rng.randint(0,2)
    base = p1hist[0] if whoAmI == 1 else p2hist[0]
    match len(p1hist) % 6:
        case 0: return (base) % 3
        case 1: return (base) % 3
        case 2: return (base) % 3
        case 3: return (base + 1) % 3
        case 4: return (base + 1) % 3
        case 5: return (base) % 3

# 5 Pattern Bot 2
# plays scissors, rock, rock, paper, paper, rock 200110 = 011221
def pattern_bot_2(p1hist, p2hist, whoAmI, rng): # no hist usage; de se & random just for random first move as root of pattern
    if not p1hist:
        return rng.randint(0,2)
    base = p1hist[0] if whoAmI == 1 else p2hist[0]
    match len(p1hist) % 6:
        case 0: return (base) % 3
        case 1: return (base + 1) % 3
        case 2: return (base + 1) % 3
        case 3: return (base + 2) % 3
        case 4: return (base + 2) % 3
        case 5: return (base + 1) % 3

# 6 Random Throwback Bot
# after a random move, chooses a random player and a random past round and plays the historical move
def random_throwback_bot(p1hist, p2hist, whoAmI, rng): # 100% hist usage
    if not p1hist:
        return rng.randint(0,2)
    if (rng.randint(0,1) == 0):
        return rng.choice(p1hist)
    else:
        return rng.choice(p2hist)

# 7 Historian Bot
# after a random move, plays p1's first move, then p2's first move, then p1's second move, then p2's second move...
def historian_bot(p1hist, p2hist, whoAmI, rng): # 100% hist usage; random just for first move
    if not p1hist:
        return rng.randint(0,2)
    turn = len(p1hist) - 1 # minus one to offset the very first turn where a random move is played
    if turn % 2 == 0:
        return p1hist[turn // 2]
    else:
        return p2hist[turn // 2]

# 8 Bet You'll Stay The Same Bot
# (1 random, then) plays the move that will beat the move rival just played
def youll_remain_bot(p1hist, p2hist, whoAmI, rng): # most-recent-1 hist usage; de se knows which player it is
    if not p1hist:
        return rng.randint(0,2)
    prev_rival_move = p2hist[len(p1hist)-1] if whoAmI == 1 else p1hist[len(p1hist)-1]
    return (prev_rival_move + 1) % 3

# 9 Bet You'll Change Bot
# (1 random, then) plays the move that could lose to the move rival just played (and so cant lose if you change)
def youll_change_bot(p1hist, p2hist, whoAmI, rng): # most-recent-1 hist usage; de se knows which player it is
    if not p1hist:
        return rng.randint(0,2)
    prev_rival_move = p2hist[len(p1hist)-1] if whoAmI == 1 else p1hist[len(p1hist)-1]
    return (prev_rival_move - 1) % 3

# 10 Bet You'll Stay The Same If You Won Otherwise Bet You'll Change Bot
# (1 random, then) plays the move that will beat the move rival just played if rival just won,
# otherwise (draw or rival lost) plays the move that could lose to the move rival just played
def youll_remain_if_won_else_change_bot(p1hist, p2hist, whoAmI, rng): # most-recent-1 hist usage; de se knows which player it is
    if not p1hist:
        return rng.randint(0,2)
    prev_rival_move = p2hist[len(p1hist)-1] if whoAmI == 1 else p1hist[len(p1hist)-1]
    prev_self_move = p1hist[len(p1hist)-1] if whoAmI == 1 else p2hist[len(p1hist)-1]
    if (prev_rival_move - prev_self_move) % 3 == 1: # if rival won; cf. do_round code
        return (prev_rival_move + 1) % 3 # same as youll_remain bot
    else:
        return (prev_rival_move - 1) % 3 # same as youll_change

# String Bots
# loop through a fixed string of moves forever: a sort of poor man's randomness, with no rng at all
def string_bot(moves, name): # only uses hist length
    def bot(p1hist, p2hist, whoAmI, rng):
        return moves[len(p1hist) % len(moves)]
    bot.__name__ = name
    return bot

def de_bruijn(order): # a loop of 3**order moves in which every run of `order` moves appears exactly once
    moves = [0] * order # (greedy construction: start with all rocks, then keep adding the highest move that makes a new run)
    seen = {tuple(moves)}
    while True:
        for move in (2, 1, 0):
            run = tuple(moves[len(moves) - order + 1:] + [move])
            if run not in seen:
                seen.add(run); moves.append(move)
                break
        else:
            break
    return moves[:3 ** order]

# 11 De Bruijn Bot
# loops through an order-3 de Bruijn string: 27 moves in which every run of 3 moves appears exactly once
# simple to describe (low kolmogorov complexity), but gives a predictor that looks back 2 moves nothing to go on
de_bruijn_bot = string_bot(de_bruijn(3), "de_bruijn_bot")

# 12 Battery 12 Bot
# loops through an arbitrary 12-move string (drawn at random once, when the bot was written)
battery_12_bot = string_bot([2, 2, 2, 1, 1, 0, 1, 1, 2, 1, 0, 0], "battery_12_bot")

# Memory
# A bot decorated with @with_memory gets a fifth argument, memory: a dict that lasts for one game (one per seat).
# It's only for keeping track of things worked out from the history so the bot doesn't redo them every move,
# so the bot still behaves as a function of the history.
def with_memory(bot):
    memories = {}
    @functools.wraps(bot)
    def bot_with_memory(p1hist, p2hist, whoAmI, rng):
        if not p1hist or whoAmI not in memories: memories[whoAmI] = {} # new game
        return bot(p1hist, p2hist, whoAmI, rng, memories[whoAmI])
    return bot_with_memory

# 13 Favorite Bot
# bets the rival will play their most common move so far, and plays what beats it (ties go to rock, so it opens with paper)
@with_memory
def favorite_bot(p1hist, p2hist, whoAmI, rng, memory): # 100% hist usage (rival's); de se knows which player it is
    rival_hist = p2hist if whoAmI == 1 else p1hist
    counts = memory.setdefault("counts", [0, 0, 0])
    for move in rival_hist[sum(counts):]:
        counts[move] += 1
    favorite = counts.index(max(counts))
    return (favorite + 1) % 3

# 14 Habit Bot
# bets the rival will play whatever they've most often played after their last two moves, and plays what beats it
# (if those two moves haven't come up before, it falls back on Favorite Bot's bet)
@with_memory
def habit_bot(p1hist, p2hist, whoAmI, rng, memory): # 100% hist usage (rival's); de se knows which player it is
    rival_hist = p2hist if whoAmI == 1 else p1hist
    counts = memory.setdefault("counts", [0, 0, 0])
    after = memory.setdefault("after", {}) # the rival's two moves -> counts of what they played next
    for t in range(sum(counts), len(rival_hist)):
        counts[rival_hist[t]] += 1
        if t >= 2:
            after.setdefault((rival_hist[t - 2], rival_hist[t - 1]), [0, 0, 0])[rival_hist[t]] += 1
    guess_counts = after.get(tuple(rival_hist[-2:]), counts)
    guess = guess_counts.index(max(guess_counts))
    return (guess + 1) % 3

# 15 Deja Vu Bot
# finds the last time the rival's most recent moves (up to 20 of them) came up before, bets they'll do what they did next,
# and plays what beats it (rock if it has nothing to go on); catches any string bot once its string loops
@with_memory
def deja_vu_bot(p1hist, p2hist, whoAmI, rng, memory): # 100% hist usage (rival's); de se knows which player it is
    rival_hist = p2hist if whoAmI == 1 else p1hist
    seen = memory.get("seen", "") # the rival's moves as a string, like "0120"
    after = memory.setdefault("after", {}) # a run of the rival's moves -> where the move after its latest appearance is in seen
    for move in rival_hist[len(seen):]:
        for length in range(1, min(20, len(seen)) + 1):
            after[seen[-length:]] = len(seen)
        seen += str(move)
    memory["seen"] = seen
    guess = None
    for length in range(1, min(20, len(seen)) + 1): # (if the last `length` moves never came up before, longer runs didn't either)
        position = after.get(seen[-length:])
        if position is None: break
        guess = int(seen[position])
    if guess is None: return 0
    return (guess + 1) % 3

# Engine
NUM_ROUNDS = 5000 # 10000
MAX_BRANCHES = 4096 # a game is computed exactly if its random draws have at most this many possible sequences (4096 = 12 bits)
NUM_SAMPLES = 200 # otherwise it's estimated from this many sampled games

# Randomness
# Bots get all their randomness from rng, never from the random module directly. Every draw goes onto the game's Tape,
# so the engine can either sample a game, or replay it once for every possible sequence of draws and get exact results.
# rng also counts the bits of randomness each bot uses.

class TooManyBranches(Exception):
    pass

class Tape:
    def __init__(self, script=None):
        self.script = script # draws to replay when enumerating (any draw past the end is 0); None means sample
        self.draws = [] # (value, n) for each draw made this game
        self.branches = 1 # when enumerating, this path's probability is 1 / branches
    def draw(self, n):
        if self.script is None:
            value = random.randrange(n)
        else:
            value = self.script[len(self.draws)] if len(self.draws) < len(self.script) else 0
            self.branches *= n
            if self.branches > MAX_BRANCHES: raise TooManyBranches
        self.draws.append((value, n))
        return value

class Rng:
    def __init__(self, tape):
        self.tape = tape
        self.bits = 0.0
    def randint(self, a, b): # like random.randint: a <= result <= b
        self.bits += math.log2(b - a + 1)
        return a + self.tape.draw(b - a + 1)
    def choice(self, seq): # like random.choice
        self.bits += math.log2(len(seq))
        return seq[self.tape.draw(len(seq))]

def points(margin): # 1 for a win, 1/2 for a tie, 0 for a loss; you have to win by more than 1 round
    if margin > 1: return 1
    if margin < -1: return 0
    return Fraction(1, 2)

def play_game(p1, p2, tape=None): # returns p1's margin (rounds won minus rounds lost) and the bits of randomness each bot used
    if tape is None: tape = Tape()
    rng1 = Rng(tape); rng2 = Rng(tape)
    p1hist = []; p2hist = []
    margin = 0
    for _ in range(NUM_ROUNDS):
        p1_move = p1(p1hist, p2hist, 1, rng1); p2_move = p2(p1hist, p2hist, 2, rng2)
        outcome = (p1_move - p2_move) % 3
        p1hist.append(p1_move)
        p2hist.append(p2_move)
        if outcome == 1: margin += 1
        elif outcome == 2: margin -= 1
    # print(f"{p1.__name__} vs {p2.__name__}: p1 margin {margin}")
    # print(p1hist)
    # print(p2hist)
    return margin, rng1.bits, rng2.bits

# play_game(random_bot, constant_bot)
# play_game(random_bot, historian_bot)
# play_game(random_throwback_bot, constant_bot) # VERY INTERESTING
# play_game(random_throwback_bot, random_throwback_bot) # high variance at 100000 rounds
# play_game(historian_bot, pattern_bot_1) # contrast a
# play_game(historian_bot, pattern_bot_2) # contrast a
# play_game(random_throwback_bot, pattern_bot_1) # contrast b
# play_game(random_throwback_bot, pattern_bot_2) # contrast b
# play_game(historian_bot, three_cycle_bot) # these results are striking but I checked that three_cycle_bot is implemented correctly and the match works out logically
  # example match:
  # [1, 1, 2, 1, 0, 2, 1, 1, 2, 0, 0, 2, 1, 1, 2, 1, 0, 2, 1, 0, 2, 0, 0, 2, 1, 1, 2, 1, 0, 2]
  # [2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1]
  # big win for historian bot after it fails to gain any traction against the two pattern bots (although has different draw rates for each of them)
# play_game(youll_remain_bot, constant_bot) # good sanity check
# play_game(youll_change_bot, constant_bot) # lmao
# play_game(youll_remain_bot, youll_change_bot) # p1 wins 33% of matches (if it wins round 1 it wins every round), p2 66% of matches (draw/p2-win alternation); there are two equilibria that might happen of different rarity
# play_game(youll_remain_if_won_else_change_bot, youll_remain_bot)

# Exact & Sampled Games
# A game's result is the probability of each margin p1 can end up with, which is enough to score a match either way (below).

def exact_game(p1, p2): # plays every possible sequence of draws once: {p1's margin: probability}, and each bot's expected bits
    outcomes = {}
    p1_bits = p2_bits = 0
    script = []
    while True: # (each path has probability >= 1 / MAX_BRANCHES, so there are at most MAX_BRANCHES paths)
        tape = Tape(script)
        random_state = random.getstate()
        margin, bits_1, bits_2 = play_game(p1, p2, tape)
        if random.getstate() != random_state: # a bot used the random module, so this wouldn't really be exact
            raise RuntimeError(f"{p1.__name__} or {p2.__name__} uses the random module; bots must get randomness from rng")
        chance = Fraction(1, tape.branches)
        outcomes[margin] = outcomes.get(margin, 0) + chance
        p1_bits += float(chance) * bits_1; p2_bits += float(chance) * bits_2
        # next sequence of draws, like an odometer: bump the last draw that isn't at its max, and drop everything after it
        draws = tape.draws
        while draws and draws[-1][0] == draws[-1][1] - 1:
            draws.pop()
        if not draws: break
        script = [value for value, n in draws[:-1]] + [draws[-1][0] + 1]
    return outcomes, p1_bits, p2_bits, True

def sampled_game(p1, p2): # same as exact_game, but estimated from NUM_SAMPLES sampled games
    outcomes = {}
    p1_bits = p2_bits = 0
    for _ in range(NUM_SAMPLES):
        margin, bits_1, bits_2 = play_game(p1, p2)
        outcomes[margin] = outcomes.get(margin, 0) + 1 / NUM_SAMPLES
        p1_bits += bits_1 / NUM_SAMPLES; p2_bits += bits_2 / NUM_SAMPLES
    return outcomes, p1_bits, p2_bits, False

def expected_game(p1, p2):
    try:
        return exact_game(p1, p2)
    except TooManyBranches:
        return sampled_game(p1, p2)

# Match Scoring
# Every match is two games with the seats swapped. There are two ways to score it:
# PER-GAME: each game is worth half a point on its own
# AGGREGATE: add up the margins from both games and score the total like one long game
# Either way the result is exact if both games are, and otherwise comes with a standard error.

def per_game_points(outcomes, exact): # p1's expected points from one game, and the standard error
    mean = sum(chance * points(margin) for margin, chance in outcomes.items())
    if exact: return mean, 0
    variance = sum(chance * (points(margin) - mean) ** 2 for margin, chance in outcomes.items())
    return mean, math.sqrt(variance / max(NUM_SAMPLES - 1, 1))

def aggregate_points(outcomes_1, exact_1, outcomes_2, exact_2): # a's expected points with both games' margins added up, and the standard error
    # (outcomes_1 are a's margins as p1 and outcomes_2 are b's margins as p1, so a's total margin is margin_1 - margin_2)
    mean = 0
    given_1 = {} # a's expected points given its margin in game 1
    given_2 = {} # a's expected points given b's margin in game 2
    for margin_1, chance_1 in outcomes_1.items():
        for margin_2, chance_2 in outcomes_2.items():
            p = points(margin_1 - margin_2)
            mean += chance_1 * chance_2 * p
            given_1[margin_1] = given_1.get(margin_1, 0) + chance_2 * p
            given_2[margin_2] = given_2.get(margin_2, 0) + chance_1 * p
    variance = 0 # (each sampled game contributes how much the result varies with its margin)
    if not exact_1: variance += sum(chance * (given_1[m] - mean) ** 2 for m, chance in outcomes_1.items()) / max(NUM_SAMPLES - 1, 1)
    if not exact_2: variance += sum(chance * (given_2[m] - mean) ** 2 for m, chance in outcomes_2.items()) / max(NUM_SAMPLES - 1, 1)
    return mean, math.sqrt(variance)

# Round Robin Tournament Engine

SCORINGS = ["PER-GAME", "AGGREGATE"]

def round_robin(competitors):
    # returns, for each scoring, a table of the row bot's expected points vs the column bot (0 to 1) and a table of
    # standard errors, a table of which matches were sampled rather than exact, and each bot's average bits of randomness per game
    n = len(competitors)
    tables = {scoring: [[0] * n for _ in range(n)] for scoring in SCORINGS}
    errors = {scoring: [[0] * n for _ in range(n)] for scoring in SCORINGS}
    sampled = [[False] * n for _ in range(n)] # whether either game of the match was sampled
    bits = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            a = competitors[i]; b = competitors[j]
            outcomes_1, a_bits_1, b_bits_1, exact_1 = expected_game(a, b) # a is p1
            outcomes_2, b_bits_2, a_bits_2, exact_2 = expected_game(b, a) # b is p1
            a_points_1, error_1 = per_game_points(outcomes_1, exact_1)
            b_points_2, error_2 = per_game_points(outcomes_2, exact_2)
            results = {"PER-GAME": ((a_points_1 + (1 - b_points_2)) / 2, math.sqrt(error_1 ** 2 + error_2 ** 2) / 2),
                       "AGGREGATE": aggregate_points(outcomes_1, exact_1, outcomes_2, exact_2)}
            for scoring, (a_points, error) in results.items():
                tables[scoring][i][j] = clamp(a_points); tables[scoring][j][i] = clamp(1 - a_points)
                errors[scoring][i][j] = errors[scoring][j][i] = error
            sampled[i][j] = sampled[j][i] = not (exact_1 and exact_2)
            bits[i] += a_bits_1 + a_bits_2; bits[j] += b_bits_1 + b_bits_2
    bits_per_game = [b / (2 * (n - 1)) for b in bits]
    return tables, errors, sampled, bits_per_game

def clamp(points): # (keeps float rounding in sampled results from showing up as -0.000 or 1.000...02)
    return min(max(float(points), 0.0), 1.0)

def score_text(score, error, sampled):
    return f"{score:.4f} ± {error:.4f}" if sampled else f"{score:.4f}"


if __name__ == "__main__":
    print(f"NUM_ROUNDS: {NUM_ROUNDS}")
    print(f"MAX_BRANCHES: {MAX_BRANCHES}, NUM_SAMPLES: {NUM_SAMPLES}")
    # tournament_competitors = [random_bot, constant_bot, random_throwback_bot, historian_bot, pattern_bot_1, pattern_bot_2, youll_remain_bot, youll_change_bot, three_cycle_bot]
    tournament_competitors = [random_bot, constant_bot, three_cycle_bot, pattern_bot_1, pattern_bot_2, random_throwback_bot, historian_bot, youll_remain_bot, youll_change_bot, youll_remain_if_won_else_change_bot,
                              de_bruijn_bot, battery_12_bot, favorite_bot, habit_bot, deja_vu_bot]
    competitor_names = list(map(lambda x: x.__name__, tournament_competitors))
    print("COMPETITORS:")
    for number, name in enumerate(competitor_names, 1):
        print(f"  {number}. {name}")
    tables, errors, sampled, bits_per_game = round_robin(tournament_competitors)
    print("~~ Tournament Complete ~~")
    n = len(tournament_competitors)
    scores = {s: [sum(row) for row in tables[s]] for s in SCORINGS}
    score_errors = {s: [math.sqrt(sum(e ** 2 for e in row)) for row in errors[s]] for s in SCORINGS}
    ranks = {}
    for s in SCORINGS:
        ranks[s] = [0] * n
        for rank, i in enumerate(sorted(range(n), key = lambda i: scores[s][i], reverse = True), 1): # sort by score greatest to least
            ranks[s][i] = rank
    width = max(map(len, competitor_names)) + 2
    print("RANK".ljust(6) + "BOT".ljust(width) + "PER-GAME SCORE".ljust(22) + "AGGREGATE SCORE (RANK)".ljust(28) + "BITS OF RANDOMNESS PER GAME")
    for i in sorted(range(n), key = lambda i: ranks["PER-GAME"][i]):
        print(f"{ranks['PER-GAME'][i]}".ljust(6) + competitor_names[i].ljust(width)
              + score_text(scores["PER-GAME"][i], score_errors["PER-GAME"][i], any(sampled[i])).ljust(22)
              + f"{score_text(scores['AGGREGATE'][i], score_errors['AGGREGATE'][i], any(sampled[i]))} ({ranks['AGGREGATE'][i]})".ljust(28)
              + f"{bits_per_game[i]:.2f}")
    print("MATCHUPS THE TWO SCORINGS DISAGREE ON (row bot's points)")
    for i in range(n):
        for j in range(i + 1, n):
            difference = abs(tables["PER-GAME"][i][j] - tables["AGGREGATE"][i][j])
            if difference > 1e-9 + 2 * (errors["PER-GAME"][i][j] + errors["AGGREGATE"][i][j]):
                print(f"  {competitor_names[i]} vs {competitor_names[j]}: PER-GAME {tables['PER-GAME'][i][j]:.3f}, AGGREGATE {tables['AGGREGATE'][i][j]:.3f}")
    for s in SCORINGS:
        print(f"WIN TABLE, {s} SCORING (row bot's expected points vs column bot; ~ means sampled, otherwise exact)")
        print("    " + "".join(f"{j + 1}".ljust(8) for j in range(n)))
        for i in range(n):
            cells = ["--" if i == j else ("~" if sampled[i][j] else "") + f"{tables[s][i][j]:.3f}" for j in range(n)]
            print(f"{i + 1}".ljust(4) + "".join(cell.ljust(8) for cell in cells))

# Botdex
#1 Random Bot 20230120
#2 Constant Bot 20230121
#3 3-Cycle Bot 20230121
#4 Pattern Bot 1 20230121
#5 Pattern Bot 2 20230121
#6 Random Throwback Bot 20230120
#7 Historian Bot 20230121
#8 You'll Remain Bot 20230121
#9 You'll Change Bot 20230121
#10 You'll Stay The Same If You Won Otherwise You'll Change Bot 20230121
#11 De Bruijn Bot 20260929
#12 Battery 12 Bot 20260929
#13 Favorite Bot 20260929
#14 Habit Bot 20260929
#15 Deja Vu Bot 20260929

#10 ??? unknown meta remain/change strat? maybe something like "if I'm losing, switch to my alter ego" thing


# De Se Bot Template
# def de_se_bot(p1hist, p2hist, whoAmI, rng): # de se knows which player it is
#     if (whoAmI == 1): 
#         #
#     else: #luigi
#         #


# rationing out randomness bit by bit?
# as a step up from purely deterministic bots which always have a perfect counter-bot that formally exists
# how un-counter-bottable can you become with one bit of randomness per move?
# and what about just having a "battery" in the form of one arbitrary high-kolmogorov-complexity string? eg length 12
# in lieu of randomness you can use your opponent's moves as a source of arbitrary variation.
# so you can have a different fixed arbitrary string that you'd do in response to any different arbitrary sequence
# (ideally they're not correlated with each other, nor with the input sequences that trigger them; fully arbitrary)