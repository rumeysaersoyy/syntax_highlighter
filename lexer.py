import re

TOKEN_SPEC = [
    ('KEYWORD',   r'\b(if|while|print|else|elif|True|False)\b'),
    ('BOOL',      r'\b(True|False)\b'),
    ('NUMBER',    r'\d+(\.\d+)?'),
    ('STRING',    r'(\".*?\"|\'.*?\')'),
    ('IDENTIFIER',r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('OPERATOR',  r'(==|!=|<=|>=|[+\-*/=<>])'),
    ('DELIMITER', r'[:(),]'),
    ('COMMENT',   r'#.*'),
    ('WHITESPACE',r'[ \t]+'),
    ('NEWLINE',   r'\n')
]

master_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC)
token_pattern = re.compile(master_regex)

def tokenize(code):
    tokens = []
    indent_stack = [0]
    line_num = 1
    pos = 0
    line_start = 0
    
    while pos < len(code):
        if code[pos] == '\n':
            tokens.append(('NEWLINE', '\n', line_num, pos - line_start))
            pos += 1
            line_num += 1
            line_start = pos

            space_count = 0
            while pos < len(code) and code[pos] in ' \t':
                if code[pos] == ' ':
                    space_count += 1
                elif code[pos] == '\t':
                    space_count += 4
                pos += 1
            
            if space_count > indent_stack[-1]:
                indent_stack.append(space_count)
                tokens.append(('INDENT', '', line_num, 0))
            else:
                while space_count < indent_stack[-1]:
                    indent_stack.pop()
                    tokens.append(('DEDENT', '', line_num, 0))
            continue

        match = token_pattern.match(code, pos)
        if not match:
            raise SyntaxError(f'Unknown token at line {line_num} col {pos - line_start}')
        
        kind = match.lastgroup
        value = match.group(kind)
        column = pos - line_start
        
        if kind == 'WHITESPACE':
            pass
        elif kind == 'NEWLINE':
            pass
        else:
            tokens.append((kind, value, line_num, column))
        
        pos = match.end()

    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(('DEDENT', '', line_num, 0))

    tokens.append(('EOF', '', line_num, 0))
    return tokens

if __name__ == "__main__":
    test_code = '''\
x = 5
if x > 3:
    print(x)
    if True:
        print("nested")
print("done")
'''
    for t in tokenize(test_code):
        print(t)
