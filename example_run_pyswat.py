import pyswat as ps

model = ps.connect(r"C:\Users\David\Desktop\Barigui_swales\Scenarios\Default\TxtInOut")

#model.run(swat_version='670_rel_64')
model.resultFile_toSQL(output="swat_db.sqlite", fetch_tables=['mgt'])
#model.resultFile_toSQL(output="swat_db.sqlite", fetch_tables=['rch'])
#model.resultFile_toSQL(output="swat_db.sqlite", fetch_tables=['sub','hru','rch'])

# sql = """
# SELECT * FROM hru 
# WHERE SUB = 39
# AND MO = 1
# AND YR = 2010
# AND DA = 3
# """

# result = model.getModelQuery(file="swat_db.sqlite", query=sql, pandas_output=True)

# model.changePar(parameter = 'CN2', method = 'relative', value = -0.083233, sb=1)#1
# model.changePar(parameter = 'CN2', method = 'relative', value = -0.083233, sb=list(range(1,40)),log = 'D:\log.txt')
# table, original_table = model.getParHru()
# print(table)
# print(original_table)





