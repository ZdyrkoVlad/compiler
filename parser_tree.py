class CompilationError:
    def __init__(self, stage, line, column, msg):
        self.stage = stage
        self.line = line
        self.column = column
        self.message = msg

    def __str__(self):
        return "{} error ({}, {}): {}".format(self.stage, self.line, self.column, self.message)

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.child_nodes = []

    def add_child(self, child):
        self.child_nodes.append(child)
        child.parent = self


class TreeValue:
    def __init__(self, value_type, value):
        self.value_type = value_type
        self.value = value

    def __str__(self):
        res = ''
        if self.value_type == 0:  # non-terminal
            res += '<' + self.value + '>'
        elif self.value_type >= 1:
            res += '{} {}'.format(self.value.id, self.value.text)
        return res


class Tree:
    def __init__(self):
        self.root = TreeNode(TreeValue(0, 'program'))
        self.current_node = self.root

    def add_node(self, value, change_current=False):
        new_node = TreeNode(value)
        self.current_node.add_child(new_node)
        if change_current:
            self.current_node = new_node

    def switch_to_parent(self):
        self.current_node = self.current_node.parent

    def __str__(self):
        return "Resulting tree: \n\n" + self.print_node(self.root, 0) + "-"*50

    def print_node(self, node, ind):
        res = ''
        if ind > 0:
            res += '··'*ind
        res += str(node.value) + '\n'
        for child in node.child_nodes:
            res += self.print_node(child, ind + 1)
        return res
