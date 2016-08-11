from collections import namedtuple as NT
from typing import Union, List

Literal     = NT("Literal", "val")
IfElse      = NT("IfElse", "if_clause else_clause")
Call        = NT("Call", "name")
Word        = NT("Word", "name code")
ParseResult = NT("ParseResult", "main vars words")

# typing types
Token = List[Union[Literal, Call, IfElse]]
def parse(code: str) -> ParseResult:
    "Parses `code` and returns a ParseResult"
    tokens = list(reversed(code.split()))
    vars_ = []
    defs = [] # type: List[Word]
    main = [] # type: Token
    if_clause = [] # type: Token
    else_clause = [] # type: Token
    cur = [main]
    while tokens:
        token = tokens.pop()
        if token == "IF":
            if_clause.append([])
            else_clause.append([])
            cur.append(if_clause[-1])
        elif token == "ELSE":
            cur[-1] = else_clause[-1]
        elif token == "THEN":
            cur.pop()
            cur[-1].append(IfElse(if_clause[-1], else_clause[-1]))
            if_clause.pop()
            else_clause.pop()
        elif token == "VARIABLE":
            vars_.append(tokens.pop())
        elif is_number(token):
            cur[-1].append(Literal(to_number(token)))
        elif token == ":":
            word_name = tokens.pop()
            word_def = [] # type: List[Union[Literal, Call, IfElse]]
            cur.append(word_def)
        elif token == ";":
            word = Word(word_name, word_def)
            defs.append(word)
            cur.pop()
        elif token == "(":
            while tokens.pop() != ")":
                pass
        elif token in vars_:
            cur[-1].append(Literal(token))
        else:
            cur[-1].append(Call(token))
    return ParseResult(main, vars_, defs)

def is_number(token: str) -> bool:
    "Predicate to determine if `token` is a number"
    try:
        float(token)
    except ValueError:
        return False
    else:
        return True

def to_number(token: str) -> float:
    "Converts `token` to a number"
    return float(token)

if __name__ == '__main__':
    tests = (
        ": RINSE  FAUCETS OPEN  TILL-FULL  FAUCETS CLOSE ;",
        "1 1 + .",
        "1 1 ( this is a comment ) + .",
        "1 1 == IF 1 ELSE 2 THEN .",
        "1 2 == IF 1 ELSE 1 1 == IF 2 ELSE 3 THEN THEN .",
        "VARIABLE foo 1 .",
        """: FACT dup 1 == IF pop 1 ELSE dup 1 - FACT * THEN ;
           5 FACT .""",
        "FALSE IF 1 ELSE FALSE IF 2 ELSE TRUE IF 3 ELSE 4 THEN THEN THEN",
        )
    for test in tests:
        pr = parse(test)
        print(pr)
        print()
