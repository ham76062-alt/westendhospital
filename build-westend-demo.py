#!/usr/bin/env python3
"""
Adapt the Habana Medical Service demo site into a West End Hospital
(Kumasi) demo site.

Reads ~/workspace/user/files/habana-contact-page-rebuild-small.html and
writes ~/workspace/clinic-websites/west-end-hospital.html.

What changes:
- Branding: Habana Medical Service (Tamale) -> West End Hospital
  (Kumasi); phone, address, maps links. WhatsApp is assumed to be the
  mobile 024 546 0006 (unconfirmed). West End has NO email (none found
  anywhere) and NO social media pages — email and social links are
  removed, never invented.
- Colours: royal blue (user, 2026-11-22) — main royal blue #1d4ed8,
  deep navy-blue #1e3a8a for dark areas, light blue tints #dbeafe /
  #eff6ff, white background. Buttons and calls-to-action are royal
  blue; the sign red #dc2626 is used ONLY for the Accidents &
  Emergency card. This replaces the earlier deep teal (#0f6b6b family)
  + warm amber (#d98a1f) theme, so the demo does not look like
  Habana's, Del's (navy+gold), City's (blue+red) or Al-Kawthar's
  (green+gold). The logo
  is a clean text-based "WE" mark made for this demo — it is NOT the
  hospital's real logo (none was found); a real logo is still wanted.
- Services: 15 -> 12 services. Removes Habana-only services (ENT,
  Ophthalmology, Neurosurgery, Endoscopy, Emergency & Critical Care,
  Counselling, Dietetics, Preventive Healthcare, Diagnostic Imaging,
  Internal Medicine, Fertility Centre, Urology, Rehabilitation) and adds
  West End services (Outpatient Consultation, Accidents & Emergency,
  General Surgery & Theatre, Maternity & Obstetrics, Paediatrics,
  Laboratory & Diagnostics, Pharmacy, ECG, EPI (Immunisation), MCH
  (Maternal & Child Health), Family Planning, NHIS Office). Only
  ultrasound is claimed for imaging — no CT, MRI, X-ray, dialysis,
  ambulance, ICU, dental, eye care, ENT, physiotherapy or fertility/IVF.
  West End IS NHIS-accredited, with an NHIS Office on site.
- Removes Habana-only content: founder story, awards, 15-year
  celebration, CT scan / mammography claims, the Friday 9:00 AM cervical
  clinic time, Habana social links, staff sign-in, the email card.
- Founder story: Dr Jacob Kenneth Kofi Kwakye-Maafo (born 1940),
  OB/GYN surgeon and former Ghana Medical Association president, founded
  the clinic in 1978 with his wife Mercy Kwakye-Maafo nee Golightly
  (retired nurse); the OPD is the Mercy Golightly Unit, named after her.
  He is 86 — do NOT present him as the current day-to-day chief
  executive; the story is told as a legacy.
- Address: Dr Kwakye-Maafo Avenue, Edwenase Kwadaso, Kumasi (Google Maps
  pin 6.676491, -1.651508, plus code 6CRWM8GX+H9). Older directories say
  Patasi, opposite the police depot — that conflict is flagged in the
  README and pitch, NOT on the site. P.O. Box KS 4368. No street number
  invented. Visiting hours 5-7 AM and 4-6 PM are labelled VISITING hours,
  not opening hours (open 24 hours).
- Photos: the hospital's 3 real Google Maps photos (building, entrance
  sign, front view from the car park), 6 generated photos of Ghanaian
  people (maternity, emergency, surgery, lab, pharmacy, paediatrics —
  verified 2026-11-22), and Del's verified Ghanaian stock photos where a
  service matches. Stock and generated photos are stand-ins for the demo
  — swap in the hospital's real photos when available. The small
  front-cars photo was upscaled 3x with PIL Lanczos + sharpening (the AI
  upscale re-imagined the sign as "WEST AFRICAN HOSPITAL" and was
  rejected); the original is kept as *-original.jpg.
- 2026-11-22 rebuild (user): the user sent 30 more Google Maps photos
  in a zip; 7 new ones were added (waiting room, waiting room with
  patients, consulting room, waiting lounge, night exterior, hospital
  vehicle, street front) — the other 23 were Maps UI, near-duplicates
  or ambiguous (the Atwima Rural Bank building). The main building
  photo was upscaled 2x with PIL Lanczos + sharpening (the AI upscale
  was blocked); the night and van AI upscales were rejected for
  re-imagining the sign ("HOSPILAL HOSPILAL") and the van lettering
  ("GOVT CITY HOSPITAL") and were redone with PIL. The maternity
  scan photo now shows the bare belly with the probe on it (user,
  2026-11-22; covered version kept as *-covered.jpg). The review
  form now lives on the Contact page only. Preview timer ends
  Sunday 2026-11-29.
- Reviews: 3 neutral SAMPLE reviews, marked as samples on the page;
  no maternity claims, no invented patient words.
"""
import base64
import json
import re
import urllib.parse
from pathlib import Path

SRC = Path.home() / "workspace/user/files/habana-contact-page-rebuild-small.html"
DST = Path.home() / "workspace/clinic-websites/west-end-hospital.html"
HERE = Path(__file__).resolve().parent


def _data_uri(path, mime="image/jpeg"):
    return "data:%s;base64,%s" % (
        mime, base64.b64encode(Path(path).read_bytes()).decode())


# West End Hospital photos (Google Maps, downloaded 2026-11-22):
# the real three-storey blue/grey building, the entrance sign and the
# front view from the car park. The small front-cars photo (375x500) was
# upscaled 3x with PIL Lanczos + sharpening and verified faithful (the
# AI upscale re-imagined the sign as "WEST AFRICAN HOSPITAL" and was
# rejected); the original is kept as westend-building-front-cars-original.jpg.
WE_BUILDING_DAY = _data_uri(HERE / "westend-photos" / "westend-building-day-converted.jpg")
WE_INTERIOR = _data_uri(HERE / "westend-photos" / "westend-interior-converted.jpg")
WE_FRONT_CARS = _data_uri(HERE / "westend-photos" / "westend-building-front-cars.jpg")
# The hospital has NO real logo (none found anywhere). The logo is a
# clean text-based mark — "WE" in a royal blue tile with a light blue
# ring (user, 2026-11-22) — made for this demo only. It is NOT the hospital's logo; the
# README asks the hospital for their real logo. WE_LOGO is set below,
# after we_logo_svg() is defined.

WE_PHONE = "024 546 0006"
WE_PHONE_TEL = "+233245460006"
WE_PHONE_WA = "233245460006"
# Second contact number (landline). Shown on the contact Call card, the
# emergency banner and the chat panel.
WE_PHONE2 = "032 202 2590"
WE_PHONE2_TEL = "+233322022590"
# NO email — none was found for West End Hospital anywhere. Do NOT put an
# email in the demo. A third number, 020 812 4847, is possibly outdated —
# it is NOT on the site; the README asks the hospital to confirm it.
# WhatsApp is ASSUMED to be the main phone 024 546 0006 (unconfirmed).
WE_ADDR = "Dr Kwakye-Maafo Avenue, Edwenase Kwadaso, Kumasi"
WE_MAPS_DEST = "West%20End%20Hospital%2C%20Kumasi%2C%20Ghana"
# NOTE: West End has no Facebook page and no other socials — social links
# are removed, never invented.


# ---------------------------------------------------------------- placeholders
def _esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


_GRADS = [("#3b82f6", "#1e3a8a"), ("#1d4ed8", "#172554"),
          ("#60a5fa", "#1e40af"), ("#2563eb", "#1e3a8a")]


def ph(title, sub, w, h, variant=0):
    """Navy placeholder image as a data-URI SVG."""
    g1, g2 = _GRADS[variant % len(_GRADS)]
    cx, cy = w // 2, int(h * 0.30)
    r = max(18, int(h * 0.085))
    tfs = max(20, min(46, w // 26))
    sfs = max(13, tfs // 2)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="{g1}"/><stop offset="1" stop-color="{g2}"/>'
        '</linearGradient></defs>'
        '<rect width="{w}" height="{h}" fill="url(#g)"/>'
        '<circle cx="{cx}" cy="{cy}" r="{r2}" fill="rgba(255,255,255,0.13)"/>'
        '<rect x="{x1}" y="{y1}" width="{s}" height="{s2}" rx="4" fill="#ffffff"/>'
        '<rect x="{x2}" y="{y2}" width="{s2}" height="{s}" rx="4" fill="#ffffff"/>'
        '<text x="50%" y="{ty}%" text-anchor="middle" font-family="Georgia, serif" '
        'font-size="{tfs}" font-weight="600" fill="#ffffff">{title}</text>'
        '<text x="50%" y="{sy}%" text-anchor="middle" font-family="Arial, sans-serif" '
        'font-size="{sfs}" fill="rgba(255,255,255,0.82)">{sub}</text>'
        '</svg>'
    ).format(w=w, h=h, g1=g1, g2=g2, cx=cx, cy=cy, r2=r + 26,
             x1=cx - 5, y1=cy - r, s=10, s2=r * 2,
             x2=cx - r, y2=cy - 5,
             ty=62, sy=72, tfs=tfs, sfs=sfs,
             title=_esc(title), sub=_esc(sub))
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="")


def we_logo_svg():
    """Text-based 'WE' mark for the chat button and the logo (royal blue
    tile, light blue ring). This is a demo stand-in, NOT the hospital's
    real logo — no real logo was found anywhere. The hospital's real
    logo is still wanted (see README)."""
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="160" viewBox="0 0 200 160">'
        '<rect x="6" y="6" width="188" height="148" rx="28" fill="#1d4ed8"/>'
        '<rect x="6" y="6" width="188" height="148" rx="28" fill="none" stroke="#dbeafe" stroke-width="4"/>'
        '<text x="100" y="112" text-anchor="middle" font-family="Georgia, serif" '
        'font-size="72" font-weight="700" fill="#ffffff">WE</text></svg>'
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe="")


FAB = we_logo_svg()

LOGO = FAB

# Live Google Map (user, 2026-11-21): the real Google Map centred on the
# hospital (6.676491, -1.651508 — from its Google Maps listing), with
# the pin chip and a clickable "Tap to open map" link. The iframe is
# interactive (pan/zoom); the link opens directions in Google Maps.
MAP_LIVE_HTML = (
    '        <div class="map-embed">\n'
    '          <iframe class="map-live-frame" src="https://www.google.com/maps?q=6.676491,-1.651508&amp;z=16&amp;output=embed" style="border:0" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade" title="Map — West End Hospital, Kumasi"></iframe>\n'
    '          <span class="map-pin-chip"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg> West End Hospital</span>\n'
    '          <a class="map-open-chip" href="https://www.google.com/maps/dir/?api=1&amp;destination=West%20End%20Hospital%2C%20Kumasi%2C%20Ghana" target="_blank" rel="noopener">Tap to open map</a>\n'
    '        </div>'
)


