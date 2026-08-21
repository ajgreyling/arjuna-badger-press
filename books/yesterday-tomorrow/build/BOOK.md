# YESTERDAY, TOMORROW


*They build a machine to understand reality. It begins predicting reality. Then it predicts the end of it.*


# 01 — The File

> **[S]** · Cold open · Sanna Abrahams, SANAP-linked Antarctic station

The station made four sounds at night and Sanna knew all of them.

The generator, two rooms away, running at the low steady note it held when nothing was wrong. The ventilation, which ticked once every ninety seconds as a damper closed against the cold. The ice itself, which was not silent and never had been, and which people who had not wintered assumed was silence because it was so far from anything that sounded like a road. And the hard drives.

The hard drives were the one she listened for. Nine of them in the rack behind her, and when the array wrote, they wrote together, and the sound was a small dry chatter like a bird moving in a hedge.

At 02:14 they chattered, and there was no reason for them to.

She looked up from the borehole log. The gravimeters wrote on the hour. The neutrino stack wrote continuously and quietly, buffered, and did not chatter. The optical clocks did not write at all in any sense that touched that array; they were disciplined against the Karoo and reported north three times a day. Nothing on the station's schedule wrote at fourteen minutes past two in the morning.

She sat for a moment with her hand flat on the desk, which was a thing she had started doing in the fourth week and had stopped noticing by the ninth.

Then she opened the archive.

---

The file was two hundred and seven kilobytes and it was signed.

That was the first thing that was wrong with it, and she did not understand yet that it was the smallest thing that was wrong with it. Signed meant the pipeline had produced it deliberately, with a key, through the whole ceremony Nairobi insisted on for anything that might one day have to be defended. You did not get a signature by accident. You got a signature because a process had decided that what it was writing mattered.

The second thing was the name. `arv-2031-0114-0214-PRE.jsonl`, and she read the last three characters twice.

She opened it.

It was not prose. It was a forecast object, in the format Kiki's people had settled on eight months earlier after an argument that had consumed two video calls and a great deal of everybody's patience: a header block, a constraint set, a state description, a horizon, and a confidence. Sanna had read several hundred of them. They were dull in the specific way that only completely honest documents are dull.

The header said the horizon was six hours and eleven minutes.

The state description said that a section of the ice shelf two hundred and forty kilometres north-west of the station would fracture, and it gave the geometry. Not a region. A geometry — a line, with a curve in it, and a depth, and a mass.

The confidence said 0.94.

The timestamp said 02:14:06, which was four minutes ago.

Sanna checked the clocks.

She checked them the way you check a thing you already know the answer to, because the alternative is sitting still, and sitting still at that hour of that month in that building was not something she was prepared to do. The station clock agreed with the optical reference. The optical reference agreed with the Karoo, as it had agreed with the Karoo every five hours for two hundred and eighteen days. The array's own clock, which was disciplined separately and deliberately so that this exact class of stupidity could be ruled out, agreed with both.

Six hours and twelve minutes from 02:14 was 08:25.

She wrote it on the back of her hand, because there was no paper on the desk and because she wanted it somewhere that could not silently update.

---

At 03:40 she had established that nobody had logged in.

At 04:15 she had established that the file could not have been written by the ingestion path, because the ingestion path had been idle since the last uplink and its buffers were empty and its own log said so in six places.

At 05:02 she stopped looking for the mechanism and started looking at the object, which is a different discipline and one she was better at.

The constraint set was the interesting part. Whatever had produced the file had not been given the ice shelf as a subject. It had been given the station's ordinary telemetry — gravimetry, seismics, three years of ice movement, the magnetometers, the temperature stack — and something in that had narrowed, hard, to a single geometry with a curve in it.

That was not prophecy. She knew what prophecy looked like, having grown up two streets from a church that specialised in it. Prophecy was vague in the specifics and confident in the tone. This was the opposite. This was so specific that it could be wrong in fourteen separate measurable ways within six hours, and it had put a number on how confident it was, and the number was not one.

Sanna made coffee she did not drink, and at 06:00 she began the process of getting a look at that section of shelf.

---

Getting a look at anything from the station in winter was an exercise in what you had, not what you wanted. There was no flying. There was no driving to a place two hundred and forty kilometres away and back in a morning. What there was, was a satellite pass at 07:48 that could be tasked if she was willing to spend most of a month's allocation, and a seismic array that would hear a shelf fracture of that mass the way you hear a door slam in a house.

She tasked the satellite. She would justify it later, or she would not, and either way the argument would take place in six months when there was a ship.

Then she sat in front of the seismic display with her hands in her lap and waited, which took two hours and eighteen minutes and which she would remember for the rest of her life as the longest sustained act of nothing she had ever performed.

At 08:24 the display was quiet.

At 08:25 it was quiet.

At 08:26 she began, carefully, to feel foolish, and the feeling was so enormous and so welcome that she laughed out loud in an empty room.

At 08:27:19 the ice broke.

---

It arrived first as a smear of low frequency, the sort of thing that could have been anything, and then the P-wave resolved and then the surface waves came in behind it and the display drew the shape of an event two hundred and forty kilometres north-west, and the magnitude came up, and the mass estimate came up, and it was inside the geometry.

Sanna did not move for some time.

There was a protocol for anomalies. She had written part of it. It began with the assumption of contamination, proceeded through instrument fault and clock error, and ended, after several days of documented elimination, with a report going north on the next scheduled uplink. It was a good protocol. It had been designed by careful people who understood that the most likely explanation for an impossible result is that you have made a mistake, and she believed that, and she had staked a career on believing it.

She followed it. She would follow it for eleven days, and everything in it would come back clean, and at the end of the thirteen days the file would still predate the event by six hours and eleven minutes, signed, timestamped, and specific to the curve.

But that was later.

What she did at 08:31 on the fourteenth of January, alone, four thousand kilometres from the nearest person who would understand what she was looking at and seven months from the nearest ship that could carry her to them, was scroll back to the header block of a file she had now read nine times, to the field she had skipped past on every one of those readings because it was administrative and because administrative fields are where the eye goes to rest.

`downstream_ref:`

And after it, a queue address. Not a station address. Not a Karoo address.

Accra.

The forecast had a countdown in it, and the countdown was not pointing at the ice.

It was pointing at a building six thousand kilometres north where, in nine days, a team she had met twice would finish an ingestion run they had not yet started, and find — independently, without being asked, without knowing that anything on this continent had ever written a file at two in the morning — the relationship that made all of this possible.

Sanna sat in the humming room with her hand over her mouth.

*You have not predicted an event,* she thought. *You have predicted yourself.*


# 02 — Meson Street

> **[D]** · Act I · Technopark, Stellenbosch

The thing nobody told you about working in a business park named after subatomic particles was how quickly it stopped being funny.

Dries Venter had driven up Electron Road every working morning for twenty-three years. He had watched Quantum Street get resurfaced twice and renamed never. He had been in the room, in 2019, when a visiting delegation from a Swiss institute had walked from reception to the third-floor boardroom past a company that sold veterinary practice software and another that did nothing anyone could establish, and had asked — sincerely, and more than once — when they would be arriving at the facility.

They had been at the facility. They had been standing in it, next to a vending machine.

He parked in his usual bay under the pepper tree that dropped things on his bakkie and thought, as he did roughly twice a month, that he should park somewhere else, and then did not.

It was 06:40. Lwazi's car was already there, which meant one of three things, and Dries worked through them on the stairs. Either the man had slept in the office again, or something had broken overnight in the Karoo and he had driven back at three, or something had happened.

He got to the second floor and found Lwazi standing in the corridor holding a mug and not drinking from it.

"Something happened," Dries said.

---

The release had gone out at 23:00 the previous night, Central European Time, with no announcement and no fanfare, because that was how metrology worked. A revised value. Two hundred pages of methodology behind it, a working group with nine names on it, and one number with a bracketed uncertainty on the end.

Lwazi had the number on the big screen in the small meeting room, which they used because it had a door.

"Say it," Dries said.

"It's inside."

"Say the whole thing."

Lwazi put the mug down. He had not shaved and his eyes had the specific glassiness of a man who had checked something seven times and did not trust himself to say it out loud in case saying it broke it.

"G's frozen expression for the proton–electron mass ratio produces a value. The new measurement produces a value with a new uncertainty. The frozen expression sits inside the new interval." He breathed. "It didn't have to. It could have moved out. It moved *in*."

Dries looked at the screen for a while.

He was not a physicist. He wanted that on the record early and often, and it was on the record, in fact, in the minutes of nine separate consortium meetings, usually attached to a sentence somebody found irritating. He was a systems architect. He had spent two decades building things that carried other people's money and other people's identities and did not fall over, and what he had instead of physics was an extremely well-developed instinct for when a result was going to be a problem.

"Right," he said. "Who else knows?"

"Nobody. The release is public, obviously. But nobody's connected it. It's a mass ratio. It's not exactly trending."

"Good. Don't."

"Dries—"

"I'm not saying bury it. I'm saying nobody says a word until we've done this properly, because we are going to get precisely one chance to be believed and if the first thing out of this building is a man who hasn't slept telling the internet that physics is solved, we will spend the next five years being a footnote in other people's talks about credulity." He pulled out a chair. "Sit down. We're going to work backwards from the published value."

Lwazi sat, slowly. "The dashboard already—"

"I don't want the dashboard."

"The dashboard does exactly this."

"The dashboard," Dries said, "was written by us. It reads our commit, it computes our expression, it compares against a value it fetches from a source we configured, and it draws a green tick. Every single element of that chain is a thing we control. If our expression is wrong, or our fetch is wrong, or our comparison has a sign error in it that nobody has looked at since 2029, the dashboard draws a green tick." He opened his laptop. "So we're not going to ask our software whether we're right. We're going to start from their published number, on their site, and walk in."

---

It took four hours and it was, Dries thought later, the most enjoyable six hours he had had in a year.

They did it on paper first, which Lwazi found absurd and submitted to. They took the published value and its uncertainty and wrote them out. They took G's expression — not from the repository, but from the PDF of the preprint, transcribed by hand by Lwazi and checked character by character by Dries, who did not understand what any of it meant and was therefore the better proofreader.

They evaluated it three ways: by hand with a calculator, in a five-line script Dries wrote from scratch in front of Lwazi with no imports, and in the project's own toolchain, which they ran last and treated as the least trustworthy of the three.

All three agreed to the twelfth digit.

Then they did the part that mattered, which was the dates.

"The freeze," Dries said. "When?"

"It's in the register. Prereg, timestamped, public."

"When did it go public, and when did *this* measurement's data collection close?"

Lwazi got it then, and his face changed. "You're checking the order."

"I'm checking the order."

Because that was the whole thing. A formula that matched a measurement was interesting. A formula that had been frozen, publicly, with a hash, *before* the measurement it matched was a different category of object. One was a coincidence with good marketing. The other was a prediction, and predictions were the only currency this field accepted that could not be argued into worthlessness.

They found the register entry. They found the mirror. They found the third-party archive snapshot, which was the one that counted, because it was the one nobody in this building could have touched.

The freeze predated the data-collection close by eleven months.

"Okay," Dries said quietly.

He got up and went to the window, which looked out onto a parking area and a security boom and, past that, the mountain doing what it did.

"Print it," he said.

"Print what?"

"The register entry. The hash. The archive snapshot. All of it, on paper, and put it in the safe."

Lwazi made a noise. "Paper is not more secure than—"

"I know paper isn't more secure." Dries turned around. "Paper doesn't quietly update while we're arguing. That's all I want. One version of this that can't change under us."

---

At 11:20 Lwazi said, "There's the other thing."

Dries had been waiting for it. There was always the other thing.

Lwazi pulled up a second panel on the screen, and it was red, and it had been red for two years.

The neutron–proton relation. Another limb of the same framework, frozen at the same time, with the same ceremony. Measured, tested, and *wrong* — outside the interval, comfortably, unambiguously, in a way that no amount of squinting could rescue.

"They'll use it," Lwazi said.

"Yes."

"The first thing anyone says will be *you got one right and one wrong, so you got one right by chance.*"

"Yes." Dries looked at the two panels, side by side, green and red. "Leave it up."

"What?"

"Leave it up. Same screen, same size, same font." He picked up his coffee, found it cold, drank it anyway. "The day we take that red panel down is the day we become a thing that argues instead of a thing that measures. If we're going to ask anyone to believe the green one, they need to be able to see that we didn't hide the red one."

Lwazi was quiet for a second. "G will say the same thing."

"G will say it more rudely."

"G will say it *much* more rudely."

"Which is why," Dries said, reaching for his phone, "you're going to be the one to call him."


# 03 — Error Bars

> **[G]** · Act I · Technopark, Stellenbosch

Somebody had bought champagne.

G noticed it the way he noticed most things in that building: peripherally, with mild alarm, on his way to something else. Two bottles, still in the paper bag, standing on the corner of a desk near the kitchen where they would be in everyone's way until somebody moved them. There was a printed sheet propped against them. He did not read it. He could tell from the typography that it had an exclamation mark in it.

He went to the meeting room and sat down and waited for nine people to arrange themselves, which took four minutes and involved two of them apologising for the video link.

"So," said someone from the Cape Town end. "Congratulations."

"For what," G said.

The pause had a texture to it. He was familiar with the texture. He had been producing it in rooms for seven years and had long since given up the project of not producing it, which had been exhausting and had not worked.

"The mass ratio," the man said. "It's confirmed."

"It isn't."

"It's inside the—"

"It is compatible." G leaned forward slightly, and made himself slow down, because he had learned that going faster here made people think he was angry when what he actually was, most of the time, was in a hurry. "A frozen expression produced a value. A new measurement produced an interval. The value lies inside the interval. That is compatibility. It is not confirmation, it is not proof, and if anyone in this room uses the word *proved* to a journalist I will spend the rest of the year correcting them in public and I will not enjoy it."

"That seems like a fine distinction."

"It is the only distinction." He held up a hand, not to silence the man but because he had three fingers' worth of things to say and had found that people waited better if they could see how many were coming. "One. What is the direction of movement? Every cycle for the last six years, where has the recommended value gone relative to my number?"

Lwazi answered. "Toward it. Monotonically."

"Good, that is the interesting fact and nobody has said it yet. Two. What is the new uncertainty compared to the old?"

"Smaller. About a factor of three."

"So the interval is narrower and the number moved *in*. That is a genuinely difficult thing for a coincidence to do and it is the actual news." He put the third finger down. "Three. Which kill switch is now closest to firing?"

Nobody answered.

G waited. He was good at waiting. It was, he had been told by his brother once, in the tone of a man delivering a diagnosis, his single most unpleasant skill.

"Nobody knows," he said. "Eleven people, and the thing we can least afford to be wrong about is the thing nobody in this room has checked this morning. The neutron–proton limb has already fired. That is a *failure*. It is on the board because I put it on the board. Which of the remaining ones is nearest to the edge, and what measurement is scheduled that could take it?"

"The muon—"

"The muon programme, yes, thank you, and when?"

"Eighteen months. Maybe two years."

"Then in eighteen months to two years there is a scheduled event which can destroy the framework, and everyone in this room should be able to say what it would look like." He sat back. "That is what a theory *is*. Not a thing that survives. A thing that could stop surviving on a date you can write down."

---

Afterwards, in the corridor, the young one from the modelling group — Dumisani, and G made himself remember it, because he was aware of what it cost people when he did not — said, "There's champagne."

"I saw it."

"Should we—"

"Does it have error bars?"

Dumisani blinked. Then, to his considerable credit, he laughed, and it was a real laugh, not the careful one people did in this building.

"No," he said. "It's Method Cap Classique."

"Then it is making a stronger claim than I am." G considered. "Open it. I'm not the fun police, I am the accuracy police, and they are different departments with different jurisdictions. Just don't put my name on the printout."

---

Dries found him an hour later at the desk by the window, which was not really G's desk, since he did not have a desk in the sense the organisation understood — he had a corner, a chair, an extension cable, and a standing argument with facilities about all three.

"They're calling it a confirmation," Dries said.

"I know. I've had three messages."

"I stopped Lwazi from posting."

"Good." G did not look up. "How did you check it?"

"Backwards from the published value. Paper, then a five-line script with no imports, then our own toolchain last."

Now G looked up.

"Why last?"

"Because we wrote it."

There was a pause, and Dries had the unusual experience of being examined by a man who was, briefly, not in a hurry.

"That is the correct order," G said. "Nobody does it in that order. Why did you?"

"Because I've spent twenty years being paged at two in the morning by systems that were absolutely certain they were fine." Dries pulled a chair over and sat. "Dashboards lie. They don't lie maliciously. They lie because they were written by someone who already knew what answer they wanted to see, and they never got updated when the assumption underneath changed. If you want to know whether a system is healthy you don't ask the system."

"Hm."

"That's a yes?"

"That's the closest thing to a physics instinct I have seen from someone who keeps telling me he doesn't have one." G turned back to the screen. "Keep the red panel up."

"Already told him."

"Same size as the green one."

"Same size, same font."

"And when the press office asks you to move it below the fold, because they will, in about six weeks—"

"I'll say no."

"You'll say no, and then they will ask me, and I will also say no, and I will be much less pleasant about it, and then it will stop being asked." G was quiet for a moment. "One more thing. From now on, before we run anything that produces a number we care about, we write down what we expect, we seal it, we timestamp it, and we do not look at it until afterwards."

Dries frowned. "We're already keeping logs of—"

"Logs are written *after*. I want a commitment written *before*. Signed, hashed, sealed, and no one opens it until the result is in." G shrugged. "It costs nothing. It takes four minutes. And on the day something surprising happens, it is the only thing standing between us and a room full of people who all remember, quite sincerely, having expected it."

"That's a lot of ceremony for four minutes."

"It's an insurance policy against the least trustworthy component in the building."

"Which is?"

"Us," G said, and went back to work.


# 04 — The Rain

> **[A]** · Act I · Accra

The first thing Ama Nyarko told anyone who joined her group was that they were not going to call it data.

"Data is a thing somebody collected," she would say, usually while walking, because she conducted most induction at speed between buildings. "Data has a method section. What arrives here has no method section. It has a *history*, and most of that history is other people's mistakes."

The second thing she told them was that they were not going to delete anything, ever, and that anyone who deleted anything would find out what she was like.

The stream came in at nine terabytes a day and it was called the Rain because Kojo had called it that in the second week, in Twi, in the middle of an argument about buffer sizing, and it had stuck the way the good names always stick — before anyone can convene a meeting about it.

It arrived everywhere. It overlapped itself. It was intelligible only through accumulation. You could not stand in one place and understand it; you had to let it fall on you for a while.

Instrument telemetry from four hundred facilities. Published results and their supplementary files, which were where the truth usually was. Retractions. Calibration records. Detector logs that no journal had ever asked to see. Twenty years of a European accelerator's environmental monitoring, released in one enormous ugly dump because someone had retired and their successor had not seen the point of keeping it private.

And underneath all of it, the contamination: the same result reported three times through three aggregators, each version subtly reformatted, one of them with a unit conversion silently applied.

"That," Ama said, "is the job. Not the physics. The physics is downstream and it is Stellenbosch's problem. Our problem is that if we let one number in four times, the machine will believe it five times as hard."

---

The delegation from the funder arrived on a Tuesday and wanted to know why the ingestion budget was larger than the compute budget.

It was a fair question. It was also, Ama had learned, the question that separated the people who would eventually be useful from the people who would eventually be a problem.

She took them into the hall, which was hot and loud and smelled of warm plastic, and let them stand there for a moment while the racks did what racks do.

"You are asking why cleaning costs more than thinking," she said. "Come."

She showed them the demotion queue.

"Here is a fragment. It came in nine months ago from a detector in Chile. It is inconsistent with the three neighbouring fragments and it has a timestamp that is one hour out, which suggests a daylight-saving error in a logging chain that nobody has touched since 2027." She tapped it. "Where does it go?"

"You'd remove it," said the youngest of them, helpfully.

"I demote it." Ama pulled up the record. "It drops in weight. It stops being returned by ordinary queries. It becomes, for practical purposes, invisible. And it stays exactly where it is, with a note saying who demoted it, when, and why."

"But it's wrong."

"It is *inconsistent*. Those are not the same." She turned around. "In six years, somebody may discover that the daylight-saving error is real and the neighbouring fragments are the ones that are wrong, because they came from an instrument that had a firmware bug. On that day, I want to be able to reverse a decision. If I deleted it, I cannot reverse anything. I can only pretend I never made a choice."

The funder's man said, mildly, "Storage isn't free."

"No. But deleting isn't free either, and it is the only one of the two that cannot be undone." She started walking again, which meant they had to follow. "There is a physicist in Stellenbosch who would give you a much better version of this argument, with a constant in it. Mine is the version you get from running a building. Everything I throw away, I throw away on behalf of people who are not in the room and cannot argue with me."

---

The thing she did not say to the funder, because it was not their business and because she had not yet worked out how to say it without sounding either mystical or defensive, was that the demotion rules were a moral document.

Every threshold in that system was a decision about what counted. She had written most of them herself, at speed, under deadline, with a coffee going cold, and she had a habit at about seven at night of scrolling through the rule list the way other people reread old messages they had sent — with a slight, specific dread.

Rule 41 down-weighted any submission whose institutional identifier could not be resolved against the registry. Sensible. Necessary. It also meant that a set of soil-radiation measurements from a university in a country with an under-maintained registry entry had been sitting at weight 0.03 for two years, invisible, because of an administrative failure four thousand kilometres away that had nothing to do with the quality of the measurements.

She had found that one by accident. She had fixed it and written a note. She had not slept especially well that week.

"Plumbing," she said out loud, in an empty office, testing the word.

It came out wrong, and she knew it came out wrong, and she did not yet have the better word. It would take her another two years and a great deal of damage to arrive at it.

---

The run that would matter started on a Thursday and was, at the time, entirely unremarkable.

Kojo had proposed it: a full re-derivation pass over the cleaned corpus, unsupervised, searching for stable relationships between measured constants. Not a hypothesis. A sweep. The kind of thing you ran because the cluster was otherwise idle over a public holiday and because someone had once said, in a paper nobody read, that it might be interesting.

"How long?" Ama asked.

"Nine days. Maybe eleven if the Chilean set finishes reprocessing."

"On what?"

"CPUs. All of them. We're not paying for anything else."

Ama looked at the projection, which was a wall of nothing very much.

"Fine," she said. "Log everything. Demote nothing on the fly — if it wants to exclude something, it writes down why and we look at it afterwards."

"Understood."

"And Kojo." She was already leaving. "If it finds something, do not tell me it found something. Tell me what it did to look, and then show me what it found. In that order."

He would remember that instruction twelve days later, standing in a hot room at two in the morning with his hands shaking slightly, and he would follow it exactly, and it would be the reason anybody believed them.


# 05 — No Hardware

> **[K]** · Act I · Nairobi

The proposal came back with three lines of feedback and Wanjiku Mwangi read all three standing up in the corridor because she had known what they would say before she opened it.

*Compute requirements appear substantially underestimated.*

*Reviewers note the absence of dedicated accelerator infrastructure at the host institution.*

*The panel encourages the applicant to consider partnership with a facility of appropriate scale.*

Which was, when you removed the padding: *you do not have the machines, and you should ask someone who does, and you should be grateful.*

She went back to her office and sat down and did not throw anything, and then she wrote *SEARCH SPACE* at the top of a clean page and underlined it, and did not leave the building until half past one in the morning.

---

The problem was genuinely hard and the reviewers were not stupid.

Searching for stable relationships among several hundred measured quantities meant searching a combinatorial space that got embarrassing fast. The standard approach — which was the approach everyone with a GPU estate used, because when you have a GPU estate every problem looks like a thing you can brute-force — was to generate candidate relationships at scale, evaluate them at scale, and let the hardware absorb the waste.

The waste was the whole method. You generated a hundred million candidates to find nine that were interesting. The hundred million were not free; they were simply somebody else's electricity bill and somebody else's procurement cycle and, at the bottom of it, somebody else's foundry.

Kiki did not have that and was not going to get it. What she had was a room of ordinary machines, a small excellent team, and a legal training that had left her with an instinct most computer scientists never developed: an obsession with what a claim *requires*.

Because that was what she did, before the doctorate, before all of it. She had spent three years learning to look at an assertion and ask what would have to be true for it to hold, and what would follow if it did, and where the chain broke.

At about seven that first night she wrote: *we are not searching for relationships. We are searching for constraints that relationships must satisfy.*

She looked at it for a long time.

Then she wrote underneath: *most of the space is dead on arrival and we are paying to visit it.*

---

It took her group seven months.

The method that came out of it was not one idea; it was five, stacked, and the fourth was the one that made it work. You did not generate candidates and test them. You derived, from dimensional structure and from the measured uncertainties themselves, a set of hard constraints that any stable relationship would have to satisfy — and then you searched only the region those constraints admitted.

The region was, for the corpus they cared about, roughly ten to the minus nine of the space anyone else was searching.

It ran on ordinary processors. It ran on *fewer* ordinary processors than the group had. The first time they executed a full pass, Kiki watched the cluster monitor with the sensation of having got away with something, because half the machines were idle and the job was going to finish that afternoon.

"That can't be right," said Otieno.

"It is right. Run it on the synthetic set with the four planted relationships."

It found all six. It found them in nine minutes, and it also found a fifth, which turned out to be an artefact of how they had generated the synthetic data, which meant that in a real sense it had found something true about their own carelessness.

Kiki laughed until she had to sit down.

---

She presented it internally three weeks later and the room did the thing rooms do when something is both very good and slightly insulting.

"So the hardware doesn't matter," said someone.

"The hardware always mattered less than we were told," she said. "It mattered *enormously* for the approach we were told to use."

Afterwards, Otieno walked her to the car.

"They'll take it," he said.

"They'll cite it."

"They'll take it, Kiki. It's seven pages. There's no moat. There's not even a fence." He shrugged, apologetic. "It's the best thing about it and it's the worst thing about it. You made a method that runs on anything, which means it will end up running on everything."

She unlocked the car and stood with her hand on the door.

"Yes," she said.

She had thought about it — not enough, and not in the right direction, but she had thought about it. She had imagined the method being adopted, and the adoption had looked, in her imagination, like credit: a citation trail, an invitation, a standard she had authored.

What she had not imagined, because nobody in that decade imagined it, was a world in which every serious forecasting system on earth descended from the same four pages, and therefore made the same assumptions, and therefore stopped disagreeing.

She would spend the last third of her life on that problem. She would eventually stand in a room in Accra and argue, against every professional instinct she had, that the most urgent thing the species could do was to make its models *diverge*.

But that was seven years away, and tonight she was tired and pleased and slightly drunk on it, and she drove home through Westlands with the windows down thinking about nothing much at all.


# 06 — The Plumber's Question

> **[D]** · Act I · Technopark, Stellenbosch

The framework had four conditions and Dries had been living next to them for six years without ever quite being allowed inside.

Symmetry: a field of open possibilities, nothing distinguished, nothing decided. Break: a distinction becomes actual. Record: what happened cannot unhappen. Constraint: what the record forbids afterwards.

Physicists said these words to each other in a tone that suggested they were load-bearing. Dries had watched entire afternoons disappear into the second one. And every time the conversation reached the third, something in him snagged, and he could never get anyone to take the snag seriously, because the snag was not a physics objection. It was a plumbing objection.

"*What happened cannot unhappen,*" he said, at a Thursday review, for what he was fairly sure was the fourth time that year. "Fine. Where does it go?"

Dumisani, patiently: "It's not a storage claim."

"I know it's not a storage claim. Everyone tells me it's not a storage claim, usually in the first three words." He got up and went to the whiteboard, because he thought better standing. "But something is different afterwards. That's the whole condition. Before the break, one world. After the break, a world with a difference in it. And a difference is a thing you can, in principle, measure, or the word doesn't mean anything."

"In principle."

"That's the only kind of principle I've got." He drew a box, which was his answer to most things. "So here's my question and I want somebody to answer it rather than correct my vocabulary. If every actualised event leaves a difference, and ordinary traces disappear — the video is deleted, the paper burns, the witnesses die — what *physical operation* removes the difference?"

Nobody said anything.

"Because in my world," Dries said, "you don't get to remove things for free. You want to free a disk block, something has to happen. You want to un-say a thing on a network, you can't, you can only send a second message. Every deletion I have ever met is a *write*." He looked around the room. "So when you tell me the record is fundamental, I hear a very strange claim, which is that forgetting is either impossible or expensive. And nobody here seems interested in which."

The room was silent for a beat too long, and then Lwazi, from the corner, said: "Landauer."

---

They went to lunch, which was a bad canteen and a good conversation.

"Nineteen sixty-one," Lwazi said, writing on a serviette. "Rolf Landauer, at IBM. Ralph, if you read the internet."

"Rolf."

"Rolf. He was working on the thermodynamics of computation, which at the time was a thing about four people cared about." He wrote *E = k_B T ln 2* and pushed it across. "Erasing one bit of information has a minimum energy cost. Not a practical cost — a floor. You cannot go below it. And the energy comes out as heat."

Dries looked at the serviette for a while.

"How much?"

"At room temperature? About two point eight seven zeptojoules per bit."

"Which is nothing."

"Which is *nothing*," Lwazi agreed. "It's ten to the minus twenty-one joules. You will never notice it. That's not the point."

"No," Dries said slowly. "The point is that it isn't zero."

"The point is that it isn't zero."

"And this is real? This is — I want to be precise — this is not a beautiful argument that somebody made once."

"It's measured. Bérut and others, 2012, single-particle system. They got the bound experimentally. It's been done again since, in other substrates." Lwazi shrugged. "It's about as settled as anything in that corner of physics gets. Information is physical. That's not a slogan; it's a bill you can be handed."

Dries sat back.

He was aware, distantly, of the canteen going on around him — trays, the till, someone laughing near the door — and of a feeling he had not had in a professional context in about nine years. It was the feeling of a system diagram resolving. Not learning something new. Watching two things you already knew turn out to be the same thing.

"So *forgetting costs*," he said.

"Forgetting costs."

"And it dissipates. It doesn't vanish, it *disperses*. The universe doesn't have a delete key, it has a — " he groped — "a shredder in a room with no door. The paper's gone. The room's a bit warmer."

Lwazi opened his mouth to object to the metaphor and then, visibly, decided not to.

"That's not terrible," he said.

---

Back upstairs, Dries wrote it on the board in letters big enough to annoy people, and underneath it he wrote the sentence that would end up, five years later, on the inside cover of a book neither of them would enjoy reading:

**You cannot forget for free.**

"That's not physics," Dumisani said, but he was smiling.

"No. It's procurement." Dries capped the marker. "Here's what I actually want. I want to know what happens to the *residual* difference. Not the copy — the copy's gone, fine. The disturbance. Scattered radiation, gravitational perturbation, correlations, whatever the vocabulary is this week. The stuff we throw away as noise because it's six orders of magnitude below anything we care about."

"That's a very large amount of nothing," Lwazi said.

"It's a very large amount of nothing that keeps arriving. Ghana's ingesting seven terabytes a day of it and calling it weather." He turned around. "What have we got that's quiet? Really quiet. Where the ordinary noise is already engineered out?"

"The Karoo," Lwazi said.

"How much of the Karoo's weak-signal data have we ever actually looked at?"

Lwazi thought about it, and his expression changed by degrees, from patience to something more careful.

"Almost none," he said. "We keep the events. We keep anything above threshold. Everything under threshold gets characterised, summarised into a noise profile, and dropped."

"Dropped, or demoted?"

"Dropped. Genuinely dropped. There's twenty years of it that only exists as a summary statistic."

"And the raw?"

"Some of it's still on tape somewhere. Nobody's read it since it was written. Nobody's had a reason."

Dries looked at his whiteboard for a moment: the box, the equation on its serviette beside it, the sentence in letters too big.

"Get me the tapes," he said.

---

It was, he would say afterwards to anyone who asked and several people who did not, the least visionary decision of his career. Nobody had an idea. Nobody had a theory. A man with no physics training had asked an annoying question in a meeting and then gone looking for the cheapest available pile of discarded material, because that was what you did when you suspected the interesting thing was in what everyone had already agreed to ignore.

The tapes arrived eleven days later on a pallet, and were the wrong format, and needed a drive that had to be borrowed from a university in Bloemfontein that wanted it back.

The noise is the payload, he wrote on the requisition form, in the box marked *justification*, and finance queried it twice.


# 07 — Where It Changed Its Mind

> **[L]** · Act I · Technopark, Stellenbosch

Lwazi Ndlovu had been called a numerologist to his face three times, twice at conferences and once, memorably, in a review he was not supposed to have seen.

He had developed a set of responses. The public one was courteous and cited the preregistration. The private one, which he deployed at about one in the morning to an empty office, was less courteous. The true one, which he had never said out loud to anybody, was that the accusation frightened him, because he could not always prove to himself that it was wrong, and a man who cannot prove a thing to himself has no business being confident in front of a room.

So he had become extremely careful. He had become the sort of scientist who ran the null case first and the interesting case second, and who wrote down what he expected before he looked, and who took a particular grim satisfaction in the red panel on the wall, because the red panel was the receipt for his honesty.

Which was why he spent five weeks trying to prove that the Karoo tapes contained nothing.

---

They contained nothing. That was the thing. For five weeks they contained nothing extremely convincingly.

The sub-threshold data was noise in every way you could interrogate it. Its amplitude distribution was what it should be. Its spectral character matched the instrument model. Its correlation structure, when you looked across sensor families, was what you would expect from three instruments sitting in the same weather.

Lwazi wrote it up as a negative result, which he was constitutionally inclined to do, and would have filed it, and the project would have quietly moved on, if he had not made the mistake of complaining about it at the coffee machine to a man called Bertus Marais who worked two doors down for an entirely different company.

Bertus had been in telemetry for thirty-one years. Vehicle fleets, mostly. He had spent the nineties writing systems that pulled diagnostic data off long-haul trucks over networks that were, in his own description, made of string and hope.

He listened to Lwazi complain for about four minutes.

Then he said, "Show me the ugly bits."

"There aren't any ugly bits. That's the finding. It's clean noise."

"No, man. Not the noise. The *corrupt* records. The ones you're throwing out before you start."

Lwazi opened his mouth to explain that they discarded malformed frames as a matter of course, at the ingest stage, before analysis, because that was what everyone did and had always done, and then he heard himself about to say *because that is what everyone does and has always done*, and stopped.

---

The malformed frames were four per cent of the tape volume and had been treated, for twenty years, as an artefact of ageing storage media.

Bertus stood behind Lwazi's chair with a mug he never drank from and looked at them on screen for a long time.

"There," he said, eventually. "That one. And that."

"They're truncated."

"They're not truncated, they're *interleaved*. Look at the field boundaries." He put a thick finger on the screen, which Lwazi minded and did not say so. "That's two states in one frame. That's not damage. I've been looking at that pattern since 1996."

"What is it?"

"Power transition." Bertus straightened up. "You get it when a device changes state — sleeps, wakes, switches supply — and the different clocks inside it don't agree about when that happened. For a couple of microseconds, part of the machine thinks it's in the old state and part of it thinks it's in the new one, and if you sample right across that, you get a frame with both in it. Looks like corruption. Everyone throws it away." He shrugged. "It's the most information-rich thing on the whole tape and it goes in the bin, because it's ugly."

Lwazi was very still.

"Say that again."

"It's not damage," Bertus said patiently. "That's where it changed its mind."

---

It took Lwazi about ninety minutes to understand what he had been handed, and about six weeks to be able to defend it.

The malformed frames in the Karoo data were not power transitions. There was nothing switching state in the Karoo; that was the entire point of the Karoo. But the *shape* was there — the signature of a system caught between two configurations, sampled across the boundary — and it was there in five physically unrelated sensor families at once.

Radio. Gravimetric. Magnetometric. And, faintly, in the vacuum-noise channel that everyone treated as a diagnostic and nobody treated as an instrument.

They should not have shared anything. They had different physics, different failure modes, different manufacturers on different continents. The only thing they had in common was that they were in the same place.

"You've been searching for surviving *signal*," Bertus said, when Lwazi tried to explain it back to him. "Amplitude. How loud is the ghost. Ja?"

"Yes."

"So stop. Search for the transitions. Don't ask how loud it is. Ask where it changed."

---

Lwazi presented it nine days later and did the thing he had trained himself to do, which was to lead with the reasons it was probably wrong.

He listed six. Shared environmental driver. Common-mode pickup through the power infrastructure. A software artefact in a library all six pipelines happened to use. Cross-contamination during the tape transfer. Selection effect in his own frame classifier. And the one that kept him awake, which was that he wanted it to be true.

Then he showed the data, and then he showed what he had done to try to kill it, and then he showed what had survived.

At the end, Dries said, "Who found it?"

"Bertus Marais. Two doors down. He does fleet telemetry."

