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
import glob

#----------Import Lib Pkg End----------

#----------Initialize Start---------- 
'''
filein = fdmContext["INBOXDIR"]+"/InputFile.txt"
fileout = fdmContext["INBOXDIR"]+"/DataFile.txt"
fileoutw = open(fileout, "w")
'''
'''
filein="C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0001 - 43158271 - MtM Op. Balances.xlsm"
print filein
fisin = FileInputStream(filein)
print fisin

wbin = XSSFWorkbook(fisin)
sheetin = wbin.getSheet('sheet1')
print wbin, sheetin
'''
#print glob.glob("C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\*.xlsm")

fileoutw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\CombinedTest.txt","w")

#filelist = [ "C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0001 - 43158271 - MtM Op. Balances.xlsm","C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\HOSP-2016-PD12-0010 - 43666390 - BPS 646 Deep River Hospital.xlsm","C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\MOHLTC-OGOS-2016-ADJ1-0016 - IFIS 43560690 - CCO Retained Earnings GRE Redistribution.xlsm"]
filelist = glob.glob("C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\*.xlsm")

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
  ee.setIncludeSheetNames(False);
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

'''
row_idx = 0

for r in range (0,rowCount,1):
  for c in range (0,colCount,1):
      #Extract text file instead of formula, but work on whole workbook, not a specific sheet
      
      ee = XSSFExcelExtractor(wbin)
      ee.setFormulasNotResults(False)
      ee.setIncludeSheetNames(False);
      cellText=ee.getText()
      fileoutw.write(cellText.encode('utf8'))
row_idx += 1 


fileoutw.close()
fisin.close()
'''
print 'Export successfully!'