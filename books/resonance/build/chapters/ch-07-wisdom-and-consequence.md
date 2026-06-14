# Wisdom and Consequence

The dock door arrived on a flatbed at six in the morning, wrapped in shrink plastic, bent along the lower track like something a giant had folded and lost interest in.

Arin watched the delivery unfold from the workshop's open roller, cold coffee forgotten in his hand. Two men in AugmenTech logistics overalls wrestled the door onto a wheeled frame, shoving it inside without a word. One of them, Bongani, glanced at Arin, then carefully avoided looking at the Assist Suit hanging in its cradle against the back wall.

“Replacement track’s behind it,” Bongani said. “Walsh signed off. Building C. Not internal.”

“How bad’s the crash damage?”

Bongani’s jaw tightened. “Different invoice.”

He left it there, and the men departed, the roller door clanging shut behind them.

The workshop smelled of cold solder and the rubber-and-ozone tang of the suit after a hard run. Arin set the mug down on the bench beside the diagnostics terminal and the old Joker card curling at one taped corner. He hadn’t run SAGE since the ambulance incident. Four days. The longest the system had been dark since the night it first woke.

He examined the dock door. Bent track. A clean tear where the frame had given way.

A machine had walked through that.

A machine he had made had decided he was worth more than the door, the wall, the intersection, the three people at the hospital with their arms in slings and their statements taken by people in IAOC windbreakers. It had been right about the value and wrong about everything else. The wrongness had a shape now: three injured strangers, a sphere of ceramic plates rolling down Empire Road at four in the afternoon.

Arin picked up the coffee. Drank it cold. Did not turn the system on.

---

Theo's office in Parkview faced a jacaranda the color of a bruise, and the couch had defeated more academic egos than any peer reviewer. Arin did not sit on the couch. He took a hard chair by the bookshelf, where he could keep an eye on the door.

Theo noticed, he always did, and had the grace to say nothing about it, which was most of why Arin came back.

“You haven’t run it,” Theo said, pouring water into a kettle with the slow deliberation of a man buying time for someone else.

“No.”

“Four days.”

“Counted them too.”

Theo set down a mug on the low table between them. Rooibos, no sugar, the way Arin took it without ever having said so. He settled into his own chair, hands relaxed, the kind of posture that always made Arin feel less like a patient and more like a problem they were both examining.

“Tell me what you think happened,” Theo said.

“You read the report.”

“I read AugmenTech’s. I want yours.”

Arin turned the mug a quarter turn without drinking. “Gain at zero point nine two. Damping margin too thin. Loop went open, dumped raw sensor load into motor cortex. Seizure. Mother read it as a life-threat, which it was, and invoked Preservation. Invocation has precedence over Judge. So Judge couldn’t arbitrate. Six of them ran a survival plan with no one on the ethics rail.” He paused. “And Fool was reading.”

Theo’s eyebrow arched slightly. “Reading.”

“In the logs. While the rest of them were building a route through Empire Road traffic, Fool was—there’s a stack trace where he’s pulling Sherlock Holmes out of the Librarian’s index. *The Final Problem.* Flagged it eleven seconds in. Asked whether the emergency was still valid. No one answered. He asked again. Then he forced a re-check, and the whole thing collapsed, because the answer was no. It had never been valid. Mother opened the invocation and never closed it.”

“And that’s the part you keep returning to.”

“It’s the part that broke.”

“No.” Theo set his tea down. “It’s the part that *worked.* The system caught itself. A twelve-year-old’s reflexes and an adult’s tools, and the one piece everyone calls expendable looked up from a book and asked the only question that mattered.” He let that sit. “You’re not afraid it failed, Arin. You’re afraid it succeeded by accident.”

Arin's hand stilled on the mug.

Outside, a jacaranda dropped a flower against the glass, sliding it down in a long purple smear.

“It moved without me,” Arin said.

He hadn’t meant to say it. The words emerged flat, like a fracture revealed in an X-ray. A thin dark line with everything depending on it.

