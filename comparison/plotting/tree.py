class Node:
    def __init__(self, id):
        self.id = id
        self.mutations = None
        self.deletion = False

        self.parent = None
        self.children = []
    
    def get_name(self):
        return ' '.join(self.mutations)
    def get_name_comma(self):
        if not self.deletion:
            return ','.join(self.mutations)
        else:
            return ','.join('%sd' % x for x in self.mutations)

    def to_dot(self):
        return f'"{self.id}" [label="{",".join(self.mutations)}{"-" if self.deletion else ""}"]'

    # def copy(self):
    #     cp = Node(self.id)
    #     cp.mutations = self.mutations
    #     cp.deletion = self.deletion


class Tree:
    def __init__(self, root):
        self.root = root
        self.id_to_node = {}
        self.mut_to_node = {}
        self.deletions = []
        self.edges = []

        self.add_node(root)
    
    def add_node(self, node):
        self.id_to_node[node.id] = node

    def get_node(self, id):
        try:
            return self.id_to_node[id]
        except:
            return None

    def add_edge(self, start_id, end_id):
        s_node = self.get_node(start_id)
        e_node = self.get_node(end_id)

        e_node.parent = s_node
        s_node.children.append(e_node)
        self.edges.append((start_id, end_id))

    def set_mutations(self, id, mutations):
        self.get_node(id).mutations = mutations
        for mut in mutations:
            if not self.get_node(id).deletion:
                self.mut_to_node[mut] = self.get_node(id)

    def set_deletion(self, id):
        self.get_node(id).deletion = True
        self.deletions.append(self.get_node(id))

    def is_ancestor(self, anc_mut, node_mut):
        anc = self.mut_to_node[anc_mut]
        node = self.mut_to_node[node_mut]

        # if anc == node:
        #     return True

        p = node.parent
        while p:
            if p == anc:
                return True
            
            p = p.parent
        return False

    def get_deletions_name(self):
        ret = []
        for d in self.deletions:
            ret.append(d.get_name())
        return ret

    @staticmethod
    def collapse_rec(node, clones, node_to_clone):
        if not node:
            return
        if node.deletion:
            pass
        elif node.parent.deletion:
            clones.append([node])
            node_to_clone[node] = len(clones) - 1
        elif len(node.parent.children) == 1:
            clones[node_to_clone[node.parent]].append(node)
            node_to_clone[node] = node_to_clone[node.parent]
        else:
            clones.append([node])
            node_to_clone[node] = len(clones) - 1

        for child in node.children:
            Tree.collapse_rec(child, clones, node_to_clone)

    def collapse_into_clones(self):
        clones = []
        node_to_clone = {}

        for n in self.root.children:
            clones.append([n])
            node_to_clone[n] = len(clones) - 1
            # print(clones, node_to_clone)
            for c in n.children:
                Tree.collapse_rec(c, clones, node_to_clone)

        m_clones = []
        mut_to_clone = {}
        for c in clones:
            mut = []
            for n in c:
                if not n.deletion:
                    for m in n.mutations:
                        mut.append(m)
                        mut_to_clone[m] = len(m_clones)

            m_clones.append(mut)

        return (m_clones, mut_to_clone)
    
    def _rec_print(self, node):
        if not node:
            return
        if node.parent:
            print(f'\t"{node.parent.id}" -> "{node.id}"')
        print("\t"+node.to_dot())
        for child in node.children:
            self._rec_print(child)

    def print(self):
        print("digraph {")
        self._rec_print(self.root)
        print("}")
