import os
import sys
import argparse
from lxml import etree

class createTestSuiteXml():
    def __init__(self):
        pass
    def createTestTag(self,testSuiteDict):
		s = '<?xml version="1.0" encoding="UTF-8"?><suite></suite>' 
		suite = etree.fromstring(s)
		suite.set('name',"SuteName")
		comment=etree.Comment('Test Ng suite')
		suite.append(comment)
		for key,value in testSuiteDict.items():
			test=etree.SubElement(suite,'test')
			test.set('name',key)
			classtag=etree.SubElement(test,'classes')
			className=etree.SubElement(classtag,'class')
			className.set('name',key)
			for testcase in testSuiteDict[key]:
				methods=etree.SubElement(className,"methods")
				method=etree.SubElement(methods,"include")
				method.set('name',testcase)

		xmlDoc = etree.tostring(suite, encoding="UTF-8",
                     xml_declaration=True,
                     pretty_print=True,
                     doctype='<!DOCTYPE suite SYSTEM "http://testng.org/testng-1.0.dtd">')
		return xmlDoc
			
if __name__ == "__main__":
    objTestSuiteXml=createTestSuiteXml()
    print objTestSuiteXml.testNgXmlValue+objTestSuiteXml.createTestTag()+objTestSuiteXml.suiteEnd