from appJar import gui

def generateCompileCmd(application,tree,mode):
    cmd = ""
    if application == "UnitTest":
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


def generateRunCmd(application,tree,mode,cextPath,pls,etcDir,log):
    cmd = ""
    if application == "UnitTest":
        if tree == "I410":
            cmd = "./meMem_unitTest64"
        elif tree == "4.14.1":
            cmd = "./meMem_unitTest"

        if mode == "Debug":
            cmd += "d "

        base = "{}/{}/{}".format(cextPath,pls,pls)
        cmd += " --base={} -sClipName={} :".format(base,pls)

    elif application == "SRD":
        if tree == "I410":
            pass
        elif tree == "4.14.1":
            if mode == "Release":
                cmd = "./GV_SRD --library ./libSRD.so"
            if mode == "Debug":
                cmd = "./GV_SRDd --library ./libSRDd.so"

        cmd += " Clip: --clip {} :".format(pls)



    elif application == "PC":
        if tree == "I410":
            pass
        elif tree == "4.14.1":
            if mode == "Release":
                cmd = "./PC_PC GVP: --library ./libPC.so Clip: --clip "
            else:
                cmd = "./PC_PCd GVP: --library ./libPCd.so Clip: --clip "

            cmd += "{} --etcDir {} Logging: --inDir {} :".format(pls,etcDir,log)


    return cmd

def getStateStr():
    application = app.getMenuRadioButton("Application", "Application")
    tree = app.getMenuRadioButton("Tree", "Tree")

    stateStr = tree + "_" + application
    return stateStr

def stateChanged():
    application = app.getMenuRadioButton("Application", "Application")
    tree = app.getMenuRadioButton("Tree","Tree")
    mode = app.getMenuRadioButton("Mode", "Mode")

    # set the compilation cmd
    compileCmd = generateCompileCmd(application,tree,mode)
    app.setEntry("CompileCmd", compileCmd)

    applicationFrame = application + "_frame"
    stateStr = getStateStr()

    # show the relevant running options
    app.raiseFrame(applicationFrame)
    app.raiseFrame(stateStr)







def fillRunCmd():
    application = app.getMenuRadioButton("Application", "Application")
    tree = app.getMenuRadioButton("Tree","Tree")
    mode = app.getMenuRadioButton("Mode", "Mode")

    cextPath = app.getEntry("cextPathEntry")
    pls = app.getEntry("plsEntry")
    etcDir = app.getEntry("etcDirEntry")
    log = app.getEntry("logEntry")

    stateStr = getStateStr()
    stateSections = sections[stateStr]
    cmd = generateRunCmd(application, tree, mode,cextPath=cextPath,pls=pls,etcDir=etcDir,log=log)
    for section in stateSections:
        sectionStr = " {}:".format(section._name)
        addSection = False
        for flag in section._flags:
            if app.getCheckBox(flag._id):
                addSection = True
                sectionStr += " {}".format(flag._name)
                if flag._type == "input":
                    val = app.getEntry(flag._id+"_entry")
                    if val == "" and flag._defaultVal is not None:
                        val = flag._defaultVal
                        sectionStr += "={}".format(val)
                elif flag._type == "choice":
                    val = app.getOptionBox(flag._id+"_optionBox")
                    sectionStr += "={}".format(val)
        if addSection:
            cmd += sectionStr

    app.setEntry("RunCmd",cmd)


def toggleEntry(flagId):
    if app.getCheckBox(flagId):
        app.showEntry(flagId + "_entry")
    else:
        app.setEntry(flagId + "_entry", "")
        app.hideEntry(flagId + "_entry")

def toggleOptionBox(flagId):
    if app.getCheckBox(flagId):
        app.showOptionBox(flagId + "_optionBox")
    else:
        app.hideOptionBox(flagId + "_optionBox")





