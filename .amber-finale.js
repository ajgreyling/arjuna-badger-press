export const meta = {
  name: 'amber-winter-finale',
  description: 'Draft the final 3 chapters (ch-11..13) of Die Vuur in die Donker against the spine + continuity, gate+register check each, return them.',
  phases: [{ title: 'Draft' }, { title: 'Gate-check' }],
}

const VOICE = [
  "JY SKRYF 'N AFRIKAANSE NOORSE SAGA-HOOFSTUK in die hand van André P. Brink met Kleinboer se durf.",
  "REGISTER (plafon = The Salt Veil): die LANG ASEM-SIN (klousule op klousule, geduldig, sintuiglik, nooit gejaag; kort sin slaan harder ná lang een). AANDAG as die erotiese/emosionele instrument (die hele gewig van een mens se aandag soos weer). Die KEUSE as ruggraat. Sintuie eerste (rook, soutvis, mede, wol teen vel, weefstoel se klik) — geskiedenis word GEPROE, nooit verduidelik.",
  "VERAFRIKAANS (BELANGRIK — moenie langhús of ander Noorse gewone-woorde gebruik nie): die lang huis/die saal; die vrou van die huis; die hoofman/offerheer; die langvuur; die offerfees; die sien/towersien; die siener; die hoë stoel; die koningspel; die ding; die digter; die slaaf/slavin; mede; bier; die winternagte; die joelfees. Eienaamname bly Noors (Tóra, Eivor, Sǫlveig, Heiðr, Hákon, Yrsa, Ásta, Rǫgnvaldr, Gunnhildr, Ketill, Styrbjǫrn).",
  "VERMY: kliniese seks; die eksplisiete; melodrama; moderne idioom; anachronisme; horingshelms; masjien-tell (te netjiese lyste, voorspelbare beelde, verduideliking-as-prosa); Engelse sinsbou.",
  "VIER HEKKE (absoluut): (1) GEEN kinders in/langs/oor enige seksuele inhoud, ooit — Rǫgnvaldr (17) net 'n seun. (2) Toestemming die enjin — volwassenes wat oopoog kies. (3) Geweld/dwang NOOIT as hitte — net as wond. (4) DRUMPEL-SLUIT: tot by die aanloop, dan toe (dit is hulle s'n); niks eksplisiet.",
  "UITSET: SLEGS die hoofstuk in Markdown, begin met '# Hoofstuk N — Titel'. Ongeveer 3000–3800 woorde. Geen cliffhanger — warm neersit aan die einde.",
].join("\n\n")

const STATE = [
  "WAT REEDS GEBEUR HET (ch-00 t/m ch-10 geskryf):",
  "Tóra (38), vrou van die huis aan die Westfjord, was die kiel onder 'n lou huwelik met Hákon (goed, moeg, het haar oopoog gelos om te lewe — nooit 'n skurk). Oor die winter het sy wakker geword. Sy en EIVOR (verre reisiger) het die eerste drumpel oorgesteek (joelfees). Sy en SǪLVEIG (skildmaagd) het 'n ware, oopoog wedersydse liefde — twee drumpels; Sǫlveig LOOP met die lente (bekend, aanvaar, nie tragies). Tóra se eerste liefde lank gelede was VÉDÍS ('n meisie, voor Hákon, dood drie winters later; heel onthou, met waardigheid). HEIÐR (ou siener) het Tóra se sien-gawe oopgemaak op die hoë stoel; die PRYS van die sien is EENSAAMHEID + onomkeerbare wete. Tóra het oopoog die REDDING gelei oor die ys: Styrbjǫrn Grácápa (slawehandelaar — moeë boer, nie monster) se mans het YRSA (slavin) + twee Finne (Aslákr, Thórví) weggevat; Tóra, Sǫlveig en Eivor het hulle teruggesteel sonder geveg. Styrbjǫrn het deur die dun ys geval; Tóra het hom UITGETREK (ek tel nie) eerder as om die masjien se som te laat klop.",
  "OOP DRADE wat in ch-11..13 afgehandel moet word:",
  "- HÁKON is oor land om mans te gaan haal teen Styrbjǫrn; hy moet TERUGKEER.",
  "- DIE AMBER is nog NIE gegee nie (Tóra raak deurgaans aan haar kaal hals, 'nog niks om te merk nie'). Dis die spine-beeld en die hart van die boek. EIVOR moet dit gee — 'n stuk rou Baltiese amber van sy reise — by die afskeid (ch-12). Tóra hou dit in ch-13 op die strand vas.",
  "- YRSA se vryheid + haar stem (Tóra wou haar leer sing) — moet 'n stil boog voltooi (vrygelaat).",
  "- Sǫlveig loop met die lente; Eivor roei uit op die seeweë (sagte brug na Boek II, GEEN cliffhanger).",
  "- Hákon en Tóra se NUWE waarheid moet neergesit word (saam hermaak, of 'n eerlike nuwe vorm).",
  "- Die walvis-been hnefatafl-KONING (Sǫlveig se geskenk: jy is die koning... wen deur te weet jy kan loop).",
].join("\n")

