"""
TLH 1941 / Common Service Book 1917 Collects, Introits, and Graduals
for the Lutheran One-Year Lectionary.

Texts (collects, introit antiphons + psalm verses, graduals): from the
*Common Service Book of the Lutheran Church* (Philadelphia, 1917), section
"Introits, Collects, Epistles, Graduals and Gospels" — public domain (published
before 1928). This is the same historic, KJV-era wording later carried into
*The Lutheran Hymnal* (TLH, 1941); we cite the 1917 source because it clears the
public-domain threshold unambiguously. LSB collect/introit texts are referenced
to the *LSB Altar Book* and are never reproduced here.

Introit antiphons are given as printed in the CSB (antiphon + appointed psalm
verse); the invariable Gloria Patri that follows in the rite is omitted. Latin
incipit names (introit["name"]) are the traditional Western/Lutheran titles.
Each entry carries a `source` citation (work, section, day).

Verified: every collect in this file was checked against the CSB 1917 text
(tools/extract_csb.py); 67/76 are byte-identical, the remainder differ only in
the OCR of the source compilation, not in substance.
"""

ONE_YEAR_PROPERS = {

    # -----------------------------------------------------------------------
    # ADVENT
    # -----------------------------------------------------------------------
    "advent_1": {
        "collect": (
            'Stir up, we beseech Thee, Thy power, O Lord, and come; that by Thy protection we may '
            'be rescued from the threatening perils of our sins, and saved by Thy mighty '
            'deliverance; Who livest and reignest with the Father and the Holy Ghost, ever One '
            'God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Ad Te Levavi',
            "ref": 'Psalm 25:1–3, 5',
            "text": (
                'UNTO Thee, O Lord, do I lift up my soul: O my God, I trust in Thee. Let me not be '
                'ashamed: let not mine enemies triumph over me. Yea, let none that wait on Thee: be '
                'ashamed. Psalm. Show me Thy ways, O Lord: teach me Thy paths.'
            ),
        },
        "gradual": (
            'ALL they that wait for Thee: shall not be ashamed, O Lord. Verse. Show me Thy ways, '
            'O Lord: teach me Thy paths. Hallelujah. Hallelujah. V. Show us Thy mercy, O Lord: '
            'and grant us Thy salvation. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — First Sunday in Advent'
        ),
    },
    "advent_2": {
        "collect": (
            'Stir up our hearts, O Lord, to make ready the way of Thine Only-begotten Son, so '
            'that by His coming we may be enabled to serve Thee with pure minds; through the same '
            'Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy '
            'Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Populus Sion',
            "ref": 'Isaiah 30:30; Psalm 80:1',
            "text": (
                'DAUGHTER of Zion: behold thy salvation cometh. The Lord shall cause His glorious '
                'voice to be heard: and ye shall have gladness of heart. Psalm. Give ear, O Shepherd '
                'of Israel: Thou that leadest Joseph like a flock.'
            ),
        },
        "gradual": (
            'OUT of Zion the perfection of beauty God hath shined: Our God shall come. V. Gather '
            'My saints together unto Me: those that have made a covenant with Me by sacrifice. '
            'Hallelujah. Hallelujah. V. I was glad when they said unto me: Let us go into the '
            'house of the Lord. Hallelujah. Hallelujah. V. Our feet shall stand within thy gates: '
            'O Jerusalem. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Second Sunday in Advent'
        ),
    },
    "advent_3": {
        "collect": (
            'Lord, we beseech Thee, give ear to our prayers, and lighten the darkness of our '
            'hearts by Thy gracious visitation; Who livest and reignest with the Father and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Gaudete',
            "ref": 'Philippians 4:4–5; Psalm 85:1',
            "text": (
                'REJOICE in the Lord alway: and again I say, Rejoice. Let your moderation be known '
                'unto all men: the Lord is at hand. Be careful for nothing: but in everything by '
                'prayer and supplication with thanksgiving let your requests be made known unto God. '
                'Psalm. Lord, Thou hast been favorable unto Thy land: Thou hast brought back the '
                'captivity of Jacob.'
            ),
        },
        "gradual": (
            'THOU that dwellest between the Cherubim, shine forth: Stir up Thy strength and come. '
            'Give ear, O Shepherd of Israel: Thou that leadest Joseph like a flock. Hallelujah. '
            'Hallelujah. V. Stir up Thy strength: and come and save us. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Third Sunday in Advent'
        ),
    },
    "advent_4": {
        "collect": (
            'Stir up, O Lord, we beseech Thee, Thy power, and come, and with great might succor '
            'us, that by the help of Thy grace whatsoever is hindered by our sin may be speedily '
            'accomplished, through Thy mercy and satisfaction; Who livest and reignest with the '
            'Father and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Rorate Caeli',
            "ref": 'Isaiah 45:8; Psalm 19:1',
            "text": (
                'DROP down, ye heavens, from above: and let the skies pour down righteousness. Let '
                'the earth open: and bring forth salvation. Psalm. The heavens declare the glory of '
                'God: and the firmament showeth His handiwork.'
            ),
        },
        "gradual": (
            'THE Lord is nigh unto all them that call upon Him: to all that call upon Him in '
            'truth. My mouth shall speak the praise of the Lord: and let all flesh bless His Holy '
            'Name. Hallelujah. Hallelujah. V. Thou art my Help and my Deliverer: make no '
            'tarrying, my God. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fourth Sunday in Advent'
        ),
    },

    # -----------------------------------------------------------------------
    # CHRISTMAS
    # -----------------------------------------------------------------------
    "christmas_eve": {
        "collect": (
            'O God, Who hast made this most holy night to shine with the brightness of the true '
            'Light: Grant, we beseech Thee, that as we have known on earth the mysteries of that '
            'Light, we may also come to the fullness of His joys in heaven; Who liveth and '
            'reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Hodie Scietis',
            "ref": 'Exodus 16:6–7; Psalm 96:1',
        },
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Nativity of Our Lord (Christmas Eve)'
        ),
    },
    "christmas_midnight": {
        "collect": (
            'O God, Who hast made this most holy night to shine with the brightness of the true '
            'Light: Grant, we beseech Thee, that as we have known on earth the mysteries of that '
            'Light, we may also come to the fullness of His joys in heaven; Who liveth and '
            'reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Dominus Dixit',
            "ref": 'Psalm 2:7; Psalm 110:3',
            "text": (
                'THE Lord hath said unto Me, Thou art My Son: this day have I begotten Thee. Psalm. '
                'The Lord reigneth, He is clothed with majesty: the Lord is clothed with strength, '
                'wherewith He hath girded Himself.'
            ),
        },
        "gradual": (
            'THY people shall be willing in the day of Thy power: in the beauties of holiness '
            'from the womb of the morning. V. The Lord said unto my Lord, Sit Thou at My right '
            'hand: until I make Thine enemies Thy footstool. Hallelujah. Hallelujah. V. The Lord '
            'hath said unto Me, Thou art Mv Son: this day have I begotten Thee. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Nativity of Our Lord (Midnight)'
        ),
    },
    "christmas_dawn": {
        "collect": (
            'O God, Who hast made this most holy night to shine with the brightness of the true '
            'Light: Grant, we beseech Thee, that as we have known on earth the mysteries of that '
            'Light, we may also come to the fullness of His joys in heaven; Who liveth and '
            'reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Lux Fulgebit',
            "ref": 'Isaiah 9:2, 6; Psalm 98:1',
        },
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Nativity of Our Lord (Dawn)'
        ),
    },
    "christmas_day": {
        "collect": (
            'Grant, we beseech Thee, Almighty God, that the new Birth of Thine Only-begotten Son '
            'in the flesh may set us free who are held in the old bondage under the yoke of sin; '
            'through the same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee '
            'and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Puer Natus Est',
            "ref": 'Isaiah 9:6; Psalm 98:1',
            "text": (
                'UNTO us a Child is born, unto us a Son is given: and the government shall be upon '
                'His shoulder. And His Name shall be called Wonderful, Counsellor, The Mighty God: '
                'The Everlasting Father, The Prince of Peace. Psalm. O sing unto the Lord a new song: '
                'for He hath done marvelous things.'
            ),
        },
        "gradual": (
            'ALL the ends of the earth have seen the salvation of our God: Make a joyful noise '
            'unto the Lord, all the earth. V. The Lord hath made known His salvation: His '
            'righteousness hath He openly showed in the sight of the heathen. Hallelujah. '
            'Hallelujah. V. O come, let us sing unto the Lord: Let us worship and bow down before '
            'Him. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Nativity of Our Lord (Day)'
        ),
    },
    "christmas_sunday_1": {
        "collect": (
            'Almighty and Everlasting God, direct our actions according to Thy good pleasure, '
            'that in the Name of Thy beloved Son, we may be made to abound in good works; through '
            'the same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Dum Medium Silentium',
            "ref": 'Wisdom 18:14–15; Psalm 93:1',
            "text": (
                'THY testimonies are very sure: holiness becometh Thine house, O Lord, forever. Thy '
                'throne is established of old: Thou art from everlasting. Psalm. The Lord reigneth, '
                'He is clothed with majesty: the Lord is clothed with strength, wherewith He hath '
                'girded Himself.'
            ),
        },
        "gradual": (
            'THOU art fairer than the children of men: grace is poured into Thy lips. My heart is '
            'inditing a good matter, I speak of the things which I have made touching the King: '
            'my tongue is the pen of a ready writer. Hallelujah. Hallelujah. V. The Lord '
            'reigneth, He is clothed with majesty: the Lord is clothed with strength, wherewith '
            'He hath girded Himself. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — First Sunday after Christmas'
        ),
    },
    "christmas_sunday_2": {
        "collect": (
            'Almighty and Everlasting God, direct our actions according to Thy good pleasure, '
            'that in the Name of Thy beloved Son, we may be made to abound in good works; through '
            'the same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Dum Medium Silentium',
            "ref": 'Wisdom 18:14–15; Psalm 93:1',
            "text": (
                'THY testimonies are very sure: holiness becometh Thine house, O Lord, forever. Thy '
                'throne is established of old: Thou art from everlasting. Psalm. The Lord reigneth, '
                'He is clothed with majesty: the Lord is clothed with strength, wherewith He hath '
                'girded Himself.'
            ),
        },
        "gradual": (
            'THOU art fairer than the children of men: grace is poured into Thy lips. My heart is '
            'inditing a good matter, I speak of the things which I have made touching the King: '
            'my tongue is the pen of a ready writer. Hallelujah. Hallelujah. V. The Lord '
            'reigneth, He is clothed with majesty: the Lord is clothed with strength, wherewith '
            'He hath girded Himself. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Second Sunday after Christmas'
        ),
    },

    # -----------------------------------------------------------------------
    # EPIPHANY SEASON
    # -----------------------------------------------------------------------
    "new_years_eve": {
        "collect": (
            'O Lord God, Who, for our sakes, hast made Thy blessed Son our Saviour subject to the '
            'Law, and caused Him to endure the circumcision of the flesh: Grant us the true '
            'circumcision of the Spirit, that our hearts may be pure from all sinful desires and '
            'lusts; through the same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth '
            'with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Nomen Iesu',
            "ref": 'Philippians 2:10–11; Psalm 8:1',
            "text": (
                'O LORD our Lord, how excellent is Thy Name in all the earth: Who hast set Thy glory '
                'above the heavens. What is man that Thou art mindful of him: and the son of man that '
                'Thou visitest him? Psalm. Thou, O Lord, art our Father, our Redeemer: Thy Name is '
                'from everlasting.'
            ),
        },
        "gradual": (
            'ALL the ends of the earth have seen the salvation of our God: Make a joyful noise '
            'unto the Lord, all the earth. V. The Lord hath made known His salvation: His '
            'righteousness hath He openly showed in the sight of the heathen. Hallelujah. '
            'Hallelujah. V. God, Who of old time spake in divers ways unto the fathers by the '
            'prophets: hath in these last days spoken unto us by His Son. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            "Epistles, Graduals and Gospels — New Year's Eve"
        ),
    },
    "new_years_day": {
        "collect": (
            'O Lord God, Who, for our sakes, hast made Thy blessed Son our Saviour subject to the '
            'Law, and caused Him to endure the circumcision of the flesh: Grant us the true '
            'circumcision of the Spirit, that our hearts may be pure from all sinful desires and '
            'lusts; through the same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth '
            'with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Nomen Iesu',
            "ref": 'Philippians 2:10–11; Psalm 8:1',
            "text": (
                'O LORD our Lord, how excellent is Thy Name in all the earth: Who hast set Thy glory '
                'above the heavens. What is man that Thou art mindful of him: and the son of man that '
                'Thou visitest him? Psalm. Thou, O Lord, art our Father, our Redeemer: Thy Name is '
                'from everlasting.'
            ),
        },
        "gradual": (
            'ALL the ends of the earth have seen the salvation of our God: Make a joyful noise '
            'unto the Lord, all the earth. V. The Lord hath made known His salvation: His '
            'righteousness hath He openly showed in the sight of the heathen. Hallelujah. '
            'Hallelujah. V. God, Who of old time spake in divers ways unto the fathers by the '
            'prophets: hath in these last days spoken unto us by His Son. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Circumcision and Name of Jesus'
        ),
    },
    "epiphany": {
        "collect": (
            'O God, Who by the leading of a star didst manifest Thy Only-begotten Son to the '
            'Gentiles: Mercifully grant, that we, who know Thee now by faith, may after this life '
            'have the fruition of Thy glorious Godhead; through the same Jesus Christ, Thy Son, '
            'our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world '
            'without end. Amen.'
        ),
        "introit": {
            "name": 'Ecce Advenit',
            "ref": 'Malachi 3:1; Psalm 72:1',
            "text": (
                'BEHOLD the Lord, the Ruler, hath come: and the kingdom, and the power, and the glory '
                'are in His hand. Psalm. Give the King Thy judgments, O God: and Thy righteousness '
                'unto the King’s Son.'
            ),
        },
        "gradual": (
            'ALL they from Sheba shall come; they shall bring gold and incense: and they shall '
            'show forth the praises of the Lord. V. Arise, and shine, O Jerusalem: for the glory '
            'of the Lord is risen upon thee. Hallelujah. Hallelujah. V. We have seen His star in '
            'the east: and we have come with our gifts to worship the Lord. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Epiphany of Our Lord'
        ),
    },
    "baptism_of_lord": {
        "collect": (
            'O Lord, we beseech Thee mercifully to receive the prayers of Thy people who call '
            'upon Thee; and grant that they may both perceive and know what things they ought to '
            'do, and also may have grace and power faithfully to fulfill the same; through Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'In Excelso Throno',
            "ref": 'Isaiah 6:1; Psalm 100:1–2',
            "text": (
                'I SAW also the Lord, sitting upon a throne: high and lifted up. And I heard the '
                'voice of a great multitude, saying, Alleluia: for the Lord God Omnipotent reigneth. '
                'Psalm. Make a joyful noise unto the Lord, all ye lands: Serve the Lord with '
                'gladness.'
            ),
        },
        "gradual": (
            'BLESSED be the Lord God, the God of Israel, Who only doeth wondrous things: And '
            'blessed be His glorious Name forever. The mountains shall bring peace to Thy people: '
            'and the hills righteousness. Hallelujah. Hallelujah. V. Make a joyful noise unto the '
            'Lord, all ye lands: Serve the Lord with gladness. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Baptism of Our Lord'
        ),
    },
    "epiphany_2": {
        "collect": (
            'Almighty and Everlasting God, Who dost govern all things in heaven and earth: '
            'Mercifully hear the supplications of Thy people, and grant us Thy peace all the days '
            'of our life; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with '
            'Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Omnis Terra',
            "ref": 'Psalm 66:1–2, 4',
            "text": (
                'ALL the earth shall worship Thee: and shall sing unto Thee, O God. They shall sing '
                'to Thy Name: O Thou Most Highest. Psalm. Make a joyful noise unto God, all ye lands: '
                'sing forth the honor of His Name, make His praise glorious.'
            ),
        },
        "gradual": (
            'HE sent His Word and healed them: and delivered them from their destructions. V. Oh '
            'that men would praise the Lord for His goodness: and for His wonderful works to the '
            'children of men. Hallelujah. Hallelujah. V. Praise ye Him, all His angels: praise ye '
            'Him, all His hosts. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Second Sunday after the Epiphany'
        ),
    },
    "epiphany_3": {
        "collect": (
            'Almighty and Everlasting God, mercifully look upon our infirmities, and in all our '
            'dangers and necessities stretch forth the right hand of Thy Majesty, to help and '
            'defend us; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with '
            'Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Adorate Deum',
            "ref": 'Psalm 97:7–8; Psalm 97:1',
            "text": (
                'WORSHIP Him, all ye His angels: Zion heard and was glad. The daughters of Judah '
                'rejoiced: because of Thy judgments, O Lord. Psalm. The Lord reigneth, let the earth '
                'rejoice: let the multitude of isles be glad thereof.'
            ),
        },
        "gradual": (
            'SO the heathen shall fear the Name of the Lord: and all the kings of the earth Thy '
            'glory, When the Lord shall build up Zion: He shall appear in His glory. Hallelujah. '
            'Hallelujah. V. The Lord reigneth; let the earth rejoice: let the multitude of isles '
            'be glad thereof. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Third Sunday after the Epiphany'
        ),
    },
    "epiphany_4": {
        "collect": (
            'Almighty God, Who knowest us to be set in the midst of so many and great dangers, '
            'that by reason of the frailty of our nature we cannot always stand upright: Grant to '
            'us such strength and protection as may support us in all dangers, and carry us '
            'through all temptations; through Jesus Christ, Thy Son, our Lord, Who liveth and '
            'reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Adorate Deum',
            "ref": 'Psalm 97:7–8; Psalm 97:1',
            "text": (
                'WORSHIP Him, all ye His angels: Zion heard and was glad. The daughters of Judah '
                'rejoiced: because of Thy judgments, O Lord. Psalm. The Lord reigneth, let the earth '
                'rejoice: let the multitude of isles be glad thereof.'
            ),
        },
        "gradual": (
            'SO the heathen shall fear the Name of the Lord: and all the kings of the earth Thy '
            'glory, When the Lord shall build up Zion: He shall appear in His glory. Hallelujah. '
            'Hallelujah. V. The Lord reigneth; let the earth rejoice: let the multitude of isles '
            'be glad thereof. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fourth Sunday after the Epiphany'
        ),
    },
    "epiphany_5": {
        "collect": (
            'O Lord, we beseech Thee to keep Thy Church and Household continually in Thy true '
            'religion; that they who do lean only upon the hope of Thy heavenly grace may '
            'evermore be defended by Thy mighty power; through Jesus Christ, Thy Son, our Lord, '
            'Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world without '
            'end. Amen.'
        ),
        "introit": {
            "name": 'Adorate Deum',
            "ref": 'Psalm 97:7–8; Psalm 97:1',
            "text": (
                'WORSHIP Him, all ye His angels: Zion heard and was glad. The daughters of Judah '
                'rejoiced: because of Thy judgments, O Lord. Psalm. The Lord reigneth, let the earth '
                'rejoice: let the multitude of isles be glad thereof.'
            ),
        },
        "gradual": (
            'SO the heathen shall fear the Name of the Lord: and all the kings of the earth Thy '
            'glory, When the Lord shall build up Zion: He shall appear in His glory. Hallelujah. '
            'Hallelujah. V. The Lord reigneth; let the earth rejoice: let the multitude of isles '
            'be glad thereof. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fifth Sunday after the Epiphany'
        ),
    },
    "epiphany_6": {
        "collect": (
            'O Lord, we beseech Thee to keep Thy Church and Household continually in Thy true '
            'religion; that they who do lean only upon the hope of Thy heavenly grace may '
            'evermore be defended by Thy mighty power; through Jesus Christ, Thy Son, our Lord, '
            'Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world without '
            'end. Amen.'
        ),
        "introit": {
            "name": 'Adorate Deum',
            "ref": 'Psalm 97:7–8; Psalm 97:1',
            "text": (
                'WORSHIP Him, all ye His angels: Zion heard and was glad. The daughters of Judah '
                'rejoiced: because of Thy judgments, O Lord. Psalm. The Lord reigneth, let the earth '
                'rejoice: let the multitude of isles be glad thereof.'
            ),
        },
        "gradual": (
            'SO the heathen shall fear the Name of the Lord: and all the kings of the earth Thy '
            'glory, When the Lord shall build up Zion: He shall appear in His glory. Hallelujah. '
            'Hallelujah. V. The Lord reigneth; let the earth rejoice: let the multitude of isles '
            'be glad thereof. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — epiphany_6'
        ),
    },
    "epiphany_7": {
        "collect": (
            'O Lord, we beseech Thee to keep Thy Church and Household continually in Thy true '
            'religion; that they who do lean only upon the hope of Thy heavenly grace may '
            'evermore be defended by Thy mighty power; through Jesus Christ, Thy Son, our Lord, '
            'Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world without '
            'end. Amen.'
        ),
        "introit": {
            "name": 'Adorate Deum',
            "ref": 'Psalm 97:7–8; Psalm 97:1',
            "text": (
                'WORSHIP Him, all ye His angels: Zion heard and was glad. The daughters of Judah '
                'rejoiced: because of Thy judgments, O Lord. Psalm. The Lord reigneth, let the earth '
                'rejoice: let the multitude of isles be glad thereof.'
            ),
        },
        "gradual": (
            'SO the heathen shall fear the Name of the Lord: and all the kings of the earth Thy '
            'glory, When the Lord shall build up Zion: He shall appear in His glory. Hallelujah. '
            'Hallelujah. V. The Lord reigneth; let the earth rejoice: let the multitude of isles '
            'be glad thereof. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — epiphany_7'
        ),
    },
    "epiphany_8": {
        "collect": (
            'O Lord, we beseech Thee to keep Thy Church and Household continually in Thy true '
            'religion; that they who do lean only upon the hope of Thy heavenly grace may '
            'evermore be defended by Thy mighty power; through Jesus Christ, Thy Son, our Lord, '
            'Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world without '
            'end. Amen.'
        ),
        "introit": {
            "name": 'Adorate Deum',
            "ref": 'Psalm 97:7–8; Psalm 97:1',
            "text": (
                'WORSHIP Him, all ye His angels: Zion heard and was glad. The daughters of Judah '
                'rejoiced: because of Thy judgments, O Lord. Psalm. The Lord reigneth, let the earth '
                'rejoice: let the multitude of isles be glad thereof.'
            ),
        },
        "gradual": (
            'SO the heathen shall fear the Name of the Lord: and all the kings of the earth Thy '
            'glory, When the Lord shall build up Zion: He shall appear in His glory. Hallelujah. '
            'Hallelujah. V. The Lord reigneth; let the earth rejoice: let the multitude of isles '
            'be glad thereof. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — epiphany_8'
        ),
    },
    "transfiguration": {
        "collect": (
            'O God, Who in the glorious Transfiguration of Thy Only-begotten Son, hast confirmed '
            'the mysteries of the faith by the testimony of the fathers, and Who, in the voice '
            'that came from the bright cloud, didst in a wonderful manner foreshow the adoption '
            'of sons: Mercifully vouchsafe to make us co-heirs with the King of His glory, and '
            'bring us to the enjoyment of the same; through the same Jesus Christ, Thy Son, our '
            'Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world '
            'without end. Amen.'
        ),
        "introit": {
            "name": 'Illuxerunt',
            "ref": 'Psalm 77:18; Psalm 84:1',
            "text": (
                'THE lightnings lightened the world: the earth trembled and shook. Psalm. How amiable '
                'are Thy tabernacles, O Lord of hosts: My soul longeth, yea, even fainteth for the '
                'courts of the Lord.'
            ),
        },
        "gradual": (
            'THOU art fairer than the children of men: grace is poured into Thy lips. V. The Lord '
            'said unto my Lord. Sit Thou at My right hand: until I make Thine enemies Thy '
            'footstool. Hallelujah. Hallelujah. V. Sing unto the Lord. bless His Name; show forth '
            'His salvation from day to day: Declare His glory among all people. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Transfiguration of Our Lord'
        ),
    },

    # -----------------------------------------------------------------------
    # PRE-LENT
    # -----------------------------------------------------------------------
    "septuagesima": {
        "collect": (
            'O Lord, we beseech Thee favorably to hear the prayers of Thy people: that we, who '
            'are justly punished for our offences, may be mercifully delivered by Thy goodness, '
            'for the glory of Thy Name; through Jesus Christ, Thy Son, our Lord, Who liveth and '
            'reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Circumdederunt Me',
            "ref": 'Psalm 18:4–5; Psalm 18:1–2',
            "text": (
                'THE sorrows of death compassed me: the sorrows of hell compassed me about. In my '
                'distress I called upon the Lord: and He heard my voice out of His temple. Psalm. I '
                'will love Thee, Lord my Strength: The Lord is my Rock and my Fortress.'
            ),
        },
        "gradual": (
            'THE Lord also will be a refuge for the oppressed, a refuge in times of trouble: And '
            'they that know Thy Name will put their trust in Thee; for Thou, Lord, hast not '
            'forsaken them that seek Thee. V. For the needy shall not alway be forgotten: the '
            'expectation of the poor shall not perish forever. Arise, O Lord; let not man '
            'prevail. Tract. Out of the depths have I cried unto Thee, O Lord: Lord, hear my '
            'voice.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Septuagesima'
        ),
    },
    "sexagesima": {
        "collect": (
            'O Lord God, Who seest that we put not our trust in anything that we do: Mercifully '
            'grant that by Thy power we may be defended against all adversity; through Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Exsurge',
            "ref": 'Psalm 44:23–24, 26; Psalm 44:1',
            "text": (
                'AWAKE, why sleepest Thou, O Lord: arise, cast us not off for ever. Wherefore hidest '
                'Thou Thy face: and forgettest our affliction? Our soul is bowed down to the dust: '
                'arise for our help and redeem us. Psalm. We have heard with our ears, O God: our '
                'fathers have told us what work Thou didst in their days.'
            ),
        },
        "gradual": (
            'LET the nations know that Thy Name is Jehovah: A Thou alone art the Most High over '
            'all the earth. My God, make them like a wheel: and like chaff before the wind. '
            'Tract. Thou hast given a banner to them that fear Thee: that it may be displayed '
            'because of the truth.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Sexagesima'
        ),
    },
    "quinquagesima": {
        "collect": (
            'O Lord, we beseech Thee mercifully hear our prayers, and, having set us free from '
            'the bonds of sin, defend us from all evil; through Jesus Christ, Thy Son, our Lord, '
            'Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world without '
            'end. Amen.'
        ),
        "introit": {
            "name": 'Esto Mihi',
            "ref": 'Psalm 31:2–3; Psalm 31:1',
            "text": (
                'BE Thou my strong Rock: for an house of defense to save me. Thou art my Rock and my '
                'Fortress: therefore for Thy Name’s sake lead me and guide me. Psalm. In Thee, O '
                'Lord, do I put my trust; let me never be ashamed: deliver me in Thy righteousness.'
            ),
        },
        "gradual": (
            'THOU art the God that doest wonders: Thou hast declared Thy strength among the '
            'peoples. V. Thou hast with Thine arm redeemed Thy people: the sons of Jacob and '
            'Joseph. Tract. Make a joyful noise unto the Lord, all ye lands: Serve the Lord with '
            'gladness.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Quinquagesima'
        ),
    },

    # -----------------------------------------------------------------------
    # LENT
    # -----------------------------------------------------------------------
    "ash_wednesday": {
        "collect": (
            'Almighty and Everlasting God, Who hatest nothing that Thou hast made, and dost '
            'forgive the sins of all those who are penitent: Create and make in us new and '
            'contrite hearts, that we, worthily lamenting our sins, and acknowledging our '
            'wretchedness, may obtain of Thee, the God of all mercy, perfect remission and '
            'forgiveness; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with '
            'Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Miserere Mihi',
            "ref": 'Psalm 57:1; Psalm 57:1',
            "text": (
                'I WILL cry unto God Most High: unto God that performeth all things for me. Yea, in '
                'the shadow of Thy wings will I make my refuge I until these calamities be overpast. '
                'Psalm. Be merciful unto me, O God, be merciful unto me: for my soul trusteth in '
                'Thee.'
            ),
        },
        "gradual": (
            'BE merciful unto me, God, be merciful unto me: for my soul trusteth in Thee. V. He '
            'shall send from heaven: and save me from the reproach of him that would swallow me '
            'up. Tract. O Lord, deal not with us after our sins; nor reward us according to our '
            'iniquities: Help us, O God of our salvation; for the glory of Thy Name.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Ash Wednesday'
        ),
    },
    "lent_1": {
        "collect": (
            'O Lord, mercifully hear our prayer, and stretch forth the right hand of Thy Majesty '
            'to defend us from them that rise up against us; through Jesus Christ, Thy Son, our '
            'Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world '
            'without end. Amen.'
        ),
        "introit": {
            "name": 'Invocavit',
            "ref": 'Psalm 91:15–16; Psalm 91:1',
            "text": (
                'HE shall call upon Me, and I will answer him: I will deliver him and honor him. With '
                'long life will I satisfy him: and show him My salvation. Psalm. He that dwelleth in '
                'the secret place of the Most High: shall abide under the shadow of the Almighty.'
            ),
        },
        "gradual": (
            'FOR He shall give His angels charge over thee: to keep thee in all thy ways. V. They '
            'shall bear thee up in their hands: lest thou dash thy foot against a stone Tract. He '
            'that dwelleth in the secret place of the Most High: shall abide under the shadow of '
            'the Almighty.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — First Sunday in Lent (Invocabit)'
        ),
    },
    "lent_2": {
        "collect": (
            'O God, Who seest that of ourselves we have no strength: Keep us both outwardly and '
            'inwardly; that we may be defended from all adversities which may happen to the body, '
            'and from all evil thoughts which may assault and hurt the soul; through Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Reminiscere',
            "ref": 'Psalm 25:6–7; Psalm 25:1–2',
            "text": (
                'REMEMBER, O Lord, Thy tender mercies and Thy loving-kindnesses I for they have been '
                'ever of old. Let not mine enemies triumph over me: God of Israel, deliver us out of '
                'all our troubles. Psalm. Unto Thee, O Lord, do I lift up my soul: my God, I trust in '
                'Thee; let me not be ashamed.'
            ),
        },
        "gradual": (
            'THE troubles of my heart are enlarged: bring Thou me out of my distresses. V. Look '
            'upon mine affliction and my pain: and forgive all my sins. Tract. give thanks unto '
            'the Lord; for He is good: for His mercy endureth forever.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Second Sunday in Lent (Reminiscere)'
        ),
    },
    "lent_3": {
        "collect": (
            'We beseech Thee, Almighty God, look upon the hearty desires of Thy humble servants, '
            'and stretch forth the right hand of Thy Majesty to be our defence against all our '
            'enemies; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee '
            'and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Oculi',
            "ref": 'Psalm 25:15–16; Psalm 25:1',
            "text": (
                'MINE eyes are ever toward the Lord: for He shall pluck my feet out of the net. Turn '
                'Thee unto me, and have mercy upon me: for I am desolate and afflicted. Psalm. Unto '
                'Thee, Lord, do I lift up my soul: my God, I trust in Thee; let me not be ashamed.'
            ),
        },
        "gradual": (
            'ARISE, O Lord; let not man prevail: let the heathen be judged in Thy sight, When '
            'mine enemies are turned back: they shall fall and perish at Thy presence. Tract. '
            'Unto Thee lift I up mine eyes, O Thou that dwellest in the heavens: Have mercy upon '
            'us, Lord, have mercy upon us.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Third Sunday in Lent (Oculi)'
        ),
    },
    "lent_4": {
        "collect": (
            'Grant, we beseech Thee, Almighty God, that we, who for our evil deeds do worthily '
            'deserve to be punished, by the comfort of Thy grace may mercifully be relieved; '
            'through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Laetare',
            "ref": 'Isaiah 66:10–11; Psalm 122:1',
            "text": (
                'REJOICE, ye with Jerusalem, and be glad with her: all ye that love her. Rejoice for '
                'joy with her: all ye that mourn for her. Psalm. I was glad when they said unto me: '
                'Let us go into the house of the Lord.'
            ),
        },
        "gradual": (
            'I WAS glad when they said unto me I Let us go into the house of the Lord. V. Peace '
            'be within thy walls: and prosperity within thy palaces. Tract. They that trust in '
            'the Lord shall be as Mount Zion! which cannot be removed, but abideth forever.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fourth Sunday in Lent (Laetare)'
        ),
    },
    "lent_5": {
        "collect": (
            'We beseech Thee, Almighty God, mercifully to look upon Thy people, that by Thy great '
            'goodness they may be governed and preserved evermore, both in body and soul; through '
            'Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy '
            'Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Judica',
            "ref": 'Psalm 43:1–2; Psalm 43:1',
            "text": (
                'JUDGE me, O God: and plead my cause against an ungodly nation. O deliver me from the '
                'deceitful and unjust man: for Thou art the God of my strength. Psalm. send out Thy '
                'light and Thy truth: let them lead me; let them bring me unto Thy holy hill.'
            ),
        },
        "gradual": (
            'DELIVER me, O Lord, from mine enemies: teach me to do Thy will. V. He delivereth me '
            'from mine enemies; yea, Thou liftest me up above those that rise up against me: Thou '
            'hast delivered me from the violent man. Tract. Many a time have they afflicted me '
            'from my youth. V. May Israel now say: Many a time have they afflicted me from my '
            'youth. V. Yet they have not prevailed against me.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fifth Sunday in Lent (Judica)'
        ),
    },

    # -----------------------------------------------------------------------
    # HOLY WEEK
    # -----------------------------------------------------------------------
    "palm_sunday": {
        "collect": (
            'Almighty and Everlasting God, Who hast sent Thy Son, our Saviour Jesus Christ, to '
            'take upon Him our flesh, and to suffer death upon the Cross, that all mankind should '
            'follow the example of His great humility: Mercifully grant that we may both follow '
            'the example of His patience, and also be made partakers of His resurrection; through '
            'the same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Palmarum',
            "ref": 'Psalm 22:19, 21–22; Psalm 22:1',
            "text": (
                'BE not Thou far from me, O Lord: O my Strength, haste Thee to help me. Save me from '
                'the lion’s mouth I and deliver me from the horns of the unicorns. Psalm. My God, my '
                'God, why hast Thou forsaken me: why art Thou so far from helping me?'
            ),
        },
        "gradual": (
            'THOU hast holden me by my right hand: Thou shalt guide me with Thy counsel, and '
            'afterward receive me to glory. V. Truly God is good to Israel: even to such as are '
            'of a clean heart. Tract. My God, my God, why hast Thou forsaken me: why art Thou so '
            'far from helping me? V. Our fathers trusted in Thee: They cried unto Thee and were '
            'delivered.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Sunday of the Passion (Palmarum)'
        ),
    },
    "maundy_thursday": {
        "collect": (
            'O Lord God, Who hast left unto us in a wonderful Sacrament a memorial of Thy '
            'Passion: Grant, we beseech Thee, that we may so use this Sacrament of Thy Body and '
            'Blood, that the fruits of Thy redemption may continually be manifest in us; Who '
            'livest and reignest with the Father and the Holy Ghost, ever One God, world without '
            'end. Amen.'
        ),
        "introit": {
            "name": 'Nos Autem Gloriari',
            "ref": 'Galatians 6:14; Psalm 67:1',
            "text": (
                'GOD forbid that I should glory: save in the Cross of our Lord Jesus Christ. In Him '
                'is salvation, life, and resurrection from the dead: by Him we are redeemed and set '
                'at liberty. Psalm. God be merciful unto us, and bless us: and cause His face to '
                'shine upon us.'
            ),
        },
        "gradual": (
            'CHRIST hath humbled Himself, and become obedient unto death: even the death of the '
            'Cross. V. Wherefore God also hath highly exalted Him: and given Him a Name which is '
            'above every name.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Maundy Thursday'
        ),
    },
    "good_friday": {
        "collect": (
            'Almighty God, we beseech Thee graciously to behold this Thy family, for which our '
            'Lord Jesus Christ was contented to be betrayed, and given up into the hands of '
            'wicked men, and to suffer death upon the Cross; through the same Jesus Christ, Thy '
            'Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, '
            'world without end. Amen.'
        ),
        "introit": {
            "name": 'Popule Meus',
            "ref": 'Isaiah 52:13–53:3; Psalm 102:1',
            "text": (
                'SURELY He hath borne our griefs and carried our sorrows: He was wounded for our '
                'transgressions, He was bruised for our iniquities. All we like sheep have gone '
                'astray: and the Lord hath laid on Him the iniquity of us all. Psalm. Hear my prayer, '
                'O Lord: and let my cry come unto Thee.'
            ),
        },
        "gradual": (
            'HE was wounded for our transgressions, He was bruised for our iniquities: the '
            'chastisement of our peace was upon Him; and with His stripes we are healed. V. He '
            'shall see of the travail of His soul: and shall he satisfied.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Good Friday'
        ),
    },

    # -----------------------------------------------------------------------
    # EASTER SEASON
    # -----------------------------------------------------------------------
    "easter": {
        "collect": (
            'Almighty God, Who, through Thine Only-begotten Son, Jesus Christ, hast overcome '
            'death, and opened unto us the gate of everlasting life: We humbly beseech Thee, '
            'that, as Thou dost put into our minds good desires, so by Thy continual help we may '
            'bring the same to good effect; through Jesus Christ, Thy Son, our Lord, Who liveth '
            'and reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Resurrexi',
            "ref": 'Psalm 139:18, 5–6',
            "text": (
                'WHEN I awake, I am still with Thee. Hallelujah: Thou hast laid Thine hand upon me. '
                'Hallelujah. Such knowledge is too wonderful for me: it is high, I cannot attain unto '
                'it. Hallelujah. Hallelujah. Psalm. O Lord, Thou hast searched me, and known me: Thou '
                'knowest my down-sitting and mine uprising.'
            ),
        },
        "gradual": (
            'THIS is the day which the Lord hath made: we will rejoice and be glad in it. V. O '
            'give thanks unto the Lord for He is good: for His mercy endureth forever. '
            'Hallelujah. Hallelujah. V. Christ our Passover is sacrificed for us. Psalm. Let us '
            'keep the feast: with the unleavened bread of sincerity and truth. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Resurrection of Our Lord (Easter Day)'
        ),
    },
    "easter_2": {
        "collect": (
            'Grant, we beseech Thee, Almighty God, that we who have celebrated the solemnities of '
            "the Lord's Resurrection, may, by the help of Thy grace, bring forth the fruits "
            'thereof in our life and conversation; through the same Jesus Christ, Thy Son, our '
            'Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world '
            'without end. Amen.'
        ),
        "introit": {
            "name": 'Quasimodogeniti',
            "ref": '1 Peter 2:2; Psalm 81:1',
            "text": (
                'AS newborn babes: desire the sincere milk of the Word. Hear, O my people, and I will '
                'testify unto thee: O Israel, if thou wilt hearken unto Me. Psalm. Sing aloud unto '
                'God our strength: make a joyful noise unto the God of Jacob.'
            ),
        },
        "gradual": (
            'HALLELUJAH. Hallelujah. V. The angel of the Lord descended from heaven: and came and '
            'rolled back the stone from the door, and sat upon it. Hallelujah. V. After eight '
            'days when the doors were shut, came Jesus and stood in the midst of His disciples: '
            'and saith unto them, Peace be unto you. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Second Sunday of Easter (Quasimodo Geniti)'
        ),
    },
    "easter_3": {
        "collect": (
            'God, Who, by the humiliation of Thy Son, didst raise up the fallen world: Grant unto '
            'Thy faithful ones perpetual gladness, and those whom Thou hast delivered from the '
            'danger of everlasting death, do Thou make partakers of eternal joys; through the '
            'same Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy '
            'Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Misericordias Domini',
            "ref": 'Psalm 33:5–6; Psalm 33:1',
            "text": (
                'THE earth is full of the goodness of the Lord: By the Word of the Lord were the '
                'heavens made. Psalm. Rejoice in the Lord, O ye righteous: for praise is comely for '
                'the upright.'
            ),
        },
        "gradual": (
            'HALLELUJAH. Hallelujah. V. Then was the Lord Jesus known of the disciples: in the '
            'breaking of bread. Hallelujah. V. I am the Good Shepherd: and know My sheep, and am '
            'known of Mine. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Third Sunday of Easter (Misericordias Domini)'
        ),
    },
    "easter_4": {
        "collect": (
            'Almighty God, Who showest to them that be in error the light of Thy truth, to the '
            'intent that they may return into the way of righteousness: Grant unto all them that '
            "are admitted into the fellowship of Christ's Religion that they may eschew those "
            'things that are contrary to their profession, and follow all such things as are '
            'agreeable to the same; through Jesus Christ, Thy Son, our Lord, Who liveth and '
            'reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Jubilate',
            "ref": 'Psalm 66:1–2; Psalm 66:3',
            "text": (
                'MAKE a joyful noise unto God, all ye lands: sing forth the honor of His Name; make '
                'His praise glorious. Psalm. Say unto God, How terrible art Thou in Thy works: '
                'through the greatness of Thy power shall Thine enemies submit themselves unto Thee.'
            ),
        },
        "gradual": (
            'HALLELUJAH. Hallelujah. V. The Lord hath sent redemption: unto His people. '
            'Hallelujah. V. It behooved Christ to suffer, and to rise from the dead: and thus to '
            'enter into His glory. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fourth Sunday of Easter (Jubilate)'
        ),
    },
    "easter_5": {
        "collect": (
            'O God, Who makest the minds of the faithful to be of one will: Grant unto Thy people '
            'that they may love what Thou commandest, and desire what Thou dost promise: that, '
            'among the manifold changes of this world, our hearts may there be fixed where true '
            'joys are to be found; through Jesus Christ, Thy Son, our Lord, Who liveth and '
            'reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Cantate',
            "ref": 'Psalm 98:1–2; Psalm 98:3',
            "text": (
                'O SING unto the Lord a new song: for He hath done marvelous things. The Lord hath '
                'made known His salvation: His righteousness hath he openly showed in the sight of '
                'the heathen. Psalm. His right hand, and His holy arm: hath gotten Him the victory.'
            ),
        },
        "gradual": (
            'HALLELUJAH. Hallelujah. V. The right hand of the Lord is exalted: The right hand of '
            'the Lord doeth valiantly. Hallelujah. V. Christ, being raised from the dead, dieth '
            'no more I death hath no more dominion over Him. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fifth Sunday of Easter (Cantate)'
        ),
    },
    "easter_6": {
        "collect": (
            'O God, from Whom all good things do come: Grant to us Thy humble servants, that by '
            'Thy holy inspiration we may think those things that be right, and by Thy merciful '
            'guiding may perform the same; through Jesus Christ, Thy Son, our Lord, Who liveth '
            'and reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Vocem Iucunditatis',
            "ref": 'Isaiah 48:20; Psalm 66:1',
            "text": (
                'WITH the voice of singing declare ye, and tell this: utter it even to the end of the '
                'earth. Hallelujah. The Lord hath redeemed His servant Jacob: Hallelujah. Hallelujah. '
                'Psalm. Make a joyful noise unto God, all ye lands: sing forth the honor of His Name; '
                'make His praise glorious.'
            ),
        },
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Sixth Sunday of Easter (Rogate)'
        ),
    },
    "easter_7": {
        "collect": (
            'Almighty, Everlasting God, make us to have always a devout will towards Thee, and to '
            'serve Thy Majesty with a pure heart; through Jesus Christ, Thy Son, our Lord, Who '
            'liveth and reigneth with Thee and the Holy Ghost, ever One God, world without end. '
            'Amen.'
        ),
        "introit": {
            "name": 'Exaudi',
            "ref": 'Psalm 27:7–9; Psalm 27:1',
            "text": (
                'HEAR, O Lord, when I cry with my voice: Hallelujah. When Thou saidst, Seek ye My '
                'face: my heart said unto Thee, Thy face, Lord, will I seek. Hide not Thy face from '
                'me: Hallelujah. Hallelujah. Psalm. The Lord is my Light, and my Salvation: whom '
                'shall I fear?'
            ),
        },
        "gradual": (
            'HALLELUJAH. Hallelujah, V. God reigneth over the heathen: God sitteth upon the '
            'throne of His holiness. Hallelujah. V. I will not leave you comfortless: I go, and I '
            'will come again to you, and your heart shall rejoice. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Seventh Sunday of Easter (Exaudi)'
        ),
    },
    "ascension": {
        "collect": (
            'Grant, we beseech Thee, Almighty God, that like as we do believe Thy Only-begotten '
            'Son, our Lord Jesus Christ, to have ascended into the heavens; so may we also in '
            'heart and mind thither ascend, and with Him continually dwell, Who liveth and '
            'reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Viri Galilaei',
            "ref": 'Acts 1:11; Psalm 47:1',
            "text": (
                'YE men of Galilee, why stand ye gazing up into heaven?: Hallelujah. This same Jesus '
                'which is taken up from you into heaven, shall so come in like manner as ye have seen '
                'Him go into heaven: Hallelujah. Hallelujah. Psalm. O clap your hands, all ye people: '
                'shout unto God with the voice of triumph.'
            ),
        },
        "gradual": (
            'HALLELUJAH. Hallelujah, V. God is gone up with a shout: the Lord with the sound of a '
            'trumpet. Hallelujah. Thou hast ascended on high: Thou hast led captivity captive. '
            'Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Ascension of Our Lord'
        ),
    },
    "pentecost": {
        "collect": (
            'O God, Who didst teach the hearts of Thy faithful people, by sending to them the '
            'light of Thy Holy Spirit: Grant us by the same Spirit to have a right judgment in '
            'all things, and evermore to rejoice in His holy comfort; through Jesus Christ, Thy '
            'Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, '
            'world without end. Amen.'
        ),
        "introit": {
            "name": 'Spiritus Domini',
            "ref": 'Wisdom 1:7; Psalm 68:1',
            "text": (
                'THE Spirit of the Lord filleth the world: Hallelujah. Let the righteous be glad: let '
                'them rejoice before God: yea, let them exceedingly rejoice. Hallelujah. Hallelujah. '
                'Psalm. Let God arise; let His enemies be scattered! let them also that hate Him flee '
                'before Him.'
            ),
        },
        "gradual": (
            'HALLELUJAH. Hallelujah. V. Thou sendest forth Thy Spirit, they are created: and Thou '
            'renewest the face of the earth. Hallelujah. V. Come, Holy Spirit, fill the hearts of '
            'the faithful: and kindle in them the fire of Thy love. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Day of Pentecost'
        ),
    },

    # -----------------------------------------------------------------------
    # TRINITY SEASON
    # -----------------------------------------------------------------------
    "holy_trinity": {
        "collect": (
            'Almighty and Everlasting God, Who hast given unto us, Thy servants, grace, by the '
            'confession of a true faith, to acknowledge the glory of the Eternal Trinity, and in '
            'the power of the Divine Majesty to worship the Unity: We beseech Thee, that Thou '
            'wouldest keep us steadfast in this faith, and evermore defend us from all '
            'adversities; Who livest and reignest, One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Benedicta Sit',
            "ref": 'Tobit 12:6; Psalm 8:1',
            "text": (
                'BLESSED be the Holy Trinity, and the undivided Unity: Let us give glory to Him '
                'because He hath shown His mercy to us. Psalm. O Lord, our Lord: how excellent is Thy '
                'Name in all the earth.'
            ),
        },
        "gradual": (
            'BLESSED art Thou, O Lord, Who beholdest the deep: and Who dwellest between the '
            'cherubim. V. Blessed art Thou, O Lord, in the firmament of heaven: and greatly to be '
            'praised, and glorified, and highly exalted forever. Hallelujah. Hallelujah. V. '
            'Blessed art Thou, O Lord God of our fathers: and greatly to be praised and glorified '
            'forever. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Holy Trinity'
        ),
    },
    "trinity_1": {
        "collect": (
            'O God, the Strength of all them that put their trust in Thee: Mercifully accept our '
            'prayers: and because through the weakness of our mortal nature we can do no good '
            'thing without Thee, grant us the help of Thy grace, that in keeping Thy commandments '
            'we may please Thee, both in will and deed; through Jesus Christ, Thy Son, our Lord, '
            'Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world without '
            'end. Amen.'
        ),
        "introit": {
            "name": 'Domine in Tua Misericordia',
            "ref": 'Psalm 13:5–6; Psalm 13:1',
            "text": (
                'O LORD, I have trusted in Thy mercy: my heart shall rejoice in Thy salvation. I will '
                'sing unto the Lord: because He hath dealt bountifully with me. Psalm. How long wilt '
                'Thou forget me, O Lord: how long wilt Thou hide Thy face from me?'
            ),
        },
        "gradual": (
            'I SAID, Lord, be merciful unto me: heal my soul, for I have sinned against Thee. V. '
            'Blessed is He that considereth the poor I the Lord will deliver him in time of '
            'trouble. Hallelujah. Hallelujah. V. O Lord my God, in Thee do I put my trust: save '
            'me from all them that persecute me, and deliver me. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — First Sunday after Trinity'
        ),
    },
    "trinity_2": {
        "collect": (
            'O Lord, Who never failest to help and govern those whom Thou dost bring up in Thy '
            'steadfast fear and love: Make us to have a perpetual fear and love of Thy holy Name; '
            'through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Factus Est Dominus',
            "ref": 'Psalm 18:18–19; Psalm 18:1',
            "text": (
                'THE Lord was my Stay: He brought me forth also into a large place. He delivered me: '
                'because He delighted in me. Psalm. I will love Thee, Lord, my Strength: The Lord is '
                'my Rock, and my Fortress.'
            ),
        },
        "gradual": (
            'IN my distress I cried unto the Lord: and He heard me. V. Deliver my soul, O Lord, '
            'from lying lips: and from a deceitful tongue. Hallelujah. Hallelujah. V. I will '
            'praise the Lord according to His righteousness: and will sing praise to the Name of '
            'the Lord Most High. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Second Sunday after Trinity'
        ),
    },
    "trinity_3": {
        "collect": (
            'O God, the Protector of all that trust in Thee, without Whom nothing is strong, '
            'nothing is holy: Increase and multiply upon us Thy mercy: that Thou being our Ruler '
            'and Guide, we may so pass through things temporal, that we finally lose not the '
            'things eternal; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth '
            'with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Respice in Me',
            "ref": 'Psalm 25:16, 18; Psalm 25:1',
            "text": (
                'TURN Thee unto me, and have mercy upon me: for I am desolate and afflicted. Look '
                'upon mine affliction and my pain: and forgive all my sins. Psalm. Unto Thee, O Lord, '
                'do I lift up my soul: my God, I trust in Thee, let me not be ashamed.'
            ),
        },
        "gradual": (
            'CAST thy burden upon the Lord: and He shall sustain thee. V. I will call upon God; '
            'and the Lord shall save me: He hath delivered mv soul in peace. Hallelujah. '
            'Hallelujah, V. I will love Thee, O Lord, my Strength: The Lord is my Rock, and my '
            'Fortress, and my Deliverer. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Third Sunday after Trinity'
        ),
    },
    "trinity_4": {
        "collect": (
            'Grant, Lord, we beseech Thee, that the course of this world may be so peaceably '
            'ordered by Thy governance, that Thy Church may joyfully serve Thee in all godly '
            'quietness; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with '
            'Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Dominus Illuminatio',
            "ref": 'Psalm 27:1, 3; Psalm 27:4',
            "text": (
                'THE Lord is my Light and my Salvation; whom shall I fear: The Lord is the strength '
                'of my life; of whom shall I be afraid? When the wicked, even mine enemies and my '
                'foes, came upon me: they stumbled and fell. Psalm. Though an host should encamp '
                'against me: my heart shall not fear.'
            ),
        },
        "gradual": (
            'FORGIVE our sins, O Lord: lest the heathen say, Where is their God? V. Help us, O '
            'God of our salvation: and for the glory of Thy Name, deliver us. Hallelujah. '
            'Hallelujah. V. The king shall joy in Thy strength, O Lord and in Thy salvation how '
            'greatly shall he rejoice! Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fourth Sunday after Trinity'
        ),
    },
    "trinity_5": {
        "collect": (
            "O God, Who hast prepared for them that love Thee such good things as pass man's "
            'understanding: Pour into our hearts such love toward Thee, that we, loving Thee '
            'above all things, may obtain Thy promises, which exceed all that we can desire; '
            'through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Exaudi Domine',
            "ref": 'Psalm 27:7–8; Psalm 27:1',
            "text": (
                'HEAR, O Lord, when I cry with my voice: Thou hast been my help. Leave me not, '
                'neither forsake me: God of my Salvation. Psalm. The Lord is my Light and my '
                'Salvation: whom shall I fear?'
            ),
        },
        "gradual": (
            'BEHOLD, God, our Shield: and look upon Thy servants. V. O Lord God of hosts: hear '
            'our prayer. Hallelujah. Hallelujah. V. In Thee, O Lord, do I put my trust ; let me '
            'never be ashamed: deliver me in Thy righteousness. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fifth Sunday after Trinity'
        ),
    },
    "trinity_6": {
        "collect": (
            'Lord of all power and might, Who art the Author and Giver of all good things: Graft '
            'in our hearts the love of Thy Name, increase in us true religion, nourish us with '
            'all goodness, and of Thy great mercy keep us in the same; through Jesus Christ, Thy '
            'Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, '
            'world without end. Amen.'
        ),
        "introit": {
            "name": 'Dominus Fortitudo',
            "ref": 'Psalm 28:8–9; Psalm 28:1',
            "text": (
                'THE Lord is the strength of His people: He is the saving strength of His anointed. '
                'Save Thy people, and bless Thine inheritance: feed them also, and lift them up '
                'forever. Psalm. Unto Thee will I cry, O Lord, my Rock; be not silent unto me: lest '
                'if Thou be silent to me, I become like them that go down into the pit.'
            ),
        },
        "gradual": (
            'RETURN, O Lord, how long: and let it repent Thee concerning Thy servants. V. Lord, '
            'Thou hast been our dwelling place: in all generations. Hallelujah. Hallelujah. V. O '
            'clap your hands, all ye people: shout unto God with the voice of triumph. '
            'Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Sixth Sunday after Trinity'
        ),
    },
    "trinity_7": {
        "collect": (
            'O God, Whose never-failing Providence ordereth all things both in heaven and earth: '
            'We humbly beseech Thee to put away from us all hurtful things, and to give us those '
            'things which be profitable for us; through Jesus Christ, Thy Son, our Lord, Who '
            'liveth and reigneth with Thee and the Holy Ghost, ever One God, world without end. '
            'Amen.'
        ),
        "introit": {
            "name": 'Omnes Gentes',
            "ref": 'Psalm 47:1–2; Psalm 47:3',
            "text": (
                'O CLAP your hands: all ye people. Shout unto God: with the voice of triumph. Psalm. '
                'He shall subdue the people under us: and the nations under our feet.'
            ),
        },
        "gradual": (
            'COME, ye children, hearken unto me: I will teach you the fear of the Lord. V. Look '
            'unto Him and be lightened: and let your faces not be ashamed. Hallelujah. '
            'Hallelujah. V. Deliver me from mine enemies, my God: defend me from them that rise '
            'up against me. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Seventh Sunday after Trinity'
        ),
    },
    "trinity_8": {
        "collect": (
            'Grant to us, Lord, we beseech Thee, the Spirit to think and do always such things as '
            'are right; that we, who cannot do anything that is good without Thee, may by Thee be '
            'enabled to live according to Thy will; through Jesus Christ, Thy Son, our Lord, Who '
            'liveth and reigneth with Thee and the Holy Ghost, ever One God, world without end. '
            'Amen.'
        ),
        "introit": {
            "name": 'Suscepimus Deus',
            "ref": 'Psalm 48:9–10; Psalm 48:1',
            "text": (
                'WE have thought of Thy loving-kindness, O God: in the midst of Thy Temple. According '
                'to Thy Name, O God, so is Thy praise unto the ends of the earth: Thy right hand is '
                'full of righteousness. Psalm. Great is the Lord, and greatly to be praised: in the '
                'city of our God, in the mountain of His holiness.'
            ),
        },
        "gradual": (
            'BE Thou my strong Rock: for an house of defence to save me. V. In Thee, O Lord, do I '
            'put my trust: let me never be ashamed. Hallelujah. Hallelujah. V. The Lord knoweth '
            'the way of the righteous: but the way of the ungodly shall perish. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Eighth Sunday after Trinity'
        ),
    },
    "trinity_9": {
        "collect": (
            'Let Thy merciful ears, O Lord, be open to the prayers of Thy humble servants: and, '
            'that they may obtain their petitions, make them to ask such things as shall please '
            'Thee; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and '
            'the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Dum Clamarem',
            "ref": 'Psalm 54:2–3; Psalm 54:1',
            "text": (
                'BEHOLD, God is mine Helper: the Lord is with them that uphold my soul. He shall '
                'reward evil unto mine enemies: cut them off in Thy truth, O Lord. Psalm. Save me, O '
                'God, by Thy Name: and judge me by Thy strength.'
            ),
        },
        "gradual": (
            'OLORD, our Lord, how excellent is Thy Name in all the earth: Who hast set Thy glory '
            'above the heavens. Hallelujah. Hallelujah. V. Give ear, O My people, to My law: '
            'incline your ears to the words of My mouth. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Ninth Sunday after Trinity'
        ),
    },
    "trinity_10": {
        "collect": (
            'O God, Who declarest Thine almighty power chiefly in showing mercy and pity: '
            'Mercifully grant unto us such a measure of Thy grace, that we, running the way of '
            'Thy commandments, may obtain Thy gracious promises, and be made partakers of Thy '
            'heavenly treasure; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth '
            'with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Dum Clamarem',
            "ref": 'Psalm 55:16–17; Psalm 55:1',
            "text": (
                'AS for me, I will call upon God, and He shall hear my voice: He hath delivered my '
                'soul in peace from the battle that was against me. God shall hear and afflict them, '
                'even He that abideth of old: Cast thy burden upon the Lord, and He shall sustain '
                'thee. Psalm. Give ear to my prayer, O God: and hide not Thyself from my '
                'supplication.'
            ),
        },
        "gradual": (
            'KEEP me, Lord, as the apple of the eye: hide me under the shadow of Thy wings. V. '
            'Let my sentence come forth from Thy presence: let Thine eyes behold the things that '
            'are equal. Hallelujah. Hallelujah. V. Deliver me from mine enemies, my God I defend '
            'me from them that rise up against me. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Tenth Sunday after Trinity'
        ),
    },
    "trinity_11": {
        "collect": (
            'Almighty and Everlasting God, Who art always more ready to hear than we to pray, and '
            'art wont to give more than either we desire or deserve: Pour down upon us the '
            'abundance of Thy mercy, forgiving us those things whereof our conscience is afraid, '
            'and giving us those good things which we are not worthy to ask, but through the '
            'merits and mediation of Jesus Christ, Thy Son, our Lord, Who liveth and reigneth '
            'with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Deus in Loco Sancto',
            "ref": 'Psalm 68:5–6; Psalm 68:1',
            "text": (
                'GOD is in His holy habitation: He is God Who setteth the solitary in families. The '
                'God of Israel is He that giveth strength: and power unto His people. Psalm. Let God '
                'arise, let His enemies be scattered: let them also that hate Him flee before Him.'
            ),
        },
        "gradual": (
            'MY heart trusteth in God, and I am helped: therefore my heart greatly rejoiceth; and '
            'with my song will I praise Him. V. Unto Thee will I cry, O Lord my Rock: be not '
            'silent to me. Hear the voice of my supplications. Hallelujah. Hallelujah. V. Praise '
            'waiteth for Thee, God, in Sion: and unto Thee shall the vow be performed. '
            'Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Eleventh Sunday after Trinity'
        ),
    },
    "trinity_12": {
        "collect": (
            'Almighty and Merciful God, of Whose only gift it cometh that Thy faithful people do '
            'unto Thee true and laudable service: Grant, we beseech Thee, that we may so '
            'faithfully serve Thee in this life, that we fail not finally to attain Thy heavenly '
            'promises; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee '
            'and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Deus in Adiutorium',
            "ref": 'Psalm 70:1–2; Psalm 70:4',
            "text": (
                'MAKE haste, O God, to deliver me: make haste to help me, O Lord. Let them be ashamed '
                'and confounded: that seek after my soul. Psalm. Let them be turned backward, and put '
                'to confusion that desire my hurt.'
            ),
        },
        "gradual": (
            'I WILL bless the Lord at all times: His praise shall continually be in my mouth. V. '
            'My soul shall make her boast in the Lord I the humble shall hear thereof and be '
            'glad. Hallelujah. Hallelujah. V. Sing aloud unto God our Strength: make a joyful '
            'noise unto the God of Jacob. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Twelfth Sunday after Trinity'
        ),
    },
    "trinity_13": {
        "collect": (
            'Almighty and Everlasting God, give unto us the increase of faith, hope, and charity; '
            'and that we may obtain that which Thou dost promise, make us to love that which Thou '
            'dost command; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with '
            'Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Respice Domine',
            "ref": 'Psalm 74:20, 19, 23; Psalm 74:1',
            "text": (
                'HAVE respect, O Lord, unto Thy covenant: O let not the oppressed return ashamed. '
                'Arise, O God, plead Thine own cause: And forget not the voice of Thine enemies. '
                'Psalm. O God, why hast Thou cast us off forever I why doth Thine anger smoke against '
                'the sheep of Thy pasture?'
            ),
        },
        "gradual": (
            'HAVE respect, O Lord, unto Thy covenant: O let not the oppressed return ashamed, V. '
            'Arise, O God, plead Thine own cause: And forget not the voice of Thine enemies. '
            'Hallelujah. Hallelujah. V. O Lord God of my salvation: I have cried day and night '
            'before Thee. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Thirteenth Sunday after Trinity'
        ),
    },
    "trinity_14": {
        "collect": (
            'Keep, we beseech Thee, O Lord, Thy Church with Thy perpetual mercy; and, because the '
            'frailty of man without Thee cannot but fall, keep us ever by Thy help from all '
            'things hurtful, and lead us to all things profitable to our salvation; through Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Protector Noster',
            "ref": 'Psalm 84:9–10; Psalm 84:1',
            "text": (
                'BEHOLD, O God our Shield: and look upon the face of Thine Anointed; For a day in Thy '
                'courts: is better than a thousand. Psalm. How amiable are Thy tabernacles, O Lord of '
                'Hosts: My soul longeth, yea, even fainteth for the courts of the Lord.'
            ),
        },
        "gradual": (
            'IT is better to trust in the Lord: than to put confidence in man. V. It is better to '
            'trust in the Lord: than to put confidence in princes. Hallelujah. Hallelujah. V. '
            'Lord Thou hast been our dwelling place: in all generations. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fourteenth Sunday after Trinity'
        ),
    },
    "trinity_15": {
        "collect": (
            'O Lord, we beseech Thee, let Thy continual pity cleanse and defend Thy Church: and '
            'because it cannot continue in safety without Thy succor, preserve it evermore by Thy '
            'help and goodness; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth '
            'with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Inclina Domine',
            "ref": 'Psalm 86:1–3; Psalm 86:6',
            "text": (
                'BOW down Thine ear, O Lord, hear me: O Thou, my God, save Thy servant that trusteth '
                'in Thee. Be merciful unto me, O Lord: for I cry unto Thee daily. Psalm. Rejoice the '
                'soul of Thy servant: for unto Thee, Lord, do I lift up my soul.'
            ),
        },
        "gradual": (
            'IT is a good thing to give thanks unto the Lord: and to sing praises unto Thy Name, '
            'O Most High. V. To show forth Thy lovingkindness in the morning: and Thy '
            'faithfulness every night. Hallelujah. Hallelujah. V. O God, my heart is fixed: I '
            'will sing and give praise, ever with my glory. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Fifteenth Sunday after Trinity'
        ),
    },
    "trinity_16": {
        "collect": (
            'Lord, we pray Thee, that Thy grace may always go before and follow after us, and '
            'make us continually to be given to all good works; through Jesus Christ, Thy Son, '
            'our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world '
            'without end. Amen.'
        ),
        "introit": {
            "name": 'Miserere Mihi Domine',
            "ref": 'Psalm 86:3, 5; Psalm 86:1',
            "text": (
                'BE merciful unto me, O Lord: for I cry unto Thee daily. For Thou, Lord, art good, '
                'and ready to forgive: and plenteous in mercy unto all them that call upon Thee. '
                'Psalm. Bow down Thine ear, O Lord, hear me: for I am poor and needy.'
            ),
        },
        "gradual": (
            'THE heathen shall fear the Name of the Lord: and all the kings of the earth Thy '
            'glory. V. When the Lord shall build up Zion: He shall appear in His glory. '
            'Hallelujah. Hallelujah. V. O sing unto the Lord a new song: for He hath done '
            'marvelous things. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Sixteenth Sunday after Trinity'
        ),
    },
    "trinity_17": {
        "collect": (
            'Lord, we beseech Thee, grant Thy people grace, to withstand the temptations of the '
            'devil, and with pure hearts and minds to follow Thee, the only God; through Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Iustus Es Domine',
            "ref": 'Psalm 119:137–138; Psalm 119:1',
            "text": (
                'RIGHTEOUS art Thou, O Lord: and upright are Thy judgments. Deal with Thy servant: '
                'according to Thy mercy. Psalm. Blessed are the undefiled in the way: who walk in the '
                'law of the Lord.'
            ),
        },
        "gradual": (
            'BLESSED is the nation whose God is the Lord: and the people whom He hath chosen for '
            'His own inheritance. V. By the Word of the Lord were the heavens made: and all the '
            'host of them by the breath of His month. Hallelujah. Hallelujah. V. I love the Lord: '
            'because He hath heard my voice and my supplications. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Seventeenth Sunday after Trinity'
        ),
    },
    "trinity_18": {
        "collect": (
            'O God, forasmuch as without Thee we are not able to please Thee: Mercifully grant, '
            'that Thy Holy Spirit may in all things direct and rule our hearts; through Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Da Pacem Domine',
            "ref": 'Psalm 122:6–7; Psalm 122:1',
            "text": (
                'REWARD them that wait for Thee, O Lord let Thy prophets be found faithful. Hear the '
                'prayer of Thy servants: and of Thy people Israel. Psalm. I was glad when they said '
                'unto me: Let us go into the house of the Lord.'
            ),
        },
        "gradual": (
            'I WAS glad when they said unto me: Let us go into the house of the Lord. V. Peace be '
            'within thy walls: and prosperity within thy palaces. Hallelujah. Hallelujah. V. O '
            'praise the Lord, all ye nations: praise Him, all ye people. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Eighteenth Sunday after Trinity'
        ),
    },
    "trinity_19": {
        "collect": (
            'O Almighty and most Merciful God, of Thy bountiful goodness keep us, we beseech '
            'Thee, from all things that may hurt us; that we, being ready, both in body and soul, '
            'may cheerfully accomplish those things that Thou wouldest have done; through Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Salus Populi',
            "ref": 'Psalm 38:22–23; Psalm 38:1',
            "text": (
                'SAY unto my soul, I am thy salvation: The righteous cry, and the Lord heareth. He '
                'delivereth them out of all their troubles: He is their God forever and ever. Psalm. '
                'Give ear, O My people, to My law: incline your ears to the words of My mouth.'
            ),
        },
        "gradual": (
            'LET my prayer be set forth before Thee as incense: and the lifting up of my hands as '
            'the evening sacrifice. Hallelujah. Hallelujah, V. The right hand of the Lord is '
            'exalted: the right hand of the Lord doeth valiantly. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Nineteenth Sunday after Trinity'
        ),
    },
    "trinity_20": {
        "collect": (
            'Grant, we beseech Thee, Merciful Lord, to Thy faithful people pardon and peace, that '
            'they may be cleansed from all their sins, and serve Thee with a quiet mind; through '
            'Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy '
            'Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Omnia Quae Fecisti',
            "ref": 'Psalm 48:9; Psalm 48:1',
            "text": (
                'THE Lord our God is righteous in all His works which He doeth: for we obeyed not His '
                'voice. Give glory to Thy Name. O Lord: and deal with us according to the multitude '
                'of Thy mercies. Psalm. Great is the Lord, and greatly to be praised: in the city of '
                'our God, in the mountain of His holiness.'
            ),
        },
        "gradual": (
            'THE eyes of all wait upon Thee, O Lord: and Thou givest them their meat in due '
            'season. V. Thou openest Thine hand: and satisfiest the desire of every living thing. '
            'Hallelujah. Hallelujah. V. O give thanks unto the Lord; call upon His Name: make '
            'known His deeds among the people. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Twentieth Sunday after Trinity'
        ),
    },
    "trinity_21": {
        "collect": (
            'Lord, we beseech Thee to keep Thy household, the Church, in continual godliness; '
            'that through Thy protection it may be free from all adversities, and devoutly given '
            'to serve Thee in good works, to the glory of Thy Name; through Jesus Christ, Thy '
            'Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, '
            'world without end. Amen.'
        ),
        "introit": {
            "name": 'In Voluntate Tua',
            "ref": 'Esther 13:9–10; Psalm 119:1',
            "text": (
                'THE whole world is in Thy power, O Lord, King Almighty: there is no man that can '
                'gainsay Thee. For Thou hast made heaven and earth, and all the wondrous things under '
                'the heaven: Thou art Lord of all. Psalm. Blessed are the undefiled in the way: who '
                'walk in the law of the Lord.'
            ),
        },
        "gradual": (
            'LORD, Thou hast been our dwelling place: in all generations. V. Before the mountains '
            'were brought forth or ever Thou hadst formed the earth and the world: even from '
            'everlasting to everlasting, Thou art God. Hallelujah. Hallelujah. V. They that trust '
            'in the Lord shall be as Mount Zion: which cannot be removed, but abideth forever. '
            'Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Twenty-first Sunday after Trinity'
        ),
    },
    "trinity_22": {
        "collect": (
            'O God, our Refuge and Strength, Who art the Author of all godliness: Be ready, we '
            'beseech Thee, to hear the devout prayers of Thy Church; and grant that those things '
            'which we ask faithfully, we may obtain effectually; through Jesus Christ, Thy Son, '
            'our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world '
            'without end. Amen.'
        ),
        "introit": {
            "name": 'Si Iniquitates',
            "ref": 'Psalm 130:3–4; Psalm 130:1',
            "text": (
                'IF Thou, Lord, shouldest mark iniquities: O Lord, who shall stand? But there is '
                'forgiveness with Thee: that Thou mayest be feared, O God of Israel. Psalm. Out of '
                'the depths have I cried unto Thee, O Lord: Lord, hear my voice.'
            ),
        },
        "gradual": (
            'BEHOLD how good and how pleasant it is: for brethren to dwell together in unity! V. '
            'The Lord commanded blessing: even life for evermore. Hallelujah. Hallelujah. V. '
            'Praise the Lord, O my soul. While I live will I praise the Lord: I will sing praises '
            'unto my God. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Twenty-second Sunday after Trinity'
        ),
    },
    "trinity_23": {
        "collect": (
            'Absolve, we beseech Thee, O Lord, Thy people from their offences; that from the '
            'bonds of our sins which, by reason of our frailty, we have brought upon us, we may '
            'be delivered by Thy bountiful goodness; through Jesus Christ, Thy Son, our Lord, Who '
            'liveth and reigneth with Thee and the Holy Ghost, ever One God, world without end. '
            'Amen.'
        ),
        "introit": {
            "name": 'Dicit Dominus',
            "ref": 'Jeremiah 29:11, 12, 14; Psalm 85:1',
            "text": (
                'I KNOW the thoughts that I think toward you, saith the Lord: thoughts of peace, and '
                'not of evil. Then shall ye call upon Me, and pray unto Me, and I will hearken unto '
                'you: and I will turn your captivity, and gather you from all nations and from all '
                'places. Psalm. Lord, Thou hast been favorable unto Thy land: Thou hast brought back '
                'the captivity of Jacob.'
            ),
        },
        "gradual": (
            'THOU hast saved us from our enemies: and hast put them to shame that hated us. V. In '
            'God we boast all the day long: and praise Thy Name forever. Hallelujah. Hallelujah. '
            'V. Ye that fear the Lord, trust in the Lord: He is their Help and their Shield. '
            'Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Twenty-third Sunday after Trinity'
        ),
    },
    "trinity_24": {
        "collect": (
            'Stir up, we beseech Thee, O Lord, the wills of Thy faithful people; that they, '
            'plenteously bringing forth the fruit of good works, may of Thee be plenteously '
            'rewarded; through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee '
            'and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Dicit Dominus',
            "ref": 'Psalm 95:6–7; Psalm 95:1',
            "text": (
                'O COME, let us worship and bow down I let us kneel before the Lord our Maker. For He '
                'is our God: and we are the people of His pasture, and the sheep of His hand. Psalm. '
                'O come, let us sing unto the Lord: let us make a joyful noise to the Rock of our '
                'salvation.'
            ),
        },
        "gradual": (
            'BLESSED is the man: that walketh not in the counsel of the ungodly. V. His delight '
            'is in the law of the Lord: and in His law doth he meditate day and night. '
            'Hallelujah. Hallelujah, V. He shall call upon Me and I will answer him: with long '
            'life will I satisfy him and show him My salvation. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Twenty-fourth Sunday after Trinity'
        ),
    },
    "trinity_25": {
        "collect": (
            'Almighty God, we beseech Thee, show Thy mercy unto Thy humble servants, that we who '
            'put no trust in our own merits may not be dealt with after the severity of Thy '
            'judgment, but according to Thy mercy; through Jesus Christ, Thy Son, our Lord, Who '
            'liveth and reigneth with Thee and the Holy Ghost, ever One God, world without end. '
            'Amen.'
        ),
        "introit": {
            "name": 'Dicit Dominus',
            "ref": 'Psalm 31:9–10; Psalm 31:1',
            "text": (
                'HAVE mercy upon me, O Lord, for I am in trouble: deliver me from the hand of mine '
                'enemies, and from them that persecute me. Let me not be ashamed, O Lord I for I have '
                'called upon Thee. Psalm. In Thee, O Lord, do I put my trust: let me never be '
                'ashamed.'
            ),
        },
        "gradual": (
            'I WILL say of the Lord, He is my Refuge and my Fortress: my God, in Him will I '
            'trust, V. His truth: shall be thy shield and buckler. Hallelujah. Hallelujah. V. He '
            'that dwelleth in the secret place of the Most High: shall abide under the shadow of '
            'the Almighty. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Twenty-fifth Sunday after Trinity'
        ),
    },
    "trinity_26": {
        "collect": (
            'God, so rule and govern our hearts and minds by Thy Holy Spirit, that being ever '
            'mindful of the end of all things, and the day of Thy just judgment, we may be '
            'stirred up to holiness of living here, and dwell with Thee forever hereafter; '
            'through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Ego Autem',
            "ref": 'Psalm 54:4–5; Psalm 54:1',
            "text": (
                'SAVE me, O God, by Thy Name: and judge me by Thy strength. Hear my prayer, O God: '
                'give ear to the words of my mouth. Psalm. He shall reward evil to mine enemies I cut '
                'them off in Thy truth.'
            ),
        },
        "gradual": (
            'WHO shall ascend into the hill of the Lord: or who shall stand in His holy place? V. '
            'He that hath clean hands and a pure heart: He shall receive the blessing from the '
            'Lord. Hallelujah. Hallelujah. V. Fear not, for I have redeemed thee: I have called '
            'thee by thy name; thou art Mine. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Twenty-sixth Sunday after Trinity'
        ),
    },
    "trinity_27": {
        "collect": (
            'Absolve, we beseech Thee, O Lord, Thy people from their offences; that from the '
            'bonds of our sins which, by reason of our frailty, we have brought upon us, we may '
            'be delivered by Thy bountiful goodness; through Jesus Christ, Thy Son, our Lord, Who '
            'liveth and reigneth with Thee and the Holy Ghost, ever One God, world without end. '
            'Amen.'
        ),
        "introit": {
            "name": 'Ego Autem',
            "ref": 'Psalm 54:4–5; Psalm 54:1',
            "text": (
                'I AM Alpha and Omega, the beginning and the ending: which is, and which was, and '
                'which is to come, the Almighty. Behold, the tabernacle of God is with men, and He '
                'will dwell with them: and they shall be His people, and God Himself shall be with '
                'them, and be their God. Psalm. Lift up your heads, O ye gates; and be ye lift up, ye '
                'everlasting doors: and the King of Glory shall come in.'
            ),
        },
        "gradual": (
            'I AM the Light of the world: he that followeth Me shall not walk in darkness, but '
            'shall have the light of life. V. The Spirit and the bride say, Come, and let him '
            'that heareth say, Come land let him that is athirst come. Hallelujah. Hallelujah. V. '
            'Even so, come: Lord Jesus. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — trinity_27'
        ),
    },
    "last_sunday": {
        "collect": (
            'Absolve, we beseech Thee, O Lord, Thy people from their offences; that from the '
            'bonds of our sins which, by reason of our frailty, we have brought upon us, we may '
            'be delivered by Thy bountiful goodness; through Jesus Christ, Thy Son, our Lord, Who '
            'liveth and reigneth with Thee and the Holy Ghost, ever One God, world without end. '
            'Amen.'
        ),
        "introit": {
            "name": 'Ego Sum Alpha et Omega',
            "ref": 'Revelation 1:8; Psalm 24:7',
            "text": (
                'I AM Alpha and Omega, the beginning and the ending: which is, and which was, and '
                'which is to come, the Almighty. Behold, the tabernacle of God is with men, and He '
                'will dwell with them: and they shall be His people, and God Himself shall be with '
                'them, and be their God. Psalm. Lift up your heads, O ye gates; and be ye lift up, ye '
                'everlasting doors: and the King of Glory shall come in.'
            ),
        },
        "gradual": (
            'I AM the Light of the world: he that followeth Me shall not walk in darkness, but '
            'shall have the light of life. V. The Spirit and the bride say, Come, and let him '
            'that heareth say, Come land let him that is athirst come. Hallelujah. Hallelujah. V. '
            'Even so, come: Lord Jesus. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Last Sunday of the Church Year'
        ),
    },

    # -----------------------------------------------------------------------
    # PRINCIPAL FEASTS
    # -----------------------------------------------------------------------
    "reformation": {
        "collect": (
            'O Lord God, Heavenly Father, pour out, we beseech Thee, Thy Holy Spirit upon Thy '
            'faithful people, keep them steadfast in Thy grace and truth, protect and comfort '
            'them in all temptation, defend them against all enemies of Thy Word, and bestow upon '
            "Christ's Church militant Thy saving peace; through the same Jesus Christ, Thy Son, "
            'our Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world '
            'without end. Amen.'
        ),
        "introit": {
            "name": 'Dominus Fortitudo Plebis',
            "ref": 'Psalm 46:7, 4; Psalm 46:1',
            "text": (
                'THE Lord of Hosts is with us: the God of Jacob is our Refuge. Therefore will not we '
                'fear, though the earth be removed: and though the mountains be carried into the '
                'midst of the sea. Psalm. God is our Refuge and Strength: a very present help in '
                'trouble.'
            ),
        },
        "gradual": (
            'GREAT is the Lord, and greatly to be praised: in the city of our God, in the '
            'mountain of His holiness. V. Walk about Zion; tell the towers thereof. Mark well her '
            'bulwarks, consider her palaces: that ye may tell it to the generation following. '
            'Hallelujah. Hallelujah. V. For this God is our God for ever and ever: He will be our '
            'guide even unto death. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Reformation Day'
        ),
    },
    "all_saints": {
        "collect": (
            'O Almighty God, Who hast knit together Thine elect in one communion and fellowship '
            'in the mystical Body of Thy Son, Christ our Lord: Grant us grace so to follow Thy '
            'blessed Saints in all virtuous and godly living, that we may come to those '
            'unspeakable joys which Thou hast prepared for those who unfeignedly love Thee; '
            'through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Gaudeamus',
            "ref": 'Revelation 7:14, 17; Psalm 33:1',
            "text": (
                'THESE are they which have come out of great tribulation: and have washed their robes '
                'and made them white in the Blood of the Lamb. Therefore are they before the Throne '
                'of God: and serve Him day and night in His Temple. Psalm. Rejoice in the Lord, O ye '
                'righteous: for praise is comely for the upright.'
            ),
        },
        "gradual": (
            'O FEAR the Lord, ye His saints: for there is no want to them that fear Him. V. They '
            'that seek the Lord ; shall not want any good thing. Hallelujah. Hallelujah. V. Come '
            'unto Me, all ye that labor and are heavy laden: and I will give you rest. '
            'Hallelujah. THE eyes of all wait upon Thee: and Thou givest them their meat in due '
            'season. V. Thou openest Thine hand: and satisfiest the desire of every living thing. '
            'Hallelujah. Hallelujah. V. Bless the Lord, O my soul, and all that is within me, '
            'bless His holy Name: Bless the Lord, O my soul, and forget not all His benefits. '
            'Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            "Epistles, Graduals and Gospels — All Saints' Day"
        ),
    },
    "st_michael": {
        "collect": (
            'O Everlasting God, Who hast ordained and constituted the services of angels and men '
            'in a wonderful order: Mercifully grant, that as Thy holy angels always do Thee '
            'service in Heaven, so by Thy appointment they may succor and defend us on earth; '
            'through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit": {
            "name": 'Benedicite Dominum',
            "ref": 'Psalm 103:20–21; Psalm 103:1',
            "text": (
                'BLESS the Lord, ye His angels, that excel in strength: that do His commandments, '
                'hearkening unto the voice of His word. Bless ye the Lord, all ye His hosts: ye '
                'ministers of His that do His pleasure. Psalm. Bless the Lord, my soul I and all that '
                'is within me bless His holy Name.'
            ),
        },
        "gradual": (
            'BLESS the Lord, ye His angels, that excel in strength: that do His commandments, '
            'hearkening unto the voice of His word. V. God hath given His angels charge over '
            'thee: to keep thee in all thy ways. Hallelujah. Hallelujah. V. Bless the Lord, O my '
            'soul: and all that is within me, bless His holy Name. Hallelujah. V. And one cried '
            'unto another, and said: Holy, Holy, Holy, is the Lord of Hosts: the whole earth is '
            'full of His glory. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Michael and All Angels'
        ),
    },
    "thanksgiving": {
        "collect": (
            'Almighty God, our Heavenly Father, Whose mercies are new unto us every morning, and '
            'Who, though we have in no wise deserved Thy goodness, dost abundantly provide for '
            'all our wants of body and soul: Give us, we pray Thee, Thy Holy Spirit, that we may '
            'heartily acknowledge Thy merciful goodness toward us, give thanks for all Thy '
            'benefits, and serve Thee in willing obedience; through Jesus Christ, Thy Son, our '
            'Lord, Who liveth and reigneth with Thee and the Holy Ghost, ever One God, world '
            'without end. Amen.'
        ),
        "introit": {
            "name": 'Laudate Dominum',
            "ref": 'Psalm 150:6, 2; Psalm 150:1',
            "text": (
                'LET every thing that hath breath praise the Lord: Praise ye the Lord. Praise Him for '
                'His mighty acts: praise Him according to His excellent greatness. Psalm. Praise ye '
                'the Lord. Praise God in His sanctuary: praise Him in the firmament of His power.'
            ),
        },
        "gradual": (
            'THE eyes of all wait upon Thee: and Thou givest them their meat in due season. V. '
            'Thou openest Thine hand: and satisfiest the desire of every living thing. '
            'Hallelujah. Hallelujah. V. Bless the Lord, O my soul, and all that is within me, '
            'bless His holy Name: Bless the Lord, O my soul, and forget not all His benefits. '
            'Hallelujah. LESSONS. Deuteronomy 8:1-20. Isaiah 26:1-12. 1 Timothy 2:1-8'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — Day of Thanksgiving'
        ),
    },

}
