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
#----------Import Lib Pkg End----------

#----------Initialize Start---------- 
'''
filein = fdmContext["INBOXDIR"]+"/InputFile.txt"
fileout = fdmContext["INBOXDIR"]+"/DataFile.txt"
fileoutw = open(fileout, "w")
'''
#filein = "C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGOForm_SourceData_FlipSignTest.xlsx"
filein = "C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16_WendyCopy_OriginalTest.xlsx"
#filein="C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0001 - 43158271 - MtM Op. Balances.xlsm"
print filein
fisin = FileInputStream(filein)
print fisin

wbin = XSSFWorkbook(fisin)
sheetin = wbin.getSheet('TB')
print wbin, sheetin


#fileoutw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGOForm_SourceData_FlipSignTest.txt","w")
fileoutw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16w_WendyCopy_OriginalTest_Formula.txt","w")
#fileoutw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0001 - 43158271 - MtM Op. Balances.txt","w")
#----------Initialize End---------- 

'''
#Extract text file instead of formula, but work on whole workbook, not a specific sheet
ee = XSSFExcelExtractor(wbin)
ee.setFormulasNotResults(False)
ee.setIncludeSheetNames(False);
cellText=ee.getText()
fileoutw.write(cellText.encode('utf8'))
'''


#----------Counting the No. of Columns Start----------
colCount = 14 
tmp = 0

# This ensures that we get the data properly even if it doesn't start from first few rows
for i in range(0, 15,1):
    row = sheetin.getRow(i)
    #row = sheetin.getRow(i)
    

    if(row != None):
        #tmp = sheetin.getRow(i).getPhysicalNumberOfCells()
        tmp = sheetin.getRow(i).getLastCellNum()
        if tmp > colCount:
            colCount = tmp
      
   
# Print No. of rows and columns
print "Cols = %d" % (colCount)
rowCount = sheetin.getPhysicalNumberOfRows()
print "Rows = %d" % (rowCount)
#----------Counting the No. of Columns End----------


#Read and Write (formula, not text)
for r in range(1, rowCount, 1):
    rowin = sheetin.getRow(r)
    #print r+1
    if(rowin != None):
      for c in range(0, colCount, 1):
        cellin = rowin.getCell(c)
        #cellin.setCellValue(int(rowin.getCell(c)))
        #print cellin.getCellType()
        print "%s" % (cellin)
        #cellin.setCellType(Cell.CELL_TYPE_NUMERIC)
        #data =cellin.getNumericCellValue()
        #fileoutw.write("%s" % (data)+",")
        fileoutw.write("%s" % (cellin)+" \t")
        #fileoutw.write(cellin.getNumericCellValue());
      print "\n"            
    fileoutw.write("\n")


fileoutw.close()
fisin.close()
print 'Export successfully!'