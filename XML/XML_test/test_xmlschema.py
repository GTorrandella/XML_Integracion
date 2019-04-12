'''
Created on Mar 19, 2019

@author: Gabriel Torrandella
'''
import pytest
import unittest
import os
import xmlschema
from xmlschema.etree import ParseError

class TestXML(unittest.case.TestCase):
    
    def setUp(self):
        self.path = os.getcwd()+"/"
        if '/XML/XML_test/' not in self.path:
            self.path += '/XML/XML_test/'
    
    def test_Invalid_Schema(self):
        with pytest.raises(ParseError) as excinfo:
            xmlschema.XMLSchema(self.path+"BancoInvalidSchema.xsd")
        print("ParseError: %s" % excinfo.value)

    def test_is_Valid_XML(self):
        XSFormacion = xmlschema.XMLSchema(self.path+"BancoSchema.xsd")
        self.assertTrue(XSFormacion.is_valid(self.path+"Banco.xml"))

    def test_is_Invalid_XML(self):
        XSFormacion = xmlschema.XMLSchema(self.path+"BancoSchema.xsd")
        self.assertFalse(XSFormacion.is_valid(self.path+"Banco_Invalido.xml"))
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()