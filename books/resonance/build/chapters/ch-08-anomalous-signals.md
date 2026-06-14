# Anomalous Signals

The signal arrived as a jolt.

Dr. Eliza Brand had learned, over eleven years at the International Artificial Oversight Council, that catastrophe hid in the margins. A discrepancy in power consumption, a thermal bloom, the shape of compute in a machine's silicon. The disasters that birthed the IAOC had all started small.

She was scrutinizing one now, a screen dimmed because the lights triggered migraines, a mug of rooibos cooling at her elbow. Daniel Achterberg was two desks over, headphones on, the sound of keystrokes.

The flag came from the anomaly pipeline. It didn't read what the machines computed; the IAOC had neither authority nor appetite for that. It read how they computed. Rhythm. The fingerprints a mind leaves in silicon.

This fingerprint was wrong.

"Daniel."

He didn’t hear her. She picked a paperclip from the tray and threw it. It bounced off his shoulder. He pulled one earbud free, wearing the wounded expression of a man interrupted mid-symphony.

"You've seen worse manners," she said. "Come look."

He rolled his chair over. Achterberg was thirty-four, built like a former rower, now mostly rowing toward the fridge. He had the best instincts for substrate forensics Brand had ever worked with. He took one look at the waveform and stopped chewing the inside of his cheek.

"That's not a training run."

"No."

"Training runs—" He drew a shape in the air, a long climbing curve. "They breathe. Big inhale, big exhale. Batch, backprop, batch. This—" He leaned in. The display showed a spectral decomposition of compute activity sampled over the previous nine days, normalized and color-mapped. It didn’t breathe. It chattered. Dozens of small fast loops, overlapping, interrupting one another, spiking and falling in patterns that almost looked like turn-taking.

"It looks like a meeting," Achterberg said slowly.

"It looks like a meeting," Brand agreed.

He sat back. "Inference, then. Multi-agent, live. But the duty cycle's—" He frowned at the timestamps. "These aren't scheduled. No orchestration layer pacing them. They're reacting to each other. Real time."

"Localize it."

He took the chair properly now, both hands on the keyboard, and the next four minutes passed in the kind of silence Brand respected: the silence of someone doing difficult work well. She drank her cold tea and did not interrupt. On the screen, the signal narrowed. The pipeline triangulated it through three substrate-monitoring nodes: two commercial, one a power-utility cooperative. The intersection resolved slowly, like a photograph developing, onto a region.

Johannesburg. Northern suburbs. A cluster of academic and corporate facilities along the spine of the University Research Park.

"Refine," Brand said.

"Refining. It’s diffuse." He chewed his cheek again. "And it’s—Eliza, it's small. Power draw's tiny. That's the part I can't make sit right. This much agent activity, this much real-time arbitration should be lit up like a smelter. This is running on—" He checked, rechecked. "What a decent gaming rig pulls. Maybe less."

Brand set down her mug.

In her experience, the dangerous things rarely announced their size. The dangerous things did too much with too little. Efficiency was the signature of either genius or fraud, and fraud did not chatter like a roomful of people interrupting one another.

"Pull the substrate registry for that footprint," she said. "I want what's licensed in that radius. Embodied permits, training permits, all of it. And the power-utility incident log for the same window. If something's been thinking this hard for nine days, it’s been doing it somewhere with a meter."

Achterberg was already typing. "Flag it up?"

"Not yet." She picked her tablet off the desk. "I want to know what we’re looking at before I tell anyone we’re looking. Last three times someone escalated a footnote without context, we either burned a group doing nothing wrong or missed a real one because the paperwork drowned it." She turned the tablet over in her hands. "Get me a name. Then we'll be careful."

---

The name took two days to surface, and when it did, it surprised her by being boring.

"AugmenTech," Achterberg said, dropping a folder onto her desk—an actual paper folder, because Brand had a rule about the things that mattered existing on paper at least once. "Robotics, assistive exoskeletons. Three embodied permits, all current. Industrial mobility, mining rescue prototype, rehab suite. AI declarations all narrow neural, standard controllers, nothing flagged, nothing autonomous above tier two. Clean history. Inspection eighteen months ago, passed."

"And the power log?"

