
import my_parser
from parser_tree import CompilationError


class Generator():
    def __init__(self):
        self.procedure_declarations = []
        self.parameter_declarations = []
        self.program_identifier = ''
        self.program_date = []

        self.current_program_date = {'identifier': '', 'parameters': []}
        self.current_procedure_declaration = {'identifier': '', 'parameters': []}
        self.current_parameter_declaration = None
        self.current_program_identifier = ''

    def parse_node(self, node):

        node_val = node.value
        print(str(node_val.value))
        print(str(node_val))
        print(str(node_val.value_type))

        if node_val.value_type== 1:
            if str(node_val.text)=="404 VAR":
                self.parse_node(node.child_nodes[1])

                self.parse_node(node.child_nodes[2])
                self.current_program_date['identifier'] = self.current_program_identifier
                self.current_program_date['parameters'] = self.parameter_declarations
                self.program_date.append(self.current_procedure_declaration)

                self.current_program_date = {'identifier': '', 'parameters': []}
                self.program_date = []


        if node_val.value_type == 0:

            # for each declaration new

            if node_val.value == "program":

                self.parse_node(node.child_nodes[1])

                self.parse_node(node.child_nodes[2])

                self.current_procedure_declaration['identifier'] = self.current_program_identifier
                self.current_procedure_declaration['parameters'] = self.parameter_declarations
                self.procedure_declarations.append(self.current_procedure_declaration)

                self.current_procedure_declaration = {'identifier': '', 'parameters': []}
                self.parameter_declarations = []


            # each declaration will add value

            elif node_val.value=="variable-declarations":
                self.parse_node(node.child_nodes[0])

                if node_val.value=="declarations-list":
                     self.parse_node(node.child_nodes[0])

            elif node_val.value == 'procedure-identifier':
                if node.parent.value.value == 'program':
                    self.program_identifier = node.child_nodes[0].value.value
                self.current_program_identifier = node.child_nodes[0].value.value

            elif node_val.value == 'declaration':
                self.current_parameter_declaration = {'identifiers': [], 'attributes': []}
                self.parameter_declarations.append(self.current_parameter_declaration)

            elif node_val.value == 'variable-identifier':
                self.current_parameter_declaration['identifiers'].append(
                    node.child_nodes[0].value.value)

            elif node_val.value == 'attribute':
                self.current_parameter_declaration['attributes'].append(
                    node.child_nodes[0].value.value)
        else:
            pass

        for node in node.child_nodes:

            self.parse_node(node)

    def translate(self, filename):
        global  tmt
        tree = my_parser.parse(filename)

        self.parse_node(tree.root)

        print(self.program_date)
        result = ''

        errors = []

        code_section = 'codeSeg SEGMENT\n \t\t ASSUME cs:code1, ds:dataSeg, ss:stackSeg\n'
        data_section = 'dataSeg SEGMENT\n'
        stack_section = 'stackSeg SEGMENT\n\tdb 4096 dup (?)\nstackSeg ends\n\n'

        ext_params = []
        proc_identifiers = []
        for proc_decl in self.procedure_declarations:

            idn_lexem = proc_decl['identifier']
            if idn_lexem.text in proc_identifiers :
                errors.append(CompilationError('Generator', idn_lexem.line, idn_lexem.column,
                                               'identifier "{}" already exists'.format(idn_lexem.text)))
                continue
            proc_identifiers.append(idn_lexem.text)
            code_section += idn_lexem.text + ' proc\n'

            total_parameter_length = 4
            param_identifiers = []
            for parameter in proc_decl['parameters']:

                
                # determine type of parameters and its length

                basic_type = None
                compound_type = None
                contains_ext = False
                for attribute in parameter['attributes']:
                    if attribute.text == 'INTEGER' or attribute.text == 'FLOAT' \
                            or attribute.text == 'BLOCKFLOAT':
                        if basic_type is not None:
                            errors.append(CompilationError('Generator', attribute.line, attribute.column,
                                                           'attribute "{}" can`t be used together with attribute '
                                                           '"{}"'.format(attribute.text, basic_type)))
                        basic_type = attribute.text
                    elif attribute.text == 'COMPLEX' or attribute.text == 'SIGNAL':
                        if compound_type is not None:
                            errors.append(CompilationError('Generator', attribute.line, attribute.column,
                                                           'attribute "{}" can`t be used together with attribute '
                                                           '"{}"'.format(attribute.text, compound_type)))
                        compound_type = attribute.text
                    elif attribute.text == 'EXT':
                        contains_ext = True

                parameter_memory_size = 4
                if basic_type == 'INTEGER' or basic_type == 'FLOAT':
                    parameter_memory_size = 4
                if compound_type == 'COMPLEX':
                    parameter_memory_size *= 2


                for idn in parameter['identifiers']:
                    if idn.text in param_identifiers:
                        errors.append(CompilationError('Generator', idn.line, idn.column,
                                                       'parameter "{}" already defined'.format(idn.text)))
                    param_identifiers.append(idn.text)

                    if not contains_ext:
                        code_section += '\t@{}\t equ \t [bp+{}]\n'.format(idn.text, total_parameter_length)
                        total_parameter_length += parameter_memory_size
                    else:
                        if idn.text not in ext_params:
                            ext_params.append(idn.text)
                            data_section += '\t{} \t db\t{} dup (0)\n'.format(idn.text, parameter_memory_size)


            code_section += '\t\t push bp\n'
            code_section += '\t\t mov bp, sp\n\n'

            code_section += '\t\t pop bp\n'
            if total_parameter_length - 4 != 0:
                code_section += '\t\t retn ' + str(total_parameter_length - 4) + '\n'
            else:
                code_section += '\t\t ret\n'

            code_section += idn_lexem.text + ' endp\n\n'



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