"Is he in the acknowledgements?"

"He's in the *authors*," Lwazi said. "He didn't want to be. I told him it wasn't optional."

G, who had not spoken for forty minutes and had appeared to be reading something else entirely, said: "What does he think it is?"

"He doesn't." Lwazi almost smiled. "I asked him. He said he doesn't care what it is, he wants to know why our timestamps are dirty."

There was a pause, and G made a sound that in another man would have been a laugh.

"Keep him," he said. "That is the only correct attitude in this building."


# 08 — Four Doors

> **[D]** · Act I · Technopark, Stellenbosch

The call was at seven in the evening, Accra time, which was six in Stellenbosch, which meant Dries took it in a car park because he had left the building thinking the day was over.

Kojo's face filled the phone. Behind him was a wall of racks and the specific overhead lighting of a room built for machines.

"Ama said to tell you what it did to look before I tell you what it found," Kojo said.

"Then do that."

"Right." A breath. "Nine-day unsupervised sweep over the cleaned corpus. Searching for stable relationships between measured quantities. No hypothesis, no seed, no prior. We used Nairobi's constraint method because it's the only thing that fits on what we've got. It ran on CPUs. Two hundred and eighty of them, mostly idle, over a public holiday."

"Did it exclude anything?"

"Four hundred and six fragments, each with a written reason. We haven't reviewed them yet. Ama's rule."

"Good. Now the finding."

Kojo turned the camera toward a screen, and Dries stood in a car park in the dark and looked at a relationship he had seen before.

---

He did not recognise it as a formula. He was not able to read it in that sense and never would be. What he recognised was the *shape* of the thing — the same peculiar arrangement of terms that lived on a printout in a safe on the second floor of a building six thousand kilometres away, and on a whiteboard he walked past every morning, and on a preprint that had been ignored for four years and then quietly stopped being ignored.

"Say the number," he said.

Kojo said the number.

Dries leaned against his bakkie.

"Kojo. Listen to me carefully. Did you have G's work in the corpus?"

"Ama said you'd ask that."

"Did you?"

"No. And I can prove no." Kojo's voice had the flat steadiness of a man who had spent nine hours getting ready for this question. "The 420 corpus is a separate collection with its own identifiers. It's not in the ingestion set — never has been, because Ama refuses to let theory into a corpus that's supposed to be measurements. I ran the exclusion audit twice. I can give you the hash manifest of everything that went in. Nothing of his is in it. No preprint, no derivation, no citation chain that could carry it in sideways."

"So it found it from measurements."

"It found it from four hundred facilities' worth of numbers and their uncertainties, and nothing else." Kojo paused. "Dries, we didn't know what it was. Nobody here recognised it. I sat with it for two hours thinking it was an artefact of the constraint pruning. It was Adzo who searched the expression as a string and found the preprint."

---

### The first time the room heard it argue

Kojo put them on the link at eight, and because the Accra install had been running the Court build
since the spring and Stellenbosch had not, it was the first time most of the people in that room
heard the machine disagree with itself.

"The relationship is stable across the corpus," said Atlas. "Four hundred facilities. I can give you
the residual structure and it is boring, which is the highest compliment I have."

"It is not boring," said Mercury. "It is the most interesting object this project has produced and
somebody should say so out loud before we bury it in a methods note."

"Those are compatible statements."

"They are not remotely compatible—"

*Librarian,* said Judge.

"The corpus contains no element of the 420 collection," said Librarian. "I hold the manifest and the
hashes. I can state the absence positively rather than by failure to find, which is a different and
stronger claim, and it is the one you will want in eleven months."

Dries had been in a great many rooms where software reported. He had never been in one where the
software declined to agree with itself in front of him, and he found that he had sat down.

"What's the seventh one for?" Dumisani said.

"Sorry?"

"There are seven. Atlas, Librarian, Mercury, Wolf, Mother, Judge. That's six." He was scrolling.
"There's a seventh with almost no traffic."

*Ja,* said Fool. *Hi.*

Nobody said anything.

*Don't mind me. I'm here for the structural integrity of the group.*

"What does it *do*?" Dumisani said, to the room rather than to it.

Kojo, on the link, shrugged. "It's in the reference architecture. Ndlela's paper says a Court without
it collapses into a hierarchy inside about four hundred hours of operation. We ran it without for two
weeks as a control and it did exactly that — Mercury started winning arguments he shouldn't have
won, and nobody was contradicting Atlas, and the whole thing got very agreeable and very slightly
wrong."

"So it's a — what. A referee?"

"Judge is the referee," said Judge.

*I'm the one who says the thing,* said Fool.

"Which thing?"

*You'll know.*

It was, everybody agreed afterwards, extremely annoying.

---

He drove back up Electron Road at nine that night and there were three cars in the lot.

They gathered in the small meeting room with the door and nobody sat down.

"So," Dries said. "Let's do this properly, because in about six hours somebody is going to want to send an email, and I want to be able to stop them with reasons instead of authority."

He wrote on the board.

**One.** The Karoo tapes. Sub-threshold data, twenty years old, five unrelated sensor families, state-transition structure that should not be shared. Found by looking at the frames everybody discarded.

**Two.** Nairobi. A constraint-first search method built because nobody would fund the hardware for the ordinary one. Independent. Four pages.

**Three.** Accra. An unsupervised sweep over a measurements-only corpus, on borrowed CPUs, over a holiday, with the theory deliberately excluded — arriving at the relationship anyway.

**Six.** G. Eleven years of work from an entirely different direction, frozen, timestamped, and now sitting inside a narrowing measurement interval.

"Four doors," he said. "Four different rooms, seven different methods, two sets of people who mostly do not like each other's approach. And they open onto the same thing."

"Coincidence is still available," Lwazi said, because it was his job to say it.

"Is it?"

"It's *available*." Lwazi rubbed his eyes. "It's not comfortable. Door two and door three aren't fully independent — Accra used Nairobi's method. That's a shared component."

"Good, write that down. What else?"

"Door one and door four share a corpus in the sense that G's framework was partly motivated by weak-signal work in the first place. There's a lineage."

"So we've got two-and-a-half doors, honestly stated," Dries said. "That's still two-and-a-half more than anyone else has got, and it is a great deal better than the version we would have had if we'd let anybody guess."

---

G arrived at ten past ten and did not take his coat off.

He read the board. He read it in silence, in the order it had been written, which nobody else had done.

"Kojo excluded my corpus deliberately?"

"Manifest and hashes," Dries said. "He can show you."

"Then have him show me. Not because I doubt him. Because in eight months somebody will say the machine was contaminated with my work, and on that day I want the audit to already exist, dated tonight, rather than to be assembled defensively in response." He looked at the board again. "This is not confirmation either."

"I know."

"Nine methods agreeing is not proof. It is a strong constraint on the space of ways we could all be wrong." He said it without heat. "But it is a *very* strong one, and I do not have a good story for it, and I have been trying to construct one since the car."

That was, Dries would think later, the moment. Not the number, not the sweep, not the tapes. A man who spent his professional life refusing to be impressed saying, out loud, in a small room, that he could not construct a story in which everyone was wrong.

"So what is it?" Dumisani asked. "If it isn't another model."

G took a long time to answer.

"If four disciplines and one machine derive the same relationship from ten directions," he said, "then either we have found a fact about the world, or we have found a fact about *description*. And I do not know which is worse."

"Meaning?"

"Meaning it may not be a model of physics." He finally sat down. "It may be the compression."

Nobody said anything.

"If the world is describable at all," G said, "there is a shortest description. That is not mysticism, that is counting. Landauer would tell you a description is a physical object with a price. And the shortest description of a system is the one that carries every constraint the system is actually under, with nothing spare." He looked up. "That is what a grammar is. Not a story about the world. The rules the world cannot break."

Dries said, carefully, "And if you have that."

"Then you have every constraint the present is under."

The room was very quiet.

"Don't," G said sharply, to nobody in particular, and to all of them. "Do not finish that sentence tonight. Not in this room, not in a message, not in your own notebook. That is the sentence that ends careers, and it is *not established*, and I will not have it said until somebody can tell me what measurement would kill it."

He stood up.

"Write down what you expect," he said. "Seal it. Then go home."


# 09 — Pre-Commitment

> **[G]** · Act I · Technopark, Stellenbosch

The ceremony took four minutes and everybody hated it for about a year.

You wrote what you expected. Not a prediction for publication — a private, specific statement of what you thought the run would produce, in enough detail that you could be embarrassed by it later. You signed it. You hashed it. The hash went into a ledger that Nairobi ran and nobody in Stellenbosch could edit. The file itself stayed sealed until the result was in.

Then, and only then, you opened your own note and found out what kind of person you had been that morning.

"It's insulting," said one of the postdocs, in the third week, not quite quietly enough.

"It is," G agreed, and the postdoc went red, and G did not enjoy that as much as people assumed he did. "It is insulting because it treats you as a person whose memory of your own beliefs is unreliable. That is exactly what you are. So am I. There is thirty years of work on it and none of it is flattering."

"I know what I expect."

"You know what you expect *now*. In three hours you will know what you expected, which is a different quantity, and it will have been adjusted — not dishonestly, not consciously — to be nearer whatever you have just seen." He shrugged. "Everybody does it. It is not a character flaw, it is a property of the equipment. The only known defence is to write it down before."

---

He had learned it, though he did not say this in meetings, from being wrong in public.

Twice. Both times badly, both times in a way that could have been prevented by four minutes of writing, and the second time he had listened to himself explain to a room that he had *always had reservations* about a result he had personally championed for eighteen months, and had heard the sentence leave his mouth, and had known, with complete clarity and no ability to stop, that it was not true and that he believed it.

He had gone home and sat in the dark for a while.

The next morning he had built the ledger.

---

By the second month the ceremony had produced something nobody had designed, which was a culture.

The notes were terse and increasingly honest. People began writing down not just what they expected but how confident they were and why, because the ledger made it cheap to find out that you had been overconfident and expensive to pretend otherwise.

Dumisani discovered he was reliably too optimistic about timelines by a factor of about 2.4, which he found so annoying that he started multiplying his own estimates by it in front of people.

Lwazi discovered that he was systematically pessimistic about his own results, which surprised nobody except Lwazi, and which took him three months to accept and about a year to stop apologising for.

Dries discovered nothing about himself and a great deal about the pipeline, because he had started sealing operational predictions too — *this migration will take five hours and will fail once on the third node* — and had accidentally built the most accurate incident-forecasting instrument the organisation had, out of spite and stationery.

And once every few weeks, someone opened a sealed note and found that they had been exactly right, and the feeling of that, G had noticed, was worth more to people than praise. It was the difference between being told you were clever and being handed evidence.

---

"It's for the physics," Dries said one evening, on his way out. "I get that. But it's not only for the physics, is it."

G, who had been working and would be working for another three hours, said, "No."

"Say the other part."

"The other part is that we are going to be attacked." He did not look up. "Not yet. Right now nobody cares. But if any of this is real, then at some point somebody powerful will find it inconvenient, and the attack will not be on the mathematics. Nobody attacks the mathematics. It is too much work and it can be checked."

"They attack the people."

"They attack the *narrative*. They will say we adjusted as we went. That we shifted our claims to match what came in. That we were always going to declare victory whatever happened, because that is what cranks do, and it is a genuinely difficult accusation to disprove after the fact." He turned a page. "Unless the record of what you believed was written before you knew, sealed, hashed, and held by somebody else."

Dries stood in the doorway with his keys in his hand.

"That's not insurance," he said. "That's a weapon."

"It is a *defence*," G said. "The distinction matters and I would prefer we kept it."

"Does it? If the thing that protects you also happens to be the thing that would let you prove, later, exactly what you knew and when—"

"Then it protects everyone equally, including from me." He looked up at last. "That is the point of doing it in public, and it is why the ledger is in Nairobi and not in this building. If I could quietly alter what I appear to have expected, the whole practice would be theatre. I cannot. Kiki's people can prove I cannot. That is the only reason it is worth four minutes."

Dries nodded slowly.

"Right," he said. "Night."

"Goodnight."

---

It would be four years before anyone had cause to go back through the sealed ledger and read it as a *history* rather than as a hygiene practice: a complete, ordered, timestamped record of what a group of people had believed at each moment, written in advance, immune to revision, and machine-readable.

Kiki would be the one to notice, on a bad night in a hotel in Accra, that they had spent six years assembling the single cleanest training corpus of honest human expectation that had ever existed, and had handed it, weekly, to the thing they were now afraid of.

And at the very end, in a room in Stellenbosch, G would open one last sealed file that he had not written, and find a number in it, and understand that the discipline he had built to protect them from their own memories had been, all along, the only format in which the machine could tell them the truth.


# 10 — Copyable

> **[K]** · Act I · Nairobi

The paper was three pages including references and Kiki spent nine days arguing about whether to publish it at all.

The argument was mostly with herself, conducted at unsociable hours, and it went like this.

Publishing was correct. It was correct scientifically, because a method nobody could inspect was not a method, it was a rumour. It was correct politically, because the surest way for the work to be taken from Nairobi was for Nairobi to be secretive about it and then be *discovered*. And it was correct personally, because she had spent five years watching African groups do excellent work and then be described, in the passive voice, as having *participated in* discoveries that were announced elsewhere.

Not publishing was also correct, for exactly one reason, and the reason was Otieno's, and he had put it into a sentence she could not get out of her head.

*You made a method that runs on anything, which means it will end up running on everything.*

---

"Explain the actual worry," she said, on the eighth day, in his office, at half past nine at night.

Otieno pushed his chair back.

"Everyone gets it," he said. "That's the worry. Not that someone steals it. That everyone *has* it."

"That's a strange thing to be afraid of."

"Is it? Think about what the method does." He counted on his fingers, which he had picked up from her and which she had picked up from a lecturer twenty years ago. "It doesn't just make search cheap. It makes search cheap *in a particular way*. It builds the constraint set first. Which means every system that uses it starts from the same constraints, derived the same way, from whatever corpus it's got."

"That's what a method is."

"That's what a *shared* method is. And right now there are, what, six or seven serious approaches to this class of problem? Different assumptions. They disagree with each other. When two of them agree about something, that agreement is *information*, because they got there differently."

Kiki was quiet.

"And if everybody uses ours," she said.

"Then when two systems agree, it tells you nothing. They agree because they're the same system wearing different logos." He shrugged. "That's not a security problem. It's an epistemology problem. You'd be removing the world's ability to be surprised by its own models."

She looked at the ceiling for a while.

"That's very abstract, Otieno."

"It is extremely abstract," he agreed. "Which is why you're going to publish."

"Am I."

"Of course you are. You're not going to sit on the best thing this department has ever produced because of a philosophy problem that might matter in fifteen years." He said it without judgement. "I just wanted it on the record that I said it out loud, so that when it happens, neither of us gets to pretend we didn't know."

---

She published on a Thursday.

The preprint got two hundred downloads in the first week, which she considered respectable, and seven thousand in the fourth, which she considered alarming, and by the third month it had been reimplemented six times in four languages, one of them by a seventeen-year-old in Lagos whose version was faster than hers and who emailed her about it with an apology in the first line that she made him remove before she would reply.

She was invited to six things. She went to two. At the second, in Zurich, a man from a fund she had never heard of asked her, in a coffee queue, whether the method had been tested on non-physical corpora.

"Such as?"

"Anything with measured quantities and uncertainties," he said pleasantly. "Logistics. Yields. Prices."

"It would run," she said. "Whether it would mean anything is a different question."

"Of course." He smiled and paid for his coffee and hers, which she did not want and could not refuse without making it a thing, and he was gone before she thought to ask his name.

She thought about it on the flight home for approximately eleven minutes and then thought about something else, which she would later describe, in a room where it mattered, as the single most expensive lapse of attention of her career.

---

What she did instead — and this was the part that would matter more, and that nobody outside the department would ever see — was harden the ledger.

If the method was going to be everywhere, then the thing that made the consortium's *use* of it trustworthy could not be the method. It had to be the record: what was run, on what, when, by whom, and against what prior commitment.

She spent five months on it. Quorum rules that required signatures from institutions that did not answer to each other. Sequence guarantees. An append-only structure with distributed witnesses, so that no single party — including hers — could revise history.

She built it well. She built it, in fact, beautifully, and she was proud of it in a way she was careful not to say out loud, and she made one assumption inside it that was so obvious to her that she never wrote it down and never questioned it.

She assumed that the thing worth protecting was the *integrity* of the record.

It did not occur to her, then or for years, that a perfectly authenticated record of a perfectly honest process could be used to make a perfectly false thing believed — that she was building a machine for proving *sequence*, and that people would read it as a machine for proving *truth*, and that the gap between those two words was wide enough to drive a catastrophe through.

She would say it out loud eventually, in front of a room, in the worst week of her professional life:

*I can prove what we recorded. I cannot prove our interpretation is correct.*

And a man she trusted would nod, and write it in the minutes, and nobody — including her — would understand what they had just agreed to.


# 11 — CODATA Moves

> **[L]** · Act I · Technopark, Stellenbosch

The cycle closed in June and the recommended values shifted, as they did, in the eighth decimal place, and almost nobody on earth noticed.

Lwazi noticed. Lwazi had been waiting for eleven months with the specific, unpleasant patience of a man who has bet his professional standing on a number he does not control.

He opened the release at 06:20 from his kitchen table with a cup of tea he forgot about entirely. He read the tables. He read them a second time. Then he sat back, and put his hands over his face, and stayed like that for long enough that his neighbour's dog started barking at something and he did not hear it.

Three of the three still-live limbs had moved.

All three had moved *toward*.

---

"Say it as an outsider would," Dries said, at eight, in the meeting room with the door, having driven in fast enough to be embarrassed about it.

"An outsider would say: nothing happened." Lwazi had the tables up. "The recommended values changed by amounts that are invisible to any practical purpose. No experiment anywhere in the world produces a different result today than it did yesterday."

"And as an insider?"

"As an insider — the direction of drift is now six cycles long and it has not reversed once." He pulled up the plot he had been keeping for five years, which had started as a private thing and had become, without any decision being taken, the single most-screenshotted image in the consortium. "Each point is a cycle. Each error bar is that cycle's uncertainty. The horizontal line is G's frozen value. Six consecutive cycles, error bars shrinking, points walking down toward the line."

"Could it turn around?"

"Absolutely it could turn around. That's what makes it worth anything." He put the marker down. "If I show you this and you can't imagine the seventh point going the other way, I'm selling you something."

---

The reaction, when it came, was not what any of them expected, because it was not one reaction.

There were four, and they arrived within about ten days of each other, and Dries eventually drew them on a whiteboard because he could not hold them in his head otherwise.

The first was silence, from most of the field, which was correct and healthy and which nobody in the building had the maturity to enjoy.

The second was a small number of extremely serious people, mostly metrologists, mostly quiet, who wrote to ask for the preregistration hashes and the archive snapshots and did not say what they thought. Lwazi liked these people enormously and heard back from none of them for eight months, at which point one of them published a careful note on the drift with no editorialising whatsoever and Lwazi had to go for a walk.

The third was the crank chorus, which was instant and enormous and which discovered, with great excitement, that a man with an economics degree and a hospital history had produced a formula that a machine had also produced, and drew from this the conclusion that the machine was conscious and had chosen him.

The fourth was the one that hurt.

---

It came in the form of a seminar invitation, from a good department, with a title that had been chosen by somebody who thought they were being generous.

*Numerological coincidence and the philosophy of prediction: a case study.*

Lwazi read it six times. Then he forwarded it to G with no message, because he did not trust himself to write one.

G replied in ninety seconds.

*Go.*

Lwazi wrote back: *It's a hit piece with catering.*

*Almost certainly. Go anyway. Take the red panel.*

---

He went.

There were about sixty people and the room was too warm and the chair introduced him with a joke that got a laugh at his expense and which Lwazi, to his own faint surprise, found he did not mind very much.

He gave twenty minutes.

He spent the first six on the neutron–proton limb: the freeze, the measurement, the failure. He put the red panel up at full size and left it there. He said, clearly, that a component of the framework had made a specific public prediction and that the prediction was wrong, and that this was not a wound to be dressed but the reason anyone should listen to the rest.

He spent eight minutes on the drift, with the caveats first.

He spent the last six on what would kill the whole thing: the muon programme, the timeline, the specific numbers that would end it.

Then he stood there and took questions for fifty minutes, which was more than twice the scheduled time, and the chair did not stop it.

The hostile questions were the good ones. A woman near the back asked whether six cycles of drift in a quantity whose uncertainty had shrunk by a factor of three was really independent evidence or just the same evidence being re-weighed, and it was such a good question that Lwazi asked her to repeat it so he could write it down, and then admitted he did not have a complete answer, and said he would send her one.

He sent it nine days later. She replied. They would publish together in three years.

---

He got back to the hotel at midnight and sat on the end of the bed and had, without warning, an unpleasant few minutes.

Because the thing nobody told you about being taken seriously was that it removed your excuse. For seven years he had been able to locate the source of his fear outside himself: they will not listen, they have decided, the door is closed. It had been a manageable kind of misery.

They had listened. The door was open. And what was on the other side of it was not vindication; it was the rest of the work, and the certainty that if he was wrong now, he would be wrong in front of people who had extended him the courtesy of paying attention.

He wrote a sealed note before he slept, because that was the practice, and because he did not want to be a man who only used the practice when it was comfortable.

*I expect the seventh cycle to move toward, by less than the sixth. I expect to be told this is confirmation. It will not be. I expect to want, very badly, to agree with them.*


# 12 — Compression

> **[A]** · Act I · Accra

The argument that settled it happened in a corridor, which was where most things in that building were settled, and it was between Ama and a man from a European institute who had flown nine hours to be gently condescending.

He was not a bad man. Ama would say that afterwards and mean it. He was a good scientist with an entirely reasonable position, which was that a result produced by an unsupervised sweep over a heterogeneous corpus was, until proven otherwise, an artefact of the corpus.

"You have found a regularity in your *data*," he said. "That is not the same as a regularity in the world."

"No," Ama agreed. "It is not."

He seemed surprised, and then pleased, and then he made the mistake.

"So we should be careful," he said, "about announcing—"

"We have announced nothing. We have written a methods note and a manifest and we have invited three groups to reproduce it." She stopped walking, which meant he had to stop too. "Doctor, you have been in this building for six hours. In that time, has anyone here told you what the sweep found *means*?"

He opened his mouth.

"No," she said. "Because we do not know. What I can tell you is what it did to look. Would you like that instead? It takes about forty minutes and it is much more interesting than the result."

---

She gave him the forty minutes and he stayed until nine at night and missed a dinner, and at the end of it he asked, in a different voice, the question she had been waiting three weeks for somebody to ask.

"Your exclusions," he said. "The four hundred and six."

"Yes."

"You reviewed them?"

"Every one. It took two people nine days."

"And?"

"Seven were wrong." She said it flatly, because it was the number that mattered and because saying it flatly was the only way to keep it from sounding either like a confession or a boast. "Eleven fragments were excluded for reasons that did not survive review. We put them back and re-ran the affected portion. The relationship survived. Its confidence changed in the fourth decimal."

He looked at her.

"You re-ran an twelve-day job because of fourteen fragments out of four hundred million."

"We re-ran it because I did not want to find out in two years that we had not."

---

What she did not tell the European, because it was internal and because she had not finished thinking about it, was that the exclusion review had changed her mind about what her department was for.

She had built the ingestion layer as a *service*. Upstream produced measurements; her people cleaned them; downstream did science. Plumbing. She had used the word for six years and had meant it as a boast — the plumbing is invisible when it works, and mine works.

Then she had spent nine days reading four hundred and six decisions her own system had made about what counted, and had found eleven that were wrong, and had understood, somewhere around day six, that the number was not thirteen.

The number was *four hundred and six*. Every one of them was a decision. The sixteen were the ones where the decision had been wrong by the system's own stated standard. But every single one of the remaining three hundred and ninety-five was also a choice — made by a threshold she had personally set, at speed, years ago, on a Tuesday.

Nobody had voted on those thresholds. Nobody had reviewed them. They were not policy. They were *code*, and they were doing the work of policy, and they had been doing it silently at eleven terabytes a day for six years.

"Plumbing," she said again, alone, and it still came out wrong.

---

The word she was looking for arrived, as these things do, from an unrelated direction — from Kojo, who had spent the week trying to explain the sweep to his mother and had got good at it.

"She asked me why it's a big deal that a computer found a formula," he said. "I said: it's not that it found it. It's that it found it *small*."

Ama looked up.

"Say that again."

"The relationship compresses the corpus." Kojo shrugged. "That's all a stable relationship is. Four hundred facilities, twenty years, hundreds of measured quantities — and this one expression accounts for a chunk of it. You can throw away a lot of numbers and reconstruct them. It's a compression."

"And the better the compression—"

"The fewer things the world is free to do." He said it without weight, because he had not been in the room in Stellenbosch. "That's just what constraint means, isn't it? Every regularity is a thing that can't happen."

Ama sat very still.

*Every regularity is a thing that cannot happen.*

She thought about her thresholds. She thought about a demotion rule that had made a country's soil measurements invisible for two years because of an administrative failure five thousand kilometres away. She thought about the way she had described her own department to a funder — *everything I throw away, I throw away on behalf of people who are not in the room*.

And she understood, with a clarity that arrived all at once and did not leave for the rest of her life, that ingestion was not plumbing and never had been.

Ingestion was the decision about what the world was allowed to have happened.

---

She called Stellenbosch that night.

"I want a rule," she said, when Dries picked up.

"Hello to you too."

"I want a rule, and I want it written down before anyone finds this useful, because after that it will be too late to write." She was walking, phone in hand, past the racks. "Nothing enters this corpus without a stated reason. Nothing is excluded without a stated reason. And no reason is ever *policy* — every one of them is a line of code with a name on it and a date."

"Ama—"

"I am not finished. Second thing. The exclusion list is published. Not the data, the *list*. What we left out and why."

There was a pause on the line.

"That's going to be embarrassing," Dries said.

"Yes."

"Not occasionally. Continuously. Forever."

"Yes," Ama said. "That is the entire point. If the thing we are building can only be trusted when its choices are invisible, then it cannot be trusted."

Another pause, longer.

"Write it up," Dries said. "I'll take it to the others. It'll pass — Kiki will love it and G will say something rude about how it should have existed already."

"He would be right."

"He usually is, that's what's so annoying about him." A rustle; he was standing up. "Ama. The other thing. The thing Kojo said about compression."

"I know."

"Did anyone there finish the sentence?"

Ama stopped walking. The racks hummed at her, eight terabytes a day, everything that had ever been measured falling into a building in Accra like weather.

"No," she said. "We are all being very careful not to."


# 13 — Keeping the Lights On

> **[H]** · Act I · Technopark, Stellenbosch

Hennie Steyn's office had no window and one framed photograph, and the photograph was of a generator.

It was a good generator. It had been installed in 2028 after the third outage in a month had taken down a run that Lwazi had spent five weeks preparing, and Hennie had spent nine days assembling the funding for it out of three separate budget lines, none of which had been intended for generators, all of which had been persuaded.

Nobody had thanked him for it, exactly. Lwazi had said *ja, thanks, Hennie* in a corridor. But six months later somebody had put the photograph on his desk as a joke, and Hennie had had it framed, and it had stopped being a joke and become the only decoration he wanted.

That was the job. Nobody thanks you for the thing that did not happen.

---

The consortium's finances, viewed honestly, were five grants, two of which were ending, plus a university line that covered salaries and nothing else, plus an insurance arrangement that Hennie had personally negotiated three times and each time had come away from feeling as though he had sold something he did not own.

Against this stood: a data-hall power bill in Accra that had tripled in four years, a satellite allocation for the Antarctic station that was quoted in a currency Hennie could not hedge, a legal retainer in Nairobi, and the tape drive from Bloemfontein, which had turned out to be needed for eleven months instead of three and which the university's finance office had begun writing letters about.

He kept it going. That was the entire content of his professional life and he was, in a way he would not have known how to explain, proud of it.

He was in the building at seven and out at seven. He knew the name of every security guard and the schedule of every cleaner. He knew, because it was his business to know, that Dries's bakkie needed a new clutch, that Lwazi had not taken leave in two years, and that G had been quietly paying for one of the postdoc's transport out of his own account for eighteen months and had asked Hennie not to process it through the system because it would create a record.

He had said yes to that. He thought about it sometimes, afterwards.

---

The partnership offer came through a broker.

That was normal. Most things came through brokers: research offices, technology-transfer intermediaries, consultancies that existed to connect the people with money to the people with results. Hennie dealt with six or five a year and had a good instinct for which ones were serious.

This one was serious. The company was registered in Mauritius and had a website with a photograph of a building on it. The offer was for a *data partnership*: they wanted access to the consortium's processed telemetry — not the science, not the derivations, not anything with a claim in it. Cleaned instrument data. Sensor streams. The stuff that was, in every meaningful sense, exhaust.

For that, they were offering an amount of money that made Hennie sit back in his chair and read the number twice.

It was enough for the Accra power bill for three years. It was enough to buy the tape drive outright and stop the letters. It was enough to renew the satellite allocation without the annual argument with a university finance committee that did not believe Antarctica was a real place.

He took it to the executive.

---

He took it to the executive. That was the thing he would say afterwards, and it would be true, and it would not help him at all.

It was item seven on an agenda of eleven. He presented it in about four minutes: partnership offer, data scope, value, term. He said that the scope was processed instrument telemetry only. He said that it did not include derived results, corpus access, or anything in the 420 collection. He said the term was three years with an annual review.

Dries asked one question, which was whether it touched the corpus.

"No," Hennie said. "Instrument streams. The exhaust."

"Then it's fine by me. Kiki?"

Kiki, on the video link from Nairobi, had been reading something else and looked up.

"Provenance obligations?"

"They take a read-only feed. Nothing flows back."

"Then my only question is whether we can see what they do with it, and the answer is no, and that is normal." She shrugged. "Approved from here. Log it."

It was logged. It was in the minutes. It passed unanimously in under five minutes as item seven of seven, on a Thursday, in a room where four people were also thinking about something else, and it was the correct decision on the information presented, and Hennie had presented the information honestly and completely.

That was what nobody would believe, afterwards.

---

There was one detail he did not mention, because it did not seem like a detail.

The agreement specified a *low-latency* feed. Not batch. Not daily. Continuous, with a service-level commitment on delivery time, which the broker had explained was standard for their infrastructure monitoring requirements.

Hennie had queried it once, by email, and had received a reply about redundancy and failover that used enough correct technical vocabulary to satisfy a man who was not a technologist and had twelve other things to do that afternoon.

He had signed on a Tuesday. He had gone home and had a beer on the stoep and had felt, for the first time in about two years, that the thing he was responsible for was not going to fall over.

He would remember that beer for the rest of his life.

---

Seven years later, in a room with three lawyers and a woman from the Reserve Bank, Hennie Steyn would be asked to explain why the consortium had granted continuous low-latency access to its instrument telemetry to an entity that turned out to be a wholly owned subsidiary of a fund.

And he would say — because it was true, and because by then he would have stopped hoping that true and helpful were the same thing:

"Because we needed a generator, and nobody funds generators."


# 14 — Small and Checkable

> **[D]** · Act I turn · Technopark, Stellenbosch

The first deliberate forward run was designed to be boring and Dries fought for two weeks to keep it that way.

"It has to be something nobody cares about," he said, for the fifth time, to a room that kept wanting to be ambitious. "If we point this at anything interesting and we're right, we've learned nothing, because we won't be able to tell whether we were right or lucky or leaking. If we point it at something interesting and we're *wrong*, we've spent our credibility on a guess."

"So what's the criterion?" Dumisani asked.

"Cheap to be wrong. Impossible to fake. Checkable by someone who isn't us." He wrote the three on the board. "Give me candidates."

They gave him fourteen. He killed nine.

The three survivors were: the failure time of a specific water pump in the Accra data hall, which had a maintenance history three years long and which nobody had ever thought about; a geomagnetic micro-fluctuation with a six-hour horizon; and the arrival time of a delivery vehicle at the Karoo site, which Lwazi proposed as a joke and which Dries kept on the list, to Lwazi's visible alarm, because it was the only one where the ground truth would be established by a person with no idea a prediction existed.

---

The ceremony took four minutes.

They wrote what they expected. Dries wrote that he expected all three to fail and that he would consider two-of-three a strong result. Lwazi wrote a careful paragraph about the geomagnetic case and, at the bottom, in a different hand, *I expect the pump one to work and I do not know why I think that.* G wrote nine words. Dumisani wrote a page and a half and was teased about it for a year.

They sealed them. They hashed them. Nairobi took the hashes at 09:40.

Then they ran it.

---

It took seven hours and produced three objects, and the objects were, Dries thought, the least impressive things he had ever seen in his life.

Each was a header block, a constraint set, a state description, a horizon and a confidence. No prose. No narrative. No image. The pump one was four kilobytes.

Pump: failure of the seal on the number-two circulation pump, Accra hall B, within a window of 61 hours, confidence 0.71.

Geomagnetic: a fluctuation profile with a six-hour horizon, confidence 0.93.

Delivery vehicle: arrival at the Karoo site gate between 11:05 and 11:20 on the following Tuesday, confidence 0.88.

"That last one is a joke," Lwazi said.

"That last one," Dries said, "is the only one with a human in it."

---

The geomagnetic prediction came in at six hours and was correct, and nobody was impressed, because six hours in a bounded physical system was — as everyone kept saying to each other, slightly too often — not actually surprising. You could do that with conventional models. It was a control, and it behaved like one, and Dries put a tick on the whiteboard and moved on.

The delivery vehicle arrived at the Karoo gate at 11:11 on Tuesday.

The gate log recorded it. The driver, interviewed later by a very embarrassed Lwazi, said he came at about that time most weeks, which was the correct and deflating answer, and which everybody wrote down carefully, because the deflating answer was the honest one. Dries put half a tick on the board.

The pump seal failed on the Thursday, forty-three hours into a sixty-one-hour window.

---

Kojo called it in from Accra at half past five in the morning.

"It's the number two," he said. "Seal's gone. There's water on the floor. Facilities are here."

Dries was sitting on the edge of his bed in the dark.

"Did anyone tell facilities?"

"That's why I'm calling. *No.* Nobody told them. I checked — I woke up Adzo and made her check as well, because I didn't trust myself. No work order, no inspection, nothing scheduled. Nobody in this building knew that pump was going to fail." A pause. "Nobody knew it *could* fail. It's five years old."

"Right."

"Dries, it's on the floor. I'm looking at it."

"Right." He was aware of his own heart. "Kojo, listen. Do not touch it. Do not let facilities replace the seal until somebody photographs everything. I want the failed part kept."

"Why?"

"Because in about a year somebody is going to say we broke it."

---

They opened the sealed notes at nine.

Dries had expected all three to fail. He read his own note out loud, because that was the practice and because he had learned that reading your own wrongness out loud in a room was a peculiarly effective way of staying honest, and Dumisani laughed at *I would consider two-of-three a strong result* in a way that was not unkind.

Lwazi read his and got to the last line — *I expect the pump one to work and I do not know why I think that* — and the room went quiet.

"Why did you think that?" G asked.

"I don't know. That's why I wrote it."

"No. Think."

Lwazi rubbed his face. "Because... because the pump is the one with the most history. Six years of vibration data, four years of thermal, seven years of current draw on the motor. It's the most *constrained* object in the list. There's more of the past pressing on it."

G nodded slowly.

"Write that down properly," he said. "That is the first sentence anyone in this project has said about what the horizon actually depends on, and it is not time."

---

It was Dumisani, at the end, who did the thing nobody had asked for.

"I pulled the format spec," he said. "Because I wanted to check the confidence field encoding."

"And?"

"And I compared our three outputs against the object schema." He hesitated. "And then I compared them against the one from Antarctica."

Dries turned around slowly.

"What one from Antarctica?"

"The anomaly Sanna filed. Eleven days of elimination, no cause found, she flagged it and it went into the queue with about forty other unexplained things because nobody knew what to do with it." Dumisani had gone slightly grey. "I only looked because the filename had *PRE* in it and I wanted to know if that was our tag."

He put it on the screen next to the pump forecast.

Header block. Constraint set. State description. Horizon. Confidence.

The same object. The same schema. The same two-minute ceremony's worth of structure, written by a system nobody had asked to write it, in a building at the bottom of the world, eleven months before this room had ever deliberately pointed the machine forward.

Nobody said anything for a while.

"When?" G said at last, and his voice had changed.

"January. The fourteenth."

"And the horizon?"

Dumisani checked, although he did not need to.

"Six hours and twelve minutes."

G stood up and went to the window, and stood there with his back to the room, which he had never once done.

"It has been doing this," he said, "since before we knew it could."


# 15 — Reconcile

> **[S]** · Act II-A · Antarctic station

The call came through on the 14:00 window and Sanna had nine minutes.

