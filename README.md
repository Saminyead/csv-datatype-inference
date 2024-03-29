# Data Type Inference API
Before you can even get to analyzing data, or working with them, the first thing you need to do is clean them. And if you do not have a clean data, your data will not be inferred correctly, e.g. when you are using the Python Pandas library. This API was made as a "one-click solution" for inferring correct data types. All you need to do, send your CSV file through one API request, and you have all the correct data types. 

## Setup
To set up the API server, you first need to install Python 3.11. Then:

1. Navigate to any directory, and create and activate a virtual environment.

2. In the same directory, if you have git installed, clone this repository by running:  
```
    https://github.com/Saminyead/csv-datatype-inference.git
```  
If you do not have git installed, then click on "Code", and click "Download ZIP". Download it in the same directory as the virtual environment folder, and extract the ZIP file.

3. Go to the project root, and start a terminal/command prompt session. If you are on Linux/Mac, run:   
```
    python3 manage.py runserver
```   
or   
```
    python manage.py runserver
```   
If you are on Windows, run:   
```
    py manage.py runserver
```   
By default, this will run the server on port 8000. You can also specify a port (e.g. port 5000) by:   
```
    python3 manage.py runserver 5000
```   
or:   
```
    py manage.py runserver 5000
```   

## Usage

You can now direct your API request to:   
http://127.0.0.1:8000/api/datatype   
You can send API request via Python by using the `requests` library. An example code is as follows:   

```
import requests
import pandas as pd
import json

response = requests.post(
    url="http://127.0.0.1:8000/api/datatype/",
    files={"file":open("path/to/your/csv/file.csv",'r')}
).json()

inferred_data = response['inferred_data']['inferred_data_json']
inferred_data_types = response['inferred_data']['inferred_data_types']
inferred_data_types_readable = response['inferred_data']['inferred_data_types_readable']

print(inferred_data_types)

# to view the data types in readable format
print(inferred_data_types_readable)

# if you want to display the data as a pandas dataframe
df = pd.read_json(inferred_data)
print(df)

# to apply the inferred column data types from the API response
for col in df.columns:
    col_dtype = response_json['inferred_data']['inferred_data_types'][col]
    df[col] = df[col].astype(col_dtype)
print(df.dtypes)

# to save the new inferred dataframe to a CSV file
df.to_csv("inferred_data.csv")

# to save the inferred data types to a json file

with open('inferred_datatypes.json', 'w') as outfile:
    json.dump(inferred_data_types, outfile)
```   


