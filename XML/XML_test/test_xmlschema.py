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
    def test_Invalid_Schema(self):
        path = os.getcwd()+'/XML/XML_test/'
        with pytest.raises(ParseError) as excinfo:
            xmlschema.XMLSchema(path+"BancoInvalidSchema.xsd")
        
        print("ParseError: %s" % excinfo.value)

    def test_is_Valid_XML(self):
        path = os.getcwd()+'/XML/XML_test/'
        XSFormacion = xmlschema.XMLSchema(path+"BancoSchema.xsd")
        assert XSFormacion.is_valid(path+"Banco.xml")

    def test_is_Invalid_XML(self):
        path = os.getcwd()+'/XML/XML_test/'
        XSFormacion = xmlschema.XMLSchema(path+"BancoSchema.xsd")
        assert not XSFormacion.is_valid(path+"Banco_Invalido.xml")
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()