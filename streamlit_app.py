import pandas 
import requests 
import streamlit
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner') 

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# adding put list  
selected_fruits = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index),['Avocado', 'Banana'])
fruits_to_show = my_fruit_list.loc[selected_fruits]                
streamlit.dataframe(fruits_to_show)

# function to get fuityvice data 
def get_fuityvice_data(this_fruit_choise):
  fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + this_fruit_choise)
  fruityvice_norm = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_norm

# New section to display Fruityvice API response 
streamlit.header('Fruityvice Fruit Advice!')
try: 
  selected_fruit = streamlit.text_input('What fruit would you like informaiton about?')
  if not selected_fruit: 
    streamlit.error("Please select a fruit to get information on.")
  else:
    #streamlit.write("The user selection is: ", selected_fruit)
    #fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + selected_fruit)
    #streamlit.text(fruityvice_response.json())

    # Norm. the json before display it in DF
    #fruityvice_norm = pandas.json_normalize(fruityvice_response.json())
    back_from_function = get_fuityvice_data(selected_fruit)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
  
  
streamlit.header("View Our Fruit List - Add Your Favorites!")

# SF realted function 
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur: 
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
  
# adding a button to load the fruit 
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

#allow end user to add a fruit to the list 
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add Fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
