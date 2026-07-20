# Four — The Crowd's Average and Yours

*Anchored in* Skin in the Game *— one casino counted two ways, and which count a single life gets.*

### The fire

The picture, paraphrased from chapter 19 of *Skin in the Game* (2018), is a casino counted two ways.

First count. A hundred people play on the same night, each with their own stake. Some win, some lose. Player 28 goes bust, and player 29 never feels it. At closing you pool what the hundred hold, divide by a hundred, and you have the ensemble average: the return of the crowd. An honest number. The one the brochure prints.

Second count. One person plays a hundred nights running. On night 28 he busts, and night 29 is never played. Ruin anywhere along the sequence removes him from every round after it, and nobody's luck can stand in for his: the crowd was reassembled fresh each round, while he arrives at each night as whatever the last night left him. Taleb's claim, at full strength: these are two different quantities. The first is measured across people, the second along one life, and wherever ruin is possible they refuse to agree. Much of what decision theory filed under irrational risk aversion, he argues in that chapter, is a person correctly declining the crowd's number for the one their own timeline pays. He names his sources for the frame — the physicists Ole Peters and Murray Gell-Mann.

His sources ran the game with a coin. Start with a dollar. Fair coin. Heads multiplies wealth by 1.5, tails by 0.6. The crowd's number is pencil work: 0.5·1.5 + 0.5·0.6 = 1.05, so the ensemble average grows ×1.05 a round, every round. Follow one player instead. The coin is fair to them too, so a long run pairs heads with tails, and each pair multiplies wealth by 1.5 × 0.6 = 0.9; a typical round is therefore worth √0.9, about ×0.9487. Both numbers are correct. After a hundred rounds the mean sits near 1.05^100 ≈ 131.5 and the median near 0.9^50 ≈ 0.005154: the average player turned a dollar into some 131; the typical player holds half a cent. The mean rides on a sliver of lucky streaks, and a room of players can easily contain none of them.

The repair is older than the quarrel. Kelly, writing in the *Bell System Technical Journal* in 1956, derived the growth-optimal fraction: a player wagering only f of their wealth each round grows, along time, at g(f) = ½ln(1+0.5f) + ½ln(1−0.4f). That curve peaks at f* = 1/4 exactly, where the typical player compounds at ×1.00623 per round, and it crosses zero at f = 0.5, since 1.25 × 0.8 = 1. A quarter staked, and the typical player finally grows. The whole stake, and the crowd gets rich while the player goes broke.

### Where the smoke goes

Contested, and worth stating the way the critics themselves would sign it. In 2020 Jason Doctor, Peter Wakker and Tong Wang replied to Peters in *Nature Physics* (volume 16, page 1168, a Matters Arising, the journal's formal channel for dissent). Nobody on either side questions the sums. Their case is that economics was never confused about them. The field has handled repeated multiplicative gambles since Bernoulli, expected-utility theory accommodates this game without strain, and the claim they reject is the large one: that ergodicity economics rewrites decision theory. In their reading the arithmetic is old and sound, and the revolution is a relabelling. Peters answered in the same journal (page 1169), standing by the reframing. The dispute is live, and the arithmetic is nobody's hostage: Taleb's chapter stands on the sums; how much of decision theory must move because of them is the open question.

### Plainly

**`plainly:`** A fund is an ensemble; a founder is a time series.

I run a small press. Somewhere a spreadsheet holds the ensemble view of what I do — many small publishers, most failing, a few compounding, an industry average that could look healthy the whole while. That view is real, and useless to me, because I am not the industry. If the press hits zero in a bad year, no luckier parallel publisher carries on in my name; the year after a zero is a zero, and so is every year after that. A life gets one path, walked in order, in which whatever is ruined stays ruined for every later step. The coin game is this fact with the sentiment removed: the crowd wins ×1.05 a round while the person playing shrinks toward half a cent, and which of those describes you depends only on where you stand. A portfolio stands in many places at once. A person only ever stands in one.

### The line

**`plainly:`** *The crowd's average is taken across many players in one round; yours is taken along one player across many rounds; wherever ruin is possible the two part company, and a life is lived on the second.* The full argument is chapter 19 of *Skin in the Game*, on the logic of risk taking. Go read it there.

### Run it

The paired instrument is https://lucid.rodeo/incerto/ergodicity/ — a thousand seeded players running the exact game Peters and Gell-Mann published in *Chaos* in 2016 and Peters later made the centrepiece of his 2019 *Nature Physics* paper. The number to check with your own hands: at full stake the gold ensemble line climbs ×1.05 a round while the simulated median falls at ×0.9487; move the bet-fraction slider to the Kelly quarter and the typical player turns upward, ×1.00623 a round. Switch the rounds to 1000 and watch the simulated mean fall below the gold line: a thousand players almost never contain the one streak that carries it. What the instrument cannot say: what fraction of anything you should wager. The page refuses that question, and so does this book. The curve it draws is one game on one seed — and a measured tail is the past, not a forecast.
