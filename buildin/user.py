import os
from random import randint
from discord import File
from ECVI import ecvi as _ecvi
try:
    from curses import wrapper
except:
    wrapper = False

def user(user, message, p_message, p):
    admin = True if user in p["admin"] else False

    if not admin and user not in p["user"]:
        return "`You don't have permisions` 🙈"

    if p["lock"] and not admin:
        return "`Command line is locked` 😋"

    if p_message[0] == "ecvi":
        return _ecvi(False, user, message, p["dir"])
    if p_message[0] == "execute":
        #if wrapper:
            d = p_message[1] if "/" in p_message[1] else p["dir"] + "/" + p_message[1]
            with open(d, "r") as txt:
                return _ecvi(False, user, txt.read(), p["dir"])
                #return wrapper(_ecvi, user, txt.read())
        #return "no `wrapper`"

    if p_message[0] == "help":
        return "## `Commands:`\n- `ecvi`\n- `ls`\n- `cd`\n- `mydir`\n- `print`\n- `read`\n- `write`\n- `append`\n - `execute`\n - `, mkdir, rmdir, copy, paste, copyinfo`"
    if p_message[0] == "ls":
        d = p_message[1] if len(p_message) > 1 else p["dir"]
        try:
            t = sorted(os.listdir(d))
        except:
            return "`"+d+"`\n`Cannot find the file/directory`"
        output = "`"+d+"`"
        for i in t:
            if admin or i[0] != ".":
                output += "\n- `" + i + "`"
        return output
    if p_message[0] == "cd":
        if len(p_message) < 2:
            return "`No argument`"
        if p_message[1] ==  "..":
            t = ""
            for i in p["dir"].split("/")[:-1]:
                t += "/" + i
            p["dir"] = t[1:] if len(t) > 0 else "/"
        elif p_message[1][0] ==  "/":
            t = p_message[1]
            if os.path.exists(t):
                p["dir"] = t
            else:
                return "`Directory not found`"
        else:
            t = p["dir"] + "/" + p_message[1]
            if os.path.exists(t):
                p["dir"] = t
            else:
                return "`Directory not found`"
        return "`" + p["dir"] + "`"
    if p_message[0] == "mydir":
        return "`" + p["dir"] + "`"
    if p_message[0] == "print":
        d = p_message[1] if "/" in p_message[1] else p["dir"] + "/" + p_message[1]
        if not os.path.exists(d):
            return "`"+d+"`\n`Cannot find the file/directory`"
            #await ctx.send(file=discord.File(r'c:\location\of\the_file_to\send.png'))
        with open(d, "r") as txt:
            t=txt.read()
        return t
    if p_message[0] == "read":
        d = p_message[1] if "/" in p_message[1] else p["dir"] + "/" + p_message[1]
        if not os.path.exists(d):
            return "`"+d+"`\n`Cannot find the file/directory`"
            #await ctx.send(file=discord.File(r'c:\location\of\the_file_to\send.png'))
        return File(d)
    if p_message[0] == "write":
        d = p_message[1] if "/" in p_message[1] else p["dir"] + "/" + p_message[1]
        if not os.path.exists(d):
            return "`"+d+"`\n`Cannot find the file/directory`"
            #await ctx.send(file=discord.File(r'c:\location\of\the_file_to\send.png'))
        m = message.split("\n")
        t = ""
        for i in m[1:]:
            t = t + i + "\n"
        with open(d, "w") as txt:
            txt.write(t[:-1])
        return "writed…"
    if p_message[0] == "append":
        d = p_message[1] if "/" in p_message[1] else p["dir"] + "/" + p_message[1]
        if not os.path.exists(d):
            return "`"+d+"`\n`Cannot find the file/directory`"
            #await ctx.send(file=discord.File(r'c:\location\of\the_file_to\send.png'))
        m = message.split("\n")
        t = ""
        for i in m[1:]:
            t = t + i + "\n"
        with open(d, "a") as txt:
            txt.write(t[:-1])
        return "appended…"
    #return "`Command not found`"

