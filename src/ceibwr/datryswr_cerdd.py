# datryswr_penillion.py
'''
Dulliau ar gyfer darganfod awdl mewn cyfres o benillion
'''
from ceibwr.pennill import Pennill
from ceibwr.cerdd import Cerdd
from ceibwr.awdl import Awdl

from ceibwr.datrysiad import Amwys

from ceibwr.datryswr_odl import prawf_odl
from ceibwr.datryswr_pennill import datryswr_pennill

from ceibwr.seinyddwr import Seinyddwr


def datryswr_cerdd(cerdd):
    '''
    Gwirio os yw pob pennill ar un o'r pedwar mesur ar hugain.

   :param cerdd: Y gerdd i'w datrys.
   :type cerdd: list[`Pennill`]
   :return: Awdl neu restr o ddatrysiadau pennill
   :rtype: `Awdl` neu `list[Datrysiad]`
   ]
    Mae'r ffwythiant yn creu rhestr o ddatrysiadau pennill. Os yw pob 
    un o'r rhain ar un o'r pedwar mesur ar hugain, mae'r ffwythiant yn
    dychwelyd gwrthrych `Awdl`; fel arall, mae'n dychwelyd rhestr o'r
    datrysiadau unigol.
    '''
    # type checks
    if type(cerdd) is not Cerdd:
        raise TypeError("Mae angen `Cerdd` fan hyn, nid {}".format(type(cerdd)))

    # duplication?
    if not all([type(x) is Pennill for x in cerdd]):
        raise TypeError("Mae angen `list` o wrthrychau `Pennill` fan hyn")

    # seinyddio - pam fan hyn?
    # se = Seinyddwr()
    # for pennill in cerdd.children:
    #     for llinell in pennill.children:
    #         se.seinyddio_llinell(llinell)
    # print(pennill)
    # print(pennill.sain())

    # penillion = list(reversed(cerdd.children))

    dats = []
    for pennill in cerdd.children:

        dat = datryswr_pennill(pennill)
        dats.append(dat)

    if all([dat.dosbarth for dat in dats]):
        return Awdl(dats)

    return Amwys(dats)


# ------------------------------------------------
# main
def main():

    # from ceibwr.profion_pennill import profion

    s1 = """dwyglust feinion aflonydd
dail saets wrth ei dâl y sydd
trwsio fal golewo glain
y bu wydrwr ei bedrain."""

    s2 = """Wele rith fel ymyl rhod - o'n cwmpas
Campwaith dewin hynod.
Hen linell bell nad yw'n bod
Hen derfyn nad yw'n darfod.
"""

    p1 = Pennill(s1)
    p2 = Pennill(s2)
    dat = datryswr_cerdd([p1, p2])

    print(dat)
    print(type(dat))
    print(repr(dat))
    print('-----')


if __name__ == '__main__':
    main()
