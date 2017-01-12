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
from org.apache.poi.xssf.extractor import *
from java.io import FileInputStream
import glob
import java.math.BigDecimal as BigDecimal
import java.sql as sql
import com.hyperion.aif.scripting.API as API
#----------Import Lib Pkg End----------

#----------Initialize Start---------- 

#filein = fdmContext["INBOXDIR"]+"/InputFile.txt"

#print glob.glob("C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\*.xlsm")
fdmAPI = API()
conn = None
conn = sql.DriverManager.getConnection("jdbc:oracle:thin:@192.168.4.244:1530:hd01", "FDMEE", "orahd01");
conn.setAutoCommit(False)
fdmAPI.initializeDevMode(conn);
print "SUCCESS CONNECTING TO DB"
fdmContext = fdmAPI.initContext(BigDecimal(15045))
fileout="C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\EDU_Full\\EDU101test.txt"
fileoutw=open(fileout,"w")
#fileout = fdmContext["INBOXDIR"]+"/EDU101.txt"
print "======="
print fileoutw
print"========"
#fileoutw=open(fileout)
#filelist = [ "C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0001 - 43158271 - MtM Op. Balances.xlsm","C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0010 - 43666390 - BPS 646 Deep River Hospital.xlsm","C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\MOHLTC-OGOS-2016-ADJ1-0016 - IFIS 43560690 - CCO Retained Earnings GRE Redistribution.xlsm"]
filelist = glob.glob("C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\EDU_Full\\files\\101test\\*.xlsm")


row_idx=0

for f in filelist:
  filein=f
  print filein
  fisin = FileInputStream(filein)
  print fisin

  wbin = XSSFWorkbook(fisin)
  sheetin = wbin.getSheet('sheet1')
  print wbin, sheetin
  
  ee = XSSFExcelExtractor(wbin)
  ee.setFormulasNotResults(False)
  ee.setIncludeSheetNames(True);
#----------Initialize End---------- 
#----------Counting the No. of Columns Start----------
  colCount = 14 
  tmp = 0
# This ensures that we get the data properly even if it doesn't start from first few rows
  for i in range(0,10,1):
    row = sheetin.getRow(i)
    if(row != None):
# Print No. of columns
      tmp = sheetin.getRow(i).getPhysicalNumberOfCells()
      if tmp > colCount:
        colCount = tmp
  print "Cols = %d" % (colCount)
# Print No. of rows  
  rowCount = sheetin.getPhysicalNumberOfRows()
  print "Rows = %d" % (rowCount)
#----------Counting the No. of Columns End----------

#----------Start to Paste the text----------
  if row_idx==0:
    cellText=ee.getText()
    #print f
    #print "=========="
    fileoutw.write(f)
    fileoutw.write(cellText.encode('utf8'))
    row_idx=row_idx+rowCount
  else:
    for r in range(row_idx+1,rowCount+row_idx+1,rowCount):
  #  for c in range(0,colCount,1):
      #print f
      #print "=========="
      cellText=ee.getText()
      fileoutw.write(f)
      fileoutw.write(cellText.encode('utf8'))
      row_idx=row_idx+rowCount
#----------Paste text End----------

fileoutw.close()
#fisin.close()

fileintxt=fileout
#fileouttxtw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\Prototype\\OGO Reporting Templates 2015-16_WendyCopy_OriginalTest_TBonly.txt","w")
fileouttxtw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\EDU_Full\\EDU101_sheet1Only.txt","w")
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

print "===========start==============="
listRow1=[]
listRow2=[]
rowCounter = 0
Row1=0
Row2=0
for n,line in enumerate(f):
    if "Sheet1" in line: 
      Row1 = n+1
      listRow1.append(Row1)
      print "s1 row starts at : %d" % (Row1)
    if "101 data" in line: 
      Row2 = n+1
      listRow2.append(Row2)
      print "s2 row starts at : %d" % (Row2)

    
    '''
    if Row1 in locals(): 
      for i in range (Row1-1, Row2, 1):
        fileouttxtw.write(line)
        print "**********************"
    else: 
      print "%d R1 NOT EXIST" % (n)
    '''  
          
lastRow = sum(1 for line in open(fileintxt))
print "Row ends at : %d" % (lastRow)

lastCol = len(line.split())
print "Column ends at: ", lastCol


f = open(fileintxt, "rb")
    
print listRow1
print listRow2


listoflen=len(listRow1)
#list1=list[0::2]
#list2=list[1::2]
for l in range (0,listoflen):
    f = open(fileintxt, "rb")
    print "l=%d" %l
    rowCounter = 0
    for line in f:
      rowCounter += 1
      if (listRow1[l] < rowCounter < listRow2[l] ):
        fileouttxtw.write(line)



    #rowCounter = Row2


fileouttxtw.close()

print 'Export successfully!'



