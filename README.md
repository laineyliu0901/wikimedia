## Wikimedia Data


### Directory Structure

```
Pandora CC/
   |---- history/
   |       |---- data that has been downloaded and ingested
   |---- waiting/
   |       |---- data that has been downloaded, waiting to be ingested
   |---- database/
   |       |---- database that store the ingested data, table name: wikimedia
   |---- __init__.py
   |---- wikimedia.py
   |---- inputdata.py
   |---- user.py
   |---- const.py
   |---- pick.py
   |---- logger.py
   |---- utils.py
   |---- README.md
   |---- requirements.txt (WIP)
```


### Running

1. 

2. This project runs with Python 3.6. Install dependencies with

   ```
   pip install -r requirements.txt
   ```

   and then run the following command(make sure you are inside the models folder)

   ```
   python merge.py left_data.csv right_data.csv left_column right_column
   ```
