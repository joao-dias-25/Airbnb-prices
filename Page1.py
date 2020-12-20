import streamlit as st
import pandas as pd

def app(df,geojson_file):
    st.write('## Top 15 Neighbourhoods with the most flat listings on AirBnB')

    top15 = df.loc[df.date == '2020-10-13']['neighbourhood_cleansed'].value_counts()[:15].index.tolist()
    top40 = df.loc[df.date == '2020-10-13']['neighbourhood_cleansed'].value_counts()[:40].index.tolist()
    df2=df.groupby(['neighbourhood_cleansed','date'],as_index=False).count()[['neighbourhood_cleansed','date','id','price']]
    df2.date = pd.to_datetime(df2.date, format='%Y-%m-%d')



    import plotly.express as px

    toplot = df2.loc[df2['neighbourhood_cleansed'].isin(top15)]
    fig = px.line(toplot, x="date", y="id", color='neighbourhood_cleansed')
    fig.update_yaxes(title_text='number of listings')

    st.plotly_chart(fig)

    df3 = df.groupby(['neighbourhood_cleansed', 'date'], as_index=False).median()[
        ['neighbourhood_cleansed', 'date', 'id', 'price']]
    df3.date = pd.to_datetime(df2.date, format='%Y-%m-%d')
    topprice = df3.loc[df2['neighbourhood_cleansed'].isin(top15)]
    fig2 = px.line(topprice, x="date", y="price", color='neighbourhood_cleansed')
    fig2.update_yaxes(title_text='Median price per night')
    st.plotly_chart(fig2)

    import json

    with open(geojson_file,encoding ='utf-8') as json_file:
        data = json.load(json_file)

    import plotly.express as px

    dfmap = df.loc[df.date == '2020-11-10']
    dfmap = dfmap.groupby(['neighbourhood_cleansed'], as_index=False).median()[
        ['neighbourhood_cleansed','id', 'price']]
    dfmap = dfmap.loc[dfmap['neighbourhood_cleansed'].isin(top40)]

    fig3 = px.choropleth_mapbox(dfmap, geojson=data, locations='neighbourhood_cleansed',
                               featureidkey="properties.neighbourhood", color='price',

                               mapbox_style="carto-positron",
                               zoom=10, center={"lat": 52.5, "lon": 13.4},
                               opacity=0.5
                               )
    fig3.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig3)


