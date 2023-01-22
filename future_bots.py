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