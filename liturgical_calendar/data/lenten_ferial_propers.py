"""
Introits and Collects for the Historic Lenten Weekday (Ferial) Masses.

Companion to lenten_ferial.py (the readings): the proper introit and collect
of each Lenten ferial Mass, Ash Wednesday through Maundy Thursday.  Good
Friday has neither — the Mass of the Presanctified opens directly with the
lessons (see GOOD_FRIDAY_NOTE).

PROVENANCE — these are HISTORIC WESTERN (Roman) texts
------------------------------------------------------
The ferial *readings* in lenten_ferial.py are demonstrably part of the
lectionary the Lutherans inherited.  The ferial *introits and collects* are
not: no classic Lutheran service book in English (Common Service Book 1917,
The Lutheran Hymnal 1941) provides propers for the Lenten weekdays — both
cover Sundays and feasts only — and The Lutheran Missal project (modern) has
not yet published its ferial minor propers ("We do not yet have the Collects
and Minor Propers entirely sorted and prepared for distribution" — its
lectionary FAQ, retrieved 2026-07-02).  What is given here is therefore the
historic Western (Gregorian/Tridentine) provision, presented for reference
alongside the readings with that label — the same footing as the ``hist``
("the most Roman") origin tag used for readings.

SOURCE TEXT (public domain)
---------------------------
F. C. Husenbeth, *The Missal for the Use of the Laity* (London, 1853) —
Latin/English parallel; English of the Douay register.  Public domain
(archive.org: missal_for_use_of_laity_1853-f_c_husenbeth, PD Mark 1.0).
Texts transcribed from the scan's OCR and corrected against it by hand;
collect endings kept as printed ("Through our Lord, &c.").

Two exceptions, both noted per entry:
- Friday of Judica (Passion Week): Husenbeth prints the feast of the Seven
  Dolours for that day and gives the feria only a commemoration collect
  (*Cordibus*).  Its introit — shared with the Saturday following — is
  transcribed from Husenbeth's Saturday printing; the sharing is confirmed
  by the 1861 witness ("The Introit … as on Friday").
- Saturday after Ash Wednesday repeats Friday's introit (both witnesses).

CROSS-VERIFICATION (two independent witnesses)
----------------------------------------------
Every day's introit incipit and collect identity was verified against
*The Roman Missal translated into the English Language for the Use of the
Laity* (Philadelphia: Cummiskey, 1861; archive.org: romanmissaltran00churgoog,
public domain) — an independent translation of the same missal.  For
Wednesday in Holy Week, where the 1861 scan's pages are disordered, the
second witness is *The Anglican Missal* (London, 1921; archive.org:
anglicanmissal00churuoft): "WEDNESDAY BEFORE EASTER … INTROIT. In Nomine
Jesu. Phil. 2".  All 38 days agree across witnesses.

CONVENTIONS
-----------
- introit["name"]  = the traditional Latin incipit.
- introit["ref"]   = source of antiphon and psalm-verse.  Husenbeth prints
  Vulgate psalm numbers; refs below are converted to the KJV/Hebrew
  numbering used throughout this app (e.g. Husenbeth "Ps. cxxii" → Psalm 123).
- introit["text"]  = antiphon, then "Psalm." and the appointed verse, as in
  one_year_propers.py; the invariable Gloria Patri is omitted.  (In
  Passiontide — Judica week and Holy Week — the rite omits the Gloria Patri
  and repeats the antiphon instead.)
- "collect" = the day's principal collect (the "Prayer" of the Mass).  On
  days with several collects (Ember Days, the two mid-Lent scrutiny masses)
  the first — the Collect of the day — is given, with a note.
"""

TRADITION = "western"           # Historic Western (Roman) — NOT in Lutheran service books
TRACK = "lenten_ferial_propers"

PROVENANCE_LABEL = (
    "Historic Western (Roman) propers — not found in Lutheran service books; "
    "given for reference alongside the historic weekday readings."
)

GOOD_FRIDAY_NOTE = (
    "Good Friday has no introit and no Collect of the Day: the Mass of the "
    "Presanctified opens in silence with the lessons, and its prayers are the "
    "Solemn Collects said after the Passion."
)

