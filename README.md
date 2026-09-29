# rps
rock paper scissors bot arena

Run `python3 rps.py` to play a round-robin tournament between the bots in `tournament_competitors` (near the bottom of `rps.py`).

## Bots
A bot is a function `bot(p1hist, p2hist, whoAmI, rng)` that returns 0 (rock), 1 (paper) or 2 (scissors).
- `p1hist`, `p2hist`: each player's moves so far
- `whoAmI`: which seat the bot is in, 1 or 2
- `rng`: the bot's only source of randomness, via `rng.randint(a, b)` and `rng.choice(seq)`. Don't use the `random` module directly: the engine needs to see every draw (and will complain if a bot uses `random` in an exact game).

A bot decorated with `@with_memory` also gets a fifth argument, `memory`: a dict that lasts for one game. It's only for keeping track of things the bot has worked out from the history (or drawn from `rng`) so it doesn't redo them every move (see the predator bots).

A bot decorated with `@rationed(every, bits)` may only draw randomness on rounds 0, `every`, 2 * `every`, ..., and at most `bits` bits each time (the engine raises `RationExceeded` otherwise). It can save what it draws in `memory` and use it later: what's rationed is how much randomness it gets, not when it uses it.

`string_bot(moves, name)` makes a bot that loops through a fixed list of moves. With `random_start=True` it starts at a random point in the list, which costs log2(len(moves)) bits of randomness. `string_counter_bot(moves, name, random_start)` is the perfect counter-bot to it: it knows the string and how the start is chosen, and works out where the string bot is.

`plan_bot(plans, name)` makes a rationed bot that, every `len(plans[0])` rounds, picks one of its plans at random and plays it; `plan_counter_bot(plans, name)` is its perfect counter-bot. `best_plans(n, rounds)` works out the n plans that buy the most margin against that counter-bot. With `mask=` (a function of the round number, like `pi_digit`), every move is shifted by the mask, which costs no randomness.

With `mask_bits=b`, the mask starts at a secret place, drawn once per game (b bits). With `base=bot` (a deterministic bot), each move is the base bot's move, varied by the plan. `plan_counter_bot` handles all of these.

`mixture_bot(strategies, name)` makes a rationed bot that, every 10 rounds, picks one of several deterministic strategies (which can react to the rival) at random and follows it; `mixture_counter_bot(target, name)` is its perfect counter-bot, which runs all the strategies alongside it and keeps track of which ones still fit. `lookahead_counter_bot(target, name)` is a far-sighted version that plans its own moves ahead (for strategies without memory). `fixed_start(bot)` turns a bot whose only randomness is its first move into a deterministic strategy.

## Tournament
- Every match is two games of `NUM_ROUNDS` rounds with the seats swapped. It's scored two ways:
  - **per-game:** each game is worth half a point on its own
  - **aggregate:** the margins (rounds won minus rounds lost) from both games are added up and scored like one long game

  Either way you have to win by more than 1 round; otherwise it's a tie. Per-game scoring rewards winning often; aggregate scoring rewards winning big.
- A game whose random draws have at most `MAX_BRANCHES` possible sequences is computed exactly, by playing every sequence and weighting it by its probability. Any other game is estimated from `NUM_SAMPLES` sampled games; those results are marked `~` and scores get a ± standard error.
- The results also report how many bits of randomness each bot used per game, and which matchups the two scorings disagree on.
- Matches are played on `NUM_WORKERS` processes at once (all your CPU cores by default; one at a time on Windows).

## Experiments
- `python3 string_experiment.py` (about 1.5 minutes):
  1. string bots (de Bruijn strings vs arbitrary strings, at lengths 3 to 6561, plus `pi_bot`) against the predator bots
  2. how much margin a random start buys a string bot against its perfect counter-bot
  3. the string of each length (3, 6, 9) whose random start buys the most, found by checking every string
  4. longer strings (up to 81) whose random start buys as much as any bot possibly could with that much randomness, found by search (`python3 string_experiment.py search LENGTH SECONDS` to search yourself)
- `python3 rationing_experiment.py` (about 15 seconds): how much a bot can protect itself against the perfect counter-bot when its randomness is rationed; how rationed bots do against their perfect counter-bot versus cheap predators; where a mixture bot's randomness goes; and why a mask is a shared secret
- `python3 mixtures_and_masks_experiment.py` (about 4 minutes): greedy vs. far-sighted counter-bots against mixtures of the original reactive bots; a mixture of different strategies vs. designed variations on one; and how many bits a mask's secret start needs

## Writeups
`writeups/` has a short illustrated writeup of each round of exploration, as Markdown and PDF. `python3 writeups/build_pdf.py writeups/NN-name.md` rebuilds a PDF (needs `pip install markdown` and Chrome or Chromium), and `python3 writeups/figures/make_NN.py` redraws its figures (needs `pip install matplotlib`).