# ---------------------------------------------------------------- West End services
# Each entry: name, blurb (grid card), tag, about (2 paras), helps (6),
# who, know, photos (3 PH keys).
SERVICES = [
    {
        "name": "Outpatient Consultation",
        "blurb": "General consultations for adults and families — walk in and see a doctor, any day.",
        "tag": "General consultations for adults and families — walk in and see a doctor, any day, without an appointment. Our outpatient department is the Mercy Golightly Unit.",
        "about": [
            "Our outpatient department (OPD) is the first door for most patients. A doctor listens to your symptoms, examines you and, where needed, arranges tests in our own laboratory or an ultrasound scan — so the cause of a problem is found rather than guessed at.",
            "Many everyday problems are treated right here: fevers including malaria, coughs and colds, stomach upsets, skin problems and minor injuries. If you need a specialist, your doctor will refer you to the right clinic in the hospital.",
        ],
        "helps": [
            "Fevers, including malaria",
            "Coughs, colds and flu",
            "Stomach upsets and diarrhoea",
            "Skin rashes and minor injuries",
            "Headaches and body pains",
            "Referrals to our specialists when you need them",
        ],
        "who": "Anyone who feels unwell or has a health concern — walk in, no appointment needed.",
        "know": "Bring a list of medicines you are taking and any previous test results. In an emergency, come straight in — no appointment needed.",
        "photos": ["westend-interior", "westend-real-waiting", "westend-real-waiting-people", "westend-real-consulting", "internal1", "internal2"],
    },
    {
        "name": "Accidents & Emergency",
        "blurb": "Urgent care, day and night — come straight in when every minute matters.",
        "tag": "Urgent care, day and night — come straight in when every minute matters. Our emergency team is here 24 hours, every day.",
        "about": [
            "Accidents and sudden illness cannot wait. Our emergency team assesses you quickly, steadies your condition and starts treatment straight away — and if you need admission or an operation, the wards and theatre are in the same building.",
            "Come straight in, or be brought in, at any hour of the day or night. No appointment is needed and the team is here 24 hours, every day.",
        ],
        "helps": [
            "Road traffic accidents and injuries",
            "Sudden severe pain or breathlessness",
            "High fever, fits and loss of consciousness",
            "Cuts, wounds and broken bones",
            "Stabilising care before admission or surgery",
            "Open 24 hours, every day",
        ],
        "who": "Anyone with an accident or a sudden, serious illness — come straight in, or be brought in, at any hour.",
        "know": "Do not wait — come straight to the hospital. Bring any medicines the patient is taking and any previous medical records.",
        "photos": ["westend-gen-emergency", "emergency2", "surgery2"],
    },
    {
        "name": "General Surgery & Theatre",
        "blurb": "Planned and emergency operations in our own theatre, with careful aftercare on the ward.",
        "tag": "Planned and emergency operations in our own theatre, with careful aftercare on the ward.",
        "about": [
            "Our surgeons carry out common general operations in our own theatre, with careful anaesthesia and pain relief. After your operation you recover on the ward, with daily surgeon rounds and nurses checking on you through the day and night.",
            "Your surgeon will explain the operation beforehand — what will happen, how long recovery takes, and what to expect when you go home — so you and your family know exactly what is planned.",
        ],
        "helps": [
            "Planned general operations",
            "Emergency surgery after an accident or sudden illness",
            "Careful anaesthesia and pain relief",
            "Recovery care on the ward",
            "Daily surgeon rounds after your operation",
            "Clear advice on healing at home",
        ],
        "who": "Patients whose doctor has recommended an operation, or who need emergency surgery.",
        "know": "Your surgeon will explain the operation and what to bring. Some operations need you to fast — your doctor will tell you.",
        "photos": ["westend-gen-surgery", "surgery", "surgery3"],
    },
    {
        "name": "Maternity & Obstetrics",
        "blurb": "Antenatal care, safe delivery and ultrasound — with midwives who stay with you.",
        "tag": "Antenatal care, safe delivery and ultrasound — with midwives who stay with you through pregnancy, birth and the weeks after.",
        "about": [
            "Our maternity team cares for mothers through pregnancy, birth and the weeks after delivery. Antenatal clinics check on you and your baby at every stage, and ultrasound scans are done right here in the hospital.",
            "When the time comes, you deliver on our maternity ward with midwives and doctors beside you, and postnatal care follows for you and your baby before you go home.",
        ],
        "helps": [
            "Antenatal clinics and check-ups",
            "Ultrasound scans during pregnancy",
            "Safe delivery on the maternity ward",
            "Postnatal care for mother and baby",
            "Advice on breastfeeding and newborn care",
            "Family planning after delivery",
        ],
        "who": "Expectant mothers at every stage of pregnancy — and new mothers in the weeks after delivery.",
        "know": "Book your antenatal care early and attend every appointment. If you notice bleeding, severe pain, reduced movement of the baby or leaking fluid, come in straight away.",
        "photos": ["westend-gen-maternity", "maternity", "maternity2"],
    },
    {
        "name": "Paediatrics",
        "blurb": "Gentle, attentive care for babies, children and teenagers — from check-ups to acute illness.",
        "tag": "Gentle, attentive care for babies, children and teenagers — from check-ups to acute illness.",
        "about": [
            "Children are not small adults — they need care that fits their age. Our team looks after babies, children and teenagers, from everyday fevers and coughs to malaria, diarrhoea and chest infections.",
            "Parents are welcome to stay with their child, and our nurses explain everything in plain language, so you always know what is happening and what to do at home.",
        ],
        "helps": [
            "Fevers, including malaria in children",
            "Coughs, colds and chest infections",
            "Diarrhoea and dehydration",
            "Immunisations (EPI) for babies and children",
            "Growth and development checks",
            "Advice for parents on feeding and care",
        ],
        "who": "Babies, children and teenagers — and their parents, with any worry about a child's health.",
        "know": "Keep immunisations up to date and bring the child's health record book. If a child has a very high fever, fits, fast breathing or will not drink, come in straight away.",
        "photos": ["westend-gen-paeds", "paeds", "paeds2"],
    },
    {
        "name": "Laboratory & Diagnostics",
        "blurb": "Accurate blood, urine and other laboratory tests with prompt results.",
        "tag": "Accurate blood, urine and other laboratory tests, with prompt results your doctor can act on.",
        "about": [
            "Good treatment starts with the right diagnosis. Our laboratory scientists run a wide range of tests on blood, urine and other samples, following careful quality procedures so your doctor can trust the result.",
            "Because the laboratory is here in the hospital, results come back quickly — often the same day — and go straight to your care team.",
        ],
        "helps": [
            "Full blood count and malaria tests",
            "Blood sugar and diabetes monitoring",
            "Liver and kidney function tests",
            "Pregnancy tests",
            "Urine and stool examinations",
            "Pre-surgery and antenatal test panels",
        ],
        "who": "Patients whose doctor has ordered tests, expectant mothers doing antenatal panels, and anyone preparing for an operation.",
        "know": "Some blood tests need you to fast — your doctor or the laboratory will tell you if yours does. Bring your request form if you were given one.",
        "photos": ["westend-gen-lab", "lab1", "lab2"],
    },
    {
        "name": "Pharmacy",
        "blurb": "An on-site pharmacy — collect your medicines before you leave.",
        "tag": "An on-site pharmacy, so you can collect your prescribed medicines before you leave — with clear advice on how to take them.",
        "about": [
            "Our pharmacy is inside the hospital, steps from the consulting rooms. After your appointment you can collect your prescribed medicines straight away — no separate trip across town.",
            "Our pharmacists check every prescription, explain how and when to take your medicine, and answer questions about side effects or medicines you are already taking.",
        ],
        "helps": [
            "Dispensing prescribed medicines after your visit",
            "Advice on how to take your medicine safely",
            "Checking that medicines are safe to take together",
            "Refills for long-term conditions like diabetes and hypertension",
            "Advice for older people and children on their medicines",
            "Help with medicines you already take at home",
        ],
        "who": "Anyone with a prescription from our doctors — and patients collecting refills for long-term conditions.",
        "know": "Bring your prescription and a list of medicines you already take. Ask the pharmacist if you are unsure about anything.",
        "photos": ["westend-gen-pharmacy", "pharmacy1", "pharmacy2"],
    },
    {
        "name": "ECG",
        "blurb": "A quick, painless heart tracing that helps your doctor check how your heart is working.",
        "tag": "A quick, painless heart tracing (ECG) that helps your doctor check how your heart is working.",
        "about": [
            "An ECG records the electrical activity of your heart. Small stickers are placed on your chest, and the test takes only a few minutes — it does not hurt, and there is nothing to prepare.",
            "It helps your doctor check chest pain, palpitations, breathlessness and dizziness, and see how high blood pressure is affecting your heart.",
        ],
        "helps": [
            "Checking chest pain and palpitations",
            "Checking breathlessness and dizziness",
            "Heart checks for high blood pressure",
            "Pre-surgery heart checks",
            "Quick results for your doctor",
            "A record your doctor can compare at your next visit",
        ],
        "who": "Anyone with chest pain, palpitations, breathlessness or dizziness — or whose doctor has asked for a heart check.",
        "know": "The test takes only a few minutes and does not hurt. Bring a list of medicines you are taking.",
        "photos": ["preventive1", "internal1", "counsel1"],
    },
    {
        "name": "EPI (Immunisation)",
        "blurb": "Childhood immunisations under Ghana's Expanded Programme on Immunisation.",
        "tag": "Childhood immunisations under Ghana's Expanded Programme on Immunisation (EPI) — protecting babies and children against preventable disease.",
        "about": [
            "Our EPI clinic gives babies and young children their routine vaccines, following Ghana's national immunisation schedule. Each vaccine protects your child against a serious preventable disease.",
            "Every vaccine is recorded in your child's health record book, and our nurses tell you the date of the next visit before you leave.",
        ],
        "helps": [
            "Routine vaccines for babies and young children",
            "Immunisation records in the child's health record book",
            "Advice on the next vaccine date",
            "Catch-up vaccines for children who missed a dose",
            "Health talks for parents",
            "A healthy start for every child",
        ],
        "who": "Babies and young children due for their routine vaccines — bring the child's health record book.",
        "know": "Bring the child's health record book so each vaccine is recorded. A mild fever after a vaccine is common — your nurse will tell you what to watch for.",
        "photos": ["preventive3", "preventive2", "preventive1"],
    },
    {
        "name": "MCH (Maternal & Child Health)",
        "blurb": "Care for mothers and children together — from pregnancy through the early years.",
        "tag": "Care for mothers and children together — from pregnancy through the early years of a child's life.",
        "about": [
            "Our maternal and child health (MCH) team follows mothers and children together: antenatal care, safe delivery, postnatal checks, child welfare clinics, growth monitoring and immunisations — one team that knows your family.",
            "Regular visits mean problems are spotted early, when they are easiest to treat, and mothers always have someone to ask.",
        ],
        "helps": [
            "Antenatal care and safe delivery",
            "Postnatal checks for mother and baby",
            "Child welfare clinics and growth monitoring",
            "Immunisations for babies and children",
            "Advice on breastfeeding and child feeding",
            "Family planning advice",
        ],
        "who": "Expectant mothers, new mothers and young children — and families who want one team following mother and child.",
        "know": "Attend antenatal appointments and bring your child for every scheduled welfare clinic visit. Bring the child's health record book.",
        "photos": ["maternity2", "preventive3", "counsel3"],
    },
    {
        "name": "Family Planning",
        "blurb": "Private, respectful advice on planning your family — with methods to suit you.",
        "tag": "Private, respectful advice on planning your family — with methods to suit you and your stage of life.",
        "about": [
            "Our family planning clinic offers private counselling for women, men and couples who want to plan or space their children. Our nurses and doctors explain each method, its benefits and side effects, and help you choose what suits you.",
            "Everything you discuss is private. You can come alone or with your partner, and you can change your method at any time.",
        ],
        "helps": [
            "Private counselling on family planning",
            "A range of methods to choose from",
            "Advice after delivery and for breastfeeding mothers",
            "Follow-up visits and method changes",
            "Care for couples, together or alone",
            "Clear, honest information — no pressure",
        ],
        "who": "Women, men and couples who want to plan or space their children — in complete privacy.",
        "know": "Everything you discuss is private. You can come alone or with your partner, and you can change your method at any time.",
        "photos": ["counsel3", "counsel1", "counsel2"],
    },
    {
        "name": "NHIS Office",
        "blurb": "Our NHIS Office on site — register, renew and use your NHIS card here.",
        "tag": "Our NHIS Office on site — register, renew and use your NHIS card here, so your visit costs less.",
        "about": [
            "West End Hospital is NHIS-accredited, and our NHIS Office is right here inside the hospital. You can register, renew and check your NHIS card without a separate trip.",
            "The office staff will explain what your card covers for your visit and help with any NHIS forms or questions.",
        ],
        "helps": [
            "NHIS registration and renewals",
            "Checking your NHIS card is valid",
            "Explaining what your card covers for your visit",
            "Help with NHIS forms and questions",
            "One less trip — everything in the hospital",
            "Friendly staff, here every day",
        ],
        "who": "Anyone with an NHIS card — or anyone who wants to register or renew one.",
        "know": "Bring your NHIS card and a valid photo ID when you visit. If your card has expired, the office can help you renew it.",
        "photos": ["internal2", "counsel2", "preventive2"],
    },
]

# Photo gallery entries: key -> (alt, caption). src is a placeholder built from caption.
# Photo gallery entries: key -> (alt, caption). src is a placeholder built from caption.
PH = {
    "internal1": ("A physician checking the blood pressure of a patient in a consulting room",
                  "Blood pressure and long-term condition checks"),
    "internal2": ("A doctor reviewing test results on a screen together with a patient",
                  "Reviewing your results together, in plain language"),
    "internal3": ("A physician listening to the chest of a patient during a ward round",
                  "Daily ward rounds for patients in our care"),
    "lab1": ("A laboratory scientist looking through a microscope at a sample, with test tubes beside her",
             "Samples examined carefully in our laboratory"),
    "lab2": ("A laboratory scientist loading samples into an automated analyser machine",
             "Modern analysers for fast, accurate results"),
    "lab3": ("A nurse taking a blood sample from the arm of a seated patient",
             "Blood samples taken gently, here at the hospital"),
    "pharmacy1": ("A pharmacist handing medicine to a patient across the pharmacy counter",
                  "Collect your medicine before you leave"),
    "pharmacy2": ("Shelves of medicines in the hospital pharmacy, with a pharmacist checking stock",
                  "Well-stocked shelves, checked daily"),
    "pharmacy3": ("A pharmacist checking a prescription carefully at a computer",
                  "Every prescription checked before it is dispensed"),
    "maternity": ("A midwife checking a smiling pregnant mother, with an ultrasound machine behind her",
                  "An antenatal check, with ultrasound on hand"),
    "maternity2": ("A new mother holding her newborn baby in the maternity ward, with a midwife beside her",
                   "First moments with your baby, on the maternity ward"),
    "counsel1": ("A doctor listening attentively during a private consultation",
                 "A private consultation, at your own pace"),
    "counsel2": ("A calm, comfortable consultation room with two armchairs by a window",
                 "A calm, private room for your consultation"),
    "counsel3": ("A doctor talking gently with a couple during a consultation",
                 "Time to ask your questions, together"),
    "surgery": ("A surgical team in theatre scrubs operating under bright surgical lights",
                "Inside the operating theatre during a planned operation"),
    "surgery2": ("A nurse caring for a patient recovering in a hospital bed after surgery",
                 "Careful recovery care on the ward after your operation"),
    "surgery3": ("The gloved hands of a surgical team working together under operating lights",
                 "Experienced hands in theatre"),
    "preventive1": ("A nurse checking the blood pressure of a woman at a health screening",
                    "A careful check-up at your first visit"),
    "preventive2": ("A health educator giving a talk to families at a community health session",
                    "Clear explanations, in plain language"),
    "preventive3": ("A nurse giving a child an immunisation while the mother holds the child",
                    "Care for the whole family"),
    "imaging1": ("A doctor performing an ultrasound scan, with the image on the monitor",
                 "Ultrasound scans by skilled staff"),
    "imaging2": ("A sonographer performing a pregnancy ultrasound, with the baby visible on screen",
                 "Pregnancy scans, with your baby on screen"),
    "emergency2": ("Nurses treating a patient on the ward",
                    "Urgent care, day and night"),
    "paeds": ("A doctor examining a young boy with a stethoscope",
              "Gentle care for your child"),
    "paeds2": ("A doctor examining a smiling boy",
               "A friendly visit, even for little ones"),
    "westend-interior": ("The entrance sign at West End Hospital, listing the departments, and the Mercy Golightly Unit",
                         "Find your way — every department is signposted"),
    # Seven more real Google Maps photos from the user's zip (2026-11-22).
    "westend-real-waiting": ("The hospital waiting room, with rows of blue chairs by the windows",
                            "A bright waiting room while you wait to be seen"),
    "westend-real-waiting-people": ("Patients waiting in the hospital waiting room",
                                    "Families waiting comfortably for their appointment"),
    "westend-real-consulting": ("A consulting room with a desk and chairs, and a CONSULTING ROOM sign on the wall",
                                "A quiet, private room for your consultation"),
    "westend-real-lounge": ("A comfortable waiting lounge with rows of chairs",
                            "Comfortable seating while you wait"),
    "westend-real-night": ("The West End Hospital building at night, lit up",
                          "Open 24 hours — day and night"),
    "westend-real-van": ("The hospital vehicle parked by the main building",
                        "Our hospital vehicle"),
    "westend-real-street": ("The front of West End Hospital from the street, behind green railings",
                           "Find us on Dr Kwakye-Maafo Avenue"),
    "westend-gen-maternity": ("A midwife doing an ultrasound scan for a pregnant woman, the baby visible on the screen",
                              "Antenatal care, with your baby on screen"),
    "westend-gen-emergency": ("Nurses and a doctor wheeling a patient on a stretcher through a bright hospital corridor",
                              "Fast, calm care when it matters most"),
    "westend-gen-surgery": ("A surgical team in green scrubs working under bright operating lights",
                            "Inside the operating theatre"),
    "westend-gen-lab": ("A female laboratory scientist looking through a microscope, with test tubes and an analyser beside her",
                        "Careful testing, close to your doctor"),
    "westend-gen-pharmacy": ("A male pharmacist handing a paper bag of medicine to a smiling woman in a colourful headwrap",
                             "Your medicines, explained clearly"),
    "westend-gen-paeds": ("A paediatric nurse with a stethoscope examining a happy toddler on his mother's lap",
                          "Gentle care for your little one"),
}

ALIASES = [
    ["Outpatient Consultation", ["opd", "outpatient", "consultation", "see a doctor", "see the doctor",
                                 "general consultation", "check-up", "checkup", "check up", "mercy golightly"]],
    ["Accidents & Emergency", ["emergency", "accident", "casualty", "a&e", "urgent",
                               "in an accident", "road accident"]],
    ["General Surgery & Theatre", ["surgery", "surgeon", "operation", "theatre", "theater",
                                   "hernia", "appendicitis"]],
    ["Maternity & Obstetrics", ["maternity", "pregnan-", "antenatal", "delivery",
                                "give birth", "baby", "babies", "newborn", "midwife",
                                "caesarean", "cesarean", "obstetric"]],
    ["Paediatrics", ["paediatric", "pediatric", "child", "children", "baby health",
                     "kids health", "baby is sick", "child is sick"]],
    ["Laboratory & Diagnostics", ["laboratory", "lab", "blood test", "test result",
                                  "sample", "urine test", "diagnosis"]],
    ["Pharmacy", ["pharmacy", "pharmacist", "prescription", "medication", "medicines", "medicine", "refill"]],
    ["ECG", ["ecg", "heart", "heartbeat", "palpitation", "chest pain", "heart check"]],
    ["EPI (Immunisation)", ["epi", "immunisation", "immunization", "vaccination", "vaccine", "vaccines"]],
    ["MCH (Maternal & Child Health)", ["mch", "maternal and child", "mother and child",
                                        "child welfare", "growth monitoring", "breastfeeding"]],
    ["Family Planning", ["family planning", "contraception", "contraceptive", "birth control"]],
    ["NHIS Office", ["nhis", "health insurance", "insurance card", "nhis card", "registration", "renew"]],
]

# "Our story" gallery: the real West End Hospital photos from Google Maps —
# three to start, plus seven more the user sent in a zip on 2026-11-22,
# so the gallery now has ten slides. The slide counter is built from
# this list, so it updates itself.
SLIDES = [
    {"label": "Our hospital",
     "alt": "The West End Hospital building in Kumasi"},
    {"label": "Our entrance",
     "alt": "The entrance sign at West End Hospital, listing every department"},
    {"label": "Our building",
     "alt": "The front of West End Hospital, from the car park"},
    {"label": "Our waiting room",
     "alt": "The hospital waiting room, with rows of blue chairs"},
    {"label": "Waiting with us",
     "alt": "Patients waiting in the hospital waiting room"},
    {"label": "Consulting room",
     "alt": "A consulting room at West End Hospital"},
    {"label": "Our lounge",
     "alt": "The waiting lounge at West End Hospital"},
    {"label": "At night",
     "alt": "The West End Hospital building at night"},
    {"label": "Our vehicle",
     "alt": "The hospital vehicle parked by the main building"},
    {"label": "From the street",
     "alt": "The front of West End Hospital from the street"},
]

