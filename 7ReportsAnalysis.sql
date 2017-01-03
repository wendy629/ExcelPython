
select * from all_tab_columns where owner = 'IFISER' and table_name = 'GL_PERIOD' order by column_id;



-- Move owner and tablename to with
with
table_name as (
   select upper('ifiser.gl_period') full_tab_name from dual
), 
separator_char as (
   select 'chr(9)' sep_char from dual
),
last_column_id as (
   select max(a.column_id) last_column_id
   from   all_tab_columns a, table_name b 
   where  a.owner || '.' || a.table_name = b.full_tab_name
)
,
data_converison as (
select 
      tc.column_id,
      lc.last_column_id,
      sp.sep_char,
      tc.column_name,
      case 
         when tc.data_type = 'VARCHAR2' 
            then tc.column_name 
         when tc.data_type = 'DATE' 
            then 'to_char(' || tc.column_name || ', ''YYYY-MM-DD HH24:MI:SS'')' 
         when tc.data_type = 'NUMBER' 
            then 'to_char(' || tc.column_name || ')' 
         else 'ERROR: Invalid DATA_TYPE'
      end                  data_cnv_text
   from  
      all_tab_columns   tc,
      table_name        tn,
      separator_char    sp,
      last_column_id    lc
   where 
      tc.owner || '.' || tc.table_name = tn.full_tab_name
)
select statement_num, statement_text from (
select 0000009 statement_num, 'select'     statement_text from dual union all
select 
      dch.column_id * 10 statement_num,
      case 
         when dch.column_id = dch.last_column_id 
            then '   ''' || dch.column_name || ''''
         else
            '   ''' || dch.column_name || ''' || ' || dch.sep_char || ' || '  
      end statement_text
   from  
      data_converison   dch
   union all
select 0009998 statement_num, 'from dual union all' 
                                           statement_text from dual union all   
select 0009999 statement_num, 'select'     statement_text from dual union all
select 
      dch.column_id * 10000 statement_num,
      case 
         when dch.column_id = dch.last_column_id 
            then '   ' || dch.data_cnv_text || ''
         else
            '   ' || dch.data_cnv_text || ' || ' || dch.sep_char || ' || '  
      end statement_text
   from  
      data_converison   dch
   union all
select 9999000 statement_num, 'from ' || tnf.full_tab_name statement_text 
   from table_name tnf union all
select 9999999 statement_num, ';'          statement_text from dual
) stmt order by stmt.statement_num;



select * from IFISER.GL_PERIOD; -- 300 Rows
select * from IFISER.ORGANIZATIONS; -- 3 Rows (ODOE, TP, MAG)
select count(0) from IFISER.AP_OUTSTANDING_INVOICE; -- 12,173,347 Rows
select * from IFISER.AP_OUTSTANDING_INVOICE;

select * from IFISER.GL_PERIOD where PERIOD_NAME_FILTER = 'Apr-16';
select * from IFISER.GL_PERIOD where PERIOD_NAME_FILTER = 'Mar-16';
select * from IFISER.GL_PERIOD where PERIOD_NAME_FILTER like 'Apr-%';
select * from IFISER.GL_PERIOD where FISCAL_YEAR_FILTER = '2017';
select * from IFISER.GL_PERIOD order by period_num desc;
select * from IFISER.ORGANIZATIONS where ORG_SHORT_NAME = 'ODOE';
select * from IFISER.AP_OUTSTANDING_INVOICE where BPS_ID  || ' - '  || BPS_DESCRIPTION = '0102 - Cambrian College of Applied Arts and Technology';
select * from IFISER.AP_OUTSTANDING_INVOICE where MINISTRY_DESCRIPTION = '014 - Health and Long Term Care';
set define off
select * from IFISER.AP_OUTSTANDING_INVOICE where VENDOR_NAME = 'CAMBRIAN COLLEGE OF APPLIED ARTS & TECHNOLOGY';

select * from IFISER.AP_OUTSTANDING_INVOICE;
select * from IFISER.ORGANIZATIONS; -- ODE, TP, MAG
select * from IFISER.AP_INVOICE;

select count(0) from IFISER.AP_OUTSTANDING_INVOICE;


select * from IFISER.AP_OUTSTANDING_INVOICE where invoice_id not in (select distinct invoice_id from IFISER.AP_INVOICE); -- There are some!!!!
select * from IFISER.AP_OUTSTANDING_INVOICE where invoice_id not in (select distinct invoice_id from AP_INVOICE_PAYMENT_DETAILS); -- There are some!!!!

select * from IFISER.AP_OUTSTANDING_INVOICE where invoice_id not in (select distinct invoice_id from IFISER.AP_INVOICES_ALL); 


select * from all_tab_columns where owner = 'IFISER' and column_name = 'INVOICE_ID' order by table_name;

select 'AP_INVOICE_PAYMENT_DETAILS'     table_name, count(0) rec_cnt from AP_INVOICE_PAYMENT_DETAILS union all
select 'IFISER.AP_INVOICE'              table_name, count(0) rec_cnt from IFISER.AP_INVOICE          union all
select 'IFISER.AP_OUTSTANDING_INVOICE'  table_name, count(0) rec_cnt from IFISER.AP_OUTSTANDING_INVOICE;

select 'IFISER.AP_INVOICE_PAYMENT_DETAILS'     table_name, count(0) rec_cnt from IFISER.AP_INVOICE_PAYMENT_DETAILS;
select 'IFISER.AP_INVOICES_ALL'     table_name, count(0) rec_cnt from IFISER.AP_INVOICES_ALL;

-- Run again with schema name on AP_INVOICE_PAYMENT_DETAILS
select * from IFISER.V3_INVOICE_VENDOR_MAP;

select * from IFISER.AP_INVOICE_PAYMENT_DETAILS;
select * from IFISER.AP_OUTSTANDING_INVOICE;

select org_id, period_name, ministry_description, sum(invoice_amount), sum(outstanding_amount) from IFISER.AP_OUTSTANDING_INVOICE 
where ministry_id = '030' and period_name = 'Apr-15' group by org_id, period_name, ministry_description;

select period_name, ministry_description, sum(invoice_amount), sum(outstanding_amount) from IFISER.AP_OUTSTANDING_INVOICE 
where ministry_id = '030' and period_name = 'Apr-15' group by period_name, ministry_description;

-- $30,401,470.01 vs $30,314,673.29


select account_id, cost_centre_id, program_id, period_name, ministry_id, sum(PAID_DISTRIBUTION_AMOUNT), sum(PAYMENT_AMOUNT) from AP_INVOICE_PAYMENT_DETAILS 
where ministry_id = '030' and 
period_name like '%-15' and 
account_id = '215710' and cost_centre_id = '314957'
group by account_id, cost_centre_id, program_id, period_name, ministry_id order by account_id, cost_centre_id, program_id;

-- Apr-15	030	505,205,613.78	1,192,634,116.09

/*******************************************************************************
IFIS Accounts Payable Trial Balance Report

Contains details of all outstanding accounts payable invoices from all selected 
non-sector ministries for each BPS/Sector Ministry OGO.  Total of BPS and 
non-BPS balances should equal to OG account 215110 YTD ending balance.

BPS Reporting: OG Reports  IFIS Accounts Payable Trial Balance  Period Name : 'Last Closed Period' , Ministry 1 : '014 - Health and Long Term Care' , BPS Supplier : ' - , 0101 - Algonquin College of Applied Arts and Technology, 0102 - Cambrian College of Applied Arts and Technology, 0103 - Canadore College of Applied Arts and Technology, 0104 - Centennial College of Applied Arts and Technology, 0105 - Collège Boréal d'arts appliqués et de technologie		, 0106 - Conestoga College Institute of  Technology and Advanced Learning, 0107 - Confederation College of Applied Arts and Technology		, 0108 - Durham College of Applied Arts and Technology, 0109 - Fanshawe College of Applied Arts and Technology, 0110 - Sir Sandford Fleming College of Applied Arts and Technology		, 0111 - George Brown College of Applied Arts and Technology, 0112 - Georgian College of Applied Arts and Technology, 0113 - Humber College Institute of Technology and Advanced Learning, 0114 - Collège d'arts appliqués et de technologie La Cité collégiale		, 0115 - Lambton College of Applied Arts and Technology, 0116 - Loyalist College of Applied Arts and Technology, 0117 - Mohawk College of Applied Arts and Technology, 0118 - Niagara College of Applied Arts and Technology, 0119 - Northern College of Applied Arts and Technology, 0120 - Sault College of Applied Arts and Technology, 0121 - Seneca College of Applied Arts and Technology, 0122 - Sheridan College Institute of Technology and Advanced Learning, 0123 - St. Clair College of Applied Arts and Technology, 0124 - St. Lawrence College of Applied Arts and Technology, 0596 - Stevenson Memorial Hospital'

IFISER.GL_PERIOD
IFISER.ORGANIZATIONS
IFISER.AP_OUTSTANDING_INVOICE
  
*******************************************************************************/

-- Original
SELECT DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers'), O4560153.VENDOR_NAME, O100138.PERIOD_NAME, O4560153.BPS_ID, O4560153.INVOICE_DATE, O4560153.INVOICE_DESCRIPTION, O4560153.INVOICE_NUM, O4560153.MINISTRY_DESCRIPTION, O4560153.ORG_ID, O4560153.SUPPLIER_NUMBER, O4560153.VENDOR_NAME, ( O4560153.BPS_ID||' - '||O4560153.BPS_DESCRIPTION ), O3280365.ORG_SHORT_NAME, MAX(O100138.SORT_KEY), MAX(O3280365.ORG_ID), SUM(O4560153.INVOICE_AMOUNT), SUM(O4560153.OUTSTANDING_AMOUNT)
FROM IFISER.GL_PERIOD O100138, IFISER.ORGANIZATIONS O3280365, IFISER.AP_OUTSTANDING_INVOICE O4560153
WHERE ( ( O100138.PERIOD_NAME = O4560153.PERIOD_NAME ) AND ( O3280365.ORG_ID = O4560153.ORG_ID ) ) AND ( O100138.PERIOD_SET_NAME = 'OPS Fiscal' ) AND ( O100138.PERIOD_NAME_FILTER = :"Period Name" ) AND ( ( O4560153.BPS_ID||' - '||O4560153.BPS_DESCRIPTION ) = :"BPS Supplier" ) AND ( O3280365.ORG_SHORT_NAME = :"Sub-Ledger" ) AND ( O4560153.VENDOR_NAME = :"Supplier Name" ) AND ( O4560153.MINISTRY_DESCRIPTION = :"Ministry 1" )
GROUP BY DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers'), O4560153.VENDOR_NAME, O100138.PERIOD_NAME, O4560153.BPS_ID, O4560153.INVOICE_DATE, O4560153.INVOICE_DESCRIPTION, O4560153.INVOICE_NUM, O4560153.MINISTRY_DESCRIPTION, O4560153.ORG_ID, O4560153.SUPPLIER_NUMBER, O4560153.VENDOR_NAME, ( O4560153.BPS_ID||' - '||O4560153.BPS_DESCRIPTION ), O3280365.ORG_SHORT_NAME
ORDER BY DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers') ASC, O4560153.BPS_ID ASC, O4560153.VENDOR_NAME ASC, O4560153.VENDOR_NAME ASC, ( O4560153.BPS_ID||' - '||O4560153.BPS_DESCRIPTION ) ASC, O4560153.SUPPLIER_NUMBER ASC, O4560153.ORG_ID ASC, O4560153.INVOICE_NUM ASC, O4560153.INVOICE_DATE ASC, SUM(O4560153.INVOICE_AMOUNT) ASC
;

SELECT DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers'),
  O4560153.VENDOR_NAME,
  O100138.PERIOD_NAME,
  O4560153.BPS_ID,
  O4560153.INVOICE_DATE,
  O4560153.INVOICE_DESCRIPTION,
  O4560153.INVOICE_NUM,
  O4560153.MINISTRY_DESCRIPTION,
  O4560153.ORG_ID,
  O4560153.SUPPLIER_NUMBER,
  O4560153.VENDOR_NAME,
  ( O4560153.BPS_ID
  ||' - '
  ||O4560153.BPS_DESCRIPTION ),
  O3280365.ORG_SHORT_NAME,
  MAX(O100138.SORT_KEY),
  MAX(O3280365.ORG_ID),
  SUM(O4560153.INVOICE_AMOUNT),
  SUM(O4560153.OUTSTANDING_AMOUNT)
FROM IFISER.GL_PERIOD O100138,
  IFISER.ORGANIZATIONS O3280365,
  IFISER.AP_OUTSTANDING_INVOICE O4560153
WHERE ( ( O100138.PERIOD_NAME    = O4560153.PERIOD_NAME )
AND ( O3280365.ORG_ID            = O4560153.ORG_ID ) )
AND ( O100138.PERIOD_SET_NAME    = 'OPS Fiscal' )
AND ( O100138.PERIOD_NAME_FILTER = 'Aug-15' )
-- AND ( ( O4560153.BPS_ID
--  ||' - '
--  ||O4560153.BPS_DESCRIPTION )      = :"BPS Supplier" )
--AND ( O3280365.ORG_SHORT_NAME       = :"Sub-Ledger" )
--AND ( O4560153.VENDOR_NAME          = :"Supplier Name" )
AND ( O4560153.MINISTRY_DESCRIPTION = '030 - Training, Colleges and Universities' )
GROUP BY DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers'),
  O4560153.VENDOR_NAME,
  O100138.PERIOD_NAME,
  O4560153.BPS_ID,
  O4560153.INVOICE_DATE,
  O4560153.INVOICE_DESCRIPTION,
  O4560153.INVOICE_NUM,
  O4560153.MINISTRY_DESCRIPTION,
  O4560153.ORG_ID,
  O4560153.SUPPLIER_NUMBER,
  O4560153.VENDOR_NAME,
  ( O4560153.BPS_ID
  ||' - '
  ||O4560153.BPS_DESCRIPTION ),
  O3280365.ORG_SHORT_NAME
ORDER BY DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers') ASC,
  O4560153.BPS_ID ASC,
  O4560153.VENDOR_NAME ASC,
  O4560153.VENDOR_NAME ASC,
  ( O4560153.BPS_ID
  ||' - '
  ||O4560153.BPS_DESCRIPTION ) ASC,
  O4560153.SUPPLIER_NUMBER ASC,
  O4560153.ORG_ID ASC,
  O4560153.INVOICE_NUM ASC,
  O4560153.INVOICE_DATE ASC,
  SUM(O4560153.INVOICE_AMOUNT) ASC ;

SELECT DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers'),
  O100138.PERIOD_NAME,
  O4560153.MINISTRY_DESCRIPTION,
  O4560153.ORG_ID,
  O3280365.ORG_SHORT_NAME,
  MAX(O100138.SORT_KEY),
  MAX(O3280365.ORG_ID),
  SUM(O4560153.INVOICE_AMOUNT),
  SUM(O4560153.OUTSTANDING_AMOUNT)
FROM IFISER.GL_PERIOD O100138,
  IFISER.ORGANIZATIONS O3280365,
  IFISER.AP_OUTSTANDING_INVOICE O4560153
WHERE ( ( O100138.PERIOD_NAME    = O4560153.PERIOD_NAME )
AND ( O3280365.ORG_ID            = O4560153.ORG_ID ) )
AND ( O100138.PERIOD_SET_NAME    = 'OPS Fiscal' )
AND ( O100138.PERIOD_NAME_FILTER in ('Apr-15', 'May-15', 'Jun-15', 'Jul-15', 'Aug-15'))
-- AND ( ( O4560153.BPS_ID
--  ||' - '
--  ||O4560153.BPS_DESCRIPTION )      = :"BPS Supplier" )
--AND ( O3280365.ORG_SHORT_NAME       = :"Sub-Ledger" )
--AND ( O4560153.VENDOR_NAME          = :"Supplier Name" )
AND ( O4560153.MINISTRY_DESCRIPTION = '030 - Training, Colleges and Universities' )
GROUP BY DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers'),
  O100138.PERIOD_NAME,
  O4560153.MINISTRY_DESCRIPTION,
  O4560153.ORG_ID,
  O3280365.ORG_SHORT_NAME
order by O100138.PERIOD_NAME, DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers'), O4560153.ORG_ID;

SELECT DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers'),
  O4560153.VENDOR_NAME,
  O100138.PERIOD_NAME,
  O4560153.BPS_ID,
  O4560153.INVOICE_DATE,
  O4560153.INVOICE_DESCRIPTION,
  O4560153.INVOICE_NUM,
  O4560153.MINISTRY_DESCRIPTION,
  O4560153.ORG_ID,
  O4560153.SUPPLIER_NUMBER,
  O4560153.VENDOR_NAME,
  ( O4560153.BPS_ID
  ||' - '
  ||O4560153.BPS_DESCRIPTION ),
  O3280365.ORG_SHORT_NAME,
  MAX(O100138.SORT_KEY),
  MAX(O3280365.ORG_ID),
  SUM(O4560153.INVOICE_AMOUNT),
  SUM(O4560153.OUTSTANDING_AMOUNT)
FROM IFISER.GL_PERIOD O100138,
  IFISER.ORGANIZATIONS O3280365,
  IFISER.AP_OUTSTANDING_INVOICE O4560153
WHERE ( ( O100138.PERIOD_NAME    = O4560153.PERIOD_NAME )
AND ( O3280365.ORG_ID            = O4560153.ORG_ID ) )
AND ( O100138.PERIOD_SET_NAME    = 'OPS Fiscal' )
AND ( O100138.PERIOD_NAME_FILTER = :"Period Name" )
AND ( ( O4560153.BPS_ID
  ||' - '
  ||O4560153.BPS_DESCRIPTION )      = :"BPS Supplier" )
AND ( O3280365.ORG_SHORT_NAME       = :"Sub-Ledger" )
AND ( O4560153.VENDOR_NAME          = :"Supplier Name" )
AND ( O4560153.MINISTRY_DESCRIPTION = :"Ministry 1" )
GROUP BY DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers'),
  O4560153.VENDOR_NAME,
  O100138.PERIOD_NAME,
  O4560153.BPS_ID,
  O4560153.INVOICE_DATE,
  O4560153.INVOICE_DESCRIPTION,
  O4560153.INVOICE_NUM,
  O4560153.MINISTRY_DESCRIPTION,
  O4560153.ORG_ID,
  O4560153.SUPPLIER_NUMBER,
  O4560153.VENDOR_NAME,
  ( O4560153.BPS_ID
  ||' - '
  ||O4560153.BPS_DESCRIPTION ),
  O3280365.ORG_SHORT_NAME
ORDER BY DECODE(O4560153.BPS_ID,NULL,'NON-BPS  Suppliers','BPS Suppliers') ASC,
  O4560153.BPS_ID ASC,
  O4560153.VENDOR_NAME ASC,
  O4560153.VENDOR_NAME ASC,
  ( O4560153.BPS_ID
  ||' - '
  ||O4560153.BPS_DESCRIPTION ) ASC,
  O4560153.SUPPLIER_NUMBER ASC,
  O4560153.ORG_ID ASC,
  O4560153.INVOICE_NUM ASC,
  O4560153.INVOICE_DATE ASC,
  SUM(O4560153.INVOICE_AMOUNT) ASC ;

/*******************************************************************************
BPS Vendor ID Details by Period

Contains details of assets/liabilities, revenues/expenses on an accrual basis 
from all selected non-Sector Ministries for each BPS/Sector Ministry OGO.

BPS Reporting: OG Reports  BPS Vendor ID Details by Period  Ministry : '014' , Accrual Period : 'Mar-16' , Account Category : '10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 28, 29, 41, 42, 43, 44, 45, 46, 47, 48' , BPS Low : '0596' , BPS High : '0596'
*******************************************************************************/

-- Original
SELECT ( ( CONCAT(CONCAT(SUBSTR(O1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(O1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')) ) ), O100131.PERIOD_NAME, O100119.ACCOUNT_DESCRIPTION, O100131.ACCOUNT_ID, O100131.BUSINESS_UNIT_ID, O100121.COST_CENTRE_DESCRIPTION, O100131.COST_CENTRE_ID, O100131.INV_ITEM_DESC, O100131.INITIATIVE_ID, O100106.INVOICE_DATE, O100131.INVOICE_NUM, O100131.JE_CATEGORY_NAME, O100131.JE_SOURCE_NAME, O100131.MINISTRY_ID, O100122.PROGRAM_DESCRIPTION, O100131.PROGRAM_ID, ( DECODE(O100131.STATUS,'P','POSTED','NOT POSTED') ), ( SUBSTR(O100119.ACCOUNT_ID,1,2) ), ( O100169.VENDOR_NAME||' - '||O100169.SUPPLIER_NUMBER ), O100169.BPS_ID, SUM(O100131.AMOUNT), SUM(0)
FROM IFISER.AP_INVOICE O100106, IFISER.FLAT_ACCOUNT_HIERARCHY O100119, IFISER.FLAT_COST_CENTRE_HIERARCHY O100121, IFISER.FLAT_PROGRAM_HIERARCHY O100122, IFISER.GL_JE_ACTUALS_DETAILS O100131, IFISER.VENDOR O100169, IFISER.FLAT_COST_CENTRE_TP_ALL_HIER O1143355, IFISER.FLAT_BOG_BPS_HIERARCHY O3521092
WHERE ( ( O100119.ACCOUNT_ID = O100131.ACCOUNT_ID ) AND ( O100121.COST_CENTRE_ID = O100131.COST_CENTRE_ID ) AND ( O100169.VENDOR_ID(+) = O100131.VENDOR_ID ) AND ( O100122.PROGRAM_ID = O100131.PROGRAM_ID ) AND ( O100131.INVOICE_DISTRIBUTION_ID = O100106.INVOICE_DISTRIBUTION_ID(+) ) AND ( O1143355.COST_CENTRE_ID = O100131.COST_CENTRE_ID ) AND ( O3521092.BPS_ID = O100169.BPS_ID ) ) AND ( O100169.BPS_ID(+) BETWEEN :"BPS Low" AND :"BPS High" ) AND ( O100169.BPS_ID IN (( O3521092.BPS_ID )) ) AND ( O100131.AMOUNT <> 0 ) AND ( ( SUBSTR(O100119.ACCOUNT_ID,1,2) ) = :"Account Category" ) AND ( O100131.PERIOD_NAME = :"Accrual Period" ) AND ( O100131.MINISTRY_ID = :"Ministry" )
GROUP BY ( ( CONCAT(CONCAT(SUBSTR(O1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(O1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')) ) ), O100131.PERIOD_NAME, O100119.ACCOUNT_DESCRIPTION, O100131.ACCOUNT_ID, O100131.BUSINESS_UNIT_ID, O100121.COST_CENTRE_DESCRIPTION, O100131.COST_CENTRE_ID, O100131.INV_ITEM_DESC, O100131.INITIATIVE_ID, O100106.INVOICE_DATE, O100131.INVOICE_NUM, O100131.JE_CATEGORY_NAME, O100131.JE_SOURCE_NAME, O100131.MINISTRY_ID, O100122.PROGRAM_DESCRIPTION, O100131.PROGRAM_ID, ( DECODE(O100131.STATUS,'P','POSTED','NOT POSTED') ), ( SUBSTR(O100119.ACCOUNT_ID,1,2) ), ( O100169.VENDOR_NAME||' - '||O100169.SUPPLIER_NUMBER ), O100169.BPS_ID
HAVING ( ( SUM(O100131.AMOUNT) ) <> 0 )
ORDER BY O100169.BPS_ID ASC, O100131.MINISTRY_ID ASC, ( O100169.VENDOR_NAME||' - '||O100169.SUPPLIER_NUMBER ) ASC, ( SUBSTR(O100119.ACCOUNT_ID,1,2) ) ASC, SUM(0) ASC
;

SELECT ( ( CONCAT(CONCAT(SUBSTR(O1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(O1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')) ) ),
  O100131.PERIOD_NAME,
  O100119.ACCOUNT_DESCRIPTION,
  O100131.ACCOUNT_ID,
  O100131.BUSINESS_UNIT_ID,
  O100121.COST_CENTRE_DESCRIPTION,
  O100131.COST_CENTRE_ID,
  O100131.INV_ITEM_DESC,
  O100131.INITIATIVE_ID,
  O100106.INVOICE_DATE,
  O100131.INVOICE_NUM,
  O100131.JE_CATEGORY_NAME,
  O100131.JE_SOURCE_NAME,
  O100131.MINISTRY_ID,
  O100122.PROGRAM_DESCRIPTION,
  O100131.PROGRAM_ID,
  ( DECODE(O100131.STATUS,'P','POSTED','NOT POSTED') ),
  ( SUBSTR(O100119.ACCOUNT_ID,1,2) ),
  ( O100169.VENDOR_NAME
  ||' - '
  ||O100169.SUPPLIER_NUMBER ),
  O100169.BPS_ID,
  SUM(O100131.AMOUNT),
  SUM(0)
FROM IFISER.AP_INVOICE O100106,
  IFISER.FLAT_ACCOUNT_HIERARCHY O100119,
  IFISER.FLAT_COST_CENTRE_HIERARCHY O100121,
  IFISER.FLAT_PROGRAM_HIERARCHY O100122,
  IFISER.GL_JE_ACTUALS_DETAILS O100131,
  IFISER.VENDOR O100169,
  IFISER.FLAT_COST_CENTRE_TP_ALL_HIER O1143355,
  IFISER.FLAT_BOG_BPS_HIERARCHY O3521092
WHERE ( ( O100119.ACCOUNT_ID          = O100131.ACCOUNT_ID )
AND ( O100121.COST_CENTRE_ID          = O100131.COST_CENTRE_ID )
AND ( O100169.VENDOR_ID(+)            = O100131.VENDOR_ID )
AND ( O100122.PROGRAM_ID              = O100131.PROGRAM_ID )
AND ( O100131.INVOICE_DISTRIBUTION_ID = O100106.INVOICE_DISTRIBUTION_ID(+) )
AND ( O1143355.COST_CENTRE_ID         = O100131.COST_CENTRE_ID )
AND ( O3521092.BPS_ID                 = O100169.BPS_ID ) )
AND ( O100169.BPS_ID(+) BETWEEN '0000' AND 'ZZZZ' )
AND ( O100169.BPS_ID                    IN (( O3521092.BPS_ID )) )
AND ( O100131.AMOUNT                    <> 0 )
AND ( ( SUBSTR(O100119.ACCOUNT_ID,1,2) ) in ('10', '11', '12', '13', '14', '16', '17', '18', '19', '20', '21', '22', '23', '24', '26', '28', '29', '41', '42', '43', '44', '45', '46', '47', '48', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69') )
AND ( O100131.PERIOD_NAME                = 'Apr-15' )
AND ( O100131.MINISTRY_ID                = '030' )
GROUP BY ( ( CONCAT(CONCAT(SUBSTR(O1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(O1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')) ) ),
  O100131.PERIOD_NAME,
  O100119.ACCOUNT_DESCRIPTION,
  O100131.ACCOUNT_ID,
  O100131.BUSINESS_UNIT_ID,
  O100121.COST_CENTRE_DESCRIPTION,
  O100131.COST_CENTRE_ID,
  O100131.INV_ITEM_DESC,
  O100131.INITIATIVE_ID,
  O100106.INVOICE_DATE,
  O100131.INVOICE_NUM,
  O100131.JE_CATEGORY_NAME,
  O100131.JE_SOURCE_NAME,
  O100131.MINISTRY_ID,
  O100122.PROGRAM_DESCRIPTION,
  O100131.PROGRAM_ID,
  ( DECODE(O100131.STATUS,'P','POSTED','NOT POSTED') ),
  ( SUBSTR(O100119.ACCOUNT_ID,1,2) ),
  ( O100169.VENDOR_NAME
  ||' - '
  ||O100169.SUPPLIER_NUMBER ),
  O100169.BPS_ID
HAVING ( ( SUM(O100131.AMOUNT) ) <> 0 )
ORDER BY O100169.BPS_ID ASC,
  O100131.MINISTRY_ID ASC,
  ( O100169.VENDOR_NAME
  ||' - '
  ||O100169.SUPPLIER_NUMBER ) ASC,
  ( SUBSTR(O100119.ACCOUNT_ID,1,2) ) ASC,
  SUM(0) ASC ;
  
/*******************************************************************************
BPS Vendor ID Cash Payments

Provides accounting details and cash payment information from all selected 
Non-Sector Ministries for each BPS/Sector Ministry OGO.  The report is on a 
cash basis.

BPS Reporting: OG Reports  BPS Vendor ID Cash Payments  ParentCC_Level 2 : '0, 1, 2, 3, 4, 5, 6, 7' , CashDetlParentCC 2 : '(6) 001014 - MOHLTC Org Roll-up Parent' , CashDetlVerName 2 : 'ALL ACCOUNTS' , CashDetlPeriodYear 2 : '2016' , GRE Low : '0596' , GRE High 2 : '0596' , Beginning payment date : '01-MAR-2016' , Ending payment date : '31-MAR-2016'
*******************************************************************************/
-- Original Query
SELECT  ((CONCAT(CONCAT(SUBSTR(o1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(o1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')))) as C_2,SUBSTR(o100169.BPS_ID,1,4) as C_1,o100119.ACCOUNT_DESCRIPTION as E100357,o100121.COST_CENTRE_DESCRIPTION as E101380,o100169.SUPPLIER_NUMBER as E103884,o100169.VENDOR_NAME as E104148,o2167250.ACCOUNT_ID as E2167282,o2167250.BUSINESS_UNIT_ID as E2167291,o2167250.CHECK_NUMBER as E2167295,o2167250.COST_CENTRE_ID as E2167298,o2167250.INITIATIVE_ID as E2167318,o2167250.INVOICE_NUMBER as E2167335,o2167250.MINISTRY_ID as E2167352,o2167250.PAID_DISTRIBUTION_AMOUNT as E2167356,o2167250.PAYMENT_AMOUNT as E2167358,o2167250.PAYMENT_DATE as E2167360,o2167250.PAYMENT_PERIOD_NAME as E2167364,o2167250.PAYMENT_PERIOD_YEAR as E2167366,o2167250.PERIOD_NAME as E2167375,o2167250.PROGRAM_ID as E2167385,o2167250.SOURCE as E2167388,o2167252.VENDOR_TYPE as E2167413,o2167254.VERSION_NAME as E2167419,o2167250.ITEM_DESCRIPTION as E2672041,o100169.BPS_ID as E3593838,as115789_2167364_OLD as as115789_2167364_OLD
 FROM IFISER.FLAT_ACCOUNT_HIERARCHY o100119,
      IFISER.FLAT_COST_CENTRE_HIERARCHY o100121,
      PARENT_COST_CENTRE o100144,
      IFISER.VENDOR o100169,
      IFISER.FLAT_COST_CENTRE_TP_ALL_HIER o1143355,
      AP_INVOICE_PAYMENT_DETAILS o2167250,
      IFISER.V3_INVOICE_VENDOR_MAP o2167251,
      IFISER.V3_VENDOR o2167252,
      IFISER.V3_VERSION_ACCT_MAP o2167254,
     ( SELECT o100138.PERIOD_NAME AS as115789_2167364_OLD_2, MAX(o100138.SORT_KEY) AS as115789_2167364_OLD FROM IFISER.GL_PERIOD o100138  WHERE (o100138.PERIOD_SET_NAME = 'OPS Fiscal') GROUP BY o100138.PERIOD_NAME)
 WHERE ( (o100144.COST_CENTRE_ID = o2167250.COST_CENTRE_ID)
   and (o2167251.INVOICE_DISTRIBUTION_ID = o2167250.INVOICE_DISTRIBUTION_ID)
   and (o2167252.V3_VENDOR_ID = o2167251.V3_VENDOR_ID)
   and (o2167254.ACCOUNT_ID = o2167250.ACCOUNT_ID)
   and (o100121.COST_CENTRE_ID = o2167250.COST_CENTRE_ID)
   and (o100169.VENDOR_ID = o2167250.VENDOR_ID)
   and (o100119.ACCOUNT_ID = o2167250.ACCOUNT_ID)
   and (o1143355.COST_CENTRE_ID = o2167250.COST_CENTRE_ID)
   and (o2167250.PAYMENT_PERIOD_NAME = as115789_2167364_OLD_2(+)))
   AND (o2167250.PAYMENT_DATE >= :"Beginning payment date" AND o2167250.PAYMENT_DATE <= :"Ending payment date")
   AND ((SUBSTR(o100119.ACCOUNT_ID,1,2)) = :"Acccount Category")
   AND (( SUBSTR(o100169.BPS_ID,1,4) ) >= :"GRE Low" AND ( SUBSTR(o100169.BPS_ID,1,4) ) <= :"GRE High 2")
   AND (o100169.BPS_ID IS NOT NULL )
   AND (o100144.COST_CENTRE_LEVEL = :"ParentCC_Level 2")
   AND (o2167250.PAYMENT_PERIOD_YEAR = :"CashDetlPeriodYear 2")
   AND ((o2167254.VERSION_NAME) = :"CashDetlVerName 2")
   AND ((REPLACE(REPLACE((o2167252.V3_VENDOR_NAME||' - '||o2167252.V3_VENDOR_ID),',',' '),'&','and')) = :"CashDetlVenNameIdParam 2")
   AND (o100144.COST_CENTRE_ID_DESC_LEVEL = :"CashDetlParentCC 2")
   AND (o2167250.POSTED_FLAG = 'Y')
   AND (o2167250.INVOICE_TYPE_LOOKUP_CODE <> 'AWT')
 ORDER BY o100169.BPS_ID ASC , o100169.VENDOR_NAME ASC , as115789_2167364_OLD ASC , o2167250.PAYMENT_AMOUNT ASC , o2167250.SOURCE ASC , SUBSTR(o100169.BPS_ID,1,4) ASC ;


SELECT ((CONCAT(CONCAT(SUBSTR(o1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(o1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')))) AS C_2,
  SUBSTR(o100169.BPS_ID,1,4)                                                                                                                   AS C_1,
  o100119.ACCOUNT_DESCRIPTION                                                                                                                  AS E100357,
  o100121.COST_CENTRE_DESCRIPTION                                                                                                              AS E101380,
  o100169.SUPPLIER_NUMBER                                                                                                                      AS E103884,
  o100169.VENDOR_NAME                                                                                                                          AS E104148,
  o2167250.ACCOUNT_ID                                                                                                                          AS E2167282,
  o2167250.BUSINESS_UNIT_ID                                                                                                                    AS E2167291,
  o2167250.CHECK_NUMBER                                                                                                                        AS E2167295,
  o2167250.COST_CENTRE_ID                                                                                                                      AS E2167298,
  o2167250.INITIATIVE_ID                                                                                                                       AS E2167318,
  o2167250.INVOICE_NUMBER                                                                                                                      AS E2167335,
  o2167250.MINISTRY_ID                                                                                                                         AS E2167352,
  o2167250.PAID_DISTRIBUTION_AMOUNT                                                                                                            AS E2167356,
  o2167250.PAYMENT_AMOUNT                                                                                                                      AS E2167358,
  o2167250.PAYMENT_DATE                                                                                                                        AS E2167360,
  o2167250.PAYMENT_PERIOD_NAME                                                                                                                 AS E2167364,
  o2167250.PAYMENT_PERIOD_YEAR                                                                                                                 AS E2167366,
  o2167250.PERIOD_NAME                                                                                                                         AS E2167375,
  o2167250.PROGRAM_ID                                                                                                                          AS E2167385,
  o2167250.SOURCE                                                                                                                              AS E2167388,
  o2167252.VENDOR_TYPE                                                                                                                         AS E2167413,
  o2167254.VERSION_NAME                                                                                                                        AS E2167419,
  o2167250.ITEM_DESCRIPTION                                                                                                                    AS E2672041,
  o100169.BPS_ID                                                                                                                               AS E3593838,
  as115789_2167364_OLD                                                                                                                         AS as115789_2167364_OLD
FROM IFISER.FLAT_ACCOUNT_HIERARCHY o100119,
  IFISER.FLAT_COST_CENTRE_HIERARCHY o100121,
  PARENT_COST_CENTRE o100144,
  IFISER.VENDOR o100169,
  IFISER.FLAT_COST_CENTRE_TP_ALL_HIER o1143355,
  AP_INVOICE_PAYMENT_DETAILS o2167250,
  IFISER.V3_INVOICE_VENDOR_MAP o2167251,
  IFISER.V3_VENDOR o2167252,
  IFISER.V3_VERSION_ACCT_MAP o2167254,
  (SELECT o100138.PERIOD_NAME AS as115789_2167364_OLD_2,
    MAX(o100138.SORT_KEY)     AS as115789_2167364_OLD
  FROM IFISER.GL_PERIOD o100138
  WHERE (o100138.PERIOD_SET_NAME = 'OPS Fiscal')
  GROUP BY o100138.PERIOD_NAME
  )
WHERE ( (o100144.COST_CENTRE_ID       = o2167250.COST_CENTRE_ID)
AND (o2167251.INVOICE_DISTRIBUTION_ID = o2167250.INVOICE_DISTRIBUTION_ID)
AND (o2167252.V3_VENDOR_ID            = o2167251.V3_VENDOR_ID)
AND (o2167254.ACCOUNT_ID              = o2167250.ACCOUNT_ID)
AND (o100121.COST_CENTRE_ID           = o2167250.COST_CENTRE_ID)
AND (o100169.VENDOR_ID                = o2167250.VENDOR_ID)
AND (o100119.ACCOUNT_ID               = o2167250.ACCOUNT_ID)
AND (o1143355.COST_CENTRE_ID          = o2167250.COST_CENTRE_ID)
AND (o2167250.PAYMENT_PERIOD_NAME     = as115789_2167364_OLD_2(+)))
AND (o2167250.PAYMENT_DATE           >= '01-APR-2015'
AND o2167250.PAYMENT_DATE            <= '31-MAR-2016')
-- AND ((SUBSTR(o100119.ACCOUNT_ID,1,2)) = :"Acccount Category")
AND (( SUBSTR(o100169.BPS_ID,1,4) )  >= '0000'
AND ( SUBSTR(o100169.BPS_ID,1,4) )   <= 'ZZZZ')
AND (o100169.BPS_ID                  IS NOT NULL )
AND (o100144.COST_CENTRE_LEVEL        = '6')
AND (o2167250.PAYMENT_PERIOD_YEAR     = '2016')
AND ((o2167254.VERSION_NAME)          = 'ALL ACCOUNTS')
-- AND ((REPLACE(REPLACE((o2167252.V3_VENDOR_NAME
--  ||' - '
--  ||o2167252.V3_VENDOR_ID),',',' '),'&','and')) = :"CashDetlVenNameIdParam 2")
AND (o100144.COST_CENTRE_ID_DESC_LEVEL          = '(6) 001030 - MTCU Org Roll-up Parent')
AND (o2167250.POSTED_FLAG                       = 'Y')
AND (o2167250.INVOICE_TYPE_LOOKUP_CODE         <> 'AWT')
ORDER BY o100169.BPS_ID ASC ,
  o100169.VENDOR_NAME ASC ,
  as115789_2167364_OLD ASC ,
  o2167250.PAYMENT_AMOUNT ASC ,
  o2167250.SOURCE ASC ,
  SUBSTR(o100169.BPS_ID,1,4) ASC ;

-- BPS Reporting: OG Reports  BPS Vendor ID Cash Payments  ParentCC_Level 2 : '6' , CashDetlParentCC 2 : '(6) 001030 - MTCU Org Roll-up Parent' , CashDetlVerName 2 : 'ALL ACCOUNTS' , CashDetlPeriodYear 2 : '2016' , GRE Low :  , GRE High 2 : 'ZZZZ' , Beginning payment date :  , Ending payment date : 

/*******************************************************************************
Suppliers with Financial Activity - Possible BPS or OGO

Enables Users to identify suppliers that need to be mapped as BPS Suppliers
*******************************************************************************/
-- Original

SELECT ( CONCAT(CONCAT(SUBSTR(O1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(O1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')) ), O100131.MINISTRY_ID, O100131.POSTED_FLAG, O100169.SUPPLIER_NUMBER, O100169.VENDOR_NAME, ( SUBSTR(O100119.ACCOUNT_ID,1,2) ), O100131.PERIOD_YEAR, O100169.BPS_ID, SUM(O100131.AMOUNT), SUM(0)
FROM IFISER.FLAT_ACCOUNT_HIERARCHY O100119, IFISER.GL_JE_ACTUALS_DETAILS O100131, IFISER.VENDOR O100169, IFISER.FLAT_COST_CENTRE_TP_ALL_HIER O1143355
WHERE ( ( O100119.ACCOUNT_ID = O100131.ACCOUNT_ID ) AND ( O100169.VENDOR_ID = O100131.VENDOR_ID ) AND ( O1143355.COST_CENTRE_ID = O100131.COST_CENTRE_ID ) ) AND ( O100169.VENDOR_NAME IN (( :"Supplier name select" )) ) AND ( O100169.BPS_ID IS NULL  ) AND ( O100131.MINISTRY_ID = :"Ministry Number" ) AND ( ( SUBSTR(O100119.ACCOUNT_ID,1,2) ) = :"Account Category 1" ) AND ( O100131.POSTED_FLAG = 'Y' ) AND ( O100131.PERIOD_YEAR = :"Fiscal Year" )
GROUP BY ( CONCAT(CONCAT(SUBSTR(O1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(O1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')) ), O100131.MINISTRY_ID, O100131.POSTED_FLAG, O100169.SUPPLIER_NUMBER, O100169.VENDOR_NAME, ( SUBSTR(O100119.ACCOUNT_ID,1,2) ), O100131.PERIOD_YEAR, O100169.BPS_ID
ORDER BY O100169.VENDOR_NAME ASC, SUM(0) ASC
;

SELECT ( CONCAT(CONCAT(SUBSTR(O1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(O1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')) ),
  O100131.MINISTRY_ID,
  O100131.POSTED_FLAG,
  O100169.SUPPLIER_NUMBER,
  O100169.VENDOR_NAME,
  ( SUBSTR(O100119.ACCOUNT_ID,1,2) ),
  O100131.PERIOD_YEAR,
  O100169.BPS_ID,
  SUM(O100131.AMOUNT),
  SUM(0)
FROM IFISER.FLAT_ACCOUNT_HIERARCHY O100119,
  IFISER.GL_JE_ACTUALS_DETAILS O100131,
  IFISER.VENDOR O100169,
  IFISER.FLAT_COST_CENTRE_TP_ALL_HIER O1143355
WHERE ( ( O100119.ACCOUNT_ID             = O100131.ACCOUNT_ID )
AND ( O100169.VENDOR_ID                  = O100131.VENDOR_ID )
AND ( O1143355.COST_CENTRE_ID            = O100131.COST_CENTRE_ID ) )
--AND ( O100169.VENDOR_NAME               IN (( :"Supplier name select" )) )
AND ( O100169.BPS_ID                    IS NULL )
AND ( O100131.MINISTRY_ID                = '030' )
--AND ( ( SUBSTR(O100119.ACCOUNT_ID,1,2) ) = :"Account Category 1" )
AND ( O100131.POSTED_FLAG                = 'Y' )
AND ( O100131.PERIOD_YEAR                = '2016' )
GROUP BY ( CONCAT(CONCAT(SUBSTR(O1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(O1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')) ),
  O100131.MINISTRY_ID,
  O100131.POSTED_FLAG,
  O100169.SUPPLIER_NUMBER,
  O100169.VENDOR_NAME,
  ( SUBSTR(O100119.ACCOUNT_ID,1,2) ),
  O100131.PERIOD_YEAR,
  O100169.BPS_ID
ORDER BY O100169.VENDOR_NAME ASC,
  SUM(0) ASC ;

/*******************************************************************************
Supplier & JE summary by period

BPS Reporting: OG Reports  Supplier & Journal Summary by Period  Ministry : '014' , Accrual Period : 'Mar-16' , Account Category : '10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 28, 29, 41, 42, 43, 44, 45, 46, 47, 48'
*******************************************************************************/

--Original
SELECT  ((CONCAT(CONCAT(SUBSTR(o1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(o1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')))) as C_2,o100131.JE_CATEGORY_NAME as E102603,o100131.JE_SOURCE_NAME as E102619,o100131.MINISTRY_ID as E102866,o100131.PERIOD_NAME as E103163,(DECODE(o100131.STATUS,'P','POSTED','NOT POSTED')) as E106402,(SUBSTR(o100119.ACCOUNT_ID,1,2)) as E159634,(o100169.VENDOR_NAME||' - '||o100169.SUPPLIER_NUMBER) as E1599718,o100169.BPS_ID as E3593838,as115789_103163_OLD as as115789_103163_OLD,SUM(o100131.AMOUNT) as E100477_SUM,SUM(0) as C_1
 FROM IFISER.FLAT_ACCOUNT_HIERARCHY o100119,
      IFISER.GL_JE_ACTUALS_DETAILS o100131,
      IFISER.VENDOR o100169,
      IFISER.FLAT_COST_CENTRE_TP_ALL_HIER o1143355,
     ( SELECT o100138.PERIOD_NAME AS as115789_103163_OLD_2, MAX(o100138.SORT_KEY) AS as115789_103163_OLD FROM IFISER.GL_PERIOD o100138  WHERE (o100138.PERIOD_SET_NAME = 'OPS Fiscal') GROUP BY o100138.PERIOD_NAME)
 WHERE ( (o100119.ACCOUNT_ID = o100131.ACCOUNT_ID)
   and (o100169.VENDOR_ID(+) = o100131.VENDOR_ID)
   and (o1143355.COST_CENTRE_ID = o100131.COST_CENTRE_ID)
   and (o100131.PERIOD_NAME = as115789_103163_OLD_2(+)))
   AND (o100131.AMOUNT <> 0)
   AND ((SUBSTR(o100119.ACCOUNT_ID,1,2)) = :"Account Category")
   AND (o100131.PERIOD_NAME = :"Accrual Period")
   AND (o100131.MINISTRY_ID = :"Ministry")
 GROUP BY as115789_103163_OLD,((CONCAT(CONCAT(SUBSTR(o1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(o1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')))),o100131.JE_CATEGORY_NAME,o100131.JE_SOURCE_NAME,o100131.MINISTRY_ID,o100131.PERIOD_NAME,(DECODE(o100131.STATUS,'P','POSTED','NOT POSTED')),(SUBSTR(o100119.ACCOUNT_ID,1,2)),(o100169.VENDOR_NAME||' - '||o100169.SUPPLIER_NUMBER),o100169.BPS_ID
 ORDER BY o100169.BPS_ID ASC , (o100169.VENDOR_NAME||' - '||o100169.SUPPLIER_NUMBER) ASC , SUM(0) ASC , (SUBSTR(o100119.ACCOUNT_ID,1,2)) ASC ;


/*******************************************************************************
BPS Vendor ID Summary by Period

BPS Reporting: OG Reports  BPS Vendor ID Summary by Period  Ministry : '014' , Accrual Period : 'Mar-16' , Account Category : '10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 28, 29, 41, 42, 43, 44, 45, 46, 47, 48'
*******************************************************************************/

-- Original
SELECT  ((CONCAT(CONCAT(SUBSTR(o1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(o1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')))) as C_2,o100131.JE_CATEGORY_NAME as E102603,o100131.JE_SOURCE_NAME as E102619,o100131.MINISTRY_ID as E102866,o100131.PERIOD_NAME as E103163,(DECODE(o100131.STATUS,'P','POSTED','NOT POSTED')) as E106402,(SUBSTR(o100119.ACCOUNT_ID,1,2)) as E159634,(o100169.VENDOR_NAME||' - '||o100169.SUPPLIER_NUMBER) as E1599718,o100169.BPS_ID as E3593838,as115789_103163_OLD as as115789_103163_OLD,SUM(o100131.AMOUNT) as E100477_SUM,SUM(0) as C_1
 FROM IFISER.FLAT_ACCOUNT_HIERARCHY o100119,
      IFISER.GL_JE_ACTUALS_DETAILS o100131,
      IFISER.VENDOR o100169,
      IFISER.FLAT_COST_CENTRE_TP_ALL_HIER o1143355,
      IFISER.FLAT_BOG_BPS_HIERARCHY o3521092,
     ( SELECT o100138.PERIOD_NAME AS as115789_103163_OLD_2, MAX(o100138.SORT_KEY) AS as115789_103163_OLD FROM IFISER.GL_PERIOD o100138  WHERE (o100138.PERIOD_SET_NAME = 'OPS Fiscal') GROUP BY o100138.PERIOD_NAME)
 WHERE ( (o100119.ACCOUNT_ID = o100131.ACCOUNT_ID)
   and (o100169.VENDOR_ID(+) = o100131.VENDOR_ID)
   and (o1143355.COST_CENTRE_ID = o100131.COST_CENTRE_ID)
   and (o3521092.BPS_ID = o100169.BPS_ID)
   and (o100131.PERIOD_NAME = as115789_103163_OLD_2(+)))
   AND (o100169.BPS_ID IN (o3521092.BPS_ID))
   AND (o100131.AMOUNT <> 0)
   AND ((SUBSTR(o100119.ACCOUNT_ID,1,2)) = :"Account Category")
   AND (o100131.PERIOD_NAME = :"Accrual Period")
   AND (o100131.MINISTRY_ID = :"Ministry")
 GROUP BY as115789_103163_OLD,((CONCAT(CONCAT(SUBSTR(o1143355.COST_CENTRE_ID_L1,1,6),' - '),REPLACE(REPLACE(o1143355.COST_CENTRE_DESCRIPTION_L1,',',''),'&','and')))),o100131.JE_CATEGORY_NAME,o100131.JE_SOURCE_NAME,o100131.MINISTRY_ID,o100131.PERIOD_NAME,(DECODE(o100131.STATUS,'P','POSTED','NOT POSTED')),(SUBSTR(o100119.ACCOUNT_ID,1,2)),(o100169.VENDOR_NAME||' - '||o100169.SUPPLIER_NUMBER),o100169.BPS_ID
 ORDER BY o100169.BPS_ID ASC , (o100169.VENDOR_NAME||' - '||o100169.SUPPLIER_NUMBER) ASC , (SUBSTR(o100119.ACCOUNT_ID,1,2)) ASC , SUM(0) ASC ;


/*******************************************************************************
Table of BPS entities in OG

Lists all BPS/OGO entities currently mapped. Flagged in OG

BPS Reporting: OG Reports  Table of BPS entities in OG
*******************************************************************************/
-- Original
SELECT DECODE(O3521092.DISABLED_DATE,NULL,' ',O3521092.DISABLED_DATE), DECODE(O3521092.END_DATE,NULL,' ',O3521092.END_DATE), DECODE(O100169.END_DATE_ACTIVE,NULL,' ',O100169.END_DATE_ACTIVE), O100169.SUPPLIER_NUMBER, O100169.VENDOR_NAME, O3521092.BPS_PARENT_DESC_L2, O100169.BPS_ID, O3521092.START_DATE, O100169.START_DATE_ACTIVE
FROM IFISER.VENDOR O100169, IFISER.FLAT_BOG_BPS_HIERARCHY O3521092
WHERE ( ( O3521092.BPS_ID = O100169.BPS_ID ) ) AND ( UPPER(O100169.BPS_ID) <> UPPER(' ') )
ORDER BY O3521092.BPS_PARENT_DESC_L2 ASC, O100169.VENDOR_NAME ASC
;
