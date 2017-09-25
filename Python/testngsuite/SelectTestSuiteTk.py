import Tkinter, tkFileDialog, Tkconstants
from Tkinter import *
import os
import sys
from collections import defaultdict
import createOption
import re
class SelectTestSuiteTk(object):
    rootdir="/home/"
    def __init__(self):
        self.root=Tk()
        self.root.title("Create your TestNG Suite xml")
        self.button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        self.brwsbtn=Button(self.root, text='Select the TestSuite folder', fg='black', command=self.openDirectory)
        self.brwsbtn.pack(**self.button_opt)
        Button(self.root, text='Exit', fg='black', command=self.exit).pack(**self.button_opt)
        self.root.minsize(width=400, height=100)
        self.root.maxsize(width=400, height=100)
        self.root.mainloop()

    def openDirectory(self):
        dirname = tkFileDialog.askdirectory(parent=self.root, initialdir=self.rootdir, title='Select your test Java folder')
        print dirname
        self.brwsbtn.destroy()
        self.createTesSuiteStracture(dirname)

    def exit(self):
        self.root.quit()

    def refreshWidget(self):
        self.root.destroy()
        self.__init__()
		
	'''def testClassName(self,fileLines,testfile):
		if fileLines.find("package"):
			for line in fileLines:
				mo=re.match("package (\w)*",line)
                if mo:
                   return mo.group(1)
		else:
			pathcomponent = testfile.split(os.sep)
			dictKey=".".join([pathcomponent[-2],pathcomponent[-1].split(".")[0]])
			return dictKey
	'''		
    def createTesSuiteStracture(self,testfilepath):
        if not os.path.exists(testfilepath):
            print "%s path does not exist:Please enter valid path" % testfilepath
            sys.exit(0)
        else:
            self.testsuitedict=defaultdict(list)
            testfiles = [os.path.join(testfilepath, testfile) for testfile in os.listdir(testfilepath) if
                         testfile.endswith(".java")]
            print testfiles
            if not testfiles:
                Button(self.root, text='No Java files found in Selected directory:Try Aagain', fg='black', command=self.refreshWidget).pack(**self.button_opt)
            for testfile in testfiles:
                testfile = testfile.replace("/", os.sep)
                print testfile
                with open(testfile, 'r') as fh:
                    fileData=fh.readlines()
                    if not " ".join(fileData).find("package") == -1:
                       for line in fileData:
                           #import pdb
                           #pdb.set_trace()
                           mo=re.match("^package (.*);",line,re.DOTALL)
                           if mo:
                              dictKey = mo.group(1)+"."+testfile.split(os.sep)[-1].split(".")[0]
                              break
                    else:	
                        pathcomponent = testfile.split(os.sep)
                        dictKey=".".join([pathcomponent[-2],pathcomponent[-1].split(".")[0]])
                    if dictKey not in self.testsuitedict.keys():
                        self.testsuitedict[dictKey]=[]
                    for index,line in enumerate(fileData):
                       # print line
                        if not line.find("@Test") == -1:
                            print line
                            mo=re.match(r'[\s\w]*\s([\w]*)',fileData[index+1])
                            if mo is not None:
                                self.testsuitedict[dictKey].append(mo.group(1))
            print self.testsuitedict
            self.root.destroy()
            createOption.createOption().createTestcaseList(self.testsuitedict)


if __name__ == "__main__":
    ts=SelectTestSuiteTk()