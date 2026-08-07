# done in python because I cannot be fucked to do string processing in C
# but will rewrite in C after exams
# or make a real compiler
# anyway I'm a crepe I am a weirdough waffle hell am i doing here i doughnut belong here

lines = []
stack = []
with open("./test.pnck", "r") as f:
    lines = list(map(lambda elem: elem.strip(), f.readlines()))

pointer = 0

while pointer < len(lines):
    operation = lines[pointer]
    pointer += 1

    # comments like ligma balls (ligma is a valuable comment)
    if operation.startswith('\\'):
        continue

    # tokenisation like deez nuts (do you know what tokenises? DEEZ NUTS!!!)
    splitted = []
    was_spch_seen = False
    string = ""
    for char in operation:
        if char == '"':
            was_spch_seen = not was_spch_seen
        elif char == ' ' and not was_spch_seen:
            splitted.append(string)
            string = ""
        else:
            string += char
    splitted.append(string)

    # parsing like mind goblin (these goblins parse with their minds)
    
    
    print(operation)

