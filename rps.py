import random

numbers_to_moves = {0: "rock", 1:"paper", 2:"scissors"}
movepairs_to_outcomes = {}

# Random Bot
# plays random moves
def random_bot(p1hist, p2hist): # no hist usage
    return random.randint(0,2)

# Constant Bot
# plays rock
def constant_bot(p1hist, p2hist): # no hist usage
    return 0

# Random Throwback Bot
# after a random move, chooses a random player and a random past round and plays the historical move
def random_throwback_bot(p1hist, p2hist): # 100% hist usage
    if not p1hist:
        return random.randint(0,2)
    if (random.randint(0,1) == 0):
        return random.choice(p1hist)
    else:
        return random.choice(p2hist)

# Historian Bot
# after an arbitary move, plays p1's first move, then p2's first move, then p1's second move, then p2's second move...
def historian_bot(p1hist, p2hist): # 100% hist usage
    if not p1hist:
        return 1
    turn = len(p1hist) - 1 # minus one to offset the very first turn where an arbitrary move is played
    if turn % 2 == 0:
        return p1hist[turn // 2]
    else:
        return p2hist[turn // 2]

# Bet You'll Stay The Same Bot
# plays the move that will beat the move you just played

# Bet You'll Change Bot
# plays the move 


# Pattern Bot 1
# plays rock, rock, rock, paper, paper, rock
def pattern_bot_1(p1hist, p2hist):
    match len(p1hist) % 6:
        case 0:
            return 0
        case 1:
            return 0
        case 2:
            return 0
        case 3:
            return 1
        case 4:
            return 1
        case 5:
            return 0

# Engine
NUM_ROUNDS = 30 # 50000
p1_game_history = []
p2_game_history = []
p1_wins = 0
p2_wins = 0
draws = 0

def do_round(p1, p2):
    # print(p1_game_history)
    # print(p2_game_history)
    p1_move = p1(p1_game_history, p2_game_history); p2_move = p2(p1_game_history, p2_game_history)
    outcome = (p1_move - p2_move) % 3
    p1_game_history.append(p1_move)
    p2_game_history.append(p2_move)
    if outcome == 1:
        global p1_wins; p1_wins += 1; #print(" p1 wins!")
    if outcome == 2:
        global p2_wins; p2_wins += 1; #print(" p2 wins!")
    if outcome == 0:
        global draws; draws += 1; #print(" draw!")

round = 0
while round < NUM_ROUNDS:
    # print(f"~ Round {round + 1} ~")
    # do_round(random_bot, constant_bot)
    # do_round(random_bot, historian_bot)
    # do_round(random_throwback_bot, constant_bot) # VERY INTERESTING
    do_round(historian_bot, pattern_bot_1)
    # p1_game_history[round] = random_throwback_bot(p1hist, p2hist)  random_throwback_bot(p1hist, p2hist, )
    round += 1

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

# winner = "PLAYER 1" if p1_wins > p2_wins else "PLAYER 2" if p2_wins > p1_wins else "DRAW"
# print(winner)




# rationing out randomness bit by bit?
# as a step up from purely deterministic bots which always have a perfect counter-bot that formally exists
# how un-counter-bottable can you become with one bit of randomness per move?

# kolmogorov complexity of extremely finite strings