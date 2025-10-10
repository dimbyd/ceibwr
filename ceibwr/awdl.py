# awdl.py
"""
`Awdl` type.

Datrysiad ar gyfer dau neu fwy o benillion ar fesurau caeth.
"""

from ceibwr.datrysiad import Datrysiad


class Awdl(Datrysiad):
    '''
    Dosbarth ar gyfer dilyniant o benillion ar y mesurau.
    Mae pob pennill yn un rhan o'r rhaniad.
    '''
    def __init__(self, rhaniad, parent=None):
        Datrysiad.__init__(self, rhaniad, parent=parent)

        self.dosbarth = 'AWD'

    def __str__(self):
        return '\n\n'.join([str(elfen) for elfen in self.children])
