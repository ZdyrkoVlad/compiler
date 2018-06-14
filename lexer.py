dict_of_key_words = {"PROCEDURE": 401, "BEGIN": 402, "END": 403, "VAR": 404,"SIGNAL":405,"COMPLEX":406,"INTEGER":407,
                     "FLOAT":408,"BLOCKFLOAT":409,"EXT":410,"ENDIF":411,"IF":412,"THEN":413,"ELSE":414}
list_of_separetors = ["(",")",";",":",","]
dict_of_identificators = {}


class Lexem:
    def __init__(self, line, column, id, text):
        self.line = line
        self.column = column
        self.id = id
        self.text = text

    def __str__(self):
        return "{}, {}\t| {}  {}".format(self.line, self.column, self.id, self.text)

class LexerError:
    def __init__(self, line, column, msg):
        self.line = line
        self.column = column
        self.msg = msg

    def __str__(self):
        return "Lexer error ({}, {}): {}".format(self.line, self.column, self.msg)


def lex(file):
    white_space = [32, 13, 10, 9, 11, 12,95]
    digits = [i for i in range(48, 57)]
    chars = [i for i in range(65, 90)] + [i for i in range(97, 123)]
    separetors = list_of_separetors
    key_words = [i for i in dict_of_key_words.keys()]
    buffer = ''
    result = []
    errors = []
    identificators_count = 1001
    count_line = 1
    count_position = 1

    f = open(file)
    symbol = f.read(1)

    while symbol:


        if symbol == "\n":
            count_line += 1
            count_position = 0

        if ord(symbol) in white_space:
            symbol = f.read(1)
            count_position+=1





        elif ord(symbol) in chars:
            buffer = ''
            buffer += symbol
            symbol = f.read(1)
            count_position += 1
            while symbol and (ord(symbol) in chars or ord(symbol) in digits):
                buffer += symbol
                symbol = f.read(1)
                count_position += 1
            if buffer in key_words:
                result.append(Lexem(count_line, count_position, dict_of_key_words[buffer], buffer))
                buffer = ''
                count_position += 1
            else:
                if buffer in dict_of_identificators.keys():
                    result.append(Lexem(count_line, count_position, dict_of_identificators[buffer], buffer))
                    buffer = ''

                else:
                    dict_of_identificators[buffer] = identificators_count
                    result.append(Lexem(count_line, count_position, identificators_count, buffer))
                    identificators_count += 1
                    buffer = ''









        elif symbol == '(':
            symbol = f.read(1)
            count_position += 1
            if symbol == '*':
                symbol = f.read(1)
                count_position += 1
                while symbol:
                    if symbol=='\n':
                        count_line+=1
                        count_position=0
                    if symbol == '*':
                        symbol = f.read(1)
                        count_position += 1
                        if symbol == ')':
                            symbol = f.read(1)
                            count_position += 1
                            break;
                    else:
                        symbol = f.read(1)
                        count_position += 1

                if not symbol:
                    errors.append(LexerError(count_line, count_position, "comment unclosed"))
            else:

                result.append(Lexem(count_line, count_position-1, ord("("), "("))


        elif symbol in separetors:
            count_position += 1
            result.append(Lexem(count_line, count_position, ord(symbol), symbol))
            symbol = f.read(1)


        else:
            errors.append(LexerError(count_line, count_position, "unknown symbol '{}'".format(symbol)))
            symbol = f.read(1)
            count_position += 1


    f.close()
    # print("Lexems:")
    # for res in result:
    #      print(res)
    # print('-'*50)
    # for err in errors:
    #     print(err)
    return result


if __name__ == '__main__':
    lex("TEST.txt")