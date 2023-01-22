import random
numbers_to_moves = {0: "rock", 1:"paper", 2:"scissors"}

# 1 Random Bot
# plays random moves
def random_bot(p1hist, p2hist, whoAmI): # no hist usage
    return random.randint(0,2)

# 2a Rock Bot
# plays rock
def rock_bot(p1hist, p2hist, whoAmI): # no hist usage
    return 0

# 2 Constant Bot
# randomly picks a move to play forever
def constant_bot(p1hist, p2hist, whoAmI): # no hist usage; de se & random just for random first move as root of pattern
    if not p1hist:
        return random.randint(0,2)
    return(p1hist[0] if whoAmI == 1 else p2hist[0])

# 3 Random Throwback Bot
# after a random move, chooses a random player and a random past round and plays the historical move
def random_throwback_bot(p1hist, p2hist, whoAmI): # 100% hist usage
    if not p1hist:
        return random.randint(0,2)
    if (random.randint(0,1) == 0):
        return random.choice(p1hist)
    else:
        return random.choice(p2hist)

# 4 Historian Bot
# after a random move, plays p1's first move, then p2's first move, then p1's second move, then p2's second move...
def historian_bot(p1hist, p2hist, whoAmI): # 100% hist usage; random just for first move
    if not p1hist:
        return random.randint(0,2)
    turn = len(p1hist) - 1 # minus one to offset the very first turn where a random move is played
    if turn % 2 == 0:
        return p1hist[turn // 2]
    else:
        return p2hist[turn // 2]

# 5 Pattern Bot 1
# plays rock, rock, rock, paper, paper, rock
def pattern_bot_1(p1hist, p2hist, whoAmI): # no hist usage; de se & random just for random first move as root of pattern
    if not p1hist:
        return random.randint(0,2)
    base = p1hist[0] if whoAmI == 1 else p2hist[0]
    match len(p1hist) % 6:
        case 0: return (base) % 3
        case 1: return (base) % 3
        case 2: return (base) % 3
        case 3: return (base + 1) % 3
        case 4: return (base + 1) % 3
        case 5: return (base) % 3

# 6 Pattern Bot 2
# plays scissors, rock, rock, paper, paper, rock 200110 = 011221
def pattern_bot_2(p1hist, p2hist, whoAmI): # no hist usage; de se & random just for random first move as root of pattern
    if not p1hist:
        return random.randint(0,2)
    base = p1hist[0] if whoAmI == 1 else p2hist[0]
    match len(p1hist) % 6:
        case 0: return (base) % 3
        case 1: return (base + 1) % 3
        case 2: return (base + 1) % 3
        case 3: return (base + 2) % 3
        case 4: return (base + 2) % 3
        case 5: return (base + 1) % 3

# 7 Bet You'll Stay The Same Bot
# (1 random, then) plays the move that will beat the move rival just played
def youll_remain_bot(p1hist, p2hist, whoAmI): # most-recent-1 hist usage; de se knows which player it is
    if not p1hist:
        return random.randint(0,2)
    prev_opponent_move = p2hist[len(p1hist)-1] if whoAmI == 1 else p1hist[len(p1hist)-1]
    return (prev_opponent_move + 1) % 3

# 8 Bet You'll Change Bot
# (1 random, then) plays the move that could lose to the move rival just played (and so cant lose if you change)
def youll_change_bot(p1hist, p2hist, whoAmI): # most-recent-1 hist usage; de se knows which player it is
    if not p1hist:
        return random.randint(0,2)
    prev_opponent_move = p2hist[len(p1hist)-1] if whoAmI == 1 else p1hist[len(p1hist)-1]
    return (prev_opponent_move - 1) % 3

# 9 3-Cycle Bot
# plays a random 3-permutation aka 3-cycle; in this case, rock, paper, scissors (where which move comes first is random)
def three_cycle_bot(p1hist, p2hist, whoAmI): # only uses hist length; de se & random just for random first move as root of pattern
    if not p1hist:
        return random.randint(0,2)
    return((p1hist[0] + len(p1hist)) % 3 if whoAmI == 1 else (p2hist[0] + len(p1hist)) % 3)

# Engine
NUM_ROUNDS = 5000 # 10000
p1_wins = 0
p2_wins = 0
draws = 0
print(f"NUM_ROUNDS: {NUM_ROUNDS}")

def do_round(p1, p2, p1hist, p2hist):
    # print(p1hist)
    # print(p2hist)
    p1_move = p1(p1hist, p2hist, 1); p2_move = p2(p1hist, p2hist, 2)
    outcome = (p1_move - p2_move) % 3
    p1hist.append(p1_move)
    p2hist.append(p2_move)
    if outcome == 1:
        global p1_wins; p1_wins += 1 #print(" p1 wins!")
    if outcome == 2:
        global p2_wins; p2_wins += 1 #print(" p2 wins!")
    if outcome == 0:
        global draws; draws += 1 #print(" draw!")

def play_game(p1, p2):
    global NUM_ROUNDS
    p1_game_history = []
    p2_game_history = []
    global p1_wins
    global p2_wins
    global draws
    # print()
    # print(f"  ~ {p1.__name__} ___vs___ {p2.__name__} ~")
    # print(f"                    ~ Match Length: {NUM_ROUNDS} Rounds ~")
    round = 0
    while round < NUM_ROUNDS:
        do_round(p1, p2, p1_game_history, p2_game_history)
        round += 1
    winner = -1
    if p1_wins > p2_wins: winner = 1; #print("PLAYER 1 WINS")
    elif p2_wins > p1_wins: winner = 2; #print("PLAYER 2 WINS")
    else: winner = 0; #print ("IT'S A TIE! DRAW")
    # print("~~ Match Complete ~~")
    # print(f"PLAYER 1 WIN % {(p1_wins/NUM_ROUNDS)*100}")
    # print(f"PLAYER 2 WIN % {(p2_wins/NUM_ROUNDS)*100}")
    # print(f"DRAW % {(draws/NUM_ROUNDS)*100}")
    # print("GAME HISTORY FOR P1 and P2:")
    # print(p1_game_history)
    # print(p2_game_history)
    p1_wins = 0
    p2_wins = 0
    draws = 0
    return winner

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
play_game(youll_remain_bot, youll_change_bot) # p1 wins 66% of matches, p2 33% of matches; there are two equilibria that might happen of different rarity

# Round Robin Tournament Engine

def round_robin(competitors, score):
    i = 0
    j = 1
    while i < len(competitors):
        while j < len(competitors):
            winner = play_game(competitors[i], competitors[j])
            if winner == 1: tournament_scores[i] += 1; win_table[i][j] += 1
            elif winner == 2: tournament_scores[j] += 1; win_table[j][i] += 1
            else: tournament_scores[i] += .5; tournament_scores[j] += .5; win_table[i][j] += .5; win_table[j][i] += .5
            # print(tournament_scores)
            j += 1
        # print(j)
        i += 1
        j = i + 1
    # print(i)

def multi_round_robin(competitors, score, numRoundRobins):
    i = 0
    while i < NUM_ROUND_ROBINS:
        round_robin(tournament_competitors, tournament_scores)
        i += 1


tournament_competitors = [random_bot, constant_bot, random_throwback_bot, historian_bot, pattern_bot_1, pattern_bot_2, youll_remain_bot, youll_change_bot, three_cycle_bot]
tournament_scores = []
for i in range(len(tournament_competitors)):
    tournament_scores.append(0)
competitor_names = list(map(lambda x: x.__name__, tournament_competitors))
win_table = []
i = 0
j = 0
while i < len(tournament_competitors):
    win_table.append([])
    while j < len(tournament_competitors):
        win_table[i].append(0)
        j += 1
    i += 1
    j = 0

NUM_ROUND_ROBINS = 5000
print(f"NUM ROUND ROBINS: {NUM_ROUND_ROBINS}")
print(f"COMPETITORS: {competitor_names}")
multi_round_robin(tournament_competitors, tournament_scores, NUM_ROUND_ROBINS)
print("~~ Tournament Complete ~~")
print(tournament_scores)
normalized_scores = list(map(lambda x: x/NUM_ROUND_ROBINS, tournament_scores))
print(normalized_scores)
competitor_objects = []
for item in zip(tournament_competitors, normalized_scores, competitor_names):
    competitor_objects.append({"bot": item[0], "score": item[1], "name": item[2]})
competitor_objects.sort(key = lambda x: x['score'], reverse = True) # sort by score greatest to least
current_rank = 1
for competitor in competitor_objects:
    print(f"RANK {current_rank}: {competitor['name']}, WITH SCORE: {competitor['score']}")
    current_rank += 1
i = 0; j = 0
while i < len(win_table):
    print("[", end="")
    while j < len(win_table):
        print(f"{win_table[i][j]},".ljust(7), end="")
        j += 1
    print("]")
    j = 0; i += 1

# Botdex
#1 Random Bot 20230120
#2 Constant Bot 20230121
#3 Random Throwback Bot 20230120
#4 Historian Bot 20230121
#5 Pattern Bot 1 20230121
#6 Pattern Bot 2 20230121
#7 You'll Remain Bot 20230121
#8 You'll Change Bot 20230121
#9 3-Cycle Bot 20230121

#10 ??? unknown meta remain/change strat? maybe something like "if I'm losing, switch to my alter ego" thing, btwn #8 and #9 (tho you could do this meta mechanism between any two other bots)

# Bet I'll Stay The Same Bot (Bugged Bot)\
# (1 arbitrary, then) plays the move that will beat the move self just played (bugged bot)
# def ill_remain_bot(p1hist, p2hist, whoAmI): # most-recent-1 hist usage; de se knows which player it is
#     if not p1hist:
#         return 2
#     prev_opponent_move = p1hist[len(p1hist)-1] if whoAmI == 1 else p2hist[len(p1hist)-1]
#     print(prev_opponent_move)
#     return (prev_opponent_move + 1) % 3

# Bet I'll Change Bot (Bugged Bot)\
# (1 arbitrary, then) plays the move that could lose to the move self just played (bugged bot)
# def ill_change_bot(p1hist, p2hist, whoAmI): # most-recent-1 hist usage; de se knows which player it is
#     if not p1hist:
#         return 1
#     prev_opponent_move = p1hist[len(p1hist)-1] if whoAmI == 1 else p2hist[len(p1hist)-1]


# De Se Bot Template
# def de_se_bot(p1hist, p2hist, whoAmI): # de se knows which player it is
#     if (whoAmI == 1): 
#         #
#     else: #luigi
#         #


# DE SE DANGER
# This would be cheating I think:
# De Se Pattern Bot 1
# if p1, plays p,s,s,r,r,s
# if p2, plays r,p,p,s,p,r,r
# because in the tournament setting that's basically just having one bit of randomness if you're randomly White or Black as in chess
# And in a set of matches with one opponent that should be shuffled randomly... and so it's just like you each get a bit of randomness.
# or you could I guess also set it up so that one of you is p1 and the other is p2 and that's always mutually exclusive.
# that is, I guess, formally different from each of you getting a random bit independently... is it??? to do...
# the idea of an id that everyone knows, a haecceity "p1" "p2", interesting to try to spell out the formal consequences if any


# _Narcissist Historian Bot
# after two arbitary moves, plays pSm1, pSm2, pRm1, pSm3, pSm4, pRm2, pSm5, pSm6, pRm3, pSm7, pSm8, etc...
# pR = rival, pS = self
# def narcissist_historian_bot(p1hist, p2hist, whoAmI): # 100% hist usage, de se
    # if not p1hist: return 2
    # if len(p1hist) == 1: return 0
    # trickier than I expected...

# _Self-Conscious Historian Bot
# after two arbitary moves, plays pRm1, pRm2, pSm1, pRm3, pRm4, pSm2, pRm5, pRm6, pSm3, pRm7, pRm8, etc...
# pR = rival, pS = self
# def selfConscious_historian_bot(p1hist, p2hist, whoAmI): # 100% hist usage, de se
    # if not p1hist: return 1
    # if len(p1hist) == 1: return 2
    # trickier than I expected...

# _Moody Historian Bot
# alternates between being a Normal, Narcissist, and Self-Conscious Historian in 8-turn phases (leading to potential history repeats)
# def moody_historian_bot(p1hist, p2hist, whoAmI) # 100% hist usage, de se, meta
    # to do... could be first meta bot

# _Circumspect Moody Historian Bot
# same as Moody Historian Bot but avoids repeats while still biasing self or rival respectively in different moods
    # to do...


# rationing out randomness bit by bit?
# as a step up from purely deterministic bots which always have a perfect counter-bot that formally exists
# how un-counter-bottable can you become with one bit of randomness per move?
# and what about just having a "battery" in the form of one arbitrary high-kolmogorov-complexity string? eg length 12
# in lieu of randomness you can use your opponent's moves as a source of arbitrary variation.
# so you can have a different fixed arbitrary string that you'd do in response to any different arbitrary sequence
# (ideally they're not correlated with each other, nor with the input sequences that trigger them; fully arbitrary)