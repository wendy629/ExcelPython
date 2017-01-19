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
fdmContext = fdmAPI.initContext(BigDecimal(15223))
print fdmContext
print fdmContext["LOCNAME"]
print fdmContext["LOCKEY"]
print fdmContext["APPID"] 
print fdmContext["RULEID"] 

locname=fdmContext["LOCNAME"]

def prepare_str(val):
    if val:
        if type(val) is str or type(val) is unicode:
            return val.strip().replace("'", "''")[:74]
        else:
            return val.toString().strip().replace("'", "''")[:74]
    return 'Null'

if fdmContext["TARGETAPPNAME"] == 'CONSOLSBX':

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

        delSQL = "DELETE FROM HYP_FDM.dbo.AIF_OPEN_INTERFACE WHERE BATCH_NAME = 'CONSBX'"
        fdmAPI.executeDML(delSQL, [], True)
        fdmAPI.commitTransaction()

        folder = io.File("c:tcu")
        need_mkdir = True

        inspreSQL = "INSERT INTO HYP_FDM.dbo.AIF_OPEN_INTERFACE (BATCH_NAME, CURRENCY, DATAVIEW, DESC1, DESC2, AMOUNT, COL01, COL02, COL03, COL04, COL05, COL06)"
        for fileEntry in folder.listFiles():
           if fileEntry.isFile():
                sSQL = ""
                file = folder.getAbsolutePath() + "\\" + fileEntry.getName()
                fis = FileInputStream(file)
                wb = XSSFWorkbook(fis)
                sheet = wb.getSheet('TB')
                rows = sheet.getPhysicalNumberOfRows()
                rNum = 19
                while True:
                    row = sheet.getRow(rNum)
                    cell = row.getCell(2).toString().strip()

                    if not cell:
                        break

                    insSQL = inspreSQL + " VALUES ('CONSBX', 'CAD', 'YTD', '" + prepare_str(row.getCell(10)) + "', " + "'" + prepare_str(str(fileEntry.getName())) + "' , "

                    evaluator = wb.getCreationHelper().createFormulaEvaluator()
                    if row.getCell(8) and row.getCell(8).toString().strip(): 
                        cellValue = evaluator.evaluate(row.getCell(8))
                        insSQL = insSQL + str(cellValue.getNumberValue()) + ", "
                    elif row.getCell(9) and row.getCell(9).toString().strip(): 
                        cellValue = evaluator.evaluate(row.getCell(9))
                        insSQL = insSQL + str(cellValue.getNumberValue()) + ", "
                    else:
                        insSQL = insSQL + "Null , "
                        cellValue = '0'

                    formatter = DataFormatter()
                    insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(2)) + "', '" + formatter.formatCellValue(row.getCell(3)) + "', "
                    insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(4)) + "', '" + formatter.formatCellValue(row.getCell(5)) + "', "
                    insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(6)) + "', '" + formatter.formatCellValue(row.getCell(7)) + "')"

                    if cellValue != '0' and cellValue.getNumberValue() != 0 : 
                        sSQL = sSQL + insSQL + '\n'
                    rNum = rNum + 1

                fdmAPI.executeDML(sSQL, [], True)
                fdmAPI.commitTransaction()
                fis.close()

                if need_mkdir:
                    copyFolder = io.File(folder.getAbsolutePath()+ "\\" + datetime.now().strftime('%Y%m%d_%H%M%S'))
                    copyFolder.mkdir()
                    need_mkdir = False

                fl = io.File(folder.getAbsolutePath() + "\\" + fileEntry.getName())
                newFl = io.File(copyFolder.getAbsolutePath() + "\\" + fileEntry.getName())
                fl.renameTo(newFl)

        # TBD files processing 
        folder = io.File("C:tcu")
        need_mkdir = True
        for fileEntry in folder.listFiles():
           if fileEntry.isFile():
                sSQL = ""
                file = folder.getAbsolutePath() + "\\" + fileEntry.getName()
                fis = FileInputStream(file)
                wb = XSSFWorkbook(fis)
                sheet = wb.getSheet('TB')
                rows = sheet.getPhysicalNumberOfRows()
                rNum = 5
                fdmAPI.logInfo(file)
                while True:
                    row = sheet.getRow(rNum)
                    if not row:
                        break
                    rNum = rNum + 1
                    accDescr = row.getCell(0).toString().strip()
                    accNum = row.getCell(1).toString().strip()

                    if not accDescr:
                        break

                    if accDescr and not accNum:
                        continue

                    insSQL = inspreSQL + " VALUES ('CONSBX', 'CAD', 'YTD', '" + prepare_str(row.getCell(0)) + "', " + "'" + prepare_str(str(fileEntry.getName())) + "' , "

                    evaluator = wb.getCreationHelper().createFormulaEvaluator()
                    if row.getCell(4) and row.getCell(4).toString().strip(): 
                        cellValue = evaluator.evaluate(row.getCell(4))
                        insSQL = insSQL + str(cellValue.getNumberValue()) + ", "
                    else:
                        insSQL = insSQL + "Null , "
                        cellValue = '0'

                    insSQL = insSQL + "'TBD', " 
                    evaluator = wb.getCreationHelper().createFormulaEvaluator()

                    clv = evaluator.evaluate(row.getCell(2))
                    if clv:
                        insSQL = insSQL + "'" + str(clv.getStringValue()) + "', "
                    else:
                        insSQL = insSQL + "'None', "
                    formatter = DataFormatter()
                    insSQL = insSQL + "'" + formatter.formatCellValue(row.getCell(1)) + "', Null, Null, Null )"

                    if cellValue != '0' and cellValue.getNumberValue() != 0 : 
                        sSQL = sSQL + insSQL + '\n'

                fdmAPI.executeDML(sSQL, [], True)
                fdmAPI.commitTransaction()
                fis.close()

                if need_mkdir:
                    copyFolder = io.File(folder.getAbsolutePath()+ "\\" + datetime.now().strftime('%Y%m%d_%H%M%S'))
                    copyFolder.mkdir()
                    need_mkdir = False

                fl = io.File(folder.getAbsolutePath() + "\\" + fileEntry.getName())
                newFl = io.File(copyFolder.getAbsolutePath() + "\\" + fileEntry.getName())
                fl.renameTo(newFl)

    except:
        fdmAPI.logError("BefImport. Error: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
        fdmAPI.logInfo("sSQL: %s " % (sSQL))
        fdmAPI.logError("insSQL: %s " % (insSQL))
        raise
