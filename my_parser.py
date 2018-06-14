import lexer
from parser_tree import Tree, TreeValue

lexems = lexer.lex('parser_true_test.txt')
tree = Tree()



errors = {0: "keyword error", 1: "identifier error",
          2: "unexpected symbol error", 3: "attribute error"}
parser_errors = []
lexem_counter = 0


def get_dict_key(dictionary, value):
    for k, v in dictionary.items():
        if v == value:
            return k


def read_lexem():
    global lexem_counter
    lex = lexems[lexem_counter]
    lexem_counter += 1
    return lex


def err(err_code, line, column, expected='', obtained=''):
    if expected:
        error = "Syntax error ({}, {}): {}: '{}' expected, but received '{}'".format(
            line, column, errors[err_code], expected, obtained)
    else:
        error = "Syntax error ({}, {}): {}".format(
            line, column, errors[err_code])
    print(tree)
    print(error)
    quit()


def separator(ch, lex, prevent_error=False):
    if lex.id == ord(ch):
        tree.add_node(TreeValue(3, lex))
    elif prevent_error:
        return False
    else:
        err(2, lex.line, lex.column, ch, lex.text)
    return True


def keyword(code, lex, prevent_error=False):
    if lex.id == code:
        tree.add_node(TreeValue(1, lex))
    elif prevent_error:
        return False
    else:
        err(0, lex.line, lex.column, get_dict_key(
            lexer.dict_of_key_words, code), lex.text)
    return True


def attribute(lex, prevent_error=False):
    if 405 <= lex.id < 411:
        tree.add_node(TreeValue(0, 'attribute'), change_current=True)
        tree.add_node(TreeValue(1, lex))
        tree.switch_to_parent()
    elif prevent_error:
        return False
    else:
        err(3, lex.line, lex.column, 'attribute', lex.text)
    return True


def identifier(lex, idn_type, prevent_error=False):
    tree.add_node(TreeValue(0, idn_type + '-identifier'), change_current=True)
    if lex.id > 1000:
        tree.add_node(TreeValue(2, lex))
        tree.switch_to_parent()
    elif prevent_error:
        return False
    else:
        err(1, lex.line, lex.column, 'identifier', lex.text)
    return True


def attributes_list_func():
    ''' <attribute> <attributes-list> | <empty>'''

    tree.add_node(TreeValue(0, 'attributes-list'), change_current=True)
    lex = read_lexem()
    if attribute(lex, prevent_error=True):
        lex = attributes_list_func()
    else:
        tree.add_node(TreeValue(0, 'empty'))
    tree.switch_to_parent()
    return lex


def identifiers_list_func():
    ''', <variable-identifier> <identifiers-list> | <empty> '''

    tree.add_node(TreeValue(0, 'identifiers-list'), change_current=True)
    lex = read_lexem()
    if separator(',', lex, prevent_error=True):
        identifier(read_lexem(), 'variable')
        lex = identifiers_list_func()
    else:
        tree.add_node(TreeValue(0, 'empty'))
    tree.switch_to_parent()
    return lex



def declarations():
    variable_declarations()


def declaration_func():
    ''' <variable-identifier> <identifiers-list> : <attribute> <attributes-list>; '''

    lex = read_lexem()
    if lex.id > 1000:
        tree.add_node(TreeValue(0, 'declaration'), change_current=True)
        tree.add_node(TreeValue(0, 'variable-identifier'), change_current=True)
        tree.add_node(TreeValue(2, lex))
        tree.switch_to_parent()
    else:
        return lex

    lex = identifiers_list_func()
    if not lex:
        lex = read_lexem()
    separator(':', lex)
    attribute(read_lexem())
    lex = attributes_list_func()
    if lex is None:
        lex = read_lexem()
    separator(';', lex)
    tree.switch_to_parent()
    return None


def declaration_list_func():
    ''' <declaration> <declarations-list> | <empty> '''

    tree.add_node(TreeValue(0, 'declarations-list'), change_current=True)
    lex = declaration_func()
    if not lex:
        lex = declaration_list_func()
    else:
        tree.add_node(TreeValue(0, 'empty'))
    tree.switch_to_parent()
    return lex


def parameters_list_func():
    ''' ( <declarations-list> ) | <empty> '''

    tree.add_node(TreeValue(0, 'parameters-list'), change_current=True)
    lex = read_lexem()
    if separator('(', lex, prevent_error=True):
        lex = declaration_list_func()
        if not lex:
            lex = read_lexem()
        separator(')', lex)
        lex = None
    else:
        tree.add_node(TreeValue(0, 'empty'))
    tree.switch_to_parent()
    return lex

def variable_declarations():
    ''' VAR <declarations-list> | <empty>'''

    tree.add_node(TreeValue(0, 'variable-declarations'), change_current=True)
    lex = read_lexem()

    if keyword(404,lex, prevent_error=True):
        lex = declaration_list_func()
    else:
        tree.add_node(TreeValue(0, 'empty'))

    tree.switch_to_parent()
    return  lex


def statements_list():
    '''<conditional-stmt><stmt-lst>|<emty>'''
    tree.add_node(TreeValue(0,'statements-list'),change_current=True)



    lex = coditional_stmt()
    if not lex:
        lex=statements_list()
    else:
        tree.add_node(TreeValue(0,'empty'))

    tree.switch_to_parent()
    return lex



def coditional_stmt():
    '''<cond-if><cond-else>ENDIF'''


    lex=cond_if()
    if lex:
        return lex
    tree.add_node(TreeValue(0, 'coditional_stmt'),change_current=True)
    lex=cond_else()
    if not lex:
        lex=read_lexem()
    keyword(411, lex, prevent_error=True)
    tree.switch_to_parent()

    return None

def cond_if():
    '''IF<attribute>THEN<decl aration>'''

    lex=read_lexem()
    if lex.id == 412:
        tree.add_node(TreeValue(0, 'cond-if'), change_current=True)
        keyword(412,lex)
        attribute(read_lexem(),prevent_error=True)
        keyword(413,read_lexem(),prevent_error=True)

        lex=declaration_func()
        tree.switch_to_parent()
    return lex

def cond_else():
    '''ELSE<identifiers-list>|<empty>'''
    tree.add_node(TreeValue(0,'cond-else'),change_current=True)
    lex=read_lexem()
    if keyword(414,lex,prevent_error=True):
        lex=identifiers_list_func()
    else:
        tree.add_node(TreeValue(0,'empty'))
    tree.switch_to_parent()
    return lex

def block_func():
    ''' <variable-declarations> BEGIN <empty> END '''

    tree.add_node(TreeValue(0, 'block'), change_current=True)
    lex = variable_declarations()
    if not lex:
        lex = read_lexem()

    keyword(402, lex)  # 402 = BEGIN

    lex=statements_list()
    if not lex:
        lex = read_lexem()

    keyword(403, lex)  # 403 = END
    tree.switch_to_parent()


def program_func():
    ''' # PROCEDURE <procedure-identifier><parameters-list>; <block>; '''

    keyword(401, read_lexem())  # 401 = PROCEDURE
    identifier(read_lexem(), 'procedure')
    lex = parameters_list_func()
    if lex is None:
        lex = read_lexem()
    separator(';', lex)
    block_func()

    separator(';', read_lexem())


def parse(filename, print_results=False):
    global lexems
    global tree
    global lexem_counter

    lexems = lexer.lex(filename)
    lexem_counter = 0
    tree = Tree()
    program_func()
    if print_results:
        print(tree)
    return tree

def main():
    parse('parser_true_test.txt', True)

if __name__ == '__main__':
    main()