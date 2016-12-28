'''
Created on Dec 28, 2016

@author: ZhouW2
'''

#----------Import Lib Pkg Start----------
from sys import path
path.append("C:\\hyp\\EPMSystem11R1\\products\\FinancialDataQuality\\lib\\poi-3.8-20120326.jar")
path.append("C:\\hyp\\EPMSystem11R1\\products\\FinancialDataQuality\\lib\\poi-ooxml-3.8-20120326.jar")
path.append("C:\\hyp\EPMSystem11R1\\products\\FinancialDataQuality\\lib\\poi-ooxml-schemas-3.8.jar")


import sys
from org.apache.poi.xssf.usermodel import *
from org.apache.poi.xssf.extractor import *
from java.io import FileInputStream
import glob
import java.math.BigDecimal as BigDecimal
import java.sql as sql
import com.hyperion.aif.scripting.API as API

fdmAPI = API()
fdmContext = fdmAPI.initContext(BigDecimal(15059))
fileout = fdmContext["INBOXDIR"]+"\\LocnameDataFile.txt"
fileoutw=open(fileout,"w")

filelist = [fdmContext["INBOXDIR"]+"\\MOHLTC-OGOS-2016-PD12-0002 - IFIS 43366768 - TCA Disposal.xlsm",fdmContext["INBOXDIR"]+"\\HOSP-2016-PD12-0010 - 43666390 - BPS 646 Deep River Hospital.xlsm"]
#----------works--------------------------

#-----------------------------------------
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
  #-------------------works---------------------
  
  
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
fisin.close()

print 'Export successfully!'