'''
Created on Dec 20, 2016

@author: zhouwendy

'''
#----------Import Lib Pkg Start----------
from sys import path
path.append("C:\\Users\\ZhouW2\\Desktop\\ETL\\EclipseInstallation\\poi-3.8-20120326.jar")
path.append("C:\\Users\\ZhouW2\\Desktop\\ETL\\EclipseInstallation\\poi-ooxml-3.8-20120326.jar")

import sys
from org.apache.poi.xssf.usermodel import *
from org.apache.poi.ss.usermodel import *
from java.io import FileInputStream
from org.apache.poi.xssf.extractor import *
from org.apache.poi.xssf.extractor.XSSFEventBasedExcelExtractor import *
#----------Import Lib Pkg End----------

#----------Initialize Start---------- 
'''
filein = fdmContext["INBOXDIR"]+"/InputFile.txt"
fileout = fdmContext["INBOXDIR"]+"/DataFile.txt"
fileoutw = open(fileout, "w")
'''
#filein = "C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGOForm_SourceData_FlipSignTest.xlsx"
#filein = "C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16wendy.xlsx"
filein="C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0001 - 43158271 - MtM Op. Balances.xlsm"
print filein
fisin = FileInputStream(filein)
print fisin

wbin = XSSFWorkbook(fisin)
sheetin = wbin.getSheet('sheet1')
print wbin, sheetin

#Extract text file instead of formula, but work on whole workbook, not a specific sheet
      


#fileoutw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGOForm_SourceData_FlipSignTest.txt","w")
#fileoutw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16wendy.txt","w")
fileoutw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0001 - 43158271 - MtM Op. Balances_EE.txt","w")
#filelist = [ "C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0001 - 43158271 - MtM Op. Balances_EE.xlsm","C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0010 - 43666390 - BPS 646 Deep River Hospital.xlsm"]
#----------Initialize End---------- 

'''
#----------Counting the No. of Columns Start----------
colCount = 0 
tmp = 0
# This ensures that we get the data properly even if it doesn't start from first few rows

for i in range(0, 10,1):
    row = sheetin.getRow(i)
    if(row != None):
        tmp = sheetin.getRow(i).getPhysicalNumberOfCells()
        if tmp > colCount:
            colCount = tmp
            
# Print No. of rows and columns
print "Cols = %d" % (colCount)
rowCount = sheetin.getPhysicalNumberOfRows()
print "Rows = %d" % (rowCount)
#----------Counting the No. of Columns End----------
'''

ee = XSSFExcelExtractor(wbin)
ee.setFormulasNotResults(False)
ee.setIncludeSheetNames(False);
cellText=ee.getText()
fileoutw.write(cellText.encode('utf8'))


fileoutw.close()
fisin.close()
print 'Export successfully!'