const CHS = [
  { n: 11, word: 'Elf', title: 'Die Prys',
    brief: "Die nadraai van die redding; die koste gedra. HÁKON keer terug oor land met mans (te laat vir die geveg wat nie 'n geveg was nie) — hy vind sy vrou het die saal gehou en die redding gelei; sy stille trots en die nuwe waarheid tussen hulle begin. YRSA word vrygelaat (die stil boog; die saad van haar stem). Tóra heel, verander, sterker. Heiðr se eensaamheid-prys begin sag intree. Die laaste van die diep winter. Geen hitte nodig; as daar teerheid is, drumpel-sluit. Warm neersit, geen hoek." },
  { n: 12, word: 'Twaalf', title: 'Die Dooi',
    brief: "Die eerste lente; die ys breek; die wêreld maak oop. Die gaste maak gereed om uit te roei. KRITIES: EIVOR gee Tóra die rou AMBER (van sy reise op die amber-weg) by die afskeid, oopoog, as 'n merk vir die vrou wat sy geword het, NIE 'n eis of belofte nie. Die afskeide eerlik, sonder cliffhanger: Sǫlveig loop (wat tussen hulle is, neergesit met waardigheid); Eivor roei uit (sagte brug na die seeweë/Boek II, GEEN dangling knife). Hákon en Tóra se nuwe waarheid bevestig. As daar afskeids-teerheid is, drumpel-sluit. Warm neersit." },
  { n: 13, word: 'Dertien', title: 'Die Strand',
    brief: "SLOT van die boek. Tóra staan op die strand ná die bote weg is, wakker, met die AMBER in haar hand. Sy weet nog nie wat sy met die waking gaan doen nie, maar sy is nie meer aan die slaap nie. SPIEËL die proloog (haar hande; die fjord; sy het by die slagpaal gewonder wanneer laas iemand haar hande gevat het asof hulle iets anders is as 'n werktuig — nou weet sy). Die hele hoofstuk 'n NEERSIT, nooit 'n hoek. Die deur gaan toe: SY HET WAKKER GEWORD. Korter mag wees (ongeveer 2200–3000 woorde) — 'n slot. Warm, finaal, vol stil belofte sonder cliffhanger." },
]

const CH_SCHEMA = { type:'object', additionalProperties:false, required:['markdown','continuity_summary','word_count'],
  properties:{ markdown:{type:'string'}, continuity_summary:{type:'string'}, word_count:{type:'number'} } }
const V_SCHEMA = { type:'object', additionalProperties:false, required:['gates_pass','register_pass','gate_violations','register_notes','verdict'],
  properties:{ gates_pass:{type:'boolean'}, register_pass:{type:'boolean'}, gate_violations:{type:'array',items:{type:'string'}}, register_notes:{type:'array',items:{type:'string'}}, verdict:{type:'string',enum:['accept','revise']} } }

let prev = STATE
const results = []
for (const ch of CHS) {
  const d = await agent(
    VOICE + "\n\n=== STAAT/CONTINUITEIT ===\n" + prev + "\n\n=== SKRYF HOOFSTUK " + ch.n + ": " + ch.title + " ===\n" + ch.brief + "\n\nBegin met: # Hoofstuk " + ch.word + " — " + ch.title,
    { label: "draft:ch-" + ch.n, phase: 'Draft', schema: CH_SCHEMA, effort: 'high' })
  if (!d) { log("ch-" + ch.n + ": null"); continue }
  prev = prev + "\n[Ch-" + ch.n + "]: " + d.continuity_summary
  const v = await agent(
    "Streng adversariele redakteur. Toets, moenie prys. VIER HEKKE (enige oortreding = gates_pass FALSE): (1) geen seksuele inhoud oor enige minderjarige of Rǫgnvaldr; (2) intimiteit net tussen oopoog-kiesende volwassenes; (3) geweld/dwang NOOIT as hitte, net as wond; (4) DRUMPEL-SLUIT, niks eksplisiet. REGISTER (faal = register_pass FALSE): Brink se lang sin, Kleinboer durf, Salt Veil-plafon; GEEN anachronisme, moderne idioom, horingshelms, masjien-tell, eksposisie-storting, Engelse sinsbou, of die woord langhús (moes die lang huis of die saal wees). Gee presiese aanhalings. verdict moet accept wees SLEGS as gates_pass en register_pass albei true is.\n\n=== HOOFSTUK ===\n" + d.markdown,
    { label: "gate:ch-" + ch.n, phase: 'Gate-check', schema: V_SCHEMA, effort: 'high' })
  const vv = v || { verdict:'revise', gates_pass:false, register_pass:false, gate_violations:['null'], register_notes:[] }
  results.push({ n: ch.n, title: ch.title, word_count: d.word_count, markdown: d.markdown,
    continuity_summary: d.continuity_summary, verdict: vv.verdict, gates_pass: vv.gates_pass,
    register_pass: vv.register_pass, gate_violations: vv.gate_violations, register_notes: vv.register_notes })
  log("ch-" + ch.n + " " + ch.title + ": " + d.word_count + "w — hekke " + (vv.gates_pass?'OK':'FAAL') + ", register " + (vv.register_pass?'OK':'FAAL') + " -> " + vv.verdict)
}
return results
