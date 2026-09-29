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

def play_game(p1, p2, tape=None): # returns p1's points (1 win, .5 tie, 0 loss) and the bits of randomness each bot used
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
    if margin > 1: points = 1 # you have to win by more than 1
    elif margin < -1: points = 0
    else: points = .5
    # print(f"{p1.__name__} vs {p2.__name__}: p1 margin {margin}")
    # print(p1hist)
    # print(p2hist)
    return points, rng1.bits, rng2.bits

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

def exact_game(p1, p2): # p1's exact expected points and each bot's expected bits, found by playing every possible sequence of draws
    points = p1_bits = p2_bits = 0
    script = []
    while True: # (each path has probability >= 1 / MAX_BRANCHES, so there are at most MAX_BRANCHES paths)
        tape = Tape(script)
        random_state = random.getstate()
        result = play_game(p1, p2, tape)
        if random.getstate() != random_state: # a bot used the random module, so this wouldn't really be exact
            raise RuntimeError(f"{p1.__name__} or {p2.__name__} uses the random module; bots must get randomness from rng")
        chance = Fraction(1, tape.branches)
        points += chance * Fraction(result[0]); p1_bits += float(chance) * result[1]; p2_bits += float(chance) * result[2]
        # next sequence of draws, like an odometer: bump the last draw that isn't at its max, and drop everything after it
        draws = tape.draws
        while draws and draws[-1][0] == draws[-1][1] - 1:
            draws.pop()
        if not draws: break
        script = [value for value, n in draws[:-1]] + [draws[-1][0] + 1]
    return float(points), p1_bits, p2_bits, 0.0

def sampled_game(p1, p2): # same as exact_game but estimated, plus the standard error of p1's points
    results = [play_game(p1, p2) for _ in range(NUM_SAMPLES)]
    points = sum(r[0] for r in results) / NUM_SAMPLES
    variance = sum((r[0] - points) ** 2 for r in results) / max(NUM_SAMPLES - 1, 1)
    return points, sum(r[1] for r in results) / NUM_SAMPLES, sum(r[2] for r in results) / NUM_SAMPLES, math.sqrt(variance / NUM_SAMPLES)

def expected_game(p1, p2):
    try:
        return exact_game(p1, p2)
    except TooManyBranches:
        return sampled_game(p1, p2)

# Round Robin Tournament Engine

def round_robin(competitors):
    # every match is a pair of games with the seats swapped, each game worth half a point
    n = len(competitors)
    win_table = [[0] * n for _ in range(n)] # expected points of row bot vs column bot (0 to 1)
    error_table = [[0] * n for _ in range(n)] # standard error of each entry; 0 means exact
    bits = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            a = competitors[i]; b = competitors[j]
            a_points_1, a_bits_1, b_bits_1, error_1 = expected_game(a, b) # a is p1
            b_points_2, b_bits_2, a_bits_2, error_2 = expected_game(b, a) # b is p1
            win_table[i][j] = (a_points_1 + (1 - b_points_2)) / 2
            win_table[j][i] = 1 - win_table[i][j]
            error_table[i][j] = error_table[j][i] = math.sqrt(error_1 ** 2 + error_2 ** 2) / 2
            bits[i] += a_bits_1 + a_bits_2; bits[j] += b_bits_1 + b_bits_2
    bits_per_game = [b / (2 * (n - 1)) for b in bits]
    return win_table, error_table, bits_per_game


if __name__ == "__main__":
    print(f"NUM_ROUNDS: {NUM_ROUNDS}")
    print(f"MAX_BRANCHES: {MAX_BRANCHES}, NUM_SAMPLES: {NUM_SAMPLES}")
    # tournament_competitors = [random_bot, constant_bot, random_throwback_bot, historian_bot, pattern_bot_1, pattern_bot_2, youll_remain_bot, youll_change_bot, three_cycle_bot]
    tournament_competitors = [random_bot, constant_bot, three_cycle_bot, pattern_bot_1, pattern_bot_2, random_throwback_bot, historian_bot, youll_remain_bot, youll_change_bot, youll_remain_if_won_else_change_bot]
    competitor_names = list(map(lambda x: x.__name__, tournament_competitors))
    print(f"COMPETITORS: {competitor_names}")
    win_table, error_table, bits_per_game = round_robin(tournament_competitors)
    print("~~ Tournament Complete ~~")
    scores = [sum(row) for row in win_table]
    errors = [math.sqrt(sum(e ** 2 for e in row)) for row in error_table]
    ranking = sorted(zip(scores, errors, competitor_names, bits_per_game), key = lambda x: x[0], reverse = True) # sort by score greatest to least
    current_rank = 1
    for score, error, name, bits in ranking:
        score_text = f"{score:.4f}" if error == 0 else f"{score:.4f} (± {error:.4f})"
        print(f"RANK {current_rank}: {name}, WITH SCORE: {score_text}, BITS OF RANDOMNESS PER GAME: {bits:.2f}")
        current_rank += 1
    print("WIN TABLE (row's expected points vs column; ~ means sampled, otherwise exact)")
    for i in range(len(win_table)):
        print("[", end="")
        for j in range(len(win_table)):
            cell = "--" if i == j else ("~" if error_table[i][j] else "") + f"{win_table[i][j]:.3f}"
            print(f"{cell},".ljust(8), end="")
        print("]")

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