profion = {
    "croes": (
        ("Mae llyn hen", "i'm llawenhau"),
        ("Y llwybrau gynt", "lle bu'r gan"),
        ("Am eu hawr", "yn ymaros"),
        ("Si'r oerwynt", "a sêr araul"),
    ),
    "traws": (
        ("Ochain cloch", "a gwreichion clir"),
        ("Hen derfyn", "nad yw'n darfod"),
        ("Ei awen brudd", "dan ein bro"),
        ("Ei awen brudd", "dan ein brodd"),
    ),
    "traws_fantach": (
        ("Y brawd", "o bellafion bro"),
        ("Brwd", "yw aderyn brig")
    ),
    "croes_o_gyswllt": (
        ("Aderyn llwyd", "ar un llaw"),
        ("Daw geiriau duw", "o'i gaer deg"),
        ("Ewch o'r Llew Coch", "i'r lle cudd"),
        ("Rhaid y car", "ydyw cyrraedd"),
        ("Actau ieuanc", "dyhewyd"),
        ("Yn un eu can", "yn eu cur"),
    ),
    "croes_o_gyswllt_gymhleth": (
        ("Hawdd yw cyrraedd", "y cyrion"),
        ("Ysgweier llesg", "ar y llawr"),
        ("Y ferch ofer", "ei chyfoeth"),
        ("Gwelais y glew", "is y glyn"),
        ("Drwg ydyw'r gwae", "o dir gwyllt"),
        ("Trist ŵr trosto", "o'r trawster"),
        ("Ni chei di barch", "wedi byw"),
    ),
    "trychben": (
        ("Canu mydr", "cyn ymadael"),
        ("Nid yn aml", "y down yma"),
        ("Ond daw gwefr", "cyn atgofion"),
        ("ei hofn", "hefyd"),
    ),
    "cysylltben": (
        ("Yma bu", "nwyf i'm beunydd"),
        ("Onid bro", "dy baradwys"),
        ("A ddaw", "fy mab i Ddyfed"),
        ("gwae", "nid gweniaith"),
        ("gwaer", "nid gwerniaith"),
        ("gwaer", "ncid gwernciaith"),
        ("a maen perl", "mewn parlment"),
    ),
    "dau-yn-ateb-un": (
        ("Ni rannodd", "yn yr einioes"),
        ("Ar warrau", "eryrod"),
        ("Fel y cawn", "afal cynnar"),
        ("Mae eryr llwyd", "am wyr llen"),
        ("Drwy'r ais", "a deuair isod"),
        ("Troes Elwy lwyd", "tros y lan"),
        ("Gorau plas", "i grupl o'i lin"),
    ),
    "caledu": (
        ("Rhwbio pridd", "ar bob brawddeg"),
        ("Ond daw gwefr", "cyn atgofion"),
        ("Oedd enwog gynt", "heb ddwyn cas"),
        ("Aeron per", "ei hwyneb hi"),
        ("Onid hoff", "yw cofio'n taith"),
        ("Meurig hir,", "mawr y carwn"),
        ("Pren a ddwg", "bob rhinwedd dda"),
        ("Ni bu trist", "yn y byd rhydd"),
        ("A fo cryf", "a fag rhyfel"),
        ("Aberconwy", "barc gwinwydd"),
    ),
    "meddalu": (
        ("Acw drwy gwymp", "Ector gynt"),  # ct > c+d
        ("Eich tadau", "oedd i'ch deudir"),  # cht > ch+d
        ("Crefft rwydd", "i gadw corff draw"),  # fft > ff+d
        ("Dy wallt aur", "i dwyllo dyn"),  # llt > ll+d
        ("Crist a roed", "i ddwyn croes drom"),  # st > s+d
    ),
    "croes_o_gyswllt_ewinog": (
        ("Cynnar y dug", "hwn i'r daith"),
        ("Traean y byd", "draw'n y banc"),
        # ("Pryd dy wyneb", "Brytanaidd"),
    ),
    "sain_siwr": (
        ("o'n cwmpas", "campwaith"),
        ("Ni ddichon", "y galon gaeth"),
        ("Can hardd croyw fardd", "Caerfyrddin"),
        ("Ond daw gwefr", "cyn atgofion"),
        ("haul", "yr ellyllon yw hi"),
        ("wedi gwneud", "gwahaniaeth"),
    ),
    "misc": (
        ("Wele rith", "fel ymyl rhod"),
        ("hofn", "hefyd"),
        # ("anabl", "anniben"),
        ("Awdur mad", "a dramodydd")
    ),
}


def main():
    import json
    s = json.dumps(profion, indent=4, ensure_ascii=False)
    print(s)


if __name__ == "__main__":
    main()
