import termcolor as p

error = "[x]: "
info  = "[-]: "
warn  = "[!]: "
noti  = "[#]: "

def ErrorPrint(msg):
    p.cprint(error + str(msg), color="red")
def WarnPrint(msg):
    p.cprint(warn + str(msg), color="yellow")
def NotifyPrint(msg):
    p.cprint(noti + str(msg), color="green")
def InfoPrint(msg):
    p.cprint(info + str(msg))