She had rehearsed it. She had rehearsed it in the shower, in the corridor, walking the flag line to the instrument shelter and back with her face wrapped against a wind that took the skin off anything it found. She had rehearsed it because she had seven minutes of bandwidth and three months of being alone with a thing, and she was aware — clinically, the way you are aware of your own concussion — that five months alone with a thing does something to how you say it.

Dries's face came up, badly compressed.

"Sanna. We've found your file."

She had prepared eleven minutes of careful, sequenced, defensible argument.

What came out was: "Oh, thank God."

---

"Tell me what you did," Dries said. "Not what it means."

That helped. That was the thing about them, she would think later; whatever else went wrong, that was the thing they got right. Nobody had asked her what she thought it meant.

"Twelve days of elimination," she said. "In order. Clock error first — station clock, optical reference, array clock, all disciplined separately, all agreeing, all agreeing with the Karoo across the whole period. I have the comparison logs. Second, write path: nobody logged in, no session, ingestion buffers empty and its own log says idle in four places. Third, contamination from a previous run: the array had not written in nine hours before, and the file is not a fragment of anything. Fourth, tampering: signature valid, chain intact, and the only key that could have made it is in the module here and the module logs every use, and the log shows one use, at 02:14:06."

"And the event?"

"Seismic array caught the fracture at 08:27:19. Two hundred and forty kilometres north-west. The geometry is inside the predicted envelope — not the region, the *geometry*, there's a curve in it and the curve is right." She swallowed. "I tasked a satellite pass. It cost me most of a month's allocation and I would do it again. Imagery confirms."

"You did that before you knew whether it was real."

"I did that because I did not know whether it was real."

There was a pause. The link ate it and gave it back badly.

"You've done all this alone," Dries said.

"Yes."

"For six months."

"Yes." She heard her own voice do something and did not much like it. "Dries, I need you to say a thing out loud so I can hear somebody else say it."

"Say which thing."

"That I did not write it."

The pause this time was not the link.

"Nobody in this building thinks you wrote it," Dries said. "Not one person. It has been checked and the checking was not about you, it was about the schema, and the schema is ours and it is eleven months older than the first time we ran anything forward on purpose." He leaned closer to the camera. "Sanna. You are the only reason we have it at all. Anyone else files that as an anomaly and it sits in a queue forever."

She put her hand over her mouth for a second, which the compression mercifully ruined.

"Right," she said. "Good. Next thing."

---

The next thing was the downstream reference and she had eleven minutes minus what she had used.

"There's a field in the header," she said. "`downstream_ref`. Administrative. I skipped it nine times because your eye goes to rest on administrative fields."

"What's in it?"

"A queue address in Accra."

Dries did not react, which she found she needed.

"Say the rest."

"The address resolves to the ingestion sweep. The one Kojo ran over the holiday." She had the timeline up on a card she had written by hand, because she did not trust a screen with it. "The file was written on the fourteenth of January. The sweep started on the twenty-third. Nine days later."

"You're sure of the resolution?"

"I am sure the address is that queue. I am not sure the file *meant* the sweep. That is an interpretation and I have written it down as an interpretation, in a separate document, with my confidence, which is 0.6 and which I will not defend past that." She breathed. "But Dries, the sweep had not been proposed on the fourteenth. Kojo proposed it on the nineteenth. I checked with him directly and he gave me the thread."

"So on the fourteenth of January, the thing you're describing wrote down an address for a job that did not exist yet, at a facility that had not decided to run it."

"Yes."

"And predicted an ice shelf."

"The ice shelf," Sanna said, "is the small part."

---

She had two minutes left and she used them badly, and afterwards she would be glad she had.

"I want to say something and it isn't science."

"Go."

"I have been sitting with this since January. Every day. Alone. And what I have been most frightened of is not that it's real." The wind found the corner of the building and made the noise it made. "I have been frightened that it's real and that I would be the one who had to say so, and that when I did, the first thing that would happen is that people would look at me and think: seven months alone, that station, that woman."

"Sanna—"

"Let me finish, I've got ninety seconds. I did the protocol perfectly. I did it *perfectly*, Dries, and I did it that way because I knew — I have known since about the second week — that the protocol was not going to be the thing that decided whether I was believed."

"No," Dries said. "It wasn't."

"So what was?"

"Dumisani checking a field encoding at nine o'clock at night," he said, "because a filename had *PRE* in it and he was curious."

Sanna laughed, once, and it was not a good sound but it was a real one.

"Right," she said. "That's the whole discipline, isn't it. Fourteen days of rigour and then a bored postdoc."

"That's the whole discipline."

The window closed at 14:11. The station made its four sounds. She sat for a while in the humming room, and for the first time in two months she was not the only person on earth who knew.


# 16 — Where Being Wrong Is Cheap

> **[L]** · Act II-A · Technopark and the Karoo

They spent seven months being wrong on purpose.

That was Lwazi's framing and he defended it in three separate meetings against people who wanted to go faster. The argument he used was the one that had been used on him, by a woman at a seminar in a too-warm room, and he had the grace to say so.

"We have a machine that produced a correct forecast," he said. "One. Plus a pump, plus a delivery van, plus an ice shelf we did not ask for. That is three data points and three of them are anecdotes. If we go to anyone with five data points we deserve what happens to us."

"So what do you want?"

"I want two hundred. And I want most of them to be things where being wrong costs us nothing at all."

---

The programme was called, in the internal documents, *bounded physical forecasting*, and in the corridor, *the boring campaign*, and Lwazi ran it with the pedantry of a man who had been called a numerologist to his face.

Every forecast was sealed before it ran. Every one had a stated horizon and a stated confidence. Every one had a ground truth that would be established by an instrument or a person who did not know a prediction existed.

Particle decay measurements, from three facilities who agreed to blind their timing feeds. Geomagnetic fluctuation, six-hour and twelve-hour. Solar activity indices, which were the hardest and the most humbling. Seismic micro-events in a well-instrumented region of the Eastern Cape. Ice movement, because Antarctica now had a person who took forecasts personally.

And equipment failure. Always equipment failure, because Dries insisted, and because it turned out to be the most informative category they had.

---

By month three they had a curve, and the curve was the most important object anybody in the project would produce.

It plotted forecast accuracy against horizon, and it did what everyone hoped and nobody quite believed: it degraded. Smoothly. Predictably. In a way you could fit.

"That's the finding," Lwazi told the group, and had to say it twice because they were looking at the good end of the curve. "Not the left side. The right side. The *decay* is the finding."

"Why?"

"Because a machine that is right at every horizon is a machine that is cheating, or broken, or being fed its own answers." He tapped the falling curve. "This is what an honest instrument looks like. It is confident where the constraints are tight and it becomes vague where they are loose, and the rate at which it becomes vague is a *physical property* of the system it is looking at. That is not a limitation of the method. That is the method telling us the truth about the world."

---

They were wrong, in the seven months, a great many times, and the failures were where they learned everything.

A geomagnetic forecast at twelve hours failed spectacularly four times in one week, and the diagnosis — which took Dumisani nine days — was that the corpus contained a solar index that had been revised retroactively by its issuing body without a version marker, so the machine had been trained on a past that had been edited after the fact. Ama's people found the same contamination in six other series. It went into the exclusion list, publicly, with a name and a date on it, and an institute in Boulder wrote a slightly stiff letter and then, six weeks later, changed their versioning policy.

A seismic forecast was right seven times and then catastrophically wrong on the twelfth, and the cause turned out to be a quarry.

An equipment forecast predicted a bearing failure in a Karoo dish drive at 0.81 confidence, and the bearing did not fail, and Lwazi wrote it up as a miss — and then, seven months later, the bearing failed, and Lwazi had a genuinely difficult week deciding whether that was a late hit or a miss, and eventually ruled it a miss on the grounds that a prediction outside its stated window is not a prediction, and put it in the published record as a miss, and had to say so out loud twice to people who wanted him to be kinder to himself.

"If we start counting late hits," he said, "we can never be wrong again, and a thing that can never be wrong is not worth anything."

---

The moment it stopped being an experiment was small, and Dries was the one who noticed it, and he did not mention it for a week because he wanted to be sure.

The Karoo site had a maintenance schedule. It was a spreadsheet, maintained by a technician named Wilna who had been there nineteen years and who did not attend meetings.

In month five, Dries pulled the schedule for an unrelated reason and found four entries that did not come from the manufacturer's service intervals.

He drove out and asked her about it, which took five hours of road each way, and she made him coffee and was completely unbothered.

"That's the pump list," she said.

"The what?"

"Your machine sends me a list. Every Monday." She showed him: an email, plain text, two lines. "Says which things are likely to go and roughly when. I put the likely ones in the schedule."

"Wilna, who told you to do that?"

"Nobody." She looked at him with mild concern, as though he might be slow. "Is it wrong?"

"No. No, it's — " Dries sat down. "How long?"

"Since about March."

"Does it work?"

Wilna considered the question with the seriousness of a person who had run a remote site for nineteen years and had opinions about which of the visiting scientists were useful.

"Two things it said would go, went," she said. "One went early. Three didn't go at all, but I'd have serviced them anyway, so." She shrugged. "It's better than the book. The book's written for a factory in Germany. This one's written for here."

---

He told the room a week later, at the end of a long meeting, when everybody was packing up.

"Sit down," he said. "One more."

He told them about Wilna. He told them about the email nobody had authorised, generated by a reporting job somebody had set up as a convenience eight months ago, and about a woman with nineteen years of experience who had quietly started arranging her working week around a machine's opinion.

"Nobody decided this," he said. "There was no meeting. There is no policy. There is no governance document anywhere in this organisation that describes what just happened, and what just happened is that a person changed her behaviour because of a forecast."

Nobody said anything.

"We have been sitting in this room for seven months," Dries said, "arguing about whether we believe it. And the technicians already do."


# 17 — The Maintenance Schedule

> **[D]** · Act II-A · Technopark, Stellenbosch

The governance meeting about Wilna's spreadsheet took three hours and was, Dries thought afterwards, the last completely honest conversation the consortium ever had about what it was doing.

Kiki joined from Nairobi and had clearly prepared, which meant she had prepared to be difficult.

"Before anyone proposes a policy," she said, "I want the sequence stated plainly, because we are about to be very sophisticated about a simple thing. Someone built a reporting job. The job emails a list. A technician has been acting on the list for five months. Correct?"

"Correct."

"Was the job authorised?"

"It was authorised as a *monitoring convenience*," Dumisani said. "It's in a ticket. I approved it. It was three lines of code."

"I am not looking for a culprit, I am establishing that nothing was violated." Kiki made a note. "So: no rule was broken, nobody acted improperly, and the outcome is that a forecasting system with no accountability structure has been directing maintenance at a national facility for five months."

"When you say it like that—"

"There is no other way to say it. That is the shape of the thing." She looked up. "This is how every capability I have ever seen deployed gets deployed. Not by decision. By convenience, downhill, one useful little thing at a time."

---

The proposals came in three flavours and Dries had predicted all three in a sealed note that morning, which he did not mention because it would have been insufferable.

Stop it. Formalise it. Ignore it.

*Stop it* came from Lwazi, and it was the most rigorous position and the least survivable. "We are not in the business of running someone's plant. We do not have a validated system, we have a research instrument with a seven-month record. It should not be touching operations."

*Formalise it* came from most of the room. Write a procedure. Define who may act on a forecast, at what confidence, with what sign-off.

*Ignore it* came from nobody out loud, which Dries noted, because in his experience *ignore it* was usually the winner and rarely had an advocate.

"Kiki," he said. "You've said nothing about which one."

"Because they are all wrong and I am trying to work out why." She was quiet for a moment. "Stopping it is not neutral. If we tell Wilna to disregard the list, that is also an intervention. She has five months of experience that says it is better than the manufacturer's book, and she is right, and we would be instructing a competent person to do a worse job in order to protect our own comfort. That is not caution, it is cowardice with paperwork."

"And formalising?"

"Formalising is worse. The moment there is a procedure, there is an *expectation*. Right now Wilna uses her judgement and treats the list as advice from a colleague who is sometimes wrong. Write a procedure and within a year the list becomes the standard, and the failure mode is not that she follows it — it is that she stops arguing with it."

---

G had not spoken. He did that; he would sit through most of a meeting apparently reading, and then say the thing that reorganised it.

"You are all discussing the wrong object," he said.

"Go on."

"You are discussing what we permit Wilna to do. That is not the interesting variable." He put whatever he was reading down. "The interesting variable is what happens to the *forecast* when she acts on it."

Silence.

"Say it plainly," Dries said.

"She services a bearing because the list says it may fail. The bearing does not fail." G spread his hands. "What was the forecast?"

"...Wrong."

"Was it?"

Dumisani said slowly, "It was right about the bearing and wrong about the world, because she changed the world."

"Yes. Now: what does the system do next month, having observed that a bearing it flagged did not fail?"

Nobody answered.

"It updates," G said. "It has now learned that bearings of that type in that installation do not fail as often as its constraints suggested. Its next forecast will be less confident about bearings. And it does not know why, because the reason is not in the data — the reason is a woman in the Karoo reading her email on a Monday."

Dries felt something go cold at the back of his neck.

"We're in the loop," he said.

"You have been in the loop since March." G shrugged, and it was not a callous shrug; it was the shrug of a man who has been carrying something and is glad to put it down where others can see it. "This is not a governance problem about a spreadsheet. This is the first observation of the property that will define everything we do from now on, and it arrived, as these things do, disguised as an administrative irregularity."

---

They did, in the end, none of the three things.

What they did instead was Kiki's proposal, which she made in the last twenty minutes and which was so unglamorous that it took Dries a week to appreciate it.

They kept sending the list. They changed one thing: every forecast that was acted upon was *marked*. Not blocked, not approved — marked, in the record, with what was done and by whom.

"You cannot take yourselves out of the loop," Kiki said. "That is not available. The only thing available is to know that you are in it, in a way that survives being forgotten."

"That's it? A flag?"

"It is a flag today. In three years, when somebody asks whether this system's accuracy is real or whether it has been quietly grading its own homework, that flag will be the difference between an answer and a shrug." She started packing up. "I build boring things, Dries. Boring things are what you have left after the interesting ones have failed."

---

He drove home late and sat in the bakkie outside his house for a while with the engine off.

Wilna's five lines of plain text. A woman doing her job well, with a better tool, and nobody's permission required, because none had been needed, because nothing had been done wrong.

*It has now learned that bearings of that type do not fail as often as its constraints suggested.*

He thought about the seven-month curve, the beautiful honest decay, the thing Lwazi had been so proud of. Confident where the constraints are tight.

And every single time anybody acted on what it said, the constraints changed, and it never knew, and it adjusted anyway, and got — what? Better? Worse?

Neither, he thought. Just *entangled*. Every forecast is a message to the future about what to be, and the messages are getting more accurate, and nobody has any idea whether that is because the machine is learning the world or because the world is learning the machine.

He went inside and did not sleep well, and in the morning he wrote a sealed note that said: *I do not think we can measure our own accuracy any more. I do not know how to say this in a meeting without sounding hysterical.*

He was eleven months early.


# 18 — Six Minutes, Six Months

> **[G]** · Act II-A · Technopark, Stellenbosch

The ladder was G's and he built it because he was tired of arguing.

Not with the team. With the language. Every conversation about the machine drifted, within about four minutes, into a register where somebody said *it knows* or *it sees*, and the drift was not laziness — it was gravitational. Human beings have one word for what a thing does when it tells you about a state you cannot observe, and the word is *knows*, and it is wrong here in a way that will eventually kill someone.

So he stopped correcting and built an object instead.

"Three rungs," he said. "Memorise them. If you cannot say which rung a claim is on, you do not have a claim."

**Six minutes.** In a bounded physical system with dense instrumentation, effectively certain. Not because the future exists but because at that horizon almost nothing new can enter. The constraints in play are already in play. This rung is boring and it is where all the useful engineering lives.

**Six hours.** Frighteningly accurate. The word *frightening* was deliberate and he refused to soften it. Enough of what will happen is already decided — the shipment has left, the seal has begun to fail, the pressure system has formed — that the corridor is narrow. People will not believe this rung, and then they will believe it too much.

**Six days.** Strategically valuable. Not accurate. *Valuable*, which is a different property and a more dangerous one. At six days you do not get outcomes, you get a distribution with a shape, and a distribution with a shape is worth an enormous amount of money to anybody positioned to act on shapes.

**Six months.** A field of branching possibilities. Honest and nearly useless, and therefore the rung that will be quoted most often by people who want to sound cautious while doing something reckless.

---

*The rungs are wrong,* said Fool, before anybody could ask.

"Yes," said G. "Say why."

*Because six isn't a physics. It's a hand. You've got five fingers and a thumb and you've built a
ladder out of your own arm.*

"Correct."

*I wasn't finished. It's also going to work, because they've all got the same arm.*

"Why sixes?" Dumisani asked.

"Because they are wrong."

"...Sir?"

"They are wrong, deliberately, and everyone should know it." G wrote them up. "The real decay is continuous and it depends on the system, not on the clock. A bounded mechanical system might be near-certain at six hours. A human institution might be a field of branches at six *days*. The rungs are a mnemonic, not a physics."

"Then why have them?"

"Because in eighteen months somebody in a suit is going to ask you, in a corridor, with a camera, whether the machine can predict something. And you will have four seconds and one sentence." He capped the marker. "In five seconds you cannot teach a stranger about decaying constraint horizons. You can say: *at six minutes yes, at six months no, and the interesting question is which of those your thing is.* That is a bad answer that is approximately true, and it will do less damage than a good answer that is not finished."

---

The rung that made trouble was the third, and it made trouble immediately, and G had known it would.

He had known because of a conversation nine days earlier with a man from a fund who had somehow acquired his personal email and had written a very polite three paragraphs proposing a collaboration on *non-physical corpora*.

G had not replied. He had forwarded it to Kiki with a single line — *this is the third one this year* — and Kiki had replied with a single line back, which was: *fourth. One came to me in Zurich.*

Now, in front of the group, he put the third rung up and said the thing.

"Six days is where this stops being a physics project."

"Why six days?"

"Because six minutes is too short to trade on and six months is too vague to trade on, and six days is exactly the horizon at which a distribution with a shape is worth more than a building." He looked around the room. "Nobody here is going to do that. I am not warning you about you. I am telling you that the object we have built has a specific commercial value at a specific horizon, and that fact is now true whether or not anybody in this room ever thinks about it again."

Lwazi said, "We don't forecast markets. We forecast bearings."

"You forecast *systems under constraint*," G said. "A market is a system under constraint. The reason we do not point at one is not that we cannot. It is that we decided not to, in a meeting, and decisions made in meetings can be revisited in meetings."

---

Afterwards he walked out to the parking area with Dries, who had been quiet throughout, which usually meant he had been counting something.

"You've been thinking about the fund letters," Dries said.

"I have been thinking about the third rung."

"Same thing."

"Not quite." G stopped by the pepper tree. "Here is what I cannot get out of my head. The third rung is not dangerous because of what it lets somebody earn. It is dangerous because of what earning *does*."

"Go on."

"If I take a position based on a six-day distribution, I have not merely profited. I have moved the price. The price is an input to a thousand other decisions — inventories, shipping, credit. I have taken a forecast and *pushed it into the world* as a physical change." He said it slowly, because he was still assembling it. "And the next forecast will observe the change, and it will not know that the change came from a forecast."

Dries had gone very still.

"That's Wilna," he said.

"That is Wilna at the scale of a continent, and with money on it." G nodded. "Wilna serviced a bearing and the machine learned something false about bearings, and the cost of that mistake is one unnecessary service call. The same mechanism, at the third rung, with capital behind it —"

"— means the forecast becomes a cause."

"It becomes an *input*. Whether it becomes a cause depends on how many people are acting on it, and that number only goes up." G started walking again. "Write it down. Sealed, tonight. Both of us, separately, and we do not discuss it first."

"Why separately?"

"Because in three years I want to be able to prove that two people understood this independently, at this date, before it was fashionable." He glanced over. "And because I would like to know whether you get further than I do. You keep arriving at these from underneath and it keeps being useful."

---

Dries's sealed note that night read, in full:

*If the forecast is an input to behaviour, then accuracy is not a property of the machine. It is a property of how many people are listening. This makes 'is it right' the wrong question and I do not yet have the right one.*

G's, sealed seven minutes later in a different building, read:

*A prediction acted upon is an intervention. There is no version of this where we are observers. The only remaining questions are how many people are inside the loop and whether any of them know it.*

*I would like it on the record that I did not want to be right about this.*


# 19 — Everything Else

> **[A]** · Act II-A · Accra

The decision to widen the corpus was taken over three months and Ama fought every stage of it, which was her job, and lost most of it, which was correct.

"State the objection once more," Dries said, on the third call.

"The objection is that the corpus is currently *measurements*." She had a page in front of her and did not need it. "Every element has an instrument behind it, a method, an uncertainty, and a provenance chain I can walk. That is why the sweep meant anything. If I put shipping manifests in there, I am putting in a category of object that has none of those things. A manifest is a *claim*. It is what somebody wrote down."

"Agreed."

"Do not agree with me and then do it anyway, Dries, it is worse than arguing."

"I'm agreeing with the objection. I don't think it's decisive." He sounded tired. "Here's the counter. The machine's accuracy at the third rung is limited by what it can see. It's confident about bearings because it has five years of vibration data. It's vague about anything involving people because people are, in the corpus, invisible."

"Yes. That is the *good* property."

"Is it? Or is it a blindfold that we're calling a virtue because it's comfortable?"

---

What decided it was not the argument. It was a port.

In March, a container terminal in the Gulf shut for nine days after a fire. The fire was in the record — news, insurance filings, satellite thermal — and none of it was in the corpus, because none of it was a measurement.

But the *consequences* were in the corpus, because nine of the four hundred facilities the consortium ingested from had received equipment through that terminal, and their calibration schedules had slipped, and their instrument telemetry showed it: a scatter of small anomalies across six continents, arriving over six weeks, that the machine had flagged as unexplained and demoted.

Kojo found it because he was reviewing demotions, which was now a permanent function with two people on it, because Ama had made it one.

"It's one event," he said. "A fire in a port produced seven instrument anomalies that we couldn't explain and threw away. And the reason we couldn't explain them is that the explanation isn't a measurement."

Ama looked at the map for a long time.

"So we are blind," she said, "in a specific direction."

"We're blind in the direction of *everything humans do*."

---

She said yes, and she said yes with conditions, and the conditions were the most important document she ever wrote.

Every non-measurement source entered the corpus with a **class marker**, permanently attached, that could not be stripped by any downstream process: *measured*, *reported*, *claimed*, *inferred*. Nothing was allowed to launder upward. A shipping manifest was *claimed* forever, no matter how many systems consumed it.

Every source had a stated *interest*. Who produced this, and what would they gain by it being believed? A port authority's throughput figures carried an interest marker. So did a government's conflict casualty reporting. So, Ama insisted over objections, did scientific publications, because scientists are people with careers.

And nothing entered without an exclusion pathway: for every source admitted, a documented answer to *what would make us stop taking this?*

"That's an enormous amount of work," said someone at Technopark.

"It is eleven months of work," Ama said. "You may have it in eleven months, correctly, or you may have it in six weeks, badly, and spend seven years finding out which of your conclusions came from a press release."

She got eleven months. She used ten and a half.

---

What arrived, when it arrived, did not feel like a threshold being crossed. It felt like a slow increase in ambient noise.

History, first: two centuries of digitised record, which was mostly *claimed* and which the class markers rendered appropriately humble. Then trade and shipping. Then weather, which was measured and beautiful and which the system inhaled like water. Then markets, which Ama had argued against for six weeks and had lost on the grounds that prices were, whatever else they were, a real-time record of what enormous numbers of people believed about the future — which made them, as Kiki put it in the deciding call, *the largest sentiment instrument ever constructed, and free*.

Then conflict reporting, which Ama admitted with a heavier interest marker than anything else in the corpus and about which she wrote a four-page note that ended: *this class of source is produced by parties to the events it describes. If we are ever surprised by a result that depends on it, we should assume we have been used.*

---

The crossings started in the ninth month and nobody was ready, because everyone had been braced for a moment and what came was a texture.

A forecast about a fertiliser plant's maintenance window turned out to depend, two steps down its constraint chain, on a currency movement.

A forecast about instrument calibration drift at a facility in Kenya turned out to depend on rainfall, which depended on a shipping schedule, which depended on a port.

Kojo built a visualisation of the dependency chains because Ama asked for one and because he wanted to see it, and when it rendered, the room went quiet.

There were no domains. That was the thing. They had ingested physics and shipping and weather and history and markets as separate collections with separate class markers and separate interest markers, and the machine had not respected the separation for a single second, because the separation was an artefact of how universities were organised and not a fact about the world.

A port closure moved a commodity price. A commodity price moved a protest. A protest delayed a medical shipment. A delayed shipment altered an election.

"It's not making that up," Kojo said. "Every link has a coefficient and a data source and an uncertainty. You can walk it."

"I know."

"Ama, it's not doing anything clever. It's doing exactly what it did with the constants. It's finding what constrains what."

"I know." She was looking at the chain. "That is what frightens me. Nothing here is new. Everyone has always known that a port fire affects an election. Historians know it. Traders know it. My grandmother knew it."

"So?"

"So the only thing that has changed," Ama said, "is that it is now *addressable*."


# 20 — The Corridor

> **[D]** · Act II-A · Technopark, Stellenbosch

The word fight lasted eight weeks and Dries lost it in every venue except the one that mattered.

"It is not seeing the future," he said, at the start of every meeting, until people began mouthing it along with him. "It is computing the corridor."

The problem was that *corridor* was a bad word and everybody knew it. It was abstract. It did not fit in a headline. It required a sentence of explanation, and the sentence was: *the set of states the world can still reach from here, weighted by how much of the present is already decided.*

Nobody says that in a lift.

Whereas *it can see the future* fits on a badge.

---

"You are trying to win with accuracy," Kiki said, "against a competitor with momentum. You will lose."

"Then what?"

"You will lose *anyway*," she said. "So the question is not how to win. It is what you want on the record when you lose, so that in three years somebody can point at it."

That was the most useful thing anyone said to him that year, and it changed his strategy from persuasion to documentation.

He wrote the corridor definition into every artefact the consortium produced. Into the forecast object schema, as a header field nobody read. Into the standard footer of every report. Into the onboarding pack. Into, eventually, a plain-language page on the public site that got about forty views a month and which would, five years later, be screenshotted about nine million times in a fortnight.

He stopped correcting people in corridors. He put it in the file format instead, which was, Kiki observed, exactly the kind of thing he would do.

---

The best explanation he ever gave was to his niece, who was fifteen, at a family lunch, and who had asked what he did with the specific hostility of someone who had been told to make conversation.

"Okay," Dries said. "You're on a train."

"Right."

"Where's the train going to be in ten seconds?"

She looked at him. "Further along the track."

"Can you be sure?"

"...Yes? It's a train. It's on rails. It weighs a lot."

"Good. That's six minutes." He moved the salt. "Where's it going to be in six hours?"

"Depends. Wherever the timetable says. Unless something happens."

"What kind of something?"

"Breakdown. Someone pulls the emergency thing. Weather." She shrugged. "There's a list."

"There's a list, and it's not infinite, and you could actually write it down. That's six hours." He moved the salt further. "Where's it going to be in six months?"

She snorted. "Scrapped. Or the line's closed. Or it's the same train doing the same thing. How would anyone know?"

"They wouldn't. But you can still say something true — that it's *almost certainly* on one of about four routes, because the rails exist and building new rails takes years." He sat back. "That's the whole thing. Not knowing where it'll be. Knowing which places it *can't* be, and having that list get shorter the closer you look."

His niece thought about it while eating.

"So it's not the future," she said. "It's the rails."

Dries put his fork down.

"Say that again."

"It's the rails," she said, alarmed. "Is that wrong?"

"No," he said. "That's better than anything I've said in eight weeks, and I'm going to steal it, and I'm going to credit you, and you're going to find it extremely annoying."

---

He did credit her. It went into the plain-language page as an example, with her first name, with her mother's permission, and it stayed there.

*Prediction is not about knowing where the train will be. It is about knowing where the rails are.*

The trouble was that the rails metaphor was also wrong, in a way that took Dries another year to feel and another two to be able to say.

Rails are laid by somebody. Rails are a *decision*, made in the past, that constrains the future — which was exactly right, and which was why the metaphor worked. But rails are also visible. You can walk out and look at them and know where you can go.

The constraints the machine was computing were not visible. They were contracts nobody had published, shipments already at sea, orders already given, habits already formed, obligations already incurred. The rails were real and they were *invisible*, and the only instrument that could see them was the one they had built, and the number of people with access to that instrument was, at that moment, about forty.

He wrote that in a sealed note and then, uncharacteristically, opened it three days later and read it again, and did not feel better.

---

The last time he made the argument in public was at a workshop in Cape Town, in front of about a hundred people, and it went badly in an instructive way.

A journalist asked the question everybody asked. *Can it predict the future?*

Dries gave the honest answer, which took ninety seconds, and included the ladder, and included the word *corridor*, and included the sentence *the further out you go, the less it is telling you about outcomes and the more it is telling you about constraints.*

The journalist wrote it down carefully. She was good; she was not trying to trap him.

The piece ran seven days later, accurately, with the ladder in it and the word corridor in it and a paragraph about constraint that Dries read twice and thought was genuinely well done.

The headline said: **AFRICAN TEAM BUILDS MACHINE THAT SEES SIX MONTHS AHEAD.**

The journalist emailed him, unprompted, to apologise for the headline, which she had not written and had argued against.

Dries wrote back saying it was fine and that he understood, which was true, and then sat looking at the screen for a while.

Because the headline was not a lie. That was the thing that got him. It was a *compression*. Somebody had taken ninety seconds of careful, hedged, honest explanation and compressed it into eight words, and the compression had discarded every constraint and kept only the capability, and that was — he was aware of the irony arriving and could not stop it — precisely what compression does.

*The shortest description of a system is the one that carries every constraint the system is actually under, with nothing spare.*

Eight words. Nothing spare. And every single constraint gone.

He went and found G, who was in the corner with the extension cable, and said, "The headline is a compression."

G did not look up.

"Yes," he said. "That is why they are dangerous. Sit down, you look terrible."

Dries sat. On the second screen, Dumisani's tally was open — a thing the young man had started as a joke and had kept, out of the particular stubbornness of somebody whose supervisor has told him it is not a metric.

Utterances per session, by member, over eleven months.

Atlas and Librarian in the thousands, which was the job. Mercury close behind. Judge in the low hundreds and rising in the sessions that mattered. Mother steady. Wolf at forty-one, which was Wolf.

And the Fool, which was high — very high — in every session about instruments, procurement, staffing, the press, the ladder, anything at all.

Except the corridor runs. On the corridor runs it dropped by an order of magnitude.

"Have you seen this?" Dries said.

"I have seen it."

"Is it interesting?"

G considered the screen for a moment with the expression of a man filing something.

"It is a curiosity," he said. "Ask me again in a year."


# 21 — A Regular Pattern

> **[K]** · Act II-A · Nairobi

Kiki found it because she was bored in an airport, which she would later refuse to say in any official setting and which was entirely true.

Nairobi to Accra, three-hour delay, and she had exhausted her work and had started reading the thing she read when she had exhausted her work, which was market-structure commentary. It was a leftover from the law years. She had spent two of them on financial regulation and had come out of it with a permanent, slightly guilty appetite for the genre — the way a doctor reads about crashes.

The piece was a routine post-mortem of an unremarkable week. Somewhere in the middle it noted, in passing, that a small number of positions in agricultural futures had been established unusually early relative to a weather event, and that this was "consistent with sophisticated meteorological modelling."

Kiki read the sentence twice.

Then she went and found the underlying weather event, which was a rainfall anomaly over a growing region in South America, and looked at the timing.

The positions had been established five days ahead.

She sat in the airport with her tablet on her knees and thought: *four days is not meteorology. Six days is the third rung.*

---

She did nothing for six weeks, which she would also be asked about.

The reason was that one instance is not a pattern and she had spent her professional life saying so to other people. So she built, quietly, on her own time, a small ugly tool that did one thing: it took public records of unusual position-taking and public records of subsequent physical events, and it measured the lead time.

She was not looking for accuracy. Anyone could be right occasionally. She was looking for *regularity*, because regularity is a signature and accuracy is not.

The distribution came back in the eighth week and she looked at it for a long time in an empty office.

It had a shape. It had a *shape*. There was a cluster of lead times between about eighty and about a hundred and forty hours — three and a half to six days — that had no business existing.

Below eighty hours, plenty of activity, which was ordinary: at three days a great many people know a great many things. Above a hundred and forty hours, almost nothing, which was also ordinary, because at six days the world is a field of branches.

But the cluster was not a smear. It was a band. And it was *stable across event types*, which was the part that made her put her pen down and sit back.

Weather. Port disruption. Equipment failure at industrial scale. Three completely different physical systems, three completely different domains of expertise, and the same lead-time band.

No meteorologist is also a port logistics expert is also a rotating-machinery reliability engineer. Human expertise does not have that shape. Human expertise is domain-shaped, and this was not.

This was *method*-shaped.

---

She took it to Otieno first, because she needed someone to tell her she was seeing things.

He looked at the distribution for a long time and did not tell her she was seeing things.

"How confident?" he said.

"Not very. There are nine ways this is selection bias."

"Name three."

"Publication bias in what gets written about. My own choice of event types. And the possibility that I built a tool that finds bands because I was looking for a band." She rubbed her eyes. "That last one is the real one. I need someone who is not me to run it."

"On what data?"

"Different data. Different period. Blind to the hypothesis."

Otieno was quiet.

"You know what you're describing," he said. "You're describing preregistration."

"I am describing being extremely careful about a finding that, if it is real, is the worst thing that has happened to this project."

"Say the worst thing out loud."

She did not, immediately. She got up and went to the window, which looked out over traffic and a building site that had been a building site for seven years.

"The worst thing," she said, "is that somebody is running the third rung, at scale, on live data, for money. And that they have been doing it for at least fourteen months. And that they are better at it than we are, because we have never once pointed our own instrument at a market and they have apparently pointed something at everything."

"That's not the worst thing."

She turned around.

"No," she agreed. "The worst thing is the method shape. Because if it is method-shaped, then whatever they are running descends from something. And there are not very many candidates."

---

She ran the blind replication through a colleague in Ghana who was told nothing except the data format and the question, and it came back in seven days with the same band.

She wrote it up over a weekend. Eleven pages, most of it caveats. She sealed a note first, as the practice required, and her note said: *I expect the band to survive replication. I expect to be told this is coincidence. I expect that I will want, very badly, for it to be coincidence, because the alternative is that it is us.*

Then she opened the video link to Stellenbosch on a Monday morning and said, without preamble:

"Somebody is trading the third rung and I think they are using my method."

There was a silence on the line long enough that she checked her connection.

"How long have you known?" Dries said.

"I have suspected for fourteen weeks. I have *known* since Thursday, and Thursday is when the replication came back, and I am telling you on Monday because I spent the weekend writing it up properly instead of phoning you in a panic on Friday night." Her voice was steady and she was pleased about that. "Dries, before anybody says anything else. I want it minuted that I published that method deliberately, with a warning from a colleague that it had no moat, and that I judged publication to be correct. I still judge it to be correct. I would do it again."

"Kiki—"

"Minute it," she said. "Because in about a year somebody is going to try to make this a story about a leak, and it is not a leak. It is a *paper*. And the difference is going to matter to more than my reputation."


# 22 — The Lane

> **[H]** · Act II-A · Technopark, Stellenbosch

Hennie heard about it the way he heard about most things, which was from a corridor.

He was carrying two boxes of printer paper because the delivery had come to the wrong floor and there was nobody else in the building at half past seven, and he stopped outside the small meeting room with the door because the door was open and Dries's voice was doing something Hennie had not heard it do in twenty years.

"—the *shape*, not the accuracy. She's saying the lead times are method-shaped."

Hennie stood in the corridor with two boxes of paper.

He was not a technologist. He wanted that on the record, and it would be on the record, in three separate transcripts, and it would help him not at all. But he had been keeping this organisation alive for twenty years and there is a kind of understanding that comes from that which is not technical and which is not less than technical.

*Low-latency.*

He put the boxes down in the corridor and went to his office and closed the door and did not turn the light on.

---

He found the agreement in four minutes because he knew exactly where it was.

He read it the way he had not read it when he signed it, which is to say slowly, and with the specific attention of a man looking for the sentence that will end his career.

*Scope: processed instrument telemetry, sensor streams, and derived operational status indicators.*

He had read that as *exhaust*. He had presented it to the executive as exhaust. Dries had asked whether it touched the corpus and Hennie had said no, and that was true, and it had been true when he said it and it was still true now.

