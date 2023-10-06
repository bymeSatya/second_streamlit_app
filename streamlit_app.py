import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('😎This is My streamlit Application')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_file = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_file = my_file.set_index('Fruit')
fruit_selected=streamlit.multiselect("Pick Some Fruits:",list(my_file.index))
# streamlit.dataframe(my_file)
fruit_to_show=my_file.loc[fruit_selected]
streamlit.dataframe(fruit_to_show)


def get_fruityvicedata(this_fruit_choice):
    #streamlit.write('The User Entered',fruit_choice)
    fruity_responce=requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    #streamlit.text(fruity_responce.json())
    fruity_normalize = pandas.json_normalize(fruity_responce.json())
    return fruity_normalize
  
streamlit.title('Fruityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input('What Fruit would you like to Informaton About ?')
  if not fruit_choice:
    streamlit.error("Please select the fruit to get infromation!")
  else:
    back_from_fruityvice=get_fruityvicedata(fruit_choice)
    streamlit.dataframe(back_from_fruityvice)
except URLError as e:
  streamlit.error()

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)
# streamlit.stop()
# my_data_row = 
# streamlit.text("My Fruit List:")

# fruit_add = streamlit.text_input('What Fruit would you like to Add ?')
# streamlit.write('Enter the fruit',fruit_add)
# my_cur.execute("insert into fruit_load_list values("+fruit_add+")")
# streamlit.text("Thanks for Adding Fruit"+fruit_add)

def get_fruitlist_data():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_fruitload=get_fruitlist_data()
    my_cnx.close()
    streamlit.dataframe(back_from_fruitload)
    
def insert_fruit_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('"+new_fruit+"')")
        return "Thanks for Adding New Fruit "+new_fruit
fruit_add = streamlit.text_input('What Fruit would you like to Add ?')
if streamlit.button("Insert a New Fruit into the List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_insertfruitload=insert_fruit_snowflake(fruit_add)
    my_cnx.close()
    streamlit.text(back_from_insertfruitload)