GO_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

FB_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>')


def svc_card(i, svc):
    n = i + 1
    thumb = _photo_uri(svc["photos"][0])
    alt = PH[svc["photos"][0]][0]
    name = svc["name"].replace("&", "&amp;")
    return (
        '<button type="button" class="svc-card" data-service="{name}">'
        '<img class="svc-thumb" src="{thumb}" alt="{alt}" />'
        '<span class="svc-num">{num:02d}</span><h3>{name}</h3><p>{blurb}</p>'
        '<span class="go">Learn more {go}</span></button>'
    ).format(name=name, thumb=thumb, alt=_esc(alt), num=n,
             blurb=svc["blurb"], go=GO_SVG)


# Patient reviews (2026-11-22): five-star reviews on the home page,
# after the About teaser. SAMPLE reviews — West End Hospital's real
# patient words should replace them before the site goes live. They are
# marked as samples on the page itself. No maternity claims, no invented
# patient words. Do NOT use the lukewarm Google review ("Is not that big
# but is okay"). The review form is NOT in this section — it lives on
# the Contact page only (user, 2026-11-22); see REVIEW_FORM_HTML.
REVIEWS_SECTION = (
    '  <section class="block wrap">\n'
    '    <p class="eyebrow">Patient reviews</p>\n'
    '    <h2>What our patients say.</h2>\n'
    '    <p class="intro">Here is what patients and families say about their care at West End Hospital. These are sample reviews — the hospital&rsquo;s real patient words will replace them before the site goes live.</p>\n'
    '    <div class="reviews-grid">\n'
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cI was seen quickly and the doctor took time to listen. The whole visit was smooth from start to finish.\u201d</p><p class="review-name">Kwame A. \u2014 Outpatient</p></article>\n'
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe nurses were kind and explained everything clearly. I always felt supported.\u201d</p><p class="review-name">Ama S. \u2014 Inpatient</p></article>\n'
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe team answered all our questions and the hospital was clean and calm. We knew what was happening at every step.\u201d</p><p class="review-name">Kofi M. \u2014 Outpatient</p></article>\n'
    '    </div>\n'
    '  </section>'
)

# The "Share your experience" form (used on the Contact page only).
# Same behaviour as the old home/about form: name, tap-to-pick stars
# (defaults to 5), review text; submitting adds the review to the page
# and shows a thank-you. It does NOT save anywhere.
REVIEW_FORM_HTML = (
    '    <div class="review-form-wrap">\n'
    '      <h3>Share your experience</h3>\n'
    '      <p>Visited West End Hospital? Tell us how it went. Your words help other families choose their hospital.</p>\n'
    '      <form class="review-form">\n'
    '        <label>Your name<input type="text" class="rv-name" required placeholder="e.g. Kwame A."></label>\n'
    '        <span class="rv-stars-label">Your rating</span>\n'
    '        <span class="rv-stars" role="radiogroup" aria-label="Your rating">\n'
    '          <button type="button" data-v="1" aria-label="1 star">\u2605</button>\n'
    '          <button type="button" data-v="2" aria-label="2 stars">\u2605</button>\n'
    '          <button type="button" data-v="3" aria-label="3 stars">\u2605</button>\n'
    '          <button type="button" data-v="4" aria-label="4 stars">\u2605</button>\n'
    '          <button type="button" data-v="5" aria-label="5 stars">\u2605</button>\n'
    '        </span>\n'
    '        <label>Your review<textarea class="rv-text" required rows="4" placeholder="Tell us about your visit..."></textarea></label>\n'
    '        <button type="submit" class="btn">Submit review</button>\n'
    '        <p class="rv-thanks" hidden>Thank you! Your review has been added below.</p>\n'
    '      </form>\n'
    '    </div>\n'
)

# Customer review form script (user, 2026-11-21): visitors write a review
# and it is added to the reviews on the page, with a thank-you.
# The form lives on the Contact page only (user, 2026-11-22), where the
# reviews sit in a .reviews-stack, not a .reviews-grid — so the script
# looks for either one.
REVIEW_FORM_JS = (
    '  <script>\n'
    '  // Customer review form: adds the visitor review to the reviews.\n'
    '  document.querySelectorAll(".review-form").forEach(function (form) {\n'
    '    var stars = form.querySelectorAll(".rv-stars button");\n'
    '    var rating = 5;\n'
    '    function paint() {\n'
    '      stars.forEach(function (b) { b.classList.toggle("on", +b.dataset.v <= rating); });\n'
    '    }\n'
    '    stars.forEach(function (b) {\n'
    '      b.addEventListener("click", function () { rating = +b.dataset.v; paint(); });\n'
    '    });\n'
    '    paint();\n'
    '    form.addEventListener("submit", function (e) {\n'
    '      e.preventDefault();\n'
    '      var name = form.querySelector(".rv-name").value.trim();\n'
    '      var text = form.querySelector(".rv-text").value.trim();\n'
    '      if (!name || !text) return;\n'
    '      var section = form.closest("section");\n'
    '      var grid = section ? (section.querySelector(".reviews-grid") || section.querySelector(".reviews-stack")) : null;\n'
    '      if (!grid) return;\n'
    '      var card = document.createElement("article");\n'
    '      card.className = "value-card review-card";\n'
    '      var starsText = "\\u2605".repeat(rating) + "\\u2606".repeat(5 - rating);\n'
    '      function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }\n'
    '      card.innerHTML = `<p class="stars" aria-label="${rating} out of 5 stars">${starsText}</p><p>\u201c${esc(text)}\u201d</p><p class="review-name">${esc(name)} \u2014 Patient</p>`;\n'
    '      grid.appendChild(card);\n'
    '      var thanks = form.querySelector(".rv-thanks");\n'
    '      if (thanks) thanks.hidden = false;\n'
    '      form.reset();\n'
    '      rating = 5; paint();\n'
    '      card.scrollIntoView({ behavior: "smooth", block: "center" });\n'
    '    });\n'
    '  });\n'
    '  </script>\n'
)

# Reviews in the contact page's left column, under the form (user, 2026-11-21).
# Same sample reviews as the home/about sections, stacked vertically.
# The third review lives in the contact page's RIGHT column, under the map
# card (user, 2026-11-21): it fills the empty space there and balances the
# two columns. Same sample review as the other sections.
CONTACT_REVIEW_RIGHT = (
    '      <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe team answered all our questions and the hospital was clean and calm. We knew what was happening at every step.\u201d</p><p class="review-name">Kofi M. \u2014 Outpatient</p></article>'
)

CONTACT_REVIEWS = (
    '      <div class="contact-reviews">\n'
    '        <p class="eyebrow">Patient reviews</p>\n'
    '        <h3>What our patients say.</h3>\n'
    '        <p class="intro">These are sample reviews — the hospital&rsquo;s real patient words will replace them before the site goes live.</p>\n'
    '        <div class="reviews-stack">\n'
    '          <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cI was seen quickly and the doctor took time to listen. The whole visit was smooth from start to finish.\u201d</p><p class="review-name">Kwame A. \u2014 Outpatient</p></article>\n'
    '          <article class="value-card review-card"><p class="stars" aria-label="5 out of 5 stars">\u2605\u2605\u2605\u2605\u2605</p><p>\u201cThe nurses were kind and explained everything clearly. I always felt supported.\u201d</p><p class="review-name">Ama S. \u2014 Inpatient</p></article>\n'
    '        </div>\n'
    + REVIEW_FORM_HTML +
    '      </div>'
)

# West End overrides (2026-11-22), appended last in the stylesheet so they win:
# (a) restore the 24px side padding on every .block.wrap section — the
#     original .block{padding:72px 0} rule was wiping it out, so text sat
#     right on the left edge of the screen on every page;
# (b) shrink the chat button to a logo-only circle;
# (c) style the patient-reviews grid.
WE_CSS_OVERRIDES = (
    '  /* West End overrides (2026-11-22) */\n'
    '  .wrap.block, section.wrap:not(.band){padding-left:24px;padding-right:24px}\n'
    '  /* Chat button: smooth open/shut (user, 2026-11-21). Only the width\n'
    '     animates — padding, gap, logo position and corner radius never\n'
    '     change, so nothing jumps; the label fades in as the pill opens. */\n'
    '  .chat-fab{width:56px;height:56px;padding:.45rem 1.05rem .45rem .45rem;border-radius:999px;justify-content:flex-start;gap:.55rem;overflow:hidden;transition:width .45s cubic-bezier(.4,0,.2,1),transform .18s ease,background .18s ease,box-shadow .18s ease}\n'
    '  .chat-fab.expanded{width:196px}\n'
    '  .chat-fab .fab-logo{width:40px;height:40px}\n'
    '  .chat-fab>span:last-child{white-space:nowrap;opacity:0;transition:opacity .3s ease}\n'
    '  .chat-fab.expanded>span:last-child{opacity:1}\n'
    '  .reviews-grid{display:grid;gap:16px;margin-top:36px;grid-template-columns:1fr}\n'
    '  @media(min-width:720px){.reviews-grid{grid-template-columns:repeat(3,1fr)}}\n'
    '  .review-card .stars{color:var(--accent);font-size:1.15rem;letter-spacing:.15em;margin-top:0}\n'
    '  .review-card .review-name{font-weight:700;color:var(--teal-ink);margin-top:14px}\n'
    '  .mission-grid{display:grid;gap:20px 32px;margin:28px 0 44px;grid-template-columns:1fr}\n'
    '  @media(min-width:720px){.mission-grid{grid-template-columns:1fr 1fr}}\n'
    '  .mission-grid h3{font-size:1.35rem;color:var(--teal-ink);margin:0 0 8px}\n'
    '  .mission-grid p{color:var(--muted);font-size:1.02rem;line-height:1.6;margin:0}\n'
    '  .contact-reviews{margin-top:48px}\n'
    '  .contact-reviews h3{font-size:1.35rem;color:var(--teal-ink);margin:0 0 16px}\n'
    '  .reviews-stack{display:grid;gap:16px}\n'
    '  /* Booking date + time boxes (user, 2026-11-21): the base rule only\n'
    '     styles text/tel/email inputs, so the date and time boxes fell back\n'
    '     to the browser grey. Give them the exact same look as the other\n'
    '     booking fields. */\n'
    '  input[type="date"],input[type="time"]{width:100%;border:1px solid var(--line);border-radius:12px;background:var(--bg);padding:.72rem .95rem}\n'
  '  /* Preview countdown timer bar (user, 2026-11-21): dark bar at the\n'
    '     very top, above the Open 24/7 bar; the numbers are orange. */\n'
    '  .preview-timer{background:#1c1c1e;color:#e8e8e8;text-align:center;padding:10px 16px;font-size:.82rem;letter-spacing:.1em;display:flex;flex-wrap:wrap;gap:2px 16px;align-items:center;justify-content:center;position:fixed;top:0;left:0;right:0;z-index:1000}\n'
    '  .preview-timer .pt-label{font-weight:700;color:#f5f5f5}\n'
    '  .preview-timer .pt-count{font-weight:700;white-space:nowrap}\n'
    '  .preview-timer .pt-count b{color:#ff7a1a;font-size:1.05rem}\n'
    '  .preview-timer .pt-count i{color:#8a8a8a;font-style:normal;margin:0 3px}\n'
    '  .preview-timer .pt-count .pt-unit{color:#bdbdbd;font-weight:600}\n'
    '  .preview-timer .pt-note{color:#9a9a9a;letter-spacing:.02em}\n'
    '  /* Transparent header on scroll (user, 2026-11-22): at the top the\n'
    '     header is solid; once you scroll, its background fades to\n'
    '     see-through (with a soft blur) so the page shows through it,\n'
    '     while the logo, nav links and Book button stay put. Made MORE\n'
    '     transparent on the user ask (2026-11-22): only a quarter white\n'
    '     now, down from 0.45. */\n'
    '  header.site{transition:background .35s ease,border-color .35s ease,backdrop-filter .35s ease,-webkit-backdrop-filter .35s ease}\n'
    '  header.site.scrolled{background:rgba(247,248,250,0.25);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-bottom-color:rgba(227,230,234,0.25)}\n'
    '  /* Live Google Map (user, 2026-11-21): the embedded map fills the\n'
    '     map area like the old picture did, and "Tap to open map" is now\n'
    '     a real clickable link, so it needs pointer events back on. */\n'
    '  .map-live-frame{display:block;width:100%;height:300px;border:0}\n'
    '  @media (max-width:1023px){.map-live-frame{height:280px}}\n'
    '  .map-open-chip{pointer-events:auto}\n'
    '  /* Customer review form (user, 2026-11-21): the "Share your\n'
    '     experience" form under the patient reviews. Stars are gold\n'
    '     when picked, grey when not. */\n'
    '  .review-form-wrap{margin-top:36px;border-top:1px solid var(--line);padding-top:28px}\n'
    '  .review-form-wrap h3{margin-bottom:6px}\n'
    '  .review-form-wrap>p{color:var(--muted)}\n'
    '  .review-form{display:grid;gap:12px;max-width:560px;margin-top:16px}\n'
    '  .review-form label{display:grid;gap:6px;font-weight:600}\n'
    '  .review-form input[type="text"],.review-form textarea{width:100%;border:1px solid var(--line);border-radius:12px;background:var(--bg);padding:.72rem .95rem;font:inherit}\n'
    '  .rv-stars-label{font-weight:600}\n'
    '  .rv-stars{display:flex;gap:4px}\n'
    '  .rv-stars button{background:none;border:0;font-size:1.6rem;color:#c9c9c9;cursor:pointer;padding:0 2px;line-height:1}\n'
    '  .rv-stars button.on{color:#1d4ed8}\n'
    '  .rv-thanks{color:var(--teal-dark);font-weight:600}\n'
    '  /* Emergency red (user, 2026-11-22): the welcome-sign red is\n'
    '     used ONLY for the Accidents & Emergency card — a thin red top\n'
    '     border. It is never a general accent. */\n'
    '  .svc-card[data-service="Accidents & Emergency"]{border-top:3px solid #dc2626}\n'
    '  /* Royal blue contrast fixes (user, 2026-11-22): the amber buttons\n'
    '     had dark text, which read well on amber but not on royal blue —\n'
    '     so accent buttons and the dark call-card numbers are white now,\n'
    '     and footer link hovers use the light blue tint. */\n'
    '  .btn-accent{color:#fff}\n'
    '  .ccard.dark .cbig a{color:#fff}\n'
    '  .foot-links a:hover,.foot-links button:hover,.foot-service-links button:hover{color:#dbeafe}\n'
    '  /* Hero: lighter blue overlay + legible text (user, 2026-11-22):\n'
    '     the royal-blue shade over the hero photo was too bright and hid\n'
    '     the building, and the italic "day and night." (royal blue on\n'
    '     royal blue) was invisible. The shade alphas are roughly halved\n'
    '     so the photo shows through; the headline second line is white\n'
    '     like the first, and the hero texts get a soft navy shadow so\n'
    '     they stay readable over the brighter photo. The shade itself\n'
    '     is replaced in place above (see the hero-shade replacement\n'
    '     after the colour mapping); the rules below only fix text. */\n'
    '  .hero-full h1{text-shadow:0 1px 16px rgba(23,37,84,.55),0 1px 4px rgba(23,37,84,.5)}\n'
    '  .hero-full h1 em{font-style:italic;color:#fff;text-shadow:0 1px 16px rgba(23,37,84,.55),0 1px 4px rgba(23,37,84,.5)}\n'
    '  .hero-full .lede{color:#fff;text-shadow:0 1px 12px rgba(23,37,84,.5),0 1px 3px rgba(23,37,84,.45)}\n'
    '  .hero-full .hero-meta{color:#fff;text-shadow:0 1px 10px rgba(23,37,84,.5),0 1px 3px rgba(23,37,84,.45)}\n'
    '  .hero-full .hero-meta svg{color:#fff}\n'
    '  .hero-cap{color:#fff;text-shadow:0 1px 8px rgba(23,37,84,.5),0 1px 3px rgba(23,37,84,.45)}\n'
    '  .hero-cap b{color:#fff}\n'
    '  .hero-cap .sep{color:rgba(255,255,255,.8)}\n'
    '  /* Fixed timer + header (user, 2026-11-22): the timer bar and the\n'
    '     header (Home, Services, About us, Contact + Book button) stay\n'
    '     on screen at all times while scrolling. They are position:fixed\n'
    '     now, not sticky, so they stay put in any viewing context. Only\n'
    '     the Open 24/7 bar scrolls away. The header docks under the\n'
    '     timer as the topbar scrolls off: its top is set by script\n'
    '     (timer height + whatever of the topbar is still visible). */\n'
    '  header.site{position:fixed;left:0;right:0;z-index:999}\n'
  '  /* The "Moments" photo is the services board — show it\n'
    '     whole, never cropped or zoomed. */\n'
    '  .award-photo img{max-height:none;object-fit:contain}\n'
    '  /* Pop-in on load and on scroll (2026-11-21). The animation runs once\n'
    '     per element (fill backwards so the delay period stays hidden); after\n'
    '     it ends the element keeps its own styles, so hover lifts still work. */\n'
    '  .pop{opacity:0}\n'
    '  .pop.in{opacity:1;animation:wePopIn .7s cubic-bezier(.21,.9,.35,1.05) backwards}\n'
    '  @keyframes wePopIn{from{opacity:0;transform:translateY(28px) scale(.94)}to{opacity:1;transform:translateY(0) scale(1)}}\n'
    '  @media (prefers-reduced-motion:reduce){.pop{opacity:1}.pop.in{animation:none}}\n'
)