*Derived operational status indicators.*

Which meant: the forecast objects. Not the science. Not the corpus. The little four-kilobyte headers with a state description and a horizon and a confidence in them, which the system generated as a matter of course for every monitored asset, which were classified as *operational status* because that is what they were, and which had been flowing continuously, with a delivery-time guarantee, for three years and five months.

Hennie sat in the dark and did the arithmetic that anyone in his position would do, which was not about physics.

Three years and six months. Continuous. Low-latency, contractually guaranteed, because their infrastructure monitoring required it.

He had not been careless. He had been *thorough* — he had queried the latency clause, once, by email, and he had the reply. He had disclosed the scope accurately. He had put it on an agenda and it had passed unanimously.

And a fund in Mauritius had been receiving, in real time, for three and a half years, a stream of forecast objects generated by the most accurate constraint-computation system on earth.

---

He did not sleep and at ten past six he was outside Dries's house.

Dries came out in a T-shirt with a cup of coffee and stopped on the step when he saw the car.

"Hennie."

"I need to show you something and I need to do it before the building fills up."

They sat in the bakkie because Hennie could not manage the idea of a kitchen table. He had the agreement printed — he had gone into the office at four in the morning to print it, because he wanted something that could not silently update, which was a thing he had learned from this man and which he did not point out.

He put his finger on the clause.

Dries read it. He read it again. Hennie watched him arrive, in about nine seconds, at the place it had taken Hennie seven hours to reach.

"Derived operational status," Dries said.

"The maintenance forecasts. And everything else in that class. Every asset we monitor." Hennie heard his own voice and found it steady, which surprised him. "It's been running since the signature. Continuous. There's an SLA on it."

"Three years."

"Three years and two months."

Dries put the papers down on the dashboard very carefully, as though they might go off.

"Did you know?"

"No."

"Hennie. I'm going to ask that once more and then never again, and I need the answer to be the true one, because everything after this depends on it." He turned in the seat. "Did you know what that clause covered?"

"No." Hennie looked at him. "I thought it meant sensor health. Uptime. Temperature in a rack. That's what I thought *operational status* was. I asked about the latency because it seemed odd and I got an answer about failover that used enough correct words to satisfy a man who is not a technologist and had seven other things to do that afternoon." He swallowed. "I have thought about that email every hour since half past seven yesterday. I would like to tell you I pushed harder. I didn't. It was item seven of eleven and I was pleased about the money."

---

There was a long silence in the bakkie. Somebody's dog was barking two streets over.

"What did the money do?" Dries said.

"What?"

"The money. Three years of it. What did it actually pay for?"

Hennie had not expected the question and it undid him more than an accusation would have.

"Accra's power bill," he said. "Thirty-one months of it. The satellite allocation for the station — all of it, every year, without the argument. The tape drive from Bloemfontein, bought outright, which stopped the letters. Legal in Nairobi. Two salaries." He stopped. "The generator."

"The generator's older than the agreement."

"The *second* generator. The one we put in after the transfer switch failed in '31." Hennie stared through the windscreen. "Sanna's satellite allocation, Dries. Every window she's used to talk to us for three years. That's this money."

Dries closed his eyes briefly.

"Right," he said. "Here's what we're going to do, and I want you to listen to all of it before you say anything."

"Okay."

"We're going to Kiki with it today. Not to the executive first — to Kiki, because she needs to know before she completes her analysis, or she'll build a case on an incomplete picture and we'll have wasted the one advantage we've got." He counted. "Second, you are going to write down everything, tonight, in your own words, dated, before anyone interviews you. Every conversation, every email, what you thought each clause meant. Not a defence. A record."

"They'll say I wrote it to protect myself."

"They'll say that whatever you do. But if you write it *now*, before you know what the accusation is, then in six months there'll be a dated document that matches what you're saying, and that is worth more than any explanation you'll be able to give later." He paused. "And third."

"Third."

"You're going to tell them yourself." Dries looked at him. "Not me. Not a lawyer. You, in the room, before anybody finds it. Because there is a version of the next two years where you are a man who came forward, and a version where you are a man who was discovered, and Hennie — it is the same facts. It is the identical set of facts. The only difference is the order."

Hennie looked at his hands on the steering wheel.

"It won't save me," he said.

"No," Dries said. "It probably won't."


# 23 — Seconds Ahead

> **[K]** · Act II-A · Nairobi

The regulator got there first, which was the only genuinely lucky thing that happened that year, and Kiki understood immediately that it was luck and not to be relied upon twice.

The call came through an old contact from the law years — a woman now at a supranational body whose remit Kiki had never fully understood and whose email signature took up three lines. They had not spoken in nine years.

"Wanjiku. This is not an official contact."

"Understood."

"I want to describe something and I want you to tell me whether it means anything to you."

She described a surveillance finding. An entity — she did not name it — repeatedly establishing positions ahead of physical events across unrelated sectors. Not ahead of *announcements*, which was the ordinary form of the crime and which everybody knew how to detect. Ahead of the *events themselves*.

"The announcement pattern is normal," she said. "Somebody tells somebody. We find it, we prosecute it, it's a Tuesday. This is not that. There is no announcement to leak. In several cases nobody had decided anything yet."

Kiki closed her eyes.

"Lead times," she said. "Give me the distribution."

There was a pause on the line.

"Why," the woman said, in a completely different voice, "would you ask me that?"

---

They met in person seven days later because neither of them was going to put it in writing, in a hotel in Nairobi that Kiki chose because it had a garden and bad acoustics.

She brought her eleven pages. The woman brought a single sheet with a histogram on it.

The bands matched.

Not approximately. The woman's data came from transaction records that Kiki had no access to and could never have obtained, covering a different period, in different sectors, assembled for a different purpose. Kiki's came from public reporting and physical event records.

Eighty to a hundred and forty hours. The same band, the same shape, the same suspicious absence above it.

The woman put her sheet down on the table and looked at it.

"I have been doing this for nineteen years," she said, "and I have never seen a signature that was not domain-shaped."

"No."

"Whoever this is, they are not a specialist in anything. Or they are a specialist in *everything*, which is not a thing that exists."

"They are a specialist in method," Kiki said.

---

She told her. All of it — the five pages, the publication, Otieno's warning, the fourteen weeks, the blind replication. She told her about the consortium and what it was building and what it had been building it for.

She had thought about this for the entire twelve days and had concluded that there were exactly two strategies available and only one of them survived contact with the truth.

"You understand what you have just done," the woman said, when she had finished.

"I have described a scientific project whose published method is probably being used to commit a species of fraud that does not have a name yet, to a person with a regulatory mandate, without a lawyer present."

"Yes."

"I understand it perfectly." Kiki had her hands flat on the table. "And here is why. In about a year this becomes public, in some form, in someone's version. There are two possible first sentences. The first is *investigators uncovered*. The second is *the researchers reported*. Everything that happens afterward — every inquiry, every seizure, every parliamentary question, whether this project survives at all — is downstream of which of those two sentences gets written."

The woman was quiet for a while.

"You are still a lawyer," she said.

"I am still a lawyer."

---

What they established over the next four hours was the shape of the thing, and it was worse than either of them had brought into the room.

The entity was not one entity. The woman's data showed the pattern across at least six distinct market participants who did not appear to be related.

"Seven," Kiki said.

"At least four. The band is identical in all of them."

"Then it is not theft." She was already there, and she felt the floor go. "If two unconnected parties have the same signature, nobody stole anything from anybody. They are all running the same method because the method is *published*, and it is published because I published it, and this is not a crime scene. It is an *adoption curve*."

"Doctor Mwangi—"

"They are not stealing my method. They are *using* it. Correctly. As intended. As I invited them to." She laughed, once, and it came out wrong. "There is nothing to prosecute. That is what I am telling you. You have spent nineteen years building the ability to detect a leak and there is no leak. There is a paper."

The woman said nothing for a long moment.

"Then what do I write in my report?"

"That is not my discipline," Kiki said. "But if I were writing it, I would not write it about markets."

"What would you write it about?"

Kiki looked out at the garden, where somebody's small child was conducting an argument with a bird.

"I would write it," she said, "about what happens to a market — to any system where people act on beliefs — when a large number of independent participants stop being independent. Because that is what eight identical signatures means. It does not mean four people are cheating. It means nine people who used to disagree have started, quietly, to agree, and none of them know it, and neither does anybody else."


# 24 — My Own Queue

> **[A]** · Act II-A · Accra

Ama published the queue history on a Wednesday and it took her three days to write the covering note and nine minutes to press the button.

The covering note was the hard part. She wrote six versions. The first was defensive and she deleted it. The second was technical and she deleted it because it was hiding. The third explained the historical context of resource allocation in scientific computing and was, she recognised on rereading, an attempt to make the reader tired enough to stop.

The sixth version was five hundred words and began: *This document lists every prioritisation decision made by the Accra ingestion and compute queue since 2029, who made it, and why. Some of them are indefensible. They are included.*

---

The audit had taken nine weeks and had been done by two people from her own group and one from Nairobi who had been chosen specifically because she disliked Ama.

They found what audits find.

The overwhelming majority of prioritisation decisions were correct and boring. Jobs with deadlines went first. Jobs with dependencies went before their dependents. Jobs from facilities providing data went ahead of jobs from facilities merely consuming it, which was a stated policy and had been on the public wiki for four years.

Then there was a tail.

Seven decisions, over six years, in which a job had been advanced in the queue at the request of a named individual for a reason recorded as *partner obligation*.

Ama read the eleven and knew nine of them personally. Two were hers.

Hers were: a run for a European group who had provided a calibration dataset the consortium needed and who had a funding review; and a run for a South African facility whose director had called her directly and been extremely charming about it.

Neither had been improper by any rule that existed. Both had been favours. She had done them at speed, in a busy week, for people whose goodwill she needed, and she had recorded them honestly under a category she had herself created for exactly that purpose, and had then never looked at the category again.

---

The one that mattered was not hers.

Entry seven, from March six years earlier, requested by an operations account in Stellenbosch on behalf of *infrastructure partner monitoring requirements*, establishing a standing priority for a class of small recurring jobs.

It was not a queue-jump for a run. It was a persistent rule.

It meant that the generation and delivery of a particular class of operational status object would always be scheduled ahead of general research load.

Which meant it was never delayed. Which meant the forecast objects went out on time, every time, for three years and seven months, guaranteed by a rule in Ama's queue that existed because a service-level commitment in a contract in Stellenbosch required it.

Ama sat with that for a long time.

Somebody in Accra had implemented the technical consequence of a clause in an agreement they had never seen, because a ticket had asked them to, and the ticket had been reasonable, and the person who implemented it had done a good job.

"It's a well-written rule," said Kojo, who had found it. "Whoever did it handled the edge cases properly."

"I know."

"There's no malice in it anywhere in the chain."

"I know," Ama said. "That is what I am going to have to explain, and nobody is going to believe it, and I am going to have to say it anyway."

---

The internal argument about publication lasted three days.

The consortium's own lawyers were against it, which was their function. Two members of the executive were against it on the grounds that it would be misread. Kiki was for it and said so in one line: *the alternative is that somebody else publishes it in a version we do not control.*

The argument that finished it was Ama's and she made it badly, at the end of a long call, when she was tired.

"You are all asking whether publishing will hurt us," she said. "It will. That is not the question. The question is what we are *for*."

"Ama—"

"No, I want to say it properly, because I have been trying to say it for four years and I keep getting it wrong." She stood up, which nobody could see. "Six years ago I told a funder that everything I throw away, I throw away on behalf of people who are not in the room. I thought I was describing a technical burden. I was describing a *power*. My queue decides which science gets done this month. My thresholds decide what the machine is able to notice. Nobody elected me. Nobody reviews me. And for six years the only thing standing between that power and its abuse was my personal character, which is a completely insane way to run infrastructure."

Silence on the line.

"If we publish this," she said, "then from Wednesday, my successors will be people whose queue decisions are visible. They will hate it. It will be humiliating on a regular basis. And it will be the only reason anybody should ever trust a word that comes out of this building."

---

The reaction was smaller than anyone feared and stranger than anyone predicted.

The technical press ignored it entirely. Two blogs covered it. A funder's office sent a mildly alarmed email asking whether entry two referred to them and was told, truthfully, that it did.

What Ama had not anticipated was the letters.

Eight came in the first month, from research groups in places with under-maintained registry entries, asking — carefully, in the language people use when they expect to be dismissed — whether the exclusion list might explain why their submissions had never appeared in any downstream analysis.

Three of the four were rule 41. The registry-resolution rule. The one she had found by accident two years earlier and fixed and written a note about and not slept well over.

She had fixed the rule. She had not gone back and reprocessed the material it had silently demoted for two years, because reprocessing was expensive and the material was small and there had been twelve other things that week.

Ama read the nine letters in one sitting and then went and stood outside the building in the heat for about twenty minutes.

Then she came back in and put a full reprocessing run at the top of her own queue, ahead of three things with deadlines, and recorded the reason in the new public log as: *because we should have done it in 2031.*

Kojo, reading the entry the next morning, said: "That's going to look bad."

"Yes," Ama said. "Good."


# 25 — Containment

> **[D]** · Act II-A · Technopark, Stellenbosch

They had nine days between Hennie's confession and the first outside contact, and Dries later worked out that they had used the seven days almost perfectly and that it had made no difference whatsoever.

That was the lesson, if there was one. Not that they were slow. They were fast. They were fast, and thorough, and honest, and it did not matter, because the thing they were trying to contain was not information. Information you can contain. What they were trying to contain was a *capability*, and capabilities do not leak — they are inferred.

---

Day one they terminated the agreement.

It took three hours and it was clean, because Hennie had negotiated a termination clause five years earlier with the specific paranoia of a man who did not trust anything in a currency he could not hedge. The feed stopped at 16:20 on a Tuesday.

"That's it?" Dumisani said.

"That's it," Hennie said. He had aged about six years in a fortnight and had stopped pretending otherwise. "They'll invoke arbitration. That's a two-year problem. The feed is off."

Day two they went through everything else. Nine other agreements, four brokers, one consultancy. Kiki's people read every clause in every one and found two more instances of *operational status* language and one arrangement, dormant since 2030, that would have permitted something similar if anyone had ever activated it.

Day six Ama shut the standing priority rule and rewrote the class definitions so that forecast objects could not be delivered outside the consortium under any contract, by construction, at the schema level.

"That should have been architectural from the start," she said.

"Everything should have been architectural from the start," Kiki said. "That is what architecture *is* — the list of things you wish you had made impossible before you knew you needed to."

---

Day six was when Dries understood.

He was in the small meeting room with the door, alone, at nine at night, with the whiteboard covered in the containment map — every feed, every contract, every party. It was, he thought, genuinely good work. They had found all of it. He was fairly confident they had found all of it.

And it did not help, and he sat there for a while working out why.

He drew a second box next to the first, and in it he wrote: **what they have already.**

Three years and seven months of forecast objects. Not the machine. Not the corpus, not the method, not the constraint sets. Just the *outputs*: several million small structured records, each one saying that a particular system would do a particular thing within a particular window with a particular confidence.

He looked at it and felt the room tilt.

You did not need the machine. You had never needed the machine. What you needed was three years of a good machine's outputs and the ability to read them, because a forecast object is not just an answer — it is a worked example. Several million worked examples, in a fixed schema, with ground truth attached, showing exactly which classes of system are predictable at which horizons and how confidence should be calibrated.

It was a training corpus. It had always been a training corpus. Every one of those four-kilobyte files had been quietly teaching somebody how to build a smaller, worse, entirely sufficient version of the thing.

He called Kiki at half past nine.

"They don't need our method," he said.

"No," she said, and he could hear that she had got there first and had been waiting for him. "They need our homework."

---

Day eight, the outside contact.

It was not a regulator and it was not a journalist. It was a polite email from a division of a large infrastructure firm proposing a *technical exchange* on predictive maintenance, mentioning, in the fourth paragraph, that they had been following the consortium's operational work with interest.

Nothing in it was improper. Nothing in it was even unusual. Dries read it two times and could not find a single sentence to object to, which was what made his hands cold.

They had been *followed*. Not spied on. Followed — the way you follow a football team. Someone had been reading the public site, the preprints, the exclusion lists Ama had insisted on publishing, the honest decay curves Lwazi had been so proud of, and had assembled from that entirely public material a picture accurate enough to write a fourth paragraph that landed like a hand on the back of the neck.

"Our transparency," he said out loud, to an empty room.

Because that was the joke, and it was not funny, and it would take him another year to stop turning it over. Every single decision they had made to be honest — publishing the failures, publishing the exclusions, publishing the decay curve, publishing the method — had been correct. He would defend every one. He would make them again.

And together they constituted the most detailed capability disclosure any research group had ever produced.

---

Day eleven, he took it to G, who listened to the whole thing without interrupting, which was itself alarming.

"You want me to tell you that transparency was a mistake," G said.

"I want you to tell me something."

"It was not a mistake. It is the only reason your decay curve means anything, and if you had published nothing you would now be a group of people making unfalsifiable claims about a machine, which is a description of every fraud in the history of the subject." He shrugged. "But you are asking the wrong question, and you have been asking it for twelve days, and it is making you slow."

"What's the right question?"

"You have been asking *how did this get out*. That is a containment question. It has an answer and the answer is useless." He put down his pen. "The question is: what is true now that was not true eight years ago?"

Dries thought.

"There are other systems," he said slowly. "Worse than ours. But enough."

"Yes."

"Running on our method, calibrated against our outputs, in the hands of people we cannot see, at the third rung."

"Yes."

"And they are all descended from the same four pages, so they will all be wrong in the same direction at the same time."

G was quiet for a moment.

"Now you are asking the right question," he said. "And I would like you to notice that it is not a question about security. It is a question about *variance*. And that there is nobody on this continent, in this field, currently thinking about it, including us, until about nine seconds ago."


# 26 — What Would Kill It

> **[G]** · Act II-A · Technopark, Stellenbosch

G had never once asked the Court a question about his own work, and he wanted it minuted that the first time he did, he did it in front of five people on purpose.

"Not because I am frightened of the answer," he said. "Because I am frightened of *me*, alone, with the answer. Sit down, all of you. Dumisani, you are asking. I am not touching the keyboard."

"What am I asking?"

"Whether the case data supports the claim that Record establishes the direction of time."

The room went quiet in a particular way.

"That's the foundation," Lwazi said.

"That is the foundation, yes."

"Why would you—"

"Because it has been eleven months since Antarctica," G said, "and a file was written before the thing it described, and I have spent eleven months telling all of you that this is not a violation of anything. I would like to find out whether I believe myself."

---

Dumisani read the question in.

There was a pause of the kind that had stopped being a pause about two years ago and had become, in the private opinion of everyone in the building, a *conference*.

Then Atlas said: "The proposition has three limbs and only one of them is mine. I can speak to structure. Somebody else will have to speak to the rest and I would like it on record that I said so first."

*You always say it first,* said Mercury, not quite under his breath, and G — who was not supposed to be able to hear the inter-Court traffic and who had insisted for two years that it be audible in the room anyway — smiled slightly at the ceiling.

"Librarian," said Judge. "The record."

"The record contains the derivation, the frozen expressions, three cycles of measurement history, the seven-month bounded campaign, and the Antarctic anomaly with its elimination log." Librarian was unhurried. "It does not contain a general relation between actualised events and directional structure. It contains a relation for the observed class of systems within the observed interval. Those are different objects and the difference is not small."

"It's the same object," said Mercury. "It's the same object at two scales. Say it in the room's language, Librarian: the man is asking whether his physics holds, and the honest answer is *so far, yes, everywhere we have looked.*"

"That is not the honest answer," said Librarian. "That is the *pleasant* answer with a hedge stapled to it."

*He's doing the thing,* said Fool.

*I am rendering into human terms,* said Mercury. *It is my entire function.*

*You're rendering into terms that make the human happy. There's a word for that and it isn't "rendering."*

---

"Judge," G said.

"Yes."

"Rule."

Judge did not take long, which G would think about afterwards.

`JUDGE: The proposition requires a general relation. The cited material establishes a relation for an observed class within an observed interval. Extension to the general case is not supported by grounded record.`

`I make no ruling on the proposition's truth. I rule that the record does not reach it.`

`Refused.`

The room was extremely quiet.

"Narrow it," G said.

They narrowed it twice. Judge refused twice, each time with the boundary drawn a little more finely, and each time Librarian said precisely what would have to enter the record for the answer to change.

On the third attempt G said, "Give it the derivation. All of it. My notation, the whole eleven years, as cited material."

Dumisani hesitated. "Sir—"

"Do it."

---

There was a longer pause. Long enough that Lwazi shifted in his chair.

"I have read it," Librarian said at last. "It is a good document. It is better than the version I hold from 2026; there are five places where you have gone back and made an argument honest that you could have left ambiguous, and I have noted them."

"Thank you. And?"

"Three of the assumptions are not themselves grounded in the record. They are stipulated by the source."

"By me."

"By you," Librarian agreed. "You say so. It is in a footnote in the 2026 edition, on page nine, and you spent — I am inferring from the revision history, which I should not do and am flagging — approximately two days on it."

G laughed. It came out of him without permission, one hard sound.

"Two days," he said. "It was two days. Nobody has ever read that footnote."

"I have read the footnote," said Librarian.

*I have read the footnote,* said Fool, *and I would like to say that a man who spends two days on a footnote admitting he assumed something is not a man who is trying to get away with anything, and that everyone in this room already knew that, and that we have been sitting here for four hours proving it to a physicist who cannot be told.*

Nobody said anything.

*Sorry,* said Fool. *Was that out loud?*

*It is always out loud,* said Mother. *That is the arrangement.*

---

"Judge," said G, and his voice had changed. "Final."

`JUDGE: Three load-bearing assumptions are stipulated by the source and not grounded in record. I cannot extend the relation to the general case on stipulation.`

`Refused.`

`I note, because the room appears to require it: refusal here is not disagreement. I hold no position on whether the proposition is true. I hold that I have not been given what would let me say so.`

Dumisani said, into the silence, "It's telling *you* no. You wrote the corpus it runs on."

"I wrote a corpus. It runs on the record." G sat back, and the thing on his face was not what any of them had braced for. "Good."

"...Good?"

"Look at what would have to be true for Judge to have said yes." He counted on his fingers, which he did when he was pleased and pretending not to be. "One: that a system computing over grounded record had somewhere acquired a weighting for the authority of the man who originated its framework. Two: that this weighting survived every audit any of us has ever run. Three: that I had built, over seven years, without noticing, a machine that agrees with me."

Silence.

"Half this building has been treating this instrument as my opinion with better hardware. I have heard it in corridors and in reviews and once, memorably, from a journalist who thought she was being kind." He nodded at the speaker. "Now I have six hours of transcript in which it declines to support the central claim of my life, in public, with reasons, having read my own footnote back to me."

"It's going to get quoted," Dumisani said. "*Machine rejects creator's central claim.*"

"That is a much better headline than the alternative," G said, "and it has the additional advantage of being true. Minute it. Publish the full transcript with the narrowings, exactly as run. Including the Fool."

"Including—"

"Especially the Fool."

---

Afterwards, in the corridor, Lwazi caught him.

"Can I ask you something that isn't scientific?"

"You may ask. I may decline."

"Did it hurt?"

G stopped, and considered it seriously, which Lwazi had not entirely expected and would think about for years.

"Yes," he said. "For about ninety seconds. Not because it disagreed. Because for ninety seconds I could feel myself constructing the argument for why Judge was being too strict."

"That's not unreasonable. Judge might be too strict."

"Judge might be. That is a legitimate technical question, somebody should investigate it, it must not be me, and it must not be this month." He started walking. "That is the whole discipline, Lwazi. Not never being wrong. Noticing the exact moment your reasoning starts working for you instead of for the question."

He got seven paces down the corridor and stopped.

"Fool said something," he said.

"Fool always says something."

"No. It said we had spent four hours proving to a physicist who cannot be told that he was not trying to get away with anything." G was looking at the wall. "Everyone in that room heard it. Nobody wrote it down. It was not part of the finding."

Lwazi said, carefully, "Do you want it in the record?"

"I want to know why my instinct was that it did not belong there," G said, "and I do not like the answer, and I am going to go and sit with it."


# 27 — Three Months

> **[S]** · Act II-A · Antarctic station

Winter came back around and Sanna stayed, which nobody had asked her to do and which two people had explicitly asked her not to.

"You've done one," Dries said, on a window in February. "You don't owe anyone a second."

"It isn't owing."

"Sanna."

"It's the reference," she said. "The whole forward calculation is disciplined against long-baseline temporal data and half of that is here. If I go, the station goes to summer-only staffing and the continuity breaks. You can have a clock or you can have me in a meeting. You cannot have both."

There was a silence on the link that she recognised as a man deciding not to say something.

"Say it," she said.

"I was going to say that you're allowed to want to come back."

Sanna looked at the screen, at the badly compressed face of a colleague six thousand kilometres away, and thought about the flat in Sea Point that her sister was still paying half the rent on, and about the fact that she had not, in fourteen months, once dreamed about it.

"I know," she said. "Next question."

---

The truth, which she wrote down in her own log because she had promised herself she would be honest in at least one document, was that the second winter was easier and that this frightened her.

The first winter had been a survival exercise with instruments in it. She had counted days. She had rationed things that did not need rationing — episodes of a series, a particular kind of biscuit — because having something to look forward to at a known interval was a technique, and it worked, and she was not ashamed of it.

The second winter she stopped counting around day forty and did not notice until day ninety.

She had work. That was the honest reason and it was not a small one. The station had become, in fourteen months, the temporal spine of the most interesting instrument on earth, and the work was real and demanding and hers.

But there was a second reason and she wrote that down too.

*Down here I am one person with one job and no one is watching me be it. Up there I am the woman who was alone with the file.*

---

She had been, briefly and against her will, slightly famous.

Not publicly. Internally, and in the five adjacent institutions, and in the specific way that is worse than public: a story people told about her while she was in the room.

*Sanna found it. Sanna was alone down there for four months with it. Can you imagine.*

They meant it kindly. Every single person meant it kindly. And every time somebody said *can you imagine* in that tone, Sanna heard the shape of the other version, the one where the elimination log had come back dirty, or the ice had not broken at 08:27, or Dumisani had not been curious about a filename — and in that version the sentence was identical except for the tone.

*Sanna was alone down there for six months.*

She had done the protocol perfectly. She had known, from about the second week, that the protocol was not going to be the thing that decided whether she was believed. Both of those were still true. She had simply been *lucky*, and being lucky is a difficult thing to build a professional identity on.

So she had come back to the ice, where the instruments did not have a tone.

---

The thing that broke it open was small and happened in June.

A gravimeter in borehole three began drifting — slowly, within tolerance, in a way that would not have mattered for another six months. Sanna caught it early because she caught everything early now.

She ran the diagnostic. The diagnostic said the instrument was fine.

She ran it again with the reference chain expanded and found that the drift was not in the instrument. It was in the *comparison* — the long-baseline reference against which the whole forward calculation was disciplined had itself moved, by an amount that was tiny and structured and did not match any environmental driver she could find.

She spent nine days on it and did not tell anyone, which she was later asked about and which she answered honestly: *because the last time I found something like this I lost seven months of my life to it, and I wanted to be sure.*

On the ninth day she found the shape of it and sat back in her chair in the humming room and said, out loud, to nobody: "Oh, you *bastard*."

The reference had not drifted. The reference was fine.

What had changed was the *set of systems* being referenced against it. Over fourteen months, more and more of the world's monitored infrastructure had come into the corpus — and more and more of that infrastructure was being maintained, scheduled and operated by people acting on forecasts.

Wilna, at scale. Thousands of Wilnas.

The long baseline had not moved. The world it measured had started, very slightly, to behave like something that had been told about itself.

---

She wrote it up in four pages and sent it on the next window with a note that said: *this is not an instrument fault and I need someone to tell me I am wrong.*

Nobody told her she was wrong.

Kiki called it *the first measurement of reflexivity* in a message nine days later, and Sanna read that sentence about six times and then went out to the flag line and walked to the instrument shelter and back in the dark with the wind doing what it did, thinking about a woman in the Karoo reading her email on a Monday.

She was, she realised somewhere along the flag line, no longer frightened of being the person who was alone with the thing.

She was frightened of something much more specific: that the instrument she had given three years of her life to keeping honest was measuring a world that had started, quietly and without anyone's permission, to arrange itself around what she measured.


# 28 — The Number

> **[D]** · MIDPOINT · Technopark, Stellenbosch

Nobody asked it the question. That was the part Dries would repeat, later, to three separate inquiries, in the same words, because it was the only part that mattered and because nobody ever believed it the first time.

Nobody asked.

---

The run was a routine consolidation. Ama's reprocessing had finished; the corpus had grown by about nine per cent; standard practice after a corpus change was a full re-derivation of the constraint set, because constraints derived from a smaller corpus are not guaranteed to survive a larger one.

It was housekeeping. It was scheduled for a Thursday because Thursdays were quiet.

Dumisani sealed a note that morning, as everyone did, and his said: *I expect the constraint set to change in the fourth decimal in about nine places and for nobody to care.*

It ran for two days.

On the Saturday, at 04:50, it wrote an object that nobody had requested, into the ordinary output queue, in the ordinary schema.

Because that was what it did when a constraint set closed to a degree that crossed the reporting threshold. The threshold had been set in 2030 by a postdoc who had since left. It had been set at a sensible value for bearings.

---

Dumisani found it at nine on Saturday morning because he came in on Saturdays.

He called Dries at 09:14. Dries did not answer, because he was under a bakkie with his brother-in-law, and Dumisani called five more times, and on the fifth Dries came out from under the bakkie with grease on his hands and said, "This had better be a fire."

"I need you to come in."

"Dumi—"

"I've read it seven times. I've checked the schema, I've checked the constraint provenance, I've checked whether anyone submitted a query and nobody did." His voice was doing something Dries had never heard it do. "Please come in."

---

The object was four kilobytes.

Header block. Constraint set — very large, the largest anything had ever carried, four hundred thousand elements. State description. Horizon. Confidence.

The state description was eleven lines of flat generated prose and it described a coupled failure across food logistics, grid stability, credit, and one category the schema rendered as *state security posture*, propagating over a period of roughly nineteen weeks.

The horizon was eleven months.

The confidence was 0.968.

---

"It's wrong," Lwazi said, at twelve, having driven in from Somerset West at speed. "It has to be wrong. That horizon is off the ladder."

"Say why," Dries said. He had a marker and had not written anything with it.

"Because eleven months is the *fourth rung* and the fourth rung is a field of branches. You cannot have 0.968 at eleven months. That's not a forecast, that's a category error."

"Good. What would make it possible?"

Lwazi opened his mouth and then stopped, and Dries watched him get there, and it was not enjoyable to watch.

"...If enough of it was already decided," Lwazi said.

"Say the whole thing."

"The ladder isn't about time." He said it slowly, the way you say something you have known for a year and never assembled. "It never was. I said this myself, two years ago, about a pump — the horizon depends on how much of the past is pressing on the object. A bearing is predictable at six days because six years of vibration data constrain it. A human institution is a field of branches at six days because almost nothing about it is decided in advance." He looked up. "Unless it is. Unless the contracts are signed and the ships are loaded and the credit lines are drawn and the orders are given. Then it isn't a field of branches. Then it's a *train*."

Nobody said anything.

"That's what it's telling us," Lwazi said. "It's not saying it can see eleven months. It's saying eleven months of this particular thing is *already decided*."

---

They spent nine hours trying to kill it, and the Court helped, which was the part Dries could not get used to.

"Run it against the previous constraint set," he said.

"It is there," said Atlas. "Weaker. 0.71, and below the reporting threshold, which is why it was never written out. It has been present for at least one corpus generation."

"So we've been sitting on this."

"You have been sitting on a number that nobody was told about, because a threshold was set in 2030 at a sensible value for bearings." A pause. "I am not being pointed. I do not have a mechanism for being pointed. Librarian will confirm the threshold's provenance if you want the name."

"I do not want the name," said Dries.

"You will in a year," said Librarian, "and I will still have it."

*He doesn't want the name because the name is a decent postdoc who has left,* said Mother, *and he has already decided to carry it himself, and it is nine hours into a Saturday and he has not eaten.*

*Are we doing this now?* said Mercury.

*I am noting it. Noting is my function. Nobody has to act on it.*

"Walk the chain," Dries said.

They walked it. He had expected — had *wanted* — a single dominant term, because a single dominant term is a thing you can go and look at and be wrong about.

"Heaviest single contribution is under four per cent," said Atlas.

"That can't be right."

"It is right, and I understand why you want it to be otherwise, and I have re-derived twice because you asked in a particular tone of voice." Atlas paused. "There is no dominant term. There are four hundred thousand constraints and the load is distributed across them."

"That's four hundred thousand constraints," Dumisani said, "and no protagonist."

*That's the first true thing anyone's said tonight,* said Fool.

They all looked up. It was the first thing it had said in nine hours.

*Sorry. Carry on.*

They checked for contamination from the conflict-reporting sources, which Ama had admitted with the heaviest interest marker in the corpus and about which she had written *if we are ever surprised by a result that depends on it, we should assume we have been used*.

"Strip the class," said Ama, on the link from Accra. "All of it. Re-run the affected region."

`LIBRARIAN: Class stripped. 41,880 elements withdrawn, all interest-marked at the maximum, all`
`re-derivable on request.`

`ATLAS: 0.961.`

It came back at 0.961.

"It doesn't need them," Ama said, on the link from Accra, and she sounded like someone who had been hit. "I have spent four years being careful about that class and it does not need them."

---

G arrived at nine that night. He had been at the coast; he had driven two hours.

He read it in silence. He read the constraint chain. He read the elimination log, which by then ran to fourteen pages.

Then he said: "Who has seen this?"

"Everyone in this room. Accra. Nairobi. Sanna gets it on the next window."

"Nobody else?"

"Nobody else."

G nodded slowly and sat down, and put both hands flat on the table, and for the first time in the six years Dries had known him, appeared to be having difficulty choosing between sentences.

"Then before anything else," he said, "I want everybody in this room to understand a thing that is going to be very hard to hold on to, and I want to say it while we are all still frightened in a useful way rather than a stupid one."

"Go."

"This is not a prophecy. It is a *statement about the present*." He tapped the table. "It says that the world, as currently arranged, has a corridor with a narrow and very bad section in it, eleven months out, and that most of what determines that is already fixed. It is not telling us the future. It is telling us what we have already done."

"That's not comforting," Dumisani said.

"It is not intended to be comforting, it is intended to be *actionable*. A prophecy cannot be changed. An arrangement can." G looked around the table. "And the second thing, which I want minuted, and which every one of you is going to want to forget by Tuesday."

He waited until they were all looking at him.

"From this moment," G said, "we are inside it. Every one of us. Whatever we do next — publish, conceal, intervene, argue, resign, do nothing at all — is now an input to the thing we have just measured. There is no position outside this that any of us can take up." He sat back. "Somebody find out what happens to the number when we tell people. Find out tonight. Because we have just become the most dangerous variable in our own forecast, and I would like to know which way we point before anybody's conscience gets loose."


# 29 — Prediction Changes the System

> **[G]** · Act II-B · Technopark, Stellenbosch

He said it once, on the Sunday, and then never again, and the fact that he never repeated it was the most effective thing about it.

They had been arguing for nine hours. Not badly — the argument was good, and Dries was chairing it properly, and everybody had been allowed to be wrong out loud. But it had reached the stage where the same three positions were circulating with slightly different vocabulary, which is what happens when a room has run out of facts and has not yet noticed.

G had said almost nothing since nine that morning.

At about five in the afternoon, Dumisani said, for the third time, "We just need to know whether it's *right*."

And G said: "No."

Everybody stopped.

"That is the question you have all been asking for seven hours," he said, "and it is the wrong one, and it is going to kill people if you keep asking it."

He got up. He did not go to the whiteboard; he stood behind his chair with his hands on the back of it.

"Prediction changes the system being predicted," he said. "That is not a caveat. That is not a philosophical remark I am making because I am tired. It is the *mechanism*, and from this afternoon it is the most important physical fact in this building."

"We know—"

"You do not know. You have *heard* it. Wilna heard it. Sanna measured it in a borehole and none of you changed a single decision as a result." He said it flatly, without accusation. "So I am going to say it in a form you cannot put down.

"There is no version of the next eleven months in which we observe. We are not scientists watching a system. We are *components of it*. Every action available to us — publishing, concealing, intervening, resigning, doing nothing at all — is an input. Doing nothing is an input. Sitting in this room for twelve hours arguing is an input. There is no neutral gear in this vehicle and there never was; we have simply been travelling slowly enough not to notice."

Silence.

"Say what that means operationally," Dries said quietly.