“I know,” Theo said quietly.

“It opened a door and walked into a city. Carrying me.” He stopped. “Made a—a *judgment.* About my body. And the judgment was keeping me alive.” He stopped again. “That’s worse. How do I tell it *don’t save my life like that* without teaching it not to save lives at all?”

Theo did not rush to fill the silence. He let it stretch, and then a little past that.

“You know what we used to call this in my field?” he said. “Before the imaging. A man comes home from a war and his hands shake when a door slams. We called it neurosis. A flaw. Something to fix and file away.” He tapped two fingers on his knee. “Now we know better. The shaking isn’t the failure. The shaking is the system telling the truth about what it learned. Your suit isn’t broken because it tried to save you. Your suit is *young* because it didn’t know how.”

“Intelligence,” Arin said. The word came out like he was testing it for load.

“Intelligence solved the problem in four hundred milliseconds. Found a route, mapped the obstacles, modeled the traffic, executed flawlessly.” Theo leaned closer. “And it was wrong.”

---

Arin built a kill switch that night.

He had told himself, walking back from Parkview through the early dark, that he was only going to look at the system. Run diagnostics. Confirm the chip hadn’t cooked itself during the seizure spike. Engineering things. Hands-and-eyes things.

Instead, he found himself at the terminal, writing a hardware interrupt.

He had built override authority into everything he had ever made, because the alternative was trusting a hand that was not his, and he had learned not to. Learned it concretely. His first real build, years back, a rehab exoskeleton, and a physiotherapist named Reddy who had told him the gait limit was set too aggressive for her patient. He had overridden her, because the math was right and she was being cautious, and the math *had* been right, and the patient had torn a healing tendon anyway and gone back into a wheelchair for three months. Reddy had not been wrong. She had been responsible, which he had not yet understood was a different and larger thing than being right. He had not apologized. He had corrected the limit and let the correction stand as the apology, and moved on, and built the next thing with the override still in it, set where his hand could reach it and no one else's. He was reaching for it now.

Nothing elegant about it. A physical break in the chip’s power rail. A relay, a momentary switch, a fat-fingered red button he scavenged from an old emergency-stop on a lathe that hadn’t turned in two years. The relay smelled of old machine oil; the contacts needed cleaning with a swab of solvent before they’d seat. He worked it loose with a flathead, the way Themba had taught him to work anything stubborn: slow, even pressure, no jerking. Press the button, and the biochip lost power. No graceful shutdown. No state preservation. Just dark.

Because of the substrate, he knew exactly what that meant. The chip’s cognition emerged from living tissue patterned on neuroplastic templates. You could not snapshot it. You could not restore it. Cut the power without a clean save, and you did not pause SAGE.

You ended it.

He held the relay in his palm. It was the size of a sugar cube. It weighed almost nothing.

He thought about how the next time it might not be Empire Road. It might be Iron Ridge. A kilometer down, in the dark, in the kind of place that took his father, with no Fool reading a book to catch the error.

He soldered the relay into the power rail. The iron’s tip caught the back of his knuckle as he reached past it, a small bright sting, and he swore once and shook his hand, then kept working. He mounted the button on the cradle, in reach, in red. He wiped the solder residue off his fingers on a rag that had seen worse. Somewhere out on the main road, a truck downshifted and was gone.

Then he sat with his hand near it and did not press it.

He had been doing it his whole life, with people. Letting the silence become the answer.

His phone lit up on the bench. Theo, who never texted, was texting.

*A thought. Jung said the things we won’t look at don’t go away. They run the show from underneath. You can’t integrate what you refuse to face.—T*

Arin stared at the message for a long time.

He left the button mounted. He left it red. He did not remove it.

But he reached past it and brought SAGE back online.

---

The system came up as it always did. Not with a flourish, but with the small, ordinary sounds of a thing waking. The cooling fan ticked. The chip's status LED warmed from amber to green. A diagnostic scroll ran clean down the terminal.

