import sys
import time
import java.math.BigDecimal as BigDecimal
import java.sql as sql
import com.hyperion.aif.scripting.API as API

print(sys.version)

from sys import path
from test.pickletester import protocols
path.append("C:\\Users\\ZhouW2\\Desktop\\ETL\\EclipseInstallation\\poi-3.8-20120326.jar")
path.append("C:\\Users\\ZhouW2\\Desktop\\ETL\\EclipseInstallation\\poi-ooxml-3.8-20120326.jar")

from org.apache.poi.xssf.usermodel import *        
from java.io import FileInputStream
from org.apache.poi.ss.usermodel import *
from datetime import datetime
import java.io as io
from org.apache.poi.xssf.extractor import *
from org.apache.poi.xssf.extractor.XSSFEventBasedExcelExtractor import *
        
        #Create a folder with time stamp
folder = io.File("C:hos")
print "folder path is: %s" % folder

for fileEntry in folder.listFiles():
  if fileEntry.isFile():
    file = folder.getAbsolutePath() + "\\" + fileEntry.getName()
    fis = FileInputStream(file)
    wb = XSSFWorkbook(fis)
    sheetob=wb.getSheetAt(2)
    sheetname = sheetob.getSheetName()
    sheet = wb.getSheet(sheetname)
    rows = sheet.getPhysicalNumberOfRows()
    rNum = 19
    
    
    while True:
      row = sheet.getRow(rNum)
      cell = row.getCell(1).toString().strip()

      if 'Totals' in cell:
      #if not cell:
        break
      
      rNum = rNum + 1
      #print row.getCell(2).toString().strip()
      
    filenameis = fileEntry.getName()
    totalline = rNum - 19
    print "Total line # of file '%s' is: %d" %(filenameis,totalline)
    
    fis.close()

#print "fl is %s" % fl
#print "newFl is %s" % newFl
print "Count End"
