# DO NOT take this language serious
# this language was one approach to making an unsettling language,
# making a proper AST which balances itself at runtime would also be great
# but I've done that in a lisp already with an RBTree
# Oh and, these comments contain very strong language
# if this is not to your liking then I advise you to stop here
# With love, disdain, and indifference,
# Simon

# done in python because I cannot be fucked to do string processing in C
# but will rewrite in C after exams
# or make a real compiler
# anyway I'm a crepe I am a weirdough waffle hell am i doing here i doughnut belong here

# so basically everything is global scope, why, because simple language you write in an evening
# and this prohibits feature creep like in brackish
# semi decent crepes are relatively easy to make
# .:. this is a testament to the simplicity of crepes
# this is jit interpreted because crepes can be done one step at a time and skipped about

# ehehehehehehe
# my comrade defines a specialist as such:
# someone that knows enough to get themselves into trouble, but not enough to get them back out of trouble again
# I will let you make that verdict ;)
try:
    from typing import Any
except ImportError: # if the above line fails, try it again
    from typing import Any
finally: # and no matter if it fails, do it again. it was so nice we imported it twice
    from typing import Any

lines = []
stack = []
storage = []
with open("./test.pnck", "r") as f:
    lines = list(map(lambda elem: elem.strip(), f.readlines()))

# those are lists because they are actually pointers
# and global is bad because it pollutes the global namespace
# "but Simon out of all this code, using global would be sane"
# shut up voice of reason, that's not the point
prog_cnt = [0,]
store_ptr = [0,]

# have something sensible
STATEMENT = "stmt"
BUILTIN = "biltin"
BLTN_ACTUAL = "actual"
STACK_PUSH = "stkpsh"
STACK_ARG = "stkarg"
STACK_POP = "stkpop"
STORAGE_PUSH = "stopsh"
STORAGE_ARG = "stoarg"
STORAGE_POP = "stopop"
STORAGE_PTR_SET = "sprset"
STORAGE_PTR_ARG = "sprarg" # sperging out

def coerce_int(value: str, strg: list):
    try:
        strg.append(int(value))
    except ValueError:
        try:
            # it is 4 am set me free please
            strg.append(float(value))
        except ValueError:
            strg.append(value)
    except Exception:
        # if there is any other error you deserve to crash
        raise IsADirectoryError("its called directory, not folder")

