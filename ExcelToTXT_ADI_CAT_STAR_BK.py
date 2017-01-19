'''
Created on Dec 20, 2016

@author: zhouwendy

'''
#----------Import Lib Pkg Start----------
from sys import path
from test.pickletester import protocols
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
'''
fdmAPI = API()
conn = None
conn = sql.DriverManager.getConnection("jdbc:oracle:thin:@192.168.4.244:1530:hd01", "FDMEE", "orahd01");
conn.setAutoCommit(False)
fdmAPI.initializeDevMode(conn);
print "SUCCESS CONNECTING TO DB"
fdmContext = fdmAPI.initContext(BigDecimal(15045))

'''
fileout="C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\addCategory.txt"
fileoutw=open(fileout,"w")

fileoutfinal="C:\\Users\\ZhouW2\\Desktop\\ETL\\ADI\\SourceFileFrom3mins\\MOHLTC\\final.txt"

#fileout = fdmContext["INBOXDIR"]+"/EDU101.txt"
print "======="
print fileoutw
print"========"
#fileoutw=open(fileout)
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
    fileoutw.write("\nFileStarts\n")
    fileoutw.write(cellText.encode('utf8'))
    fileoutw.write("\nFileEnds\n")    
    row_idx=row_idx+rowCount
  else:
    for r in range(row_idx+1,rowCount+row_idx+1,rowCount):
  #  for c in range(0,colCount,1):
      #print f
      #print "=========="
      cellText=ee.getText()
      fileoutw.write(f)
      fileoutw.write("\nFileStarts\n")
      fileoutw.write(cellText.encode('utf8'))
      fileoutw.write("\nFileEnds\n") 
      row_idx=row_idx+rowCount
#----------Paste text End----------
fileoutw.close()
f = open(fileout, "rb")

listfs=[]
listfe=[]

print "ffffffffffffffffffffffffffffffffff = %s" %f
for n,line in enumerate(f):
    if "Upl" in line: 
      fs = n+1
      listfs.append(fs)
      print "fs starts at : %d" % (fs)
    if "FileEnds" in line: 
      fe = n+1
      listfe.append(fe)
      print "fe ends at : %d" % (fe)

print listfs
print listfe

#-------First Cleaning:add category------


#list1=list[0::2]
#list2=list[1::2]
f = open(fileout, "rb")
listcg=[]
listoflen=len(listfs)
for m,lines in enumerate(f):
    cols = lines.split()
    #print "cols= %s" % (cols)
    for n, word in enumerate(cols):  
        #print "cols0= %s" % (cols[0])
        if word in ['Category']:
            print(word,cols[n+6],cols[n+7]) 
            listcg.append(cols[n+7])
print listcg

fileoutw.close() #test#


f = open(fileout, "rb")
for l in range (0,listoflen):
    f = open(fileout, "rb")
    print "l=%d" %l
    for m,lines in enumerate(f):
      lines=lines.replace('*','')
      cols=lines.split()
      #f = open(fileout, "rb")
      if (listfs[l] < m < listfe[l] ):
        
        cols.insert(0, listcg[l])
        print cols #could be inserted to databse directly as it is comma dilimited?
        
        
        #fileoutw=open(fileout,"w")#test
        #for i in cols:#test
         # fileoutw.write(i)#test
      #fileoutw.close()#test
    fileoutw.close()
#-------First Cleaning:add category------
fileoutw.close()

print 'Export successfully!'