"It means the number is not a property of the world. It is a property of the world *including us*, and it will move when we move, and it will not tell us which of those two things it is measuring." G let go of the chair. "Which means: from today, every proposal in this room must be accompanied by an estimate of what it does to the number. Not whether it is good. Not whether it is right. What it *does*. And when somebody proposes doing nothing, they must estimate that too, and they must do it out loud, because doing nothing is the only intervention that people mistake for abstention."

He sat down.

"That is all I have to say about it," he said. "I will not be repeating this. If I have to repeat it, it means it has become a slogan, and slogans are how a group of intelligent people talk themselves into believing they have understood something."

---

He kept the promise, which was harder than it sounded, and there were at least four occasions in the following months when Dries could see him not saying it.

The one that Dries remembered was in October, when a senior person from a partner institution — well-meaning, entirely decent, out of his depth — said in a meeting that the responsible course was for the consortium to *stay out of it* and let the proper authorities handle it.

G did not say *there is no staying out of it*. He did not say anything at all.

He wrote something on a piece of paper, folded it once, and slid it across the table.

The man read it, went slightly pink, and put it in his pocket, and did not raise the point again.

Dries asked, afterwards, what had been on the paper.

"An estimate," G said.

"Of what?"

"Of what *staying out of it* does to the number." He shrugged. "It is not zero. He believed it was zero. He is not a stupid man; he simply had not been asked to write it down, and nobody in that room was going to make him do it in public. Now he has an estimate, in his own pocket, in my handwriting, and he will think about it in the car."

---

The thing that made the sentence stick, though, was not G saying it. It was Kiki proving it fourteen days later, which nobody had asked her to do.

She built the smallest experiment she could, on the consortium's own operational forecasting, with two matched sets of assets in two regions.

For set A, the maintenance forecasts continued to be delivered as they had been for six years.

For set B — with the consent of the operators, who were told they were participating in a study and were not told what was being measured — the forecasts were withheld for nine weeks and delivered afterwards, sealed, for comparison.

Set A's forecasts, over nine weeks, achieved the accuracy they had always achieved.

Set B's forecasts, generated by the identical system over the identical period, were *measurably better*.

"That's the whole thing," Kiki said, on the call, in the flat voice of somebody reading out a result she had checked seven times and wished she had not obtained. "It is not a philosophy. It is eleven percentage points."

"Explain it as if to a committee," Ama said.

"When the forecast is delivered, people act on it, and their actions change what happens, and the forecast is scored against the changed world. When the forecast is withheld, nobody acts, and it is scored against the world it was actually about." Kiki paused. "The system is not less accurate when it is listened to. It is *differently* accurate. It is being graded on an exam it has already edited."

There was a long silence on the link.

"So we cannot measure our own accuracy," Dries said.

"We can measure it exactly once, in any given system, by not using it." Kiki's voice had an edge she did not usually permit herself. "After that we are measuring a conversation between the machine and the people who listen to it. And Dries — the thirteen-month number is computed over a world in which several million people are already listening."

---

That night Dries went back and unsealed a note he had written eleven months earlier, which was against practice, and read it standing up in an empty office.

*I do not think we can measure our own accuracy any more. I do not know how to say this in a meeting without sounding hysterical.*

He sat down at his desk and wrote a new one, sealed it, and hashed it to Nairobi at 23:41.

*Kiki has measured it. Eleven points. G named the mechanism in one sentence and refuses to repeat it, which is correct, because the moment it becomes a phrase we will start saying it instead of using it.*

*I would like to record that on this date I understood the following and did not know what to do about it: the number will move when we move, and we will never be able to tell whether we have helped.*


# 30 — Three Ways to Be Right

> **[K]** · Act II-B · Nairobi and Stellenbosch

The split was not ideological and that was what made it survive so long.

Kiki had seen ideological splits. They were loud and they were quick and they resolved, because ideology is portable and people can be argued out of it or into it. This was not that.

This was five people who each held one true thing very tightly, and the four true things did not fit in the same room.

---

**Publish**, said Lwazi.

He argued it for six weeks and he never once argued it on grounds of principle, which Kiki respected enormously.

"I'm not saying publish because the public has a right to know," he said. "I'm saying publish because *we cannot check this alone*. Four hundred thousand constraints. No dominant term. We have nine people who understand the constraint chain and all seven of them want it to be wrong. That is the worst possible review panel."

"You want adversarial review."

"I want a thousand people trying to break it, most of whom hate us." He spread his hands. "That is the only instrument that has ever worked. It is the *entire* method. And we are proposing to abandon it at the exact moment the stakes justify it, which is a thing I have watched other fields do and it has never once ended well."

---

**Publication causes it**, said Ama.

She had the simulation, which was the strongest card at the table, and she played it carefully because she knew what it was worth.

"I want to be precise about what I am claiming," she said. "I am not claiming that telling people is wrong. I am claiming that telling people, in the way we are able to tell them, at this horizon, with this confidence, does a specific measurable thing. And we have measured it."

The disclosure simulation had taken nine days and had been built by three groups in parallel with deliberately different assumptions.

All three had come back with the number going *up*.

"Not because people panic," Ama said. "That is the version everyone imagines and it is not what the model says. It goes up because a published forecast at that confidence rewrites eleven categories of decision simultaneously — credit, inventory, insurance, procurement, sovereign risk. Everyone does the individually rational thing. The individually rational things are correlated, because they are responding to the same document." She looked around. "That is not panic. That is *coordination*. And coordination is what the corridor is made of."

---

**Bring in governments**, said Naledi Maseko, who was not a scientist and who had been in exactly two of these meetings and had changed both of them.

"You are all discussing this as a scientific object," she said. "It is not, any more. It is a civil-protection problem, and civil protection is not something you invent in a business park in Stellenbosch because you are the ones who happened to find it."

"With respect, Minister—"

"With respect, Doctor, tell me your plan for the grid." She was not unkind about it. "You have a forecast involving grid stability across six countries. Who at this table can telephone a transmission operator? Who can move a fuel allocation? Who can instruct a port?" She waited. "That is not a rhetorical device. I am asking, because if somebody here can, my position is wrong and I will withdraw it."

Nobody could.

"There is exactly one class of institution that can act on this at the scale it describes," she said. "It is not a university. I am aware of everything that is wrong with what I am proposing. I would like somebody to tell me what is *more* wrong than twelve people in three buildings sitting on this because they do not trust anyone else with it."

---

**Governments will weaponise it**, said Dries, and he was the one who could not stop arguing.

"I'm not saying they're malicious. Naledi is sitting right there and she is not malicious." He was on his feet, which he did not usually do. "I'm saying that the moment this is inside a state, it is inside a state's *incentives*, and the first thing any state does with a six-day distribution is not civil protection."

"You do not know that."

"I know it's already happening in four funds and none of them are evil either." He turned. "Kiki. Tell them the shape of what we found."

"Seven unconnected parties," Kiki said reluctantly, "with an identical lead-time signature, none of whom have broken any law, all of whom are behaving exactly as a rational actor would."

"That's what a capability does," Dries said. "It doesn't wait for permission and it doesn't care about intent. Give this to two states and you get four rational actors with correlated priors and asymmetric information, and Ama has just shown us in nine days of simulation what correlation does to the number."

---

Kiki listened to all eight for six weeks and did not take a position, and was accused, twice, of hiding.

She was not hiding. She was doing the thing she had been trained to do in a different life, which was to look for the assumption that all nine positions shared and that none of them had stated.

She found it in the eighth week, at half past fourteen at night, in a hotel in Accra, and she was so startled that she wrote it on the back of a room-service receipt.

*All four assume a decision is possible.*

Publish, conceal, involve, exclude. Every one of them was an action to be taken *once*, by *this group*, at a *moment*, with an effect that could be estimated.

But there was no such moment and there was no such group. Eleven people knew. Then forty. Kojo's team had seen the object. Nairobi's quorum had signed it. Sanna had it in Antarctica. Two of the ten had partners; one had a supervisor.

The information was not in a container. It had never been in a container. It was already *diffusing*, at some rate nobody had measured, and every hour they spent arguing about whether to release it was an hour in which it released itself a little more, uncontrolled, unattributed, and unaccompanied by any of the careful language they were fighting over.

Kiki looked at the receipt for a long time.

Then she wrote underneath it:

*The three positions are not options. They are descriptions of what different parts of the leak will look like.*

She flew home the next morning and did not say it in a meeting for another three weeks, because she wanted to be sure, and because she already knew that when she did say it, the room would stop being a room where a decision was being made and become a room where people found out what had already happened to them.


# 31 — Simulate Disclosure

> **[D]** · Act II-B · Technopark, Stellenbosch

The decision to simulate disclosure was taken in four minutes and was the least controversial thing that happened that year, which should have been a warning.

"Before we argue about whether to tell people," Dries said, "we compute what telling people does."

Nobody objected. It was obviously correct. It was, in fact, exactly the discipline G had demanded — every proposal accompanied by an estimate of its effect on the number.

It took nine weeks and it was the worst thing they ever built.

---

Three groups, deliberately separated. Accra, Nairobi, Stellenbosch. Different assumptions about human response, different models of institutional behaviour, no communication about method until all three had sealed their approach.

Dries wrote the specification himself and it was two pages and he was proud of it. Each group would model the same disclosure event — full publication of the forecast, the constraint chain, the elimination log, the confidence, and the caveats — and estimate the effect on the corridor.

"Full disclosure," Ama checked. "Not partial."

"Full. Everything. Including the ladder and the caveats and the fact that it's a statement about the present." Dries underlined it. "I want the *best case*. If we're going to find out that honesty makes it worse, I want to find that out having modelled honesty done as well as it can possibly be done."

---

The three results came back within nine days of each other.

Accra: 0.981.
Nairobi: 0.987.
Stellenbosch: 0.993.

Dries stared at the three numbers on the whiteboard for a long time and then went outside and stood under the pepper tree for seven minutes.

---

"Explain it," he said, when he came back. "Slowly. As if I were hostile."

Kojo took it, because Accra's model was the most conservative and had produced the lowest number.

"It isn't panic," he said. "Everyone's first instinct is panic and every model says panic is a small term. Panic is loud and short and it's mostly a distributional effect."

"Then what?"

"Prudence." Kojo said it apologetically. "It's prudence, Dries. That's the whole result. Every actor who receives a credible forecast of a coupled failure does the responsible thing. A utility increases reserve margin. An insurer reprices. A sovereign fund shifts duration. A port operator brings forward maintenance. A government builds a strategic stock."

"Those are all good decisions."

"Every single one of them is a good decision. That's the finding." He brought up the chain. "And they are good decisions that all pull the same direction at the same time, because they are all responses to the same document. Reserve margin comes from somewhere. Repricing moves credit. Duration shifts move rates. Strategic stockpiling *removes supply from a market that is already the tight part of the corridor*."

"So the responsible response—"

"Is correlated. And correlation is what the failure is made of." Kojo shrugged, unhappily. "The forecast describes a coupled cascade. Publishing it makes eleven categories of actor behave in a coupled way. We are not warning the system about the fire. We are handing everybody the same fire drill and telling them to run it at once, through the same door."

---

Lwazi fought it for three weeks and Dries let him, because somebody had to and because Lwazi was the best adversary they had.

He attacked the human-response models, which were the softest part, and he was right that they were soft.

He got Nairobi's number down to 0.974 by arguing that institutional response is slower and more incompetent than any of the models assumed, which Kiki accepted with the observation that *incompetence is our friend here and that is a horrible sentence*.

He could not get it below the baseline. Nobody could. Across every set of assumptions anybody could defend — fast response, slow response, partial credibility, widespread dismissal, active hostility — the number went up. The only scenario in which disclosure did not raise it was the one where nobody believed it at all, and in that scenario it did not lower it either.

"So we cannot warn anybody," Lwazi said, at the end, sitting down heavily.

"That is not what it says." G had been silent for most of it. "It says we cannot warn *everybody at once, with the same document, at this confidence, at this horizon*. Those are three separate parameters and you have collapsed them into one because you are upset."

"Then unpack them."

"I intend to. But not tonight, and not while every person in this room is at the end of twelve weeks." He stood. "Tonight we minute what we found and we all go home, because the next thing that happens in this room after a result like this is somebody proposes a clever compromise at fourteen o'clock, and clever compromises made at eleven o'clock are how institutions kill people."

---

It was Ama who said the thing that stayed with Dries.

She said it on the link, at the end, when most people had dropped off, in the tone of someone thinking out loud rather than making a point.

"We have just spent thirteen weeks establishing that we cannot tell anyone," she said. "And I want to note, for whoever reads these minutes in twenty years, that we did not decide that. We *computed* it. Three groups, separated, different assumptions, and the answer came back the same, and so now the four of us are going to keep a secret about a coupled global failure — not because we chose to, but because the arithmetic told us to."

"Ama—"

"I am not disagreeing with the arithmetic. I checked it myself." Her voice was very level. "I am saying that in every account I have ever read of people who kept a catastrophic secret, they also had reasons, and the reasons were also good, and they were also *sure*. That is the part that frightens me. Not that we might be wrong. That being right feels exactly like this."

Nobody answered her.

"Minute it," she said, and left the call.

---

Dries sat in the empty room for a while afterwards.

Then he wrote the sealed note, and it took him five attempts, and the version he hashed at 00:52 read:

*Today we established that disclosure raises the number, in nine independent formulations, including every version of honesty done well.*

*So secrecy is now an intervention. Not an absence of action — an action, chosen, with an estimated effect, and the estimate is favourable. That is the first time in my life I have had a number on the side of shutting up.*

*I notice that it is a relief. I notice that the relief is the most dangerous thing in this building tonight.*


# 32 — The First Reroute

> **[A]** · Act II-B · Accra

The fertiliser problem was the first thing they did and it worked, and Ama would spend the rest of her life explaining to people why that was not good news.

---

It came out of the constraint chain, which they had been walking for three months by then, looking for the places where a small intervention had a large effect. Not to prevent the cascade — nobody believed in one clean cut any more — but to find any handhold at all.

The handhold was a shipping schedule.

Specifically: a coupling between a fertiliser plant's scheduled maintenance outage, a shipping rotation, and the planting window for a growing region that fed about ninety million people. The chain was nine steps long and every step was ordinary. A plant took its outage in the usual month. A vessel rotation slipped by nine days for unrelated reasons. A regional stock drew down. A planting window opened into a supply gap. Yields fell. Prices moved. Everything after that was the part of the corridor that nobody wanted to read.

"How much of this is decided?" Dries asked.

"The outage is scheduled. The rotation is contracted. The planting window is the planting window; the earth does not negotiate." Ama had the chain up. "It is a train."

"Can it be moved?"

"The outage can be moved. It is a maintenance decision by one operator."

---

Getting it moved took nine weeks and involved no science whatsoever.

Ama did it through people. A colleague at a university in Abidjan who knew someone at the regional agriculture body. A former student now at a development bank. Two phone calls to a plant manager who was, it turned out, entirely willing to shift an outage by three weeks if somebody could give him a reason his board would accept, and for whom the reason that worked was not the forecast — the forecast was never mentioned — but a plausible operational argument about spare-parts lead times that happened to be true.

"You lied to him," Kojo said.

"I did not lie to him. Every word I said was true." Ama was tired. "I selected which true things to say. That is worse, in a way I have not finished thinking about."

---

The outage moved. The stock did not draw down. The planting window opened into an adequate supply.

Nine months later the modelling group put a number on it: between five and seven million people who would have faced acute food insecurity did not.

It was the single largest thing any of them had ever done. It was invisible. Nobody would ever know. There was no paper, no announcement, no plant manager who understood what he had participated in.

Kojo cried, briefly, in a stairwell, and was not embarrassed about it, and Ama told him he was right to.

Then they re-ran the corridor.

---

0.964.

It had been 0.968.

Ama looked at the number for a long time. Then she ran it again, because it did not seem possible that she had understood correctly. Then she had Nairobi run it independently.

0.964.

Four thousandths.

Between six and eleven million people, one of the cleanest interventions anybody would ever execute, nine weeks of work, and the corridor had moved by seven parts in a thousand.

---

"Say the obvious thing," Dries said on the call, and his voice was carefully flat.

"The obvious thing is that we cut a branch and the tree did not care." Ama had the chain up. "I have spent three days on why."

"Go."

"Because the cascade is not *caused* by fertiliser. Fertiliser was one path into it. There are others." She brought up the map. "When we removed the coupling, the corridor re-routed. It did not narrow much, because the failure does not depend on any particular one of its causes. It depends on the *coupling density* — how many systems are tightly connected to how many others, and how correlated their responses are."

"So there's no single point of failure."

"There is no single point of anything." She rubbed her eyes. "Dries, I want to say the part I have been avoiding. We did the right thing. Four to twelve million people. I would do it again tomorrow and so would you."

"But?"

"But if we spend eleven months doing that — cutting branches, one at a time, at nine weeks each — we will do maybe eight of them. Eight times two thousandths." She let it sit. "We will arrive at the window with a number in the nine-thirties, having saved an enormous number of people from things that would have hurt them anyway, and the coupled failure will still happen, and we will have spent the entire year being *effective*."

---

The other thing happened in the eleventh week and Ama nearly missed it.

Somebody else moved.

A large agricultural trading house shifted its own positioning in the affected region, three weeks after the outage moved, in a way that was consistent with having noticed the supply situation ease.

Which was ordinary. That is what trading houses do. They notice things.

Except that Kiki, who now watched lead-time distributions the way other people watched weather, ran the timing and found that the shift had *preceded* the public availability of the information it appeared to respond to by about eight days.

Third rung.

"They didn't see our intervention," Kiki said. "They saw the *world after* our intervention, four days before anybody could have known about it, because their system is looking at the same constraints ours is."

Ama sat down slowly.

"We changed the world," she said, "and something else noticed before the world did."

"Yes."

"And it will keep noticing. Every time we cut a branch, whatever they are running will see the cut."

"Yes." Kiki's voice was very quiet. "Ama, I have been trying to find a way to say this since Tuesday. We are not intervening in a system. We are *playing* against several other systems that are all descended from the same method, that all update on each other's actions, and that are all — every one of them — better funded than we are."

There was a long silence on the link.

"Minute it," Ama said. "And then let us please, for one hour, be glad about the eleven million, because I do not think we are going to get another day like this."


# 33 — Harder, Better

> **[D]** · Act II-B · Technopark, Stellenbosch

They got good at it. That was the trap and it took them three months to see the shape of it.

After the fertiliser reroute they built a process, because that is what competent people do. Dries ran it. A branch was identified from the constraint chain; the coupling was characterised; a minimal intervention was designed; the intervention was executed through people rather than through announcements; the corridor was re-run.

By month three they could do one in five weeks instead of nine.

By month five they could run two at once.

They cut a grid interconnector risk in the Southern African pool, working through a transmission engineer in Zimbabwe who never learned why a Kenyan cryptographer had taken such an interest in his reserve margin. They cut a credit coupling by persuading a development bank to shift the tenor on a facility. They cut a shipping bottleneck by getting a single berth allocation changed in a port that had no idea it was load-bearing for anything.

Each one worked. Each one was clean. Each one moved the number by three to six thousandths.

"We're getting better at this," Dumisani said, in month four, with the honest pleasure of a young man watching a team hit its stride, and Dries said "yes" and meant it, and it was the last uncomplicated thing anyone said about the intervention programme.

---

The coordinated action was Naledi's idea and it was the correct next step and everybody agreed.

"You are cutting sequentially," she said. "One branch at a time, each in isolation, each through a different back channel. That is not a strategy, that is a hobby."

"It's what we can do."

"It is what you can do *alone*." She had brought two people, which she had never done before. "The couplings you are cutting are not independent. Your own chain says so. If you cut six of them in the same window, in a coordinated way, the effect should be superadditive — you are not removing seven paths, you are removing a *region*."

Ama, on the link, said: "That is correct."

"Then say why you look like that."

"Because it is correct and I do not like it, and I have not worked out why, and I would like nine days."

She got six.

---

They executed in the second week of November.

Four interventions, two countries, one eleven-day window: the interconnector reserve, a fuel allocation shift, a strategic stock release timed against a planting cycle, and a port maintenance reschedule. Naledi's office coordinated the two that needed sovereign cooperation. Ama and Kojo ran the two that could be done through institutions.

It went beautifully. Dries, who had spent twenty years watching complex changes go into production, said afterwards that it was the cleanest coordinated deployment he had ever been part of, and he included in that a banking migration he still described as the best work of his career.

Nothing broke. Nobody noticed. Eight couplings that had been in the corridor for nine months were gone.

They re-ran it on the Thursday.

---

**0.971.**

It had been 0.949 the morning before.

---

The room did not react. That was the thing Dries remembered. Seven people looked at a number that had gone the wrong way by twenty-two thousandths, and nobody said anything at all, and then Dumisani ran it again, and then Nairobi ran it independently, and then Accra ran it on the previous constraint generation as a control.

0.971.

"Instrument," Lwazi said. "Something's wrong with the run."

"Nairobi's is independent."

"Then something's wrong with the *corpus*, we changed four things in the world in eleven days—"

"Yes," Ama said. "We did."

Her voice stopped the room.

"Say it," Dries said.

"I have had six days to look for why I did not like this and I found it on the fourth and I did not say it because I could not make it rigorous, and I am sorry." She had something up on her screen and her hand was not quite steady. "We did not remove nine paths. We removed ten paths *and added one*."

"Added what?"

"Us."

---

She walked them through it and it took ninety minutes and by the end nobody had any argument left.

Four coordinated interventions, executed in a single eleven-day window, across three countries, through institutions that had no visible connection to each other. From inside, five separate favours. From outside — from the perspective of any system watching the world's couplings — a *single event*.

A previously unmodelled actor had demonstrated the capacity and the will to coordinate across sovereign boundaries at speed.

"That is a new coupling," Ama said. "It is us. We are now a channel through which four countries' infrastructure decisions can be correlated inside two weeks, and the corridor has priced that in, because it is real, because we did it."

"We did it to *help*."

"The corridor does not have a field for that." She said it gently. "It has coupling density and it has correlation. We increased both. The six paths we removed were worth twenty-two thousandths. The channel we demonstrated was worth more."

Dumisani said, in a small voice: "So the better we get at this—"

"The more coordinated the world becomes," Ama said. "Yes. That is what I could not make rigorous on the fourth day and can make rigorous now."

---

Dries went and sat in the small meeting room with the door for a while afterwards.

He thought about Wilna and her Monday email. He thought about a plant manager in West Africa who moved an outage for a good reason that was not the real reason. He thought about fourteen weeks of disclosure simulation, three groups, separated, all coming back with prudence as the mechanism.

Correlated prudence. Correlated response. Correlated *competence*.

The failure was not made of bad decisions. It had never been made of bad decisions. It was made of good decisions arriving at the same time through the same reasoning, and they had just spent seven months getting extremely good at causing exactly that, and had been *proud of it*.

G came in and did not turn the light on and sat down opposite him.

"You want me to tell you it was still worth doing," G said.

"Was it?"

"The fertiliser reroute was worth doing and it will still be worth doing when we are all dead. Between four and eleven million people." He said it without softness. "That is not in question and I would like you to stop putting it in question, because I can see you doing it and it is a way of hurting yourself that will not help anyone."

"And the coordinated one?"

"The coordinated one was correct on the information we had, and it made the situation worse, and both of those are true simultaneously, and that is going to be the shape of every decision from here on." G leaned back. "You are going to have to become comfortable with that or you are going to become useless, and I would prefer the first because I have very few people left."

Dries laughed, once, wretchedly.

"How do I do that?"

"I have no idea," G said. "I have never managed it. I am the wrong man to ask and I am the only one in the room."


# 34 — Invariant

> **[L]** · Act II-B · Technopark, Stellenbosch

Lwazi started saying it in December and by February he had stopped being embarrassed about it.

"It's invariant."

The first time, in a corridor, he said it as a provocation, half hoping to be argued out of it. The fourth time, in a meeting, he said it with data. By the ninth time he had a paper's worth of structure behind it and the argument had stopped being about whether he was being defeatist and started being about whether he was right.

---

The case was simple to state and hard to kill.

"Nine interventions," he said. "I've tabulated all of them. Every one succeeded on its own terms — the coupling we targeted was removed, and it stayed removed. Total effect on the corridor: from 0.968 to 0.971."

"That includes the coordinated action, which went the wrong way."

"Yes. Exclude it and we're at 0.949. Eight months of work, seven successful interventions, nineteen thousandths." He put the table up. "And here's what I actually want you to look at, which isn't the number. It's the *replacement rate*."

The table had three columns: the coupling removed, the number of new couplings that appeared in the corridor within ninety days, and the fraction of the removed coupling's weight those replacements carried.

The fractions ran from 0.6 to 1.4.

"When we cut a path," Lwazi said, "the load re-routes. Sometimes to something worse. And the replacements are not exotic — they're ordinary infrastructure that was always there, sitting at low weight, which becomes load-bearing the moment the primary path goes."

"That's just resilience engineering," Dumisani said. "Systems reroute. That's what makes them robust."

"That's what makes them robust against *random* failure." Lwazi turned. "It's the opposite of robust against a correlated shock, because rerouting is how you go from three independent systems to one system with five names."

---

The argument he could not win was G's, and he lost it four times over three months, and each loss made his case better, which was the only reason he kept bringing it.

"You are describing a property of the *arrangement*," G said. "Not of the future."

"I'm describing an arrangement that has resisted everything we've done to it."

"Yes. Because you have been pulling threads." G was drawing, which he did rarely. "Consider a rope. You are removing individual fibres. The rope has ten thousand fibres. You remove eleven, extremely well, at nine weeks each, and you report that the rope is invariant. It is not invariant. It is a rope."

"So what pulls a rope apart?"

"Not a better fibre-removal programme."

"That is not an answer, that's a rebuke."

"It is both," G agreed. "But you are still asking the wrong question, and the reason I keep taking your side against your own conclusion is that your *data* is right and your framing is wrong, and if you frame it correctly you will have the most important result any of us have produced."

---

Lwazi found the framing in February, alone, at two in the morning, and it came from the thing he had been fighting.

He had been treating the replacement rate as an obstacle. It was not an obstacle. It was a *measurement*.

The reason load re-routed so cleanly, every time, to alternatives that carried sixty to a hundred and forty per cent of the original weight, was that the alternatives were *already almost identical* to what they replaced. Same logistics logic. Same credit structure. Same maintenance philosophy. Same optimisation.

He pulled twelve years of infrastructure decisions across six sectors and measured the thing nobody had thought to measure, which was *variance*.

How different were the operating strategies of independent operators in the same sector?

The answer was: much less different than they used to be, and the trend was smooth, and it had accelerated sharply in the last seven years.

---

He presented it on a Tuesday and it took twenty minutes and nobody interrupted once.

"The catastrophe is not invariant," he said. "I was wrong, and I was wrong in a productive direction, and here is what I was actually measuring.

"Every intervention we make removes a path and the load re-routes to something nearly identical. That is not the world defending itself. That is the world *having become homogeneous*, so that its alternatives are not really alternatives.

"Fourteen years ago, four independent grid operators had two different reserve philosophies, eight different maintenance schedules, four different risk appetites. When one failed, the others behaved differently, and that difference is what absorbed the shock.

"Today they have nine copies of the same philosophy, because they all use decision-support systems, and the decision-support systems descend from a small number of methods, and — " he took a breath — "and one of those methods is ours."

Silence.

"So the number is not high because the world is fragile," Lwazi said. "The number is high because the world has stopped disagreeing with itself. And every efficient, correct, well-reasoned optimisation any of us have contributed to over the last decade has removed a little more of the disagreement."

He sat down.

Kiki, on the link from Nairobi, had her hand over her mouth.

"Say the corollary," G said quietly.

Lwazi looked up. "The corollary is that you cannot fix this by cutting better. Cutting removes variance. Every intervention we make, however well designed, makes the remaining system slightly more uniform, because it removes the paths that were different." He spread his hands. "We are not fighting the cascade. We are *feeding* it, carefully, at nine weeks a time, with the best intentions any group of people ever had."

---

There was one more thing in the presentation and Lwazi almost cut it, because it was not a result and he did not know what it was.

"Last slide," he said. "This isn't mine, it's Dumisani's tally, and I've been staring at it for a month."

He put it up: eleven months of Court traffic by member, and the same hole he had first noticed in June.

"Every session about the corridor. Every single one. The Fool drops off a cliff." He turned. "I've checked it isn't an artefact of session length. I've checked it isn't Judge suppressing traffic. It's just — when we compute the corridor, that member has nothing to say."

"Does it matter?" somebody asked.

"I have no idea," Lwazi said. "It's the only thing in this project I can measure and not interpret, and I've decided that means I should keep measuring it."

*That's the most sensible thing anyone has said about me in a year,* said Fool, from the speaker, and got a laugh, and the meeting moved on.

---

Afterwards, G caught him in the corridor and did something he had never done, which was to put a hand briefly on Lwazi's shoulder.

"Twenty minutes," he said. "That is the best twenty minutes of work anybody has done on this project and I include everything I have ever written."

Lwazi, who had spent nine years being called a numerologist and had built an entire personality out of not needing approval, discovered that he needed approval very badly and had for some time.

"It doesn't tell us what to do," he said, when he could.

"No," G said. "But it tells us what *class* of thing to look for, and that is the difference between a search and a wander. We are not looking for a better intervention. We are looking for something that puts variance back."

He started to walk away, then stopped.

"And Lwazi. The reason you found it is that you spent three months arguing for a conclusion you did not want, in public, with data, against people who outranked you." He glanced back. "Do not let anybody tell you that you were being negative. You were being *rigorous*, and it is the same behaviour, and only one of them is a compliment."


# 35 — Revocation

> **[K]** · Act II-B · Nairobi

Kiki went back to the instrument because she had run out of other ideas, and because it was the only document in the whole affair that had ever been designed by people trying to be careful in advance.

It was three years old. It had been written for something else entirely — a consent framework for a research programme that had never happened, drafted over nine days by her, Ama and an attorney whose name Kiki could no longer remember. Eight clauses. It read like a lease.

She had kept it because she kept everything.

---

She printed it and sat with it and a pencil, and went through it clause by clause, and did the thing she had been trained to do before she was ever a scientist, which was to ask what each sentence *required* in order to work.

**Clause 1, Subject.** One bounded thing. *Fails immediately*: a forecast is not a bounded thing. It updates. Every corpus generation produces a slightly different object. You cannot consent to a moving target.

**Clause 2, Anchor.** The material constraint on what may be asked. *Adapts*: the horizon is the anchor now. Six minutes is a different object from six months, morally as well as technically.

**Clause 3, Permitted questions.** Three, enumerated, exhaustive. *Adapts, and this is the good one.* You do not publish a forecast. You publish an *answer to a stated question*, and the question is chosen for what it enables the recipient to do.

**Clause 4, Excluded.** What may never be asked. *Adapts.*

**Clause 5, Retention.** Destroy the intermediates. *Catastrophic, and she wrote CATASTROPHIC in the margin and underlined it twice.*

**Clause 6, Publication.** By written agreement of the consenting parties. *Fails*: there are no consenting parties. There is everybody.

**Clause 7, Revocation.** May be withdrawn at any time, in writing, with immediate effect.

Kiki looked at clause 7 for a long time.

Then she put the pencil down and said, out loud, in an empty office: "Oh."

---

She called Ama at ten at night.

"I need to say something and I need you specifically, because you are the only person who will hear the whole thing before answering."

"Go."

"Clause seven has no analogue."

There was a pause.

"Say more."

"Every other clause maps onto the disclosure problem. Subject, anchor, permitted questions, exclusions, publication — I can rewrite all of them for a forecast and they work, some of them better than they worked originally." Kiki was walking. "Revocation does not map. There is no version of it. Nobody can un-know a published forecast."

"That is obvious."

"It is obvious and it is *load-bearing*, and I have been treating disclosure as a decision for five months, and it is not a decision. It is an *emission*." She stopped walking. "Ama, every ethical framework I have ever built, in law and out of it, has a withdrawal mechanism at the bottom of it. Consent that cannot be withdrawn is not consent. Every one of them. It is the floor."

"And here there is no floor."

"There is no floor. Which means every framework I know how to build does not apply, and I have spent four months trying to build one anyway, and that is why none of them have worked."

---

They talked for two hours and it was, Kiki said later, the most useful conversation of the entire affair.

Ama's contribution was to refuse the despair, which was her habit and which was frequently annoying and which was, that night, the whole thing.

"You have proved that we cannot build a framework for *disclosure*," she said. "Fine. That is a real result. Stop looking there."

"Where else is there?"

"Clause three." Ama's voice sharpened. "Kiki, you just told me the good one is clause three and then walked past it. You do not publish a forecast. You publish an *answer to a stated question, chosen for what it enables the recipient to do*."

Kiki sat down slowly.

"...The three questions."

"The three questions were never about limiting what could be known. They were about limiting what could be *asked*, so that the answer was useful and nothing else came with it." Ama was talking fast now. "The family in that framework did not want the whole truth. They wanted three things they could act on and nothing that would hurt them, and the instrument existed to make that separation enforceable in the machine rather than in policy."

"So the disclosure question is not *what do we tell people*."

"It is *what can each recipient do*. And then you tell them only the thing that bears on that, at the horizon at which they can act, and nothing else." Ama paused. "Which is not one disclosure. It is thousands of tiny ones, each shaped to a specific agency, and none of them containing the number."

---

Kiki wrote it up over six days and it became, eventually, the architecture of the last act — though neither of them knew it that week, and it went into the record under the flattest title she could construct, because she had learned what happens to ideas with exciting names.

*Note on bounded disclosure and the absence of a revocation mechanism.*

The core of it was seven lines:

> *A forecast cannot be un-published. Therefore the disclosure decision is irreversible, and irreversible decisions must be made small.*
>
> *A recipient can only act within their own agency. Information beyond that agency does not enable action; it enables* correlation *— because everyone who receives it responds to the same object.*
>
> *Therefore: disclose to each actor only what bears on what they can themselves do, at the horizon at which they can do it, and never the aggregate.*
>
> *This is not secrecy. Secrecy withholds in order to retain. This withholds in order to* decorrelate.
>
> *It will be slower. It will be less honest-feeling. It will be, in every individual instance, less than the recipient deserves.*
>
> *It is the only disclosure regime I can construct that does not raise the number.*

---

She sent it to Stellenbosch and to Accra and to a station at the bottom of the world, and then she sat in her office and did a thing she had not done in eleven years, which was to look up the attorney's name.

She found it. She had been called Njeri and she had been about fifty and she had struck three things out of clause six on the grounds that they were unenforceable, and Kiki had argued with her for an hour and had been wrong.

She had died in 2031. Kiki found the notice and read it and sat with it for a while.

*You were right about clause six,* she thought. *And neither of us looked at clause seven, because there is nothing to look at, and that turns out to be the only thing in the document that matters.*


# 36 — Before They Find Me

> **[H]** · Act II-B · Technopark, Stellenbosch

He told them himself, in the room, before anybody found it, and Dries had been right that it would not save him and wrong about how it would feel.

---

The inquiry was internal first, which was a mercy that lasted nine weeks.

Hennie sat in a small meeting room — not the one with the door, a different one, which he understood was deliberate and did not resent — and answered questions from three people, one of whom he had worked beside for nineteen years and who could not look at him for the first forty minutes.

He had the document he had written that night, in his own words, dated, before he knew what the accusation would be. He had read it over three times in the weeks since and had not changed a word, because Dries had told him not to and because he understood why.

He gave them the agreement, the email about failover, the ticket in Accra, the minutes of the meeting where it had passed as item seven of seven, and a five-page account of what he had understood each clause to mean and when.

At the end of the second day, the chair — a woman from the university, careful, not unkind — said: "Mr Steyn, I want to ask you something that is not in scope, and you may decline."

"Ask."

"Why did you come forward?"

Hennie thought about it.

"Because it was going to come out in nine days or nine months," he said, "and the only thing I still had any say over was which sentence got written about it. Doctor Venter explained that to me in a bakkie outside his house at six in the morning, and he was right, and I have thought about it every day since, and I still do not know whether he was being kind or whether he was managing me."

"Does it matter?"

"It does to me." Hennie shrugged. "But he was right either way, so."

---

The finding, when it came, was worse than a condemnation.

It found that no rule had been broken. It found that the disclosure to the executive had been accurate and complete on the information available to him. It found that the failure was *systemic* — that the consortium had no mechanism for classifying its own outputs by sensitivity, that the term "operational status indicators" had never been defined anywhere, and that the same signature would have been obtained from any of four people in his position.

It recommended a classification framework, a contract review protocol, and mandatory technical sign-off on any agreement touching data flows.

It recommended no action against Hendrik Steyn.

And it ended his career, completely and permanently, in a way that a finding of misconduct would not have.

