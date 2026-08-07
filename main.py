# DO NOT take this language serious

# done in python because I cannot be fucked to do string processing in C
# but will rewrite in C after exams
# or make a real compiler
# anyway I'm a crepe I am a weirdough waffle hell am i doing here i doughnut belong here

# so basically everything is global scope, why, because simple language you write in an evening
# and this prohibits feature creep like in brackish
# semi decent crepes are relatively easy to make
# .:. this is a testament to the simplicity of crepes
# this is jit interpreted because crepes can be done one step at a time and skipped about

lines = []
stack = []
storage = []
with open("./test.pnck", "r") as f:
    lines = list(map(lambda elem: elem.strip(), f.readlines()))

prog_cnt = 0
store_ptr = [0,]

# this parses the current stack into an AST, which is overkill but some crepes do be like that
# this is within the mind of the goblin
def goblin(line: list, idx: int):
    # in the llvm toolchain (specifically clang frontend),
    # there are declarations, statements, and types as base AST nodes
    # here, everything is a statement

    # note how I don't check for things.
    # this is because crepes don't tell you if you prepare it correctly

    # this uses riscv because it is risky making crepes for lactose intolerant people

    # before, i used raw evaluation, but ykw i want to do it semi properly
    # the comments for this looked like that:
    ### these are technically _not_ AST nodes
    ### i am skipping parsing, semantic anal, ir + ssa / sexpr tree, optimisation
    ### and doing code gen straight away
    ### but technically crepes are pancakes
    ### :trollface:
    # now it does resemble AST nodes
    match line[0]: # needs check
        ####################### built-in commands
        # looping
        case "goto":
            return [{"stmt": "biltin", "actual": "j", "relative": line[1] - idx},]
        # functions (are always called with the entire stack)
        case "call":
            return [{"stmt": "biltin", "actual": "call", "func": line[1], "args": [*stack]},]
        # conditionals
        case "if":
            return [{"stmt": "bltin", "actual": "bnez", "cond": stack[-1],
                    "True": goblin(["goto", line[1]], idx),
                    "False": goblin(["goto", line[2]], idx)},]
        ####################### stack opcodes
        # adding to stack
        case "push":
            return [{"stmt": "stkpsh", "stkarg": line[1]},]
        case "load":
            return [{"stmt": "stkpsh", "stkarg": storage[store_ptr[0]]}, goblin(["burst",], idx)]
        # removing from stack
        case "pop":
            return [{"stmt": "stkpop"},]
        ####################### storage opcodes
        case "get":
            return [{"stmt": "stopsh", "stoarg": stack[-1]}, goblin(["pop",], idx)]
        case "burst":
            return [{"stmt": "stopop"},]
        ####################### storage pointer opcodes
        case "store":
            if store_ptr[0] > len(storage):
                raise GeneratorExit("not a generator")
            return [{"stmt": "sprset", "sprarg": int(line[1])},]
        # storage pointer increase
        case "incr":
            return [{"stmt": "sprset", "sprarg": store_ptr[0] + 1},]
        case "decr":
            return [{"stmt": "sprset", "sprarg": store_ptr[0] - 1},]
        case "last":
            return [{"stmt": "sprset", "sprarg": len(storage)},]
        case _:
            raise OSError("this is an os error. my os (emacs) cannot fathom the bullshittery you put into the code and i will not help you with your code because crepes dont give you feedback")

while prog_cnt < len(lines):
    operation = lines[prog_cnt]

    # comments like ligma balls (ligma is a valuable comment)
    if operation.startswith('\\'):
        prog_cnt += 1
        continue

    # tokenisation like deez nuts (do you know what tokenises? DEEZ NUTS!!!)
    tokens = []
    was_spch_seen = False
    string = ""
    for char in operation:
        if char == '"':
            if was_spch_seen:
                tokens.append('"' + string + '"')
                string = ""
            was_spch_seen = not was_spch_seen
        elif char == ' ' and not was_spch_seen:
            tokens.append(string)
            string = ""
        else:
            string += char
    tokens.append(string)

    # parsing like mind goblin (these goblins parse with their minds)
    #match (
    ast_subtree = goblin(tokens, prog_cnt)

    # evaluation with custom dsl like kenya
    for node in ast_subtree:
        match node["stmt"]:
            case "biltin":
                # case stmt with all the builtins
                pass
            case "stkpsh":
                stack.push(node["stkarg"])
            case "stkpop":
                stack.pop()
            case "stopsh":
                storage.push(node["stoarg"])
            case "stopop":
                storage.pop(store_ptr[0])
            case "sprset":
                store_ptr[0] = node["sprarg"]

    prog_cnt += 1

