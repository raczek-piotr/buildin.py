ram = {"ax": 0,
       "bx": 0,
       "cx": 0,
       "dx": 0,
       "user": "",
       "version": "0.0.1",
       "line": 0}


def emu(command): #part of it -PR-
    global ram

    if command[0] == "(":
        value = ram[command[1:-1]]
    elif command[0] == '"' or command[0] == "'":
        value = command[1:-1]
    else:
        value = int(command)

    return value

def ecvi(user, message, p_message = ""):
    global ram
    ram["user"] = user
    output = ""

    program = [i.split(" ") for i in message[5:].split("\n")]
    long = len(program)
    while ram["line"] < long:
        line = program[ram["line"]]
        ram["line"] += 1
        command = line[0]


        if command == "jump":
            if emu(line[2]) > 0:
                ram["line"] = emu(line[1])

        elif command == "print":
            value = ""
            for i in line[1:]:
                value += str(emu(i)).replace("^", " ")
            output += value + "\n"

        elif command == "=":
            variable = line[1]
            value = 0
            for i in line[2:]:
                value += emu(i)
            ram[variable] = value


    return output

#  program example  -PR- 
#print(ecvi("no.user" , """ecvi
#print (ax)
#= ax (ax) 1
#= bx (ax) -10
#jump 5 (bx)
#jump 0 1
#print "user:^" (user)
#print "version:^" (version)"""))









        