# Scrap_Decathlon_Streamlit

Tool to scrap Decathlon website and display stocks for Gravel Bike.

Use bs4 and Selenium to populate a database (using sqlite3).
Then display the content on a webapp using Streamlit.

Files:

- create_db : to create the database and the table
- populate db: beautiful soup scrap of the website. Populate bike_name, bike_price and bike_url columns.
- dispo_scrap: selenium part of the scrapping (because a button had to be clicked). The functions inside this module are called from Steamlit interface.
- main.py: Streamlit web app. Run it using "Streamlit run main.py" command in the directory.