# this parses the current stack into an AST, which is overkill but some crepes do be like that
# this is within the mind of the goblin
def goblin(line: list, idx: int) -> list[dict[str, Any]]:
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
    # "but Simon these arent objects"
    # look at meta classes wont you
    # meta mis nueces en tu bocaaaaaaa (put my nuts in your mouth in spanish)
    # pythons underlying type system is dictionaries, so if you squint this is a list of objects
    match line[0]: # needs check
        ####################### built-in commands
        # looping
        case "goto":
            # this doesnt check for oob jumps btw, so good luck XD
            return [{STATEMENT: BUILTIN, BLTN_ACTUAL: "j", "relative": line[1] - idx - 1},]
        # functions (are always called with the entire stack)
        case "call":
            return [{STATEMENT: BUILTIN, BLTN_ACTUAL: "call", "func": line[1], "args": [*stack]},]
        # conditionals
        case "if":
            return [{STATEMENT: BUILTIN, BLTN_ACTUAL: "bnez", "cond": str(bool(stack[-1])),
                    str(True): goblin(["goto", line[1]], idx),
                    str(False): goblin(["goto", line[2]], idx)},]
        ####################### stack opcodes
        # adding to stack
        case "push":
            return [{STATEMENT: STACK_PUSH, STACK_ARG: line[1]},]
        case "load":
            # * because goblin returns a list, this unpacks
            # (unpack deez nuts)
            if store_ptr[0] < 0:
                raise FloatingPointError("voy a su pegar y la rayaraya") # or how that brainrot song went
            return [{STATEMENT: STACK_PUSH, STACK_ARG: storage[store_ptr[0]]}, *goblin(["burst",], idx)]
        case "copy":
            return [{STATEMENT: STACK_PUSH, STACK_ARG: stack[-1]}]
        # removing from stack
        case "pop":
            return [{STATEMENT: STACK_POP},]
        ####################### storage opcodes
        case "get":
            return [{STATEMENT: STORAGE_PUSH, STORAGE_ARG: stack[-1]}, *goblin(["pop",], idx)]
        case "burst":
            return [{STATEMENT: STORAGE_POP},]
        ####################### storage pointer opcodes
        case "store":
            if line[1] > len(storage):
                raise KeyboardInterrupt("useless error uwu read the code")
            return [{STATEMENT: STORAGE_PTR_SET, STORAGE_PTR_ARG: line[1]},]
        # storage pointer increase
        case "incr":
            return [{STATEMENT: STORAGE_PTR_SET, STORAGE_PTR_ARG: store_ptr[0] + 1},]
        case "decr":
            return [{STATEMENT: STORAGE_PTR_SET, STORAGE_PTR_ARG: store_ptr[0] - 1},]
        case "last":
            # this is intentional because len storage just means yeah append it broski
            return [{STATEMENT: STORAGE_PTR_SET, STORAGE_PTR_ARG: len(storage)},]
        case "crlb":
            return [{STATEMENT: BUILTIN, BLTN_ACTUAL: "call", "func": "write", "args": ['\n',]}]
        case "dump":
            ret = []
            for value in ['\n', stack, '\n', store_ptr, '\n', storage]:
                ret.append({STATEMENT: BUILTIN, BLTN_ACTUAL: "call", "func": "write", "args": [value]})
            return ret
        case _:
            # emacs is the best operating system, that unfortunately lacks a text editor
            # or is it _queue the vsauce music_
            raise OSError("this is an os error. my os (emacs) cannot fathom the tomfoolery you put into the code and i will not help you with your code because crepes dont give you feedback")