class Flag:
    def __init__(self,name,type,defaultAdd=False,defaultVal=None,possibleVals=None):
        self._name = name
        self._type = type
        self._defaultAdd = defaultAdd
        self._defaultVal = defaultVal
        self._id = -1
        self._possibleVals = possibleVals

    def add(self,id):
        self._id = id
        app.addNamedCheckBox(self._name, id)
        app.setCheckBox(id,ticked=self._defaultAdd)

        if self._type == "void":
            if self._defaultVal:
                app.setCheckBox(id)
        elif self._type == "input":
            app.addEntry(id + "_entry")
            app.setCheckBoxChangeFunction(id, toggleEntry)
            toggleEntry(id)
            if self._defaultVal != None:
                app.setEntryDefault(id + "_entry",self._defaultVal)
        elif self._type == "choice":
            app.addOptionBox(id+"_optionBox",self._possibleVals)
            app.setCheckBoxChangeFunction(id, toggleOptionBox)
            toggleOptionBox(id)
            if self._defaultVal:
                app.setOptionBox(id+"_optionBox",self._defaultVal)


class Section:
    def __init__(self,name,flags):
        self._name = name
        self._flags = flags
        self._id = -1


def getFlagByID(id):
    for sectionState,sectionsList in sections.iteritems():
        for section in sectionsList:
            for flag in section._flags:
                if flag._id == id:
                    return flag
    return None





def addSection(app,section):
    section._id = str(addSection._sectionId)
    with app.toggleFrame(section._id):
        for flag in section._flags:
            flagId = str(section._id) + "_" + str(addSection._flagId)
            flag.add(flagId)
            addSection._flagId += 1
    app.setToggleFrameText(section._id, section._name)
    addSection._sectionId += 1

addSection._sectionId = 0
addSection._flagId = 0



sections = {
    "4.14.1_UnitTest":
        [
            Section("Section1",[
                Flag("voidFlag","void")
                , Flag("inputFlag","input")
                , Flag("inputFlagDefVal","input",defaultVal=3)
                , Flag("choiceFlag","choice",possibleVals=["val1","val2","val3"])
                , Flag("choiceFlagDefVal","choice",possibleVals=["val1","val2","val3"],defaultVal="val3")
            ]),
            Section("Section2",[
                Flag("f", "void")
            ])
        ]

    ,"4.14.1_SRD":
        [
        ]
    , "4.14.1_PC":
        [
        ]

    ,"I410_UnitTest":
        [
        ]

    , "I410_SRD":
        [
        ]
    , "I410_PC":
        [
        ]



}


with gui("Runner","1000x500") as app:
    # control the state
    app.addMenuRadioButton("Tree","Tree","4.14.1",stateChanged)
    app.addMenuRadioButton("Tree", "Tree", "I410",stateChanged)
    app.addMenuRadioButton("Application","Application","UnitTest",stateChanged)
    app.addMenuRadioButton("Application","Application","SRD",stateChanged)
    app.addMenuRadioButton("Application","Application","PC",stateChanged)
    app.addMenuRadioButton("Mode", "Mode", "Release",stateChanged)
    app.addMenuRadioButton("Mode", "Mode", "Debug",stateChanged)

    app.addLabelEntry("CompileCmd")
    app.setLabel("CompileCmd","Compilation cmd: ")
    app.addLabelEntry("RunCmd")
    app.setLabel("RunCmd", "Running cmd: ")





    app.addHorizontalSeparator()
    app.setFont(14)
    app.addLabel("SetPathsLabel", "Set paths")


    clipFrameRow = 4
    with app.frame("UnitTest_frame",row=clipFrameRow):
        app.addLabelEntry("cextPathEntry")
        app.addLabelEntry("plsEntry")
    with app.frame("SRD_frame",row=clipFrameRow):
        app.addLabelEntry("clipSRDEntry")
    with app.frame("PC_frame",row=clipFrameRow):
        app.addLabelEntry("clipPCEntry")
        app.addLabelEntry("etcDirEntry")
        app.addLabelEntry("logEntry")

    app.setLabel("cextPathEntry", "cext path")
    app.setLabel("plsEntry", "pls")

    app.setLabel("clipSRDEntry", "clip")
    app.setLabel("clipPCEntry", "clip")

    app.setLabel("etcDirEntry", "etc dir")
    app.setLabel("logEntry", "log")



    app.addHorizontalSeparator()

    app.setFont(14)
    app.addLabel("ChooseFlagsLabel", "Choose flags")
    flagsFrameRow = 7

    for stateStr,sectionsList in sections.iteritems():
        with app.frame(stateStr, row=flagsFrameRow):
            for section in sectionsList:
                addSection(app, section)


    stateChanged()
    fillRunCmd()

    app.registerEvent(fillRunCmd)
    app.setPollTime(250)
    app.go()