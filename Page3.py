import streamlit as st
import pandas as pd

def app(df):

    st.title('AirBnB in Berlin')
    st.write('## Calculate your flat')

    col1, col2 = st.beta_columns(2)

    with col1:
        y=st.selectbox('neighbourhood', df.neighbourhood_cleansed.unique())
    df2=df.loc[df.neighbourhood_cleansed==y]

    import plotly.express as px

    df2.date = pd.to_datetime(df2.date, format='%Y-%m-%d')
    df3 = df2.groupby(['date']).describe()['price']

    df3 = df3.rename(columns={'25%': 'lower quantile (>25%)',
                             '50%': 'Median price',
                              '75%': 'upper quantile (<75%)',
                             'mean': 'Average price'})

    fig = px.line(df3, x=df3.index, y=['lower quantile (>25%)',
                                       'Median price',
                                       'upper quantile (<75%)',
                                       'Average price']
                  )

    fig.update_yaxes(title_text='Price per night')

    fig.update_layout(legend_title_text='price range',
                      legend=dict(y=1))

    st.plotly_chart(fig)
