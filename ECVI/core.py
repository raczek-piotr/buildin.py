from time import time


ram = {"ax": 0,
       "bx": 0,
       "cx": 0,
       "dx": 0,

       "version": "0.0.4",
       "line": 0, # pc -PR-
       #"sp": [],
       #"bp": [],

       "user": "",
       "time": 0}


def emu(command):  # part of it -PR-
    global ram

    first_character = command[0]

    if first_character == "(":
        return ram[command[1:-1]]

    if first_character == "[":
        q = emu(command[1:-1])
        return ram[str(q)]

    elif first_character in {'"', "'"}:
        return command[1:-1]

    elif first_character == '-':
        return -emu(command[1:])

    else:
        return int(command)

def ecvi(user, message, flag=""):
    global ram
    pc = 0 #program's line -PR-
    ram["user"], ram["line"], ram["time"] = user, pc, time()
    output = ""

    try:
        program = [i.split(" ") for i in message.split("\n")][1:]
        long = len(program)
        while ram["line"] < long:
            line = program[ram["line"]]
            command = line[0]

            if command in {"jump", "!jump", "mov", "!mov"}:
                if command == "jump":
                    if emu(line[2]) > 0:
                        pc = emu(line[1]) - 1  # it would be increased +1 -PR-

                elif command == "!jump":
                    if emu(line[2]) <= 0:
                        pc = emu(line[1]) - 1  # —||—

                elif command == "mov":
                    if emu(line[2]) > 0:
                        pc += emu(line[1]) - 1  # —||—

                else:  # if command == "!mov":
                    if emu(line[2]) <= 0:
                        pc += emu(line[1]) - 1  # —||—

            elif command == "print":
                value = ""
                for i in line[1:]:
                    value += str(emu(i)).replace("^", " ")
                output += value + "\n"

            elif command == "set":
                variable = line[1]
                value = 0
                for i in line[2:]:
                    value += int(emu(i))
                ram[variable] = value

            elif command == "str":
                variable = line[1]
                value = ""
                for i in line[2:]:
                    value += str(emu(i))
                ram[variable] = value

            elif command == "multi":
                variable = line[1]
                value = 1
                for i in line[2:]:
                    value *= int(emu(i))
                ram[variable] = value

            elif command == "def":
                ram.update({line[1]: emu(line[2])})

            elif command == "time":
                ram["time"] = time()

            pc += 1
            ram["line"] = pc
        return output

    except Exception as e:
        return "Error: " + str(e)

#  program example  -PR-
'''print(ecvi("no.user" , """ecvi
print (ax)
set ax (ax) 1
set bx (ax) -10
!jump 0 (bx)
print "user:^" (user)
print "version:^" (version)"""))'''