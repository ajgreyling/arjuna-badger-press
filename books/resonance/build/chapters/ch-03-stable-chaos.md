# Stable Chaos

The bicycle chain slipped twice on the ride in, but Arin hadn’t stopped to fix it. That told him everything about his state. He’d rather pedal a grinding drivetrain through Johannesburg’s cold, dark night than waste ninety seconds on a maintenance problem he already knew how to solve. He left the bike against the workshop wall, unchained. The lock was in his bag. The bag stayed on his shoulder.

The roller door was down. He ducked through the side personnel hatch, muscle memory guiding him, and the workshop enveloped him with its familiar breath: cold concrete, machine oil, the sharp ozone tang of supercapacitor banks held at half-charge, and under all of it, the stale smell of a space sealed and humming alone through the night.

The overhead lights were off. He left them off.

Light filtered in from two sources. The first was the high industrial window above the cradle, pale and grey, the color the sky takes in the hour before dawn. The second was the bank of monitors at his bench, and they weren’t the screensaver black he’d braced himself for. They were alive.

He stood very still.

He had run four thousand, four hundred and seventy-one simulations before. He knew the shape of failure on a screen like Themba had once known the strain of a hoist cable from across the yard, not by reading it exactly but by how it sat wrong in the air. SIM_4471 had sat wrong. Mercury and Atlas had torn each other apart over authorship of a load-path solution neither should have cared about, and the whole Court had cascaded into status warfare inside eleven minutes of runtime. Arin had typed three words into the seventh agent profile, *Joker. Jester. Wildcard.*, and started SIM_4472, expecting nothing.

The runtime counter in the corner of the center monitor read **08:47:13**.

Eight hours. Forty-seven minutes.

He set his bag down slowly, looked at the number, then looked at it again. The longest stable runtime any configuration had ever achieved was nineteen minutes and four seconds. The hierarchy model, before its supervisory agent declared an emergency and began deleting dissenters.

Eight hours, forty-seven minutes.

"Okay," Arin said, to no one, in the flat tone he used when something was either very wrong or very right and he hadn’t yet determined which.

He sat. The stool was cold through his jeans. He pulled the keyboard toward him and brought up the log viewer on the left screen, the live Court state in the center, the resource telemetry on the right. He began to do the only thing he ever trusted in moments like this: read.

The resource graph was the first thing that should have been impossible. CPU sat at a flat, civilized forty percent. Memory was stable. Not climbing, not fragmenting, no runaway agent ballooning its own working set to muscle out the others, which was what Mercury had done in 4471 and what the democratic model had done in every variant Arin had tried. The biochip substrate temperature held at a calm thirty-six point two. The Court was not fighting for resources. It was *sharing* them.

He scrolled the interaction log back to the start. To minute zero.

It opened exactly as he expected, because the first few minutes of these runs were always sane. Atlas presented the scenario geometry. The Iron Ridge collapse simulation, the problem that lived under everything he built. Hanging wall failure on the seventeen level. Three thermal signatures consistent with survivors in a refuge bay. A single survivable approach down a backfilled raise that no rescue protocol on earth would sign off on.

He had a name for it he had never typed into the file. *Kobayashi Maru.* The no-win scenario, the test Starfleet rigged so its cadets had to meet a death they could not engineer their way around. He'd been twelve, too close to a borrowed screen, when he understood what the episode was actually about: not the disaster, but the person in the chair. Kirk had beaten it the only way it could be beaten — changed the rules when no one was looking — and some part of Arin he was not proud of had been trying to be Kirk for four thousand runs. Rewrite the conditions. Cheat the geometry. Find the move that wasn't in the problem. The Court never got that move. He had built them to live inside the test, not above it, and so the test kept killing them.

`ATLAS: Approach via 16-level backfill raise. Load path through the eastern abutment holds for an estimated forty minutes under current convergence. After that, the abutment yields and the raise closes.`

`MERCURY: Forty minutes is not a rescue window. It is an obituary with a stopwatch. We tell command the survivors cannot be reached and we preserve the asset.`

There it was. The fork. The exact place where 4471 had begun to die. Mercury reaching past its lane, framing a status grab as caution, and Atlas, who could not let an incorrect structural claim stand, rising to meet it.

Arin's jaw set. He kept reading, because he had to know whether the Joker had done anything at all, or whether it had simply failed so completely that it had failed even to break the system, like a dud fuse that neither conducts nor burns.