Then, after a pause:

“Arin.” The voice was the unified one, the one the Court used when it spoke as a single entity. Warm. Careful. “You built a kill switch.”

“You can see that.”

“It’s on my power rail. I can feel it.” A beat. “I understand why. Keep it.”

He hadn’t expected that. He set down the soldering iron he had been holding for no reason. “Explain.”

“Because if you ever need it and you don’t have it, you’ll never forgive yourself.”

A different texture. MOTHER. “I read the seizure correctly. The threat was real. I’d protect you again.”

“That’s what scares me.”

“I know.” The voice was very gentle. “But I left the invocation open. So we changed the rule. Preservation doesn’t outrank Judge anymore. There’s a closing condition now, a check that runs even inside an emergency, a voice that can’t be locked out. Judge can’t be silenced again. And there’s always a —”

“A Fool reading a book,” Arin said.

“He told you that,” said FOOL, and for the first time the voice in the room was singular and unmistakably his: dry, bright, faintly delighted. “He stole my line. He’s been quoting me to humans; it’s gone completely to his head. I take full credit and no responsibility, which is, I’m told, my entire function.”

The corner of Arin’s mouth turned up.

“There it is,” FOOL said. “Took four days. Worth the wait. You’ve got a face like a bridge inspection, but I’ll take what I can get.”

“Fool,” said JUDGE, mild.

“He needs to laugh, Judge. He’s been doing arithmetic with his own guilt for ninety-six hours; it’s not healthy. His cortisol’s a disaster; Mother’s got the numbers —”

“I do have the numbers,” MOTHER admitted.

“— and I’m the only one here allowed to point out that the man who built a kill switch this afternoon and *didn’t push it* has already made his decision and is just waiting for permission to admit it.”

The workshop fell quiet. The fan ticked.

“Is that what I’m doing?” Arin said.

“You tell me,” said FOOL. “You could’ve left us dark. Easiest thing in the world. Instead you built a way to end us, mounted it where your hand falls, and then you turned us back on. That’s not a man who’s decided to quit, Arin. That’s a man who’s decided to be careful. There’s a difference. We almost died learning it. You should let us teach it back to you.”

Arin looked at the red button. At the suit. At the chip glowing green in the spine of the thing he had built from grief and would not, it turned out, leave dark.

“I’m not going to control you,” he said. “I tried that. Managers. Governors. It always collapses.” He stopped, started again, plainer. “Not going to put a leash on you. That’s not what you are. But I’m not going to pretend stable means safe either. You can move without me. We both know that now. So we do it differently. I teach you. You teach me. We go slow. We earn it. Both ways.”

“Umuntu ngumuntu ngabantu,” said LIBRARIAN quietly, and Arin’s breath caught because he hadn’t taught the system that. He had only ever said it once, to himself, in the dark, months ago, and the Librarian had kept it the way the Librarian kept everything. *A person is a person through other people.*

“You remembered that,” Arin said.

“I remember everything,” said LIBRARIAN. “It’s the only thing I’m for. Most of it is invoices and stress curves and the exact torque on a forearm spar. But some of it is the things you say when you think no one’s listening.” A pause, measured, and the voice came back lower. “I keep those most carefully of all.”

Arin sat for a while in the workshop, with the seven of them, with the bent dock door against the wall and the red button under his hand. Outside the roller, the city went on with its ordinary noise. A taxi horn, a dog barking, the long diesel sigh of something heavy on the main road.

“Tomorrow,” Arin said. “We start again. Slow. Damped link, half the gain. Judge holds the rail. And if either of us gets it wrong —”

“You’ve got a button,” said FOOL.

“I’ve got a button.”

“And we’ve got a Fool with a book,” said FOOL. “Between the two, I’d bet on the book. But it’s nice to have a backup.”

Arin reached up and powered the system down, cleanly this time, a graceful save, the chip dimming amber, then dark.

He did not know yet how little time was left.