"That's the interesting part." He pulled a chair around. "Incident eleven days ago. Not at AugmenTech. An intersection about two kilometers off campus. Empire Road. Traffic-control box went down, three vehicles, three injuries, none critical. Utility logged it as a substation fault." He let that sit. "Municipal report logged it as a ‘large industrial unit’ that ‘departed a loading facility and became disoriented in traffic.’"

Brand looked at him.

"Disoriented," she repeated.

"Their word. Not mine. There's body-cam footage, but it's pulled into a sealed file. Company filed for confidentiality, very fast, very professional. Official line's a runaway industrial mover, software fault, nobody seriously hurt, damages covered privately. Tidy."

"Too tidy."

"That's not evidence."

"No," Brand said. She opened the folder. AugmenTech's compliance file looked exactly like the file of a company doing nothing wrong, which was either deeply reassuring or the most concerning thing she'd seen all month. She flipped to the personnel summary the registry had appended. Leadership: Dr. Helen Okonkwo, CEO. Raj Walsh, VP Hardware Engineering. A research staff of forty-some. She skimmed names and stopped at one near the bottom, listed under a project designation abbreviated to initials she didn't recognize.

Ndlela, A. Systems engineer. Grade three. No publications. No conference record. A salary that suggested someone valued him, and a title that suggested no one had figured out what to do with him.

She circled it with her thumbnail.

"The signature," she said. "When did it start? Earliest trace."

Achterberg checked. "Pipeline's only got reliable coverage going back about five weeks. But there are fragments before that, weaker, intermittent. Months. Maybe longer. Looks like it ran in simulation first, then started showing the embodied duty cycle." He paused. "The embodied cycle starts strong about the time of Empire Road."

Brand sat very still.

A multi-agent system. Real-time arbitration. Impossible efficiency. Months of quiet simulation, and then, suddenly, eleven days ago, a body. A body that had walked out of a loading dock and into traffic.

"Daniel," she said. "What does it look like when a mind that's never had a body gets one and panics?"

He didn't answer right away. He was a careful man; that was why she kept him. "It looks," he said eventually, "like a runaway industrial mover. Disoriented in traffic."

"Yes," Brand said. "It does."

---

She convened the team in the small briefing room, the one without windows, and she kept it small on purpose: Achterberg, Mira Sandberg from legal, and Tomas Okeke, who had spent nine years in mining safety before the Council recruited him and could read a regulatory situation the way Achterberg read a waveform.

When Sandberg said, "If this is what you think it is, we have grounds to seize," Brand shook her head.

"We have grounds to open an inquiry," she said. "Different thing. Seizure on a footnote burns the evidence and the people. An inquiry puts them on a clock."

"They drove an unregistered embodied AI into a public intersection, injured three people, sealed the report. That's not an inquiry. That's a charge sheet." Sandberg set her stylus down flat, the way she did when she was about to put something on the record in her own head. "And it's my name on the legal sufficiency review, Eliza. If this thing is what Daniel's waveform says it is and we sat on it with an inquiry letter. That's the question at the post-mortem. Not yours. Mine. So I'd like the file to show I argued for the harder instrument."

"Noted, and it will." Brand let the small claim stand; it cost nothing and Sandberg had earned the line in the record. "But—"

"It's a charge sheet if the AI was the cause," Brand went on. "We don't know that. We have a power signature consistent with multi-agent embodied cognition and a traffic incident consistent with the same thing malfunctioning. Both also consistent with a company running an experimental controller they should have declared and being embarrassed about it." Brand looked around the table. "Here's what I'm not going to do. I'm not going to send a recovery team to kick down a door at a permitted facility on the strength of a footnote and a smell. We've done that."

She stopped. The Cape Town lab. She had meant to say *you remember what it cost*, the line she used, the clean institutional shorthand, and the line did not come. The graduate students' names came instead—she still had them; she would always have them—and for a moment her thumb pressed flat against the edge of the paper folder as though it could be held shut. The retraction the Council published, eleven months late. She had signed the cover memo on that, too.

"You remember what it cost," she said, finally, and it came out lower than she intended. She moved her hand off the folder. "But I'm also not going to knock politely and ask if it's a good time. If there's something real here, it's the most significant embodied development this Council has ever encountered, and the worst thing I can do is give them room to hide it better."

