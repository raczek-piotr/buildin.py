import os
from random import randint


def sudo(user, message, p_message, p):
    if user not in p["admin"]:
        return "`You don't have permisions` 😋"

    if p_message[0] == "help":
        return "## `Sudo commands:`\n- `sudo lock`\n- `sudo unlock`\n- `sudo adduser`\n- `sudo deluser`\n- `sudo user`" # read, write, mkdir, rmdir, copy, paste, copyinfo
    if p_message[0] == "lock":
        p["lock"] = True
        return "`Locked the command line` 😋"
    if p_message[0] == "unlock":
        p["lock"] = False
        return "`Unlocked the command line` 😋"
    if p_message[0] == "adduser":
        if len(p_message) > 1:
            p["user"].add(p_message[1])
            return "`Added user: " + p_message[1] + "`"
        return "`No user name`"
    if p_message[0] == "deluser":
        for i in p["user"]:
            p["user"].remove(p_message[1])
            return "`Delated user: " + p_message[1] + "`"
        return "`No user name`"
    if p_message[0] == "user":
        t = "## Users:"
        for i in p["user"]:
            t += "\n`" + i + "`"
        return t
    return "`Nie znaleziono polecenia`"
