# cerddi.py
'''
Creu `dict o wrthrychau `Cerdd` o'r ffeiliau yn /data/cerddi/.

Mae hyn ar gyfer `ceibwrapp` - dyle fe fod fana, neu o leia
dyle hwn allbynnu ffeil .json (h.y. fformat safonol).
'''

# import os
import yaml
from pathlib import Path
from slugify import slugify

from ceibwr.settings import CERDDI_ROOT
from ceibwr.peiriant import Peiriant


def creu_cerddi_dict():

    db = {}

    rp = Path(CERDDI_ROOT)
    for subdir in rp.iterdir():

        # ignore dot folders
        if subdir.name.startswith('.'):
            continue

        db[subdir.name] = {
            'slug': slugify(subdir.name),
            'cerddi': [],
         }

        for file in subdir.iterdir():

            # ignore dot files
            if file.name.startswith('.'):
                continue

            with open(file) as f:

                s = f.read().strip()

                # parse header
                parts = s.split('---')
                if not parts[0]:
                    parts = parts[1:]
                head = parts[0].strip()
                body = parts[1].strip()

                cerdd = yaml.safe_load(head)

                # enforce `teitl`
                if 'teitl' not in cerdd:
                    continue

                cerdd['slug'] = slugify(subdir.name + ' ' + cerdd['teitl'])
                cerdd['testun'] = body
                cerdd['amrwd'] = s  # hac

                db[subdir.name]['cerddi'].append(cerdd)

        db[subdir.name]['cerddi'] = sorted(db[subdir.name]['cerddi'], key=lambda d: d['teitl'])

    db = {key: value for key, value in sorted(db.items())}

    return db


# mefus
def creu_mefus():

    pe = Peiriant()
    mefus = []

    rp = Path(CERDDI_ROOT)
    for subdir in rp.iterdir():

        # skip dot folders
        if subdir.name.startswith('.'):
            continue

        for file in subdir.iterdir():

            # skip dot files
            if file.name.startswith('.'):
                continue

            with open(file) as f:
                s = f.read().strip()

                # parse
                meta, uned = pe.parse(s)

                # datrys
                dat = pe.datryswr(uned)
                dat.meta = meta

                # cofnodi
                mefus.append(dat.xml_str())

    return mefus


def main():
    import pprint

    # cd = creu_cerddi_dict()
    # pprint.pprint(cd)
    # print()

    mefus = creu_mefus()
    mefus = ''.join(mefus)
    pprint.pprint(mefus)
    print()


if __name__ == "__main__":
    main()