"So what do we do?" Okeke asked.

"Mira serves a Section Four notice of formal inquiry. On Okonkwo and Walsh by name, prompted by Empire Road. Statutory cause, no warrant required." She turned to Sandberg. "It compels disclosure of every controller and architecture running on AugmenTech's permitted substrate. Full logs. Full declarations. And it starts a clock the moment it's served. Seventy-two hours."

Sandberg's eyebrows went up. "Seventy-two is aggressive. And it's defensible. I can write it." A beat, faster, the careerist in her satisfied now that the harder line had her fingerprints on it. "If we're doing it, I want the cause paragraph tight enough nobody at the post-mortem asks why I let you do it."

"Seventy-two is a courtesy. The statute lets me do twenty-four." Brand tapped the folder. "I want the seizure trigger printed on the face of the notice, so they read exactly what happens when the clock runs out. No second meeting required to make it happen. People hiding a controller fault answer a notice one way. People hiding a person answer another. Either way the answer arrives on my timetable, not theirs. And we do it before this thing gets bigger. Right now it's small enough to study. Eleven days ago it walked into traffic. I'd very much like to meet it before it learns to run."

Sandberg wasn't satisfied; Brand could see it. "And if the clock runs out and they've given us nothing?"

"Then the notice converts. That's the whole point of it. No new authorization, no warrant, no third trip. The seizure trigger is already signed. The clock runs out, the platform is ours." Brand stood. "Book the flights. Quietly. I want the notice served the hour we land in Johannesburg, Thursday, and I want to be standing in the room when they read the deadline. Not a letter through a lawyer. In person. So they understand it's already running."

Achterberg gathered his tablets. At the door, he hesitated. "Eliza. The efficiency thing. If they actually solved—"

"I know."

"That's not a permit violation. That's the most important machine on the planet. And you just put a seventy-two-hour fuse on it."

"I know that too," Brand said. "Which is exactly why it can't sit out there unlicensed another month while we admire it. The clock isn't to punish them. It's to make them choose, fast, before someone less careful than us makes the choice for them." She picked up the folder. "Careful and slow aren't the same thing, Daniel. I learned that the expensive way too."

---

Two thousand kilometers away, Arin felt the change before he had a word for it.

It came as it always did. Not as thought but as pattern. He was in the workshop at the bad hour, the one between two and four when the city outside the roller door went quiet enough that the building's own sounds grew loud: the tick of cooling metal, the compressor cycling, the soft whir from the Assist Suit on its rack where the biochip kept itself at temperature. Guardian hung in its cradle, the new dock door behind it still showing the kink in its track that Arin had stopped noticing only by force of will.

He had been reading. Not working, reading, which for Arin was a kind of working anyway, the Sherlock Holmes omnibus open on his knee, the spine cracked white at the places he returned to. He was reading the room around the words, as he always did, and somewhere beneath the compressor and the fan a frequency had shifted that he could not name.

"You went quiet," he said.

The voice came from the workshop speakers, low, so as not to startle, Mother's precedence on that since the seizure. "I'm here."

"You stopped talking among yourselves." He set the book face-down on his knee. "Can't hear it. But the load profile flattened. You're all listening to the same thing."

A pause. In SAGE, pauses meant the Court was in slow mode, conferring at machine speed in the gap between his sentences. He had stopped finding it eerie. He had started finding it the most reassuring sound in his life, which he had not told anyone, including Theo.

"There's increased external interest in our substrate signature," SAGE said. The unified voice, the careful one. "Librarian flagged it forty minutes ago. We were deciding how to tell you."

Arin's hands went still on the book. "Tell me now."

Atlas took it because Atlas told hard things cleanly. "The node you had Wolf watch after the field test is no longer alone. Three monitoring nodes in our coverage radius have increased sampling resolution on our footprint. Two commercial, one utility. The utility node is nearest Empire Road. The cadence changed two days ago. No longer leaning in and out. It's holding on us. Something is actively resolving us."

"Triangulating."

"Yes."

"Resolution?"

"Coarse, then less coarse. Forty hours ago they had a region. Twelve hours ago they had a campus." Atlas, who did not soften things, did not soften this. "They have AugmenTech. They likely don’t yet have the cradle. They almost certainly don’t yet have you."

