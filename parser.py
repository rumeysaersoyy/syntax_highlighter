class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '', -1, -1)

    def eat(self, token_type):
        current = self.current_token()
        if current[0] == token_type:
            self.pos += 1
        else:
            line = current[2]
            col = current[3]
            raise Exception(f"Satır {line} Sütun {col}: Beklenen {token_type}, ancak {current[0]} geldi ({current[1]})")

    def parse_program(self):
        while self.current_token()[0] != 'EOF':
            self.parse_statement()

    def parse_statement(self):
        token = self.current_token()
        if token[0] == 'KEYWORD' and token[1] == 'if':
            self.parse_if_statement()
        elif token[0] == 'KEYWORD' and token[1] == 'print':
            self.parse_print_statement()
        elif token[0] == 'IDENTIFIER':
            self.parse_assignment()
        else:
            line = token[2]
            col = token[3]
            raise Exception(f"Satır {line} Sütun {col}: Geçersiz ifade başlangıcı: {token}")

    def parse_if_statement(self):
        self.eat('KEYWORD')  # if
        self.parse_expression()
        self.eat('DELIMITER') # ':'
        self.eat('NEWLINE')
        self.eat('INDENT')
        while self.current_token()[0] != 'DEDENT' and self.current_token()[0] != 'EOF':
            self.parse_statement()
        self.eat('DEDENT')

    def parse_print_statement(self):
        self.eat('KEYWORD')  # print
        self.eat('DELIMITER') # (
        self.parse_expression()
        self.eat('DELIMITER') # )

    def parse_assignment(self):
        self.eat('IDENTIFIER')
        self.eat('OPERATOR')  # =
        self.parse_expression()

    def parse_expression(self):
        token = self.current_token()
        if token[0] in ('IDENTIFIER', 'NUMBER', 'STRING', 'BOOL'):
            self.eat(token[0])
            if self.current_token()[0] == 'OPERATOR':
                self.eat('OPERATOR')
                right = self.current_token()
                if right[0] in ('IDENTIFIER', 'NUMBER', 'STRING', 'BOOL'):
                    self.eat(right[0])
                else:
                    line = right[2]
                    col = right[3]
                    raise Exception(f"Satır {line} Sütun {col}: Beklenen IDENTIFIER, NUMBER, STRING veya BOOL, fakat {right} geldi")
        else:
            line = token[2]
            col = token[3]
            raise Exception(f"Satır {line} Sütun {col}: Geçersiz ifade tokenı: {token}")

if __name__ == "__main__":
    from lexer import tokenize
    code = '''\
x = 5
if x > 3:
    print(x)
    if True:
        print("nested")
print("done")
'''
    tokens = tokenize(code)
    parser = Parser(tokens)
    parser.parse_program()
    print("Parsing başarıyla tamamlandı.")
