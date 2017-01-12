import sys
import xlrd

workbook=xlrd.open_workbook("C:\Users\ZhouW2\Desktop\ETL\ADI\SourceFileFrom3mins\MOHLTC\HOSP-2016-PD12-0001 - 43158271 - MtM Op. Balances.xlsm")

sh=workbook.sheet_by_name("Sheet1")

print sh.nrows

print sh.ncols

r=0

c=0

file=open("ADITEST2TabD.txt","w")

for r in range(sh.nrows):

    for c in range(sh.ncols):

        data =str(sh.cell_value(r,c))

        print  data,

        file.write(data+" ")

    print 

    file.write("\n")

file.close()