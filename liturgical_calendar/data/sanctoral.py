"""
LCMS Sanctoral Calendar — Principal and Minor Feasts.

Fixed-date observances that may coincide with or displace Sundays.
Readings are per the Lutheran Service Book (LSB).

Collects, introit antiphons (antiphon + psalm verse; Gloria Patri omitted), and
graduals are from the *Common Service Book of the Lutheran Church* (Philadelphia,
1917), public domain. Apostles and Evangelists without a proper collect use the
respective CSB "common" (Apostles' Days / Evangelists' Days). Feasts not present
in CSB 1917 (Holy Innocents, Confession of St. Peter, St. Barnabas, St. Mary
Magdalene) carry readings only.
"""


def _r(ot=None, ps=None, ep=None, go=None):
    return {"ot": ot, "ps": ps, "ep": ep, "go": go}


# Key: slot name used in calculator.py / date_to_slot()
SANCTORAL_SLOTS = {
    "st_andrew": {
        "name": 'St. Andrew, Apostle',
        "date_str": 'Nov 30',
        "season": 'Pentecost',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Ezekiel 3:16-21', ps='Psalm 19:1-6', ep='Romans 10:10-18', go='John 1:35-42a'),
        "collect": (
            'O ALMIGHTY God, Whom to know is everlasting life: Grant us perfectly to know Thy Son '
            'Jesus Christ to be the Way, the Truth, and the Life; that following His steps we may '
            'steadfastly walk in the way that leadeth to eternal life; through the same Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'I KNOW Whom I have believed: and am persuaded that He is able to keep that which I '
            'have committed unto Him against that day. There is laid up for me a crown of '
            'righteousness: which the Lord, the righteous Judge, shall give me. Psalm. O Lord, '
            'Thou hast searched me and known me: Thou knowest my downsitting and mine uprising.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Andrew, Apostle'
        ),
    },
    "st_thomas": {
        "name": 'St. Thomas, Apostle',
        "date_str": 'Dec 21',
        "season": 'Christmas',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Judges 6:36-40', ps='Psalm 136:1-4,23-26', ep='Ephesians 4:7-16', go='John 20:24-29'),
        "collect": (
            'O ALMIGHTY God, Whom to know is everlasting life: Grant us perfectly to know Thy Son '
            'Jesus Christ to be the Way, the Truth, and the Life; that following His steps we may '
            'steadfastly walk in the way that leadeth to eternal life; through the same Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'I KNOW Whom I have believed: and am persuaded that He is able to keep that which I '
            'have committed unto Him against that day. There is laid up for me a crown of '
            'righteousness: which the Lord, the righteous Judge, shall give me. Psalm. O Lord, '
            'Thou hast searched me and known me: Thou knowest my downsitting and mine uprising.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Thomas, Apostle'
        ),
    },
    "holy_innocents": {
        "name": 'The Holy Innocents, Martyrs',
        "date_str": 'Dec 28',
        "season": 'Christmas',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Jeremiah 31:15-17', ps='Psalm 54', ep='Revelation 14:1-5', go='Matthew 2:13-18'),
    },
    "confession_of_st_peter": {
        "name": 'The Confession of St. Peter',
        "date_str": 'Jan 18',
        "season": 'Epiphany',
        "color": 'White',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Acts 4:8-13', ps='Psalm 118:19-29', ep='2 Peter 1:1-15', go='Mark 8:27-35(36–9:1)'),
    },
    "conversion_of_st_paul": {
        "name": 'The Conversion of St. Paul',
        "date_str": 'Jan 25',
        "season": 'Epiphany',
        "color": 'White',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Acts 9:1-22', ps='Psalm 67', ep='Galatians 1:11-24', go='Matthew 19:27-30'),
        "collect": (
            'O ALMIGHTY God, Whom to know is everlasting life: Grant us perfectly to know Thy Son '
            'Jesus Christ to be the Way, the Truth, and the Life; that following His steps we may '
            'steadfastly walk in the way that leadeth to eternal life; through the same Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'I KNOW Whom I have believed: and am persuaded that He is able to keep that which I '
            'have committed unto Him against that day. There is laid up for me a crown of '
            'righteousness: which the Lord, the righteous Judge, shall give me. Psalm. O Lord, '
            'Thou hast searched me and known me: Thou knowest my downsitting and mine uprising.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Conversion of St. Paul'
        ),
    },
    "presentation_of_lord": {
        "name": 'The Presentation of Our Lord',
        "date_str": 'Feb 2',
        "season": 'Epiphany',
        "color": 'White',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Numbers 8:5-22', ps='Psalm 84', ep='Hebrews 2:14-18', go='Luke 2:22-40'),
        "collect": (
            'ALMIGHTY and Everliving God, we humbly beseech Thy Majesty, that as Thine '
            'Only-begotten Son was this day presented in the Temple in substance of our flesh, so '
            'we may be presented unto Thee with pure and clean hearts; through the same Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'WE have thought of Thy loving-kindness, O God: in the midst of Thy Temple. According '
            'to Thy Name, O God, so is Thy praise unto the ends of the earth: Thy right hand is '
            'full of righteousness. Psalm. Great is the Lord, and greatly to be praised: in the '
            'city of our God, in the mountain of His holiness.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Presentation of our Lord'
        ),
    },
    "st_matthias": {
        "name": 'St. Matthias, Apostle',
        "date_str": 'Feb 24',
        "season": 'Epiphany',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Isaiah 66:1-2', ps='Psalm 56', ep='Acts 1:15-26', go='Matthew 11:25-30'),
        "collect": (
            'O ALMIGHTY God, Whom to know is everlasting life: Grant us perfectly to know Thy Son '
            'Jesus Christ to be the Way, the Truth, and the Life; that following His steps we may '
            'steadfastly walk in the way that leadeth to eternal life; through the same Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'I KNOW Whom I have believed: and am persuaded that He is able to keep that which I '
            'have committed unto Him against that day. There is laid up for me a crown of '
            'righteousness: which the Lord, the righteous Judge, shall give me. Psalm. O Lord, '
            'Thou hast searched me and known me: Thou knowest my downsitting and mine uprising.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Matthias, Apostle'
        ),
    },
    "annunciation": {
        "name": 'The Annunciation of Our Lord',
        "date_str": 'Mar 25',
        "season": 'Lent',
        "color": 'White',
        "feast": True,
        "minor": False,
        "readings": _r(ot='Isaiah 7:10-14', ps='Psalm 45:7-15', ep='Hebrews 10:4-10', go='Luke 1:26-38'),
        "collect": (
            'WE beseech Thee, O Lord, pour Thy grace into our hearts; that as we have known the '
            'Incarnation of Thy Son Jesus Christ by the message of an angel, so by His Cross and '
            'Passion we may be brought unto the glory of His Resurrection; through the same Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'ALL the rich among the people shall entreat Thy favor: she shall be brought unto the '
            'King in raiment of needle-work. Her companions shall be brought unto Thee: with '
            'gladness and rejoicing. Psalm. My heart is inditing a good matter: I speak of the '
            'things which I have made touching the King.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Annunciation'
        ),
    },
    "st_mark": {
        "name": 'St. Mark, Evangelist',
        "date_str": 'Apr 25',
        "season": 'Easter',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Isaiah 52:7-10', ps='Psalm 57', ep='Ephesians 4:7-16', go='Mark 16:14-20'),
        "collect": (
            'O ALMIGHTY God, Who hast instructed Thy holy Church with the heavenly doctrine of '
            'Thy Evangelists: Give us grace, that being not like children carried away with every '
            'blast of vain doctrine, we may be established in the Truth of Thy Holy Gospel; '
            'through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'GO ye into all the world: and preach the gospel to every creature. Their sound went '
            'forth through all the earth: and their words to the end of the world. Psalm. Thy '
            'Word is a lamp unto my feet: and a light unto my path.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Mark, Evangelist'
        ),
    },
    "philip_and_james": {
        "name": 'St. Philip and St. James, Apostles',
        "date_str": 'May 1',
        "season": 'Easter',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Isaiah 30:18-21', ps='Psalm 49:1-10', ep='James 1:1-12', go='John 14:1-14'),
        "collect": (
            'O ALMIGHTY God, Whom to know is everlasting life: Grant us perfectly to know Thy Son '
            'Jesus Christ to be the Way, the Truth, and the Life; that following His steps we may '
            'steadfastly walk in the way that leadeth to eternal life; through the same Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'I KNOW Whom I have believed: and am persuaded that He is able to keep that which I '
            'have committed unto Him against that day. There is laid up for me a crown of '
            'righteousness: which the Lord, the righteous Judge, shall give me. Psalm. O Lord, '
            'Thou hast searched me and known me: Thou knowest my downsitting and mine uprising.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Philip and St. James, Apostles'
        ),
    },
    "st_barnabas": {
        "name": 'St. Barnabas, Apostle',
        "date_str": 'Jun 11',
        "season": 'Pentecost',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Isaiah 42:5-12', ps='Psalm 112', ep='Acts 11:19-30', go='Mark 6:7-13'),
    },
    "nativity_of_john_baptist": {
        "name": 'The Nativity of St. John the Baptist',
        "date_str": 'Jun 24',
        "season": 'Pentecost',
        "color": 'White',
        "feast": True,
        "minor": False,
        "readings": _r(ot='Isaiah 40:1-5', ps='Psalm 85:7-13', ep='Acts 13:13-26', go='Luke 1:57-67,80'),
        "collect": (
            'O LORD God, Heavenly Father, Who, through Thy servant John the Baptist, didst bear '
            'witness that Jesus Christ is the Lamb of God Which taketh away the sin of the world, '
            'and that all who believe in Him shall inherit eternal life: We humbly pray Thee to '
            'enlighten us by Thy Holy Spirit that we may at all times find comfort and joy in '
            'this witness, continue steadfast in the true faith, and at last with all believers '
            'attain unto eternal life; through the same Jesus Christ, Thy Son, our Lord, Who '
            'liveth and reigneth with Thee and the Holy Ghost, ever One God, world without end. '
            'Amen.'
        ),
        "introit_text": (
            'THE voice of him that crieth in the wilderness: Prepare ye the way of the Lord, make '
            'straight in the desert a highway for our God. And the glory of the Lord: shall be '
            'revealed. Psalm. It is a good thing to give thanks unto the Lord: and to sing '
            'praises unto Thy Name, O Most High.'
        ),
        "gradual": (
            'AND thou, child, shalt be called the prophet of the Highest: for thou shalt go '
            'before the face of the Lord to prepare His ways. V. John bare witness of Him, and '
            'cried saying, This was He of Whom I spake, He that cometh after me is preferred '
            'before me: for He was before me. Hallelujah. Hallelujah. V. Behold the Lamb of God: '
            'Which taketh away the sin of the world. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — The Nativity of St. John, the Baptist'
        ),
    },
    "st_peter_st_paul": {
        "name": 'St. Peter and St. Paul, Apostles',
        "date_str": 'Jun 29',
        "season": 'Pentecost',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Ezekiel 34:11-16', ps='Psalm 87', ep='Acts 15:1-12', go='Mark 8:27-35'),
        "collect": (
            'O ALMIGHTY God, Who by Thy Son Jesus Christ, didst give to Thy holy Apostles many '
            'excellent gifts, and commandedst them earnestly to feed Thy flock: Make, we beseech '
            'Thee, all Pastors diligently to preach Thy holy Word, and the people obediently to '
            'follow the same, that they may receive the crown of everlasting glory; through Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'I KNOW Whom I have believed: and am persuaded that He is able to keep that which I '
            'have committed unto Him against that day. There is laid up for me a crown of '
            'righteousness: which the Lord, the righteous Judge, shall give me. Psalm. O Lord, '
            'Thou hast searched me and known me: Thou knowest my downsitting and mine uprising.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Peter and St. Paul, Apostles'
        ),
    },
    "st_mary_magdalene": {
        "name": 'St. Mary Magdalene',
        "date_str": 'Jul 22',
        "season": 'Pentecost',
        "color": 'White',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Proverbs 31:10-31', ps='Psalm 73:23-28', ep='Acts 13:26-33a', go='John 20:11-18'),
    },
    "st_james": {
        "name": 'St. James the Elder, Apostle',
        "date_str": 'Jul 25',
        "season": 'Pentecost',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='1 Kings 19:9-18', ps='Psalm 67', ep='Acts 11:27–12:3', go='Mark 10:35-45'),
        "collect": (
            'O ALMIGHTY God, Whom to know is everlasting life: Grant us perfectly to know Thy Son '
            'Jesus Christ to be the Way, the Truth, and the Life; that following His steps we may '
            'steadfastly walk in the way that leadeth to eternal life; through the same Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'I KNOW Whom I have believed: and am persuaded that He is able to keep that which I '
            'have committed unto Him against that day. There is laid up for me a crown of '
            'righteousness: which the Lord, the righteous Judge, shall give me. Psalm. O Lord, '
            'Thou hast searched me and known me: Thou knowest my downsitting and mine uprising.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. James the Elder, Apostle'
        ),
    },
    "st_bartholomew": {
        "name": 'St. Bartholomew, Apostle',
        "date_str": 'Aug 24',
        "season": 'Pentecost',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Proverbs 3:1-7', ps='Psalm 12', ep='2 Corinthians 4:7-10', go='John 1:43-51'),
        "collect": (
            'O ALMIGHTY God, Whom to know is everlasting life: Grant us perfectly to know Thy Son '
            'Jesus Christ to be the Way, the Truth, and the Life; that following His steps we may '
            'steadfastly walk in the way that leadeth to eternal life; through the same Jesus '
            'Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the Holy Ghost, '
            'ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'I KNOW Whom I have believed: and am persuaded that He is able to keep that which I '
            'have committed unto Him against that day. There is laid up for me a crown of '
            'righteousness: which the Lord, the righteous Judge, shall give me. Psalm. O Lord, '
            'Thou hast searched me and known me: Thou knowest my downsitting and mine uprising.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Bartholomew, Apostle'
        ),
    },
    "st_matthew": {
        "name": 'St. Matthew, Apostle and Evangelist',
        "date_str": 'Sep 21',
        "season": 'Pentecost',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Ezekiel 2:8–3:11', ps='Psalm 119:33-40', ep='Ephesians 4:7-16', go='Matthew 9:9-13'),
        "collect": (
            'O ALMIGHTY God, Who by Thy blessed Son didst call Matthew from the receipt of custom '
            'to be an Apostle and Evangelist: Grant us grace to forsake all covetous desires, and '
            'inordinate love of riches, and to follow the same Thy Son Jesus Christ, Who liveth '
            'and reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'I KNOW Whom I have believed: and am persuaded that He is able to keep that which I '
            'have committed unto Him against that day. There is laid up for me a crown of '
            'righteousness: which the Lord, the righteous Judge, shall give me. Psalm. O Lord, '
            'Thou hast searched me and known me: Thou knowest my downsitting and mine uprising.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Matthew, Apostle, Evangelist'
        ),
    },
    "st_michael": {
        "name": 'St. Michael and All Angels',
        "date_str": 'Sep 29',
        "season": 'Pentecost',
        "color": 'White',
        "feast": True,
        "minor": False,
        "readings": _r(ot='Daniel 10:10-14;12:1-3', ps='Psalm 91', ep='Revelation 12:7-12', go='Matthew 18:1-11 | Luke 10:17-20'),
        "collect": (
            'O EVERLASTING God, Who hast ordained and constituted the services of angels and men '
            'in a wonderful order: Mercifully grant, that as Thy holy angels always do Thee '
            'service in Heaven, so by Thy appointment they may succor and defend us on earth; '
            'through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'BLESS the Lord, ye His angels, that excel in strength: that do His commandments, '
            'hearkening unto the voice of His word. Bless ye the Lord, all ye His hosts: ye '
            'ministers of His that do His pleasure. Psalm. Bless the Lord, my soul I and all that '
            'is within me bless His holy Name.'
        ),
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
    "st_luke": {
        "name": 'St. Luke, Evangelist',
        "date_str": 'Oct 18',
        "season": 'Pentecost',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Isaiah 35:5-8', ps='Psalm 147:1-11', ep='2 Timothy 4:5-18', go='Luke 10:1-9'),
        "collect": (
            'O ALMIGHTY God, Who hast instructed Thy holy Church with the heavenly doctrine of '
            'Thy Evangelists: Give us grace, that being not like children carried away with every '
            'blast of vain doctrine, we may be established in the Truth of Thy Holy Gospel; '
            'through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'GO ye into all the world: and preach the gospel to every creature. Their sound went '
            'forth through all the earth: and their words to the end of the world. Psalm. Thy '
            'Word is a lamp unto my feet: and a light unto my path.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Luke, Evangelist'
        ),
    },
    "simon_and_jude": {
        "name": 'St. Simon and St. Jude, Apostles',
        "date_str": 'Oct 28',
        "season": 'Pentecost',
        "color": 'Red',
        "feast": True,
        "minor": True,
        "readings": _r(ot='Jeremiah 26:1-16', ps='Psalm 11', ep='1 John 4:1-6', go='John 15:17-21'),
        "collect": (
            'O ALMIGHTY God, Who hast built Thy Church upon the foundation of the Apostles and '
            'Prophets. Jesus Christ Himself being the Head Corner-Stone: Grant us so to be joined '
            'together in unity of spirit by their doctrine, that we may be made a holy temple '
            'acceptable unto Thee; through the same Jesus Christ, Thy Son, our Lord, Who liveth '
            'and reigneth with Thee and the Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'I KNOW Whom I have believed: and am persuaded that He is able to keep that which I '
            'have committed unto Him against that day. There is laid up for me a crown of '
            'righteousness: which the Lord, the righteous Judge, shall give me. Psalm. O Lord, '
            'Thou hast searched me and known me: Thou knowest my downsitting and mine uprising.'
        ),
        "gradual": (
            'THEIR sound went forth through all the earth: and their words to the end of the '
            'world. V. The heavens declare the glory of God: and the firmament showeth His '
            'handiwork. Hallelujah. Hallelujah. V. I have chosen you out of the world: that ye '
            'should go and bring forth fruit, and that your fruit should remain. Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — St. Simon and St. Jude, Apostles'
        ),
    },
    "all_saints": {
        "name": "All Saints' Day",
        "date_str": 'Nov 1',
        "season": 'Pentecost',
        "color": 'White',
        "feast": True,
        "minor": False,
        "readings": _r(ot='Revelation 7:(2-8)9-17', ps='Psalm 149', ep='1 John 3:1-3', go='Matthew 5:1-12'),
        "collect": (
            'O ALMIGHTY God, Who hast knit together Thine elect in one communion and fellowship '
            'in the mystical Body of Thy Son. Christ our Lord: Grant us grace so to follow Thy '
            'blessed Saints in all virtuous and godly living, that we may come to those '
            'unspeakable joys which Thou hast prepared for those who unfeignedly love Thee; '
            'through Jesus Christ, Thy Son, our Lord, Who liveth and reigneth with Thee and the '
            'Holy Ghost, ever One God, world without end. Amen.'
        ),
        "introit_text": (
            'THESE are they which have come out of great tribulation: and have washed their robes '
            'and made them white in the Blood of the Lamb. Therefore are they before the Throne '
            'of God: and serve Him day and night in His Temple. Psalm. Rejoice in the Lord, O ye '
            'righteous: for praise is comely for the upright.'
        ),
        "gradual": (
            'O FEAR the Lord, ye His saints: for there is no want to them that fear Him. V. They '
            'that seek the Lord ; shall not want any good thing. Hallelujah. Hallelujah. V. Come '
            'unto Me, all ye that labor and are heavy laden: and I will give you rest. '
            'Hallelujah.'
        ),
        "source": (
            'Common Service Book of the Lutheran Church (Philadelphia, 1917), Introits, Collects, '
            'Epistles, Graduals and Gospels — All Saints’ Day'
        ),
    },
}
