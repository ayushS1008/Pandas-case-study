import streamlit as st
import pandas as pd
import plotly.express as px
# import matplotlib.pyplot as plt

st.set_page_config(layout="wide",page_title="Startup Analysis")

df = pd.read_csv('startup_cleaned.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

startup_replacements = {
    "Flipkart.com": "Flipkart",
    "Ola Cabs": "Ola",
    "Olacabs": "Ola",
    "Rapido": "Rapido Bike Taxi",
    "Big Basket": "BigBasket",
    r"BYJU\\'S": "BYJU’S",
    r"BYJU\\xe2\\x80\\x99s": "BYJU’S",
    "\"BYJU\\'S\"": "BYJU’S",
    r"Byju\\xe2\\x80\\x99s": "BYJU’S",

}

df["Startup"] = df["Startup"].astype("string").str.strip().replace(
    startup_replacements
)


total_amt = round(df["Amount"].sum())
max_amt = round(df.groupby("Startup")["Amount"].max().
                sort_values(ascending=False).head(1).values[0])
count = df["Startup"].nunique()
mean = round(df.groupby("Startup")["Amount"].sum().mean())


def load_overall_analysis():

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total",str(total_amt)+" cr")
    with col2:
        st.metric("Max", str(max_amt) + " cr")
    with col3:
        st.metric("Count", str(count))
    with col4:
        st.metric("Average", str(mean) + " cr")

    temp_df1 = df.groupby(["Year","Month"])["Amount"].sum().reset_index()
    temp_df1["x_axis"] = (temp_df1["Year"].astype(str) +"-"+
                          temp_df1["Month"].astype(str))
    temp_df1 = temp_df1[["Amount","x_axis"]]

    temp_df2 = df.groupby(["Year", "Month"])["Startup"].count().reset_index()
    temp_df2["x_axis"] = (temp_df2["Year"].astype(str) + "-" +
                          temp_df2["Month"].astype(str))

    ##
    st.subheader("M-O-M Analysis")

    option1 = st.selectbox("Select Type of M-O-M Analysis",
                           ("Total","Count"))
    if option1 == "Total":
        fig1 = px.line(temp_df1,x="x_axis",y="Amount")
        st.plotly_chart(fig1)
    else:
        fig2 = px.line(temp_df2, x="x_axis", y="Startup")
        st.plotly_chart(fig2)
    ##
    st.subheader("Sector Analysis")

    option2 = st.selectbox("Select type of Sector Analysis",
                           ("Total", "Count"))
    if option2 =="Total":
        sectors = df.groupby("Vertical")["Amount"].sum()\
                   .sort_values(ascending=False).head(10)
    else:
        sectors = df.groupby("Vertical")["Amount"].count()\
                   .sort_values(ascending=False).head(10)

    fig3 = px.pie(sectors, names=sectors.index,
                  values=sectors.values)
    st.plotly_chart(fig3)

    ##
    st.subheader("Types of funding")

    funding = df.groupby("Round")["Round"].count().sort_values(ascending=False)\
               .head(10)
    funding = funding.drop(['Seed/ Angel Funding', 'Seed / Angel Funding',
                            'Seed/Angel Funding'])
    ind = funding.index.values
    val = funding.values
    fig4 = px.bar(funding,x=ind,y=val)
    fig4.update_layout(
        xaxis_title="Type of funding",
        yaxis_title="Amount",
    )
    st.plotly_chart(fig4)

    ##
    st.subheader("Top cities for funding")

    df["City"] = df["City"].replace({"Bengaluru": "Bangalore", "Gurugram":
        "Gurgaon"})
    cities = df.groupby("City")["Amount"].sum().sort_values(ascending=False)\
              .head(10).reset_index()

    fig4 = px.bar(cities, x="City", y="Amount")
    fig4.update_layout(
        xaxis_title="Type of funding",
        yaxis_title="Amount",
    )
    st.plotly_chart(fig4)

    ##
    st.subheader("Top Startups")

    # df["Startup"] = df["Startup"].replace(
    #     {"Flipkart.com": "Flipkart", "Ola Cabs": "Ola",
    #      "BYJU\\xe2\\x80\\x99s": "BYJU’S", "Byju\\xe2\\x80\\x99s": "BYJU’S",
    #      "BYJU\\'S": "BYJU’S", "Rapido": "Rapido Bike Taxi", "Olacabs": "Ola",
    #      "Big Basket": "BigBasket"})
    startup = df.groupby("Startup")["Amount"].sum().sort_values(ascending=False)\
               .head(10).reset_index()

    fig5 = px.bar(startup, x="Startup", y="Amount")
    fig5.update_layout(
        xaxis_title="Startup",
        yaxis_title="Amount",
    )
    st.plotly_chart(fig5)

    ##
    st.subheader("Top 10 Investors")

    investors = (df.groupby("Investors")["Amount"].sum()\
    .sort_values(ascending=False).head(10).reset_index())

    # fig6 = px.bar(cities, x="City", y="Amount")
    fig6 = px.pie(investors, names="Investors",
                  values="Amount")
    st.plotly_chart(fig6)


def load_investor_details(investor):
    st.title(investor)
    last5_df = df[df["Investors"].str.contains(investor)].head()[["Date",
    "Startup","Vertical","City","Round","Amount"]]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)
    # col1, col2 = st.columns(2)
    # col3, col4 = st.columns(2)
    # col5, col6 = st.columns(2)


    #1st figure
    big_df = df[df["Investors"].str.contains(investor)].groupby('Startup')\
        ["Amount"].sum().sort_values(ascending=False).head().reset_index()
    st.subheader("Biggest Investments")
    fig1 = px.bar(big_df,x="Startup",y="Amount")
    st.plotly_chart(fig1)

    # with col2:
    #     ###
    #     fig_a, ax_a = plt.subplots()
    #     ax_a.bar(x=big_df["Startup"],height=big_df["Amount"])
    #     st.pyplot(fig_a)


    #2nd figure
    st.subheader("Sector Analysis")
    vertical_series = df[df["Investors"].str
    .contains(investor)].groupby("Vertical")["Amount"].sum()
    fig2 = px.pie(vertical_series,names=vertical_series.index,
                  values=vertical_series.values)
    st.plotly_chart(fig2)


    # with col4:
    #     ###
    #     fig_b, ax_b = plt.subplots()
    #     ax_b.pie(x=vertical_series.values,labels=vertical_series.index)
    #     st.pyplot(fig_b)


    #3rd figure
    st.subheader("Y-O-Y Analysis")
    yoy = df[df["Investors"].str.contains(investor)]\
    .groupby("Year")["Amount"].sum().reset_index()

    fig3 = px.line(yoy,y="Amount",x="Year")
    st.plotly_chart(fig3)

    # with col6:
    #     ###
    #     yoy = df[df["Investors"].str.contains(investor)] \
    #         .groupby("Year")["Amount"].sum()
    #     fig_c, ax_c = plt.subplots()
    #     ax_c.plot(yoy)
    #     st.pyplot(fig_c)


def load_startup_details(startup):
    st.header(startup)
    industry = df[df['Startup'] == startup]["Vertical"].values[0]
    sub_industry = df[df['Startup'] == startup]["Vertical"].values[0]

    funding_rounds = df[df['Startup'] == "Rapido Bike Taxi"]\
    [["Round","Amount"]].set_index("Round").reset_index()
    city = df[df['Startup'] == "Flipkart"]["City"].values[0]
    st.write(f"**Industry: {industry}**")
    st.write("**Sub-Industry: {}**".format(sub_industry))
    st.write("**Location: {}**".format(city))

    st.subheader("Funding Rounds")

    fig = px.bar(funding_rounds,x="Round",y="Amount")
    st.plotly_chart(fig)




st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select your analysis',
                              ['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    # btn0 = st.sidebar.button("Show Overall Analysis")
    # if btn0:
    load_overall_analysis()

elif option == 'StartUp':
    startup = st.sidebar.selectbox('Select StartUp',
                         sorted(df['Startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
    if btn1:
        load_startup_details(startup)



else:
    x = st.sidebar.selectbox('Select StartUp',
                             sorted(set(df["Investors"].str.split(",").sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(x)
