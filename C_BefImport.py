import sys
import time
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
fdmContext = fdmAPI.initContext(BigDecimal(15447))
print fdmContext
print fdmContext["LOCNAME"]
print fdmContext["LOCKEY"]
print fdmContext["APPID"] 
print fdmContext["RULEID"] 

locname=fdmContext["LOCNAME"]
pername=fdmContext["PERIODNAME"][:3]


def prepare_str(val):
    if val:
        if type(val) is str or type(val) is unicode:
            return val.strip().replace("'", "''")[:74]
        else:
            return val.toString().strip().replace("'", "''")[:74]
    return 'Null'

RSet = fdmAPI.executeQuery("SELECT nvl(b.PARTNAME, a.PARTNAME) PartLocation FROM TPOVPARTITION a left join TPOVPARTITION b ON a.partparentkey=b.PARTITIONKEY WHERE a.PARTNAME = '"+locname+"'", []) 
print "SELECT nvl(b.PARTNAME, a.PARTNAME) PartLocation FROM TPOVPARTITION a left join TPOVPARTITION b ON a.partparentkey=b.PARTITIONKEY WHERE a.PARTNAME = '%s' " % locname

if RSet.next(): pl = RSet.getString('PartLocation')

if pl == 'LOC_CONSBX_BPS' :

    print "--Target App is found"
    try:
  
        path = 'C:\poi'
        sys.path.append(path + '\poi-3.15.jar')
        sys.path.append(path + '\poi-ooxml-3.15.jar')
        sys.path.append(path + '\poi-ooxml-schemas-3.15.jar')

        #from org.apache.poi.xssf.usermodel import *
        #from org.apache.poi.hssf.usermodel import *
        import org.apache.poi.xssf.usermodel.XSSFWorkbook as XSSFWorkbook
        import org.apache.poi.xssf.usermodel.XSSFSheet as XSSFSheet
        import org.apache.poi.xssf.usermodel.XSSFRow as XSSFRow
        import org.apache.poi.xssf.usermodel.XSSFCell as XSSFCell
        import org.apache.poi.xssf.usermodel.XSSFFormulaEvaluator as XSSFFormulaEvaluator
        import org.apache.poi.hssf.usermodel.HSSFWorkbook as HSSFWorkbook
        import org.apache.poi.hssf.usermodel.HSSFSheet as HSSFSheet
        import org.apache.poi.hssf.usermodel.HSSFRow as HSSFRow
        import org.apache.poi.hssf.usermodel.HSSFCell as HSSFCell
        import org.apache.poi.hssf.usermodel.HSSFFormulaEvaluator as HSSFFormulaEvaluator
        from java.io import FileInputStream
        from org.apache.poi.ss.usermodel import *
        from datetime import datetime
        
        import java.io as io
        
        #Create a folder with time stamp
        
        if locname[-3:]=="EDU" and pername =="Mar":
          folder = io.File("C:Mar")
        elif locname[-3:]=="EDU" and pername =="Aug":
          folder = io.File("C:Aug")
        else:
        #  folder = io.File("C:Aug")
          folder = io.File("C:TCUBF")
        
        #folder = io.File("C:hos")
        #print "folder path is: %s" % folder
        #copyFolder = io.File(folder.getAbsolutePath()+ "\\" + datetime.now().strftime('%Y%m%d_%H%M%S'))
        #print "folder with timestamp locates at: %s" % copyFolder
        #copyFolder.mkdir()
        

        
        #Delete so will not reload the previously file?
        print "Start SQL delete"
        delSQL = "DELETE FROM AIF_OPEN_INTERFACE WHERE BATCH_NAME = 'CONSBX'"
        fdmAPI.executeDML(delSQL, [], True)
        fdmAPI.commitTransaction()

        print "Start SQL pre-insert"
        inspreSQL = " INTO AIF_OPEN_INTERFACE (BATCH_NAME, CURRENCY, DATAVIEW, DESC1, DESC2, AMOUNT, COL01, COL02, COL03, COL04, COL05, COL06)"
        for fileEntry in folder.listFiles():
           if fileEntry.isFile():
                sSQL = ""
                file = folder.getAbsolutePath() + "\\" + fileEntry.getName()
                fis = FileInputStream(file)


                if fileEntry.getName().split(".")[-1]=='xlsm':
                #  print 'yes'
                  wb = XSSFWorkbook(fis)
                  sheetob1=wb.getSheetAt(1)
                  sheetob2=wb.getSheetAt(2)
                #print sheetob1
                  sheetname1 = sheetob1.getSheetName()
                  sheetname2 = sheetob2.getSheetName()
                #print "sheetname1=%s" % sheetname1
                #print "sheetname2=%s" % sheetname2
                  if sheetname1=='Sheet1':
                    sheet = wb.getSheet(sheetname1)
                  #print "sheet 1 wins"
                  else:
                    sheet = wb.getSheet(sheetname2)
                  #print "sheet 2 wins"
                else:
                  wb = HSSFWorkbook(fis)
                  sheet = wb.getSheet('Sheet1')
                
                #wb = XSSFWorkbook(fis)
                #sheet = wb.getSheet('Sheet1')


                rows = sheet.getPhysicalNumberOfRows()
                rNum = 19
                
                #file type detector
                rowft = sheet.getRow(7)
                cellft = rowft.getCell(4).toString().strip()
                
                print "FileType: %s" % cellft
                
                #while cellft in ['BOG Adjustment','BOG Redistribution','BOG Statements','Elimination']:

                while True:
                    #print "Yes, FileType: %s" % cellft
                    row = sheet.getRow(rNum)
                    cell = row.getCell(1).toString().strip()

                    if 'Totals' in cell:
                    #if cellDR == cellCR:
                    #if not cell:
                        break

                    
                    insSQL = inspreSQL + " VALUES ('CONSBX', 'CAD', 'YTD', '" + prepare_str(row.getCell(10)) + "', " + "'" + prepare_str(str(fileEntry.getName())) + "' , "
                    
                    evaluator = wb.getCreationHelper().createFormulaEvaluator()
                    if row.getCell(8) and row.getCell(8).toString().strip(): 
                        cellValue = evaluator.evaluate(row.getCell(8))
                        insSQL = insSQL + str(cellValue.getNumberValue()) + ", "
                        #print "8" + insSQL
                    elif row.getCell(9) and row.getCell(9).toString().strip(): 
                        cellValue = evaluator.evaluate(row.getCell(9))    
                        insSQL = insSQL + str(cellValue.getNumberValue() * -1) + ", "
                        #print "9" + insSQL                        
                    else:
                        insSQL = insSQL + "Null , "
                        cellValue = '0'
                        
                    '''
                    elif fileEntry.getName()[:8] in ['511A-EDU']:
                      formatter = DataFormatter()
                      cellValue5=evaluator.evaluate(row.getCell(5))
                      #print cellValue5
                      string5=str(cellValue5.getStringValue())
                      if string5 == 'None':
                        string5 = '0000'
                      #print string5
                    
                      insSQL = insSQL + "'" + fdmContext["LOCNAME"] + '!'+ formatter.formatCellValue(rowft.getCell(4)) + "', '" + formatter.formatCellValue(row.getCell(2)) +'!'+ formatter.formatCellValue(row.getCell(3)) + "', "
                      insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(4)) + "', '" + string5 + "', "
                      insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(6)) + "', '" + formatter.formatCellValue(row.getCell(7)) + "')"
                    #print "value: " + insSQL
                    '''
                      
                    formatter = DataFormatter()
                    
                    if fileEntry.getName()[:7] in ['453-EDU','463-EDU','711-EDU']:
                      
                      insSQL = insSQL + "'" + fdmContext["LOCNAME"] + '!Elimination' + "', '" + formatter.formatCellValue(row.getCell(2)) +'!'+ formatter.formatCellValue(row.getCell(3)) + "', "
                      insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(4)) + "', '" + formatter.formatCellValue(row.getCell(5)) + "', "
                      insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(6)) + "', '" + formatter.formatCellValue(row.getCell(7)) + "')"
                    elif fileEntry.getName()[:7] in ['201-EDU','202-EDU','101-EDU']:
                      
                      insSQL = insSQL + "'" + fdmContext["LOCNAME"] + '!BOG Adjustment' + "', '" + formatter.formatCellValue(row.getCell(2)) +'!'+ formatter.formatCellValue(row.getCell(3)) + "', "
                      insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(4)) + "', '" + formatter.formatCellValue(row.getCell(5)) + "', "
                      insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(6)) + "', '" + formatter.formatCellValue(row.getCell(7)) + "')"
                    else:
                      
                      #print "NO elimination"
                      insSQL = insSQL + "'" + fdmContext["LOCNAME"] + '!' + formatter.formatCellValue(rowft.getCell(4)) + "', '" + formatter.formatCellValue(row.getCell(2)) +'!'+ formatter.formatCellValue(row.getCell(3)) + "', "
                      insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(4)) + "', '" + formatter.formatCellValue(row.getCell(5)) + "', "
                      insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(6)) + "', '" + formatter.formatCellValue(row.getCell(7)) + "')"
                    
    
                    if cellValue != '0' and cellValue.getNumberValue() != 0 : 
                        insSQL= insSQL.encode('utf8')
                        sSQL = sSQL + insSQL
                        #sSQL = sSQL + insSQL + ';' + '\n'
                        #fdmAPI.executeDML(insSQL, [], True)
                        #print sSQL
                    rNum = rNum + 1
                


                #fdmAPI.executeDML(sSQL, [], True)
                #fdmAPI.executeDML('INSERT ALL '+ sSQL + 'select * from dual;', [], True)
                print "sql statement:" + 'INSERT ALL'+ sSQL + 'select * from dual;'
                #print "##########"
                #fdmAPI.commitTransaction()
                fis.close()

                #print "start to move file"
                #fl = io.File(folder.getAbsolutePath() + "\\" + fileEntry.getName())
                #newFl = io.File(copyFolder.getAbsolutePath() + "\\" + fileEntry.getName())
                #fl.renameTo(newFl)

          
    except:
  
        fdmAPI.logError("BefImport. Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
        fdmAPI.logError("insSQL: %s " % (insSQL))
        raise

#print "fl is %s" % fl
#print "newFl is %s" % newFl
    print "ADI file load End"

if pl == 'LOC_CONSBX_ENTITY':

    print "--Target App is found"
    try:
  
        path = 'C:\poi'
        sys.path.append(path + '\poi-3.15.jar')
        sys.path.append(path + '\poi-ooxml-3.15.jar')
        sys.path.append(path + '\poi-ooxml-schemas-3.15.jar')

        from org.apache.poi.xssf.usermodel import *
        from java.io import FileInputStream
        from org.apache.poi.ss.usermodel import *
        from datetime import datetime
        import java.io as io
        
        #Create a folder with time stamp
        folder = io.File("C:OGO")
        print "folder path is: %s" % folder
        copyFolder = io.File(folder.getAbsolutePath()+ "\\" + datetime.now().strftime('%Y%m%d_%H%M%S'))
        print "folder with timestamp locates at: %s" % copyFolder
        copyFolder.mkdir()
        

        #Delete so will not reload the previously file?
        print "Start SQL delete"
        delSQL = "DELETE FROM AIF_OPEN_INTERFACE WHERE BATCH_NAME = 'CONSBX'"
        fdmAPI.executeDML(delSQL, [], True)
        fdmAPI.commitTransaction()

        print "Start SQL pre-insert"
        inspreSQL = " INTO AIF_OPEN_INTERFACE (BATCH_NAME, CURRENCY, DATAVIEW, DESC1, DESC2, AMOUNT, COL01, COL02, COL03, COL04, COL05, COL06)"
        for fileEntry in folder.listFiles():
           if fileEntry.isFile():
                sSQL = ""
                file = folder.getAbsolutePath() + "\\" + fileEntry.getName()
                fis = FileInputStream(file)
                wb = XSSFWorkbook(fis)
                sheet = wb.getSheet('Sheet1')
                rows = sheet.getPhysicalNumberOfRows()
                rNum = 5
                
                
                #while cellft in ['BOG Adjustment','BOG Redistribution','BOG Statements','Elimination']:
                while True:
                    #print "Yes, FileType: %s" % cellft
                    row = sheet.getRow(rNum)
                    cell = row.getCell(2).toString().strip()

                    if not cell:
                        break

                    insSQL = inspreSQL + " VALUES ('CONSBX', 'CAD', 'YTD', '" + prepare_str(row.getCell(10)) + "', " + "'" + prepare_str(str(fileEntry.getName())) + "' , "
                    
                    evaluator = wb.getCreationHelper().createFormulaEvaluator()
                    if row.getCell(8) and row.getCell(8).toString().strip(): 
                        cellValue = evaluator.evaluate(row.getCell(8))
                        #print cellValue
                        insSQL = insSQL + str(cellValue.getNumberValue()) + ", "
                        #print insSQL
                    elif row.getCell(9) and row.getCell(9).toString().strip(): 
                        cellValue = evaluator.evaluate(row.getCell(9))    
                        #print cellValue
                        insSQL = insSQL + str(cellValue.getNumberValue() * -1) + ", "
                    else:
                        insSQL = insSQL + "Null , "
                        cellValue = '0'
                    
                    
                    formatter = DataFormatter()
                    insSQL = insSQL + "'" + fdmContext["LOCNAME"] + '!'+ formatter.formatCellValue(rowft.getCell(4)) + "', '" + formatter.formatCellValue(row.getCell(3)) + "', "
                    insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(4)) + "', '" + formatter.formatCellValue(row.getCell(5)) + "', "
                    insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(6)) + "', '" + formatter.formatCellValue(row.getCell(7)) + "')"
    
                    
    
                    if cellValue != '0' and cellValue.getNumberValue() != 0 : 
                        sSQL = sSQL + insSQL
                        #sSQL = sSQL + insSQL + ';' + '\n'
                        #fdmAPI.executeDML(insSQL, [], True)
                        print "*****************" + sSQL
                    rNum = rNum + 1
                
                
                #fdmAPI.executeDML(sSQL, [], True)
                #fdmAPI.executeDML('INSERT ALL '+ sSQL + 'select * from dual;', [], True)
                #print 'INSERT ALL '+ sSQL + 'select * from dual;'
                #fdmAPI.commitTransaction()
                fis.close()

                #print "start to move file"
                #fl = io.File(folder.getAbsolutePath() + "\\" + fileEntry.getName())
                #newFl = io.File(copyFolder.getAbsolutePath() + "\\" + fileEntry.getName())
                #fl.renameTo(newFl)

                
           #print "DO NOT NEED TO LOAD"
          
    except:
  
        fdmAPI.logError("BefImport. Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
        fdmAPI.logError("insSQL: %s " % (insSQL))
        raise

#print "fl is %s" % fl
#print "newFl is %s" % newFl
    print "OGO file load End"

