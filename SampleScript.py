'''
Created on Dec 20, 2016
FromGithub
@author: zhouwendy
'''
import sys

import java.math.BigDecimal as BigDecimal
import java.sql as sql
import com.hyperion.aif.scripting.API as API

print(sys.version)

fdmAPI = API()
conn = None
conn = sql.DriverManager.getConnection("jdbc:oracle:thin:@192.168.4.244:1530:hd01", "FDMEE", "orahd01");
conn.setAutoCommit(False)
fdmAPI.initializeDevMode(conn);
print "SUCCESS CONNECTING TO DB"
fdmContext = fdmAPI.initContext(BigDecimal(15045))

print fdmContext["LOCNAME"]
print fdmContext["LOCKEY"]
print fdmContext["APPID"] 

if __name__ == '__main__':
    pass
  
'''






































































"""    read.py
Read an existant Excel file (Book1.xls) and show it on the screen
"""   
from sys import path
path.append("C:\\Users\\ZhouW2\\Desktop\\ETL\\EclipseInstallation\\poi-3.8-20120326.jar")
path.append("C:\\Users\\ZhouW2\\Desktop\\ETL\\EclipseInstallation\\poi-ooxml-3.8-20120326.jar")

import sys
from org.apache.poi.xssf.usermodel import *
from org.apache.poi.ss.usermodel import *
from java.io import FileInputStream
from java.io import FileOutputStream

filein = "C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGOForm_SourceData_FlipSignTest.xlsx"
print filein
fisin = FileInputStream(filein)
print fisin
wbin = XSSFWorkbook(fisin)
sheetin = wbin.getSheetAt(2)
# get No. of rows
print wbin, sheetin

wbout = XSSFWorkbook()
fileOut = FileOutputStream("C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGOForm_SourceData_FlipSignTest2.xlsx")
sheetout = wbout.createSheet("TB_FDMEE")
'''
'''
fileout = "C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGOForm_SourceData_FlipSignTest.csv"
print fileout
fisout = FileOutputStream(fileout)
print fisout
wbout = XSSFWorkbook(fisout)
sheetout = wbout.getSheetAt(0)
print wbout, sheetout


colCount = 0 # No. of columns
tmp = 0

# This trick ensures that we get the data properly even if it
# doesn't start from first few rows

for i in range(0, 10,1):
    row = sheetin.getRow(i)
    if(row != None):
        tmp = sheetin.getRow(i).getPhysicalNumberOfCells()
        if tmp > colCount:
            colCount = tmp
print "Cols = %d" % (colCount)
rowCount = sheetin.getPhysicalNumberOfRows()
print "Rows = %d" % (rowCount)

for r in range(0, rowCount, 1):
    rowin = sheetin.getRow(r)
    print r
    if(rowin != None):
        for c in range(0, colCount, 1):
            cellin = rowin.getCell(c)
            if cellin != None:
                print cellin


for q in range(0, rowCount, 1):
    rownew = sheetout.createRow(q)
    rowout = sheetout.getRow(q)
    print q
    if(rowout != None):
        for p in range(0, colCount, 1):
            cell = rownew.createCell(p)
            cellout = rowout.getCell(p)
            if cellout != None:
              cell.setCellValue(666)


wbout.write(fileOut)
fileOut.close()

#wb.close()
fisin.close()

'''

