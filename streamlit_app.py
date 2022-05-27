import pandas 
import requests 
import streamlit

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

# New section to display Fruityvice API response 
fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response)
