print (ord('4'))
if symbol == '[':
    buffer += symbol
    symbol = f.read(1)
    count_position += 1
    if symbol == '<':
        buffer += symbol
        symbol = f.read(1)
        count_position += 1
        if ord(symbol) > 47 and ord(symbol) < 51:
            buffer += symbol
            symbol = f.read(1)
            count_position += 1
            if ord(symbol) > 47 and ord(symbol) < 53:
                buffer += symbol
                symbol = f.read(1)
                count_position += 1
                if symbol == ':':
                    buffer += symbol
                    symbol = f.read(1)
                    count_position += 1
                    if ord(symbol) > 47 and ord(symbol) < 58:
                        buffer += symbol
                        symbol = f.read(1)
                        count_position += 1
                        if ord(symbol) > 47 and ord(symbol) < 58:
                            buffer += symbol
                            symbol = f.read(1)
                            count_position += 1
                            if symbol == '>':
                                buffer += symbol
                                symbol = f.read(1)
                                count_position += 1
                                if symbol == ']':
                                    buffer += symbol
                                    symbol = f.read(1)
                                    count_position += 1

                                    if buffer in key_words:
                                        result.append(
                                            Lexem(count_line, count_position, dict_of_key_words[buffer],
                                                  buffer))
                                        buffer = ''
                                        count_position += 1
                                    else:
                                        if buffer in dict_of_identificators.keys():
                                            result.append(Lexem(count_line, count_position,
                                                                dict_of_identificators[buffer], buffer))
                                            buffer = ''



        if symbol == '<':
            buffer += symbol
            symbol = f.read(1)
            count_position += 1
            if symbol == '(':
                buffer += symbol
                symbol = f.read(1)
                count_position += 1
                if symbol == '0':
                    buffer += symbol
                    symbol = f.read(1)
                    count_position += 1
                    if symbol == '5' or symbol == '6':
                        buffer += symbol
                        symbol = f.read(1)
                        count_position += 1
                        if symbol == '0' or symbol == '7':
                            buffer += symbol
                            symbol = f.read(1)
                            count_position += 1
                            if symbol == ')':
                                buffer += symbol
                                symbol = f.read(1)
                                count_position += 1
                                if (ord(symbol) > 48 and ord(symbol) < 57) or (ord(symbol) > 64 and ord(symbol) < 91):
                                    buffer += symbol
                                    symbol = f.read(1)
                                    count_position += 1
                                    if (ord(symbol) > 48 and ord(symbol) < 57) or (
                                            ord(symbol) > 64 and ord(symbol) < 91):
                                        buffer += symbol
                                        symbol = f.read(1)
                                        count_position += 1
                                        if (ord(symbol) > 48 and ord(symbol) < 57) or (
                                                        ord(symbol) > 64 and ord(symbol) < 91):
                                            buffer += symbol
                                            symbol = f.read(1)
                                            count_position += 1
                                            if symbol == '-':
                                                buffer += symbol
                                                symbol = f.read(1)
                                                count_position += 1
                                                if ord(symbol) > 64 and ord(symbol) < 91:
                                                    buffer += symbol
                                                    symbol = f.read(1)
                                                    count_position += 1
                                                    if ord(symbol) > 64 and ord(symbol) < 91:
                                                        buffer += symbol
                                                        symbol = f.read(1)
                                                        count_position += 1
                                                        if symbol == '-':
                                                            buffer += symbol
                                                            symbol = f.read(1)
                                                            count_position += 1
                                                            if ord(symbol) > 47 and ord(symbol) < 58:
                                                                buffer += symbol
                                                                symbol = f.read(1)
                                                                count_position += 1
                                                                if ord(symbol) > 47 and ord(symbol) < 58:
                                                                    buffer += symbol
                                                                    symbol = f.read(1)
                                                                    count_position += 1
                                                                    if symbol == '>':
                                                                         buffer += symbol
                                                                         symbol = f.read(1)
                                                                         count_position += 1
                                                                    if buffer in key_words:
                                                                        result.append(Lexem(count_line, count_position,
                                                                                            dict_of_key_words[buffer],
                                                                                            buffer))
                                                                        buffer = ''
                                                                        count_position += 1
                                                                    else:
                                                                        if buffer in dict_of_identificators.keys():
                                                                            result.append(
                                                                                Lexem(count_line, count_position,
                                                                                      dict_of_identificators[buffer],
                                                                                      buffer))
                                                                            buffer = ''

                                                                        else:
                                                                            dict_of_identificators[
                                                                                buffer] = identificators_count
                                                                            result.append(
                                                                                Lexem(count_line, count_position,
                                                                                      identificators_count, buffer))
                                                                            identificators_count += 1
                                                                            buffer = ''