SOURCE_CITATION = (
    "Introits and collects: F. C. Husenbeth, The Missal for the Use of the Laity "
    "(London, 1853), public domain; cross-verified against The Roman Missal … for "
    "the Use of the Laity (Philadelphia, 1861) and The Anglican Missal (1921)."
)


def _e(name, ref, text, collect_name, collect, note=None, day=None):
    entry = {
        "introit": {"name": name, "ref": ref, "text": text},
        "collect_name": collect_name,
        "collect": collect,
        "source": (
            "Husenbeth, The Missal for the Use of the Laity (London, 1853)"
            + (f" — {day}" if day else "")
        ),
    }
    if note:
        entry["note"] = note
    return entry


FERIAL_PROPERS = {

    # --- Ash Wednesday and the first days ----------------------------------
    "fer_ash_wed": _e(
        "Misereris omnium", "Wisdom 11; Psalm 57",
        "Thou hast mercy upon all, O Lord, and hatest none of the things which thou hast "
        "made, winking at the sins of men for the sake of repentance, and sparing them; "
        "for thou art the Lord our God. Psalm. Have mercy on me, O God, have mercy on me; "
        "for my soul trusteth in thee.",
        "Praesta Domine",
        "Grant to thy faithful, O Lord, that they may begin the venerable solemnities of "
        "fasting with becoming piety, and perform them with secure devotion. Through our "
        "Lord, &c.",
        day="Ash Wednesday"),

    "fer_ash_thu": _e(
        "Dum clamarem", "Psalm 55",
        "When I cried to the Lord, he heard my voice from them that draw near to me; and "
        "he humbled them, who is before all ages, and remains for ever: cast thy care upon "
        "the Lord, and he shall sustain thee. Psalm. Hear, O God, my prayer, and despise "
        "not my supplication; be attentive to me and hear me.",
        "Deus qui culpa",
        "O God, who by sin art offended, and by penance pacified, mercifully regard the "
        "prayers of thy people making supplication to thee; and turn away the scourges of "
        "thy anger, which we deserve for our sins. Through our Lord, &c.",
        day="Thursday after Ash Wednesday"),

    "fer_ash_fri": _e(
        "Audivit Dominus", "Psalm 30",
        "The Lord hath heard, and hath had mercy on me: the Lord became my helper. "
        "Psalm. I will extol thee, O Lord, for thou hast upheld me; and hast not made my "
        "enemies to rejoice over me.",
        "Inchoata jejunia",
        "Regard the fast we have begun, we beseech thee, O Lord, with kind favour; that "
        "the observance we exhibit corporally, we may be able also to exercise with "
        "sincere minds. Through our Lord, &c.",
        day="Friday after Ash Wednesday"),

    "fer_ash_sat": _e(
        "Audivit Dominus", "Psalm 30",
        "The Lord hath heard, and hath had mercy on me: the Lord became my helper. "
        "Psalm. I will extol thee, O Lord, for thou hast upheld me; and hast not made my "
        "enemies to rejoice over me.",
        "Adesto",
        "Be attentive, O Lord, to our supplications: and grant that we may celebrate with "
        "devout homage this solemn fast, which is a wholesome institution to heal both our "
        "souls and bodies. Through, &c.",
        note="The introit repeats Friday's (so in the missal).",
        day="Saturday after Ash Wednesday"),

    # --- Invocavit — First Week ---------------------------------------------
    "fer_invocavit_mon": _e(
        "Sicut oculi", "Psalm 123",
        "As the eyes of servants are on the hands of their masters, so are our eyes unto "
        "the Lord our God, until he have mercy on us: have mercy on us, O Lord, have mercy "
        "on us. Psalm. To thee have I lifted up my eyes: who dwellest in heaven.",
        "Converte nos",
        "Convert us, O God, our salvation: and that the fast of Lent may benefit us, "
        "instruct our minds with heavenly discipline. Through, &c.",
        day="Monday, First Week"),

    "fer_invocavit_tue": _e(
        "Domine refugium", "Psalm 90",
        "Lord, thou hast been our refuge from generation to generation: from eternity and "
        "to eternity thou art. Psalm. Before the mountains were made, or the earth and the "
        "world was formed: from eternity and to eternity thou art God.",
        "Respice Domine",
        "Look down upon thy family, O Lord, and grant that our minds may shine in thy "
        "sight with the desire of thee, which are afflicted by the mortification of the "
        "flesh. Through our Lord, &c.",
        day="Tuesday, First Week"),

    "fer_ember_wed": _e(
        "Reminiscere", "Psalm 25",
        "Remember, O Lord, thy bowels of compassion, and thy mercies that are from the "
        "beginning of the world; lest at any time our enemies rule over us: deliver us, "
        "O God of Israel, from all our tribulations. Psalm. To thee, O Lord, have I lifted "
        "up my soul: in thee, O my God, I put my trust; let me not be ashamed.",
        "Preces nostras",
        "Mercifully hear our prayers, we beseech thee, O Lord; and against all our "
        "adversaries extend the right hand of thy Majesty. Through our Lord, &c.",
        note="An Ember Day: a second collect (Devotionem) follows the first lesson.",
        day="Ember Wednesday in Lent"),

    "fer_invocavit_thu": _e(
        "Confessio et pulchritudo", "Psalm 96",
        "Praise and beauty are before him: holiness and majesty in his sanctuary. "
        "Psalm. Sing ye to the Lord a new canticle: sing to the Lord all the earth.",
        "Devotionem",
        "Favourably look down, O Lord, upon the devotion of thy people, that we, who are "
        "afflicted in body by abstinence, may be refreshed in mind by the fruit of good "
        "works. Through our Lord, &c.",
        day="Thursday, First Week"),

    "fer_ember_fri": _e(
        "De necessitatibus", "Psalm 25",
        "Deliver me from my necessities, O Lord: see my abjection and my labour, and "
        "forgive me all my sins. Psalm. To thee, O Lord, have I lifted up my soul: in "
        "thee, O my God, I put my trust, let me not be ashamed.",
        "Esto Domine",
        "Be merciful, O Lord, to thy people; and as thou makest them devout to thee, "
        "mercifully refresh them with kind assistance. Through our Lord, &c.",
        day="Ember Friday in Lent"),

    "fer_ember_sat": _e(
        "Intret oratio mea", "Psalm 88",
        "Let my prayer come in before thee: incline thy ear to my petition, O Lord. "
        "Psalm. O Lord the God of my salvation: I have cried in the day, and in the night "
        "before thee.",
        "Populum tuum",
        "Favourably look down upon thy people, we beseech thee, O Lord, and mercifully "
        "turn away from them the scourges of thy anger. Through, &c.",
        note="Ember Saturday: each of the day's five lessons has its own collect; the "
             "first — the Collect of the day — is given here.",
        day="Saturday, Ember Day"),

    # --- Reminiscere — Second Week ------------------------------------------
    "fer_reminiscere_mon": _e(
        "Redime me", "Psalm 26",
        "Redeem me, O Lord, and have mercy on me; for my foot hath stood in the direct "
        "way: in the churches I will bless the Lord. Psalm. Judge me, O Lord, for I have "
        "walked in my innocence; and hoping in the Lord, I shall not be weakened.",
        "Praesta quaesumus",
        "Grant, we beseech thee, O Almighty God, that thy family, who afflicting their "
        "flesh abstain from food, by following justice may fast from sin. Through our "
        "Lord, &c.",
        day="Monday, Second Week"),

    "fer_reminiscere_tue": _e(
        "Tibi dixit cor meum", "Psalm 27",
        "My heart hath said to thee, I have sought thy face; thy face, O Lord, will I "
        "seek: turn not away thy face from me. Psalm. The Lord is my light and my "
        "salvation: whom shall I fear?",
        "Perfice",
        "Perfect, we beseech thee, O Lord, in thy mercy, the help of this holy observance "
        "within us; that what by thy instruction we know we are to do, by thy grace we "
        "may be enabled to accomplish. Through our Lord, &c.",
        day="Tuesday, Second Week"),

    "fer_reminiscere_wed": _e(
        "Ne derelinquas me", "Psalm 38",
        "Forsake me not, O Lord my God, do not thou depart from me; attend unto my help, "
        "O Lord, the power of my salvation. Psalm. Rebuke me not, O Lord, in thy "
        "indignation: nor chastise me in thy wrath.",
        "Populum tuum",
        "Mercifully regard thy people, O Lord, we beseech thee, and grant that we, whom "
        "thou commandest to abstain from carnal food, may also cease from hurtful vices. "
        "Through our Lord, &c.",
        day="Wednesday, Second Week"),

    "fer_reminiscere_thu": _e(
        "Deus in adjutorium", "Psalm 70",
        "O God, come to my assistance, O Lord, make haste to help me: let my enemies be "
        "confounded and ashamed that seek my soul. Psalm. Let them be turned backward and "
        "blush for shame, that desire evils to me.",
        "Praesta nobis",
        "Grant us, we beseech thee, O Lord, the help of thy grace: that being duly intent "
        "on fasts and prayers, we may be delivered from enemies of mind and body. Through "
        "our Lord, &c.",
        day="Thursday, Second Week"),

    "fer_reminiscere_fri": _e(
        "Ego autem cum justitia", "Psalm 17",
        "But I will appear before thy sight in justice: I shall be satisfied when thy "
        "glory shall be made manifest. Psalm. Hear, O Lord, my justice: attend to my "
        "supplication.",
        "Da quaesumus",
        "Grant, we beseech thee, Almighty God, that purified by a holy fast, we may "
        "arrive by thy grace with sincere minds at the festivals to come. Through our "
        "Lord, &c.",
        day="Friday, Second Week"),

    "fer_reminiscere_sat": _e(
        "Lex Domini", "Psalm 19",
        "The law of the Lord is unspotted, converting souls; the testimony of the Lord is "
        "faithful, giving wisdom to little ones. Psalm. The heavens shew forth the glory "
        "of God; and the firmament declareth the work of his hands.",
        "Da quaesumus",
        "Grant, we beseech thee, O Lord, a salutary effect to our fasts: that the "
        "chastisement of the flesh, which we have taken upon us, may promote the vigour "
        "of our souls. Through, &c.",
        day="Saturday, Second Week"),

    # --- Oculi — Third Week --------------------------------------------------
    "fer_oculi_mon": _e(
        "In Deo laudabo", "Psalm 56",
        "In God I will praise the word, in the Lord I will praise his speech: in God I "
        "will trust, I will not fear what man can do against me. Psalm. Have mercy on me, "
        "O God, for man hath trodden me under foot: all the day long he hath afflicted "
        "me, fighting against me.",
        "Cordibus nostris",
        "Pour forth in thy mercy, we beseech thee, O Lord, thy grace into our hearts, "
        "that as we abstain from flesh, we may also restrain our senses from hurtful "
        "excesses. Through, &c.",
        day="Monday, Third Week"),

    "fer_oculi_tue": _e(
        "Ego clamavi", "Psalm 17",
        "I have cried, for thou, O God, hast heard me: O incline thine ear and hear my "
        "words: keep me, O Lord, as the apple of thy eye: protect me under the shadow of "
        "thy wings. Psalm. Hear, O Lord, my justice: attend to my prayer.",
        "Exaudi nos",
        "Graciously hear us, O Almighty and merciful God; and favourably grant to us the "
        "gifts of wholesome self-denial. Through, &c.",
        day="Tuesday, Third Week"),

    "fer_oculi_wed": _e(
        "Ego autem in Domino sperabo", "Psalm 31",
        "But I will hope in the Lord: I will be glad, and rejoice in thy mercy; for thou "
        "hast regarded my humility. Psalm. In thee, O Lord, have I hoped, let me never be "
        "confounded: deliver me in thy justice, and rescue me.",
        "Praesta nobis",
        "Grant us, we beseech thee, O Lord, that instructed by wholesome fasting, and "
        "abstaining from dangerous vices, we may more easily obtain thy favour. Through "
        "our Lord, &c.",
        day="Wednesday, Third Week"),

    "fer_oculi_thu": _e(
        "Salus populi", "Liturgical text; Psalm 78",
        "I am the salvation of the people, saith the Lord: from whatever tribulation they "
        "shall cry to me, I will hear them; and I will be their Lord for ever. "
        "Psalm. Attend, O my people, to my law; incline your ear to the words of my mouth.",
        "Magnificet",
        "May the blessed solemnity of thy saints Cosmas and Damian magnify thee, O Lord: "
        "by which thou hast both granted eternal glory to them, and assistance to us in "
        "thy ineffable providence. Through our Lord, &c.",
        note="The collect names Sts. Cosmas and Damian because the day's ancient Roman "
             "station was at their basilica — a fixture of the old missal, kept here as "
             "printed.",
        day="Thursday, Third Week"),

    "fer_oculi_fri": _e(
        "Fac mecum", "Psalm 86",
        "Shew me, O Lord, a token for good; that they who hate me may see, and be "
        "confounded: because thou, O Lord, hast helped me, and comforted me. Psalm. Bow "
        "down thy ear, O Lord, and hear me: for I am needy and poor.",
        "Jejunia",
        "Look down on our fasts, we beseech thee, O Lord, with merciful favour; that as "
        "we abstain from food in body, so we may fast from vice in mind. Through our "
        "Lord, &c.",
        day="Friday, Third Week"),

    "fer_oculi_sat": _e(
        "Verba mea", "Psalm 5",
        "Give ear, O Lord, to my words, understand my cry: hearken to the voice of my "
        "prayer, O my King and my God. Psalm. For to thee will I pray: O Lord, in the "
        "morning thou shalt hear my voice.",
        "Praesta",
        "Grant we beseech thee, O Almighty God, that they who, afflicting their flesh, "
        "abstain from food, may, following justice, fast from sin. Through our Lord, &c.",
        note="The missal appoints the same collect as on Monday of the Second Week.",
        day="Saturday, Third Week"),

    # --- Laetare — Fourth Week -----------------------------------------------
    "fer_laetare_mon": _e(
        "Deus in nomine tuo", "Psalm 54",
        "Save me, O God, by thy name, and in thy strength deliver me: O God, hear my "
        "prayer; give ear to the words of my mouth. Psalm. For strangers have risen up "
        "against me: and the mighty have sought after my soul.",
        "Praesta",
        "Grant, we beseech thee, Almighty God, that keeping with yearly devotion these "
        "sacred observances, we may please thee both in body and mind. Through, &c.",
        day="Monday, Fourth Week"),

    "fer_laetare_tue": _e(
        "Exaudi Deus", "Psalm 55",
        "Hear, O God, my prayer, and despise not my supplication: be attentive to me, and "
        "hear me. Psalm. I am grieved in my exercise; and am troubled at the voice of the "
        "enemy, and at the tribulation of the sinner.",
        "Sacrae nobis",
        "We beseech thee, O Lord, that the fasts of this holy observance may procure us "
        "an increase of piety in our lives, and the continual help of thy mercy. Through "
        "our Lord, &c.",
        day="Tuesday, Fourth Week"),

    "fer_laetare_wed": _e(
        "Cum sanctificatus fuero", "Ezekiel 36; Psalm 34",
        "When I shall be sanctified in you, I will gather you from every land: and I will "
        "pour upon you clean water, and you shall be cleansed from all your filthiness: "
        "and I will give you a new spirit. Psalm. I will bless the Lord at all times: his "
        "praise shall be ever in my mouth.",
        "Deus qui et justis",
        "O God, who grantest to the just the reward of their merits, and to sinners "
        "pardon by means of fasting, have mercy on thy supplicants, that the confession "
        "of our guilt may enable us to receive the forgiveness of our sins. Through, &c.",
        note="The great mid-Lent scrutiny Mass: the collect is preceded by Oremus — "
             "Flectamus genua, and a second collect follows the first lesson.",
        day="Wednesday, Fourth Week"),

    "fer_laetare_thu": _e(
        "Laetetur cor", "Psalm 105",
        "Let the heart of them rejoice that seek the Lord: seek the Lord, and be "
        "strengthened: seek his face evermore. Psalm. Give glory to the Lord, and call "
        "upon his name; declare his deeds among the gentiles.",
        "Praesta quaesumus",
        "Grant we beseech thee, Almighty God, that we who are chastised by the fasts we "
        "have undertaken, may rejoice with holy devotion; that our earthly affections "
        "being weakened, we may more easily apprehend heavenly things. Through our "
        "Lord, &c.",
        day="Thursday, Fourth Week"),

    "fer_laetare_fri": _e(
        "Meditatio cordis mei", "Psalm 19",
        "The meditation of my heart is always in thy sight: O Lord, my helper and my "
        "redeemer. Psalm. The heavens shew forth the glory of God; and the firmament "
        "declareth the work of his hands.",
        "Deus qui ineffabilibus",
        "O God, who renewest the world by unspeakable mysteries, grant, we beseech thee, "
        "that thy Church may profit by thy eternal institutions, and not be deprived of "
        "temporal assistance. Through, &c.",
        day="Friday, Fourth Week"),

    "fer_laetare_sat": _e(
        "Sitientes venite", "Isaiah 55; Psalm 78",
        "O you that thirst, come to the waters, saith the Lord; and you that have no "
        "money, come and drink with joy. Psalm. Attend, O my people, to my law: incline "
        "your ears to the words of my mouth.",
        "Fiat Domine",
        "May the affection of our devotion be made fruitful by thy grace, we beseech "
        "thee, O Lord, for then will the fasts we have undertaken become profitable to "
        "us, if they are pleasing to thy mercy. Through, &c.",
        day="Saturday, Fourth Week"),

    # --- Judica — Passion Week -----------------------------------------------
    "fer_judica_mon": _e(
        "Miserere mihi Domine", "Psalm 56",
        "Have mercy on me, O Lord, for man hath trodden me under foot: all the day long "
        "he hath afflicted me, fighting against me. Psalm. My enemies have trodden on me "
        "all the day long: for they are many that make war against me.",
        "Sanctifica",
        "Sanctify our fasts, we beseech thee, O Lord, and mercifully grant us the pardon "
        "of all our faults. Through our Lord, &c.",
        day="Monday, Passion Week"),

    "fer_judica_tue": _e(
        "Exspecta Dominum", "Psalm 27",
        "Expect the Lord, do manfully: and let thy heart take courage, and wait thou for "
        "the Lord. Psalm. The Lord is my light and my salvation; whom shall I fear?",
        "Nostra tibi",
        "May our fasts be acceptable to thee, O Lord; and by expiating our sins, may they "
        "make us worthy of thy grace, and conduct us to eternal remedies. Through our "
        "Lord, &c.",
        day="Tuesday, Passion Week"),

    "fer_judica_wed": _e(
        "Liberator meus", "Psalm 18",
        "My deliverer from the angry nations: thou wilt lift me up above them that rise "
        "up against me: from the unjust man thou wilt deliver me, O Lord. Psalm. I will "
        "love thee, O Lord, my strength: the Lord is my firmament, and my refuge, and my "
        "deliverer.",
        "Sanctificato",
        "Sanctify this fast, O God; and mercifully enlighten the hearts of thy faithful; "
        "and to those to whom thou grantest the grace of devotion, mercifully grant when "
        "they pray to thee, a favourable hearing. Through our Lord, &c.",
        day="Wednesday, Passion Week"),

    "fer_judica_thu": _e(
        "Omnia quae fecisti", "Daniel 3; Psalm 119",
        "All that thou hast done to us, O Lord, thou hast done in true judgment: because "
        "we have sinned against thee, and have not obeyed thy commandments: but give "
        "glory to thy name, and deal with us according to the multitude of thy mercy. "
        "Psalm. Blessed are the undefiled in the way: who walk in the law of the Lord.",
        "Praesta quaesumus",
        "Grant, we beseech thee, Almighty God, that the dignity of human nature, wounded "
        "by excess, may be reformed by attention to medicinal temperance. Through, &c.",
        day="Thursday, Passion Week"),

    "fer_judica_fri": _e(
        "Miserere mihi Domine quoniam tribulor", "Psalm 31",
        "Have mercy on me, O Lord, for I am afflicted: deliver me out of the hands of my "
        "enemies, and from them that persecute me: let me not be confounded, O Lord, for "
        "I have called upon thee. Psalm. In thee, O Lord, have I hoped, let me never be "
        "confounded: deliver me in thy justice.",
        "Cordibus",
        "Mercifully infuse thy grace into our hearts, we beseech thee, O Lord; that "
        "refraining from sin by voluntary chastisement, we may be rather afflicted in "
        "time, than condemned to punishment for eternity. Through our Lord, &c.",
        note="In the old missal this Friday was kept as the feast of the Seven Dolours, "
             "the feria being commemorated by this collect; the introit — shared with "
             "Saturday — is transcribed from the Saturday printing.",
        day="Friday, Passion Week (commemoration of the feria)"),

    "fer_judica_sat": _e(
        "Miserere mihi Domine quoniam tribulor", "Psalm 31",
        "Have mercy on me, O Lord, for I am afflicted: deliver me out of the hands of my "
        "enemies, and from them that persecute me: let me not be confounded, O Lord, for "
        "I have called upon thee. Psalm. In thee, O Lord, have I hoped, let me never be "
        "confounded: deliver me in thy justice.",
        "Proficiat",
        "We beseech thee, O Lord, may the people prosper who are devoted to thee by the "
        "affection of pious devotion: that, instructed by holy actions, they may be "
        "blessed with better gifts, as they are made more pleasing in the sight of thy "
        "majesty. Through our Lord, &c.",
        note="The introit repeats Friday's (so in the missal).",
        day="Saturday, Passion Week"),

    # --- Holy Week ------------------------------------------------------------
    "fer_holyweek_mon": _e(
        "Judica Domine", "Psalm 35",
        "Judge thou, O Lord, them that wrong me; overthrow them that fight against me: "
        "take hold of arms and shield, and rise up to help me, O Lord, the strength of my "
        "salvation. Psalm. Bring out the sword, and shut up the way against those who "
        "persecute me: say to my soul, I am thy salvation.",
        "Da quaesumus",
        "Grant, we beseech thee, almighty God, that we who fail, through our infirmity, "
        "in so many adversities, may be relieved by the passion of thy Son making "
        "intercession for us. Who lives and reigns, &c.",
        day="Monday in Holy Week"),

    "fer_holyweek_tue": _e(
        "Nos autem gloriari", "Galatians 6; Psalm 67",
        "But it behoves us to glory in the cross of our Lord Jesus Christ: in whom is our "
        "salvation, life, and resurrection; by whom we are saved and delivered. "
        "Psalm. May God have mercy on us, and bless us: may he cause the light of his "
        "countenance to shine upon us, and may he have mercy on us.",
        "Omnipotens",
        "O Almighty and everlasting God, grant us so to celebrate the mysteries of our "
        "Lord's passion, that we may deserve to obtain pardon. Through the same Lord, &c.",
        day="Tuesday in Holy Week"),

    "fer_holyweek_wed": _e(
        "In nomine Jesu", "Philippians 2; Psalm 102",
        "In the name of Jesus let every knee bow, of things in heaven, on earth, and "
        "under the earth: for the Lord became obedient unto death, even the death of the "
        "cross: therefore the Lord Jesus Christ is in the glory of God the Father. "
        "Psalm. O Lord, hear my prayer; and let my cry come to thee.",
        "Praesta quaesumus",
        "Grant, we beseech thee, Almighty God, that we who are continually afflicted "
        "through our excesses, may be delivered by the passion of thy only begotten Son. "
        "Who lives, &c.",
        note="The collect is preceded by Oremus — Flectamus genua, and a second prayer "
             "follows the first lesson.",
        day="Wednesday in Holy Week"),

    "maundy_thursday_fer": _e(
        "Nos autem gloriari", "Galatians 6; Psalm 67",
        "But it behoves us to glory in the cross of our Lord Jesus Christ: in whom is our "
        "salvation, life, and resurrection; by whom we are saved and delivered. "
        "Psalm. May God have mercy on us, and bless us: may he cause the light of his "
        "countenance to shine upon us, and may he have mercy on us.",
        "Deus a quo",
        "O God, from whom Judas received the punishment of his guilt, and the good thief "
        "the reward of his confession; grant us the effect of thy mercy, that as our Lord "
        "Jesus Christ, in his passion, gave to each different retribution according to "
        "their deserts, so he would take from us our old errors, and grant us the grace "
        "of his resurrection. Who lives and reigns, &c.",
        day="Maundy Thursday"),

    # Good Friday intentionally absent — see GOOD_FRIDAY_NOTE.
}


def propers_for_slot(slot):
    """Return the ferial propers entry for a lenten_ferial slot, or None.

    Sundays and Good Friday return None: Sunday propers live in
    one_year_propers.py, and Good Friday has none (GOOD_FRIDAY_NOTE).
    """
    return FERIAL_PROPERS.get(slot)
