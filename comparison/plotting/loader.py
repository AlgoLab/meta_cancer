from tree import Node, Tree
import re

def load_from_ground(filepath):
    tree = []
    with open(filepath, 'r') as f:
        tree = f.readlines()

    ROOT = Node(0)
    TREE = Tree(ROOT)
    gv = tree[1:-1]
    for line in gv:
        line = line.strip()
        if ' -> ' in line:
            s, e = line.split(' -> ')

            s = int(s.replace('"', ''))
            e = int(e.replace('"', ''))

            x = TREE.get_node(s)
            if not x:
                x = Node(s)
                TREE.add_node(x)

            y = TREE.get_node(e)
            if not y:
                y = Node(e)
                TREE.add_node(y)

            TREE.add_edge(s, e)

        if 'label' in line:
            id, label = line.split(' [')

            id = int(id.replace('"', '').strip())
            label = label[7: -3]
            if '-' in label:
                TREE.set_deletion(id)
                label = label.replace('-', '')
                TREE.set_mutations(id, [label])
            else:
                mut = label.split(' ')
                node = TREE.get_node(id)
                TREE.set_mutations(id, mut)

    return TREE

def load_from_sasc(filepath, score=True):
    tree = []
    with open(filepath, 'r') as f:
        tree = f.readlines()

    ROOT = Node(0)
    TREE = Tree(ROOT)
    if score:
        gv = tree[1:-3]
    else:
        gv = tree[1:-1]

    for line in gv:
        line = line.strip()[:-1]
        if ' -> ' in line:
            s, e = line.split(' -> ')

            s = int(s.replace('"', ''))
            e = int(e.replace('"', ''))

            x = TREE.get_node(s)
            if not x:
                x = Node(s)
                TREE.add_node(x)

            y = TREE.get_node(e)
            if not y:
                y = Node(e)
                TREE.add_node(y)

            TREE.add_edge(s, e)
            # print(s, e)

        if 'label' in line:
            id, label = line.split(' [')

            id = int(id.replace('"', '').strip())
            label = label[: -1]
            if 'color=indianred1' in label:
                m = re.search(r'label="(\d+)"', label)
                mut = str(m.group(1))
                TREE.set_deletion(id)
                TREE.set_mutations(id, [mut])
            else:
                if id != 0:
                    m = re.search(r'label="(\d+)"', label)
                    mut = str(m.group(1))
                else:
                    mut = 'germline'
                # node = TREE.get_node(id)
                TREE.set_mutations(id, [mut])

    return TREE

def load_from_pso(filepath):
    tree = []
    with open(filepath, 'r') as f:
        tree = f.readlines()

    ROOT = Node(0)
    TREE = Tree(ROOT)

    gv = tree[4:-1]
    for line in gv:
        line = line.strip()[:-1]
        if ' -- ' in line:
            s, e = line.split(' -- ')

            s = s.replace('"', '').strip()
            e = e.replace('"', '').strip()

            x = TREE.get_node(s)
            if not x:
                x = Node(s)
                TREE.add_node(x)

            y = TREE.get_node(e)
            if not y:
                y = Node(e)
                TREE.add_node(y)

            TREE.add_edge(s, e)

    for line in gv:
        if 'label' in line:
            id, label = line.split(' [')

            id = id.replace('"', '').strip()
            label = label[: -1]
            if 'color' in label:
                m = re.search(r'label="(\d+)"', label)
                mut = str(m.group(1))
                TREE.set_deletion(id)
                TREE.set_mutations(id, [mut])
            else:
                if 'germline' in label:
                    TREE.root = TREE.id_to_node[id]
                    TREE.id_to_node[id] = TREE.root
                    TREE.set_mutations(id, ['germline'])
                else:
                    m = re.search(r'label="(\d+)"', label)
                    mut = str(m.group(1))
                    TREE.set_mutations(id, [mut])

    return TREE

def load_from_ea(filepath):
    tree = []
    with open(filepath, 'r') as f:
        tree = f.readlines()

    ROOT = Node(0)
    TREE = Tree(ROOT)

    gv = tree[1:-1]
    for line in gv:
        line = line.strip()[:-1]
        if ' -- ' in line:
            s, e = line.split(' -- ')

            s = s.replace('"', '').strip()
            e = e.replace('"', '').strip()

            x = TREE.get_node(s)
            if not x:
                x = Node(s)
                TREE.add_node(x)

            y = TREE.get_node(e)
            if not y:
                y = Node(e)
                TREE.add_node(y)

            TREE.add_edge(s, e)

    for line in gv:
        if 'label' in line:
            id, label = line.split(' [')

            id = id.replace('"', '').strip()
            label = label[: -1]
            print(line, label)
            if '-' in label:
                m = re.search(r'label="(\d+)-"', label)
                mut = str(m.group(1))
                TREE.set_deletion(id)
                TREE.set_mutations(id, [mut])
            else:
                if 'germline' in label:
                    TREE.root = TREE.id_to_node[id]
                    TREE.id_to_node[id] = TREE.root
                    TREE.set_mutations(id, ['germline'])
                else:
                    m = re.search(r'label="(\d+)"', label)
                    mut = str(m.group(1))
                    TREE.set_mutations(id, [mut])

    return TREE

if __name__ == '__main__':
    import sys
    test = load_from_ea(sys.argv[1])

    test.print()