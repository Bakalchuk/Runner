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


def frame():
    # get all the inputs from the GUI
    entries = {}

    for d in [app.getAllInputs(),app.getAllEntries()]:
        for k,v in d.iteritems():
            entries[k] = v

    if(frame.entries == entries):
        return

    # set the compilation cmd
    compileCmd = generateCompileCmd(entries["Application"],entries["Tree"],entries["Mode"])
    app.clearAllTextAreas(callFunction=True)
    app.setTextArea("CompileCmd", compileCmd, end=False, callFunction=True)

    # show the relevant running options
    if entries["Application"] == "unit test":
        app.raiseFrame("unit_test_frame")
    elif entries["Application"] == "SRD":
        app.raiseFrame("SRD_frame")
    elif entries["Application"] == "PC":
        app.raiseFrame("PC_frame")


    # set the run cmd
    pass

    frame.entries = entries
frame.entries = None



with gui("Runner","600x400") as app:
    with app.frame("State"):
        app.setFont(20)
        app.addOptionBox("Tree", ["I410","4.14.1"],app.getRow(),0,2)
        app.addOptionBox("Application", ["unit test","SRD","PC"],app.getRow(),0,2)
        app.addRadioButton("Mode", "Release",app.getRow(),0)
        app.addRadioButton("Mode", "Debug","p",1)

    with app.frame("CompileFrame",row=0,column=1):
        app.addLabel("CompileLabel","Compile")
        app.addScrolledTextArea("CompileCmd")


    app.setFont(14)
    app.addLabel("RunLabel", "Run",row=1,column=1)
    with app.frame("unit_test_frame",row=2,column=1):
        app.addLabelEntry("clipexts path")
        app.addLabelEntry("pls path")
        app.addLabelEntry("pls")
    with app.frame("SRD_frame",row=2,column=1):
        app.addLabelEntry("clip SRD")
    with app.frame("PC_frame",row=2,column=1):
        app.addLabelEntry("clip PC")
        app.addLabelEntry("etc")
        app.addLabelEntry("logs")


    app.registerEvent(frame)
    app.setPollTime(250)
    app.go()