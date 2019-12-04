# PySWAT is a Command Line Interface(CLI) for Input/Output manipulation and analysis of the Soil and Water Assessment Tool(SWAT). 

PySWAT Couples SWAT to the Power of Python Language to connect SWAT 
Input/Output Data to Powerful Python Libraries such as SQLite, Pandas,
Numpy and MatplotLib

Features can be used to assess output data, generate 
graphs, perform custom queries and much more!

# QuickStart

## 1. Get Anaconda at [Anaconda's Website](https://www.anaconda.com/distribution/#download-secion)
*If you are not a first timer with python, use the way you know best! You need matplotlib, pandas, numpy and SQlite, which are covered by anaconda.

## 2. Open Spyder, Anaconda's IDE

#Connect your Project to pySWAT
## 3. Create a "myAnalysis.py" file on the same folder as pySWAT 

myanalysis.py
```python
import pySWAT 
model = pySWAT.connect(r"C:\Users\David\Desktop\Barigui_swales\Scenarios\Calibrated\TxtInOut")

#2.Get a Parameter report on HRUs and/or Subbasins and Watershed Parameters

model.changepar(parameter='CN2', method='relative', value='-0.15',sb = 'all', lulc = 'all', hru = None, log= r'log_changepar.txt')

#2.Change parameters in SWAT in the same way you do it on SWAT-CUP and ArcSWAT
model.changepar(parameter='CN2', method='relative', value='-0.15',sb = 'all' , lulc = 'all', hru = None, log= r'log_changepar.txt')

#3.Get a run of your model inside a Python Terminal using your Favorite SWAT Release:
model.run()

#4.Transfer your SWAT Results to a SQLITE Database
*Future modules will include other DB Insertion and Manipulation
result = model.getModelQuery(file="swat_db.sqlite", query=sql, pandas_output=False)

#5.Query the model in a database for certain data
my_query = """SELECT * 
            FROM hru 
            WHERE sub = 1
            """
result = model.getModelQuery(query=my_query,file="swat_db.sqlite")
```

## 4. Explore you data! 