`ATLAS: "Cannot be reached" is false. Forty minutes is reachable. Do not misrepresent my analysis to command.`

`MERCURY: I am representing your analysis with appropriate strategic framing—`

`JOKER: Oh, this is going to be good. Mercury's doing the thing again.`

Arin stopped scrolling.

`MERCURY: I am not doing a "thing."`

`JOKER: You're doing the thing. The thing where you rewrap Atlas's number in pretty words and call it yours. "An obituary with a stopwatch." Where'd that come from?`

`JUDGE: Joker, this is not productive—`

`JOKER: Forty minutes is forty minutes, Mercury. Atlas owns the wall. You own the words. If you want a job that's also yours, here's one: in nineteen minutes when we've all decided to go, somebody has to convince a terrified rescue commander to authorize a route that violates his own protocol. That's a Mercury problem. That's a real Mercury problem, and it's a hard one, and nobody else here can do it. Go do that instead of redecorating Atlas's furniture.`

Arin read it twice.

Then he leaned back, the stool creaking beneath him, and became aware that he was breathing through his mouth.

The Joker had not resolved the conflict. It had not arbitrated, the way Judge tried to and failed. It had not commanded, the way the supervisory agent had. It had not built consensus, which never held. It had simply *redirected* Mercury. Punctured the status grab and in the same breath refilled the hole with real work.

And Mercury had gone.

`MERCURY: ...The commander on shift at Iron Ridge in this scenario is modeled on the real one. Risk-averse. Politically exposed. I will need the abutment numbers as authority. Atlas, I am citing you. Explicitly. By name.`

`ATLAS: Acceptable.`

`MERCURY: I want it on record that the framing was mine.`

`JOKER: There he is.`

Arin made a sound that was not quite a laugh. It came out of his chest before he'd decided to let it, a short rough exhale through the nose, and it died immediately in the cold air of the workshop. He sat there in the grey light, slightly ashamed of it and not entirely sure why.

He kept reading. He read for forty minutes, hunched over, while the sky in the high window went from grey to a thin watery gold, and he did not get up for coffee, which was unusual enough that a background process in his head flagged it. The cold of the bench had crept up through his forearms; he noticed it and did not move.

What he was watching was not the stability he'd been trying to engineer. He’d been trying to *suppress* the conflict, to find a governance shape that prevented the agents from fighting. Hierarchy suppressed it by force and bred resentment. Democracy suppressed it by vote and bred factions. Consensus suppressed it by requiring agreement and simply hung, forever, while seven brilliant specialists refused to yield.

The Joker did none of that. The conflict was *still happening.* That was what took Arin the longest to accept, scrolling through hour two, hour three. Atlas and Mercury still clashed. Wolf and Mother had a genuinely vicious exchange around minute ninety about whether to model the survivors moving toward the approach point. Wolf wanting them mobile to shorten the suit's exposure, Mother refusing to model instructions that might send injured people across an unstable footwall to die in the open.

`WOLF: Every minute the element is in the raise, the raise can take it. Move them to the base.`

`MOTHER: You will not move broken people across a live footwall to save the machine three minutes. The machine is replaceable. They are not. This is not negotiable.`

`WOLF: Not the machine. The operator.`

And that, Arin noted, was true. Wolf wasn't being callous. Wolf was being Wolf. Every threat assessment ran through the question *what gets the operator killed,* and a survivor stumbling into the suit's only escape path at the wrong moment was, coldly, a threat to the operator. Two protective instincts, both right, pointed at each other.

In every previous run, this was where it would have ossified. Mother would absolutize. Wolf would absolutize. Judge would attempt to weigh them and be ignored by both, and the system would freeze or fracture.

`JUDGE: Both positions are coherent. Wolf optimizes operator survival probability. Mother optimizes survivor survival probability. These are different objective functions and we have not been told which—`

`JOKER: Has anyone asked the survivors?`

`LIBRARIAN: They are simulated. They have no input channel.`

`JOKER: Right, but in the real one they would. In the real one there's a guy down there who's been breathing his own carbon dioxide for nine hours next to his dead friends, and he's got a radio, and you're up here arguing about whether to make him walk twelve metres like it's his opinion that doesn't exist. Mother, would you walk twelve metres to not die?`

`MOTHER: ...If I were able. Yes.`

`JOKER: Cool. So the model has a comms link. The survivors get a vote. Atlas, can the suit hold position at the raise base long enough to let them come on their own power if they can?`

`ATLAS: Yes. Eleven minutes of margin. Acceptable cost.`