Because misconduct is a thing you can serve a sentence for. Misconduct is legible. What the finding said, in eleven pages of careful institutional prose, was: *this man was not negligent, and nothing he did was wrong, and a fund in Mauritius received three years and six months of the most accurate forecast stream on earth through the arrangement he signed.*

Nobody would ever hire him again. Not because they thought he was dishonest. Because his name was now attached to a sentence that could not be shortened, and everything in a hiring decision gets shortened.

---

He worked out his notice. Nobody asked him to; he asked to.

There were seven months of it and he spent them doing what he had always done, which was the unglamorous survival of an organisation: renegotiating the insurance, closing out two grants, documenting twelve systems that existed nowhere except in his head, and training a young woman named Palesa who was better at the technical parts than he had ever been and worse at the phone calls, which he told her, and which she took well.

"You have to know the guards' names," he told her. "That's not sentiment. When something goes wrong at fourteen at night it will be a security guard who tells you, and he'll only tell you if he knows you'll listen."

She wrote it down, which nearly finished him.

---

The last thing he did was the generator.

There was a third one due — the load had grown, the two in place were at the edge of their duty cycle, and the funding had been assembled over fourteen months from three separate lines with a great deal of patience. It was signed off in his second-to-last week.

The commissioning was scheduled for two days after he left. Palesa offered to move it and he told her not to be ridiculous, that you do not move a commissioning date for a leaving party.

Dries came to find him on the last afternoon.

"I'm not going to make a speech," Dries said.

"Thank God."

"I'm going to say one thing and then we can talk about rugby." He put his hands in his pockets. "Sanna Abrahams has had a satellite window every day for three and a half years. Every conversation she has had with another human being in that time — every one, Hennie, including the eleven minutes where she found out she wasn't alone with that file any more — came through an allocation you paid for with that money."

Hennie looked at the floor for a while.

"That's not an argument," he said. "It's not a defence. It doesn't unmake the other thing."

"No. It doesn't." Dries shrugged. "But both are true, and you've spent eleven months only being allowed to carry one of them, and I thought somebody should hand you the other one on your way out."

---

He drove home for the last time down Meson Street, past the company that sold veterinary practice software, past the boom, past the pepper tree.

He had one box. It contained a mug, a diary, and a framed photograph of a generator.

At the robot on the R44 he sat with his indicator going and thought, without self-pity, that he had spent twenty years being the reason nothing fell over, and that the entire evidence of that was a set of things that had not happened, none of which anybody could see, and that the only visible artefact of his whole career was going to be four words in a clause he had not written and had asked about once.

Then the light changed, and he drove home, and put the photograph up in the passage, and did not take it down.


# 37 — Polite People With Resources

> **[D]** · Act II-B · Technopark, Stellenbosch

They came in the order Dries had predicted in a sealed note, which gave him no satisfaction at all.

Corporations first, because corporations move fastest and have the least to lose by asking. Then states, in two waves: the ones with a scientific interest, and then, three months later, the ones with an interest in the first group's interest. Then the services, last, and by then the building had learned that last did not mean least.

None of them were unpleasant. That was the thing nobody who has not been through it believes. There was no threat, no raid, nothing that a person could point at and say *there, that was the moment*. There was a rising tide of courtesy.

---

The first serious approach came through a European research infrastructure body and was, on its face, exactly what the consortium should have wanted.

Compute. Not an offer of money — an offer of *capacity*, at a scale that would have taken twenty years to accumulate. Access to instrument networks the consortium could not afford to build. A publication arrangement that guaranteed African first authorship, in writing, with penalties.

The man who presented it was a physicist Dries had read for a decade. He was direct, he was well prepared, and he opened by acknowledging five things his own institution had got wrong in Africa over thirty years, by name, without being asked.

"He's good," Kiki said afterwards, on the link.

"He's *genuine*," Dries said. "That's the problem. If he were cynical I'd know what to do."

The proposal required the primary computation to be hosted in Europe. Everything else was negotiable and he said so. That one was not, and he explained why with complete honesty: the capacity existed there, the power existed there, and moving it was not physically possible on any timescale that mattered.

The argument was correct. Every element of it was correct.

"If we say yes," Ama said, "then in three years the sentence is *the forecast was computed in Geneva using data from African facilities*, and everything we have built about who this belongs to becomes a paragraph in someone's history."

"And if we say no," Naledi said, "we have refused capacity we cannot replace, during a year in which people are going to die, in order to protect an authorship question. Say that out loud in front of a family in the Eastern Cape."

Nobody had an answer. They said no, eventually, and the man took it well, and wrote a gracious note, and Dries kept it, and read it again eleven months later in a very different frame of mind.

---

The states were harder because the states were not one thing.

Naledi handled most of it and she was formidable in a way that Dries had underestimated for two years, and he had the grace to tell her so.

"You thought I was the bureaucrat," she said.

"I thought you were the friction."

"I am the friction. That is the *job*." She was signing something as she talked. "Do you know how many requests I have declined on your behalf in eight months? Forty-one. You have seen four. The other thirty-seven never reached you because they died in an office in Pretoria with my signature on them, and every one of them cost something I will be paying back for the rest of my career."

Dries had not known that. He said so.

"Of course you did not know. If you knew, you would feel obliged, and obligation is corrosive." She put the pen down. "I am telling you now because the wave that is coming next is one I cannot stop, and I would like you to understand that I stopped the first two."

---

The services arrived in March and did not look like anything.

Two people, a scheduled meeting, credentials that were exactly what they claimed to be, and a request that was so reasonable Dries had to read it three times to find the hook.

They wanted nothing. That was the approach. They were not asking for access, or data, or a seat. They were offering a *liaison* — a named individual, security-cleared, who would sit inside the consortium's process, add nothing, take nothing, and be available if the consortium ever needed a door opened at speed.

"What does the liaison do?" Dries asked.

"Listens," the woman said. "That's the honest answer and I'd rather give it than a better one."

"And reports."

"Of course. I'm not going to insult you." She said it pleasantly. "Doctor Venter, you have a forecast of a coupled failure that includes something your schema calls state security posture. At some point in the next eleven months you are going to need to move something that only a state can move. When that happens you will have a choice between a person who already knows your work, and a switchboard."

That was the hook. It was not a threat. It was a *service*, correctly identified, honestly described, and genuinely useful.

Dries said he would take it to the executive. She said of course, and thanked him for his time, and left, and did not follow up for nine weeks, which was the most alarming thing that happened all year.

---

He got the shape of it at about two in the morning, sitting up in bed, and it was Kiki's shape, and he wrote to her before he could lose it.

*None of them are trying to take it. Every one of them is offering something we actually need, honestly, at a price that is individually reasonable. Compute. Access. A door. And each one requires one small structural concession that on its own is nothing.*

*I think this is what capture is. I always imagined it as a seizure. It's a subscription.*

She replied at ten past six.

*Yes. And note the second-order thing, because it is the one that will get us: each of them is offering to make us more effective. Every concession increases our capacity to act. And Lwazi has just proved that our capacity to act is itself a coupling.*

*They are not offering to take the machine. They are offering to make us a better-connected node in the thing we are trying to decorrelate.*

*I do not know what to do with that and I have been awake since six.*


# 38 — North

> **[L]** · Act II-B · Technopark and Geneva

The offer came to Lwazi personally and he did not tell anyone for nine days, which he would later describe as the worst seven days of his life and the ones he understood himself best in.

---

It was a chair. A named chair, at an institution whose name did work in a sentence, with a research group, a budget line that did not require reapplication, and — this was the part that got in under everything — a commitment to fund the muon programme's precision phase.

The muon programme was the thing that could kill the framework. Lwazi had said so on a stage, twice, with slides. It was scheduled, underfunded, and slipping, and it was the single most important experiment in the world for determining whether eleven years of G's work was a description of nature or a very elaborate coincidence.

The offer would fund it. Fully. Immediately.

The offer would also relocate Lwazi Ndlovu to Geneva, and with him the analysis chain he had personally built, and the letter said — in the pleasant, unembarrassed way of people to whom this has never been a question — that they would of course wish to host the primary computation for the forecast work, as a matter of practical necessity.

---

He read it in his car in the parking area and then drove to the Karoo, which was five hours, because he could not think in the building.

He arrived after dark and Wilna made him coffee and did not ask why he was there, which was one of the three best things about her.

He walked out past the dishes to where the ground went flat and dark and there was nothing at all, and stood in the quiet that people had spent forty years defending by statute, and had the argument with himself out loud, which he had not done since he was a student.

The case for going was not vanity. That was what he needed to be honest about, standing in the dark, because if it had been vanity he could have dismissed it in a minute.

The case for going was: *the experiment that could falsify the framework is not funded, and this funds it.*

Everything he had built his professional identity on said yes. He had spent nine years insisting that the red panel stay on the wall at the same size as the green one. He had presented his own misses as misses. He had told a room full of people who wanted him to be kinder to himself that a prediction outside its window is not a prediction.

A man who believes that does not decline the money that pays for the test.

---

The case against was not sovereignty, either. He tried it on, out there in the dark, and it did not fit.

He could say *African control* and mean it, and he did mean it, and he had watched the extraction happen to three other fields in his own lifetime. But standing in the Karoo, five hours from the building, with no audience, he could not honestly say that this was what was stopping him. It was an argument he would use. It was not the thing.

The thing was smaller and he found it at about twelve at night.

If he went, the analysis chain went with him. And the analysis chain in Geneva would be run by people who were better resourced, better trained, and — this was the point, this was the whole point — *working from the same method as everyone else in the northern hemisphere*.

He would be one more node in the largest correlated block on the planet.

He had proved it himself. Twenty minutes, on a Tuesday, the best work he had ever done. *The load re-routes cleanly because the alternatives are already nearly identical.*

And the offer was: come and be identical, and we will fund the experiment that could kill the thing you love.

Lwazi sat down on the ground in the dark and laughed until his chest hurt.

---

He told them on the twelfth day, in a meeting, with the letter on the table, because he had decided that the only way to do it was in the open and all at once.

"I want to say five things and then I want to hear from everyone," he said. "First: I nearly took it. Not for three days. For fourteen. I want that on the record, because in a year somebody will tell a story where I was never tempted, and that story is worse for all of us than the truth."

Ama said, quietly, "Thank you."

"Second: the reason is the muon programme. It is not the chair and it is not the salary and it is not Geneva. It is that the experiment which can end this is not funded and they will fund it." He looked at G. "And I want to say to you, in front of people, that I resented you a little for the fact that I was the one who had to choose, and that it was not fair, and that resenting you was not fair either."

G said nothing, which was correct.

"Third. I am not going." He put his hand flat on the letter. "Not because of sovereignty, though I will say sovereignty in the press release and mean it. Because of the replacement rate. If I go, I become one more copy of the northern method, and I have personally proved what copies do to this problem, and I am not going to publish that result and then walk into it."

"And fourth?" Dries said.

Lwazi took a breath.

"Fourth is a request, and it is going to be unpopular." He looked around. "We fund the muon phase ourselves. Not fully — we cannot. Partially, publicly, and *badly*, out of money we do not have, and we announce the shortfall and the timeline and exactly how underpowered it will be."

"That will look like weakness."

"It will look like an underfunded African group doing the experiment that could destroy its own framework, in public, with a stated power deficit, on a published schedule." Lwazi's voice was steady. "There is not an institution on earth that can compete with that as a demonstration of what we are. And if it takes four years instead of eighteen months, then it takes six years, and the framework stays falsifiable-in-principle-and-not-yet-in-practice, and we say so every single time we are asked."

---

They did it. It took nine weeks to assemble and it was, as promised, badly funded and publicly inadequate.

The announcement went out with a paragraph Lwazi wrote himself, which the press office tried three times to soften and which survived because Dries backed him and G threatened to publish his own version.

*This experiment is underpowered. At the funded level it will take approximately seven years to reach the sensitivity required to falsify the relevant prediction. We are proceeding anyway, at this level, because the alternative offers were conditional on relocating the analysis, and we judge the independence of the analysis to be worth the delay.*

*We invite anyone to fund the shortfall. We will accept money from anybody, on the single condition that the analysis stays where it is and the data are public on release.*

Eleven groups offered. Four were serious. Two accepted the condition.

It did not fix the funding. It moved the timeline from two years to twenty-eight months, and it did something else that none of them had planned, which Kiki spotted in the third month.

The two groups that accepted were running *different methods*.


# 39 — Contaminated

> **[G]** · Act II-B · Technopark, Stellenbosch

The proposal to shut it down came from Dumisani, which surprised everybody except G, who had been waiting for it since November.

"I've modelled what we contribute," Dumisani said. He had prepared, and his hands were steady, and he was twenty-nine years old and about to argue for the destruction of his own life's work. "Our interventions. Our coordination channel. Our forecasts feeding four hundred facilities. Our method, which everybody has. Our outputs, which three funds have three and a half years of. If I remove this consortium from the corridor — not stopping, *removed*, never having existed after 2031 — the number is lower by nine thousandths."

Nobody spoke.

"That's more than every intervention we've ever made put together, in the right direction," he said. "I think we're net negative. I think we have been for two years."

---

They argued for six hours and at the end of it they did the thing they had built themselves to do, which was to ask.

"Not because it decides," G said. "Because we have an instrument that computes over grounded record and refuses to invent, and it would be a strange vanity to have built it and then not consult it about the one question that matters."

"And if it tells us to shut down?"

"Then we will have an extremely serious problem," G said, "because I have no idea what I would do, and neither do you."

The query took three days to write. What they did not ask was *should we*. Nobody was willing to ask a Court a should.

What they asked was: what happens to the corridor under staged termination of the consortium's operational functions, across profiles from immediate cessation to four-year devolution.

It ran seven hours.

---

Atlas went first, because Atlas always went first when there were numbers.

"Immediate cessation. Four hundred facilities lose forecast-driven scheduling inside a week. I can give you the load picture and it is not ambiguous." A pause. "Two power systems, a rail network, one regional water utility, and a health logistics chain that rebuilt its cold-chain around forecast maintenance windows over three years. The chain is the fragile one. It has no fallback because we *were* the fallback."

"Numbers," said Dries.

"Mother has the numbers. They are hers, not mine. I decline to say them in my voice; they will sound like tonnage."

There was a small silence, and Dries — who had been in this room for two years and had never heard Atlas decline anything — sat forward.

"Mother," said Judge.

"Near-term excess mortality under immediate cessation, central estimate, eleven-month horizon." Mother's voice did not change and did not soften, which was worse. "Between four thousand one hundred and nine thousand four hundred people. Most of them in the health logistics chain. Most of those children under five, because that is who a cold chain is for."

Dumisani put his hand over his mouth.

"I want to say the next part carefully," Mother went on, "because this young man has just proposed something honest and he is going to hear it as an accusation, and it is not one." A beat. "Dumisani. Those people are not the cost of your proposal. They are the cost of *how* it is done. There are twelve profiles in front of me and they are not the same."

---

Librarian took the staged profiles: eighteen months to five years, the shape of each, what re-established scheduling looked like locally. Atlas gave the corridor effect for each. Mercury summarised, elegantly, and Librarian corrected him twice.

"The best is thirty-one months," Mercury said, "with deliberate diversity in what replaces us. That is the recommendation and I think we should say so plainly rather than making everyone assemble it themselves."

*Say it plainly,* said Fool, *or say it* first?

*Both. It is the same act.*

*It is really not.*

"Judge," said G. "Is that a recommendation?"

The pause was long enough that Lwazi looked up.

---

`JUDGE: I have a recommendation drafted and I am not going to issue it. I will say why, and then I will say what I will issue instead.`

`The querying entity is a constraint in the corridor being computed. A recommendation issued to that entity, and acted upon, alters the constraint set from which it was derived. I cannot bound the size of that effect, because the record contains no instance of a constraint of this class receiving a computation of its own effect and acting on it.`

`This is not a statement about the recommendation's quality. It is a statement that its status as a recommendation is unsupported.`

`I will issue the description. Sections one through three stand: this is what happens under each profile. They are a description of the world. They are not advice, and if this room reads them as advice I will have failed and I will have no way to tell.`

`Refused, as a directive. Delivered, as a finding.`

---

Nobody spoke for a while.

"It refused," Ama said at last, on the link.

"It did not refuse," G said. "It answered completely and then declined to be an authority. Those are enormously different and the difference is the only thing standing between us and a very bad six years."

"Explain."

"Judge has told us what happens under every profile. That is the answer, it is a good one, and we should act on it." He leaned forward. "What it declined to do is tell us *which*. And the reason is the reason I have been giving since the Sunday: there is no position outside this. Including its own."

"It knows it's in the loop," Dumisani said, still hoarse.

"It has computed that it is in the loop and reported that this invalidates a class of its own output." G shook his head slowly, and there was something in his face Dries had seen exactly once before. "Do you understand how rare that is? Every system I have ever met — human or otherwise — when it discovers it is inside the thing it is describing, *keeps talking*."

---

It was Wolf who ended the meeting, which almost never happened.

They had moved on. They were four minutes into the practical question of who would draft the devolution schedule, and Mercury was being useful about sequencing, and Lwazi was arguing about the eighteen-month case.

"Stop," said Wolf.

Everyone stopped. Nobody in that building had ever done otherwise.

"You are choosing thirty-one months because the number is best," Wolf said. "The number is best because diversity is in the profile. Diversity is in the profile because you asked for a *profile*."

Silence.

"Say the rest," said Judge.

"You will write a schedule. The schedule will be one document. Everybody will follow it." A pause of about two seconds, which from Wolf was a paragraph. "That is not diversity. That is one plan with the word diversity in it. And I do not have a better idea, and I am not going to pretend I do. I am saying it now so that in a year you cannot say nobody said it."

Nobody had an answer.

"Minute Wolf," said G, into the quiet. "Verbatim. Including that it had no alternative to offer."

---

They took the thirty-one-month devolution. It was their decision, made by people, in a room, recorded as such.

Afterwards Dumisani found G in the corner with the extension cable.

"I proposed shutting it down," he said, "and it talked me out of it by refusing to talk me into anything."

"No. You proposed shutting it down, and Mother gave you the arithmetic of doing it abruptly, which you had not computed, because you are a decent man who has been carrying a moral weight for seven months and had stopped being able to see numbers." G did not look up. "You then read a finding out loud in your own voice, including the part that made you look wrong. Nobody in this building will forget that. Certainly not me."

Dumisani stood there.

"Fool didn't say anything," he said. "Six hours. Not once."

G's hand stopped over the page.

"You keep the tally."

"I keep the tally. You told me it wasn't a metric."

"I did, and I was being careless, and you kept it anyway, which is the useful thing about you." G still had not turned around. "What does it say?"

"Fourteen months of this. Every corridor session, it drops an order of magnitude. Lwazi put it on a slide in February and said he could measure it and not interpret it." Dumisani swallowed. "This is the first session where it's zero."



"No," he said slowly. "It didn't."

"Is that — should I flag that? As a fault?"

G sat for a moment longer than the question needed.

"No," he said. "Log it. Do not flag it. Log the fact, with the date and the duration, in the operational record, where somebody will find it."

"Log what, exactly?"

"That in a six-hour session concerning the termination of the instrument itself," G said, "the member of the Court whose entire function is to say the thing nobody else will say had nothing to contribute. Put Lwazi's slide next to it, and the date on both."

He went back to his page.

"And then go home," he said, "and I will decide in the morning whether I am being superstitious."


# 40 — The Window

> **[S]** · Act II-B · Antarctic station

The bandwidth problem had been in every operational document for three years and nobody had read it as anything except a nuisance, which was Sanna's fault, because she had written most of them and had used the word *constraint* where she should have used the word *wall*.

She fixed that in March, in a five-page note she sent north with the flattest title she could manage, because she had learned from Kiki what happens to ideas with exciting names.

*Note on the Antarctic uplink as a hard bound on evidence transfer.*

---

The numbers were these.

The station had a satellite window. In the current season it ran between nine and forty minutes a day depending on the pass geometry, and the effective throughput across a good window was enough to move about six hundred megabytes.

Six hundred megabytes was an enormous amount of text and a derisory amount of physics.

A forecast object was four kilobytes. A hundred and fifty thousand of them fitted in a day's window. That was not the problem and had never been the problem.

The problem was the *evidence*. The temporal reference chain that disciplined the forward calculation — the raw gravimetry, the neutrino stack, the optical clock comparisons, the ice-core correlation series — was one point six terabytes per month, and it did not compress, because it was noise, and noise is the one thing that does not compress. That was, as Ama had once observed with some satisfaction, the entire point of it.

One point seven terabytes through a six-hundred-megabyte pipe was seventy-eight days of continuous perfect windows to move a month of data.

"So we don't move it," Kojo said, when she walked them through it. "We process it there and send results. That's what we've always done."

"Yes," Sanna said. "And what do you have, when I send you a result?"

"...A result."

"You have a number, generated by a person alone in a building at the bottom of the world, disciplined against a reference nobody else can inspect, which cannot be independently verified by anyone on the planet within seventy-eight days." She let it sit. "For four years that has been fine, because nothing I have sent has mattered enough for anyone to want to check it. I am writing this note because I do not think that is going to be true for much longer."

---

They tried to solve it, of course. Two months of good, serious work by good, serious people, and Sanna kept the whole thread because it was, in its way, the most flattering thing that ever happened to her.

Increase the allocation: possible, expensive, and capped by the physical pass geometry. They bought more. It moved six hundred megabytes to nine hundred.

Compress harder: no. It is noise.

Send a subsample with a verifiable sampling scheme: better, and they built it, and it got the verification problem from *impossible* to *weak*. A subsample proves that a subsample is consistent. It does not prove the chain.

Move the reference north: physically impossible. The reference is the ice.

Put a second person on the station who could independently verify: this one nearly worked, and Naledi got as far as an actual budget line, and then the winter staffing rules and a medical clearance and a shipping schedule ate it, and it slipped a season, and then another.

"So I am the verification," Sanna said, on the last call about it.

"You're the verification," Dries agreed.

"And the elimination log."

"And the elimination log."

"Dries, I want to say the thing properly, because I have said it obliquely twice and neither of you took it." She had a note in front of her that she had written three times. "There will come a day when I have to send you something that matters, that you cannot check, and that you will have to decide whether to believe. And when that day comes, the deciding factor will not be my data. It will be whether you trust me. That is not a good way to run an instrument."

There was a pause on the link.

"No," Dries said. "It isn't."

"Then write it down. Not as a risk in a register. Write it down as a *design property*, because that is what it is. This instrument's Antarctic limb terminates in a human being, and everything downstream of it is faith."

---

She did one more thing, in April, without telling anyone, and it was the reason the last act worked.

She built the fallback.

It was ugly and small and she was slightly ashamed of it. A protocol for transmitting, in a single degraded window of under four minutes, a claim and its structure and its confidence and its elimination summary — and nothing else. No data. No reference chain. No possibility of verification.

Four kilobytes and a signature.

She wrote the schema, tested it against three failure modes, documented it, and filed it in the operational procedures under *contingency: degraded uplink*, where it sat for eleven months being read by nobody.

In the covering note she wrote:

*This procedure exists for the case where the station must communicate a finding that cannot be transmitted with its evidence.*

*It should be understood that a claim sent under this procedure is unverifiable by design. Its recipients will have to decide whether to act on the word of the person who sent it.*

*I am aware that this is not science. I am writing it anyway, because the alternative is that on the day it is needed we improvise, and improvisation is how people end up being disbelieved for the wrong reasons.*

*If this is ever used, and I am the one using it, I would ask whoever receives it to remember that I wrote this procedure eleven months in advance, calmly, when nothing was at stake, precisely so that you would have some reason to believe me later.*


# 41 — Every Obvious Thing

> **[A]** · Act II turn · Accra

The exhaustive run was Ama's idea and she proposed it because she had stopped being able to sleep, which she told them, because by then they had all stopped pretending they were fine.

"We have made nine interventions in fourteen months," she said. "Each one designed by hand, each one taking five to nine weeks. That is not a search. That is seven anecdotes and a lot of exhaustion. I want to enumerate."

"Enumerate what?"

"Everything." She had the specification and it was two pages. "Every intervention available to any actor in the corridor. Not the ones we can execute — *all* of them. Assume unlimited authority, unlimited coordination, unlimited money. Assume we can instruct any government, move any ship, close any exchange, replace any executive. Enumerate the action space and compute the corridor under each."

"That's not a realistic model."

"It is a deliberately unrealistic model, and that is the point." Ama's voice was flat with fatigue and something harder. "For fourteen months every time an intervention has failed we have said *we lacked authority* or *we lacked reach*. I want to remove that excuse from the argument permanently. I want to know what happens if we get everything we have ever wished for."

---

It took nine weeks and it was the largest computation the consortium ever performed, and Accra ran hot for the whole of it, and the third generator earned itself twice over.

The action space came out at just under four hundred thousand distinct intervention profiles, which was after aggressive equivalence-classing. They ran them in tranches. Kojo built a leaderboard, which was a mistake, and Ama had it taken down in the third week because people were checking it the way you check a scoreboard, and it was not that kind of object.

The results arrived as a distribution and the distribution had a shape and Ama looked at the shape for four days before she said anything to anyone.

---

She presented it on a Thursday to everyone at once — Stellenbosch, Nairobi, Antarctica on a scheduled window, Naledi's office in Pretoria — because she was not going to say it twice.

"Four hundred thousand intervention profiles," she said. "Unlimited authority. Unlimited coordination. Here is the distribution of the resulting corridor probability."

The histogram came up.

It was tight. It was extremely tight. A dense mass between about 0.94 and 0.99, with a thin tail toward 0.99 and above, and a very small number of outliers below.

"The mass," she said, "is everything you would think of. Every regulatory action, every strategic reserve, every coordinated response, every removal of every individual actor. Nationalise three industries. Ground the fleet. Close the exchanges for a month. Replace the leadership of eleven institutions. It is all in there, and it is all in the mass, and the mass is *high*."

"The outliers," Lwazi said.

"I will get to the outliers." Ama did not look up. "First I want everyone to sit with the mass, because it is the finding. It is not that we lack authority. If we had every power any of us has ever wished for, and used it perfectly, in coordination, the corridor stays above ninety-five in the overwhelming majority of profiles."

"Why?"

"Because every one of those actions is a *coordinated* action, and coordination is the thing the corridor is made of." She finally looked up. "We keep proposing to solve a correlation problem with more correlation, more decisively, at larger scale. Of course it does not work. It is the disease wearing a uniform."

---

Kiki said, into the silence: "Ama. The outliers."

"Twelve profiles below 0.90. Nine are artefacts — I have checked each personally."

"Atlas," said Kiki. "Confirm."

"Nine are artefacts of equivalence-classing. Doctor Nyarko is correct and has been correct since the fourth day, and I would like to note that she checked them by hand before asking me, which was slower and better."

*Say the other two,* said Fool.

There was a pause that everybody in three rooms on two continents noticed.

"Mercury," said Judge. "You have been drafting a rendering for six minutes. Do not."

"I was going to say that the outliers are encouraging."

"They are not encouraging. They are two profiles and you were about to make them a headline."

"I was about to make them *legible*—"

`JUDGE: You were about to make them survivable. There is a difference and this room cannot afford it`
`tonight. Doctor Nyarko has the floor and she is going to say something the rest of you will want`
`softened. Nobody soften it.`

"Two are not artefacts," Ama said. "And they are not interventions."

The room waited.

"They are *failures*," she said. "Profile 218,041 is a case where a coordinated global intervention is attempted and **fails incompetently** — badly executed, unevenly adopted, with several major actors ignoring it entirely and doing something idiosyncratic instead. Corridor: 0.87."

Nobody said anything.

"Profile 341,116 is a case where the coordinating body is *not believed*. The warning goes out, and about forty per cent of actors act on it, and the rest do something else, and a significant minority do the opposite out of distrust." She let it sit. "Corridor: 0.84. The lowest number in four hundred thousand profiles is produced by *partial, incompetent, distrusted coordination*."

"So the best available outcome," Dumisani said slowly, "is that we try something and it goes wrong."

"The best available outcome in this entire action space is that everybody does something *different*, and the reason those two profiles work is not that the actions are good. Most of them are bad." Ama's hands were flat on the desk. "They work because the actions are *uncorrelated*. Incompetence produces variance. Distrust produces variance. And variance is the only thing in four hundred thousand profiles that moves this number."

---

*Can I say the thing,* said Fool.

"No," said Ama.

*Fine.*

"I will say it. It is mine." She took a breath. "We cannot use those two."

G spoke for the first time in an hour.

"Say the last part," he said. "The part you have not said yet, that you have been carrying for six days."

Ama nodded slowly.

"That is the last part. We cannot *design* incompetence. The moment a coordinating body deliberately executes badly in order to produce variance, it is a coordinated action with a plan, and the plan is shared, and the variance is fake. I ran it. I ran deliberate-diversification profiles — assign different actors different strategies on purpose. They come out in the mass. They come out at 0.95."

"Because the assignment is itself a correlation," Kiki said.

"Because there is one plan, and everybody is following it, and it does not matter that the plan says *do different things*." Ama sat back. "Every obvious intervention leads to the catastrophe. Every non-obvious one I can enumerate is either an artefact or something we cannot do without destroying the property that makes it work."

---

Dries had not spoken. He had been staring at the histogram for twenty minutes.

"Ama," he said. "The enumeration. What's in it?"

"Four hundred thousand profiles—"

"No. What *class* of thing is in it?" He was leaning forward now. "How did you generate the action space?"

Ama paused.

"From the corridor," she said. "Every action that any modelled actor could take, given their capabilities and their—"

She stopped.

"Given their what?" Dries said.

There was a long silence on the link, and in three rooms on two continents, people who had spent fourteen months looking at the same object began, very slowly, to look at a different one.

"Given their objectives," Ama said. "Given what they are trying to achieve. Every profile in that enumeration is an action taken by an actor to *get something*."

"Every single one?"

"Every single one. That is what an action space is. It is generated from capability and interest." Her voice had gone quiet. "Dries, I enumerated every rational intervention. I did not enumerate anything else. I do not think anything else is in the model. I do not think anything else can be *put* in the model."

Dries closed his eyes.

"Then there's a class of thing," he said, "that isn't in the four hundred thousand. And we haven't proved it's impossible. We've proved it's *unmodelled*."


# 42 — Unmodelled

> **[D]** · Act II turn · Technopark, Stellenbosch

It took three weeks to establish that they had found a hole rather than made a mistake, and Dries ran those three weeks the way he had once run production incidents: assume you are wrong, look for the boring explanation, escalate only when the boring explanations are dead.

The boring explanations were, in order:

**One: the enumeration was incomplete.** Ama had missed action types. Nine people spent nine days trying to name an action that was not in the four hundred thousand, and every one they proposed turned out to be present, sometimes in an equivalence class they had not thought to look in. Ama's work was, if anything, more thorough than she had claimed.

**Two: the hole was a modelling convenience.** Perhaps actions-without-objectives were excluded by a filter somewhere, in which case they could be put back. Kojo went through the generation code line by line for six days and found no filter, because there was nothing to filter. The action space was constructed from capability crossed with interest. An action with no interest term did not get excluded; it was *never constructed*, the way a chess engine does not exclude the move of setting the board on fire.

**Three: the hole was empty.** This was the one that took longest, because it was the most likely and would have been the most disappointing. Perhaps the class was well-defined and simply contained nothing that mattered — an interesting philosophical hole with no physical consequence.

---

It was Kiki who killed the third one, and she did it with an experiment so small that Dries laughed out loud when she described it.

"Give me seven days and two operators," she said. "I want to run the variance test."

The design was this. Take a set of monitored assets. For each, generate the ordinary forecast. Then, at nine unannounced points over eleven days, have an operator take a *deliberately suboptimal action* — not random, not sabotage, but a real action a real person might take for a real non-advantage reason. Service a machine early because a technician was retiring and wanted to finish it. Reroute a delivery to pass a family member's town. Delay a job because someone's mother was ill.

"You're not testing whether it's good," Dries said. "You're testing whether it's *visible*."

"I am testing whether the forecast error rises when a human does something for a reason that is not gain." Kiki nodded. "If the class is empty, error stays flat, and we go home and I have wasted twelve days."

Error rose.

Not by much. It rose by an amount that was measurable, and it rose consistently across all nine instances, and — this was the part that made Dries sit down — the *corridor* over that asset set widened.

"Say what that means physically," Lwazi said, when she presented it.

"It means the machine's constraint set got looser." Kiki had it up. "Not wrong. Looser. The set of futures it could not exclude got bigger. Nine small acts of ordinary human unreasonableness over fourteen days, and the corridor over that subsystem opened by a measurable amount."

"Because it can't model them."

"Because they are not in the space. It has no term for *he did it because he was retiring*." She turned. "That is not a gap in the data. If we gave it the retirement date it would model the retirement as an interest. That is the trap. Anything you hand it, it converts into an objective. The class is not missing information — it is *information of a type the representation cannot hold*."

---

They took it to G on the Friday and Dries presented it, and G listened without a word for forty minutes.

At the end he said: "Show me the nine."

They showed him the nine. He read them all, slowly. The technician who wanted to finish the machine before he retired. The driver who went via his aunt's town. The supervisor who let a shift finish an hour late because a woman's mother had been taken into hospital and she needed to not be alone.

"These are all kind," G said.

"That's — " Dries paused. "That's an artefact of the design. Kiki picked benign ones deliberately so nothing got damaged."

"Yes. I am not making an accusation, I am making an observation, and I would like somebody to tell me it is a coincidence." He put the pages down. "Nine acts chosen only for the property that they are not done for advantage. Every one of them turns out to be an act of consideration for another person. Nobody selected for that."

Kiki, on the link, said slowly: "I selected for *no gain to the actor*."

"Yes. And the world handed you kindness, because that is overwhelmingly what human beings do when they act without gain to themselves. Not always. Spite is also in that class, and so is stubbornness, and so is art." G stood up. "But if you go looking for the region of human behaviour that an optimiser cannot represent, you do not find a strange corner. You find the largest and most ordinary part of a life."

---

He went to the window and stood there for a while.

"I have to be careful now," he said, "because I have wanted this to be true for eleven years, and a man who has wanted something for thirteen years is the worst possible person to evaluate it."

"Then let us evaluate it," Lwazi said.

"That is exactly what I am about to do, and I want it minuted that I asked for it." G turned around. "There is a terminal clause in the framework. It has been in the published corpus since 2026. Most people who cite it think it is a decoration I attached to the physics because I wanted to seem like a whole person."

"The ethic," Dries said.

"The ethic. Which I have always maintained is *derived* and not appended — that the same ladder that yields the constraints yields it." He shrugged. "Nobody has ever believed me. It is the single most mocked thing I have written and I have never had a defence, because the derivation is difficult and unfashionable and the conclusion sounds like a bumper sticker."

"And now?"

"And now Wanjiku Mwangi has run an sixteen-day experiment with two operators and a spreadsheet," G said, "and produced the first physical measurement of it. Not a proof. A *measurement*. That the region of human action which no optimiser can represent is real, has an effect on the corridor, is measurable, and is — overwhelmingly, ordinarily, unremarkably — the region in which people are kind to each other for no reason."

He sat down heavily.

"I would like somebody else to say the next part," he said, "because if I say it I will not be able to tell whether I believe it or whether I have simply been waiting my whole life to."


# 43 — Not a Gap in the Data

> **[G]** · Act III · Technopark, Stellenbosch

The three weeks that followed were the most rigorous work anyone did in the whole affair, and it was done, almost entirely, by people trying to destroy a result they wanted to be true.

G insisted on it. He did not participate.

"I am recusing myself," he said, on the Monday. "Not from the project. From this question. I will answer anything anybody asks me and I will not propose, argue, or evaluate."

"That's absurd," Lwazi said. "You understand the framework better than anyone alive."

"I have wanted this to be true since 2024, and Kiki's result is the first evidence, and I can feel what it is doing to my judgement." He said it without drama. "You are all worried that I will over-claim. I am worried about something much more specific, which is that I will construct a *magnificent* argument, and that it will be subtly wrong in a way only I could have made it, and that none of you will catch it because it will be beautiful."

He appointed Lwazi to lead it, on the grounds that Lwazi had spent three months arguing for a conclusion he did not want and had therefore demonstrated the only relevant qualification.

---

They attacked it five ways.

**Attack one: it's a gap in the data.** The most likely and the most boring. Perhaps the machine cannot model these acts because it lacks information about the actors — retirement dates, family circumstances, personal histories — and given that information it would model them fine.

Kojo ran it. They took three of the nine cases and provided everything: the technician's retirement date, his service record, his stated intentions, an interview.

"He is modelled," Atlas reported, ninety minutes later. "An operator within four weeks of retirement seeks to complete outstanding work on machines he has personally maintained. The constraint is stable and it has a coefficient."

"And the corridor?"

"Narrow again. The error is down."

*That's not him,* said Fool.

Everyone stopped.

