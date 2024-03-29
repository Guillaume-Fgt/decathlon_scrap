# Scrap_Decathlon_Streamlit

Tool to scrap Decathlon website and display stocks for Gravel Bike.

Use bs4 and Selenium to populate a database (using sqlite3).
Then display the content on a webapp using Streamlit.

Files:

- db_operations : to create the database and the table
- populate db: beautiful soup scrap of the website. Populate bike_name, bike_price and bike_url columns.
- stocks_scrap: selenium part of the scrapping (because a button had to be clicked). The functions inside this module are called from Steamlit interface.
- decathlon_scrap.py: Streamlit web app. Run it using "Streamlit run decathlon_scrap.py" command in the directory.

![Animation](https://user-images.githubusercontent.com/66461774/156323899-2bcf364e-d461-4b86-b642-ab241bf2adab.gif)

How to use it:

clone the repo:
```
git clone https://github.com/Guillaume-Fgt/decathlon_scrap.git
```
Navigate to the clone directory and use [poetry](https://python-poetry.org/docs/) to install dependencies:
```
poetry install
```



Activate the virtual environment created and run streamlit:
```
streamlit run decathlon_scrap\decathlon_scrap.py
```
