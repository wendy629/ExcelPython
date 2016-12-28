'''
Created on Dec 20, 2016
FromLocal
@author: zhouwendy
'''
import sys

import java.math.BigDecimal as BigDecimal
import java.sql as sql
import com.hyperion.aif.scripting.API as API
from org.apache.poi.xssf.usermodel import *
from org.apache.poi.ss.usermodel import *
from java.io import FileInputStream
from org.apache.poi.xssf.extractor import *
import glob


fdmAPI = API()
conn = None
conn = sql.DriverManager.getConnection("jdbc:oracle:thin:@192.168.4.244:1530:hd01", "FDMEE", "orahd01");
conn.setAutoCommit(False)
fdmAPI.initializeDevMode(conn);
print "SUCCESS CONNECTING TO DB"
fdmContext = fdmAPI.initContext(BigDecimal(15059))

Locname =fdmContext["LOCNAME"] 

outfilename = fdmContext["INBOXDIR"]+"/DataFile2222.txt"
outfile = open(outfilename, "w")

#fileoutw=open("C:\\Users\\ZhouW2\\Desktop\\ETL\\FDMEETest.txt","w")
outfile.write(Locname)

#filelist = [fdmContext["INBOXDIR"]+"\\MOHLTC-OGOS-2016-PD12-0002 - IFIS 43366768 - TCA Disposal.xlsm",fdmContext["INBOXDIR"]+"\\HOSP-2016-PD12-0010 - 43666390 - BPS 646 Deep River Hospital.xlsm"]


if __name__ == '__main__':
    pass