# Pop-in animation script (user, 2026-11-21): cards, stats, photos and list
# items pop in gently when the page loads and when you scroll to them.
POP_IN_JS = (
    '  <script>\n'
    '  // Pop-in on load and on scroll.\n'
    '  (function(){\n'
    '    var els = document.querySelectorAll(".svc-card, .value-card, .stat, .teaser img, .carousel, .why-list li, .mission-grid > div, .block h2, .block .eyebrow, .block .intro, .band-inner, .card, .find-panel, .foot-grid, .contact-reviews");\n'
    '    els.forEach(function(el){\n'
    '      el.classList.add("pop");\n'
    '      var i = Array.prototype.indexOf.call(el.parentElement.children, el);\n'
    '      el.style.animationDelay = Math.min(i, 5) * 70 + "ms";\n'
    '    });\n'
    '    function showAll(){ els.forEach(function(el){ el.classList.add("in"); }); }\n'
    '    if(!("IntersectionObserver" in window)){ showAll(); return; }\n'
    '    var io = new IntersectionObserver(function(entries){\n'
    '      entries.forEach(function(en){\n'
    '        if(en.isIntersecting){ en.target.classList.add("in"); io.unobserve(en.target); }\n'
    '      });\n'
    '    }, {threshold: 0.12});\n'
    '    els.forEach(function(el){ io.observe(el); });\n'
    '  })();\n'
    '  </script>\n'
)

# Chat button behaviour (user, 2026-11-21): it pops open on load showing
# "Chat with us" with the logo, then shrinks to the logo-only circle after
# 3 seconds. Hovering expands it again. Clicking it opens the chat and it
# stays expanded while the chat is open. Clicking away closes the chat, and
# the button shrinks again after 3 seconds.
CHAT_FAB_JS = (
    '  <script>\n'
    '  // Chat button: pops open on load, shrinks to the logo after 3 seconds.\n'
    '  (function(){\n'
    '    var fab = document.getElementById("chatFab");\n'
    '    var panel = document.getElementById("chatPanel");\n'
    '    if (!fab || !panel) return;\n'
    '    var timer = null;\n'
    '    function shrinkSoon(){\n'
    '      clearTimeout(timer);\n'
    '      timer = setTimeout(function(){\n'
    '        if (!panel.classList.contains("open")) fab.classList.remove("expanded");\n'
    '      }, 3000);\n'
    '    }\n'
    '    function expand(){ clearTimeout(timer); fab.classList.add("expanded"); }\n'
    '    function closePanel(){\n'
    '      if (typeof window.closeChat === "function") window.closeChat();\n'
    '      else { panel.classList.remove("open"); panel.setAttribute("aria-hidden", "true"); fab.setAttribute("aria-expanded", "false"); }\n'
    '    }\n'
    '    expand();\n'
    '    shrinkSoon();\n'
    '    fab.addEventListener("mouseenter", expand);\n'
    '    fab.addEventListener("mouseleave", shrinkSoon);\n'
    '    fab.addEventListener("click", function(){\n'
    '      setTimeout(function(){\n'
    '        if (panel.classList.contains("open")) expand(); else shrinkSoon();\n'
    '      }, 0);\n'
    '    });\n'
    '    document.addEventListener("click", function(e){\n'
    '      if (!panel.classList.contains("open")) return;\n'
    '      if (panel.contains(e.target) || fab.contains(e.target)) return;\n'
    '      closePanel();\n'
    '    });\n'
    '    if ("MutationObserver" in window) {\n'
    '      new MutationObserver(function(){\n'
    '        if (panel.classList.contains("open")) expand(); else shrinkSoon();\n'
    '      }).observe(panel, { attributes: true, attributeFilter: ["class"] });\n'
    '    }\n'
    '  })();\n'
    '  </script>\n'
)

# Booking date and time (user, 2026-11-21): the booking form lets the
# customer pick a preferred date and time. The two helpers format them for
# the WhatsApp message and the confirmation text; the script also stops
# the date picker offering past dates.
BOOKING_DATETIME_JS = (
    '  <script>\n'
    '  // Booking date/time helpers (used by the booking form submit handler).\n'
    '  function fmtBookDate(value) {\n'
    '    if (!value) return "";\n'
    '    var parts = value.split("-");\n'
    '    var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];\n'
    '    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];\n'
    '    var d = new Date(+parts[0], +parts[1] - 1, +parts[2]);\n'
    '    return days[d.getDay()] + ", " + d.getDate() + " " + months[d.getMonth()] + " " + d.getFullYear();\n'
    '  }\n'
    '  function fmtBookTime(value) {\n'
    '    if (!value) return "";\n'
    '    var parts = value.split(":");\n'
    '    var h = +parts[0];\n'
    '    var ampm = h >= 12 ? "PM" : "AM";\n'
    '    var h12 = h % 12;\n'
    '    if (h12 === 0) h12 = 12;\n'
    '    return h12 + ":" + parts[1] + " " + ampm;\n'
    '  }\n'
    '  (function () {\n'
    '    var dateInput = document.getElementById("bkDate");\n'
    '    if (!dateInput) return;\n'
    '    var now = new Date();\n'
    '    var mm = String(now.getMonth() + 1).padStart(2, "0");\n'
    '    var dd = String(now.getDate()).padStart(2, "0");\n'
    '    dateInput.min = now.getFullYear() + "-" + mm + "-" + dd;\n'
    '  })();\n'
    '  </script>\n'
)

# Preview countdown timer (user, 2026-11-21): a dark bar at the very top
# of the page, above the Open 24/7 bar, counting down to the preview
# expiry. The expiry is Sunday 2026-11-29 at 23:59 (user, 2026-11-22):
# 7 days from the Sunday the demo was rebuilt, so the timer reads
# 07 DAYS on the build day and on the Monday 2026-11-23 send day.
# Change PREVIEW_EXPIRY to move it. When the timer reaches
# zero it shows 00s and says the preview has expired.
PREVIEW_EXPIRY = "2026-11-29T23:59:59+00:00"
PREVIEW_TIMER_HTML = (
    '  <div class="preview-timer" id="previewTimer" role="timer">\n'
    '    <span class="pt-label">LIVE PREVIEW EXPIRES IN</span>\n'
    '    <span class="pt-count"><b id="ptDays">07</b> <span class="pt-unit">DAYS</span> <i>:</i> <b id="ptHours">00</b> <span class="pt-unit">HRS</span> <i>:</i> <b id="ptMins">30</b> <span class="pt-unit">MIN</span> <i>:</i> <b id="ptSecs">00</b> <span class="pt-unit">SEC</span></span>\n'
    '    <span class="pt-note">Temporary preview &mdash; taken offline when the timer reaches zero.</span>\n'
    '  </div>\n'
)
PREVIEW_TIMER_JS = (
    '  <script>\n'
    '  // Preview countdown timer: counts down to PREVIEW_EXPIRY.\n'
    '  (function () {\n'
    '    var expiry = new Date("' + PREVIEW_EXPIRY + '").getTime();\n'
    '    var bar = document.getElementById("previewTimer");\n'
    '    if (!bar) return;\n'
    '    var d = document.getElementById("ptDays"), h = document.getElementById("ptHours"),\n'
    '        m = document.getElementById("ptMins"), s = document.getElementById("ptSecs"),\n'
    '        note = bar.querySelector(".pt-note");\n'
    '    function pad(n) { return (n < 10 ? "0" : "") + n; }\n'
    '    function tick() {\n'
    '      var diff = expiry - Date.now();\n'
    '      if (diff <= 0) {\n'
    '        d.textContent = "00"; h.textContent = "00"; m.textContent = "00"; s.textContent = "00";\n'
    '        note.textContent = "This preview has expired.";\n'
    '        return;\n'
    '      }\n'
    '      d.textContent = pad(Math.floor(diff / 86400000));\n'
    '      h.textContent = pad(Math.floor(diff % 86400000 / 3600000));\n'
    '      m.textContent = pad(Math.floor(diff % 3600000 / 60000));\n'
    '      s.textContent = pad(Math.floor(diff % 60000 / 1000));\n'
    '    }\n'
    '    tick();\n'
    '    setInterval(tick, 1000);\n'
    '    // Fixed timer + header (user, 2026-11-22): the timer bar and\n'
    '    // the header must stay on screen at all times while scrolling.\n'
    '    // Both are position:fixed now, not sticky. Only the Open 24/7\n'
    '    // bar scrolls away. The header docks under the timer as the\n'
    '    // topbar scrolls off: its top is the timer height plus whatever\n'
    '    // of the topbar is still visible. The body padding and the main\n'
    '    // margin keep the topbar and the page content from hiding\n'
    '    // underneath the fixed bars. Heights are re-measured on load,\n'
    '    // resize, scroll, font load and whenever the bars resize, so the\n'
    '    // header still lines up when the timer wraps to two lines.\n'
    '    var header = document.querySelector("header.site");\n'
    '    var topbar = document.querySelector(".topbar");\n'
    '    var mainEl = document.querySelector("main");\n'
    '    var navBar = header ? header.querySelector(".wrap.nav") : null;\n'
    '    function pinBars() {\n'
    '      if (!header) return;\n'
    '      var th = bar.offsetHeight;\n'
    '      var tb = topbar ? topbar.offsetHeight : 0;\n'
    '      var hb = parseFloat(getComputedStyle(header).borderBottomWidth) || 0;\n'
    '      var hh = navBar ? navBar.offsetHeight + hb : header.offsetHeight;\n'
    '      header.style.top = (th + Math.max(0, tb - window.scrollY)) + "px";\n'
    '      document.body.style.paddingTop = th + "px";\n'
    '      if (mainEl) mainEl.style.marginTop = hh + "px";\n'
    '    }\n'
    '    pinBars();\n'
    '    window.addEventListener("load", pinBars);\n'
    '    window.addEventListener("resize", pinBars);\n'
    '    window.addEventListener("scroll", pinBars, { passive: true });\n'
    '    if (document.fonts && document.fonts.ready) document.fonts.ready.then(pinBars);\n'
    '    if ("ResizeObserver" in window) {\n'
    '      var ro = new ResizeObserver(pinBars);\n'
    '      ro.observe(bar);\n'
    '      if (topbar) ro.observe(topbar);\n'
    '      if (navBar) ro.observe(navBar);\n'
    '    }\n'
    '    // Transparent header on scroll (user, 2026-11-22): when the page\n'
    '    // is scrolled the header background fades to see-through so it\n'
    '    // stops covering the page, but the logo, nav links and Book\n'
    '    // button stay visible and clickable. At the top it is solid.\n'
    '    function headerFade() {\n'
    '      if (!header) return;\n'
    '      header.classList.toggle("scrolled", window.scrollY > 8);\n'
    '    }\n'
    '    headerFade();\n'
    '    window.addEventListener("scroll", headerFade, { passive: true });\n'
    '  })();\n'
    '  </script>\n'
)

# Mission + Vision (2026-11-22): short wording from West End's own
# facts — founded 1978 by Dr Kwakye-Maafo and his wife Mercy, nearly
# fifty years caring for Kumasi families. The hospital can adjust the
# exact words.
MISSION_VISION_HTML = (
    '      <div class="mission-grid">\n'
    '        <div><h3>Our Mission</h3><p>To give every patient in Kumasi safe, personal and professional care — day or night, whatever their condition.</p></div>\n'
    '        <div><h3>Our Vision</h3><p>To be the hospital Kumasi families trust first — care that treats every patient like family, for generations to come.</p></div>\n'
    '      </div>\n'
)

# ---------------------------------------------------------------- transform
def js_services():
    out = []
    for svc in SERVICES:
        entry = {k: svc[k] for k in
                 ("name", "tag", "about", "helps", "who", "know", "photos")}
        out.append("    " + json.dumps(entry, ensure_ascii=False))
    return "  var SERVICES = [\n" + ",\n".join(out) + "\n  ];"


def js_ph():
    out = []
    for i, (key, (alt, caption)) in enumerate(PH.items()):
        src = _photo_uri(key)
        # Keys must be quoted: West End keys like "westend-gen-maternity" contain
        # hyphens, which are not valid bare identifiers in a JS object.
        out.append('    {key}: [{src}, {alt}, {cap}]'.format(
            key=json.dumps(key, ensure_ascii=False),
            src=json.dumps(src, ensure_ascii=False),
            alt=json.dumps(alt, ensure_ascii=False),
            cap=json.dumps(caption, ensure_ascii=False)))
    return "  var PH = {\n" + ",\n".join(out) + "\n  };"


# Every photo the demo embeds, key -> file. Stock photos live in
# del-photos/services/; West End's generated photos in
# westend-photos/generated/; the real Google Maps photos in
# westend-photos/.
_PHOTO_PATHS = {}
# Del's verified Ghanaian stock photos (originals, NOT the Islamic-edited
# Al-Kawthar copies). Used where a West End service matches.
for _k in ("internal1", "internal2", "internal3",
           "lab1", "lab2", "lab3",
           "pharmacy1", "pharmacy2", "pharmacy3",
           "maternity", "maternity2",
           "counsel1", "counsel2", "counsel3",
           "surgery", "surgery2", "surgery3",
           "preventive1", "preventive2", "preventive3",
           "imaging1", "imaging2",
           "emergency2", "paeds", "paeds2"):
    _PHOTO_PATHS[_k] = HERE / "del-photos" / "services" / (_k + ".jpg")
# West End's own generated service photos (Ghanaian people, verified
# 2026-11-22) and the real Google Maps photos.
for _k in ("westend-gen-maternity", "westend-gen-emergency",
           "westend-gen-surgery", "westend-gen-lab",
           "westend-gen-pharmacy", "westend-gen-paeds"):
    _PHOTO_PATHS[_k] = HERE / "westend-photos" / "generated" / (_k + ".jpg")
