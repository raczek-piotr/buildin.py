from time import time


ram = {"ax": 0,
       "bx": 0,
       "cx": 0,
       "dx": 0,

       "version": "0.0.2",
       "line": 0,

       "user": "",
       "time": 0}


def emu(command): #part of it -PR-
    global ram

    first_caracter = command[0]

    if first_caracter == "(":
        return ram[command[1:-1]]

    elif first_caracter in {'"', "'"}:
        return command[1:-1]

    elif first_caracter == '-':
        return - emu(command[1:])

    else:
        return int(command)

def ecvi(user, message, flag = ""):
    global ram
    ram["user"], ram["line"], ram["time"] = user, 0, time()
    output = ""

    program = [i.split(" ") for i in message[5:].split("\n")]
    long = len(program)
    while ram["line"] < long:
        line = program[ram["line"]]
        command = line[0]


        if command == "jump":
            if emu(line[2]) > 0:
                ram["line"] = emu(line[1]) -1 # it will increase +1 -PR-

        elif command == "!jump":
            if emu(line[2]) <= 0:
                ram["line"] = emu(line[1]) -1 # it will increase +1 -PR-

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

        elif command == "def":
            ram.update({line[1]: emu(line[2])})

        elif command == "time":
            ram["time"] = time()


        ram["line"] += 1
    return output

#  program example  -PR-
#print(ecvi("no.user" , """ecvi
#print (ax)
#set ax (ax) 1
#set bx (ax) -10
#jump 5 (bx)
#jump 0 1
#print "user:^" (user)
#print "version:^" (version)"""))

#  program example2  -PR-
print(ecvi("no.user" , """ecvi
def (ax)
set ax (ax) 1
set bx (ax) -10
jump 5 (bx)
jump 0 1
print "user:^" (user)
print "version:^" (version)"""))









        