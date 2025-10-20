# main.py
'''
CLI entry point.
'''

import sys
import logging
from argparse import ArgumentParser

from ceibwr.peiriant import Peiriant

from ceibwr.cysonion import llythrenwau
from ceibwr.llinell import Llinell

# static
from ceibwr.settings import LOG_FILE_NAME
from ceibwr.settings import GEIRIADURON
odlau_file = GEIRIADURON['default']['ODLIADUR']        # json
geirfa_file = GEIRIADURON['default']['GEIRFA']      # txt


def main(args=None):
    '''
    CLI entry point.
    '''
    # options
    parser = ArgumentParser()

    parser.add_argument("-d", "--datrys",
                        help="datrys mewnbwn uniongyrchol (cli)")

    parser.add_argument("-df", "--datrys-ffeil",
                        help="datrys cynnwys ffeil (utf-8)")

    parser.add_argument("-o", "--odl",
                        help="chwilio am eiriau sy'n odli")

    parser.add_argument("-c", "--clec",
                        help="chwilio am eiriau sy'n cynganeddu")

    parser.add_argument("-ll", "--llusg",
                        action="store_true",
                        help="chwilio am odlau llusg")

    parser.add_argument("-ac", "--acennog",
                        action="store_true",
                        help="cyrchu geiriau acennog yn unig")

    parser.add_argument("-pr", "--proest",
                        action="store_true",
                        help="cynnwys geiriau sy'n proestio")

    parser.add_argument("-de", "--demo-llinellau",
                        action="store_true",
                        help="demo datrys llinell")

    parser.add_argument("-dc", "--demo-cwpledi",
                        action="store_true",
                        help="demo datrys cwpled")

    parser.add_argument("-dp", "--demo-penillion",
                        action="store_true",
                        help="demo datrys pennill")

    parser.add_argument("-p", "--pysgota",
                        help="pysgota am gynghanedd mewn testun rydd")

    parser.add_argument("--max",
                        type=int,
                        default=8,
                        help="nifer mwyaf o sillafau (pysgotwr)")

    parser.add_argument("--min",
                        type=int,
                        default=4,
                        help="nifer isaf o sillafau (pysgotwr)")

    # parser.add_argument("--ipa",
    #                     action="store_true",
    #                     help="allbwn seinegol (IPA)")

    # parser.add_argument("-v", "--verbose",
    #                     action="store_true",
    #                     help="manylion cynhwysfawr")

    parser.add_argument("-x", "--xml",
                        action="store_true",
                        help="allbwn xml")

    # prosesu opts
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    # init robot
    pe = Peiriant()

    # 1. datrysiad uniongyrchol
    # TODO: handle stdin ("cat cerdd.txt | ceibwr-cli > datrysiad.txt")
    if args.datrys:

        dat = pe.datryswr(Llinell(args.datrys))

        print()
        if args.xml:
            print(dat.xml_str())
        else:
            print(dat, end='')
            print(dat.create_tabular(fancy=True, toriad='|', cmap=pe.cmap))
            print(pe.beiro.cyan(dat.dosbarth) if dat.dosbarth else pe.beiro.coch('XXX'))
        print()

    # 2. datrysiad ffeil
    elif args.datrys_ffeil:

        with open(args.datrys_ffeil) as f:
            s = f.read()

        meta, uned = pe.parse(s)

        if meta:
            print('------------------------------')
            for key, value in meta.items():
                print(f'{key.title()}: {value}')
            print('------------------------------')
        
        dat = pe.datryswr(uned)
        print(dat.create_tabular(fancy=True, toriad='|', cmap=pe.cmap))
        print('')

    # 3. odliadur
    elif args.odl:
        odlau = pe.odliadur(args.odl, acennog=args.acennog, llusg=args.llusg)
        if odlau:
            print(pe.beiro.cyan(' '.join(odlau)))

    # 4. cleciadur
    elif args.clec:
        clecs = pe.cleciadur(args.clec)
        if clecs:
            for key, val in clecs.items():
                if val:
                    print(key)
                    print(pe.beiro.cyan(' '.join(clecs[key])))

    # 5. pysgotwr
    elif args.pysgota:

        with open(args.pysgota) as f:
            s = f.read()

        dats = pe.pysgotwr(s, min_sillafau=args.min, max_sillafau=args.max)

        print('------------------------------')
        for dat in dats:
            print(dat.show_fancy(toriad='|', cmap=pe.cmap))
            if dat.dosbarth:
                dosb_str = llythrenwau['cynghanedd'][dat.dosbarth]
                print(pe.beiro.cyan(dosb_str + ' ' + str(dat.nifer_sillafau())))
            print('---------------')

        print('------------------------------')
        print('Nifer geiriau:', len(s.split()))
        print('Nifer cynganeddion:', len(dats))
        print('Cyfradd:', round(len(dats)/len(s.split()), 3))

    # A. demo llinellau
    elif args.demo_llinellau:
        pe.demo_llinellau()

    # B. demo cwpledi
    elif args.demo_cwpledi:
        pe.demo_cwpledi()

    # C. demo penillion
    elif args.demo_penillion:
        pe.demo_penillion()

    else:
        print('Heb adnabod y dewisiad fan hyn.')

    return


if __name__ == '__main__':

    from datetime import datetime

    # TODO: logging drwyddi draw
    logging.basicConfig(
        filename=LOG_FILE_NAME,
        filemode='w',
        encoding='utf-8',
        level=logging.DEBUG,
    )
    logging.info('Helo.')
    logging.info("Amser nawr: " + str(datetime.now()))

    main()

    logging.info('Hwyl fawr.')
