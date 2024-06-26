import os
from random import randint
from discord import File
from ECVI import ecvi as _ecvi


def user(user, message, p_message, p):
    admin = True if user in p["admin"] else False

    if not admin and user not in p["user"]:
        return "`You don't have permisions` 😋"

    if p["lock"] and not admin:
        return "`Command line is locked` 😋"

    if p_message[0] == "ecvi":
        return _ecvi(user, message)
    if p_message[0] == "help":
        return "## `Commands:`\n- `ecvi`\n- `ls`\n- `cd`\n- `mydir`\n- `read`\n - `, write, mkdir, rmdir, copy, paste, copyinfo`"
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
        if p_message[1] ==  ".":
            t = ""
            for i in p["dir"].split("/")[:-1]:
                t += "/" + i
            p["dir"] = t[1:] if len(t) > 0 else "/"
        elif p_message[1] ==  "..":
            p["dir"] = "/home/pi"
        else:
            t = p["dir"] + "/" + p_message[1]
            if os.path.exists(t):
                p["dir"] = t
            else:
                return "`Directory not found`"
        return "`" + p["dir"] + "`"
    if p_message[0] == "mydir":
        return "`" + p["dir"] + "`"
    if p_message[0] == "read":
        d = p_message[1] if len(p_message) > 1 else p["dir"]
        if not os.path.exists(d):
            return "`"+d+"`\n`Cannot find the file/directory`"
            #await ctx.send(file=discord.File(r'c:\location\of\the_file_to\send.png'))
        return File(d)
    return "`Command not found`"

