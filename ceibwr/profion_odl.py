# data profi odlau

profion = {
    "odlau_cyflawn": (
        ("cath", "math"),
        ("pren", "llen"),
        ("mafon", "duon"),  # deusain ddwbl
        ("calon", "creulon"),
        ("gwlad", "cariad"),
        ("galwad", "cariad"),  # dwy ddeusiain talgron
        ("wiwd", "liwd"),
        ("croes", "oes"),
    ),
    "odlau_llafarog": (
        ("tro", "llo"),
        ("cadno", "banjo"),
    ),
    "proestau_cyflawn": (
        ("hen", "dyn"),
        ("llawn", "mewn"),
        ("telyn", "ystyrlon"),
    ),
    "proestau_llafarog": (
        ("tew", "byw"),
        ("bro", "da"),
    ),
    "odlau_llusg": (
        ("beiddgar", "cariad"),
        ("morfudd", "cuddio"),
        ("tawel", "heli"),
    ),
    "odlau_llusg_cudd": (
        ("yma", "bu", "cydnabod"),
        ("wele", "lid", "gelyn"),
        ("ddifa", "lawer", "calon"),
        ("wiw", "dyfiant", "liwdeg"),
        ("ddinas", "draw", "wastraff"),
        # ("ddinas", "draw", "wasdraff"),
        ("wele", "wychder", "Dewi"),
        ("dring", "lethr", "carningli"),
    ),
    "odlau_llusg_ewinog": (
        ("wyneb", "haul", "Epynt"),
        ("esgob", "biau", "popeth"),
        ("nghariad", "hyd", "ato"),
        ("garreg", "hon", "eco"),
    ),
}


def main():
    import json
    s = json.dumps(profion, indent=4, ensure_ascii=False)
    print(s)


if __name__ == "__main__":
    main()
