def DRCR_AMOUNT(strField,strRecord):

#--Put record fields in array.

 strFieldList = strRecord.split("  ")

#--Get debit value.

 strAmountDR=strFieldList[7].strip()

#--Get credit value.

 strAmountCR=strFieldList[8].strip()

#--Evaluate Debit/credit values (Begin)

 if (strAmountDR=='null') or (len(strAmountDR)==0):
 
#-- strResult=strAmountCR

  strResult=strAmountCR

 else:

  strResult=strAmountDR

 return strResult
