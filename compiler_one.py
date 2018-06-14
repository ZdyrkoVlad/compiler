import my_parser
from parser_tree import CompilationError
global a

class Generator():
    global a
    a=False
    def __init__(self):
        self.procedure_declarations = []
        self.parameter_declarations = []
        self.program_identifier = ''
        self.program_date=[]


        self.current_procedure_declaration = {'identifier': '', 'parameters': []}
        self.current_parameter_declaration = {'identifier': '', 'parameters': []}
        self.current_program_identifier = ''
        self.current_program_date={'identifier':'','attribute':[]}

    def parse_node1(self,node):
        node_val = node.value
        global  a

        if node_val.value == 'declaration':
            a = True
            self.current_program_date = {'identifiers': [], 'attributes': []}
            self.program_date.append(self.current_parameter_declaration)

        elif node_val.value == 'variable-identifier':
            self.current_program_date['identifiers'].append(
                node.child_nodes[0].value.value)

        elif node_val.value == 'attribute':
            self.current_program_date['attributes'].append(
                node.child_nodes[0].value.value)

        for node in node.child_nodes:
            self.parse_node1(node)


    def parse_node(self, node):


        node_val = node.value
        # print(str(node_val.value))
        # print( str(node_val))
        # print(str(node_val.value_type))

        if node_val.value=='variable-declarations':
            print('VAR')
            self.parse_node1(node)

            if node_val.value == 'declaration':
                self.current_program_date = {'identifiers': [], 'attributes': []}
                self.program_date.append(self.current_parameter_declaration)

            elif node_val.value == 'variable-identifier':
                self.current_program_date['identifiers'].append(
                    node.child_nodes[0].value.value)

            elif node_val.value == 'attribute':
                self.current_program_date['attributes'].append(
                    node.child_nodes[0].value.value)

            for node in node.child_nodes:
                self.parse_node(node)


        # for each declaration new
        if node_val.value == 'program':
            # print("ONE")
            self.parse_node(node.child_nodes[1])
            self.parse_node(node.child_nodes[2])


            self.current_procedure_declaration['identifier'] = self.current_program_identifier
            self.current_procedure_declaration['parameters'] = self.parameter_declarations
            self.procedure_declarations.append(self.current_procedure_declaration)

            self.current_procedure_declaration = {'identifier': '', 'parameters': []}
            self.parameter_declarations = []

        # each declaration will add value
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


        for node in node.child_nodes:
            self.parse_node(node)

    def translate(self, filename):
        global  a
        tree =my_parser.parse(filename)
        print(tree)
        self.parse_node(tree.root)

        result = ''

        errors = []

        code_section = 'codeSeg SEGMENT\n \t\t ASSUME cs:code1, ds:dataSeg, ss:stackSeg\n'
        data_section = 'dataSeg SEGMENT\n'
        stack_section = 'stackSeg SEGMENT\n\tdb 4096 dup (?)\nstackSeg ends\n\n'

        ext_params = []
        proc_identifiers = []
        param_identifiers = []
        data_indefiers=[]
        contains_ext = False

        #print(str(self.parameter_declarations))
        print(self.program_date)


        for proc_decl in self.procedure_declarations:
            idn_lexem = proc_decl['identifier']
            #print( proc_decl['identifier'])
            if idn_lexem.text in proc_identifiers or idn_lexem.text == self.program_identifier:
                errors.append(CompilationError('Generator', idn_lexem.line, idn_lexem.column,
                                               'identifier "{}" already exists'.format(idn_lexem.text)))
                continue
            proc_identifiers.append(idn_lexem.text)
            code_section += idn_lexem.text + ' proc\n'

            total_parameter_length = 4

            for parameter in proc_decl['parameters']:
                # determine type of parameters and its length

                basic_type = None
                compound_type = None

                for attribute in parameter['attributes']:
                    print(basic_type)


                    if attribute.text == 'INTEGER' or attribute.text == 'FLOAT' \
                            or attribute.text == 'BLOCKFLOAT':

                        if basic_type is not None or basic_type=='EXT':
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
                        if basic_type==None:
                            errors.append(CompilationError('Generator', attribute.line, attribute.column,
                                                           'attribute "{}" can`t be used together with attribute '
                                                           '"{}"'.format(attribute.text, compound_type)))
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

        basic_type = None
        compound_type = None
        if a == True:

            for indet in self.current_program_date['attributes']:
                print(indet.text)
                if indet.text == 'INTEGER' or indet.text == 'FLOAT' \
                        or indet.text == 'BLOCKFLOAT':
                    if basic_type is not None:
                        errors.append(CompilationError('Generator', indet.line, indet.column,
                                                       'attribute "{}" can`t be used together with attribute '
                                                       '"{}"'.format(indet.text, basic_type)))
                    basic_type = indet.text

                elif indet.text == 'COMPLEX' or indet.text == 'SIGNAL':
                    if compound_type is not None:
                        errors.append(CompilationError('Generator', indet.line, indet.column,
                                                       'attribute "{}" can`t be used together with attribute '
                                                       '"{}"'.format(indet.text, compound_type)))
                    compound_type = indet.text

            parameter_memory_size = 4
            if basic_type == 'INTEGER' or basic_type == 'FLOAT':
                parameter_memory_size = 4
            if compound_type == 'COMPLEX':
                parameter_memory_size *= 2

            for indet1 in self.current_program_date['identifiers']:
                if contains_ext==True:
                    if indet1.text in param_identifiers:
                        errors.append(CompilationError('Generator', indet1.line, indet1.column,
                                                       'identifier "{}" already exists'.format(indet1.text)))
                        continue
                elif indet1.text in data_indefiers:
                    errors.append(CompilationError('Generator', indet1.line, indet1.column,
                                                   'identifier "{}" already exists'.format(indet1.text)))
                    continue
                data_indefiers.append(indet1.text)
                param_identifiers.append(indet1.text)
                print(indet1.text)
                data_section += '\t{} \t db\t{} dup (0)\n'.format(indet1.text, parameter_memory_size)

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