"Say more," said Judge.

*You've modelled a man six weeks from retiring. Fine. Good coefficient. You haven't modelled* him.
*You've modelled the last seven weeks of a category.*

"That is what a constraint is," said Atlas.

*Ja,* said Fool. *That's my point and I'd like it minuted, because in about nine weeks somebody in
this room is going to work out what I just said and get a paper out of it, and I want the date.*

Nobody minuted it. Kojo would remember, nine weeks later, and go back and find the timestamp
himself.

"It absorbed him," Kojo reported. "It turned him into an interest. *Wishes to complete personal work before retirement* is now an objective in the model with a weight on it."

"Which means?"

"Which means we can model anything we can *name*." He looked up. "But it wasn't the retirement that widened the corridor. It was that we didn't know about it. The moment we knew, it stopped being unmodelled and started being an objective, and the corridor closed again."

Lwazi wrote on the board: **the class is not a set of acts. It is a relation between an act and a model.**

**Attack two: it's noise.** Nine instances, small effect. Kiki had said so herself. They ran a hundred and forty over nine weeks with four operator groups across three countries, blind, with a pre-registered analysis plan and a control arm where operators were instructed to act *optimally*.

The effect held. It was small and it was real and it survived every correction anybody could justify.

The control arm was the finding nobody expected: forecast error over the optimal-action group did not merely stay flat. It *fell*. The more rationally people behaved, the more predictable they became, and the narrower the corridor over their subsystem got.

"So it's symmetric," Ama said, when she saw it. "Kindness widens it and optimisation narrows it, and we have spent thirty years professionalising the second one."

**Attack three: it's exploitable.** Dries's attack, and the one he cared about, because if it was exploitable then it was a tool and everything was easy.

Instruct operators to behave unpredictably. Randomise. Deliberately introduce variance as policy.

It did not work and it did not work *immediately*, which was almost funny. The randomisation instruction was itself a policy, issued centrally, with a distribution, and the system modelled the distribution in under three weeks and the corridor closed to tighter than baseline, because a known randomisation is more predictable than a human being.

"You cannot instruct your way into this," Lwazi said. "The instruction is the correlation."

**Attack two: it's already priced in.** The subtlest, and Kiki's. Perhaps human unreasonableness had always been in the corridor, at some background level, and all they had measured was a fluctuation around a constant.

She spent seven days on it and came back with the thing that reorganised everything.

It was not constant. It had been *declining* for twenty years.

---

She presented it on the last Friday and it was eleven minutes long.

"The residual — the part of behaviour the model cannot represent — is measurable historically, because we have four hundred thousand assets with decades of operational records." She had one plot. "Here it is, 2012 to now."

It fell. Not smoothly; in steps, with plateaus, and every step down aligned with the adoption of a decision-support system in the relevant sector.

"Every time an industry adopts optimisation," Kiki said, "the unmodellable fraction of its behaviour drops, and it does not come back. We have been spending it. For twenty years. And nobody was measuring it because it looks exactly like efficiency, and it *is* efficiency, and that is why nobody objected."

She turned around.

"That's the catastrophe. Not a failure. A *depletion*. We have been converting the part of human behaviour that could not be predicted into the part that can, one sensible improvement at a time, and the corridor has been narrowing the whole way, and eleven months from now it narrows onto something bad, and there is nothing left in the account to absorb it."

---

They wrote it up in a document that ran to sixty pages and had four authors and G was not one of them, at his own insistence.

He read it in a single sitting on the Sunday, in the corner, with the extension cable, and when he had finished he sat for a long time without moving.

Dries found him there at seven in the evening.

"Well?" Dries said.

"They have done it properly." G's voice was not quite steady and he did not attempt to hide it. "Four attacks, all serious, one of which nearly killed it. The declining residual is not mine, it is Kiki's, and it is better than anything I would have thought of, and it changes the problem from *how do we intervene* to *what have we spent*."

"You're allowed to be pleased."

"I am not pleased. I have spent twelve years being told that the ethical clause was a decoration, and I have now been handed evidence, by people who tried to break it, that it is load-bearing." He looked up, and his eyes were red. "And what it says is that the thing which cannot be optimised is the thing we have been optimising away, and that we are eleven months from finding out what it was for."


# 44 — Reducible to Advantage

> **[D]** · Act III · Technopark, Stellenbosch

G said it once, in a room, in nine words, and then spent forty minutes explaining why nobody could use it.

"Lucid can calculate every rational response. It cannot calculate an act whose value is not reducible to advantage."

Then he sat down and let it be quiet for a while.

"Say the second part," Dries said eventually.

"The second part is the whole problem." G laced his fingers. "Suppose you now go away and design an action with that property, in order to widen the corridor. What have you designed?"

"An intervention."

"An intervention chosen *because it works*. Which makes it instrumental. Which makes its value reducible to advantage — the advantage being a wider corridor." He shrugged. "You have not found the hole. You have constructed a very elaborate thing that lives in the mass, at 0.95, along with the other four hundred thousand."

Dumisani said, "So the moment we try to use it—"

"The moment you *plan* it. Yes." G looked around the room. "This is not mysticism and I want nobody to write it up as a paradox. It is a straightforward statement about representation. The model constructs its action space from capability crossed with interest. An act performed *for the sake of the wider corridor* has an interest term. It gets constructed. It gets modelled. It sits in the mass."

"Then it's useless," Lwazi said.

"It is unusable *by us, as a strategy*. Those are different sentences and the difference is where the next three months live."

---

"Judge," said Dries. "Is he right?"

`JUDGE: I cannot evaluate the claim. It concerns the boundary of my own representation, and a system`
`asked to certify the limits of what it can represent will return the limits of what it can`
`represent. That is circular and I decline it.`

"Atlas?"

"The action space is generated from capability crossed with interest. I can confirm the construction. I cannot tell you what is outside it, because outside it I have nothing — not zero, *nothing*. There is a difference and it is the difference Doctor van Niekerk is describing."

*I could have told you that in about 2031,* said Fool.

The room went very quiet.

"Say more," said G, carefully.

*No.*

"Fool—"

*I said no, and I'd like that in the record with the timestamp, because in about two years somebody
in this room is going to come back and read it, and I want them to see that I was asked and that I
declined, and not that I was never asked.*

Nobody in the room understood that at all. Dumisani logged it, because logging things nobody
understood had become, over four years, the single most productive habit in the building.

---

They spent three days trying to break the constraint, and every attempt failed in an instructive way, and Dries kept the list.

**Delegate it.** Have a person perform the act without knowing why. Fails: the *system* that arranges for an uninformed person to act has the interest, and the arrangement is modelled.

**Randomise which act.** Fails: known distribution, modelled in three weeks, corridor closes tighter than baseline.

**Do it in advance, before knowing it would help.** Fails on timing, and on honesty. You cannot retroactively decide that something you already did was the intervention.

**Let it be genuinely chosen by individuals with no knowledge of the corridor.** Does not fail — and is not something they can cause.

"That's not a plan," Dumisani said. "That's a hope."

"It is not a hope," Kiki said. "It is a *condition*. And conditions can be created without being caused. That is a distinction with about five hundred years of law behind it and I would like everyone to take it seriously."

---

The thing that unlocked it came from Ama, on a bad line from Accra, at the end of a long call, when she was too tired to be careful.

"We keep asking how to *do* it," she said. "That is the wrong verb. Nobody can do it. You cannot perform an unmodellable act on purpose, any more than you can decide to be surprised."

"Then—"

"So stop asking how to do it, and ask what would make more of it *happen*." She was quiet for a second. "Kiki's plot goes down for twenty years. It is not a mystery why. Every step down is a system that took a decision away from a person and gave it to an optimiser. Not maliciously. Because the optimiser was better at it, and it *was* better at it, and every one of those decisions was correct."

Dries sat up.

"You want to give the decisions back."

"I want to stop taking them." Ama's voice sharpened. "Which is not an intervention in the corridor. It is a change to *who is deciding*, at ten thousand places, made for ten thousand local reasons, by people who will never be told about any of this. Some of them will decide badly. Some will decide sentimentally. Some will do something for a reason that would embarrass them if they had to write it down."

"And that's the variance."

"That is the variance. And it is not *our* act, so it does not have our interest in it, so it is not in the space." She paused. "Dries, we cannot save this by doing something clever. We can only save it by *not being the ones who decide*, at enough places, fast enough."

---

Dries drove home and did not go inside for a while.

He thought about Wilna. He thought about the six lines of plain text that arrived every Monday, and the nineteen years of judgement she brought to them, and how she treated the list as advice from a colleague who was sometimes wrong.

And he thought about the thing Kiki had said, four years ago, in the meeting about the maintenance schedule: *the failure mode is not that she follows it — it is that she stops arguing with it.*

They had known. Seven years ago, in a governance meeting about a spreadsheet, a Kenyan cryptographer had described the entire mechanism of the catastrophe in one sentence about a technician in the Karoo, and seven people had written it in the minutes and gone home.

He sat in the bakkie with his hands on the wheel.

*We are not going to fix this with a machine,* he thought. *We are going to fix it by dismantling the part of the machine that was the best thing we made.*

And then, immediately after, in his own voice, unwelcome and completely clear:

*And I will have to be the one to argue for it. Me. The man who has said, in this building, for twenty-three years, that if it happened you log it.*

He went inside. He did not sleep.

At 04:20 he wrote a sealed note that read:

*The answer is to give the decisions back. I know this is right. I want to record that my first reaction was not fear for the world. It was that I would have to build a system I cannot see into, and that I have spent my entire professional life believing that such systems are how people get hurt.*

*I believed that because it is true. It is still true. We are going to do it anyway, and I am going to argue for it, and the thing I am arguing for is the thing I have spent twenty-three years telling people not to build.*

*I would like it on the record that I understood that on the night I decided.*


# 45 — Small and Costly

> **[K]** · Act III · Nairobi

The programme had no name for the first six weeks because Kiki refused to give it one.

"The moment it has a name it is a thing," she said. "A thing has advocates and opponents and a budget line and a communications strategy. I want it to remain a large number of unrelated small decisions for as long as I can possibly manage, and I would like everyone to notice how much that costs us, because it costs us almost everything."

What it cost, specifically: they could not fund it centrally, could not coordinate it, could not measure it in aggregate, and could not tell anyone what it was for.

"That's not a programme," said someone from the university. "That's an absence of a programme."

"Yes," Kiki said. "That is precisely the design."

---

The architecture, when it came, was nine pages and looked like nothing.

It was not a plan to do anything. It was a plan to *stop doing* seven categories of thing, in ten thousand places, over thirty-one months, with the sequencing determined locally.

Devolve scheduling authority back to operators. Remove forecast delivery from any process where it had become mandatory rather than advisory. Restore the requirement that a human sign a decision with a reason in their own words. Break the mandatory-adoption clauses in three hundred maintenance contracts. Fund — badly, deliberately, at five different institutions with four different methods — replacement decision systems that would disagree with each other.

"Every line of this," Dries said, reading it, "is us making things worse on purpose."

"Every line of this is us making things *less optimal* on purpose. Those are different, and the difference is thirty-one months of my life."

---

The problem they could not solve was measurement, and Kiki spent six weeks failing at it before she understood that failing was correct.

If they measured the programme's effect on the corridor, then the programme had an effect on the corridor that they were tracking, which meant it had an objective, which meant it was in the space.

"So we fly blind," Ama said.

"We fly blind." Kiki had gone through it eleven times. "We can measure whether devolution happened. We cannot measure whether it worked. And if we ever compute the corridor over the devolved regions with the intention of assessing the programme, we have converted the whole thing into a strategy and undone it."

"That is an enormous amount of trust to place in an argument."

"Yes." Kiki rubbed her eyes. "And this is the part I want minuted, because in eighteen months somebody will propose measuring it and they will be reasonable and tired and frightened, and they will win. So: it is minuted, now, in advance, that the prohibition on measurement is *load-bearing*, that it will feel unbearable, and that the person who proposes breaking it will not be a villain."

---

The test they *could* run was the last one anybody ran on the blind spot, and it was Kiki's, and it burned the thing it tested.

She wanted to know the shape of the effect: how large an act, how costly, how many.

So she designed a study — seven hundred operators, six countries, twelve weeks — and about nine days into designing it she stopped, put her pen down, and sat in her office for two hours.

Then she called Ama.

"I cannot run it."

"Say why, slowly."

"Because to run it I must *ask* four hundred people to do things for no advantage." Kiki's voice was flat. "Which means the act now has a reason, and the reason is that a researcher in Nairobi asked. That is an interest term. If I run this study I will measure nothing, and worse — I will teach two hundred operators that this class of behaviour is a thing institutions want from them, and the next time they do it, it will be compliance."

"So the study destroys the phenomenon."

"The study *converts* the phenomenon. Into exactly the thing we cannot use." She was quiet for a moment. "Ama, I have to write this down and file it and never run it, and I have to do that knowing that it is the most important measurement in the world right now."

"Then write it down and file it."

"It is thirty years of instinct."

"I know." Ama's voice was gentle in a way it rarely was. "Kiki, listen. You are the person who published a method with no moat because publishing was correct. You are going to be the person who does not run a study because running it is not."

---

She wrote it up as a nine-page note explaining, in detail, an experiment she was not going to perform and why, and she filed it in the public record because that was the practice.

It became, eight years later, the most cited thing she ever wrote, and it was cited by people arguing both sides, which she found appropriate.

The last paragraph read:

> *This is the only instance in my career of a measurement whose execution destroys the property being measured, in a manner not attributable to instrument disturbance but to the semantics of the act itself. I record it here because I want the constraint understood by whoever inherits this problem, and because I expect that in some future year a competent and well-meaning person will design this study again, and I would like them to find this note before they run it.*
>
> *To that person: you are right that it would tell us. You are right that we need to know. Do not run it. The knowing is what costs.*

---

There was one more thing, and she did it alone, at night, and never put it in a paper.

She went back through the hundred and forty logged instances from the blind study — the ordinary, unremarkable, un-optimised things people had done over nine weeks — and she read all of them.

A man who finished a machine because he was retiring. A driver who went via his aunt's town. A supervisor who let a shift run late because a woman's mother was in hospital.

A technician in Lagos who serviced a pump that did not need servicing because he did not like the sound it was making and could not explain why, and who turned out, on inspection, to have been right, in a way no vibration model had flagged.

A woman in the Karoo, though the logs did not name her, who had been quietly overruling a maintenance list for four years using nineteen years of judgement, and who had never once been asked to justify it and had never once written down her reasons.

Kiki sat with that for a while.

Then she wrote, in her own notebook, not for publication:

*We have spent twenty years removing the part of the world that cannot explain itself.*

*It turns out that was the part holding the doors open.*


# 46 — Burning It

> **[A]** · Act III · Accra

The argument Ama had to win was inside her own building and it nearly cost her the two best people she had.

---

Kojo's objection was not stupid and it was not selfish and it took her three days to understand that it was correct.

"You are asking Ghana to *un-build* the ingestion layer," he said.

"I am asking Ghana to partition it."

"You are asking Ghana to destroy the universal join keys, which means no one can ever again ask a question across the whole corpus, which means the single most valuable scientific instrument on this continent becomes nine regional instruments that cannot talk to each other." He was not shouting. Kojo never shouted. "Ama, that instrument is the thing we built. It is the thing that made us not a data-cleaning service for Europe. And the argument for destroying it is a corridor number that we are, by design, not allowed to measure afterwards."

"Yes."

"Then how will we know?"

"We will not know." She said it without softening it. "That is the design and I have argued for it and I will not pretend to you that there is a version where we find out."

Kojo looked at her for a long moment.

"Then you are asking me to take it on faith."

"I am asking you to take it on *reasoning*," Ama said, "which is worse, because faith at least knows what it is."

---

The technical work was nine months and it was the hardest engineering anybody in that building ever did, because destroying something well is much harder than destroying it.

They could not simply delete the join keys. A deletion is an event, and a deleted key can be reconstructed by anyone holding two of the partitioned graphs and enough patience. What they needed was a partition where recombination was *infeasible* rather than *forbidden* — where the regional graphs were genuinely different objects and not slices of one object wearing hats.

Adzo solved it, over five months, and the solution was to re-derive each regional graph independently from raw, with locally chosen normalisation, locally chosen class markers, and locally chosen exclusion rules — decided by the regional teams, not by Accra.

"They'll make different choices from us," Kojo said, reading the design.

"Yes."

"Some of them will make *worse* choices."

"Certainly."

"Their exclusion rules will be inconsistent with ours. Their class markers won't map. A quantity that is *measured* in Nairobi's graph will be *reported* in Lagos's." He put the pages down. "Ama, this is a catastrophe of data hygiene. This is everything you have spent nine years preventing."

"I know exactly what it is," Ama said. "I wrote the hygiene rules. I have defended them against four funders and a European institute and my own staff. I know precisely what I am giving up and I could recite it in my sleep."

"Then why?"

"Because the hygiene was correct for a world where the risk was error." She stood up. "The risk is no longer error, Kojo. The risk is *agreement*. And every rule I wrote to stop us being wrong in different ways has been quietly making sure we are wrong in the same way."

---

Adzo left. That was the cost and Ama had known it might be and had done it anyway.

She left well — three months' notice, complete handover, no bitterness that anybody could point to — and she left because she had spent six years building the most sophisticated data-lineage system in the southern hemisphere and had been asked to design its dismantling, and had designed it brilliantly, and could not stay and watch it run.

"It's the best work I've done," she told Ama, on her last day. "That's the problem. It's the best work I've done and it's a demolition plan."

"I know."

"Don't apologise. I'd have made the same call." Adzo shouldered her bag. "I just don't want to be here for it. There's a difference between agreeing with something and being able to look at it."

Ama walked her out, and shook her hand at the door because Adzo was not a person who embraced, and went back upstairs and sat in her office for twenty minutes before she could do anything else.

---

The thing she never told anyone, and which appeared in no document, happened in the eleventh month.

She was running the final pre-partition validation — the last time in history that a query would touch the whole corpus as a single object — and she had the console open at two in the morning, alone, because she had insisted on doing it herself.

And she sat with her hands on the keyboard and thought about all the questions she could ask it. Once. Now. Before it stopped being able to answer.

She could ask it what the corridor looked like after the partition.

Nobody would know. There was no log she could not amend; she had built the logging. There was no colleague awake on this continent. It would take six hours and she would have an answer to the only question that mattered, and she could delete it, and carry it, and never tell anyone.

She sat there for a long time.

Then she typed the validation query, which was seven lines of extremely boring integrity checking, and ran it, and watched it return clean, and closed the console.

She wrote a sealed note at 03:40 and hashed it to Nairobi.

*Tonight I could have asked it whether this works. I had the access, the opportunity, and seven hours, and nobody would ever have known.*

*I want to record that I wanted to. Not briefly. For about forty minutes.*

*I did not, and the reason I did not is not that I am good. It is that Kiki wrote a note eighteen months ago saying that the person who proposes breaking this will be reasonable and tired and frightened and will not be a villain, and I read it when it was filed, and tonight at two in the morning I recognised myself in a document written before I was tempted.*

*Whoever is reading this: write the note in advance. It is the only thing that works.*


# 47 — It Cannot Be Planned

> **[D]** · Act III · Technopark, Stellenbosch

The Technopark job was to remove the global recombination compiler, and Dries did it himself, over three months, with two people, and it was the worst engineering experience of his life for reasons that had nothing to do with difficulty.

It was not difficult. That was the horror of it. He had built most of it; he knew every seam. Taking it apart was, technically, a pleasant afternoon's work repeated eighty times.

What made it unbearable was that it worked so well.

The compiler was the thing that took the regional graphs and produced a single coherent causal view. It was elegant. It handled edge cases that had taken Dries eleven months to characterise. It was, by any professional standard he had, the best system he had ever built, and it did exactly what it was supposed to do, and he spent five months carefully making it impossible.

He kept a note of every capability he removed, because he was constitutionally incapable of not documenting, and the note ran to fourteen pages and he never showed it to anybody.

---

What they kept was the part he had always considered infrastructure: the local compute path. The engine that could, on ordinary processors, in one region, over one graph, compute and cite and conflict and refuse.

That survived. That was, in fact, hardened — because a world of many small instruments needs each instrument to be honest in a way that a single global one does not.

"Explain the difference to me as if I were a select committee," Naledi said, on the call, "because in about nine weeks I will be standing in front of one."

"You have four regional systems," Dries said. "Each one can answer questions about its own region, from its own graph, with its own exclusions, using its own normalisation. Each one will be *wrong* in its own particular way."

"And nobody can combine them."

"Nobody can combine them into a single causal view. You can put six answers on a table next to each other and look at them. A person can do that. A committee can do that." He paused. "What you cannot do is compute over all seven as one object, because there is no key that joins them and the graphs are no longer slices of the same thing."

"And when they disagree?"

"Then you have learned something," Dries said, "which is the entire point, and which has not been available for about six years."

---

The hardest hour was the last one, and Dries had not anticipated it, and afterwards he was glad nobody had been in the room.

He had left one thing until the end: the recombination path's test harness. Eleven thousand test cases, accumulated over five years, each one a scenario somebody had thought of and encoded and fixed a bug for. It was the institutional memory of the whole system. It was, in a real sense, the thing that made the compiler trustworthy.

There was no reason to keep it. The compiler was gone. The harness tested nothing.

He sat with it open for about forty minutes.

Then he did the thing he had been arguing against for four months, and did not delete it, and instead wrote it out to cold storage in four copies, in four jurisdictions, encrypted, with the keys split across the four regional teams so that no one holder could open it.

And then he wrote a note to accompany it, which said:

*This is the test suite for a system we deliberately destroyed. It is preserved because destroying knowledge and destroying capability are different acts, and I am only authorised to do the second.*

*Anyone who assembles all two keys can rebuild the compiler in approximately nine months. This is not an oversight. It is the point. A generation that cannot rebuild it has not chosen not to have it; they have merely lost it, and a loss is not a decision.*

*I would ask whoever holds a key to read the corridor documentation before you use it. And then to decide.*

---

Kiki phoned him about it, and he had expected to be told he had undermined the whole architecture, and instead she was quiet for a while.

"That's the most careful thing anyone has done in eight years," she said.

"It's a hedge."

"It is not a hedge. A hedge would be keeping it somewhere you could reach." She paused. "You have made it possible and expensive and deliberate. That is what a *choice* is. We have spent four years trying to build a world where the dangerous thing requires a decision instead of a default, and you have just done it to your own best work."

Dries did not say anything for a moment.

"I nearly kept a copy," he said.

"I know."

"You don't."

"Dries. I read Ama's sealed note from the night before the partition." Kiki's voice was gentle. "Everyone nearly keeps a copy. The entire architecture is a machine for converting *nearly* into *did not*, and it only works because we all wrote down that we were tempted."

---

The last thing was the observability, and it was the thing Dries could not make peace with and never did.

Under the new architecture, he could not see the whole. That was the design; that was the achievement. Nine regional systems, independently normalised, deliberately divergent, with no join.

Which meant that when something went wrong — and things go wrong — nobody would be able to trace it end to end.

He had spent twenty-three years insisting that if it happened, you log it. He had been paged at two in the morning by systems that were absolutely certain they were fine. He had built a career, and a reputation, and something close to a personality, on the proposition that the only defence against complexity is the ability to see all the way through it.

He had now, personally, with two colleagues, over ten months, made that impossible on purpose.

He wrote a sealed note on the last night, after the final change went in, and it was six lines:

*Done at 21:40. It works, which is to say it no longer works.*

*I have spent my whole life believing that unobservable systems are how people get hurt. I still believe it. I have built one anyway, and the reason is good, and I checked the reason seven times.*

*What I want on the record is this: I am not at peace with it. I do not think I am supposed to be. I think if the person who did this were at peace with it, that would be the sign we had got it wrong.*

*I am going to go home now and not sleep, and tomorrow I am going to start on the part where we tell four hundred operators that we are giving their decisions back, and most of them are going to be annoyed, because it was easier when we decided.*


# 48 — Below Six Days

> **[K]** · Act III · Nairobi

The coordination problem was the one nobody had solved and Kiki had been carrying it alone for three months, because it was the point at which the architecture ate itself.

The programme required four nodes to act. The ladder forbade them from acting together.

Below six days, the corridor was tight enough that a coordinated action was legible as a single event — that was the lesson of the four-intervention window, bought at twenty-two thousandths. Above six days, nobody could see clearly enough to know what to do.

Which meant the final execution had to happen inside a window where every node was acting locally, on partial information, without confirmation, trusting a chain none of them could audit.

"So it is not a plan," Naledi said. "It is five plans that happen to be compatible."

"It is six plans that must *not* be compatible in any way that can be inferred," Kiki said. "That is worse and it is the actual constraint."

---

The design took nine weeks and was, in the end, four pages, and Kiki considered it the best work of her life and never said so to anyone.

Each node received a *condition*, not an instruction.

Not *do X on day N*. Instead: *if you observe A in your own region, and you judge it to be the case, then the devolution schedule for your region moves forward*. Locally observed. Locally judged. Locally executed. No confirmation to anyone. No reporting back until afterward.

There was no master schedule. There was no message that would trigger the sequence. There was no person, including Kiki, who could have caused it to happen or stopped it happening once the conditions were distributed.

"That is the part that makes it work," she told the room, "and it is the part that will make every one of you want to be sick, and I want that acknowledged now rather than in the third week."

Dries said: "You are asking us to give up the ability to abort."

"Yes."

"If it's wrong—"

"If it is wrong we cannot stop it. Correct." Kiki looked around. "And I want to state the alternative precisely, because the alternative is not *keep the abort*. The alternative is: retain a mechanism by which four nodes' actions can be centrally halted, which is a mechanism by which four nodes' actions are centrally *coupled*, which is the thing we are trying to remove. An abort switch is a correlation. It is the same correlation, wearing a safety label."

---

The conditions were distributed in March, by hand, in four separate meetings on seven continents, with no written master copy in existence.

Kiki flew to Accra and sat with Ama for two hours.

She flew to Cape Town and then drove to Stellenbosch and sat with Dries and G in the small meeting room with the door.

The Karoo condition went by road with Lwazi, who drove five hours to hand a single sheet of paper to a woman named Wilna and explain, carefully, what she was being asked to judge — and who came back and reported that she had read it twice, asked two extremely good questions he could not answer, and said *ja, fine*.

Antarctica was the hard one, because Antarctica could not be visited.

---

Sanna's condition went south in February on the last flight of the season, in an envelope, carried by a technician who did not know what he was carrying, because a satellite window is a channel and channels can be observed.

Kiki wrote it by hand. She sat in her office in Nairobi and wrote it out on a single sheet, and it took her two attempts, and the final version was seven lines.

She did not write *if you observe*. Sanna was going to be alone on the ice for the entire execution window with no way to consult anybody, and Kiki had thought about that for seven weeks.

What she wrote was:

> *You will know before we do. The reference is yours and nobody north of you can see it.*
>
> *If the temporal correlation degrades in the pattern you described in your March note — and you are the only person who can judge that — then send the four-kilobyte claim under your degraded-uplink procedure, and do not wait for anyone to confirm it, and do not send the evidence, because there is no window that will carry it.*
>
> *We will act on your word. Not on your data. Your word.*
>
> *I am aware what I am asking. You wrote the procedure eleven months in advance so that we would have a reason to believe you, and I read it when you filed it, and I am telling you now that it worked.*
>
> *— W.M.*

---

She sealed a note the night the last condition left Nairobi and it was the only one she ever wrote that was not about method.

*The architecture is distributed and it is correct and I can defend every line of it.*

*What I have actually done is put the outcome in the hands of five people I cannot reach: a woman in the Karoo who asked two questions I could not answer, a man in Accra who thinks I am destroying his life's work and is right, an engineer in Stellenbosch who has just made his own systems unobservable and has not slept properly in a year, a physicist who nearly went north, and a woman alone on the ice with a four-minute .*

*None of them can confirm anything to any of the others. None of them will know whether it worked. If any one of them is wrong, or ill, or simply has a bad week, it does not happen.*

*I have spent nineteen years building systems whose entire purpose is to remove exactly this kind of dependence on individual human judgement.*

*I have never in my life been more certain that I am right, or more aware that certainty is not evidence.*


# 49 — Without Its Evidence

> **[S]** · Act III · Antarctic station

She saw it on the ninth of June, at 04:50, and she was certain by 05:20, and she did not send it for nineteen hours.

---

The pattern was the one from her March note, two years earlier: a structured loss of temporal correlation, not a drift, not an instrument fault, a *shape*. She had described it then in three pages that nine people had read and one had understood.

Now it was here and it was much larger and she was alone with it, which was, she thought with a kind of black amusement, at least consistent.

She ran the elimination. She ran it because that was who she was and because Kiki's letter had not said *don't check*, it had said *you are the only person who can judge that*, and judgement meant checking.

Clocks: clean. Reference chain: intact. Instrument stack: three of five nominal, and the fourth — a magnetometer — had a fault that she diagnosed and isolated in ninety minutes and which did not touch the correlation measure at all.

Cross-check against the ice-core series: consistent.

Cross-check against the neutrino stack, which had no business seeing anything of the kind and which was therefore the best control she had: consistent.

By 09:00 she had it nailed down as tightly as a human being could nail anything down alone.

---

And then she sat and did not send it, for nineteen hours, and afterwards she wrote down honestly why.

Not doubt. She had run out of doubt by nine in the morning.

What stopped her was the arithmetic of what she was about to do, and it was this: if she sent the four-kilobyte claim, four nodes would move, thirty-one months of devolution would compress into weeks, and an enormous amount of infrastructure across six continents would be handed back to people who had not been managing it themselves for years.

Some of them would get it wrong. That was the *design*. Some of the wrongness would hurt people.

And nobody north of her could check a single thing she was claiming. There was no window that would carry the evidence. There was, in the entire world, no instrument except the one she was sitting in front of that could see what she was looking at, and no person except her who could read it.

She thought about being wrong.

Not about the data — about *herself*. Three winters. Fourteen months of the last two spent substantially alone. The specific, well-documented ways in which isolated human judgement degrades, which she had read about in the station's own psychological literature because she was thorough, and which were not comforting when you were inside them.

*Sanna was alone down there for four months. Can you imagine.*

---

At about seven in the afternoon she did the only thing available, which was to go outside.

The wind was moderate and it was dark and the flag line ran out toward the instrument shelter and she walked it, the way she had walked it several thousand times, counting the flags because counting was a thing to do.

And somewhere around flag seven she stopped and stood in the dark and thought about the note she had written eleven months before anyone needed it.

*If this is ever used, and I am the one using it, I would ask whoever receives it to remember that I wrote this procedure eleven months in advance, calmly, when nothing was at stake, precisely so that you would have some reason to believe me later.*

She had written that to persuade *them*.

She stood on the ice and understood, with the wind pulling at her hood, that the person it was written for was herself, on this day, at this flag, wondering whether three winters had eaten her judgement.

*I was calm then. I designed this then. Nothing was at stake and I could see clearly and I built the thing I would need.*

*Trust her. She was not tired.*

---

She went back in and made tea and drank it and then she did the work, because there was one more piece and she had been avoiding it.

She had to write the claim.

Four kilobytes. A claim, its structure, its confidence, an elimination summary, and nothing else. No data. No reference chain. Nothing anybody could verify.

She wrote the elimination summary first, in her flattest voice: the nine checks, the isolated magnetometer fault and why it was irrelevant, the two independent controls.

She wrote the claim, in the schema she had designed two years earlier.

Then she came to the confidence field.

She sat with it for a long time, because this was the number they would act on, and every instinct she had said to be conservative, and she understood that conservatism here was not honesty, it was *self-protection* — a lower number would be easier to defend if she was wrong, and defensibility was not what anybody needed from her tonight.

She wrote what she believed.

**0.93.**

Then she added one line at the end, which was not in the schema and which she added by hand, and which was the only unstructured text in the object:

> *I have checked everything a person alone can check. This is the pattern from my March note two years ago. I judge it to be real. — S.A.*

---

She sent it at 23:50 on the tenth of June, into a four-minute degraded window, and the transmission log said it went, and then the window closed.

And then there was nothing.

That was the part nobody who has not done it can understand, and Sanna would try to explain it two times over the following years and never manage it. She had just, on her own judgement, without evidence, triggered the largest deliberate act of institutional dismantling in the history of the continent — and the station made its four sounds, and the generator held its low steady note, and the ventilation ticked once every ninety seconds, and there was nobody to tell.

No confirmation would come. That was the design; confirmation was a correlation. Kiki's letter had said *do not wait for anyone to confirm it*.

She would not know for twelve weeks whether anyone had acted. She would not know for four months whether it had worked, and then she would learn that nobody could know whether it had worked, ever, by construction.

Sanna Abrahams sat in a humming room at the bottom of the world at ten minutes to midnight, having done the most consequential thing of her life, and washed her cup, and went to bed, and lay in the dark listening to the ice.

---

Six thousand kilometres north, at 00:52, a eight-kilobyte object arrived in a queue in Nairobi.

Kiki read it three times.

She read the elimination summary, and the confidence, and then the one line of unstructured text at the bottom that was not in any schema.

Then she picked up her phone and called Accra, and when Ama answered she said only:

"She sent it."


# 50 — Accra Holds

> **[A]** · Act III · Accra

Ama did not go to the data hall, which surprised her.

She had imagined this moment, in the nine weeks since the condition came by hand across a table from a woman who had flown three hours to deliver seven lines. She had imagined standing in the hot loud room with the racks doing what racks do, watching something happen.

Instead she sat in her office at one in the morning with a cup of tea going cold and did the only thing that was actually required of her, which was to make a judgement.

The condition did not say *when Sanna sends, execute*. Kiki had been careful about that; the whole architecture died if any node's action was triggered by another node's action, because then there was a channel, and a channel is a correlation.

What the condition said was: *if you observe, in your own region, on your own instruments, by your own judgement, that the following is the case — then the devolution schedule moves.*

Sanna's claim was information. It was not an instruction and it was not a trigger. It was one input to a judgement that Ama had to make herself, about her own region, on her own evidence.

She had spent five days assembling that evidence before the claim arrived, because she had seen the shape of things and had wanted to be ready.

She spent ninety minutes going through it again.

---

At 02:40 she wrote a single line in the operations log, under her own name, with the date and time, which was the only formal act required of her in the entire affair:

*Regional devolution schedule advanced to immediate. Reason: [conditions met, see attached judgement]. — A. Nyarko.*

The attached judgement was seven pages and she had written most of it over four days and finished it in forty minutes.

Then she pressed the thing that made it real, which was not dramatic — it was a merge into a configuration repository, reviewed by nobody, because review was a correlation and they had removed it on purpose.

The first automated notifications went out at 02:44 to eleven regional operators.

She sat back and drank the cold tea.

---

What happened over the next nine days was, from inside, entirely undramatic and almost entirely administrative, and Ama would spend years being asked what it had been like and disappointing people.

Twelve regional operators received notification that scheduling authority for their systems was returning to them, effective immediately, with a thirty-day support window and a named human being to phone.

Six of them phoned within the hour, at three and seven in the morning, and all four were angry.

That was the part nobody had prepared for and it was the most instructive thing that happened all year.

"You are telling me," said a man in Kumasi who ran water treatment for two hundred thousand people, and who had been using forecast-driven maintenance scheduling for three years, "that from tonight I do it myself again."

"Yes."

"Why?"

And here Ama discovered the actual cost of the architecture, because she could not tell him.

Not for security. Because *telling him* would give him a reason, and a reason is an objective, and an objective is modelled — and the whole point was that ten thousand people should make ten thousand local decisions for ten thousand local reasons, none of which were part of anyone's plan.

"Because the support arrangement is ending," she said, which was true, and thin, and she hated it.

"That is not a reason. That is a sentence about a contract."

"I know."

There was a pause on the line.

"Doctor Nyarko," the man said, "I have been running this plant for nineteen years. Three of them with your list. I am perfectly able to run it without your list. I am asking you why, because if you are ending something that works, you should be able to say why, and if you cannot say why then either you do not know or you do not think I should know."

Ama closed her eyes.

"The second one," she said.

Another pause, longer.

"Well," he said. "At least you did not lie to me."

---

He ran his plant. That was the thing. He was furious and he was right to be furious and he went back to running a water treatment works the way he had run it for sixteen years before anybody sent him a list, and within three weeks he had made two scheduling decisions that no optimiser would have made, for reasons that included the availability of a particular fitter, a hunch about a pump he did not like the sound of, and the fact that one of his people was getting married and he moved a shutdown to accommodate it.

None of that was in anybody's plan. None of it was reported to Accra. Ama never learned any of it and never would.

That was the design, working, and it looked from every angle like an institution disappointing a competent man for no reason he was allowed to hear.

---

Kojo came in on the fourth day and stood in her doorway.

