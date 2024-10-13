from time import time
import os
try:
    import curses as c
except:
    curses = False

all_r = {"ax", "bx", "cx", "dx", "gp", "sp", "d1", "d2", "d3", "d4", "ip", "version", "user", "time", "f"}
str_r = {"gp", "sp", "d1", "d2", "d3", "d4"}

ram = {"ax": 0,
       "bx": 0,
       "cx": 0,
       "dx": 0,

       "gp": 0,    # general pointer (self made) -PR-
       "sp": 0,    # second pointer (self made) -PR-
       "1p": 0,    # 1. pointer (self made) -PR-
       "2p": 0,    # 2. pointer (self made) -PR-
       "3p": 0,    # 3. pointer (self made) -PR-
       "4p": 0,    # 4. pointer (self made) -PR-
       "5p": 0,    # 5. pointer (self made) -PR-
       "6p": 0,    # 6. pointer (self made) -PR-
       "7p": 0,    # 7. pointer (self made) -PR-
       "8p": 0,    # 8. pointer (self made) -PR-

       "d1": 0,    # 1. data (self made) -PR-
       "d2": 0,    # 2. data (self made) -PR-
       "d3": 0,    # 3. data (self made) -PR-
       "d4": 0,    # 4  data (self made) -PR- (your directory at the start of run)

       #"sp": 0,   #stack pointer
       "ip": 0,    #instruction pointer
       "f": False, # flag

       "version": "0.0.6",

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

def ecvi(wrapper, user, message, directory):
    global ram
    pc = 0 # program's line -PR-
    ram["user"], ram["ip"], ram["time"], ram["gp"], ram["d4"] = user, pc, time(), directory, ""
    del user, directory
    maxtime = ram["time"] + 30
    output = ""

    try:
        program = [i.split(" ") for i in message.split("\n")]
        try:
            pc = int(program[0][1])
            ram["ip"] = pc
        except:
            pass # pc = 0
        f = ram["f"]
        program = program[1:]
        long = len(program)
        while (wrapper or ram["time"] < maxtime):
            line = program[ram["ip"]]
            command = line[0]
            body = line[1:]
            #print(ram)

            if command in {"jump", "!jump", "mov", "!mov", "loop", "jf", "!jf"}:

                if command == "jump":
                    if emu(line[2]) > 0:
                        pc = emu(line[1]) - 1  # it would be increased +1 -PR-

                elif command == "!jump":
                    if emu(line[2]) <= 0:
                        pc = emu(line[1]) - 1  # —||—

                elif command == "mov":
                    if emu(line[2]) > 0:
                        pc += emu(line[1]) - 1  # —||—

                elif command == "!mov":
                    if emu(line[2]) <= 0:
                        pc += emu(line[1]) - 1  # —||—

                else:#elif command == "loop":
                    if ram["cx"] > 0:
                        pc = emu(line[1]) - 1  # —||—
                        ram["cx"] -= 1

            elif command in {"use", "cmp", "!cmp", "jumpf", "!jumpf", "clf"}:

                if command == "use":
                    if not przerwanie(wrapper, ram, body):
                        return "Error in line: " + str(ram["ip"]) + " #1"
                    f = ram["f"]

                elif command == "cmp":
                    f = emu(line[1]) == emu(line[2])

                elif command == "!cmp":
                    f = not emu(line[1]) == emu(line[2])

                elif command == "jumpf":
                    if ram["f"]:
                        pc = emu(line[1]) - 1  # —||—

                elif command == "!jumpf":
                    if not ram["f"]:
                        pc = emu(line[1]) - 1  # —||—

                else:#elif command == "clf":
                    f = False

            elif command == "print":
                value = ""
                for i in line[1:]:
                    value += str(emu(i))#.replace("^", " ")
                ram["d4"] += value + "\n"

            elif command == "set":
                variable = line[1]
                value = 0
                for i in line[2:]:
                    value += int(emu(i))
                ram[variable] = value

            elif command == "multi":
                variable = line[1]
                value = 1
                for i in line[2:]:
                    value *= int(emu(i))
                ram[variable] = value

            elif command == "str":
                variable = line[1]
                value = ""
                for i in line[2:]:
                    value += str(emu(i))
                ram[variable] = value

            elif command == "split":
                try:
                    variable = int(emu(line[1])) #localization
                    spliter = emu(line[3])
                    value = str(emu(line[2])).split(spliter)
                    for i in range(len(value)):
                        ram[str(variable+i)] = value[i]
                    ram["gp"] = variable
                    ram["sp"] = variable+len(value)
                except:
                    return "Error in line: " + str(ram["ip"]) + " #split"

            elif command == "struct":
                try:
                    variable = line[1]
                    spliter = str(emu(line[4]))
                    value1 = int(emu(line[2]))
                    value2 = int(emu(line[3]))-1
                    ram[variable] = ""
                    for i in range(value1, value2+1):
                        ram[variable] += str(ram[str(i)])
                        if i < value2:
                            ram[variable] += spliter
                except:
                    return "Error in line: " + str(ram["ip"]) + " #struct"

            elif command == "spread":
                try:
                    variable = emu(line[1]) #localization (int) -PR-
                    value = emu(line[2])
                    for i in range(len(value)):
                        ram[variable+i] = value[i]
                except:
                    return "Error in line: " + str(ram["ip"]) + " #spread"

            elif command == "end":
                return ram["d4"]
            elif command == "nop":
                pass
            else:
                return "Error in line: " + str(ram["ip"]) + " #2"

            pc += 1
            ram["ip"] = pc
            ram["f"] = f
            ram["time"] = time()

        return "Error in line: " + str(ram["ip"]) + " #-1 " + str(e)

    except Exception as e:
        return "Error in line: " + str(ram["ip"]) + " #0 " + str(e)

def przerwanie(w, ram, arg = 0):
    command = int(arg[0]) # here could be an error -PR-
    if (not w or not c) and command > 50:
        return True
    if command == 30: #get whitespaces
        ram["bx"] = " "
        ram["cx"] = "	"
        ram["dx"] = "\n"
    if command == 31: #read
        if os.path.exists(ram["gp"]):
            with open(ram["gp"], "r") as txt:
                t = txt.read()
                ram["d1"] = t
        else:
            ram["f"] = True
    elif command == 32: #write
        if os.path.exists(ram["gp"]):
            with open(ram["gp"], "w") as txt:
                txt.write(ram["d1"])
        else:
            ram["f"] = True
    elif command == 33: #append
        if os.path.exists(ram["gp"]):
            with open(ram["gp"], "a") as txt:
                txt.write(ram["d1"])
        else:
            ram["f"] = True
    elif command == 35: #read dir
        if os.path.exists(ram["gp"]):
            ram["d1"] = os.listdir(ram["gp"])
        else:
            ram["f"] = True
    return True

#  program example  -PR-
'''print(ecvi("no.user" , """ecvi
set ax 0
print (ax)
set ax (ax) 1
set bx (ax) -10
!jump 1 (bx)
use 30
print "user:" (bx) (user)
print "version:" (bx) (version)"""))'''