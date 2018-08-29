from appJar import gui

def generateCompileCmd(application,tree,mode):
    cmd = ""
    if application == "Unit test":
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

    state = {"Tree":app.getMenuRadioButton("Tree","Tree"),
             "Application": app.getMenuRadioButton("Application", "Application"),
             "Mode": app.getMenuRadioButton("Mode", "Mode")
             }



    # get all the inputs from the GUI
    entries = {}

    for d in [app.getAllInputs(),app.getAllEntries()]:
        for k,v in d.iteritems():
            entries[k] = v

    if(frame.state == state and frame.entries == entries):
        return

    frame.entries = entries
    frame.state = state

    # set the compilation cmd
    compileCmd = generateCompileCmd(state["Application"],state["Tree"],state["Mode"])
    app.setEntry("CompileCmd", compileCmd)

    # show the relevant running options
    if state["Application"] == "unit test":
        app.raiseFrame("unit_test_frame")
    elif state["Application"] == "SRD":
        app.raiseFrame("SRD_frame")
    elif state["Application"] == "PC":
        app.raiseFrame("PC_frame")


    if state["Application"] == "unit test" and state["Tree"] == "4.14.1":
        if app.getCheckBox("REM: enabled"):
            app.enableRadioButton("Rem: enabled options")
        else:
            app.disableRadioButton("Rem: enabled options")


    # set the run cmd
    pass

frame.state = None
frame.entries = None



with gui("Runner","600x400") as app:
    # control the state
    app.addMenuRadioButton("Tree","Tree","4.14.1")
    app.addMenuRadioButton("Tree", "Tree", "I410")
    app.addMenuRadioButton("Application", "Application", "Unit test")
    app.addMenuRadioButton("Application", "Application", "SRD")
    app.addMenuRadioButton("Application", "Application", "PC")
    app.addMenuRadioButton("Mode", "Mode", "Release")
    app.addMenuRadioButton("Mode", "Mode", "Debug")

    app.addLabelEntry("CompileCmd")
    app.setLabel("CompileCmd","Compilation cmd: ")


    app.setFont(14)
    app.addLabel("RunLabel", "Run")
    with app.frame("unit_test_frame",row=2):
        app.addLabelEntry("clipexts path")
        app.addLabelEntry("pls path")
        app.addLabelEntry("pls")
    with app.frame("SRD_frame",row=2):
        app.addLabelEntry("clip1")
    with app.frame("PC_frame",row=2):
        app.addLabelEntry("clip2")
        app.addLabelEntry("etc")
        app.addLabelEntry("logs")

    app.setLabel("clip1", "clip")
    app.setLabel("clip2", "clip")

    # with app.frame("unit_test_4.14.1_flags",row=3):
    #     app.addCheckBox("-sCompressedUT")
    #     app.setCheckBox("-sCompressedUT")
    #     app.addCheckBox("-sframe-verbose")
    #     app.setCheckBox("-sframe-verbose")
    #     app.addCheckBox("-sMEMemUnitTestDebug")
    #     app.setCheckBox("-sMEMemUnitTestDebug")
    #
    #     app.addCheckBox("REM:")
    #     app.setCheckBox("REM:")
    #     app.addNamedCheckBox("enabled","REM: enabled")
    #     app.setCheckBox("REM: enabled")
    #     app.addRadioButton("Rem: enabled options","true")
    #     app.addRadioButton("Rem: enabled options", "false")





    app.registerEvent(frame)
    app.setPollTime(250)
    app.go()