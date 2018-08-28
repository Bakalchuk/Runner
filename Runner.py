from appJar import gui

def generateCompileCmd(application,tree,mode):
    cmd = ""
    if application == "unit test":
        if tree == "I410":
            cmd += "makeuo "
        elif tree == "4.14.1":
            cmd += "makeu "

        if mode == "Release":
            cmd += "rel"
        elif mode == "Debug":
            cmd += "dbg"
    elif application == "SRD":
        cmd += "make "
        if tree == "I410":
            cmd += "SRD_p3 "
        elif tree == "4.14.1":
            cmd += "SRD_s4 "

        cmd += "MODE="
        if mode == "Release":
            cmd += "rel"
        elif mode == "Debug":
            cmd += "dbg"
    elif application == "PC":
        cmd += "make "
        if tree == "I410":
            cmd += "PC_p3 "
        elif tree == "4.14.1":
            cmd += "PC_s4 "

        cmd += "MODE="
        if mode == "Release":
            cmd += "rel"
        elif mode == "Debug":
            cmd += "dbg"

    return cmd


def generateRunCmd(application,tree,mode,flags):
    cmd = ""
    if application == "unit test":
        if tree == "I410":
            cmd += "./meMem_unitTest64"
        elif tree == "4.14.1":
            cmd += "./meMem_unitTest"

        if mode == "Release":
            cmd += " "
        elif mode == "Debug":
            cmd += "d "
    elif application == "SRD":
        cmd += "make "
        if tree == "I410":
            cmd += "SRD_p3 "
        elif tree == "4.14.1":
            cmd += "SRD_s4 "

        cmd += "MODE="
        if mode == "Release":
            cmd += "rel"
        elif mode == "Debug":
            cmd += "dbg"
    elif application == "PC":
        cmd += "make "
        if tree == "I410":
            cmd += "PC_p3 "
        elif tree == "4.14.1":
            cmd += "PC_s4 "

        cmd += "MODE="
        if mode == "Release":
            cmd += "rel"
        elif mode == "Debug":
            cmd += "dbg"

    return cmd




app=gui()
app.setTitle("Runner")

app.setFont(20)
app.addLabelOptionBox("Application", ["unit test","SRD","PC"])
app.addLabelOptionBox("Tree", ["I410","4.14.1"])

app.addRadioButton("Mode", "Release")
app.addRadioButton("Mode", "Debug")


def make(btn):
    cmd = generateCompileCmd(app.getOptionBox("Application"),app.getOptionBox("Tree"),app.getRadioButton("Mode"))
    app.setTextArea("Compile", cmd, end=False, callFunction=False)

app.addButton("Make",make)

app.setFont(12)
app.addScrolledTextArea("Compile",text=None)



app.go()