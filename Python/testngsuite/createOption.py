import Tkinter, tkFileDialog, Tkconstants
from Tkinter import *
from collections import defaultdict
from createTestSuiteXml import createTestSuiteXml as createSuiteXml
class createOption():
    def __init__(self):
        self.cb = []
        self.cb_v = []

    def createTestcaseList(self,testSuiteInfo):
        def chkboxChecked():
            testSuiteDict = defaultdict(list)
            opt = []
            for ix, item in enumerate(self.cb):
                opt.append(self.cb_v[ix].get())
            print opt
            for value in opt:
                if not value == "0":
                    key = value.split("#")[0]
                    val = value.split("#")[1]
                    testSuiteDict[key].append(val)
            print testSuiteDict
            obj=createSuiteXml()
            return obj.createTestTag(testSuiteDict)
        def fileSave():
            f = tkFileDialog.asksaveasfile(mode='w', defaultextension="xml")
            if f is None:
               return
            text2save = str(chkboxChecked())
            f.write(text2save)
            f.close()
        root = Tk()
        root.title("Select test cases")
        testCaseList=[]
        for key,value in testSuiteInfo.items():
            for testcaseName in value:
                testCaseList.append(key+"#"+str(testcaseName))
            print testCaseList
        count=1
        testSuiteName=[]
        count=0
        for index,text in enumerate(testCaseList):
            testSuite=str(text).split("#")[0]
            if testSuite not in testSuiteName:
                testSuiteName.append(testSuite)
                label = Label(root, text="List of test cases of %s Testsuite" %testSuite)
                label.grid(row=count, column=0, sticky='w')
                count+=1
            self.cb_v.append(StringVar(value=0))
            self.cb.append(Checkbutton(root, text=str(text).split("#")[1], onvalue=text, variable=self.cb_v[index]).grid(row=count, sticky=W))
            count+=1
        def exitFromApp():
            sys.exit(0)

        saveXml = Button(root,width=20, text="Save TestSuite",command=fileSave)
        saveXml.grid(row=count+3, column=5)
        runTestSuite = Button(root,width=20, text="Run TestSuite",command=chkboxChecked)
        runTestSuite.grid(row=count+3, column=10)
        exitButton = Button(root,width=20, text="Exit",command=exitFromApp)
        exitButton.grid(row=count+3,column=20)
        root.mainloop()