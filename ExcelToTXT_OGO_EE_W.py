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
from org.apache.poi.xssf.usermodel.XSSFTextRun import *
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
#filein="C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16_WendyCopy_OriginalTest.xlsx"
filein = "C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16_WendyCopy_FormatBrush.xlsx"
print filein
fisin = FileInputStream(filein)
print fisin

wbin = XSSFWorkbook(fisin)
sheetin = wbin.getSheet('TB')
print wbin, sheetin

#fileout="C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16_WendyCopy_OriginalTest.txt"
fileout="C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16_WendyCopy_FormatBrush.txt"
fileoutw=open(fileout,"w")
#----------Initialize End---------- 


#Extract text file instead of formula, but work on whole workbook, not a specific sheet
ee = XSSFExcelExtractor(wbin)
ee.setFormulasNotResults(False)
ee.setIncludeSheetNames(True);
cellText=ee.getText()
fileoutw.write(cellText.encode('utf8'))
fileoutw.close()




fileintxt=fileout
#fileouttxtw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16_WendyCopy_OriginalTest_TBonly.txt","w")
fileouttxtw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16_WendyCopy_FormatBrush_TBonly.txt","w")
#fileintxt="C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\rowcountertest.txt"

'''
a=open(fileintxt,'rb')
lines = a.readlines()
if lines:
    first_line = lines[:1]
    last_line = lines[-1]
print last_line
'''
'''
f = open(fileintxt,'r')
line_num = 0
search_phrase = "CHECK"
for line in f.readlines():
    line_num += 1
    if line.find(search_phrase) >= 0:
        print line_num
#rowTB=
'''
'''
for n,line in enumerate(open(fileintxt)):
    if "Other Opening accumulated amorti" in line: print n+1
'''
#for r in range (rowTB,rows,1)
f = open(fileintxt, "rb")


for n,line in enumerate(f):
    if "TB" in line: 
      TBRow = n+1
      print "TB row starts at : %d" % (TBRow)

lastRow = sum(1 for line in open(fileintxt))
print "Row ends at : %d" % (lastRow)

lastCol = len(line.split())
print "Column ends at: ", lastCol

f = open(fileintxt, "rb")
i = 0
for line in f:
  i += 1
  if (TBRow-1 < i):
    fileouttxtw.write(line)

fileouttxtw.close()




'''
lastCol = f.readline().count('\t\r') + 1
print lastCol
'''
'''
for i in range (TBRow, lastRow, 1):
    k = i.split()
    for j in k:
        print j
'''
'''  
for line in f:
  if (1444 < line < 1739):
  #for j in range (0,lastCol,1):
    #print "(i = %d,j = %d)" %(i,j)
    result = f.readlines()
    print  result
'''    



'''
eee = XSSFEventBasedExcelExtractor(wbin)
eee.processSheet()
eee.setFormulasNotResults(False)
eee.setIncludeSheetNames(True);
cellTexteee=eee.getText()
#print cellText.encode('utf8')
fileoutw.write(cellTexteee.encode('utf8'))
''' 


'''
eee = XSSFEventBasedExcelExtractor()
eee.processSheet(sheetin)
eee.setFormulasNotResults(False)
eee.setIncludeSheetNames(True);
cellTexteee=eee.getText()
#print cellText.encode('utf8')
fileoutw.write(cellTexteee.encode('utf8'))
'''

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

#Numeric Cell type (0)
#String Cell type (1)
#Formula Cell type (2)
#Blank Cell type (3)
#Boolean Cell type (4)
#Error Cell type (5)

'''
#Read and Write (formula, not text)
for r in range(1, rowCount, 1):
    rowin = sheetin.getRow(r)
    #print r+1
    if(rowin != None):
      for c in range(0, colCount, 1):
        cellin = rowin.getCell(c)
        #cellin.setCellValue(int(rowin.getCell(c)))
        #print cellin.getCellType()
        #cellin.setCellType(Cell.CELL_TYPE_NUMERIC)
        #data =cellin.getNumericCellValue()
        #fileoutw.write("%s" % (data)+",")
        #fileoutw.write("%d" % (cellin)+",")
        #fileoutw.write(cellin.getNumericCellValue());
      print "\n"            
    fileoutw.write("\n")
'''


