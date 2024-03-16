from lark import Lark, Transformer, v_args

c_grammar = """
    start: type_specifier declarator ";"
    type_specifier: "void" | "char" | "short" | "int" | "long" | "float" | "double" | "signed" | "unsigned"
    declarator: direct_declarator
    direct_declarator: (IDENTIFIER | "(" declarator ")") declarator_suffix*
    declarator_suffix: "[" constant_expression? "]" | "(" parameter_type_list? ")"
    parameter_type_list: parameter_list ("," "...")?
    parameter_list: parameter_declaration ("," parameter_declaration)*
    parameter_declaration: type_specifier declarator
    constant_expression: NUMBER
    IDENTIFIER: /[a-zA-Z_][a-zA-Z_0-9]*/
    NUMBER: /\d+/
    %import common.WS
    %ignore WS
"""


class CTransformer(Transformer):
    @v_args(inline=True)
    def start(self, type_specifier, declarator):
        return {"type": type_specifier, "declarator": declarator}

    def type_specifier(self, children):
        return str(children[0])

    @v_args(inline=True)
    def declarator(self, direct_declarator):
        return direct_declarator

    @v_args(inline=True)
    def direct_declarator(self, children):
        return {"name": str(children[0]), "parameters": children[1:]}

    @v_args(inline=True)
    def declarator_suffix(self, children):
        return children

    @v_args(inline=True)
    def parameter_type_list(self, children):
        return children

    @v_args(inline=True)
    def parameter_list(self, children):
        return children

    @v_args(inline=True)
    def parameter_declaration(self, type_specifier, declarator):
        return {"type": type_specifier, "declarator": declarator}

    def constant_expression(self, children):
        return int(children[0])

    def IDENTIFIER(self, token):
        return str(token)

    def NUMBER(self, token):
        return int(token)


def parse_c(c_code):
    parser = Lark(c_grammar, parser='lalr', transformer=CTransformer())
    return parser.parse(c_code)


code = """
int add(int a, int b);
"""

print(parse_c(code))