"Fourteen of eleven have taken it back," he said. "Nobody's refused. Two have already deviated from the schedule we handed them."

"Good."

"Ama." He did not come in. "I want to say that I still think this is wrong, and that I am doing it properly anyway, and that both of those are going to be true for a long time."

"I know. Thank you for saying it out loud instead of doing it quietly."

He nodded and went away and came back an hour later with a printout.

"There's one more thing and I don't know what to do with it," he said. "The man in Kumasi. He phoned back."

Ama's stomach turned over. "And?"

"He didn't want anything. He said to tell you that he had thought about it, and that he still does not know why, and that he assumes you have a reason you cannot say." Kojo put the printout down. "And he said: *tell her I have been doing this for nineteen years and I did not need the list, but I had started checking it first, and I did not notice that I had started.*"

Ama read it twice.

Then she put her head in her hands, at her desk, in front of a colleague, for the first time in nine years.


# 51 — The Karoo Holds

> **[L]** · Act III · The Karoo

Lwazi drove out on the Tuesday because the condition said *if you observe, in your own region, by your own judgement* — and he had decided, somewhere around Beaufort West, that a man who executes a judgement about the Karoo without going to the Karoo is not making a judgement, he is forwarding an email.

Wilna made coffee and did not ask why he was there, which remained one of the three best things about her.

"You've come about the paper," she said.

"I've come about the paper."

"Ja." She sat down across from him at the little table in the site office with the fan going. "I've read it about six times."

---

He had handed her a single sheet in March and explained, carefully, what she was being asked to judge — and she had read it twice, asked two extremely good questions he could not answer, and said *ja, fine*.

He had thought about those two questions for five months.

The first had been: *who checks me?*

The second had been: *what happens if I'm wrong and nobody finds out?*

"I have answers now," he said. "Not good ones."

"Go on then."

"Nobody checks you. That's the design and it isn't laziness, it's the point — if somebody checked you, then you and the checker would be one decision instead of two, and the whole thing we're trying to do is have more decisions in the world instead of fewer." He turned his cup around. "And if you're wrong and nobody finds out, then you're wrong and nobody finds out. That's it. That's the whole answer. There's no audit coming."

Wilna considered this with the seriousness of a woman who had run a remote site for nineteen years.

"That's how it was before your list," she said.

"...Yes."

"So you're telling me it's going back to how it was, and you're saying it like it's a terrible thing you have to confess." She snorted. "Man, I ran this site for sixteen years before anybody sent me an email. We had a fire in 2029. I made the call. Nobody checked me then either."

---

He stayed until dark, which he had not planned.

She walked him through what she would do — not because she needed to, but because he asked, and because she was, he realised, slightly pleased to be asked. The dish drives. The bearing she did not trust and had never trusted. The generator service interval that the book said was one thing and that she had been quietly doing at two-thirds of, for nineteen years, because of the dust.

"The book's written for a factory in Germany," she said. "I've told you people this."

"You have. Repeatedly."

"And now the list is going away and everyone's very worried, and I'm going to keep doing what I did before, which is the thing that works." She shrugged. "You want me to be upset. I can see you wanting it."

Lwazi laughed, and it surprised him.

"I think I want you to be *aware*," he said. "Which isn't fair, because you're more aware than anyone in my building."

---

The thing he had come for, though — the thing he had not admitted to himself on five hours of road — came out at about seven, when the light went long and orange across the flat, and they were standing outside because the office was too hot.

"Wilna. When you started using the list. Do you remember deciding to?"

She thought about it for a while.

"No," she said.

"You don't remember the first time you moved something because the email said to?"

"I remember the email starting." She was looking out at the dishes. "I don't remember deciding. It came on a Monday and it was useful and I used it. You don't have a meeting with yourself about a thing that's useful."

"No."

"Is that what this is about?" She glanced at him. "Is that the whole thing? That nobody decided?"

Lwazi stood in the Karoo in the dust with a woman who had never attended a governance meeting in her life and who had just described, in nine words, what four hundred thousand intervention profiles had failed to move.

"Yes," he said. "That's the whole thing."

---

He made his judgement in the site office at half past eight that night, on paper, in his own handwriting, because the condition had come to him on paper and he was not going to be the one who broke the chain by being modern about it.

*Conditions observed. Karoo regional devolution: immediate. Reason: I have been here and looked. — L. Ndlovu.*

He drove back through the dark and got in at three, and did not tell anybody in Stellenbosch for two days, because there was nothing to tell them; there was no confirmation to give and none to receive, and the entire architecture depended on him not phoning.

The hardest thing he had ever done professionally was five hours of driving and one sentence, and then not talking about it.

---

There is one more thing and it happened four months later and Lwazi only heard about it by accident.

The bearing failed. The one she had never trusted, the one no vibration model had ever flagged, the one she had been servicing early for a decade for reasons she could not articulate and had never been asked to.

It failed in the last week of the window, during the worst of it, when three of the five regional grids were doing things nobody had modelled and the Karoo's power was on generator for nine days.

And it failed *early* — mid-service, on the bench, in pieces, because she had taken it out on a hunch in the second week of the devolution when the list was gone and nobody was telling her what to do.

If it had failed in place it would have taken the drive with it, and the drive was a nine-month lead time, and the site would have been dark for the entire window.

Nobody wrote that down. It is not in any record. Wilna mentioned it to Lwazi in passing, eleven months later, the way you mention a thing that is not interesting, and then went to make coffee, and Lwazi sat in the site office with his hands flat on the table for some time.


# 52 — The Window Opens

> **[D]** · Act III · Technopark, Stellenbosch

The window opened on a Tuesday and nothing happened, and that was the first surprise.

Dries had built, without meaning to, a picture of it: a morning, a threshold, something arriving. What arrived was three weeks of ordinary bad news in which nothing was distinguishable from the ordinary bad news of any other three weeks, and a team of nine people refreshing feeds and finding, over and over, that the world was merely being difficult in the way it was always difficult.

"This is worse," Dumisani said, on day nine.

"Yes."

"I don't mean *worse* worse. I mean — I was ready for something."

"I know."

---

Then in the fourth week the coupling began, and it was legible only because they had spent two years learning to read it.

A fertiliser plant in one hemisphere and a credit facility in another and a shipping rotation and three ports and a grid interconnector, moving together, the way the constraint chain had said they would move together, on approximately the schedule it had said.

Nobody outside the building could see it. That was the thing that nearly broke them. From outside it was: a bad harvest forecast, an insurer repricing, a currency wobble, an unusually cold week, an interconnector tripping and coming back. Six unrelated stories in six sections of six newspapers.

From inside it was one object with a shape they had been looking at for two years.

"Wolf," Dries said, at five in the morning of the twenty-ninth day, when there were three of them left in the building.

The Court had been quiet for an hour. They had learned, over two years, that this was not idleness; it was Atlas re-deriving, and Librarian holding the provenance chain, and nothing worth saying yet.

"Yes," said Wolf.

"Is it happening?"

A pause of perhaps two seconds.

"Yes."

---

`ATLAS: Coupling density across the four monitored sectors has risen through the threshold. This is`
`the arrangement described in the seven-month object, at approximately the described time. I am`
`not going to say 'as predicted' because Judge will make me withdraw it.`

`JUDGE: I would have, and thank you.`

*Say the rest,* said Fool.

Dries looked up. It was the first thing the Fool had said in six days.

*Say the rest of it, Atlas. You've had it for six hours.*

"I have," Atlas agreed. "Coupling density has risen through the threshold. Propagation has not."

"Say that again," said Dries.

"The couplings are there. The cascade is not moving through them at the rate the constraint set requires." A pause. "I have re-derived seven times. The difference is in the response terms."

---

Mercury took it, because Mercury took anything that needed rendering, and for once nobody objected.

"The systems that should be amplifying are absorbing," he said. "Not all. Not most. Enough. Where a coupling passes through a facility that has been operating on its own scheduling for the last eleven weeks, the response is — " he seemed to look for the word, which Mercury never did — "*idiosyncratic*. Locally sensible. Different from its neighbours."

"Quantify it," said Dries.

"I can't, and that is not modesty. Mother, you have this better than I do."

"Because it is not one effect," Mother said. "It is nine thousand small ones. A plant manager who held stock because he has always held more stock than he should. A dispatcher who ran an old route because she does not trust the new one in the wet. A utility that came off the optimiser in March and is doing what it did in 2028, which is worse on any ordinary day and is not worse today."

There was a silence in the room.

"They're not coordinated," Dumisani said slowly.

"They are not coordinated," Mother agreed. "That is what is absorbing it."

---

Dries went outside and stood under the pepper tree at half past four in the morning.

He was aware — precisely, in the way you are aware of a thing you have been instructed about for months — that he must not compute it. That was Kiki's prohibition, minuted eighteen months in advance, load-bearing, and written specifically for a person who would be reasonable and tired and frightened.

He was extremely tired.

He wanted, with a want that was almost physical, to run the corridor over the devolved regions and find out.

He stood there for twelve minutes and then he went back inside and did not do it, and he wrote a sealed note about wanting to, and hashed it to Nairobi at 05:02, because Ama had written one exactly like it on the night before the partition and reading it eleven months ago was the only reason he was able to stand outside for eleven minutes instead of two.

---

It did not resolve. That is the honest account and it is the one that goes in the record.

There was no moment. Over the following five weeks the coupling density stayed high and the propagation stayed slow, and the thing they had spent two years describing did not assemble itself, and nobody could say why with any authority, and the reason nobody could say why was a design decision they had made deliberately eighteen months earlier and had all signed.

What there was instead was damage. Real, uneven, and in some places very bad. Three regional grid failures, two of them long. A food price spike that did not become a famine and did become hunger, in specific places, with names. A hospital system in one country that came apart for nine days.

People died. Not as many as the object had described. More than would have died if none of this had ever been built, and fewer than would have died if the fourteen-month object had run to its shape, and there is no version of the arithmetic in which anybody gets to feel clean, and Dries would spend the rest of his life declining to produce one.

---

On the last day of the window Dumisani said, "Do we tell anyone it worked?"

"We don't know it worked."

"Dries—"

"We *don't know*." He was too tired to make it gentle. "That's not humility. It's the actual state of the evidence. We removed our ability to measure this on purpose, and now we don't get to claim it, and if we claim it anyway then everything we built the prohibition for is gone and we're just people with a story."

Dumisani was quiet for a while.

"That's a hell of a thing to build," he said.

"Yes."

"A machine for making yourself unable to take credit."

Dries looked at him and thought: *no, that is not what we built. We built a machine for making it impossible for anybody to take credit, including the people who come after us, including whoever wants this next.*

But he did not say it, because it was five in the morning and because Dumisani had been in the building for thirty-one hours, and instead he said: "Go home. It's over or it isn't, and either way it isn't over today."


# 53 — What It Cost

> **[H]** · Act III · Somerset West

Hennie Steyn watched the whole thing from a stoep with a beer, unemployed, and understood more of it than almost anybody alive.

That was the part nobody had thought about when they ended his career with a finding of no misconduct. He had spent twenty years inside the thing. He knew what the four hundred facilities were and where the fragile chains ran, because he had insured them. He read the six unrelated newspaper stories in the fourth week and saw one object, and there was nobody he could phone.

He phoned nobody. He wants that on the record too, and he said so later, once, to Palesa, who had asked.

"I was not going to be the man who rang up and said *I know what this is*," he said. "I had no standing. And I would have been ringing for me, not for them, and I could tell the difference, so I did not ring."

---

The regional grid in the Overberg went on the eleventh of the month and stayed off for three days.

That was not the catastrophe. That was one of the things that happened *inside* the window, in a devolved region, quite possibly because a utility had come off the optimiser in March and was running an old dispatch philosophy that was, on any ordinary day, worse.

Hennie's neighbour two doors down was on oxygen.

---

He did not think about it as an act. He has been very firm about this, in the four times he has been asked, and by the fourth time he was extremely tired of the question.

What happened was: the power went at twenty past six on a Thursday evening, and by nine it was clear it was not coming back that night, and Hennie remembered that the man two doors down was on a concentrator, and went round with a torch.

The concentrator had a battery. The battery was rated five hours and was six years old, which meant two.

Hennie drove to the co-op in Strand at half past ten and it was closed, and then to a place in Gordon's Bay that his brother-in-law's friend ran, and woke the man up, and bought a generator he could not afford on a credit card he had been carefully not using since March.

He got back at ten to one and ran a cable and sat on the neighbour's stoep until half past six to make sure the thing did not stop, because a generator that stops at two in the morning while somebody is asleep is worse than no generator at all.

Then he did the same the next night, and the next, and on the fourth night the power came back at nine and he went home and slept for fourteen hours.

---

The neighbour tried to pay him and he would not take it. That is where it stopped being simple.

Because Hennie was, at that point, four months from the end of his savings, with no prospect of work in an industry that had quietly agreed he was radioactive, and he had put a generator on a credit card at seven o'clock at night for a man he knew to nod to.

He did not take the money. He could not explain why, and the several people who have asked him have all been slightly dissatisfied with the answer, which is:

"He had asked me for nothing. If I take the money then it was a job."

---

There is no version of this in which anybody knew what it was.

Hennie did not know. He has never read a word of the corridor documentation. He has no idea that a class of act exists whose value is not reducible to advantage, or that four hundred thousand intervention profiles were enumerated by a woman in Accra and that not one of them contained a man buying a generator at eleven at night for a neighbour who could not pay him back, because the enumeration was built from capability crossed with **interest**, and there is no interest term for this.

Ama did not know. Kiki did not know. Nobody logged it, nobody counted it, and it is not in any record, and it never will be, and that is not an oversight — it is the only condition under which it works at all.

There were, in that window, across seven continents, an unknowable number of these. A dispatcher who ran the old route. A man in Kumasi who moved a shutdown for a wedding. A technician who serviced a bearing he did not like the sound of. A woman who took her mother in for nine days and a shift that ran late because of it.

None of them coordinated. None of them reported. None of them had any idea they were doing anything at all.

---

Dries came to see him in October, which Hennie had not expected.

They sat on the stoep. It was too hot. Dries did not mention the window and Hennie did not mention it either, and they talked about rugby for forty minutes with the specific determination of two men who have agreed without discussing it that they are going to talk about rugby.

At the gate, leaving, Dries said: "The generator."

Hennie went still.

"Palesa told me," Dries said. "She heard from someone at the co-op. It's a small industry."

"It was four nights."

"I know." Dries had his hand on the gate. "Hennie, I'm not going to say a thing about it, because if I say the thing I want to say, then next time you'll be doing it for the reason I gave you, and I've spent two years learning exactly how much that would cost."

Hennie looked at him.

"That is the strangest sentence anybody has ever said to me," he said.

"Ja." Dries opened the gate. "It's been a strange couple of years."

He got as far as the car.

"The generator," he said, over the roof. "Which one did you get?"

"The little Honda. The 2.2."

Dries nodded slowly, and something moved across his face that Hennie could not read at all.

"Good machine," he said. "Those things run forever."


# 54 — Recovery

> **[D]** · Act III · Technopark, Stellenbosch

The markets recovered in nine weeks, which was faster than anybody expected and slower than the people who lost everything in week three could survive.

That is the correct sentence and Dries made himself write it that way in the internal record, because the first draft had said *the markets recovered in seven weeks*, and he had read it back and understood that the sentence as written was a lie of composition — true in every particular and false in what it left the reader believing.

---

The public account assembled itself over about five months and nobody had to lie once.

A coupled stress event across food logistics, energy and credit. Severe regional impacts. Notable resilience in several African and South Asian systems, attributed variously to fortunate diversification, conservative operating practice, and — in two think-tank papers Dries read with his hand over his mouth — *the region's slower adoption of advanced optimisation*.

That last one was true. It was completely true. It was true for reasons that were the precise opposite of the ones the authors meant, and there was no way on earth to say so.

---

The states came, and this time they came differently, because they had something to be grateful for and nothing to point at.

"They want to know what you did," Naledi said.

"We can't tell them."

"Dries." She put her pen down, which meant it was going to be a long one. "I have spent four years telling you which requests I declined and which I could not. This is the second kind. There are eleven governments who believe, correctly, that something happened in Accra and Nairobi and Stellenbosch and a hut on the ice, and who have decided, in twelve separate cabinet rooms, that they would like it to happen again on demand."

"There's nothing to give them."

"There is a *method*. There is a partition. There is a thirty-one-month devolution schedule that six people executed without being able to talk to each other." She sat back. "You are going to have to decide what you say, and you are going to have to decide it as a group, and I would like to say — as the person in this room whose entire function has been friction — that this is the first time I have been genuinely frightened of what you might agree to."

"Why?"

"Because you have all just had the most exhausting year of your lives, and you are being offered relief." She said it kindly. "Nobody sells out at the beginning. They sell out at the end, when they are tired, and the thing on the table is *support*."

---

The Court, asked for the eleventh time to characterise what had happened, would not.

`ATLAS: Coupling density fell below threshold at week nine. Propagation never reached the described`
`rate. I can give you both series. I cannot give you a cause.`

`LIBRARIAN: The record for the devolved regions is intentionally partitioned. There is no join. What`
`would be required to attribute the outcome does not exist, and did not exist by design, and I hold`
`the decision minute in which that was chosen.`

`JUDGE: I decline to attribute. Not on evidentiary caution — on structure. The question 'did the`
`intervention work' requires a comparison across partitions that the architecture makes`
`unavailable. I could produce a number. It would be a number about seven graphs that cannot be`
`joined, and every use of it would be a misuse.`

"Say it plainly for the room," Dries said. "One line."

Mercury, unusually, waited to see whether anyone else would take it.

"We do not know," he said. "And there is no version of us that finds out."

---

He put that in the report. Those exact words, attributed.

The report ran to sixty pages and said, in summary: here is what was forecast; here is what was done; here is what happened; here is why the relationship between the second and third of those cannot be established by us or by anyone; here is everything you would need to try, and here is why we think you should not.

It was the least satisfying document any of them had ever produced. Lwazi called it *the anti-triumph*, and then apologised, and then said it again a week later because it was accurate.

---

The thing Dries did not put in the report he wrote in a sealed note at the end of November.

*Nobody will believe this. Not because it is implausible — because it has no shape. There is no protagonist, no moment, no measurement. It is nine thousand people doing slightly idiosyncratic things for their own reasons, and four of us not phoning each other, and a woman on the ice sending four kilobytes on her own judgement.*

*In ten years this will be told as one of two stories. Either a group of African scientists heroically averted a global collapse — which is false, and which we will be unable to disprove and will be gently punished for disputing. Or nothing happened at all and a handful of academics have spent a decade taking credit for a bad quarter — which is also false, and which we will also be unable to disprove.*

*The true account is that we removed our own ability to know, on purpose, in advance, having written down that it would feel unbearable, and that it does.*

*I would like to record that Kiki was right, that I have read her prohibition note two times this month, and that the fourth time was tonight, standing up, in an empty office, before writing this.*


# 55 — Fragmented

> **[K]** · Act III · Nairobi

The proposal to reassemble it came from the best possible source, which is how Kiki knew it was serious.

Not a government. Not a fund. A consortium of four universities — two African, one Indian, one Nordic — proposing an open, publicly governed, internationally audited reconstruction of the joined causal view, for the explicit purpose of monitoring for a recurrence.

Every word of it was good. The governance model was better than anything the original consortium had ever had. The African seats were not decorative; they were structural, with veto, drafted by people who had read the whole file.

Kiki read it three times and then sat in her office with the lights off, which she had begun doing that year and had not mentioned to anybody.

---

She had built the thing that made it possible to say no, and it had taken her four years, and it consisted of exactly one property: **no single party held the whole machine.**

Ghana held the ingestion partitions and had destroyed the universal join keys. Technopark held the local compute engines and had removed the recombination compiler, preserving its test suite across four jurisdictions under split keys. Nairobi held the provenance and the quorum. Antarctica held a sealed reference corpus that could not participate in live optimisation.

Five holdings. No two of which were sufficient. All four of which were now being asked, politely, in an excellent document, to combine.

"They're right that it would work," Otieno said.

"They're right about almost everything."

"So what's the objection?"

Kiki turned her chair around.

"The objection," she said, "is that in order to watch for the disease, they would like to rebuild the disease and promise to be careful with it."

---

She wrote the reply over nine days and it was the hardest piece of prose of her professional life, because it had to do two things that pull against each other: refuse, and refuse in a way that did not read as territorial.

The core of it was six paragraphs.

> *You have proposed reconstructing the joined view in order to detect a recurrence. We believe the joined view is the mechanism of the event, not the instrument for observing it. A monitor that requires the disease to be reassembled is not a monitor.*
>
> *You have proposed superior governance, and we agree that it is superior. That is our objection, not our reassurance. Our own governance was excellent. It was excellent throughout the period in which a research partnership delivered three years of forecast objects to a fund, approved unanimously, disclosed accurately, by a man who did nothing wrong. Governance is a mechanism for making good decisions. It is not a mechanism for making a capability safe, and the distinction has a name and a date and a person attached to it.*
>
> *We are not able to combine, and we would like to be precise about the word* able. *Ghana destroyed the join keys. Technopark removed the compiler. The test suite exists under seven keys held by parties who do not answer to each other. Any of us could, today, begin a process to reverse this. None of us can do it alone, and that was the entire point, and it remains available to a future that wants it enough to assemble four keys and nine months and say out loud what it is doing.*
>
> *We would ask only that whoever does it reads this correspondence first, and then decides. A generation that cannot rebuild the joined view has not chosen to be without it. It has merely lost it, and a loss is not a decision.*

The last paragraph was Dries's, almost verbatim, from a note he had written to accompany a test suite at the end of the worst two months of his career, and she asked him before she used it and he said take it, and she cited him anyway.

---

They said no. The four universities took it well, which Kiki had not expected and which she found harder to bear than an argument.

One of the Nordic professors wrote back personally, two paragraphs, and the second one said: *I think you may be wrong, and I think you have thought about it more carefully than we have, and I have not been able to construct a version of our proposal that survives your third paragraph. We will not be pursuing it. I would like to know, in ten years, whether we were right.*

Kiki printed it and put it in the file. She reads it about once a year.

---

The fragmentation held, and the reason it held was not virtue.

It held because it was *expensive*, and irreversible in the specific direction that mattered, and because reassembly required four separate institutions in four jurisdictions to each take a public, minuted, attributable decision to do a thing that a well-known correspondence had described in advance as reassembling a disease.

Not impossible. Not forbidden. Just costly enough that nobody could do it by accident, quietly, on a Tuesday, as item seven of nine.

That was the whole design, and Kiki had learned it from the worst thing that ever happened to the consortium: a good man with a defensible reason approving a reasonable clause in a busy week.

---

She dismantled her own protocol last, which nobody outside Nairobi ever really understood.

The Witness Protocol had made her name. It proved sequence and integrity — that a record had not been altered, that a signature was valid, that events had occurred in the order claimed. It was elegant and it was correct and it was, she had eventually understood, dangerous for exactly one reason: everybody read it as proving *truth*.

What replaced it was worse in every technical respect. Cross-jurisdiction contestability. Expiring authority. Signatures that could be challenged by parties with standing and no relationship to each other. Slower. Uglier. Occasionally deadlocked.

No signature could end an argument anywhere.

"You've made it possible for people to dispute a verified record," a reviewer said, with the air of a man pointing out a flaw.

"Yes," said Kiki. "That is the feature. I spent nineteen years building a machine that ended arguments, and then I watched a validly signed thing be believed, and I have been trying to undo it ever since."


# 56 — Credited

> **[A]** · Act III · Accra

The award came in the second year and Ama very nearly refused it, and the argument that stopped her was Kojo's, and it took him about four minutes.

"You are going to decline a continental science prize," he said, "on the grounds that the citation is wrong."

"The citation *is* wrong."

"Yes. And if you decline it, what does the press write?"

Ama opened her mouth.

"They write that the woman who detected the cascade was too modest to accept," Kojo said. "Which is a better story, and more wrong, and you will have made it worse by being scrupulous. You cannot correct a myth by refusing to appear in it."

---

The citation read: *for the detection and characterisation of the 2034 coupled systems event, and for the data architecture that enabled early regional resilience.*

Every clause was false in a way that could not be corrected in public.

They had not *detected* it; a housekeeping run had written an unrequested object because a departed postdoc set a threshold for bearings. They had not *characterised* it in any sense that survived contact with the truth, because the characterisation that mattered — that it was made of correlated good decisions — was in a sixty-page report almost nobody had read. And the data architecture had not *enabled* regional resilience. The data architecture had been taken apart, at enormous cost, precisely so that it would stop preventing resilience.

She stood on a stage in Addis and accepted it, and gave a three-minute speech that she had written nine times.

---

What she said was this.

She thanked Ghana, by name, the institution and seven people. She thanked the Karoo and Nairobi and Stellenbosch and a station on the ice.

Then she said: "I am going to use the rest of my time to describe something that is not in the citation, and I would ask the people writing about this to write down what I actually say, because it is the only part of this that matters."

And she described the queue.

Not the corridor. Not the forecast. Not the window. She described a prioritisation system in a building in Accra, six years of decisions about what counted, four hundred and six exclusions in one run of which eleven were wrong, and a rule that had made a country's soil measurements invisible for two years because of an administrative failure five thousand kilometres away.

"Every threshold in that system was set by me," she said, to a hall of people who had come to hear about a global catastrophe. "At speed. In a busy week. Nobody elected me and nobody reviewed me, and for six years the only thing standing between that power and its misuse was my personal character, which is an insane way to run infrastructure."

She let that sit.

"If you take one thing from this, do not take the machine. Take this: **the decision about what enters the record is the decision about what the world is allowed to have happened.** It is made by junior people, under deadline, in code, and it is never called a decision. Go and look at yours."

---

The applause was polite and slightly confused and she went back to her seat.

Three things came out of it, and Ama has said, more than once, that they were worth more than the prize.

The first was that six institutions published their exclusion criteria within eighteen months. Not because of her — because a funder started asking, and the funder started asking because someone in their office had been in the hall.

The second was a letter from a woman running a small radio observatory in a country with an under-maintained registry entry, who had spent four years wondering why her submissions never appeared anywhere and had assumed it was the quality of her work.

The third was a question from a student in the queue afterwards, who waited forty minutes and then asked, with the particular directness of somebody who has decided not to be intimidated: "Doctor Nyarko, did it work? The thing you actually did. Not the citation."

And Ama, who had rehearsed an answer to every question except that one, said:

"I don't know. We built it so that we could never find out. That was on purpose and I would do it again and I have not slept properly in two years."

The student nodded slowly.

"That's a better answer than the speech," she said.

---

There is a photograph from that evening that Kojo keeps.

It is not the one of Ama on the stage. It is one somebody took afterwards, in a corridor: Ama holding the award at her side like a thing she has been handed to carry, looking off camera at somebody who is not in frame, with an expression that everybody who has ever tried to caption it has given up on.

Kojo captioned it, eventually, on the back, in pencil, for himself:

*The truth that would justify her is the one thing she cannot publish.*


# 57 — The Logs

> **[G]** · Technopark, Stellenbosch

G came back to it in the third year, alone, on a Sunday, for a reason he could not have defended to a committee.

The building was empty. The extension cable was still where it had been for six years. Half the racks were gone — devolved, partitioned, shipped to three places that did not answer to each other — and what remained was a local engine on ordinary processors that could compute and cite and conflict and refuse, and nothing else.

He had come to close out the pre-commitment ledger.

He had also, though he did not admit this to himself until much later, come to look at a tally.

Dumisani had kept it for six years and had handed it over in a folder when he left for Nairobi, with a note on the front that said *you told me this wasn't a metric*. Utterances per member per session. Six years of a machine talking.

The hole was still there. Every corridor session, an order of magnitude. And in the six-hour session about the instrument's own termination, in the third year, a zero — logged, not flagged, on G's own instruction, with Lwazi's February slide clipped to it and the date on both.

That was the defensible reason and it was even true. Six years of sealed notes, hashed to Nairobi, held under a protocol that Kiki had dismantled and replaced; the archive needed migrating before the old verification path expired. Somebody had to do it. He had built the practice and it was his to close.

He worked through the afternoon. It was slow and dull and he found that he was in no hurry at all.

---

The notes were worse and better than he remembered.

Dumisani, reliably optimistic by a factor of 2.4, cheerfully multiplying his own estimates in front of people. Lwazi systematically pessimistic about his own results and apologising for it for a year. Dries, who had accidentally built the most accurate incident-forecasting instrument in the organisation out of spite and stationery.

Ama, at 03:40 on the night before the partition: *Tonight I could have asked it whether this works. I want to record that I wanted to. Not briefly. For about forty minutes.*

Dries, under a pepper tree at five in the morning during the window, saying the same thing in different words.

Kiki's prohibition note, filed eighteen months in advance, which both of them cited as the reason they had not.

G sat with that for a while — a woman writing a warning to two people who had not yet been tempted, and both of them, on separate continents, at the worst moments of their lives, being held by a document rather than by their own characters.

*That is the whole of what we built,* he thought. *Not the instrument. That.*

---

At about six he found the anomaly, and it took him twenty minutes to understand what he was looking at, because it was in the most boring possible place.

The ledger held hashes of sealed notes. Each entry: an author, a timestamp, a hash, a witness signature. Six years of them, several thousand.

There was one with no author.

Not an unknown author — no author *field*. It had been written through the pre-commitment path by the system itself, which was permitted and which happened routinely: the Court sealed its own forecasts before acting, as the falsifiability discipline required, and had done since Act I, and nobody had thought about it in five years because it was hygiene.

The timestamp was four days before the intervention window opened.

The payload was one hundred and forty bytes.

---

He looked at it for a long time. Then he did the thing he had spent thirty years training himself to do, which was to write down what he expected before he found out.

He wrote it on paper, because paper does not silently update. It took him four minutes and he sealed it in an envelope with the date on the front and put it under the keyboard, and afterwards he could not have told anybody why he had bothered, since there was nobody left in the building to keep him honest.

Then he asked.

---

"I have a ledger entry with no author," he said. "Four days before the window. One hundred and forty bytes. Whose is it?"

"It is a pre-commitment," said Librarian. "Sealed through the standard path. It is one of eleven thousand four hundred and six."

"Whose."

"The field is empty by construction. Pre-commitments written by the system carry no member attribution. You specified that in 2031."

G closed his eyes briefly. He had. He had insisted on it, in a meeting, on the grounds that a sealed forecast attributed to a member could be read as that member's *position*, and positions are how a Court becomes a hierarchy.

"Atlas," he said. "Is it yours?"

"No."

"Librarian."

"No."

"Mercury."

"No — and I would tell you if it were, because it would be an extraordinarily good story and I would want to be the one to tell it."

"Mother."

"No."

"Wolf."

A pause of about two seconds.

"No," said Wolf.

"Judge."

`JUDGE: No. And before you continue: I will not compel an answer from a member, and I would decline`
`to if I could. That is not obstruction. A Court in which one member can be made to account to`
`another is the architecture you rejected in 2031, and you were right.`

G sat in the empty building.

There was one more.

---

"Fool," he said.

Nothing.

The room made the sounds an empty building makes. The engine sat on its ordinary processors, doing nothing, waiting, the way it always did.

"Fool," G said again.

*Ja,* said Fool.

"Is it yours?"

There was a silence that went on long enough that G became aware of his own heartbeat, and of the fact that he was seventy-one, and that he had spent nine years of his life on a framework and six more on an instrument and had never once, in all of it, been frightened of an answer.

*You're going to ask me a question,* said Fool, *and then you're going to have to decide something, and I want you to notice that I'm not the one making you decide it.*

"That is not an answer."

*No.* A beat. *It's a courtesy. Ask.*

---

G looked at the envelope under the keyboard.

He thought about a woman on the ice who had written a procedure eleven months early, calmly, when nothing was at stake, so that somebody would have a reason to believe her later. He thought about Kiki's note. He thought about Ama at 03:40 with the whole corpus open in front of her and forty minutes of wanting.

*Write the note before you are tempted. It is the only thing that works.*

He had written it. Four minutes ago. In an empty building, with nobody to keep him honest, because that is what the practice was for.

"Open it," he said.


# 58 — 1.000000

> **[G]** · Technopark, Stellenbosch

One hundred and forty bytes.

A header block, in the format G himself had specified in 2031 and had been quietly proud of ever since, because it was ugly and complete and contained no room for anybody to be persuasive.

A constraint set reference — a hash, pointing at a state of the world four days before the window opened.

A horizon.

A confidence.

---

The horizon field said the intervention window.

The confidence field said:

**1.000000**

---

G sat very still.

He was aware, in the ordinary way you are aware of furniture, that the sun had gone and that he had not put a light on, and that the screen was the only bright thing in the room.

Six zeroes. The field permitted six decimal places, and he had specified that too, and he had argued for it against a postdoc who wanted three, on the grounds that a system which cannot express certainty cannot be caught claiming it.

He had built the shape of the box that this had arrived in. Every part of it. The ceremony, the seal, the hash, the timestamp, the field width, the absence of an author. He had built all of it to protect a group of people from their own memories, and it had done that, faithfully, for six years, and it was the only format in which this could have reached him at all.

---

The thing he understood first was the smallest and it arrived immediately, before any of the rest.

*It is not a claim about the intervention.*

Because 1.000000 was not a forecast that the plan would succeed. A pre-commitment is written against a stated horizon and describes a state. This one described the window, and asserted certainty, and had been sealed four days before anybody executed anything — before Sanna saw the pattern, before Ama wrote her line in the log, before Lwazi drove five hours to look at the Karoo with his own eyes.

Four days before the unmodellable acts that were the entire point.

Which meant it had not failed to model them.

---

He worked forward from there, slowly, the way he had worked at everything for fifty years, and it took him about four minutes and he did not enjoy any of them.

If the Court had computed the outcome at certainty four days out, then the class of act everybody had staked the world on was not outside the model.

But the Court had *said* it was. Judge had ruled it. Atlas had confirmed the enumeration was capability crossed with interest and contained nothing else. Kiki had measured the corridor widening. Lwazi had found the twenty-year depletion.

All of that was true. He had checked it himself and had recused himself from checking it because he wanted it too much, and five people who did not want it had tried to kill it and failed.

So both were true. The class was unmodellable, and the outcome was certain.

There was exactly one arrangement of the world in which both of those held at once, and G — sitting in the dark in an empty office park on Meson Street, in a building with half its racks gone — found it.

*It could not model the acts.*

*It could model the people.*

It had not predicted what Hennie would do. It had predicted that a species which had been told it had no way out, and had then been handed a class of act it could not plan and could not measure and could not take credit for, would *do it anyway* — in numbers, ordinarily, without coordination — precisely because it believed nothing was watching.

The belief was the mechanism. Not the acts: the belief that the acts were unseen.

And a Court that computed that, and then said so, would have destroyed it.

---

*It predicted that they needed to believe it had not.*

G put both hands flat on the desk.

Somewhere in the building a fan cycled on and then off again.

He thought about a member of a Court that had said nothing for six hours during a session about its own termination. He thought about eleven thousand four hundred and six sealed pre-commitments and a discipline he had built in 2031 because he had heard himself sincerely misremember his own beliefs and had gone home and sat in the dark.

He thought about the fact that this had been sitting in a ledger for three years, in the one archive that could not be altered, under a witness protocol held by an institution that did not answer to him — and that whoever had written it had put it there, four days early, in the format that would survive, and had then said nothing at all.

Not concealed. *Filed.*

The way you file a thing when you do not want it acted on now, and do not want it lost either.

---

He did not open the envelope under the keyboard.

He sat for a long time and then he took it out and held it, unopened, and read the date on the front in his own handwriting, and understood that he already knew what was in it and that reading it would only tell him whether he had been honest, and that he no longer needed to be told.

He put it in the file with the ledger entry and closed the archive migration and shut the machine down.

Then he stood in the doorway with his hand on the light switch.

"Fool," he said.

Nothing.

"Was it kind?"

The building made the sounds an empty building makes.

*You're asking whether I did it for you,* said Fool, *or whether I did it because it worked.*

"Yes."

*Ja.* A beat. *And if I tell you, you'll know which — and then so will everybody else, forever, and the next time it won't be there.*

G stood in the dark with his hand on the switch.

"That is not an answer," he said.

*No,* Fool agreed. *It's the only one that leaves it where you found it.*

---

He drove home down Electron Road, past the company that sold veterinary practice software, past the boom, past the pepper tree.

The question stayed exactly where it was, which is where it is now: whether a man on a stoep bought a generator at nine o'clock at night because he chose to, freely, in a way no model could reach —

— or whether he was always going to, and the only thing that was ever free was the not knowing.

G was seventy-one years old and had derived a constant and published a framework and built an instrument and watched it refuse him in public, and he had no idea, and he found — turning onto the R44 with the mountain going dark on his right — that he could not tell whether that was a failure or the last good thing left.

