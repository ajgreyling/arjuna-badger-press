# One — The Turkey's Ledger

*Anchored in* The Black Swan *— a thousand mornings of good evidence, and the one morning that outranks them all.*

### The fire

Taleb opens the fourth chapter of *The Black Swan* (2007) with a bird keeping honest books.

A turkey is fed every morning. The hand arrives, the grain arrives, and the bird's ledger records another confirmation: the world provides. A hundred mornings, five hundred, a thousand: not one bad entry in the record. By any fair reading of its own data, the turkey's confidence should grow with every feeding, and it does. Then comes day 1,001. The feed goes to zero, and the bird learns, briefly, what the feeding was for.

The part that cuts is that the turkey is not a fool. Give the bird the best estimator in the classroom and its ledger only improves. Laplace's rule of succession says that after n good mornings and none bad, the probability of one more is (n+1)/(n+2). On hatch day, with nothing observed, the rule offers even odds. After the full thousand mornings it says 1001/1002, which works out to about 99.9002%. Every step of that calculation is correct. The turkey's statistics were never bad; its reference class was. It counted the mornings it observed. The butcher counted a different list, fixed before the first feeding, and the hazard lived only in the second list. So each new day of data made the bird more certain and not one day safer, and confidence peaked on the exact morning it mattered least.

Taleb tells this in a book about markets because a trader's daily record has the same shape. A series can confirm you for a thousand days and carry no information at all about the day that ends the series. The track record is the feed. The confidence line is the risk report the desk prints every morning. And the sample, however long, was never the calendar.

### Where the smoke goes

Two pushbacks, both honest, and a debt to pay first.

The debt: the farmyard is borrowed ground, and Taleb says so. Bertrand Russell put a chicken there in 1912 — fed every day of its life, trusting the hand right up to the morning that same hand wrings its neck (*The Problems of Philosophy*, ch. VI). Russell in turn was walking a road Hume cut in 1748, asking what entitles us to step from bread that nourished us yesterday to bread that will nourish us tomorrow. Taleb swapped the chicken for a turkey and priced the intuition. The parable is his sharpest telling of a three-century-old problem, and he credits the lineage.

First pushback, marked contested: induction mostly works. The sun does rise. The bread does nourish. A reader who refused every extrapolation would starve faster than one who trusts too much, and critics note that most of the series a working person meets are not turkeys. The fair version of Taleb's reply is that he never claimed induction fails everywhere — only that in some domains the single exception carries more weight than the whole record, and those are precisely the domains where the record reads most reassuring.

Second, and this one matters to the working reader: the turkey could not have known. It had no access to the butcher's paperwork, and from inside the barn its despair or its confidence changed nothing. A trader is not quite in the barn. Some of the butcher's calendar is legible from inside a market — position reports, leverage cycles, the crowding visible in public filings. The parable, read carefully, says look rather than despair: the question it leaves behind is which mornings your series never sampled, whose schedule your data cannot contain. Whether that looking succeeds is itself contested — plenty of people read the filings before the crash and stayed turkeys — but the parable at least tells you where to point your eyes.

### Plainly

**`plainly:`** I built a backtest once that I very nearly trusted.

A simple rule, run over years of daily data. The equity curve came out smooth as a handrail. Modest maximum drawdown, steady win rate, and I remember the specific comfort of scrolling through it. Every historical day the rule survived felt like one more spoonful of feed. What took me embarrassingly long to say out loud was that the sample was calm because I had chosen a calm sample. The worst loss in my backtest was just the worst loss that window happened to contain, and the window did not contain its own ending. No window does. My daily marks were the feed line. My drawdown figure was the turkey's confidence: computed correctly from the mornings it had, and silent about the morning already scheduled. The rule may even have been fine. The ledger simply could not know, and I had been reading its growing smoothness as growing safety, which is the one thing a ledger of good mornings can never certify.

### The line

**`plainly:`** *A record of good mornings measures the mornings, never the calendar that schedules them — the arithmetic can be flawless while the reference class is wrong.* The bird itself lives in *The Black Swan*, chapter 4. It is a short chapter, and Taleb's own telling will outlast every summary of it, including this one. Go read him.

### Run it

The paired instrument is live at https://lucid.rodeo/incerto/turkey/. On hatch day, before you press anything, Laplace's rule sits at even odds; press Live a day and the count begins, and fast-forward and the blue confidence line climbs while the gold feed line holds near 100 units, exactly as the exhibit draws it. The number to check with your own hands: the morning the feed drops to zero, the confidence reads 99.9002% — that is 1001/1002, and you can rebuild it with a pencil. What the instrument cannot say: which of your own series is a turkey. It replays a parable whose ending is already scheduled, and a measured tail is the past, not a forecast.
