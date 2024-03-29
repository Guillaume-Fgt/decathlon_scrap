import streamlit as st
from datetime import datetime
import stocks_scrap
import config
from db_operations import open_db

st.title("Decathlon gravel bikes stocks*")
col1, col2 = st.columns(2)
col1 = st.caption("* N/A = size doesn't exist")

st.sidebar.title("Filters")
dispo = st.sidebar.checkbox("Only available ones")


with open_db(config.DB_PATH) as cursor:
    if dispo:
        data = cursor.execute(
            """
            SELECT *
            FROM bike
            WHERE XXS LIKE ? OR XS LIKE ? OR S LIKE ? OR M LIKE ? OR L LIKE ? OR XL LIKE ?
        """,
            (
                "En stock%",
                "En stock%",
                "En stock%",
                "En stock%",
                "En stock%",
                "En stock%",
            ),
        )
    else:
        data = cursor.execute(
            """
            SELECT *
            FROM bike 
        """
        )
    data_fetched = data.fetchall()

# prices slider
prices = [data_price["price"] for data_price in data_fetched]
prix = st.sidebar.slider("Price filter (€)", value=[0, max(prices)])
#

# # Number of bike corresponding to filter price
with open_db(config.DB_PATH) as cursor:
    if dispo:
        data = cursor.execute(
            """
            SELECT COUNT(id)
            FROM bike
            WHERE (price >=? AND price <=?) AND (XXS LIKE ? OR XS LIKE ? OR S LIKE ? OR M LIKE ? OR L LIKE ? OR XL LIKE ?)
            """,
            (
                prix[0],
                prix[1],
                "En stock%",
                "En stock%",
                "En stock%",
                "En stock%",
                "En stock%",
                "En stock%",
            ),
        )
    else:
        data = cursor.execute(
            """
            SELECT COUNT(id)
            FROM bike
            WHERE price >=? AND price <=?
            """,
            (
                prix[0],
                prix[1],
            ),
        )
    st.sidebar.caption(f"{data.fetchone()[0]} bikes meet criterias")


for data_one in data_fetched:
    if prix[0] <= data_one["price"] <= prix[1]:
        st.subheader(f'{data_one["bike_name"]}')
        st.caption(f'Price: {data_one["price"]} €')
        st.markdown(f'**Go to website:** [Decathlon.com]({data_one["bike_link"]})')
        avail = [
            data_one["XXS"],
            data_one["XS"],
            data_one["S"],
            data_one["M"],
            data_one["L"],
            data_one["XL"],
        ]
        columns = ["XXS", "XS", "S", "M", "L", "XL"]
        nbr_col = 6
        col_str = ""
        for i in range(1, 7):
            col_str += "col" + str(i) + ","
        col_str = st.columns(6)
        for index, col in enumerate(col_str):
            with col:
                st.markdown(f"**{columns[index]}**")
                if avail[index] == "N/A" or avail[index] == "En rupture de stock":
                    st.write(f":red_circle:{avail[index]}")
                else:
                    st.write(f":white_check_mark:{avail[index]}")

# Update stocks
st.sidebar.title("Update stocks ( = scrap website)")
clicked = st.sidebar.button("MàJ")
if clicked:
    urls = stocks_scrap.generate_url_list()
    outputs = stocks_scrap.selenium_avalaiblility(urls)
    clear = st.sidebar.button("Clear logs")
    col2 = st.caption(f"Updated: {datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}")
    if clear:
        outputs = st.sidebar.write("")
#