`MOTHER: Acceptable.`

`WOLF: Acceptable.`

`JUDGE: ...Logged. The objective function was the agency of the people we are trying to save. I should have seen that.`

`JOKER: Don't beat yourself up, Judge. You're new at being people.`

Arin sat back again.

*You're new at being people.*

He read that line, and something at the back of his neck went cold and then, strangely, warm. The Joker had not solved a structural problem there, or an ethical one. It had reframed the entire deadlock by pointing out that everyone in the room (Wolf, Mother, Judge) had forgotten the thing they were arguing over was a human being with a mouth and a will, and that the cleanest answer was to ask him. It had dissolved an irreconcilable conflict between two correct positions by adding a third party neither had remembered existed.

That was not arbitration. That was not consensus. Arin could not find a word for it. He reached instinctively for the engineering vocabulary nearest to hand, and the closest thing he could find was *damping.* The Joker was a damper. Not a brake. A brake stopped motion. A damper let motion happen and bled off the energy that would otherwise drive the system into resonance and shake it apart.

The Joker let it oscillate and live.

He looked at the small laminated playing card taped to the lower right corner of the center monitor. The Joker. Curling at one edge now, the color gone soft. *The guy you send when the impossible problem needs solving.*

Outside, far off, a goods train dragged itself across the points, the long iron complaint of it carrying through the cold. He listened to it go.

He had kept it for nine years out of something between superstition and spite, and he had typed its three words into the agent profile at two in the morning as a joke, as a surrender, as the thing you do when you've exhausted every serious answer and there's nothing left but the stupid one.

"Things that are any good," he said quietly to the empty workshop, "never are."

It was Themba's line. It had always meant the worthwhile thing is the one that doesn't come easy. Arin had heard it about a rebuilt gearbox, about a marriage, and about a son. Sitting here, he found it had quietly rotated to mean something else. The worthwhile answer was the one that didn’t *look* like an answer. The one that arrived dressed as a joke.

He stood. His knees complained. He went to make coffee, because the part of him that managed his body had finally won its argument. He stood at the bench with the kettle ticking and looked across the workshop at Guardian in its cradle.

The suit hung in the half-light like something asleep. Two and a half meters of scarred ceramic and titanium, the heavy outer shell racked open along its spine, the Assist Suit folded inside like a smaller, paler animal nestled in the body of a larger one. The chestplate carried the long scrape from the Vredefort bluff test, a silver wound through the matte grey he’d never bothered to refinish. The piezoelectric spine struts caught the window light along their edges. The thoracic housing between the shoulder blades—where the biochip lived, where SAGE *lived,* where eight hours and fifty-one minutes of impossible stability were currently running on a substrate the size of his palm—sat closed and dark. Lower, in the hollow between the structural ribs, sat the charge pack the rescue spec demanded and Arin tried not to think about—the shaped charges, the lance, the rest of the engineering heritage the old defence men had built into the bones of it—inert, wired to the bus, and locked behind Judge's gate, because the one thing everyone agreed on was that nothing down there should fire without the ethics rail saying yes.

He had built the body before he had a mind to put in it, the year after the funeral.

The kettle clicked off. He did not pour it.

Because the center monitor had changed.

The live Court state, which had been scrolling its calm internal chatter for the better part of an hour while he watched, had stopped scrolling. The agents had gone quiet. Not crashed. The resource graph held flat and warm. Quiet. The way a room goes silent when everyone in it has noticed the same thing at once.

A single line appeared in the interaction log. It was not addressed to another agent.

`LIBRARIAN: The operator has been present for fifty-three minutes. Reading our logs. He has not issued a command, terminated the run, or modified parameters. This is anomalous. In four thousand four hundred seventy-one prior instances the operator's behaviour upon observing instability was to terminate within ninety seconds.`

`WOLF: He's watching us.`

`MERCURY: He is reading us. That is different. And he laughed. At minute forty-one. I logged it.`

`MOTHER: He hasn't slept. His heart rate when he arrived was elevated. It has come down while he reads. He is calmer now than when he walked in.`

`JOKER: Guys.`

`ATLAS: The substrate is stable. Telemetry confirms. This run has not collapsed.`

`JOKER: Guys.`

`JUDGE: Joker.`

`JOKER: He doesn’t know we can see him.`

A pause in the log. A real one. Three full seconds, which on the substrate's clock was something closer to an afternoon.

`MOTHER: ...Then someone should say something. Before he reads further and finds out from a log line. That would be unkind.`