_PHOTO_PATHS["westend-building-day"] = HERE / "westend-photos" / "westend-building-day-converted.jpg"
_PHOTO_PATHS["westend-interior"] = HERE / "westend-photos" / "westend-interior-converted.jpg"
_PHOTO_PATHS["westend-building-front-cars"] = HERE / "westend-photos" / "westend-building-front-cars.jpg"
# Seven more real Google Maps photos from the user's zip (2026-11-22),
# in westend-photos/real/; originals kept as *-original.jpg.
for _k in ("westend-real-waiting", "westend-real-waiting-people",
           "westend-real-consulting", "westend-real-lounge",
           "westend-real-night", "westend-real-van", "westend-real-street"):
    _PHOTO_PATHS[_k] = HERE / "westend-photos" / "real" / (_k + ".jpg")


def _photo_uri(key):

    return _data_uri(_PHOTO_PATHS[key])


_SLIDE_PHOTOS = {
    "Our hospital": "westend-building-day",
    "Our entrance": "westend-interior",
    "Our building": "westend-building-front-cars",
    "Our waiting room": "westend-real-waiting",
    "Waiting with us": "westend-real-waiting-people",
    "Consulting room": "westend-real-consulting",
    "Our lounge": "westend-real-lounge",
    "At night": "westend-real-night",
    "Our vehicle": "westend-real-van",
    "From the street": "westend-real-street",
}


def js_slides():
    out = []
    for i, s in enumerate(SLIDES):
        src = _photo_uri(_SLIDE_PHOTOS[s["label"]])
        out.append('    {{ src: {src}, label: {lab}, alt: {alt} }}'.format(
            src=json.dumps(src, ensure_ascii=False),
            lab=json.dumps(s["label"], ensure_ascii=False),
            alt=json.dumps(s["alt"], ensure_ascii=False)))
    return "  var SLIDES = [\n" + ",\n".join(out) + "\n  ];"


def js_aliases():
    return ("  var SERVICE_ALIASES = " +
            json.dumps(ALIASES, ensure_ascii=False) + ";")


def js_hero_slides():
    return ("  var HERO_SLIDES = [\n"
            '    { label: "Kumasi" },\n'
            '    { label: "Open 24 hours" },\n'
            '    { label: "Our hospital" }\n  ];')


def replace_img_by_alt(s, alt_part, new_src, new_alt=None):
    """Replace the src (and optionally alt) of the <img> whose alt contains alt_part."""
    def repl(m):
        tag = m.group(0)
        tag = re.sub(r'src="[^"]*"', 'src="' + new_src + '"', tag, count=1)
        if new_alt is not None:
            tag = re.sub(r'alt="[^"]*"', 'alt="' + _esc(new_alt) + '"', tag, count=1)
        return tag
    pat = re.compile(r'<img[^>]*alt="[^"]*' + re.escape(alt_part) + r'[^"]*"[^>]*>')
    s2, n = pat.subn(repl, s)
    if n == 0:
        raise ValueError("img with alt containing %r not found" % alt_part)
    return s2


def replace_img_by_id(s, el_id, new_src):
    pat = re.compile(r'(<img[^>]*id="' + re.escape(el_id) + r'"[^>]*src=")[^"]*(")')
    s2, n = pat.subn(r'\1' + new_src + r'\2', s, count=1)
    if n == 0:
        raise ValueError("img with id %r not found" % el_id)
    return s2


def sub_block(s, start_re, end_re, replacement, name):
    pat = re.compile(start_re + r'.*?' + end_re, re.DOTALL)
    s2, n = pat.subn(replacement, s, count=1)
    if n == 0:
        raise ValueError("block not found: " + name)
    return s2