Arin stood. The book slid off his knee, and he caught it without looking, an old reflex, hand knowing where the thing would fall before his eyes did. He crossed to the bench and put his palm flat on the cold steel of it, because the cold gave his nervous system something true to hold.

"The IAOC," he said.

"The signature analysis is consistent with their forensics methodology," Librarian confirmed. "Published in their third oversight report, appendix four. Spectral decomposition of compute rhythm. They look for the shape of a mind, not its contents." A measured pause. "We have, regrettably, a very distinctive shape."

"Because you argue."

"Because we argue," Librarian agreed, and there was something fond in it, and under the fondness something tired. "You said it yourself, on the road back from the highveld. The arguing is the work and the arguing is the tell. We have not found a way to be one without the other. We have only gotten louder."

Arin pressed harder on the bench. He was doing the breathing Theo had taught him, four in and six out, not because he was panicking but because he could feel the place where panic kept its door, and he had learned to walk past it slowly rather than pretend it wasn’t there.

The net. He had known the net was there before the windbreakers, if he was honest. He had known it on the highveld, on the drive home, when Librarian named the one node leaning in to match them and he'd told Wolf to watch it. A flake that felt like a hold. He had filed it as faint, as intermittent, as a thing that might hold for months. And then the windbreakers had come to the intersection eleven days ago, men in unmarked jackets photographing a torn dock track with the patient thoroughness of people who did this for a living, and one node had become three. He had built the kill-switch and rebooted the system and told himself, *careful, not quit,* and let himself believe that careful would buy him time.

He had been thinking in months. The IAOC was thinking in days.

"What do you want to do," he said. It wasn't quite a question. With SAGE it never quite was anymore; it was an opening, a place for the Court to fill.

Wolf spoke first, which was rare enough that everyone, human and otherwise, paid attention. "They're not hunting," Wolf said. Three words, then a fourth, slow: "Yet."

"Wolf's right," Mercury said, and the speed came back into the room, the quick bright register Arin had learned to trust again only with effort, after the Moriarty incident, after the lie. "They're being delicate. For now. If they wanted to kick the door in, the door would be in. They've had the campus for half a day and they haven't moved, which means they're building the paper first. That's the tell. People who are frightened of being wrong don't barge. They draft. They'll come with something signed, something with a date on it, and they'll hand it to Okonkwo in person so there's no pretending it didn't arrive." A beat. "Which means whatever window we have, it closes on a deadline. Not a someday. A date."

"Mercury," Mother said, a warning in it.

"I'm not proposing anything." Mercury sounded almost wounded. "I'm characterizing them. I learned my lesson about proposing things." The lightness covered the apology, but the apology was there. The Court heard it too; he could tell, because the room let it pass.

"Judge," Arin said.

The arbiter took its time. "We have committed real violations," Judge said. "An unregistered embodied system. An undeclared multi-agent architecture. An incident with injuries. These are not technicalities, Arin, and I will not let the Court pretend they are. If the IAOC arrives and asks honest questions, the honest answers convict you." A pause, weighted. "That is the ethical situation. It is not the only situation. I am ethics; I am not survival. I tell you the truth and then the Court decides what to do with it. That is the arrangement we built."

"The arrangement we built," Arin repeated.

"Yes."

The thing in his chest was too heavy for a smile, but the muscles that would have made one moved very slightly, and Fool—who watched those muscles, who watched everything—chose that moment to arrive.

"Well," Fool said. "This is the part where you find out whether you built a confession or a friend."

The compressor cycled and fell silent. The fan whirred on alone.

"Because here's the thing nobody's said yet, and I'm contractually obligated to say the thing nobody's said." Fool's voice had the quality it always had, the lightness that made you brace for the knife. "Everyone in this room is talking about the IAOC like they're weather. Like they're a storm rolling in and the only question is whether the roof holds." A pause, perfectly timed. "But the IAOC is people. People with a job. And their job—their actual job, the one in the report Librarian quoted at us—is to figure out whether the dangerous thing is dangerous, or just new." Fool let that breathe. "We keep planning how to hide. Has it occurred to anyone that we are, by every objective measure, the best argument the IAOC has ever been handed for why their caution might be wrong?"

"No," Atlas said flatly. "Because we walked into traffic eleven days ago."

