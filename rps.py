import random
numbers_to_moves = {0: "rock", 1:"paper", 2:"scissors"}

# Random Bot
# plays random moves
def random_bot(p1hist, p2hist, whoAmI): # no hist usage
    return random.randint(0,2)

# Constant Bot
# plays rock
def constant_bot(p1hist, p2hist, whoAmI): # no hist usage
    return 0

# Random Throwback Bot
# after a random move, chooses a random player and a random past round and plays the historical move
def random_throwback_bot(p1hist, p2hist, whoAmI): # 100% hist usage
    if not p1hist:
        return random.randint(0,2)
    if (random.randint(0,1) == 0):
        return random.choice(p1hist)
    else:
        return random.choice(p2hist)

# Historian Bot
# after an arbitary move, plays p1's first move, then p2's first move, then p1's second move, then p2's second move...
def historian_bot(p1hist, p2hist, whoAmI): # 100% hist usage
    if not p1hist:
        return 1
    turn = len(p1hist) - 1 # minus one to offset the very first turn where an arbitrary move is played
    if turn % 2 == 0:
        return p1hist[turn // 2]
    else:
        return p2hist[turn // 2]

# Pattern Bot 1
# plays rock, rock, rock, paper, paper, rock
def pattern_bot_1(p1hist, p2hist, whoAmI): # no hist usage
    match len(p1hist) % 6:
        case 0: return 0
        case 1: return 0
        case 2: return 0
        case 3: return 1
        case 4: return 1
        case 5: return 0

# Pattern Bot 2
# plays scissors, rock, rock, paper, paper, rock
def pattern_bot_2(p1hist, p2hist, whoAmI): # no hist usage
    match len(p1hist) % 6:
        case 0: return 2
        case 1: return 0
        case 2: return 0
        case 3: return 1
        case 4: return 1
        case 5: return 0

# 3-Permutation Bot
# plays an arbitrary 3-permutation aka 3-cycle; in this case, scissors, rock, paper.
def three_cycle_bot(p1hist, p2hist, whoAmI): # only uses hist length
    return (len(p1hist) - 1) % 3

# Bet You'll Stay The Same Bot
# (1 arbitrary, then) plays the move that will beat the move rival just played
def youll_remain_bot(p1hist, p2hist, whoAmI): # most-recent-1 hist usage; de se knows which player it is
    if not p1hist:
        return 2
    prev_opponent_move = p2hist[len(p1hist)-1] if whoAmI == 1 else p1hist[len(p1hist)-1]
    return (prev_opponent_move + 1) % 3

# Bet You'll Change Bot
# (1 arbitrary, then) plays the move that could lose to the move rival just played (and so cant lose if you change)
def youll_change_bot(p1hist, p2hist, whoAmI): # most-recent-1 hist usage; de se knows which player it is
    if not p1hist:
        return 1
    prev_opponent_move = p2hist[len(p1hist)-1] if whoAmI == 1 else p1hist[len(p1hist)-1]
    return (prev_opponent_move - 1) % 3

# Engine
NUM_ROUNDS = 30 # 100000
p1_game_history = []
p2_game_history = []
p1_wins = 0
p2_wins = 0
draws = 0

def do_round(p1, p2):
    # print(p1_game_history)
    # print(p2_game_history)
    p1_move = p1(p1_game_history, p2_game_history, 1); p2_move = p2(p1_game_history, p2_game_history, 2)
    outcome = (p1_move - p2_move) % 3
    p1_game_history.append(p1_move)
    p2_game_history.append(p2_move)
    if outcome == 1:
        global p1_wins; p1_wins += 1; #print(" p1 wins!")
    if outcome == 2:
        global p2_wins; p2_wins += 1; #print(" p2 wins!")
    if outcome == 0:
        global draws; draws += 1; #print(" draw!")

def play_game(p1, p2):
    global NUM_ROUNDS;
    print(f"  ~ {p1.__name__} ___vs___ {p2.__name__} ~")
    print(f"                    ~ Match Length: {NUM_ROUNDS} Rounds ~")
    round = 0
    while round < NUM_ROUNDS:
        do_round(p1, p2)
        round += 1

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
play_game(youll_change_bot, constant_bot) # lmao
# play_game(youll_remain_bot, youll_change_bot) # p1 wins 100%

print("~~ Tournament Complete ~~")
winner = -1
if p1_wins > p2_wins: winner = 1; print("PLAYER 1 WINS")
elif p2_wins > p1_wins: winner = 2; print("PLAYER 2 WINS")
else: winner = 0; print ("IT'S A TIE! DRAW")
print(f"PLAYER 1 WIN % {(p1_wins/NUM_ROUNDS)*100}")
print(f"PLAYER 2 WIN % {(p2_wins/NUM_ROUNDS)*100}")
print(f"DRAW % {(draws/NUM_ROUNDS)*100}")
print("GAME HISTORY FOR P1 and P2:")
print(p1_game_history)
print(p2_game_history)

tournament_competitors = [random_bot, constant_bot, random_throwback_bot, historian_bot, pattern_bot_1, pattern_bot_2, youll_remain_bot, youll_change_bot]
# def round_robin(competitors):
#     #rodo

# round_robin(tournament_competitors)

# winner = "PLAYER 1" if p1_wins > p2_wins else "PLAYER 2" if p2_wins > p1_wins else "DRAW"
# print(winner)



# Botdex
#1 Random Bot 20230120
#2 Constant Bot 20230120
#3 Random Throwback Bot 20230120
#4 Historian Bot 20230120
#5 Pattern Bot 1 20230120
#6 Pattern Bot 2 20230120
#7 3-Permutation Bot 20230120
#8 You'll Remain Bot 20230120
#9 You'll Change Bot 20230120

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