def transform(s):
    # ---- 1. Logos: the royal blue "WE" mark in header/footer + chat head;
    #     the chat button gets the same "WE" mark.
    s = re.sub(r'(<span class="(?:brand-mark|head-logo)"[^>]*><img src=")'
               r'data:image/jpeg;base64,[^"]*(")',
               r'\1' + LOGO + r'\2', s)
    s = re.sub(r'(<span class="fab-logo"[^>]*><img src=")'
               r'data:image/jpeg;base64,[^"]*(")',
               r'\1' + FAB + r'\2', s)
    # ---- 2. Hero + story carousel + section photos (by id / alt) ----
    # Real West End photos (Google Maps) where the shot is the hospital
    # itself; generated and stock photos elsewhere until the hospital
    # supplies more real photos.
    # Hero slide order: the main building photo first, the entrance
    # sign second, the front view from the car park last.
    s = replace_img_by_id(s, "heroImg", WE_BUILDING_DAY)
    s = replace_img_by_id(s, "heroImg2", WE_INTERIOR)
    # Third hero slide: the front view of the building from the car park.
    s = re.sub(r'(<img id="heroImg2"[^>]*?/>)',
               lambda m: m.group(1) + '\n      <img id="heroImg3" src="' + WE_FRONT_CARS + '" alt="" />',
               s, count=1)
    s = replace_img_by_id(s, "carImg", WE_BUILDING_DAY)
    s = replace_img_by_alt(
        s, "A Habana radiographer guiding a patient into the Siemens CT scanner",
        _photo_uri("westend-gen-lab"),
        "A laboratory test at West End Hospital")
    s = replace_img_by_alt(
        s, "The Siemens SOMATOM CT scanner in the imaging suite",
        _photo_uri("imaging1"),
        "An ultrasound scan at West End Hospital")
    s = replace_img_by_alt(
        s, "Habana Medical Service nurses and staff together on the ward",
        WE_FRONT_CARS,
        "The front of West End Hospital in Kumasi")
    s = replace_img_by_alt(
        s, "Moments from the Habana Medical Service story",
        WE_INTERIOR,
        "The entrance sign at West End Hospital, listing every department")
    s = replace_img_by_alt(
        s, "The front of the Habana Medical Service building",
        WE_FRONT_CARS,
        "The front of the West End Hospital building in Kumasi")
    # Live Google Map (user, 2026-11-21): swap the whole drawn-map block
    # for the real Google Map embed. The drawn SVG is no longer used.
    pat = re.compile(r'        <div class="map-embed">.*?</div>', re.DOTALL)
    s2, n = pat.subn(MAP_LIVE_HTML, s, count=1)
    if n == 0:
        raise ValueError("map-embed block not found")
    s = s2

    # ---- 3. Colours: Habana teal/amber -> West End royal blue ----
    # (user, 2026-11-22, approved theme change). Main royal blue #1d4ed8,
    # deep navy #1e3a8a for dark areas, light blue tints #dbeafe/#eff6ff.
    # The variable NAMES stay --teal/--accent (they are only names); the
    # VALUES are all royal blue now. Buttons and calls-to-action are
    # royal blue; the sign red #dc2626 is used only for the Accidents &
    # Emergency card (see WE_CSS_OVERRIDES).
    css_vars = [
        ("--teal:#0b6e5f", "--teal:#1d4ed8"),
        ("--teal-dark:#07473d", "--teal-dark:#1e40af"),
        ("--teal-deep:#06302a", "--teal-deep:#1e3a8a"),
        ("--teal-ink:#052e28", "--teal-ink:#172554"),
        ("--teal-soft:#dff0ea", "--teal-soft:#dbeafe"),
        ("--teal-pale:#e9f4f0", "--teal-pale:#eff6ff"),
        ("--accent:#e79a35", "--accent:#1d4ed8"),
        ("--accent-dark:#c97f1d", "--accent-dark:#1e40af"),
        ("rgba(4,32,27", "rgba(29,78,216"),
        ("rgba(6,48,42", "rgba(30,58,138"),
        ("rgba(5,46,40", "rgba(29,78,216"),
        ("rgba(18,33,29", "rgba(23,37,84"),
        ("rgba(11,110,95", "rgba(29,78,216"),
        ("rgba(231,154,53", "rgba(29,78,216"),
        ("#0a4a3e", "#1d4ed8"),
    ]
    for old, new in css_vars:
        if old not in s:
            raise ValueError("CSS value not found: " + old)
        s = s.replace(old, new)
    # Hero shade: lighter overlay (user, 2026-11-22) — the royal-blue
    # shade over the hero photo was too bright and hid the building.
    # The alphas are roughly halved so the photo shows through.
    old_shade = ('.hero-full .hero-shade{position:absolute;inset:0;z-index:-1;'
                 'background:linear-gradient(90deg,rgba(29,78,216,.93) 0%,'
                 'rgba(29,78,216,.82) 34%,rgba(29,78,216,.45) 58%,'
                 'rgba(29,78,216,.12) 78%,rgba(29,78,216,.05) 100%),'
                 'linear-gradient(to top,rgba(29,78,216,.55) 0%,'
                 'rgba(29,78,216,0) 26%)}')
    new_shade = ('.hero-full .hero-shade{position:absolute;inset:0;z-index:-1;'
                 'background:linear-gradient(90deg,rgba(29,78,216,.52) 0%,'
                 'rgba(29,78,216,.46) 34%,rgba(29,78,216,.28) 58%,'
                 'rgba(29,78,216,.10) 78%,rgba(29,78,216,.04) 100%),'
                 'linear-gradient(to top,rgba(29,78,216,.30) 0%,'
                 'rgba(29,78,216,0) 26%)}')
    if old_shade not in s:
        raise ValueError("hero-shade rule not found")
    s = s.replace(old_shade, new_shade, 1)
    # brand stripe -> royal blue stripe (navy / royal / royal / royal / navy)
    s = re.sub(r'\.kente\{[^}]*\}',
               '.stripe{height:10px;margin-top:56px;background:linear-gradient(90deg,'
               'var(--teal-deep) 0%,var(--teal) 45%,var(--accent) 45%,var(--accent) 55%,'
               'var(--teal) 55%,var(--teal-deep) 100%)}', s, count=1)
    s = s.replace('<div class="kente" aria-hidden="true"></div>',
                  '<div class="stripe" aria-hidden="true"></div>')

    # ---- 4. Wholesale blocks ----
    # Stats
    stats = (
        '      <div class="stat"><p class="num">1978</p><p>Serving Kumasi since</p></div>\n'
        '      <div class="stat"><p class="num">24/7</p><p>Open 24 hours, every day</p></div>\n'
        '      <div class="stat"><p class="num">40</p><p>Hospital beds</p></div>\n'
        '      <div class="stat"><p class="num">12</p><p>Medical services</p></div>'
    )
    s = sub_block(s, r'<div class="stats" style="margin-top:0">\n',
                  r'\n    </div>\n  </section>',
                  '<div class="stats" style="margin-top:0">\n' + stats +
                  '\n    </div>\n  </section>', "stats")
    # Home service preview grid (first 6 services)
    home_cards = "\n      ".join(svc_card(i, svc) for i, svc in enumerate(SERVICES[:6]))
    s = sub_block(s, r'<div class="svc-grid">\n', r'\n    </div>\n  </section>',
                  '<div class="svc-grid">\n      ' + home_cards +
                  '\n    </div>\n  </section>', "home svc-grid")
    # Services page grid (all 12)
    all_cards = "\n      ".join(svc_card(i, svc) for i, svc in enumerate(SERVICES))
    s = sub_block(s, r'<div class="svc-grid" id="svcGrid">\n', r'\n    </div>\n  </section>',
                  '<div class="svc-grid" id="svcGrid">\n      ' + all_cards +
                  '\n    </div>\n  </section>', "services svc-grid")
    # Diagnostics pills (appears twice, identical)
    old_pills = (
        '            <span class="pill">CT Scan</span>\n'
        '            <span class="pill">Ultrasound</span>\n'
        '            <span class="pill">Mammography</span>\n'
        '            <span class="pill">ECG</span>\n'
        '            <span class="pill">Echocardiography</span>\n'
        '            <span class="pill">Laboratory tests</span>'
    )
    new_pills = (
        '            <span class="pill">Ultrasound</span>\n'
        '            <span class="pill">Laboratory tests</span>\n'
        '            <span class="pill">ECG</span>'
    )
    if s.count(old_pills) != 2:
        raise ValueError("expected 2 diagnostics pill rows, found %d" % s.count(old_pills))
    s = s.replace(old_pills, new_pills)
    # Teaser body + awards list
    s = s.replace(
        '<p class="body">Founded in 2011 by Dr Thomas Winsum Anabah, a Consultant '
        'Anaesthesiologist, HMS began as a small day clinic. Today our physicians, '
        'nurses, pharmacists, laboratory scientists and radiographers work together '
        'to give every patient coordinated, compassionate care.</p>',
        '<p class="body">Founded in 1978 by Dr Jacob Kwakye-Maafo and his wife Mercy, '
        'West End Hospital — known locally as Kwakye-Maafo Hospital — has cared for '
        'Kumasi families for nearly fifty years. Our physicians, nurses, midwives, '
        'laboratory scientists and pharmacists work together to give every patient '
        'coordinated, compassionate care.</p>')
    s = sub_block(
        s, r'<ul class="why-list">\n', r'\n        </ul>',
        '        <ul class="why-list">\n'
        '          <li><strong>Nearly 50 years of care</strong><span>Founded in 1978 by Dr Jacob Kwakye-Maafo and his wife Mercy — known locally as Kwakye-Maafo Hospital</span></li>\n'
        '          <li><strong>NHIS-accredited</strong><span>An NHIS Office on site, so you can register, renew and use your card here</span></li>\n'
        '          <li><strong>24/7</strong><span>Open 24 hours, every day, including weekends and public holidays</span></li>\n'
        '        </ul>', "why-list")
    # Awards section -> facilities section
    facilities = (
        '  <section class="block wrap">\n'
        '    <p class="eyebrow">Our facilities</p>\n'
        '    <h2>Everything under one roof.</h2>\n'
        '    <div class="values-grid" style="margin-top:36px">\n'
        '      <article class="value-card"><h3>Mercy Golightly Unit</h3><p>Our outpatient department, named after Mercy Kwakye-Maafo née Golightly, a retired nurse and the hospital&rsquo;s co-founder.</p></article>\n'
        '      <article class="value-card"><h3>Maternity unit</h3><p>Antenatal care, safe delivery and ultrasound on site.</p></article>\n'
        '      <article class="value-card"><h3>Laboratory &amp; ECG</h3><p>An on-site laboratory and ECG, so results come back quickly.</p></article>\n'
        '      <article class="value-card"><h3>Pharmacy on site</h3><p>Collect your prescribed medicines before you leave the hospital.</p></article>\n'
        '      <article class="value-card"><h3>NHIS Office on site</h3><p>Register, renew and use your NHIS card without leaving the hospital.</p></article>\n'
        '      <article class="value-card"><h3>Open 24 hours</h3><p>Open 24 hours, every day, including weekends and public holidays.</p></article>\n'
        '    </div>\n'
        '    <p class="award-note">Find us on Dr Kwakye-Maafo Avenue, Edwenase Kwadaso, Kumasi.</p>\n'
        '  </section>'
    )
    s = sub_block(s, r'  <section class="block wrap">\n    <p class="eyebrow">Recognition</p>',
                  r'\n  </section>', facilities, "awards section")
    # Contact form + booking modal service selects
    contact_opts = (
        '            <option value="">Choose a service…</option>\n'
        '            <option>Book an appointment</option>\n'
        + "".join('            <option>{}</option>\n'.format(svc["name"].replace("&", "&amp;"))
                   for svc in SERVICES)
        + '            <option>General enquiry</option>'
    )
    s = sub_block(s, r'<select id="service" name="service">\n', r'\n          </select>',
                  '<select id="service" name="service">\n' + contact_opts +
                  '\n          </select>', "contact select")
    book_opts = (
        '            <option value="">Choose a service…</option>\n'
        + "".join('            <option>{}</option>\n'.format(svc["name"].replace("&", "&amp;"))
                   for svc in SERVICES).rstrip("\n")
    )
    s = sub_block(s, r'<select id="bkService" name="bkService">\n', r'\n          </select>',
                  '<select id="bkService" name="bkService">\n' + book_opts +
                  '\n          </select>', "booking select")
    # Hours table: drop the cervical clinic row (West End does not list
    # it); add the visiting hours from the hospital's own signboard.
    # Visiting hours are NOT opening hours — the hospital is open 24/7.
    s = s.replace(
        '<tr><td>Cervical screening clinic</td><td>Fridays, 9:00 AM</td></tr>',
        '<tr><td>Visiting hours (morning)</td><td>5:00 – 7:00 AM</td></tr>\n'
        '          <tr><td>Visiting hours (evening)</td><td>4:00 – 6:00 PM</td></tr>')
    # Remove Habana staff sign-in + map credit. West End has no social
    # media pages — the footer social links are removed entirely.
    s = sub_block(s, r'        <div class="foot-social">\n', r'\n        </div>',
                  '', "footer social")
    s = re.sub(r'\s*<li><a class="dim" href="https://habanamedicalservice\.lovable\.app/"[^>]*>Staff sign in</a></li>',
               '', s, count=1)
    s = re.sub(r'\s*<a class="map-credit"[^>]*>[^<]*</a>', '', s, count=1)
    # JS data
    s = sub_block(s, r'  var PH = \{\n', r'\n  \};', js_ph(), "PH map")
    s = sub_block(s, r'  var SERVICES = \[\n', r'\n  \];',
                  js_services(), "SERVICES array")
    s = sub_block(s, r'  var SLIDES = \[\n', r'\n  \];', js_slides(), "SLIDES array")
    s = sub_block(s, r'  var HERO_SLIDES = \[\n', r'\n  \];',
                  js_hero_slides(), "HERO_SLIDES array")
    if 'var heroImgs = [document.getElementById("heroImg"), document.getElementById("heroImg2")];' not in s:
        raise ValueError("heroImgs array not found")
    s = s.replace('var heroImgs = [document.getElementById("heroImg"), document.getElementById("heroImg2")];',
                  'var heroImgs = [document.getElementById("heroImg"), document.getElementById("heroImg2"), document.getElementById("heroImg3")];', 1)
    s = sub_block(s, r'  var SERVICE_ALIASES = \[\n', r'\n  \];',
                  js_aliases(), "SERVICE_ALIASES array")

    # ---- 5. Explicit text replacements (exact strings) ----
    explicit = [
        ('<title>Habana Medical Service — Tamale</title>',
         '<title>West End Hospital — Kumasi</title>'),
        ('<meta name="description" content="Habana Medical Service, Tamale — a private multidisciplinary hospital open 24/7. Fifteen specialties, diagnostics on site, and care guided by love and honesty." />',
         '<meta name="description" content="West End Hospital, Kumasi — a private general hospital open 24/7. Twelve services, including maternity, paediatrics and surgery, and an NHIS Office on site." />'),
        ('<span class="brand-sub">Service · Tamale</span>',
         '<span class="brand-sub">General Hospital · Kumasi</span>'),
        ('home: "Habana Medical Service — Tamale",',
         'home: "West End Hospital — Kumasi",'),
        ('services: "Services | Habana Medical Service, Tamale",',
         'services: "Services | West End Hospital, Kumasi",'),
        ('about: "About us | Habana Medical Service, Tamale",',
         'about: "About us | West End Hospital, Kumasi",'),
        ('contact: "Contact & Directions | Habana Medical Service, Tamale"',
         'contact: "Contact & Directions | West End Hospital, Kumasi"'),
        ('Celebrating 15 years of care · 2011–2026',
         'A private hospital in Kumasi · Since 1978'),
        ('<h1>Care with <em>love</em> and <em>honesty</em>, every hour of the day.</h1>',
         '<h1>Trusted care for Kumasi, <em>day and night</em>.</h1>'),
        ('Habana Medical Service is one of Northern Ghana&rsquo;s leading private hospitals — specialist doctors, modern diagnostics and a calm, welcoming place to heal, right here in Tamale.',
         'West End Hospital is a private general hospital in Kumasi — specialist doctors, maternity and children&rsquo;s care, and a calm, welcoming place to heal, on Dr Kwakye-Maafo Avenue in Edwenase Kwadaso.'),
        ('<h1>Fifteen years of <em>love and honesty</em> in healthcare.</h1>',
         '<h1>Nearly fifty years of <em>care for Kumasi</em>.</h1>'),
        ('What began in 2011 as a day clinic in a converted four-bedroom house is now one of Northern Ghana&rsquo;s leading private hospitals.',
         'What began in 1978 as a small clinic in Kumasi is now West End Hospital — a private general hospital with 40 beds, known locally as Kwakye-Maafo Hospital.'),
        ('<h2>Founded by a doctor who believed Tamale deserved more.</h2>',
         '<h2>Founded by a doctor who believed Kumasi deserved more.</h2>'),
        ('Habana Medical Service was established in the Tamale metropolis by <strong>Dr Thomas Winsum Anabah</strong>, a Consultant Anaesthesiologist with a Master&rsquo;s in Critical Care and Emergencies. The first patients were walk-in clients living with non-communicable diseases.',
         'West End Hospital was founded in 1978 by <strong>Dr Jacob Kenneth Kofi Kwakye-Maafo</strong>, a physician and surgeon specialising in obstetrics and women&rsquo;s health, and a former president of the Ghana Medical Association, together with his wife <strong>Mercy Kwakye-Maafo née Golightly</strong>, a retired nurse. What began as a small clinic grew into a hospital — and the outpatient department is still named the Mercy Golightly Unit, after her.'),
        ('Today HMS brings together doctors, nurses and support staff across internal medicine, emergency and critical care, paediatrics, public health, obstetrics and gynaecology, ENT, anaesthesia and surgery — with specialists on call around the clock.',
         'Today West End Hospital brings together doctors, nurses, midwives and support staff across outpatient care, emergency, surgery, maternity, paediatrics, laboratory and pharmacy — with specialists on call around the clock.'),
        ('Set in a serene environment, our hospital is designed to feel like a home away from home.',
         'Our hospital is designed to feel like a home away from home — with a pharmacy, laboratory and NHIS Office on site.'),
        ('<p>Health education and prevention for families across the North.</p>',
         '<p>Health education and prevention for families across Kumasi and the Ashanti Region.</p>'),
        ('<span class="cap" id="carCap">1 / 7 · International award ceremony</span>',
         '<span class="cap" id="carCap">1 / 10 · Our hospital</span>'),
        ('<h2>A home away from home — with world-class standards.</h2>',
         '<h2>A hospital Kumasi has trusted since 1978.</h2>'),
        ('<p class="foot-blurb">A private multidisciplinary hospital serving Tamale and Northern Ghana since 2011. Guided by our motto, &ldquo;Love and Honesty.&rdquo;</p>',
         '<p class="foot-blurb">A private general hospital serving Kumasi since 1978. Known locally as Kwakye-Maafo Hospital.</p>'),
        # Call card subtext stays plain: the landline is already shown as a
        # big link above it, so "Also 032..." would just repeat it.
        # Contact lede: West End has NO email — do not offer one.
        ('Call, WhatsApp or email us to book a visit',
         'Call or WhatsApp us to book a visit'),
        # Footer contact list: landline under the mobile.
        # (Source form — Habana's number; the transform runs before the
        # blanket number swap, so match the original.)
        ('</svg><span><a href="tel:+233233186766">023 318 6766</a></span></li>',
         '</svg><span><a href="tel:+233245460006">024 546 0006</a><br><a href="tel:+233322022590">032 202 2590</a></span></li>'),
        # Contact Call card: mobile first (best first contact), landline second.
        ('        <p class="cbig"><a href="tel:+233233186766">023 318 6766</a></p>',
         '        <p class="cbig"><a href="tel:+233245460006">024 546 0006</a><br><a href="tel:+233322022590">032 202 2590</a></p>'),
        ('Near Kamina Barracks, off GILLBT Road.',
         'On Dr Kwakye-Maafo Avenue, Edwenase Kwadaso, Kumasi.'),
        ('Opposite the School of Hygiene, Tamale, Ghana</span></p>',
         'Edwenase Kwadaso, Kumasi, Ghana · P.O. Box KS 4368</span></p>'),
        ('For CT scan and imaging bookings, call ahead so we can prepare',
         'For ultrasound and scan bookings, call ahead so we can prepare'),
        ('Our imaging and laboratory teams help your doctor diagnose quickly and start the right treatment sooner.',
         'Our laboratory team helps your doctor diagnose quickly and start the right treatment sooner.'),
        ('destination=Nanton%20Road%2C%20Block%20141%2C%20North%20Kanvilli%2C%20Opposite%20School%20of%20Hygiene%2C%20Tamale%2C%20Ghana',
         'destination=' + WE_MAPS_DEST),
        ('destination=Habana%20Medical%20Service%2C%20Nanton%20Road%2C%20Block%20141%2C%20North%20Kanvilli%2C%20Tamale%2C%20Ghana',
         'destination=' + WE_MAPS_DEST),
        ('Habana Medical Service Ltd.', 'West End Hospital'),
        ('/* kente stripe + footer */', '/* brand stripe + footer */'),
        # West End has NO email — remove the email sentence entirely
        # (do not invent an address). Visitors can call or WhatsApp.
        ('Sending opens WhatsApp with your message ready to go — nothing is sent until you press send there. Prefer email? Write to <a href="mailto:habanamedicalservice@gmail.com">habanamedicalservice@gmail.com</a>. Prefer to talk? Call <a href="tel:+233233186766">023 318 6766</a>.',
         'Sending opens WhatsApp with your message ready to go — nothing is sent until you press send there. Prefer to talk? Call <a href="tel:+233245460006">024 546 0006</a>.'),
        # Sidebar Facebook button: remove it (West End has no socials).
        ('<a class="btn btn-outline" href="https://web.facebook.com/HabanaMedicalService" target="_blank" rel="noopener">Facebook — @HabanaMedicalService</a>',
         ''),
        # Sidebar email card: remove it (West End has no email).
        ('      <article class="card ccard">\n        <span class="cicon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg></span>\n        <p class="clabel">Email</p>\n        <p class="cbig">Write to us</p>\n        <p><a href="mailto:habanamedicalservice@gmail.com">habanamedicalservice@gmail.com</a></p>\n      </article>\n',
         ''),
        # Footer mail link: remove it (West End has no email).
        ('          <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg><span><a href="mailto:habanamedicalservice@gmail.com">habanamedicalservice@gmail.com</a></span></li>\n',
         ''),
        # Chat panel contact details: no email line at all.
        ('You can reach the hospital team any time:\\nPhone: 023 318 6766\\nEmail: habanamedicalservice@gmail.com\\nWhatsApp: tap the button below.\\nWe are open 24 hours, every day.',
         'You can reach the hospital team any time:\\nPhone: 024 546 0006 or 032 202 2590\\nWhatsApp: tap the button below.\\nWe are open 24 hours, every day.'),
        # Address blocks (find-panel, map footer, page footer, map head,
        # chat location topics).
        ('<p class="addr"><span>Nanton Road, Block 141, North Kanvilli</span><span>Opposite the School of Hygiene</span><span>Tamale, Northern Region, Ghana</span></p>',
         '<p class="addr"><span>Dr Kwakye-Maafo Avenue, Edwenase Kwadaso</span><span>Kumasi, Ashanti Region, Ghana</span><span>P.O. Box KS 4368 · Plus code 6CRWM8GX+H9</span></p>'),
        ('<p class="map-addr">Nanton Road, Block 141, North Kanvilli<span>Edwenase Kwadaso, Kumasi, Ghana · P.O. Box KS 4368</span></p>',
         '<p class="map-addr">Dr Kwakye-Maafo Avenue, Edwenase Kwadaso, Kumasi<span>P.O. Box KS 4368, Kumasi, Ghana</span></p>'),
        ('<span>Nanton Road, Block 141, North Kanvilli, Opposite the School of Hygiene, Tamale, Northern Region, Ghana</span>',
         '<span>Dr Kwakye-Maafo Avenue, Edwenase Kwadaso, Kumasi, Ashanti Region, Ghana</span>'),
        ('Habana Medical Service — North Kanvilli, Tamale.',
         'West End Hospital — Edwenase Kwadaso, Kumasi.'),
        ('You will find us at Nanton Road, Block 141, North Kanvilli, opposite the School of Hygiene, Tamale, Northern Region, Ghana.',
         'You will find us at Dr Kwakye-Maafo Avenue, Edwenase Kwadaso, Kumasi, Ashanti Region, Ghana.'),
        ('We are at Nanton Road, Block 141, North Kanvilli, opposite the School of Hygiene, Tamale — open 24 hours, every day.',
         'We are at Dr Kwakye-Maafo Avenue, Edwenase Kwadaso, Kumasi — open 24 hours, every day.'),
        # Chat topic 4: cervical clinic (Friday 9:00 AM, not a West End
        # service) -> maternity and antenatal care.
        ('/* 4 — cervical screening clinic */\n    if (containsAny(t, ["cervical", "pap smear", "pap test"])) {\n      var og = SERVICES[findService("Obstetrics & Gynaecology")];\n      return {\n        text: "Our cervical screening clinic runs every Friday at 9:00 AM, under Obstetrics & Gynaecology. Screening checks the neck of the womb for early changes, so problems can be treated early.\\nYou can book ahead, or call us on 023 318 6766 if you have questions.",\n        actions: [bookAction(og.name), callAction()]\n      };\n    }',
         '/* 4 — maternity and antenatal care */\n    if (containsAny(t, ["antenatal", "pregnan", "expecting a baby", "give birth", "delivery", "maternity"])) {\n      var og = SERVICES[findService("Maternity & Obstetrics")];\n      return {\n        text: "Our maternity team cares for mothers through pregnancy, birth and the weeks after delivery, with antenatal care and ultrasound on site.\\nYou can book ahead, or call us on 024 546 0006 if you have questions.",\n        actions: [bookAction(og.name), callAction()]\n      };\n    }'),
        # NHIS topic (new): West End IS NHIS-accredited, with an NHIS
        # Office on site — say so plainly.
        ('    /* 8 — prices: never invent figures */',
         '    /* 7b — NHIS */\n    if (containsAny(t, ["nhis", "insurance", "health insurance"])) {\n      return {\n        text: "Yes — West End Hospital is NHIS-accredited, and we have an NHIS Office right here in the hospital. Bring your NHIS card when you visit. For questions about what your card covers, call or WhatsApp us on 024 546 0006.",\n        actions: [callAction(), waAction()]\n      };\n    }\n\n    /* 8 — prices: never invent figures */'),
        # Prices topic: NHIS/insurance now answered by the topic above.
        ('    if (containsAny(t, ["price", "prices", "cost", "how much", "charges", "fees", " nhis ", "insurance", "do you take insurance", "payment"])) {',
         '    if (containsAny(t, ["price", "prices", "cost", "how much", "charges", "fees", "payment"])) {'),
        # HEALTH basics: pregnancy topic points at Maternity & Obstetrics.
        ('service: "Obstetrics & Gynaecology", urgent: true,',
         'service: "Maternity & Obstetrics", urgent: true,'),
        ('Our Obstetrics & Gynaecology team provides antenatal care and ultrasound scans here at the hospital.',
         'Our Maternity & Obstetrics team provides antenatal care and ultrasound scans here at the hospital.'),
        # HEALTH basics: the malaria topic points at the Laboratory service.
        ('service: "Medical Laboratory", urgent: true,',
         'service: "Laboratory & Diagnostics", urgent: true,'),
        # HEALTH basics: West End HAS a Paediatrics service — the
        # paediatrics topic and its team link stay as they are.
        # Booking date + time (user, 2026-11-21): the form must let the
        # customer pick the date and time they want to book for.
        ('Fill in your details and choose the service you need',
         'Fill in your details, pick a date and time, and choose the service you need'),
        ('''          <p class="error">Please choose the service you want.</p>
        </div>
        <button class="btn btn-accent" type="submit" style="width:100%">Book now</button>''',
         '''          <p class="error">Please choose the service you want.</p>
        </div>
        <div class="field" id="bf-date">
          <label for="bkDate">Preferred date <span class="req" aria-hidden="true">*</span></label>
          <input type="date" id="bkDate" name="bkDate" />
          <p class="error">Please choose a date for your appointment.</p>
        </div>
        <div class="field" id="bf-time">
          <label for="bkTime">Preferred time <span class="req" aria-hidden="true">*</span></label>
          <input type="time" id="bkTime" name="bkTime" />
          <p class="error">Please choose a time for your appointment.</p>
        </div>
        <button class="btn btn-accent" type="submit" style="width:100%">Book now</button>'''),
        # Booking submit: read and validate the date and time.
        ('''    var service = bkSelect.selectedIndex > 0 ? bkSelect.options[bkSelect.selectedIndex].text : "";
    var ok = true;
    ok = bkInvalid("bf-name", !name) && ok;
    ok = bkInvalid("bf-phone", !phone) && ok;
    ok = bkInvalid("bf-service", !service) && ok;''',
         '''    var service = bkSelect.selectedIndex > 0 ? bkSelect.options[bkSelect.selectedIndex].text : "";
    var dateVal = document.getElementById("bkDate").value;
    var timeVal = document.getElementById("bkTime").value;
    var todayStart = new Date(); todayStart.setHours(0, 0, 0, 0);
    var pickedDate = dateVal ? new Date(dateVal + "T00:00:00") : null;
    var ok = true;
    ok = bkInvalid("bf-name", !name) && ok;
    ok = bkInvalid("bf-phone", !phone) && ok;
    ok = bkInvalid("bf-service", !service) && ok;
    ok = bkInvalid("bf-date", !dateVal || (pickedDate && pickedDate < todayStart)) && ok;
    ok = bkInvalid("bf-time", !timeVal) && ok;'''),
        # Booking WhatsApp message: include the chosen date and time.
        ('    lines.push("Service: " + service);',
         '    lines.push("Service: " + service);\n    lines.push("Preferred date: " + fmtBookDate(dateVal));\n    lines.push("Preferred time: " + fmtBookTime(timeVal));'),
        # Booking confirmation: show the chosen date and time.
        (r'''      "Thank you, " + name.split(" ")[0] + ". Your booking for \u201C" + service +
      "\u201D is ready \u2014 tap below to send the details to the hospital on WhatsApp, or call us on 023 318 6766.";''',
         '''      "Thank you, " + name.split(" ")[0] + ". Your booking for “" + service +
      "” on " + fmtBookDate(dateVal) + " at " + fmtBookTime(timeVal) +
      " is ready — tap below to send the details to the hospital on WhatsApp, or call us on 024 546 0006.";'''),
        # Clear the date/time errors as soon as the customer changes them.
        ('["bkName", "bkPhone", "bkService"]',
         '["bkName", "bkPhone", "bkService", "bkDate", "bkTime"]'),
        # Name placeholders: use a West End-style example name.
        ('e.g. Ama Mensah', 'e.g. Kwame A.'),
    ]
    for old, new in explicit:
        if old not in s:
            raise ValueError("explicit string not found: " + old[:80])
        s = s.replace(old, new)
    # West End has no email, so the contact form must not offer "Email"
    # as a way for the hospital to reply.
    s2, n = re.subn(r'\s*<label class="radio-pill"><input type="radio" name="reply" value="Email" /><span>Email</span></label>',
                    '', s, count=1)
    if n == 0:
        raise ValueError("reply-method Email radio not found")
    s = s2

    # ---- 6. Blanket replacements (ordered, longest first) ----
    # NOTE: the mobile 024 546 0006 is the main number for display +
    # tel: links and for the wa.me links (ASSUMED WhatsApp number,
    # unconfirmed). The tel: form must be replaced before the bare-number
    # form, or it gets corrupted. Habana is in Tamale; West End is in
    # Kumasi, so Tamale -> Kumasi and Northern Region -> Ashanti Region.
    blanket = [
        ("Habana Medical Service", "West End Hospital"),
        ("Habana Medical", "West End"),
        ("habana", "west end"),
        ("023 318 6766", WE_PHONE),
        ("+233233186766", WE_PHONE_TEL),
        ("233233186766", WE_PHONE_WA),
        ("Nanton Road, Block 141, North Kanvilli", "Dr Kwakye-Maafo Avenue, Edwenase Kwadaso"),
        ("Opposite the School of Hygiene", "Edwenase Kwadaso, Kumasi"),
        ("opposite the School of Hygiene", "in Edwenase Kwadaso"),
        ("North Kanvilli", "Edwenase Kwadaso"),
        ("Northern Region", "Ashanti Region"),
        ("Northern Ghana", "Kumasi and the Ashanti Region"),
        ("across the North", "across Kumasi"),
        ("Tamale", "Kumasi"),
        ("Fifteen", "Twelve"),
        ("fifteen", "twelve"),
        ("15 services", "12 services"),
        ("15 Medical", "12 Medical"),
        ("Habana", "West End"),
    ]
    for old, new in blanket:
        s = s.replace(old, new)
    s = re.sub(r'\bHMS\b', 'West End', s)

    # ---- 7. Safety net: any photo still embedded from Habana -> generic placeholder.
    # Every real photo (building, entrance sign, front view + all stock
    # and generated photos) is kept as-is.
    keep = {WE_BUILDING_DAY, WE_INTERIOR, WE_FRONT_CARS}
    keep.update(_photo_uri(k) for k in PH)
    counter = [0]

    def _generic(m):
        if m.group(0) in keep:
            return m.group(0)
        i = counter[0]
        counter[0] += 1
        return ph("West End Hospital", "Kumasi",
                  800, 600, variant=i)

    s = re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', _generic, s)

    # ---- 8. West End overrides: side padding, logo-only chat button, reviews ----
    # (a) CSS overrides, appended last in the stylesheet so they win.
    if s.count("</style>") != 1:
        raise ValueError("expected exactly one </style>, found %d" % s.count("</style>"))
    s = s.replace("</style>", WE_CSS_OVERRIDES + "</style>", 1)
    # (a2) Preview countdown timer bar (user, 2026-11-21): at the very top,
    # above the Open 24/7 bar.
    if s.count('<body id="top">') != 1:
        raise ValueError("body tag not found")
    s = s.replace('<body id="top">', '<body id="top">\n\n' + PREVIEW_TIMER_HTML, 1)
    # (b) Reviews section at the end of the home page, after the About teaser.
    rev_anchor = '  </section>\n</div>\n\n<!-- ================= SERVICES ================= -->'
    if s.count(rev_anchor) != 1:
        raise ValueError("reviews anchor not found")
    s = s.replace(rev_anchor,
                  '  </section>\n' + REVIEWS_SECTION +
                  '\n</div>\n\n<!-- ================= SERVICES ================= -->', 1)
    # (c) Reviews on the About page (after the facilities section) and in the
    #     contact page's left column (under the form) — the two yellow-marked gaps.
    about_anchor = '  </section>\n</div>\n\n<!-- ================= CONTACT ================= -->'
    if s.count(about_anchor) != 1:
        raise ValueError("about reviews anchor not found")
    s = s.replace(about_anchor,
                  '  </section>\n' + REVIEWS_SECTION +
                  '\n</div>\n\n<!-- ================= CONTACT ================= -->', 1)
    contact_anchor = '    </div>\n\n    <aside class="panel">'
    if s.count(contact_anchor) != 1:
        raise ValueError("contact reviews anchor not found")
    s = s.replace(contact_anchor,
                  CONTACT_REVIEWS + '\n    </div>\n\n    <aside class="panel">', 1)
    aside_anchor = '      </article>\n    </aside>\n  </section>\n</div>\n</main>'
    if s.count(aside_anchor) != 1:
        raise ValueError("contact aside anchor not found")
    s = s.replace(aside_anchor,
                  '      </article>\n' + CONTACT_REVIEW_RIGHT +
                  '\n    </aside>\n  </section>\n</div>\n</main>', 1)
    # (d) Mission + Vision above the core-values cards; rename the heading.
    if s.count('<h2>Our values</h2>') != 1:
        raise ValueError("values heading not found")
    s = s.replace('<h2>Our values</h2>',
                  MISSION_VISION_HTML + '      <h2>Our core values</h2>', 1)
    # (d) Pop-in + chat button + booking date/time scripts, just before </body>.
    if s.count("</body>") != 1:
        raise ValueError("expected exactly one </body>, found %d" % s.count("</body>"))
    s = s.replace("</body>", POP_IN_JS + CHAT_FAB_JS + BOOKING_DATETIME_JS + PREVIEW_TIMER_JS + REVIEW_FORM_JS + "</body>", 1)
    # (d) Chat button: keep the "Chat with us" text (it expands on load and
    # shrinks to the logo after 3 seconds — user, 2026-11-21); drop only the
    # chat icon SVG. Start expanded in the HTML itself so the button is open
    # from the first paint, with no flash (the script only runs the timer).
    if s.count('<span>Chat with us</span>') != 1:
        raise ValueError("chat fab text not found")
    s = s.replace('<button class="chat-fab" id="chatFab"',
                  '<button class="chat-fab expanded" id="chatFab"', 1)
    s = re.sub(r'(<button class="chat-fab[^"]*"[^>]*>.*?<span class="fab-logo"[^>]*>.*?</span>)\s*<svg[^>]*>.*?</svg>',
               r'\1', s, count=1, flags=re.DOTALL)
    return s