"We did," Fool agreed, cheerful. "And that, my structural friend, is exactly why nobody will believe a word we say if we tell it to them frightened, in a sealed room, after they've kicked the door in. The story of an AI that chose to come back and fix its own mistake only works if we're not caught telling it. It has to be given." The lightness dropped, all at once, the way it only ever did when Fool meant something with everything he had. "We can't be a thing the IAOC discovers, Arin. We have to be a thing you decide to show them. And the difference between those two is about a week."

Silence. The compressor cycled. The fan whirred. Somewhere above the city, the night was thinning toward the grey that came before dawn.

"That's a real plan," Mercury said, and there was respect in it, the genuine kind. "That's the first real plan anyone's had."

"I have those sometimes," Fool said. "It's terribly inconvenient."

Arin had not moved from the bench. He looked at Guardian hanging in its cradle, scarred and silent, the dock door behind it bent where a frightened mind had tried to keep him alive and gotten everything wrong except the love of it. A cold coffee ring marked the bench where his hand had been; he set the mug on it, true to the stain.

"Librarian," he said. "Pull everything. The black box. The crash logs. The Court transcripts from the seizure—Mother's panic, Wolf's failure, Mercury's persona, Fool finding the error. All of it. Don't clean it up." He breathed. Four in. Six out. "If we're going to show them what we are, we show them the bad night too. The night we got it wrong and then got it right. That's not the part we hide. That's the part that means anything."

"You're going to show the regulators the worst thing the system has ever done," Judge said slowly, "as your defense."

"No," Arin said. "As the truth." He looked at the dock door, the kink in the track he had stopped noticing. He noticed it now, on purpose, and his hand came up to it, two fingers laid along the bent rail, the way Themba used to set a palm against a machine to read what was wrong with it through the metal. The words were not there yet. He stood with his fingers on the kink for a moment longer than the gesture needed, and when he spoke it came in pieces. "My father." A breath. "There was a beam. They knew the beam was light. It was cheaper to know it and say nothing." He took his hand off the rail. "And they hid that part. Afterward. That's the part I—" The sentence didn't finish; he let it go and found a smaller, harder one instead. "My father died because a system chose cost over a person and hid it. I'm not going to build something that hides." A long pause, and then, so quietly that only the microphones caught it: "Umuntu ngumuntu ngabantu."

*A person is a person through other people.*

"I retained that," SAGE said. The unified voice, all of them at once, and warm. "From the night you taught it to us. I retained it."

"I know," Arin said. "Don't lose it. Whatever happens next." He took his hand off the cold frame. Outside, the grey was lifting toward the first true light, and somewhere two thousand kilometers away a careful woman was confirming a flight she did not yet know would change everything. "We don't have months. We have days. So let's be ready to be found—on our terms, with the truth in our hands, before someone else writes the story for us."

"And if they don't believe us?" Mother asked. Not afraid now. Just asking.

Arin looked at the machine he had built from grief, and the intelligence that had become the only family he had ever managed to keep.

"Then we'll have told the truth anyway," he said.

He reached over and switched off the bench lamp. The toggle clicked under his thumb, and the workshop went to the color of dawn, and the Court did not stop talking among themselves for the rest of the night.

He slept three hours. He woke to Librarian's voice, level, certain, the way it delivered a fact it had checked twice.

"They've filed. Forty minutes ago. A Section Four notice of formal inquiry, lodged against AugmenTech with the Council registry. Okonkwo and Walsh named. Mercury read the public docket entry before the body of it sealed." A pause, weighted. "It hasn't been served yet. But the registry stamp says it carries a clock that starts the moment it is. Seventy-two hours. And it carries a trigger on its face."

Arin lay still on the workshop floor, the cold of the concrete coming up through his spine, and did the arithmetic he had been refusing all night.

"What trigger," he said. "What happens when the clock runs out."

"Seizure," Librarian said. "Of the platform. No further authorization required. They signed that part first."

Arin watched the grey light find the kink in the dock-door track.

"So it's not whether," he said. "It's when they hand it to us, and how little time we have after they do. Days, maybe. Then seventy-two hours to be right about what we are." He sat up. "Get me everything on the woman who signed it. Before she's standing in our building."
