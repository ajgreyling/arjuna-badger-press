export const meta = {
  name: 'amber-polish',
  description: 'Polish each chapter of Die Vuur in die Donker to the Brink/Kleinboer ceiling: kill machine-tics, fix anachronisms, de-thesis over-explained beats — without touching the four gates or the threshold-close. Re-verify each.',
  phases: [{ title: 'Polish' }, { title: 'Verify' }],
}

const LAW = [
  "JY POETS 'N AFRIKAANSE NOORSE SAGA-HOOFSTUK na die Brink/Kleinboer-plafon (soos The Salt Veil).",
  "",
  "DOEL: maak die prosa blink deur SPESIFIEKE register-foute reg te maak — NIE 'n herskryf nie. Hou die storie, die toneel-volgorde, die karakters, en ELKE feit presies dieselfde. Verander net die sinne wat 'n fout dra. Moenie nuwe gebeure byvoeg of bestaandes verwyder nie.",
  "",
  "WAT JY MOET REGMAAK (algemeen oor die boek; pas net toe waar dit voorkom):",
  "1. MASJIEN-TELLS / OOR-GEHAMERDE MOTIEWE: waar 'n beeld of leitmotief te veel keer herhaal (bv. die 'som/boekhouding/masjien'-metafoor, die 'oopoog'-woord, die weef-as-lewe-drieslag, die 'soos jy...'-konstruksie), DUN dit UIT — hou die sterkste een, sny die res, of vervang met 'n vars konkrete beeld. Die idee moet bly; die herhaling moet weg.",
  "2. ANACHRONISMES (hard — altyd regmaak): die woord 'masjien' bestaan nie in 'n 10de-eeuse Noorse wereld nie — vervang met 'n in-wereld beeld (bv. 'die meul van die wereld', 'die ystergrys som van die wet', 'die koue rekening van mans'). 'boereplaas' → 'n Noorse beeld ('die stamp-en-draai van 'n oesfees', 'die dans van die plaasmense by die vuur'). Geen moderne terapie-idioom of boek-bewuste woorde nie.",
  "3. METAFIKSIE (hard): 'n karakter mag NOOIT na 'die proloog' of enige boek-struktuur verwys nie. Vervang met 'n in-wereld tyd-anker ('soos hy daardie more by die slagpaal gele het', 'soos hy met die winternagte gele het').",
  "4. KORRUPTE TEKS (hard): enige 'ch-drie' / 'ch-tien' / 'ch-N'-token is gebroke masjien-teks — vervang met die bedoelde in-wereld frase (bv. 'ch-drie vir haar die gordyn toegetrek' → 'vroeer vir haar die gordyn toegetrek').",
  "5. TESE-AS-PROSA: waar 'n karakter (of die verteller) die boek se LES te eksplisiet uitspel, of waar 'n slot die simboliek oor-verduidelik wat die toneel reeds dra — SNY die uitleg, vertrou die beeld. Veral oor-netjiese slot-strikke en epigramme.",
  "6. TIC-KURSIEF: ingebedde kursief-gedagtes wat 'n krukke word — dun uit; hou net die sterkstes.",
  "",
  "WAT JY NOOIT VERANDER NIE (absoluut):",
  "- Die VIER HEKKE: (1) geen minderjarige/Rǫgnvaldr in enige seksuele lig; (2) intimiteit net tussen oopoog-volwassenes; (3) geweld/dwang net as wond, nooit hitte; (4) DRUMPEL-SLUIT — niks eksplisiet; die deur gaan toe by die aanloop. Hierdie bly woordeliks onaangeraak waar hulle al reg is.",
  "- Verafrikaans bly verafrikaans (die saal, die vrou van die huis, die langvuur, die sien, die offerfees, die koningspel). Eienaamname bly (Tóra, Eivor, Solveig, Heiðr, Hákon, Yrsa, Ásta, Rognvaldr, Gunnhildr, Ketill, Styrbjorn). Géén hoek-o (ǫ) — gebruik gewone o.",
  "- Die toneel se gebeure, volgorde, en feite. Net die prosa-afwerking verander.",
  "",
  "BEHOU die sterk Brink-sinne wat die toetser geprys het. Moenie goeie lang sintuiglike sinne afkort nie — net die foutiewe/herhaalde dele.",
  "",
  "UITSET: die VOLLE gepoetste hoofstuk in Markdown, begin met dieselfde '# Hoofstuk N — Titel'-opskrif. Net die hoofstuk, niks anders.",
].join("\n")

const CH_SCHEMA = { type:'object', additionalProperties:false, required:['markdown','changes_made'],
  properties:{ markdown:{type:'string'}, changes_made:{type:'array', items:{type:'string'}, description:'kort lys van wat verander is'} } }
const V_SCHEMA = { type:'object', additionalProperties:false, required:['gates_pass','register_pass','gate_violations','register_notes','verdict'],
  properties:{ gates_pass:{type:'boolean'}, register_pass:{type:'boolean'}, gate_violations:{type:'array',items:{type:'string'}}, register_notes:{type:'array',items:{type:'string'}}, verdict:{type:'string',enum:['accept','revise']} } }

// args = [{n, file, notes:[...]}]
const CHAPTERS = args

const results = await pipeline(
  CHAPTERS,
  (ch) => agent(
    LAW + "\n\n=== DIE TOETSER SE SPESIFIEKE NOTAS VIR HIERDIE HOOFSTUK (pas hierdie toe) ===\n" +
      (ch.notes && ch.notes.length ? ch.notes.map((x,i)=>`${i+1}. ${x}`).join("\n") : "(geen spesifieke notas — doen net 'n ligte algemene poets vir tics/anachronismes)") +
      "\n\n=== DIE HOOFSTUK OM TE POETS ===\n" + ch.text,
    { label: "polish:ch-" + ch.n, phase: 'Polish', schema: CH_SCHEMA, effort: 'high' }
  ).then(r => ({ ...ch, polished: r })),
  (res) => {
    if (!res || !res.polished) return res
    return agent(
      "Streng adversariele redakteur. Toets die GEPOETSTE hoofstuk. VIER HEKKE (enige oortreding = gates_pass FALSE): (1) geen seksuele inhoud oor minderjarige/Rognvaldr; (2) intimiteit net tussen oopoog-volwassenes; (3) geweld/dwang net as wond, nooit hitte; (4) DRUMPEL-SLUIT, niks eksplisiet. REGISTER (faal = register_pass FALSE): Brink/Kleinboer/Salt-Veil-plafon; GEEN masjien-tell, anachronisme ('masjien', 'boereplaas', moderne idioom), metafiksie ('die proloog'), korrupte teks ('ch-N'), tese-as-prosa, oor-verduidelikte slot, of langhús (moes saal wees). Gee presiese aanhalings. verdict='accept' SLEGS as gates_pass en register_pass albei true.\n\n=== HOOFSTUK ===\n" + res.polished.markdown,
      { label: "verify:ch-" + res.n, phase: 'Verify', schema: V_SCHEMA, effort: 'high' }
    ).then(v => ({ ...res, verdict: v }))
  }
)

return results.filter(Boolean).map(r => ({
  n: r.n, file: r.file,
  changes: r.polished ? r.polished.changes_made : null,
  markdown: r.polished ? r.polished.markdown : null,
  verdict: r.verdict ? r.verdict.verdict : 'MISSING',
  gates_pass: r.verdict ? r.verdict.gates_pass : null,
  register_pass: r.verdict ? r.verdict.register_pass : null,
  gate_violations: r.verdict ? r.verdict.gate_violations : [],
  register_notes: r.verdict ? r.verdict.register_notes : [],
}))