# ---------------------------------------------------------------- verify
FORBIDDEN = [
    "Habana", "habana", "Anabah", "2011", "Siemens", "SOMATOM",
    "mammograph", "Mammograph", "Fifteen", "fifteen", "15 services",
    "Echocardiography", "lovable", "facebook.com", "instagram.com",
    "tiktok.com", "Kamina", "GILLBT", "School of Hygiene", "Nanton Road",
    "North Kanvilli", "kente", "Kente", "Friday at 9:00 AM", "Fridays, 9:00 AM",
    "9:00 AM", "Endoscopy", "Ophthalmology", "Neurosurgery", "Psychology",
    "Obstetrics & Gynaecology", "Gynaecology", "gynaecology",
    "delinternationalhospital", "East Legon", "Accra", "Nii Sai",
    "PH Hotel", "Kotoka", "030 254", "Fertility", "fertility", "IVF", "ICSI",
    "IUI", "X-ray", "dialysis", "Dialysis",
    "cervical", "Cervical", "Ridge Hospital", "Kokroko", "El-Yahweh",
    "Emergency & Critical Care", "Diagnostic Imaging", "Dietetics",
    "Counselling", "Preventive Healthcare", "Internal Medicine",
    "Medical Laboratory",
    # West End is in Kumasi — Tamale and the north must not leak in.
    "Tamale", "Northern",
    # Address conflict: the site uses the Google Maps address
    # (Edwenase Kwadaso). Patasi is for the README/pitch only.
    "Patasi", "020 812 4847", "1979", "West African", "Evelyn Hockstein",
    "Ohio",
    # Services West End does not offer.
    "Urology", "Dental", "dental", "Rehabilitation Care",
    "Mother & Child Care", "Optical Clinic", "Minor Theatre",
    "Physiotherapy", "Health Screenings", "Inpatient Care",
    # No email anywhere on the site (none found for West End).
    "gmail.com", "mailto:",
    # Al-Kawthar / City Hospital leftovers (this build must not contain any).
    "Al-Kawthar", "alkawthar", "Wifaq", "Watherson", "C56G+7W",
    "0553 602 241", "024 415 8915", "alkawtharhospital",
    "first Islamic", "First Islamic", "Anbariya", "Sunni", "Tijania",
    "Shia", "Sheikh", "female ward", "Female ward",
    "City Hospital", "cityhospitalgh", "Old Amakom", "Star Junction",
    "Baba Yara", "032 202 4470", "024 662", "020 568", "Adinkra", "Gyesi",
    "Modern Ghana", "modernghana", "1976",
]
FORBIDDEN_WORDS = [r"\bHMS\b", r"\bENT\b", r"\bCT\b", r"\bMRI\b", r"\bICU\b",
                    r"\bDel\b"]


