# test data ar gyfer prawf_cynghanedd

profion = {
    'croes': (
        ("Ochain cloch", "a chanu clir"),
        ("Si'r oerwynt", "a sêr araul"),
        ("Awdur mad", "a dramodydd"),
        ("Ei awen brudd", "yn eu bro"),
        ("Onid teg", "yw ein tud?"),
    ),
    'croes_o_gyswllt': (
        ("Aderyn llwyd", "ar un llaw"),
        ("Daw geiriau Duw", "o'i gaer deg"),
        ("Rhwydd gamwr,", "hawdd ei gymell"),
        ("Hawdd yw cyrraedd", "y cyrion"),
        ("Ysgweier llesg", "ar y llawr"),
        ("Y ferch ofer", "ei chyfoeth"),
        ("Gwelais y glew", "is y glyn"),
        ("Drwg ydyw'r gwae", "o dir gwyllt"),
        ("Trist ŵr trosto", "o'r trawster"),
        ("Ni chei di barch", "wedi byw"),
    ),
    'traws': (
        ("Ochain cloch", "a gwreichion clir"),
        ("Si'r oerwynt", "dan sêr araul"),
        ("Awdur mad", "yw'r dramodydd"),
        ("Ei awen brudd", "dros ein bro"),
        ("Ni all lladd", "ond ennyn llid"),
    ),
    'traws_fantach': (
        ("Y gŵr", "aruchel ei gân"),
        ("Y brawd", "o bellafion bro"),
        ("Brwd", "yw aderyn brig"),
        ("Glaw", "ar ymylon y glyn"),
    ),
    'trychben': (
        ("Canu mydr", "cyn ymadael"),
        ("Nid yn aml", "y down yma"),
        ("Ond daw gwefr", "cyn atgofion"),
        ("Calon ddofn", "ei hofn hefyd"),
        ("A'r dyn crupl", "er doe'n cropian"),
        ("Parabl", "anabl anniben"),  # methiant: camacennu ("anabl")
    ),
    'cysylltben': (
        ("Onid bro", "dy baradwys"),
        ("A ddaw", "fy mab i Ddyfed"),
    ),
    'llusg': (
        ("Beiddgar", "yw geiriau cariad"),
        ("Y mae arogl", "yn goglais"),
        ("Pell", "ydyw coed yr ellyll"),
        ("Y mae Morfudd", "yn cuddio"),
        ("Yr haul ar dawel", "heli"),
        ("Ymysg y bedw", "yn ddedwydd"),            # methiant
    ),
    'llusg_lafarog': (
        ("Un distaw", "ei wrandawiad"),
        ("Gwynt y rhew", "yn distewi"),
    ),
    'llusg_gudd': (
        ("Ac yma", "bu cydnabod"),
        ("Ac wedi", "d'awr godidog"),
        ("Ac wele", "lid y gelyn"),
        ("Gwn ddifa", "lawer calon"),
        ("Eto dring", "lethr Carn Ingli"),
        ("Y ddinas", "draw yn wastraff"),
        ("Esgor", "mae llid ar ormes"),
        ("Bu llawer", "ddoe yn cerdded"),
        ("Dacw wiw", "dyfiant liwdeg"),
        ("Ac wele", "wychder Dewi"),
    ),
    'llusg_ewinog': (
        ("Yn wyneb", "haul ar Epynt"),
        ("Yr esgob", "biau popeth"),
        ("Aeth fy nghariad", "hyd ato"),
        ("O'r garreg", "hon daeth eco"),
        ("I'r esgob", "pur rhoed popeth"),
        ("Fy nghariad", "troaf atat"),
        ("O'r garreg", "clywaid eco"),
    ),
    'sain': (
        ("Cân ddiddig", "ar frig", "y fron"),
        ("Gŵr amhur", "yn sur", "ei sen"),
        ("Bydd alaw", "draw", "wedi'r hwyr"),
        ("Yr eos", "dlos", "rhwng dail ir"),
        ("Bydd", "y dolydd", "yn deilio"),
        ("Canlyniad", "cariad", "yw cosb"),
        ("Cân hardd", "croyw fardd", "Caerfyrddin"),
        ("Heddychwr", "gwr", "rhagorol"),
        ("Myn Pedr,", "heb na chledr", "na chlwyd"),
        ("Mae'n gas", "gennyf dras", "y dref"),
    ),
    'sain_ewinog': (
        ("Caf fynd", "draw ar hynt", "i'r rhos"),
        ("Rhoi het", "ar ei harffed", "hi"),
        ("Caf fynd", "tua'r helynt", "draw"),
    ),
    'sain_gudd': (
        ("Eu plaid", "yw duw rhai", "drwy'u hoes"),
        ("Llyfrdra", "dy wlad", "nid yw les"),
        ("A'i gord", "yn deffro'r", "dyffryn"),
        ("Nid â", "dy gariad", "o gof"),
    ),
    'sain_lafarog': (
        ("Fe ddaeth pob croes", "i'w oes", "ef"),
        ("Didranc", "ieuanc", "ei awen"),
        ("Pren gwyrddliw", "o wiw", "wead"),
        ("Gŵr o ystryw", "ydyw", "ef"),
    ),
    'sain_o_gyswllt': (
        ("Galarnad groch", "a chloch", "leddf"),
        ("Bydd sug", "i'r grug", "a'r egin"),
        ("Dy fab rhad", "O! Dad", "yw ef"),            # methiant
    ),
    'sain_gadwynog': (
        ("Dringo", "bryn", "a rhodio", "bro"),
        ("Trydar", "mwyn", "adar", "mynydd"),
        ("Un dydd", "gwelais", "brydydd", "gwiw"),
    ),
    'llusg_deirodl': (
        ("Am Fôn", "mae sôn", "digonol"),
        ("Ni chaf", "un haf", "o afiaith"),
        ("Fan draw", "mae'r glaw", "yn gawod"),
        ("Bu côr", "o'r môr", "am oriau"),
    ),
    'sain_deirodl': (
        ("Anedd", "o hedd", "yw'r bedd", "bach"),
        ("Trydar", "gwâr", "yr adar", "ydyw"),
    ),
    'sain_ddwbl': (
        ("Boch", "goch", "gain", "rhiain", "rywiog"),
        # ("Daw", "braw", "breuedd", "diwedd", "d'oes"),
    ),
}


def main():
    import json
    s = json.dumps(profion, indent=4, ensure_ascii=False)
    print(s)


if __name__ == "__main__":
    main()
