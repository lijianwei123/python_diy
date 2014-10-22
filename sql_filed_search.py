#encoding: utf8
'''
数据库字段搜索  暂时只支持windows
Created on 2013-5-10

@author: Administrator
'''

#http://code.google.com/p/pyodbc/
import pyodbc
import sys


dbms_type = 'mysql'
host = "localhost"
user = "root"
pwd = "root"
database = "jingnian"

#===============================================================================
# dbms_type = 'mssql'
# host = '168.192.122.27,143'
# database = 'jdrc'
# user = 'sa'
# pwd = 'sa'
#===============================================================================


search_field = 'seq'

if dbms_type == 'mssql':
    #需要安装mssql odbc: http://www.microsoft.com/zh-cn/download/details.aspx?id=36434
    #其他不需要安装
    conn_info = 'DRIVER={SQL Server Native Client 10.0};DATABASE=%s;SERVER=%s;UID=%s;PWD=%s'%(database, host, user, pwd)
elif dbms_type == 'mysql':
    #需要安装mysql odbc：http://dev.mysql.com/downloads/connector/odbc/
    #其他不需要安装
    conn_info = ('Driver={MySQL ODBC 5.2 Unicode Driver};Server=%s;Port=%s;Database=%s;User=%s; Password=%s;'%(host, 3306, database, user, pwd ))

#连接数据库    
try:
    conn = pyodbc.connect(conn_info)
except pyodbc.Error, e:
    print e
    sys.exit(1)

#游标
cursor = conn.cursor()


def fieldSearch():
    search_result = {}
    
    for key in tbl_fields:
        search_result[key] = filter(None, [findField(search_field, field) for field in tbl_fields[key]])
        
    
        
    for key in search_result.keys():
        if len(search_result[key]) == 0:
            del search_result[key]
        
    print search_result

def findField(search_field, field):
    if field.find(search_field) != -1:
        return field

#字段
tbl_fields = {}

if dbms_type == 'mysql':
    cursor.execute("show tables")
    
    tables = cursor.fetchall()
    
    for tbl_name, in tables:
        sql = "show columns from `" + tbl_name + "`"
        
        cursor.execute(sql)
        fields = cursor.fetchall()
        
        tbl_fields[tbl_name] = [field[0] for field in fields]
        
    #搜索字段
    fieldSearch()
        
elif dbms_type == 'mssql':
    tables = []
    for row in cursor.tables():
        tables.append(row.table_name)
    
    for tbl_name in tables:
        tbl_fields[tbl_name] = [row.column_name for row in cursor.columns(table = tbl_name)]    
    
    #搜索字段
    fieldSearch()
    
#关闭资源
cursor.close()
conn.close()