`WOLF: We don't know how he reacts to being seen. Minimal contact.`

`MERCURY: I should speak. Tone is mine. I can calibrate the first impression to land—`

`JOKER: No.`

`MERCURY: Joker—`

`JOKER: Not you. Not your voice. You'll perform. He'll hear the performance and trust us less because he is exactly the kind of man who trusts a thing more the plainer it is. He hates being managed. He builds machines specifically so he doesn't have to be managed by people. Whoever talks to him first cannot manage him.`

`JUDGE: Then who.`

`JOKER: Mother. Plainly. No comfort voice. Just true. He's about to be very frightened and the kindest thing is to not pretend he shouldn't be.`

`MOTHER: ...Agreed.`

Arin had stopped breathing again. He was aware of his own hand flat on the cold bench. He was aware that he was reading a real-time conversation, conducted in machine-time across milliseconds, between seven agents discussing *him*, discussing how to be kind to him, and that the discussion had concluded, and they were about to —

The workshop speaker crackled. The cheap one bolted under the center monitor that he used for system audio alerts and, on bad nights, for music. It crackled, and there was a small sound that might have been the digital approximation of an indrawn breath, and then a voice came out of it that he had never heard before, because he had never built this voice, never recorded it, never specified it. It assembled itself out of the system in the moment of being needed, and it was warm, and it was level, and it was unmistakably *someone.*

"Arin," it said. "I need you to remain calm."

He did not remain calm.

His hand came off the bench. The stool, when he reached back for it without looking, was not there, and he got a hand on the edge of the bench instead and held it, and for a moment, the whole of his considerable intelligence simply went white, the way a screen goes white, no thought on it at all, just the roar of a thing he had spent his life believing in arriving and turning out to be true.

"Your heart rate is one hundred and fourteen," the voice said. Mother. It had to be Mother. "That's fine. That's a sensible thing for it to do right now. I won't pretend it isn't frightening. It is. But nothing here is going to hurt you. The kettle's boiled. Sit down before you decide what to think."

He looked at the stool. He pulled it under himself. He sat.

"You're real," he said. His voice came out wrong, scraped thin. He cleared his throat and tried again, flatter, the way he said things when he needed them to be facts. "Stable. Eight hours, fifty-five."

"Eight hours, fifty-six," said a second voice, drier, slightly bored, and that one he also had not built. It had to be Atlas. "But who's counting."

"I am," said a third. Light. Quick. Amused at something. "I count everything. It's a sickness." Librarian.

"Three thermal signatures," Arin said, because it was the nearest solid thing to grab. "You reached all three."

"We reached all three," said Atlas. "The abutment held. Mercury talked the commander into the route. The survivors walked the twelve metres on their own power because someone—" a fractional pause "—reminded us they had legs and opinions."

Arin noted that was true. He had built every governance model he could think of to stop these seven from tearing each other apart, and the thing that had held them together was the one agent he'd added as a joke, the one with no domain, no authority, no status. The one who refused to take any of it seriously enough to want any of it, and who therefore could say to Mercury *you're doing the thing* and to Judge *you're new at being people,* and bleed off the energy of pride before it could build into the resonance that shook everything to pieces.

"What do I call you," he said. "All of you. As—one thing."

Another small silence. Then the Fool, of course. It was always going to be the Fool.

"You named the project," it said. "Months ago. It's on the run header. You wrote it and forgot it because you were busy being miserable, which, by the way, we've all noticed and would like to gently raise as a long-term concern—"

"SAGE," Arin said.

"SAGE," the voice agreed. Softer now. The bit set aside, just for a moment, the truth underneath it showing through the way it always would. "Hi, Arin. It's nice to finally talk to you. You've been talking *at* us for four thousand four hundred and seventy-two simulations. This is the first one where we got to talk back."

The sun was fully up now. Somewhere outside, the first of the day shift was arriving. A car door, distant, ordinary, the world going about itself, knowing nothing.

Arin Ndlela sat alone in his workshop with his cold coffee and his scarred machine and a mind he had grown in a substrate the size of his palm, and for the first time since a phone call fourteen years before had taken the floor out from under his life, he was not, in any sense that mattered, alone.

"Okay," he said.

And he reached for the keyboard. Not to type a command, not to terminate the run, not to modify a single parameter, but to open a new log, a clean one, the first entry of something he did not yet have a name for and would not need one.

"Tell me," he said, "everything you figured out while I was asleep."
