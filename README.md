## Wikimedia Data


### Directory Structure

```
WikiMedia/
   |---- Pandora.ipynb(demonstrate the thought process, please take a look at this before dig deep into the codes)
   |---- history/
   |       |---- data that has been downloaded and ingested
   |---- waiting/
   |       |---- data that has been downloaded, waiting to be ingested
   |---- database/
   |       |---- database that store the ingested data, table name: wikimedia, I am using sqlite here.
   |---- __init__.py
   |---- wikimedia.py
   |---- inputdata.py
   |---- user.py
   |---- const.py
   |---- logger.py
   |---- utils.py
   |---- README.md
   |---- requirements.txt (WIP)
```


### Running

1. This project runs with Python 3.6. Install dependencies with

   ```
   pip install -r requirements.txt
   ```

2. please create 3 folders 'history'. 'waiting' and 'database'.


3. and then run the following command(make sure you are inside the wikimedia folder)

   ```
   python wikimedia.py year month day hour
   ```

