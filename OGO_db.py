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
fdmContext = fdmAPI.initContext(BigDecimal(15185))
print fdmContext
print fdmContext["LOCNAME"]
print fdmContext["LOCKEY"]
print fdmContext["APPID"] 
print fdmContext["RULEID"] 

locname=fdmContext["LOCNAME"]

def prepare_str(val):
    if val:
        if type(val) is str or type(val) is unicode:
            return val.strip().replace("'", "''").replace(",","''")[:74]
        else:
            return val.toString().strip().replace("'", "''").replace(",","''")[:74]
    return 'Null'

#RSet = fdmAPI.executeQuery("SELECT nvl(b.PARTNAME, a.PARTNAME) PartLocation FROM TPOVPARTITION a left join TPOVPARTITION b ON a.partparentkey=b.PARTITIONKEY WHERE a.PARTNAME = '"+locname+"'", []) 
#print "SELECT nvl(b.PARTNAME, a.PARTNAME) PartLocation FROM TPOVPARTITION a left join TPOVPARTITION b ON a.partparentkey=b.PARTITIONKEY WHERE a.PARTNAME = '%s' " % locname

#if RSet.next(): pl = RSet.getString('PartLocation')

#if pl == 'LOC_CONSBX_ENTITY':
if 2>1:
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
        inspreSQL = " INTO AIF_OPEN_INTERFACE (BATCH_NAME, CURRENCY, DATAVIEW, DESC1, DESC2, AMOUNT, COL01, COL02)"
        for fileEntry in folder.listFiles():
           if fileEntry.isFile():
                sSQL = ""
                file = folder.getAbsolutePath() + "\\" + fileEntry.getName()
                fis = FileInputStream(file)
                wb = XSSFWorkbook(fis)
                sheet = wb.getSheet('TB')
                rows = sheet.getPhysicalNumberOfRows()
                rNum = 5
                
                
                #while cellft in ['BOG Adjustment','BOG Redistribution','BOG Statements','Elimination']:
                while True:
                    #print "Yes, FileType: %s" % cellft
                    row = sheet.getRow(rNum)
                    cell = row.getCell(0).toString().strip()
                    
                    if not cell:
                        break

                    insSQL = inspreSQL + " VALUES ('CONSBX', 'CAD', 'YTD', '" + prepare_str(row.getCell(0)) + "', " + "'" + prepare_str(str(fileEntry.getName())) + "' , "
                    
                    evaluator = wb.getCreationHelper().createFormulaEvaluator()
                    
                    if row.getCell(4) and row.getCell(4).toString().strip(): 
                        cellValue = evaluator.evaluate(row.getCell(4))
                        #print cellValue
                        insSQL = insSQL + str(cellValue.getNumberValue()) + ", "
                    else:
                        insSQL = insSQL + "Null , "
                        cellValue = '0'
                    
                    formatter = DataFormatter()
                    insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(1)) + "','"
    
                    #print row.getCell(2)
                    '''
                    if row.getCell(2) != '' and row.getCell(2) != 'None':
                        if row.getCell(2) and row.getCell(2).toString().strip(): 
                          cellValue = evaluator.evaluate(row.getCell(2))
                          insSQL = insSQL + str(cellValue.getNumberValue()) + ") "
                        else:
                          insSQL = insSQL + "0')"
                          cellValue = '0'
                    else:
                        insSQL = insSQL + "'ICPNONE')"
                    '''
                  
                    #if (row.getCell(2) == '' or row.getCell(2) == 'None'):
                    #   insSQL = insSQL + "'ICPNONE')"
                    #else:
                    if row.getCell(2) and row.getCell(2).toString().strip(): 
                      cellValue = evaluator.evaluate(row.getCell(2))
                      insSQL = insSQL + str(cellValue.getStringValue()) + "') "
                    else:
                      insSQL = insSQL + "None')"
                      cellValue = '0'

                    print insSQL
                    sSQL = sSQL + insSQL
                       
                        #sSQL = sSQL + insSQL + ';' + '\n'
                        #fdmAPI.executeDML(insSQL, [], True)
                    rNum = rNum + 1
                
                #fdmAPI.executeDML(sSQL, [], True)
                #fdmAPI.executeDML('INSERT ALL '+ sSQL + 'select * from dual;', [], True)
                
                print 'INSERT ALL '+ sSQL + 'select * from dual;'
                #fdmAPI.commitTransaction()
                fis.close()

                print "start to move file"
                fl = io.File(folder.getAbsolutePath() + "\\" + fileEntry.getName())
                newFl = io.File(copyFolder.getAbsolutePath() + "\\" + fileEntry.getName())
                fl.renameTo(newFl)


          
    except:
  
        fdmAPI.logError("BefImport. Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
        fdmAPI.logError("insSQL: %s " % (insSQL))
        raise

#print "fl is %s" % fl
#print "newFl is %s" % newFl
print "OGO file load End"

