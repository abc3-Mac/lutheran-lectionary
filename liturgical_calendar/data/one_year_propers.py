"""
TLH 1941 Collects and Traditional Introit Names/References
for the Lutheran One-Year Lectionary.

Collect texts: from The Lutheran Hymnal (1941) / Common Service Book of the
Lutheran Church — the traditional KJV-era wording. Source: Common Service Book
of the Lutheran Church (same propers tradition as TLH 1941).

Introit names: Traditional Latin incipit names from the historic Western/Lutheran
liturgical tradition. Psalm references are the antiphon/psalm verses used in TLH.

NOTE on Christmas: The CSB/TLH provides three Christmas masses:
  - Early (Midnight/Nocturns): "Dominus Dixit" — Ps. 2, 93
  - Dawn ("Aurora"): "Lux Fulgebit" — Ps. 98 / Is. 9
  - Day: "In Excelso Throno" / "Puer Natus" — Ps. 93, 98

NOTE on Trinity 27/Last Sunday: Trinity 27 proper is used on the Last Sunday
after Trinity each year. Some years have fewer Sundays; Trinity 25-27 propers
rotate at the end of the year.
"""

ONE_YEAR_PROPERS = {

    # -----------------------------------------------------------------------
    # ADVENT
    # -----------------------------------------------------------------------
    "advent_1": {
        "collect": (
            "Stir up, we beseech Thee, Thy power, O Lord, and come; that by Thy protection "
            "we may be rescued from the threatening perils of our sins, and saved by Thy "
            "mighty deliverance; Who livest and reignest with the Father and the Holy Ghost, "
            "ever One God, world without end. Amen."
        ),
        "introit": {"name": "Ad Te Levavi", "ref": "Psalm 25:1–3, 5"},
    },
    "advent_2": {
        "collect": (
            "Stir up our hearts, O Lord, to make ready the way of Thine Only-begotten Son, "
            "so that by His coming we may be enabled to serve Thee with pure minds; through "
            "the same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and "
            "the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Populus Sion", "ref": "Isaiah 30:30; Psalm 80:1"},
    },
    "advent_3": {
        "collect": (
            "Lord, we beseech Thee, give ear to our prayers, and lighten the darkness of our "
            "hearts by Thy gracious visitation; Who livest and reignest with the Father and "
            "the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Gaudete", "ref": "Philippians 4:4–5; Psalm 85:1"},
    },
    "advent_4": {
        "collect": (
            "Stir up, O Lord, we beseech Thee, Thy power, and come, and with great might "
            "succor us, that by the help of Thy grace whatsoever is hindered by our sin may "
            "be speedily accomplished, through Thy mercy and satisfaction; Who livest and "
            "reignest with the Father and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Rorate Caeli", "ref": "Isaiah 45:8; Psalm 19:1"},
    },

    # -----------------------------------------------------------------------
    # CHRISTMAS
    # -----------------------------------------------------------------------
    "christmas_eve": {
        "collect": (
            "O God, Who hast made this most holy night to shine with the brightness of the "
            "true Light: Grant, we beseech Thee, that as we have known on earth the mysteries "
            "of that Light, we may also come to the fullness of His joys in heaven; Who "
            "liveth and reigneth with Thee and the Holy Ghost, ever One God, world without "
            "end. Amen."
        ),
        "introit": {"name": "Hodie Scietis", "ref": "Exodus 16:6–7; Psalm 96:1"},
    },
    "christmas_midnight": {
        "collect": (
            "O God, Who hast made this most holy night to shine with the brightness of the "
            "true Light: Grant, we beseech Thee, that as we have known on earth the mysteries "
            "of that Light, we may also come to the fullness of His joys in heaven; Who "
            "liveth and reigneth with Thee and the Holy Ghost, ever One God, world without "
            "end. Amen."
        ),
        "introit": {"name": "Dominus Dixit", "ref": "Psalm 2:7; Psalm 110:3"},
    },
    "christmas_dawn": {
        "collect": (
            "O God, Who hast made this most holy night to shine with the brightness of the "
            "true Light: Grant, we beseech Thee, that as we have known on earth the mysteries "
            "of that Light, we may also come to the fullness of His joys in heaven; Who "
            "liveth and reigneth with Thee and the Holy Ghost, ever One God, world without "
            "end. Amen."
        ),
        "introit": {"name": "Lux Fulgebit", "ref": "Isaiah 9:2, 6; Psalm 98:1"},
    },
    "christmas_day": {
        "collect": (
            "Grant, we beseech Thee, Almighty God, that the new Birth of Thine Only-begotten "
            "Son in the flesh may set us free who are held in the old bondage under the yoke "
            "of sin; through the same Jesus Christ, Thy Son, our Lord, Who liveth and "
            "reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Puer Natus Est", "ref": "Isaiah 9:6; Psalm 98:1"},
    },
    "christmas_sunday_1": {
        "collect": (
            "Almighty and Everlasting God, direct our actions according to Thy good pleasure, "
            "that in the Name of Thy beloved Son, we may be made to abound in good works; "
            "through the same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with "
            "Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Dum Medium Silentium", "ref": "Wisdom 18:14–15; Psalm 93:1"},
    },
    "christmas_sunday_2": {
        # If a second Sunday after Christmas occurs before Epiphany
        "collect": (
            "Almighty and Everlasting God, direct our actions according to Thy good pleasure, "
            "that in the Name of Thy beloved Son, we may be made to abound in good works; "
            "through the same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with "
            "Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Dum Medium Silentium", "ref": "Wisdom 18:14–15; Psalm 93:1"},
    },

    # -----------------------------------------------------------------------
    # EPIPHANY SEASON
    # -----------------------------------------------------------------------
    "new_years_eve": {
        # New Year's Eve (Dec 31) — typically uses the Circumcision/Name of Jesus propers
        "collect": (
            "O Lord God, Who, for our sakes, hast made Thy blessed Son our Saviour subject "
            "to the Law, and caused Him to endure the circumcision of the flesh: Grant us the "
            "true circumcision of the Spirit, that our hearts may be pure from all sinful "
            "desires and lusts; through the same Jesus Christ, Thy Son, our Lord, Who liveth "
            "and reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Nomen Iesu", "ref": "Philippians 2:10–11; Psalm 8:1"},
    },
    "new_years_day": {
        # Jan 1 — Circumcision and Name of Jesus
        "collect": (
            "O Lord God, Who, for our sakes, hast made Thy blessed Son our Saviour subject "
            "to the Law, and caused Him to endure the circumcision of the flesh: Grant us the "
            "true circumcision of the Spirit, that our hearts may be pure from all sinful "
            "desires and lusts; through the same Jesus Christ, Thy Son, our Lord, Who liveth "
            "and reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Nomen Iesu", "ref": "Philippians 2:10–11; Psalm 8:1"},
    },
    "epiphany": {
        "collect": (
            "O God, Who by the leading of a star didst manifest Thy Only-begotten Son to the "
            "Gentiles: Mercifully grant, that we, who know Thee now by faith, may after this "
            "life have the fruition of Thy glorious Godhead; through the same Jesus Christ, "
            "Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever "
            "One God, world without end. Amen."
        ),
        "introit": {"name": "Ecce Advenit", "ref": "Malachi 3:1; Psalm 72:1"},
    },
    "baptism_of_lord": {
        # First Sunday after Epiphany — Baptism of Our Lord
        "collect": (
            "O Lord, we beseech Thee mercifully to receive the prayers of Thy people who "
            "call upon Thee; and grant that they may both perceive and know what things they "
            "ought to do, and also may have grace and power faithfully to fulfill the same; "
            "through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and "
            "the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "In Excelso Throno", "ref": "Isaiah 6:1; Psalm 100:1–2"},
    },
    "epiphany_2": {
        "collect": (
            "Almighty and Everlasting God, Who dost govern all things in heaven and earth: "
            "Mercifully hear the supplications of Thy people, and grant us Thy peace all the "
            "days of our life; through Jesus Christ, Thy Son, our Lord, Who liveth and "
            "reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Omnis Terra", "ref": "Psalm 66:1–2, 4"},
    },
    "epiphany_3": {
        "collect": (
            "Almighty and Everlasting God, mercifully look upon our infirmities, and in all "
            "our dangers and necessities stretch forth the right hand of Thy Majesty, to help "
            "and defend us; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth "
            "with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Adorate Deum", "ref": "Psalm 97:7–8; Psalm 97:1"},
    },
    "epiphany_4": {
        "collect": (
            "Almighty God, Who knowest us to be set in the midst of so many and great "
            "dangers, that by reason of the frailty of our nature we cannot always stand "
            "upright: Grant to us such strength and protection as may support us in all "
            "dangers, and carry us through all temptations; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Adorate Deum", "ref": "Psalm 97:7–8; Psalm 97:1"},
    },
    "epiphany_5": {
        "collect": (
            "O Lord, we beseech Thee to keep Thy Church and Household continually in Thy "
            "true religion; that they who do lean only upon the hope of Thy heavenly grace "
            "may evermore be defended by Thy mighty power; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Adorate Deum", "ref": "Psalm 97:7–8; Psalm 97:1"},
    },
    "epiphany_6": {
        "collect": (
            "O Lord, we beseech Thee to keep Thy Church and Household continually in Thy "
            "true religion; that they who do lean only upon the hope of Thy heavenly grace "
            "may evermore be defended by Thy mighty power; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Adorate Deum", "ref": "Psalm 97:7–8; Psalm 97:1"},
    },
    "epiphany_7": {
        "collect": (
            "O Lord, we beseech Thee to keep Thy Church and Household continually in Thy "
            "true religion; that they who do lean only upon the hope of Thy heavenly grace "
            "may evermore be defended by Thy mighty power; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Adorate Deum", "ref": "Psalm 97:7–8; Psalm 97:1"},
    },
    "epiphany_8": {
        "collect": (
            "O Lord, we beseech Thee to keep Thy Church and Household continually in Thy "
            "true religion; that they who do lean only upon the hope of Thy heavenly grace "
            "may evermore be defended by Thy mighty power; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Adorate Deum", "ref": "Psalm 97:7–8; Psalm 97:1"},
    },
    "transfiguration": {
        "collect": (
            "O God, Who in the glorious Transfiguration of Thy Only-begotten Son, hast "
            "confirmed the mysteries of the faith by the testimony of the fathers, and Who, "
            "in the voice that came from the bright cloud, didst in a wonderful manner "
            "foreshow the adoption of sons: Mercifully vouchsafe to make us co-heirs with "
            "the King of His glory, and bring us to the enjoyment of the same; through the "
            "same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the "
            "Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Illuxerunt", "ref": "Psalm 77:18; Psalm 84:1"},
    },

    # -----------------------------------------------------------------------
    # PRE-LENT
    # -----------------------------------------------------------------------
    "septuagesima": {
        "collect": (
            "O Lord, we beseech Thee favorably to hear the prayers of Thy people: that we, "
            "who are justly punished for our offences, may be mercifully delivered by Thy "
            "goodness, for the glory of Thy Name; through Jesus Christ, Thy Son, our Lord, "
            "Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world "
            "without end. Amen."
        ),
        "introit": {"name": "Circumdederunt Me", "ref": "Psalm 18:4–5; Psalm 18:1–2"},
    },
    "sexagesima": {
        "collect": (
            "O Lord God, Who seest that we put not our trust in anything that we do: "
            "Mercifully grant that by Thy power we may be defended against all adversity; "
            "through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and "
            "the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Exsurge", "ref": "Psalm 44:23–24, 26; Psalm 44:1"},
    },
    "quinquagesima": {
        "collect": (
            "O Lord, we beseech Thee mercifully hear our prayers, and, having set us free "
            "from the bonds of sin, defend us from all evil; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Esto Mihi", "ref": "Psalm 31:2–3; Psalm 31:1"},
    },

    # -----------------------------------------------------------------------
    # LENT
    # -----------------------------------------------------------------------
    "ash_wednesday": {
        "collect": (
            "Almighty and Everlasting God, Who hatest nothing that Thou hast made, and dost "
            "forgive the sins of all those who are penitent: Create and make in us new and "
            "contrite hearts, that we, worthily lamenting our sins, and acknowledging our "
            "wretchedness, may obtain of Thee, the God of all mercy, perfect remission and "
            "forgiveness; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth "
            "with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Miserere Mihi", "ref": "Psalm 57:1; Psalm 57:1"},
    },
    "lent_1": {
        "collect": (
            "O Lord, mercifully hear our prayer, and stretch forth the right hand of Thy "
            "Majesty to defend us from them that rise up against us; through Jesus Christ, "
            "Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever "
            "One God, world without end. Amen."
        ),
        "introit": {"name": "Invocavit", "ref": "Psalm 91:15–16; Psalm 91:1"},
    },
    "lent_2": {
        "collect": (
            "O God, Who seest that of ourselves we have no strength: Keep us both outwardly "
            "and inwardly; that we may be defended from all adversities which may happen to "
            "the body, and from all evil thoughts which may assault and hurt the soul; "
            "through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and "
            "the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Reminiscere", "ref": "Psalm 25:6–7; Psalm 25:1–2"},
    },
    "lent_3": {
        "collect": (
            "We beseech Thee, Almighty God, look upon the hearty desires of Thy humble "
            "servants, and stretch forth the right hand of Thy Majesty to be our defence "
            "against all our enemies; through Jesus Christ, Thy Son, our Lord, Who liveth "
            "and reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Oculi", "ref": "Psalm 25:15–16; Psalm 25:1"},
    },
    "lent_4": {
        "collect": (
            "Grant, we beseech Thee, Almighty God, that we, who for our evil deeds do "
            "worthily deserve to be punished, by the comfort of Thy grace may mercifully be "
            "relieved; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with "
            "Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Laetare", "ref": "Isaiah 66:10–11; Psalm 122:1"},
    },
    "lent_5": {
        "collect": (
            "We beseech Thee, Almighty God, mercifully to look upon Thy people, that by Thy "
            "great goodness they may be governed and preserved evermore, both in body and "
            "soul; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with "
            "Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Judica", "ref": "Psalm 43:1–2; Psalm 43:1"},
    },

    # -----------------------------------------------------------------------
    # HOLY WEEK
    # -----------------------------------------------------------------------
    "palm_sunday": {
        "collect": (
            "Almighty and Everlasting God, Who hast sent Thy Son, our Saviour Jesus Christ, "
            "to take upon Him our flesh, and to suffer death upon the Cross, that all mankind "
            "should follow the example of His great humility: Mercifully grant that we may "
            "both follow the example of His patience, and also be made partakers of His "
            "resurrection; through the same Jesus Christ, Thy Son, our Lord, Who liveth and "
            "reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Palmarum", "ref": "Psalm 22:19, 21–22; Psalm 22:1"},
    },
    "maundy_thursday": {
        "collect": (
            "O Lord God, Who hast left unto us in a wonderful Sacrament a memorial of Thy "
            "Passion: Grant, we beseech Thee, that we may so use this Sacrament of Thy Body "
            "and Blood, that the fruits of Thy redemption may continually be manifest in us; "
            "Who livest and reignest with the Father and the Holy Ghost, ever One God, world "
            "without end. Amen."
        ),
        "introit": {"name": "Nos Autem Gloriari", "ref": "Galatians 6:14; Psalm 67:1"},
    },
    "good_friday": {
        "collect": (
            "Almighty God, we beseech Thee graciously to behold this Thy family, for which "
            "our Lord Jesus Christ was contented to be betrayed, and given up into the hands "
            "of wicked men, and to suffer death upon the Cross; through the same Jesus "
            "Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy "
            "Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Popule Meus", "ref": "Isaiah 52:13–53:3; Psalm 102:1"},
    },

    # -----------------------------------------------------------------------
    # EASTER SEASON
    # -----------------------------------------------------------------------
    "easter": {
        "collect": (
            "Almighty God, Who, through Thine Only-begotten Son, Jesus Christ, hast "
            "overcome death, and opened unto us the gate of everlasting life: We humbly "
            "beseech Thee, that, as Thou dost put into our minds good desires, so by Thy "
            "continual help we may bring the same to good effect; through Jesus Christ, Thy "
            "Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One "
            "God, world without end. Amen."
        ),
        "introit": {"name": "Resurrexi", "ref": "Psalm 139:18, 5–6"},
    },
    "easter_2": {
        # Quasimodogeniti — First Sunday after Easter
        "collect": (
            "Grant, we beseech Thee, Almighty God, that we who have celebrated the "
            "solemnities of the Lord's Resurrection, may, by the help of Thy grace, bring "
            "forth the fruits thereof in our life and conversation; through the same Jesus "
            "Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy "
            "Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Quasimodogeniti", "ref": "1 Peter 2:2; Psalm 81:1"},
    },
    "easter_3": {
        # Misericordias Domini — Second Sunday after Easter
        "collect": (
            "God, Who, by the humiliation of Thy Son, didst raise up the fallen world: "
            "Grant unto Thy faithful ones perpetual gladness, and those whom Thou hast "
            "delivered from the danger of everlasting death, do Thou make partakers of "
            "eternal joys; through the same Jesus Christ, Thy Son, our Lord, Who liveth "
            "and reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Misericordias Domini", "ref": "Psalm 33:5–6; Psalm 33:1"},
    },
    "easter_4": {
        # Jubilate — Third Sunday after Easter
        "collect": (
            "Almighty God, Who showest to them that be in error the light of Thy truth, to "
            "the intent that they may return into the way of righteousness: Grant unto all "
            "them that are admitted into the fellowship of Christ's Religion that they may "
            "eschew those things that are contrary to their profession, and follow all such "
            "things as are agreeable to the same; through Jesus Christ, Thy Son, our Lord, "
            "Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world "
            "without end. Amen."
        ),
        "introit": {"name": "Jubilate", "ref": "Psalm 66:1–2; Psalm 66:3"},
    },
    "easter_5": {
        # Cantate — Fourth Sunday after Easter
        "collect": (
            "O God, Who makest the minds of the faithful to be of one will: Grant unto Thy "
            "people that they may love what Thou commandest, and desire what Thou dost "
            "promise: that, among the manifold changes of this world, our hearts may there "
            "be fixed where true joys are to be found; through Jesus Christ, Thy Son, our "
            "Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world "
            "without end. Amen."
        ),
        "introit": {"name": "Cantate", "ref": "Psalm 98:1–2; Psalm 98:3"},
    },
    "easter_6": {
        # Rogate — Fifth Sunday after Easter
        "collect": (
            "O God, from Whom all good things do come: Grant to us Thy humble servants, that "
            "by Thy holy inspiration we may think those things that be right, and by Thy "
            "merciful guiding may perform the same; through Jesus Christ, Thy Son, our Lord, "
            "Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world "
            "without end. Amen."
        ),
        "introit": {"name": "Vocem Iucunditatis", "ref": "Isaiah 48:20; Psalm 66:1"},
    },
    "easter_7": {
        # Exaudi — Sunday after Ascension
        "collect": (
            "Almighty, Everlasting God, make us to have always a devout will towards Thee, "
            "and to serve Thy Majesty with a pure heart; through Jesus Christ, Thy Son, our "
            "Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world "
            "without end. Amen."
        ),
        "introit": {"name": "Exaudi", "ref": "Psalm 27:7–9; Psalm 27:1"},
    },
    "ascension": {
        "collect": (
            "Grant, we beseech Thee, Almighty God, that like as we do believe Thy "
            "Only-begotten Son, our Lord Jesus Christ, to have ascended into the heavens; so "
            "may we also in heart and mind thither ascend, and with Him continually dwell, "
            "Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world "
            "without end. Amen."
        ),
        "introit": {"name": "Viri Galilaei", "ref": "Acts 1:11; Psalm 47:1"},
    },
    "pentecost": {
        "collect": (
            "O God, Who didst teach the hearts of Thy faithful people, by sending to them "
            "the light of Thy Holy Spirit: Grant us by the same Spirit to have a right "
            "judgment in all things, and evermore to rejoice in His holy comfort; through "
            "Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the "
            "Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Spiritus Domini", "ref": "Wisdom 1:7; Psalm 68:1"},
    },

    # -----------------------------------------------------------------------
    # TRINITY SEASON
    # -----------------------------------------------------------------------
    "holy_trinity": {
        "collect": (
            "Almighty and Everlasting God, Who hast given unto us, Thy servants, grace, by "
            "the confession of a true faith, to acknowledge the glory of the Eternal Trinity, "
            "and in the power of the Divine Majesty to worship the Unity: We beseech Thee, "
            "that Thou wouldest keep us steadfast in this faith, and evermore defend us from "
            "all adversities; Who livest and reignest, One God, world without end. Amen."
        ),
        "introit": {"name": "Benedicta Sit", "ref": "Tobit 12:6; Psalm 8:1"},
    },
    "trinity_1": {
        "collect": (
            "O God, the Strength of all them that put their trust in Thee: Mercifully accept "
            "our prayers: and because through the weakness of our mortal nature we can do no "
            "good thing without Thee, grant us the help of Thy grace, that in keeping Thy "
            "commandments we may please Thee, both in will and deed; through Jesus Christ, "
            "Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever "
            "One God, world without end. Amen."
        ),
        "introit": {"name": "Domine in Tua Misericordia", "ref": "Psalm 13:5–6; Psalm 13:1"},
    },
    "trinity_2": {
        "collect": (
            "O Lord, Who never failest to help and govern those whom Thou dost bring up in "
            "Thy steadfast fear and love: Make us to have a perpetual fear and love of Thy "
            "holy Name; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth "
            "with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Factus Est Dominus", "ref": "Psalm 18:18–19; Psalm 18:1"},
    },
    "trinity_3": {
        "collect": (
            "O God, the Protector of all that trust in Thee, without Whom nothing is strong, "
            "nothing is holy: Increase and multiply upon us Thy mercy: that Thou being our "
            "Ruler and Guide, we may so pass through things temporal, that we finally lose "
            "not the things eternal; through Jesus Christ, Thy Son, our Lord, Who liveth and "
            "reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Respice in Me", "ref": "Psalm 25:16, 18; Psalm 25:1"},
    },
    "trinity_4": {
        "collect": (
            "Grant, Lord, we beseech Thee, that the course of this world may be so peaceably "
            "ordered by Thy governance, that Thy Church may joyfully serve Thee in all godly "
            "quietness; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth "
            "with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Dominus Illuminatio", "ref": "Psalm 27:1, 3; Psalm 27:4"},
    },
    "trinity_5": {
        "collect": (
            "O God, Who hast prepared for them that love Thee such good things as pass man's "
            "understanding: Pour into our hearts such love toward Thee, that we, loving Thee "
            "above all things, may obtain Thy promises, which exceed all that we can desire; "
            "through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and "
            "the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Exaudi Domine", "ref": "Psalm 27:7–8; Psalm 27:1"},
    },
    "trinity_6": {
        "collect": (
            "Lord of all power and might, Who art the Author and Giver of all good things: "
            "Graft in our hearts the love of Thy Name, increase in us true religion, nourish "
            "us with all goodness, and of Thy great mercy keep us in the same; through Jesus "
            "Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy "
            "Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Dominus Fortitudo", "ref": "Psalm 28:8–9; Psalm 28:1"},
    },
    "trinity_7": {
        "collect": (
            "O God, Whose never-failing Providence ordereth all things both in heaven and "
            "earth: We humbly beseech Thee to put away from us all hurtful things, and to "
            "give us those things which be profitable for us; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Omnes Gentes", "ref": "Psalm 47:1–2; Psalm 47:3"},
    },
    "trinity_8": {
        "collect": (
            "Grant to us, Lord, we beseech Thee, the Spirit to think and do always such "
            "things as are right; that we, who cannot do anything that is good without Thee, "
            "may by Thee be enabled to live according to Thy will; through Jesus Christ, Thy "
            "Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One "
            "God, world without end. Amen."
        ),
        "introit": {"name": "Suscepimus Deus", "ref": "Psalm 48:9–10; Psalm 48:1"},
    },
    "trinity_9": {
        "collect": (
            "Let Thy merciful ears, O Lord, be open to the prayers of Thy humble servants: "
            "and, that they may obtain their petitions, make them to ask such things as shall "
            "please Thee; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth "
            "with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Dum Clamarem", "ref": "Psalm 54:2–3; Psalm 54:1"},
    },
    "trinity_10": {
        "collect": (
            "O God, Who declarest Thine almighty power chiefly in showing mercy and pity: "
            "Mercifully grant unto us such a measure of Thy grace, that we, running the way "
            "of Thy commandments, may obtain Thy gracious promises, and be made partakers "
            "of Thy heavenly treasure; through Jesus Christ, Thy Son, our Lord, Who liveth "
            "and reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Dum Clamarem", "ref": "Psalm 55:16–17; Psalm 55:1"},
    },
    "trinity_11": {
        "collect": (
            "Almighty and Everlasting God, Who art always more ready to hear than we to "
            "pray, and art wont to give more than either we desire or deserve: Pour down "
            "upon us the abundance of Thy mercy, forgiving us those things whereof our "
            "conscience is afraid, and giving us those good things which we are not worthy "
            "to ask, but through the merits and mediation of Jesus Christ, Thy Son, our "
            "Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world "
            "without end. Amen."
        ),
        "introit": {"name": "Deus in Loco Sancto", "ref": "Psalm 68:5–6; Psalm 68:1"},
    },
    "trinity_12": {
        "collect": (
            "Almighty and Merciful God, of Whose only gift it cometh that Thy faithful "
            "people do unto Thee true and laudable service: Grant, we beseech Thee, that we "
            "may so faithfully serve Thee in this life, that we fail not finally to attain "
            "Thy heavenly promises; through Jesus Christ, Thy Son, our Lord, Who liveth and "
            "reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Deus in Adiutorium", "ref": "Psalm 70:1–2; Psalm 70:4"},
    },
    "trinity_13": {
        "collect": (
            "Almighty and Everlasting God, give unto us the increase of faith, hope, and "
            "charity; and that we may obtain that which Thou dost promise, make us to love "
            "that which Thou dost command; through Jesus Christ, Thy Son, our Lord, Who "
            "liveth and reigneth with Thee and the Holy Ghost, ever One God, world without "
            "end. Amen."
        ),
        "introit": {"name": "Respice Domine", "ref": "Psalm 74:20, 19, 23; Psalm 74:1"},
    },
    "trinity_14": {
        "collect": (
            "Keep, we beseech Thee, O Lord, Thy Church with Thy perpetual mercy; and, "
            "because the frailty of man without Thee cannot but fall, keep us ever by Thy "
            "help from all things hurtful, and lead us to all things profitable to our "
            "salvation; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth "
            "with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Protector Noster", "ref": "Psalm 84:9–10; Psalm 84:1"},
    },
    "trinity_15": {
        "collect": (
            "O Lord, we beseech Thee, let Thy continual pity cleanse and defend Thy Church: "
            "and because it cannot continue in safety without Thy succor, preserve it "
            "evermore by Thy help and goodness; through Jesus Christ, Thy Son, our Lord, "
            "Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world "
            "without end. Amen."
        ),
        "introit": {"name": "Inclina Domine", "ref": "Psalm 86:1–3; Psalm 86:6"},
    },
    "trinity_16": {
        "collect": (
            "Lord, we pray Thee, that Thy grace may always go before and follow after us, "
            "and make us continually to be given to all good works; through Jesus Christ, "
            "Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever "
            "One God, world without end. Amen."
        ),
        "introit": {"name": "Miserere Mihi Domine", "ref": "Psalm 86:3, 5; Psalm 86:1"},
    },
    "trinity_17": {
        "collect": (
            "Lord, we beseech Thee, grant Thy people grace, to withstand the temptations of "
            "the devil, and with pure hearts and minds to follow Thee, the only God; through "
            "Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the "
            "Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Iustus Es Domine", "ref": "Psalm 119:137–138; Psalm 119:1"},
    },
    "trinity_18": {
        "collect": (
            "O God, forasmuch as without Thee we are not able to please Thee: Mercifully "
            "grant, that Thy Holy Spirit may in all things direct and rule our hearts; "
            "through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and "
            "the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Da Pacem Domine", "ref": "Psalm 122:6–7; Psalm 122:1"},
    },
    "trinity_19": {
        "collect": (
            "O Almighty and most Merciful God, of Thy bountiful goodness keep us, we "
            "beseech Thee, from all things that may hurt us; that we, being ready, both in "
            "body and soul, may cheerfully accomplish those things that Thou wouldest have "
            "done; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with "
            "Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Salus Populi", "ref": "Psalm 38:22–23; Psalm 38:1"},
    },
    "trinity_20": {
        "collect": (
            "Grant, we beseech Thee, Merciful Lord, to Thy faithful people pardon and "
            "peace, that they may be cleansed from all their sins, and serve Thee with a "
            "quiet mind; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth "
            "with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Omnia Quae Fecisti", "ref": "Psalm 48:9; Psalm 48:1"},
    },
    "trinity_21": {
        "collect": (
            "Lord, we beseech Thee to keep Thy household, the Church, in continual "
            "godliness; that through Thy protection it may be free from all adversities, "
            "and devoutly given to serve Thee in good works, to the glory of Thy Name; "
            "through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee "
            "and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "In Voluntate Tua", "ref": "Esther 13:9–10; Psalm 119:1"},
    },
    "trinity_22": {
        "collect": (
            "O God, our Refuge and Strength, Who art the Author of all godliness: Be ready, "
            "we beseech Thee, to hear the devout prayers of Thy Church; and grant that those "
            "things which we ask faithfully, we may obtain effectually; through Jesus Christ, "
            "Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever "
            "One God, world without end. Amen."
        ),
        "introit": {"name": "Si Iniquitates", "ref": "Psalm 130:3–4; Psalm 130:1"},
    },
    "trinity_23": {
        "collect": (
            "Absolve, we beseech Thee, O Lord, Thy people from their offences; that from "
            "the bonds of our sins which, by reason of our frailty, we have brought upon us, "
            "we may be delivered by Thy bountiful goodness; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Dicit Dominus", "ref": "Jeremiah 29:11, 12, 14; Psalm 85:1"},
    },
    "trinity_24": {
        "collect": (
            "Stir up, we beseech Thee, O Lord, the wills of Thy faithful people; that they, "
            "plenteously bringing forth the fruit of good works, may of Thee be plenteously "
            "rewarded; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with "
            "Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Dicit Dominus", "ref": "Psalm 95:6–7; Psalm 95:1"},
    },
    "trinity_25": {
        "collect": (
            "Almighty God, we beseech Thee, show Thy mercy unto Thy humble servants, that "
            "we who put no trust in our own merits may not be dealt with after the severity "
            "of Thy judgment, but according to Thy mercy; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Dicit Dominus", "ref": "Psalm 31:9–10; Psalm 31:1"},
    },
    "trinity_26": {
        "collect": (
            "God, so rule and govern our hearts and minds by Thy Holy Spirit, that being "
            "ever mindful of the end of all things, and the day of Thy just judgment, we may "
            "be stirred up to holiness of living here, and dwell with Thee forever hereafter; "
            "through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and "
            "the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Ego Autem", "ref": "Psalm 54:4–5; Psalm 54:1"},
    },
    "trinity_27": {
        "collect": (
            "Absolve, we beseech Thee, O Lord, Thy people from their offences; that from "
            "the bonds of our sins which, by reason of our frailty, we have brought upon us, "
            "we may be delivered by Thy bountiful goodness; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Ego Autem", "ref": "Psalm 54:4–5; Psalm 54:1"},
    },
    "last_sunday": {
        # Sunday of the Fulfillment / Last Sunday after Trinity
        "collect": (
            "Absolve, we beseech Thee, O Lord, Thy people from their offences; that from "
            "the bonds of our sins which, by reason of our frailty, we have brought upon us, "
            "we may be delivered by Thy bountiful goodness; through Jesus Christ, Thy Son, "
            "our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, "
            "world without end. Amen."
        ),
        "introit": {"name": "Ego Sum Alpha et Omega", "ref": "Revelation 1:8; Psalm 24:7"},
    },

    # -----------------------------------------------------------------------
    # PRINCIPAL FEASTS
    # -----------------------------------------------------------------------
    "reformation": {
        "collect": (
            "O Lord God, Heavenly Father, pour out, we beseech Thee, Thy Holy Spirit upon "
            "Thy faithful people, keep them steadfast in Thy grace and truth, protect and "
            "comfort them in all temptation, defend them against all enemies of Thy Word, "
            "and bestow upon Christ's Church militant Thy saving peace; through the same "
            "Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the "
            "Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Dominus Fortitudo Plebis", "ref": "Psalm 46:7, 4; Psalm 46:1"},
    },
    "all_saints": {
        "collect": (
            "O Almighty God, Who hast knit together Thine elect in one communion and "
            "fellowship in the mystical Body of Thy Son, Christ our Lord: Grant us grace so "
            "to follow Thy blessed Saints in all virtuous and godly living, that we may come "
            "to those unspeakable joys which Thou hast prepared for those who unfeignedly "
            "love Thee; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth "
            "with Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Gaudeamus", "ref": "Revelation 7:14, 17; Psalm 33:1"},
    },
    "st_michael": {
        "collect": (
            "O Everlasting God, Who hast ordained and constituted the services of angels "
            "and men in a wonderful order: Mercifully grant, that as Thy holy angels always "
            "do Thee service in Heaven, so by Thy appointment they may succor and defend us "
            "on earth; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with "
            "Thee and the Holy Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Benedicite Dominum", "ref": "Psalm 103:20–21; Psalm 103:1"},
    },
    "thanksgiving": {
        "collect": (
            "Almighty God, our Heavenly Father, Whose mercies are new unto us every morning, "
            "and Who, though we have in no wise deserved Thy goodness, dost abundantly "
            "provide for all our wants of body and soul: Give us, we pray Thee, Thy Holy "
            "Spirit, that we may heartily acknowledge Thy merciful goodness toward us, give "
            "thanks for all Thy benefits, and serve Thee in willing obedience; through Jesus "
            "Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy "
            "Ghost, ever One God, world without end. Amen."
        ),
        "introit": {"name": "Laudate Dominum", "ref": "Psalm 150:6, 2; Psalm 150:1"},
    },

}


if __name__ == "__main__":
    # Quick sanity check
    print(f"Total slots defined: {len(ONE_YEAR_PROPERS)}")
    for key, val in ONE_YEAR_PROPERS.items():
        assert "collect" in val, f"Missing collect: {key}"
        assert "introit" in val, f"Missing introit: {key}"
        assert "name" in val["introit"], f"Missing introit name: {key}"
        assert "ref" in val["introit"], f"Missing introit ref: {key}"
    print("All entries valid.")
