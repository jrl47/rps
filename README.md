# rps
rock paper scissors bot arena

Run `python3 rps.py` to play a round-robin tournament between the bots in `tournament_competitors` (near the bottom of `rps.py`).

## Bots
A bot is a function `bot(p1hist, p2hist, whoAmI, rng)` that returns 0 (rock), 1 (paper) or 2 (scissors).
- `p1hist`, `p2hist`: each player's moves so far
- `whoAmI`: which seat the bot is in, 1 or 2
- `rng`: the bot's only source of randomness, via `rng.randint(a, b)` and `rng.choice(seq)`. Don't use the `random` module directly: the engine needs to see every draw (and will complain if a bot uses `random` in an exact game).

## Tournament
- Every match is two games of `NUM_ROUNDS` rounds with the seats swapped, each worth half a point. You have to win a game by more than 1 round; otherwise it's a tie.
- A game whose random draws have at most `MAX_BRANCHES` possible sequences is computed exactly, by playing every sequence and weighting it by its probability. Any other game is estimated from `NUM_SAMPLES` sampled games; those results are marked `~` and scores get a ± standard error.
- The results also report how many bits of randomness each bot used per game.
