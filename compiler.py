
import my_parser
from parser_tree import CompilationError


class Generator():
    def __init__(self):
        self.parameter_declarations = []

        self.current_parameter_declaration = None


    def parse_node(self, node):
        node_val = node.value

        if node_val.value_type>0:
            print(node.value.value.text)

        print( str(node.value.value))
        print(str(node_val.value_type))



        for node in node.child_nodes:
            self.parse_node(node)

    def translate(self, filename):
        tree = my_parser.parse(filename)
        print(tree)
        self.parse_node(tree.root)

        result = ''

        errors = []


        code_section = 'codeSeg SEGMENT\n \t\t ASSUME cs:code1, ds:dataSeg, ss:stackSeg\n'
        data_section = 'dataSeg SEGMENT\n'
        stack_section = 'stackSeg SEGMENT\n\tdb 4096 dup (?)\nstackSeg ends\n\n'

        ext_params = []
        proc_identifiers = []


        code_section += '\t main:\n'
        code_section += '\t\t mov ax, dataSeg\n'
        code_section += '\t\t mov ds, ax\n'
        code_section += '\t\t mov ax, stackSeg\n'
        code_section += '\t\t mov ss, ax\n'
        code_section += '\t\t mov ax, 0b800h\n'
        code_section += '\t\t mov es, ax\n\n'

        code_section += '\t\t mov ax,4c00h\n'
        code_section += '\t\t int 21h\n\n'

        code_section += 'codeSeg ends \n\tend main\n'

        data_section += 'dataSeg ends\n\n'

        result += data_section
        result += stack_section
        result += code_section

        if len(errors) > 0:
            print('Errors:')
            for error in errors:
                print(error)
            return ''
        else:
            return result


def compile(filename):
    generator = Generator()
    return generator.translate(filename)


if __name__ == '__main__':
    print('\n')
    print('-' * 70)
    print('Final result:')
    print('-' * 70)
    print('\n')
    print(compile('parser_true_test.txt'))