# Video Game Sales Analysis Dashboard 
# Built-using Streamlit
#importing Libraires  
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# Reading csv file
df = pd.read_csv("E:/Projects/Dashboard/vgsales.csv")
df.info()

# Publisher column had some NULL values so those rows were dropped
df.dropna(inplace=True) 
df.info()

# dataset introduction

print(df["Year"].nunique())
print(df["Year"].unique())
print(df["Genre"].nunique())
print(df["Genre"].unique())
print(df["Publisher"].nunique())
#print(df["Publisher"].unique())
print(df["Platform"].nunique())
print(df["Platform"].unique())


# To set basic configuration of the webpage 
# Title specifies name that appears on Tab, layout used to cover the whole page default is center
st.set_page_config(
    page_title="VideoGame Sales Analysis",
    initial_sidebar_state="expanded",
    layout="wide"
)


# Code for the Sidebar Starts sidebar has 4 types of filters available which are
# Country, Year , Genre, Platform 
# All the filters are single select i.e we can only select one value for each filter 

st.sidebar.header("Please Filter Here")
country = st.sidebar.selectbox(
    "Select the Region:",
    options=df.columns[6:],    
)
Genre = st.sidebar.selectbox(
    "Select the Genre:",
    options=df["Genre"].unique(),    
)
Year = st.sidebar.selectbox(
    "Select the Year:",
    options=df["Year"].unique(),   
)
Platform = st.sidebar.selectbox(
    "Select the Platform:",
    options=df["Platform"].unique(),    
)
# SideBar FINISH 



# To write Page Heading
st.title("VideoGame Sales Analysis")

# Code for Image display
# Columns were used so that image can be placed in middle
col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    st.image("https://img.olhardigital.com.br/wp-content/uploads/2021/05/shutterstock_1860839008-1280x450.jpg",width=900)
with col3:
    st.write("")
# image display finish

# For displaying introductory texts
st.write("Video games are a billion-dollar business and have been for many years. A video game is an electronic game that can be played on a computing device, such as a personal computer, gaming console or mobile phone. Depending on the platform, video games can be subcategorized into computer games and console games.")
st.write("This dashboard can be used for comparison of video game sales using different filters present in the dashboard. The dataset used has sales data in different regions of various video games of different genre, publishers & Platform over a period of 1980-2016")
st.write("-Made By Lovish Bansal ")
## Creating a new filtered dataframe yr which only has values of year which we have selected in the sidebar
yr=df.query(
    "Year == @Year",
)
#print(yr)

# to calculate total world sales in the selected year 
total_sales_part_year=round(yr["World Sales"].sum(),2)

# makes a new object sorted by total world sales of games of different genre
# group by command groups column according to genre column then sum sums data of same group and world sales is the only column we need so we keep that column
genre_group=yr.groupby(by=["Genre"]).sum()[["World Sales"]].sort_values(by="World Sales", ascending=False)
#print(genre_group.index)

#sorts yr df according to world sales we need most sold game so we will pick it's first entry
most_sold_game=yr.sort_values(by="World Sales", ascending=False)
#print(most_sold_game)

# column used to display the above data parallel to one another
left_column,middle_column,right_column=st.columns(3)
with left_column:
    st.subheader(f"Total Sales in {Year}:")
    st.subheader(f"{total_sales_part_year:,}")

with right_column:
    st.subheader(f"Most Sold Genre in {Year}:")
    st.subheader(genre_group.index[0])

with middle_column:
    st.subheader(f"Most Sold Game in {Year}:")
    st.subheader(most_sold_game.values[0,1])

# Top notch finish

st.markdown("##")
st.markdown("##")

# Data Visulisation part starts 


# Pie chart showing Global Sale of all years of different Genres
# Grouping data from original dataframe on the basis of Genre and summing there world sales
genre_wise=(
    df.groupby(by=["Genre"]).sum()[["World Sales"]]
)
#print(genre_wise)

#code for pie chart using plotly-express
genre_pie = px.pie(
    data_frame=genre_wise, 
    names=genre_wise.index,
    values="World Sales" ,
    title= "<b>All Time Sales Of Different Genres</b>"
)
#st.plotly_chart(genre_pie)
#code for 1st pie chart ends

# Code for line chart Representing sales over different year starts 
# Grouping data from original dataframe on the basis of Year and summing there world sales
year_wise=(
    df.groupby(by=["Year"]).sum()[["World Sales"]]
)
#print(year_wise)
#code for line chart using plotly
year_line=px.line(year_wise,x=year_wise.index,y="World Sales",title="<b>Sales Trend By Year</b>")
#st.plotly_chart(year_line)
#code for 1st line chart ends

# code for displaying above charts on webpage in columns starts 
left_column,middle_column, right_column = st.columns(3)
left_column,middle_column,right_column = st.columns([1,0.15, 1])
left_column.plotly_chart(genre_pie, use_container_width=True)
right_column.plotly_chart(year_line, use_container_width=True)
#code ends 2 charts displayed


st.markdown("##")
st.markdown("##")


# Creates new filtered dataframe with genre equal to genre selected in sidebar
genre=df.query(
    "Genre == @Genre",
)

# grouping by genre
genre_hist=(
    genre.groupby(by=["Platform"]).sum()
)
#print(genre_hist)
# Plotting Histogram showing sales comparison of different platforms of selected genre in selected region
genre_hist=px.histogram(genre_hist,x=genre_hist.index,y=genre_hist[country],title="<b>Popularity Of Different Platforms for a given Genre in Selected Region</b>",width=1000)



# Code for line chart showing popularity of selected Platform over different yeyars in selected region
plt=df.query(
    "Platform == @Platform",
)
plat_line=(
    plt.groupby(by=["Year"]).sum()
)
#print(plat_line[country])

plat_line=px.line(plat_line,x=plat_line.index,y=plat_line[country],title="<b>Popularity Of Platform By Year In Selected Region</b>")
# st.plotly_chart(plat_line)
#code for line chart ends

# Code for pie chart showing sales comparison in different regions in selected year
Select_year_pie = px.pie(
    data_frame=yr,
    names=yr.columns[6:-1],
    values=yr.iloc[:,6:-1].sum(),
    hole=0.6,
    title="<b>Total sale during the given year in different Regions</b>"   
)
#st.plotly_chart(Select_year_pie)

## Code for displaying above charts on dashboard
left_column,middle_column, right_column = st.columns(3)
left_column,middle_column,right_column = st.columns([1,0.15, 1])
left_column.plotly_chart(Select_year_pie, use_container_width=True)
right_column.plotly_chart(plat_line, use_container_width=True)


st.markdown("##")
st.markdown("##")


left_column,middle_column, right_column = st.columns(3)
left_column,middle_column,right_column = st.columns([0.1,1, 0.1])
middle_column.plotly_chart(genre_hist, use_container_width=True)



## Code for displaying bar chart of total sales of top 10 publishers steps similar to those taken above 
top_publisher=(
    df.groupby(by=["Publisher"]).sum()[["World Sales"]].sort_values(by="World Sales",ascending=False).head(10)
)

top_publi=px.bar(top_publisher,x = top_publisher.index,
            y = 'World Sales', width=1000,title="Top 10 Publishers Of All Time"
            
);
left_column,middle_column, right_column = st.columns(3)
left_column,middle_column,right_column = st.columns([0.1,1, 0.1])
middle_column.plotly_chart(top_publi, use_container_width=True)

## END OF CODE 