"""
`TreeNode`: uned sylfaenol y `Tree` structures
"""

import re
from lxml import etree


class TreeNode(object):
    """
    Uned sylfaenol.

    Dosbarth haniaethol ar gyfer `Nod`, `Sillaf`, `Gair`, ayb.

    a) Mae `TreeNode.neighbours` yn `set` ar gyfer cofnodi gwrthrychau `TreeNode`
    cysylltiedig sydd ddim yn riant na'n blentyn i'r gwrthrych dan sylw). 
    Mae'r "cross-links" yn torri'r `tree structue` caled, ac felly yn cysylltu 
    gwahanol rannau o'r goeden.
    
    Yn benodol, mae `TreeNode.links` ar gyfer cofnodi:
    1. Cytseinedd: Lefel `Nod`
    2. Odlau: Lefel `Sillaf`

    (b) Mae `TreeNode.meta` yn `dict` ar gyfer cofnodi
    "meta information" am y `TreeNode` dan sylw (key:value pairs).

    Yn benodol, mae `TreeNode.meta` ar gyfer cofnodi:
    1. teitl ac awdur cerddi
    2. ???

    """

    # class variable
    counter = 0

    def __init__(self, parent=None):
        TreeNode.counter += 1
        self.id = TreeNode.counter
        self.parent = parent
        self.children = []
        self.neighbours = set()
        self.meta = {}  # meta info

        # for templates
        self.species = type(self).__name__.lower()
        self.genus = type(self).__bases__[0].__name__.lower()
        self.family = None
        if self.parent:
            self.family = type(self).__bases__[0].__bases__[0].__name__.lower()

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def __len__(self):
        return len(self.children)

    def __setitem__(self, idx, item):
        if not isinstance(item, TreeNode):
            raise ValueError('Mae angen `TreeNode` fan hyn.')
        item.parent = self
        self.children[idx] = item

    def __getitem__(self, idx):
        return self.children[idx]

    def append(self, item):
        if not isinstance(item, TreeNode):
            raise ValueError('Mae angen `TreeNode` fan hyn.')
        item.parent = self
        self.children.append(item)

    def nesaf(self):
        if not self.parent:
            return None
        idx = self.parent.children.index(self)
        if idx < len(self.parent) - 1:
            return self.parent.children[idx+1]
        else:
            parent_nesaf = self.parent.nesaf()
            if parent_nesaf and parent_nesaf.children:
                return parent_nesaf.children[0]

    def blaenorol(self):
        # print(type(self), type(self.parent))
        if not self.parent:
            return None
        idx = self.parent.children.index(self)
        # print(idx)
        if idx > 0:
            return self.parent.children[idx-1]
        else:
            parent_blaenorol = self.parent.blaenorol()
            # print('Helo', parent_blaenorol, type(parent_blaenorol), type(parent_blaenorol.parent))
            if parent_blaenorol and parent_blaenorol.children:
                return parent_blaenorol.children[-1]

    def slug(self):
        parts = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', type(self).__name__)).split()
        return '-'.join([part.lower() for part in parts])

    def xml(self):
        element = etree.Element(self.slug())
        element.set('id', str(self.id).strip())

        if self.neighbours:
            s = []
            for nbr in self.neighbours:
                s.append(str(nbr.id).strip())
            element.set('nbrs', '|'.join(s))

        if self.meta:
            for key, val in self.meta.items():
                if type(val) is bool:
                    if val:
                        element.set(str(key).strip(), "true")
                    else:
                        element.set(str(key).strip(), "false")
                else:
                    element.set(str(key).strip(), str(val))

        # recursive call
        for child in self.children:
            child_element = child.xml()  # The `Nod` subclass outputs text here
            element.append(child_element)

        return element

    def xml_str(self, include_header=True, pretty_print=False):
        xml_text = etree.tostring(self.xml(), pretty_print=pretty_print)
        xml_text = xml_text.decode("utf-8")
        if include_header:
            return ''.join([r'<?xml version="1.0" encoding="UTF-8"?>', xml_text])
        return xml_text

    def add_neighbour(self, item):
        '''
        We use `set` here to avoid checking for dupliates
        We also reject self-links
        '''
        
        # only allow links between similar types
        if type(item) is not type(self):
            raise ValueError("Mae angen type {} fan hyn.".format(type(self)))
        
        if not item == self:
            self.neighbours.add(item)
            item.neighbours.add(self)

    def add_neighbours(self, items):
        for item in items:
            self.add_neighbour(item)


# ------------------------------------------------
# test
def main():
    root = TreeNode()
    child = TreeNode()
    root.append(child)
    child.append(TreeNode())
    grandchild = TreeNode()
    grandchild.append(TreeNode())
    grandchild.append(TreeNode())
    child.append(grandchild)
    child.append(TreeNode())
    child.append(TreeNode())
    grandchild = TreeNode()
    grandchild.append(TreeNode())
    grandchild.append(TreeNode())
    child.append(grandchild)
    child.append(TreeNode())
    root.append(TreeNode())
    root.append(TreeNode())
    root.append(TreeNode())
    root.append(TreeNode())

    root.meta['root'] = True
    print(root)

    # print("root")
    print(root.xml_str())

    # node = root[0]
    node = root[0][0]
    node2 = root[0][3]
    node3 = root[0][5]
    node.add_neighbour(node2)
    node.add_neighbour(node3)

    # node = root[0][1][0]
    # print('lefel:', node.lefel())
    print('node:', node.id)
    print('node2:', node2.id)
    print('node3:', node3.id)
    print('node.neighbours:', node.neighbours)
    print('node2.neighbours:', node2.neighbours)
    print('node3.neighbours:', node3.neighbours)
    nesa = node.nesaf()
    print(nesa.id)
    print(nesa.species)
    print(nesa.genus)

    print(root.xml_str())


if __name__ == "__main__":
    main()