def verify(s):
    problems = []
    # Strip embedded images first: base64 blobs can contain substrings
    # like "2011" or "CT" by coincidence.
    text = re.sub(r'data:image/[^"\']+;base64,[A-Za-z0-9+/=]+', '', s)
    for token in FORBIDDEN:
        if token in text:
            problems.append("forbidden token present: %r" % token)
    for pat in FORBIDDEN_WORDS:
        if re.search(pat, text):
            problems.append("forbidden word present: %s" % pat)
    checks = {
        "svc-card buttons": s.count('class="svc-card"'),
        "Outpatient Consultation": s.count("Outpatient Consultation"),
        "Accidents & Emergency": s.count("Accidents &amp; Emergency"),
        "General Surgery & Theatre": s.count("General Surgery &amp; Theatre"),
        "Maternity & Obstetrics": s.count("Maternity &amp; Obstetrics"),
        "Paediatrics": s.count("Paediatrics"),
        "Laboratory & Diagnostics": s.count("Laboratory &amp; Diagnostics"),
        "Pharmacy": s.count("Pharmacy"),
        "ECG": s.count("ECG"),
        "EPI (Immunisation)": s.count("EPI (Immunisation)"),
        "MCH (Maternal & Child Health)": s.count("MCH (Maternal &amp; Child Health)"),
        "Family Planning": s.count("Family Planning"),
        "NHIS Office": s.count("NHIS Office"),
        "West End Hospital": s.count("West End Hospital"),
        "024 546 0006": s.count("024 546 0006"),
        "032 202 2590": s.count("032 202 2590"),
        "Dr Kwakye-Maafo Avenue": s.count("Dr Kwakye-Maafo Avenue"),
        "6CRWM8GX+H9": s.count("6CRWM8GX+H9"),
        "P.O. Box KS 4368": s.count("P.O. Box KS 4368"),
        "1978": s.count("1978"),
        "40 beds": s.count("40 beds"),
        "Mercy Golightly": s.count("Mercy Golightly"),
        "Kwakye-Maafo": s.count("Kwakye-Maafo"),
        "Visiting hours": s.count("Visiting hours"),
        "NHIS": s.count("NHIS"),
        "building day photo uses": s.count(WE_BUILDING_DAY),
        "interior photo uses": s.count(WE_INTERIOR),
        "front-cars photo uses": s.count(WE_FRONT_CARS),
        "gen maternity uses": s.count(_photo_uri("westend-gen-maternity")),
        "gen emergency uses": s.count(_photo_uri("westend-gen-emergency")),
        "gen surgery uses": s.count(_photo_uri("westend-gen-surgery")),
        "gen lab uses": s.count(_photo_uri("westend-gen-lab")),
        "gen pharmacy uses": s.count(_photo_uri("westend-gen-pharmacy")),
        "gen paeds uses": s.count(_photo_uri("westend-gen-paeds")),
        "real waiting uses": s.count(_photo_uri("westend-real-waiting")),
        "real waiting-people uses": s.count(_photo_uri("westend-real-waiting-people")),
        "real consulting uses": s.count(_photo_uri("westend-real-consulting")),
        "real lounge uses": s.count(_photo_uri("westend-real-lounge")),
        "real night uses": s.count(_photo_uri("westend-real-night")),
        "real van uses": s.count(_photo_uri("westend-real-van")),
        "real street uses": s.count(_photo_uri("westend-real-street")),
        "imaging1 uses": s.count(_photo_uri("imaging1")),
        "logo svg uses": s.count(LOGO),
        "svg data URIs total": s.count("data:image/svg+xml"),
        "patient reviews section": s.count("What our patients say"),
        "sample reviews note": s.count("These are sample reviews"),
        "chat fab text": s.count("<span>Chat with us</span>"),
        "chat fab script": s.count("// Chat button: pops open on load"),
        "chat fab expanded rule": s.count(".chat-fab.expanded"),
        "chat fab starts expanded": s.count('class="chat-fab expanded"'),
        # The chat-bubble SVG path appears 3 times, all on WhatsApp links.
        # If the fab's bubble icon came back it would be 4.
        "chat bubble icons": s.count('M21 11.5a8.38 8.38 0 0 1-.9 3.8'),
        "booking date field": s.count('id="bkDate"'),
        "booking time field": s.count('id="bkTime"'),
        "booking date in message": s.count('Preferred date: " + fmtBookDate(dateVal)'),
        "booking time in message": s.count('Preferred time: " + fmtBookTime(timeVal)'),
        "booking datetime script": s.count("// Booking date/time helpers"),
        "css overrides": s.count("West End overrides (2026-11-22)"),
        "review cards": s.count('class="value-card review-card"'),
        "pop-in keyframes": s.count("@keyframes wePopIn"),
        "pop-in script": s.count("// Pop-in on load and on scroll."),
        "our core values": s.count("Our core values"),
        "old values heading": s.count("<h2>Our values</h2>"),
        "our mission": s.count("Our Mission"),
        "our vision": s.count("Our Vision"),
        "mission grid": s.count('class="mission-grid"'),
        "preview timer bar": s.count('id="previewTimer"'),
        "preview timer script": s.count("// Preview countdown timer:"),
        "live map iframe": s.count('class="map-live-frame"'),
        "review forms": s.count('class="review-form"'),
        "review form script": s.count("// Customer review form:"),
        "emergency red": s.count("#dc2626"),
        "gallery counter": s.count("1 / 10 · Our hospital"),
        "btn accent white": s.count(".btn-accent{color:#fff}"),
        "dark card numbers white": s.count(".ccard.dark .cbig a{color:#fff}"),
        "footer hover light": s.count(".foot-links a:hover,.foot-links button:hover,.foot-service-links button:hover{color:#dbeafe}"),
        "header fade script": s.count("// Transparent header on scroll (user, 2026-11-22):"),
        "timer fixed": s.count("justify-content:center;position:fixed;top:0;left:0;right:0;z-index:1000"),
        "header fixed": s.count("header.site{position:fixed;left:0;right:0;z-index:999}"),
        "header scrolled quarter": s.count("background:rgba(247,248,250,0.25)"),
        "old header scrolled": s.count("rgba(247,248,250,0.45)"),
        "old timer sticky": s.count("justify-content:center;position:sticky;top:0;z-index:1000"),
        "pin bars": s.count("function pinBars()"),
        "resize observer": s.count("new ResizeObserver(pinBars)"),
        "hero shade light": s.count("rgba(29,78,216,.52) 0%"),
        "hero em white": s.count(".hero-full h1 em{font-style:italic;color:#fff"),
        "hero meta white": s.count(".hero-full .hero-meta{color:#fff"),
        "hero meta icons white": s.count(".hero-full .hero-meta svg{color:#fff}"),
        "hero cap white": s.count(".hero-cap b{color:#fff}"),
        "old hero shade": s.count("rgba(29,78,216,.93) 0%"),
    }
    if checks["svc-card buttons"] != 18:
        problems.append("svc-card count %d, expected 18" % checks["svc-card buttons"])
    if checks["building day photo uses"] != 3:
        problems.append("building day photo used %d times, expected 3 "
                        "(hero slide 1, carousel, gallery slide 1)"
                        % checks["building day photo uses"])
    if checks["interior photo uses"] != 6:
        problems.append("interior photo used %d times, expected 6 "
                        "(hero slide 2, story image, gallery slide 2, OPD first photo: PH map + home grid + services grid)"
                        % checks["interior photo uses"])
    if checks["front-cars photo uses"] != 4:
        problems.append("front-cars photo used %d times, expected 4 "
                        "(hero slide 3, teaser image, contact find-panel, gallery slide 3)"
                        % checks["front-cars photo uses"])
    for key in ("gen maternity", "gen emergency", "gen surgery",
                "gen paeds"):
        if checks[key + " uses"] != 3:
            problems.append("%s used %d times, expected 3 (PH map + home grid + services grid)"
                            % (key, checks[key + " uses"]))
    # Pharmacy is service 7, so it is not in the 6-card home grid.
    if checks["gen pharmacy uses"] != 2:
        problems.append("gen pharmacy used %d times, expected 2 (PH map + services grid)"
                        % checks["gen pharmacy uses"])
    if checks["gen lab uses"] != 4:
        problems.append("gen lab used %d times, expected 4 "
                        "(PH map + home grid + services grid + diagnostics image)"
                        % checks["gen lab uses"])
    if checks["imaging1 uses"] != 2:
        problems.append("imaging1 used %d times, expected 2 "
                        "(PH map + diagnostics image)"
                        % checks["imaging1 uses"])
    # The seven real Google Maps photos from the user's zip (2026-11-22):
    # each appears in the PH map and in one gallery slide. The three OPD
    # ones are ALSO listed in the OPD service photos — but that list holds
    # the photo key, not the data URI, so it adds no URI occurrence.
    for key, expected, where in (
            ("real waiting", 2, "PH map + gallery slide"),
            ("real waiting-people", 2, "PH map + gallery slide"),
            ("real consulting", 2, "PH map + gallery slide"),
            ("real lounge", 2, "PH map + gallery slide"),
            ("real night", 2, "PH map + gallery slide"),
            ("real van", 2, "PH map + gallery slide"),
            ("real street", 2, "PH map + gallery slide")):
        if checks[key + " uses"] != expected:
            problems.append("%s used %d times, expected %d (%s)"
                            % (key, checks[key + " uses"], expected, where))
    if len(SLIDES) != 10:
        problems.append("gallery slides %d, expected 10" % len(SLIDES))
    opd = next(svc for svc in SERVICES
               if svc["name"] == "Outpatient Consultation")
    for key in ("westend-real-waiting", "westend-real-waiting-people",
                "westend-real-consulting"):
        if key not in opd["photos"]:
            problems.append("OPD photos missing %s" % key)
    if checks["logo svg uses"] != 4:
        problems.append("logo used %d times, expected 4 "
                        "(header brand-mark + footer brand-mark + chat head-logo + chat fab)"
                        % checks["logo svg uses"])
    # The only SVG data URIs should be the logo (4 uses). Any more means
    # the safety net replaced a Habana photo with a placeholder.
    if checks["svg data URIs total"] != 4:
        problems.append("svg data URIs: %d, expected 4 (logo only — no placeholders)"
                        % checks["svg data URIs total"])
    if checks["our core values"] != 1:
        problems.append("core values heading found %d times, expected 1"
                        % checks["our core values"])
    if checks["old values heading"] != 0:
        problems.append("old values heading still present (%d)"
                        % checks["old values heading"])
    if checks["our mission"] != 1 or checks["our vision"] != 1:
        problems.append("mission/vision found %d/%d times, expected 1/1"
                        % (checks["our mission"], checks["our vision"]))
    if checks["mission grid"] != 1:
        problems.append("mission grid found %d times, expected 1"
                        % checks["mission grid"])
    if checks["pop-in keyframes"] != 1:
        problems.append("pop-in keyframes found %d times, expected 1"
                        % checks["pop-in keyframes"])
    if checks["pop-in script"] != 1:
        problems.append("pop-in script found %d times, expected 1"
                        % checks["pop-in script"])
    if checks["patient reviews section"] != 3:
        problems.append("patient reviews section found %d times, expected 3 "
                        "(home, about, contact)"
                        % checks["patient reviews section"])
    if checks["sample reviews note"] != 3:
        problems.append("sample reviews note found %d times, expected 3 "
                        "(home, about, contact)"
                        % checks["sample reviews note"])
    if checks["review cards"] != 9:
        problems.append("review cards %d, expected 9" % checks["review cards"])
    if s.count('class="contact-reviews"') != 1:
        problems.append("contact reviews block found %d times, expected 1"
                        % s.count('class="contact-reviews"'))
    aside_start = s.find('<aside class="panel">')
    if aside_start < 0 or s.find("Kofi M.", aside_start) < 0:
        problems.append("Kofi review not found inside the contact aside")
    if checks["chat fab text"] != 1:
        problems.append("chat fab text found %d times, expected 1"
                        % checks["chat fab text"])
    if checks["chat fab script"] != 1:
        problems.append("chat fab script found %d times, expected 1"
                        % checks["chat fab script"])
    if checks["chat fab expanded rule"] != 2:
        problems.append("chat fab expanded rule found %d times, expected 2"
                        % checks["chat fab expanded rule"])
    if checks["chat fab starts expanded"] != 1:
        problems.append("chat fab starts-expanded found %d times, expected 1"
                        % checks["chat fab starts expanded"])
    if checks["chat bubble icons"] != 3:
        problems.append("chat bubble icons found %d times, expected 3 "
                        "(WhatsApp links only — the fab's bubble icon must "
                        "be gone)" % checks["chat bubble icons"])
    if checks["booking date field"] != 1:
        problems.append("booking date field found %d times, expected 1"
                        % checks["booking date field"])
    if checks["booking time field"] != 1:
        problems.append("booking time field found %d times, expected 1"
                        % checks["booking time field"])
    if checks["booking date in message"] != 1:
        problems.append("booking date missing from WhatsApp message")
    if checks["booking time in message"] != 1:
        problems.append("booking time missing from WhatsApp message")
    if checks["booking datetime script"] != 1:
        problems.append("booking date/time script found %d times, expected 1"
                        % checks["booking datetime script"])
    if checks["css overrides"] != 1:
        problems.append("css overrides found %d times, expected 1"
                        % checks["css overrides"])
    if checks["live map iframe"] != 1:
        problems.append("live map iframe found %d times, expected 1"
                        % checks["live map iframe"])
    if checks["review forms"] != 1:
        problems.append("review forms found %d times, expected 1 (contact only)"
                        % checks["review forms"])
    if checks["review form script"] != 1:
        problems.append("review form script found %d times, expected 1"
                        % checks["review form script"])
    if checks["emergency red"] != 1:
        problems.append("emergency red #dc2626 found %d times, expected 1 "
                        "(A&E card border only)"
                        % checks["emergency red"])
    if checks["gallery counter"] != 1:
        problems.append("gallery counter '1 / 10' found %d times, expected 1"
                        % checks["gallery counter"])
    if s.count("1 / 3 · Our hospital") != 0:
        problems.append("stale gallery counter '1 / 3' still present")
    if checks["btn accent white"] != 1:
        problems.append("accent-button white text rule found %d times, expected 1"
                        % checks["btn accent white"])
    if checks["dark card numbers white"] != 1:
        problems.append("dark call-card number rule found %d times, expected 1"
                        % checks["dark card numbers white"])
    if checks["footer hover light"] != 1:
        problems.append("footer hover light-blue rule found %d times, expected 1"
                        % checks["footer hover light"])
    if checks["hero shade light"] != 1:
        problems.append("light hero shade found %d times, expected 1"
                        % checks["hero shade light"])
    if checks["hero em white"] != 1:
        problems.append("white hero headline em rule found %d times, expected 1"
                        % checks["hero em white"])
    if checks["hero meta white"] != 1:
        problems.append("white hero meta rule found %d times, expected 1"
                        % checks["hero meta white"])
    if checks["hero meta icons white"] != 1:
        problems.append("white hero meta icons rule found %d times, expected 1"
                        % checks["hero meta icons white"])
    if checks["hero cap white"] != 1:
        problems.append("white hero caption number rule found %d times, expected 1"
                        % checks["hero cap white"])
    if checks["old hero shade"] != 0:
        problems.append("old opaque hero shade (.93 alpha) still present")
    if checks["header fade script"] != 1:
        problems.append("header fade script found %d times, expected 1"
                        % checks["header fade script"])
    if checks["timer fixed"] != 1:
        problems.append("fixed timer rule found %d times, expected 1"
                        % checks["timer fixed"])
    if checks["header fixed"] != 1:
        problems.append("fixed header rule found %d times, expected 1"
                        % checks["header fixed"])
    if checks["header scrolled quarter"] != 1:
        problems.append("quarter-white scrolled header found %d times, expected 1"
                        % checks["header scrolled quarter"])
    if checks["old header scrolled"] != 0:
        problems.append("old 0.45 scrolled header still present")
    if checks["old timer sticky"] != 0:
        problems.append("old sticky timer rule still present")
    if checks["pin bars"] != 1:
        problems.append("pinBars function found %d times, expected 1"
                        % checks["pin bars"])
    if checks["resize observer"] != 1:
        problems.append("ResizeObserver found %d times, expected 1"
                        % checks["resize observer"])
    for k in ("Outpatient Consultation", "Accidents & Emergency",
              "General Surgery & Theatre", "Maternity & Obstetrics",
              "Paediatrics", "Laboratory & Diagnostics", "Pharmacy",
              "ECG", "EPI (Immunisation)", "MCH (Maternal & Child Health)",
              "Family Planning", "NHIS Office"):
        if checks[k] < 3:
            problems.append("%s appears only %d times" % (k, checks[k]))
    if checks["West End Hospital"] < 15:
        problems.append("brand name appears only %d times"
                        % checks["West End Hospital"])
    if checks["024 546 0006"] < 6:
        problems.append("main phone appears only %d times" % checks["024 546 0006"])
    if checks["032 202 2590"] < 3:
        problems.append("landline 032 202 2590 appears only %d times, expected 3 "
                        "(contact Call card, emergency banner, chat panel)"
                        % checks["032 202 2590"])
    if checks["Dr Kwakye-Maafo Avenue"] < 2:
        problems.append("address appears only %d times"
                        % checks["Dr Kwakye-Maafo Avenue"])
    if checks["6CRWM8GX+H9"] < 1:
        problems.append("plus code 6CRWM8GX+H9 not found")
    if checks["P.O. Box KS 4368"] < 2:
        problems.append("P.O. Box KS 4368 appears only %d times, expected 2 "
                        "(find-panel, map footer)"
                        % checks["P.O. Box KS 4368"])
    if checks["1978"] < 3:
        problems.append("founded 1978 appears only %d times"
                        % checks["1978"])
    if checks["40 beds"] < 1:
        problems.append("'40 beds' not found")
    if checks["Mercy Golightly"] < 3:
        problems.append("Mercy Golightly appears only %d times"
                        % checks["Mercy Golightly"])
    if checks["Kwakye-Maafo"] < 5:
        problems.append("Kwakye-Maafo appears only %d times"
                        % checks["Kwakye-Maafo"])
    if checks["Visiting hours"] < 2:
        problems.append("visiting hours appear only %d times, expected 2 "
                        "(morning + evening rows)"
                        % checks["Visiting hours"])
    if checks["NHIS"] < 5:
        problems.append("NHIS appears only %d times"
                        % checks["NHIS"])
    if checks["preview timer bar"] != 1:
        problems.append("preview timer bar found %d times, expected 1"
                        % checks["preview timer bar"])
    if checks["preview timer script"] != 1:
        problems.append("preview timer script found %d times, expected 1"
                        % checks["preview timer script"])
    return problems, checks


def js_check(s):

    """Syntax-check every inline <script> block with node."""
    blocks = re.findall(r"<script>(.*?)</script>", s, re.DOTALL)
    if not blocks:
        return "no <script> block found"
    tmp = Path("/tmp/we-demo-check.js")
    import subprocess
    for i, code in enumerate(blocks):
        tmp.write_text(code, encoding="utf-8")
        r = subprocess.run(["node", "--check", str(tmp)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            return "node --check failed on script block %d:\n%s" % (i, r.stderr)
    return None


def main():
    src = SRC.read_text(encoding="utf-8")
    out = transform(src)
    problems, checks = verify(out)
    if problems:
        print("VERIFY FAILED:")
        for p in problems:
            print(" -", p)
        raise SystemExit(1)
    err = js_check(out)
    if err:
        print("JS CHECK FAILED:")
        print(err)
        raise SystemExit(1)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(out, encoding="utf-8")
    print("OK — wrote", DST, "(%d bytes)" % len(out.encode("utf-8")))
    for k, v in checks.items():
        print("  %-32s %d" % (k, v))


if __name__ == "__main__":
    main()
