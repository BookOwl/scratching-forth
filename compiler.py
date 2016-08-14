from collections import namedtuple as NT
import zipfile
import io
import os
import json

Literal     = NT("Literal", "val")
IfElse      = NT("IfElse", "if_clause else_clause")
Call        = NT("Call", "name")
Word        = NT("Word", "name code")
ParseResult = NT("ParseResult", "main vars words")

def parse(code: str) -> ParseResult:
    "Parses `code` and returns a ParseResult"
    tokens = list(reversed(code.split()))
    vars_ = []
    defs = []
    main = []
    if_clause = []
    else_clause = []
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
            word_def = []
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

def compile_code(code: str, path: str) -> None:
    "Compiles `code` into a sb2 files and writes it out at `path`"
    with open(path, "wb") as f:
        f.write(compile_to_sb2(parse(code)).getvalue())

def compile_to_sb2(pr: ParseResult) -> io.BytesIO:
    "Takes a ParseResult and returns a io.BytesIO object that can be written to a sb2"
    zip_bytes = io.BytesIO()
    sb2 = zipfile.ZipFile(zip_bytes, "w")
    for filename in os.listdir("scratching forth base"):
        if filename not in ("project.json", ".DS_Store"):
            sb2.write(os.path.join("scratching forth base", filename), arcname=filename, compress_type=zipfile.ZIP_DEFLATED)
    with open("scratching forth base/project.json") as f:
        scripts = json.load(f)
    compiled = compile_json(pr)
    #print(json.dumps(compiled))
    scripts["children"][0]["scripts"].extend(compiled)
    #print(scripts)
    scripts_json = json.dumps(scripts)
    sb2.writestr("project.json", scripts_json)
    sb2.close()
    return zip_bytes

def compile_json(pr: ParseResult) -> list:
    "Compiles pr into json"
    def create_main(scripts):
        return [0, 0, [["whenGreenFlag"], ["call", "INIT"], *scripts]]
    def create_word(name, scripts):
        return [200, 0, [["procDef", name, [], [], True], *scripts]]
    def compile_token(token):
        if isinstance(token, Literal):
            return [["call", "PUSH %s", token.val]]
        elif isinstance(token, IfElse):
            return [["setVar:to:", "~branch?", ["getLine:ofList:", "last", "DATA STACK"]],
                    ["deleteLine:ofList:", "last", "DATA STACK"],
                    ["doIfElse", ["=", ["readVariable", "~branch?"], ["not", False]],
                     extract(token.if_clause),
                     extract(token.else_clause)]]
        elif isinstance(token, Call):
            return [["call", token.name]]
    def extract(code):
        c = []
        for tok in code:
            c.extend(compile_token(tok))
        return c
    main = create_main(extract(pr.main))
    words = [create_word(word.name, extract(word.code)) for word in pr.words]
    return [main, *words]

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

def test_parser() -> None:
    "Simple tests for the parser"
    tests = (
        ": RINSE  FAUCETS OPEN  TILL-FULL  FAUCETS CLOSE ;",
        "1 1 + .",
        "1 1 ( this is a comment ) + .",
        "1 1 = IF 1 ELSE 2 THEN .",
        "1 2 = IF 1 ELSE 1 1 = IF 2 ELSE 3 THEN THEN .",
        "VARIABLE foo 1 .",
        """: FACT dup 1 = IF pop 1 ELSE dup 1 - FACT * THEN ;
           5 FACT .""",
        "FALSE IF 1 ELSE FALSE IF 2 ELSE TRUE IF 3 ELSE 4 THEN THEN THEN",
        )
    for test in tests:
        pr = parse(test)
        print(pr)
        print()

if __name__ == '__main__':
    compile_code("1 1 + .", "1_plus_1.sb2")
    compile_code("1 1 = . CR 1 2 = .", "equals.sb2")