def eval_atom(ast: dict):
    match ast[STATEMENT]:
        # this makes this horrible to typo check
        # the fix _would_ be to do `case Class.BUILTIN:` but like...
        # I know the fix I just wont implement it here as a statement of rebellion
        # against the corporate slop and influx of meeting bureaucratic correctness
        # use Haskell yo, this is mathematical correctness
        # even if your mental health will plummet
        # work with clang tooling, you will be inspired to take your meds
        # lol
        case "biltin":
            # case stmt with all the builtins
            match ast[BLTN_ACTUAL]: # notice how its not named the same
                case "j":
                    # nevermind that error doesnt happen
                    prog_cnt[0] += ast["relative"]
                case "call":
                    match ast["func"]:
                        # oh this is so peak:
                        # python short circuits, so if an expression is falsy, the second pop wont execute
                        # hahahahahahahahahahahahahahahahaha
                        case "write":
                            print(ast["args"][-1], end="")
                        case "read":
                            inpt = input("\nξ ")
                            coerce_int(inpt, stack)
                        case "bee": # rot1 add
                            # even _if_ stack.pop() wouldnt default to int it would still be turing complete
                            # n would be a string of length n for example, per concatenation theory this suffices
                            # it would be a minsky machine or something, which are turing complete
                            # just... cursed like nothing else
                            stack.append(stack.pop() + stack.pop())
                        case "blt": # sub
                            stack.append(stack.pop() - stack.pop())
                        case "melt": # ^sic
                            stack.append(stack.pop() * stack.pop())
                        case "admin": # untrue mod so you can make it yourself uwu
                            stack.append(stack.pop() % stack.pop())
                        case "dividend": # /
                            stack.append(stack.pop() / stack.pop())
                        # imagine how horrible a language is that flips < and >
                        # yeah... how horrible that would be
                        # (deez nuts)
                        case "strictlylessthan": # gt
                            stack.append(stack.pop() < stack.pop())
                        case "panzerwagengti": # gte. never let them know your next move
                            stack.append(stack.pop() <= stack.pop())
                        case "notstrictlylessthanandnotstrictlygreaterthan": # eq
                            stack.append(stack.pop() == stack.pop())
                        case "strictlylessthanorstrictlygreaterthan": # neq
                            stack.append(stack.pop() != stack.pop())
                        case "strictlygreaterthan": # lt
                            stack.append(stack.pop() > stack.pop())
                        case "notstrinctlylessthan": # lte
                            stack.append(stack.pop() >= stack.pop())
                        case "knot":
                            stack.append(not stack.pop())
                        case "and":
                            stack.append(stack.pop() and stack.pop())
                        case "or":
                            stack.append(stack.pop() or stack.pop())
                        case "shore":
                            stack.append(stack.pop() ^ stack.pop())
                        # who needs nxor (xnor) anyway
                        case _:
                            raise BufferError("idk bro your buffers off")
                case "bnez":
                    for atom in ast[ast["cond"]]:
                        eval_atom(atom)
        case "stkpsh":
            stack.append(ast[STACK_ARG])
        case "stkpop":
            stack.pop()
        case "stopsh":
            # this is called an in place index write (i dont shift after insertion)
            # which makes the semantics inconsistent
            # which is good because now you will suffer when trying to code in this language
            # another possibility is to do `... or store_ptr[0] < -len(storage):` but oh well
            if store_ptr[0] > len(storage) or store_ptr[0] < 0:
                raise SystemError("this is illegal")
            elif store_ptr[0] == len(storage):
                storage.append(ast[STORAGE_ARG])
            else:
                storage[store_ptr[0]] = ast[STORAGE_ARG]
        case "stopop":
            if store_ptr[0] < 0:
                raise ChildProcessError("waa waa pharaoh wants milk")
            storage.pop(store_ptr[0])
        case "sprset":
            # i wont check for negative here, being negative sometimes is a-okay!
            # ;) XD
            store_ptr[0] = ast[STORAGE_PTR_ARG] # redundant but eat a foot pyright
        case _:
            # basically: afaik, in 3.13+ they made the GIL opt out
            # so this python code may not run in versions earlier than 3.13
            # skill issue update your python
            raise PythonFinalizationError("I am 90% sure none of the people that look at this code will have run into this error")

while prog_cnt[0] < len(lines):
    operation = lines[prog_cnt[0]]

    # comments like ligma balls (ligma is a valuable comment)
    if operation.startswith('\\') or len(operation) == 0:
        prog_cnt[0] += 1
        continue

    # tokenisation like deez nuts (do you know what tokenises? DEEZ NUTS!!!)
    tokens = []
    was_spch_seen = False
    string = ""
    for char in operation:
        if char == '"':
            if was_spch_seen:
                tokens.append(string)
                string = ""
            was_spch_seen = not was_spch_seen
        elif char == ' ' and not was_spch_seen:
            # double spaces... this would hardly be a good lexer otherwise
            if len(string) == 0:
                continue
            coerce_int(string, tokens)
            string = ""
        else:
            string += char
    # "but this doesn't catch the case when the string isnt terminated!!"
    # have you ever heard a crepe complain?
    # this language should not be used, let me be horrid
    # I thought of saying
    ### oh and: the last token wont be type cast XDXD
    ### because I am the developer of the language, I say that it is convention to add a null statement to the end
    # but at this point... no. no thank you. this would force me to implement null stmts / ; sentinels
    coerce_int(string, tokens)

    # parsing like mind goblin (these goblins parse with their minds)
    ast_subtree = goblin(tokens, prog_cnt[0])

    # evaluation with custom dsl like kenya
    for node in ast_subtree:
        eval_atom(node)

    prog_cnt[0] += 1

