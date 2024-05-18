import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import json 
import requests


#Dataframe creation

#sql connection

mydb= psycopg2.connect(host= "localhost",
                       user= "postgres",
                       port="5432",
                       database="phonepe_data",
                       password= "Peni@2315")
cursor= mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1 =cursor.fetchall()

Aggre_insurance= pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Insurance_name", 
                                                    "Insurance_count", "Insurance_amount"))

#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 =cursor.fetchall()

Aggre_transaction= pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type", 
                                                    "Transaction_count", "Transaction_amount"))


#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3 =cursor.fetchall()

Aggre_user= pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands", 
                                                    "Transaction_count", "Percentage"))


#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4 =cursor.fetchall()

Map_insurance= pd.DataFrame(table4, columns=("States", "Years", "Quarter", "Districts", 
                                                    "Users_count", "Total_amount"))


#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5 =cursor.fetchall()

Map_transaction= pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Districts", 
                                                    "Transaction_count", "Transaction_amount"))


#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6 =cursor.fetchall()

Map_user= pd.DataFrame(table6, columns=("States", "Years", "Quarter", "Districts", 
                                                    "Registered_Users", "App_Opens"))


#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7 =cursor.fetchall()

Top_insurance= pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Dis_Pincode", 
                                                    "Insurance_count", "Total_amount"))



#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8 =cursor.fetchall()

Top_transaction= pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Dis_Pincode", 
                                                    "Trans_count", "Trans_amount"))



#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9 =cursor.fetchall()

Top_user= pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Dis_Pincode", 
                                                     "Registered_Users"))

#analysis_function
def  Transaction_amount_count_Y(df,year):

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Insurance_count","Insurance_amount"]].sum()
    tacyg.reset_index(inplace=True)


    fig_amount= px.bar(tacyg, x="States",y="Insurance_amount",title=f"{year} Insurance Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
    st.plotly_chart(fig_amount)

    fig_count= px.bar(tacyg, x="States",y="Insurance_count",title=f"{year} Insurance Count",
                        color_discrete_sequence=px.colors.sequential.Burgyl_r, height=650,width=600)
    st.plotly_chart(fig_count)

    return tacy

def  Transaction_amount_count_Y_Q(df, quarter):

    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Insurance_count","Insurance_amount"]].sum()
    tacyg.reset_index(inplace=True)


    fig_amount= px.bar(tacyg, x="States",y="Insurance_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER Insurance Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount)

   

    fig_count= px.bar(tacyg, x="States",y="Insurance_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER Insurance Count",
                        color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
    st.plotly_chart(fig_count)

    return tacy


def  Trans_amount_count_Y(df, year):

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    fig_amount= px.bar(tacyg, x="States",y="Transaction_amount",title=f"{year} Transaction Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount)


    fig_count= px.bar(tacyg, x="States",y="Transaction_count",title=f"{year} Transaction Count",
                        color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
    st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1=json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations="States", featureidkey="properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name= "States",title = f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height=650,width=600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:


        fig_india_2= px.choropleth(tacyg, geojson= data1, locations="States", featureidkey="properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name= "States",title = f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height=650,width=600)
        
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
    return tacy

def Aggre_Tran_Transaction_type(df,state):
    tacy =df[df["States"] == state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)


    fig_pie_1 =px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                            width= 600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
    st.plotly_chart(fig_pie_1)

    

    fig_pie_2 =px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                            width= 600, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)
    st.plotly_chart(fig_pie_2)

def  Agree_transa_quarter(df, quarter):

    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:


        fig_amount= px.bar(tacyg, x="States",y="Transaction_amount",title=f"{tacy['Years'].min()} YEAR {quarter} qUARTER TRANSACTION Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count= px.bar(tacyg, x="States",y="Transaction_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
        st.plotly_chart(fig_count)

    return tacy


#aggre_user_year

def Aggre_user_plot_1(df,year):
    aguy=df[df["Years"]== year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg, x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                        width=1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#aggre_user_year_quarter

def Aggre_user_plot_2(df,quarter):
    aguyq=df[df["Quarter"]== quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_2=px.bar(aguyqg, x="Brands", y="Transaction_count", title=f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                        width=1000, color_discrete_sequence= px.colors.sequential.Darkmint,hover_name="Brands")
    st.plotly_chart(fig_bar_2)

    return aguyq


#aggre_user_year_quarter_state

def Aggre_user_plot_3(df,state):
    aguyqs=df[df["States"]==state ]
    aguyqs.reset_index(drop=True, inplace=True)

    fig_bar_3=px.line(aguyqs, x="Brands", y="Transaction_count", title=f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE ",
                   hover_name="Percentage",markers=True,width=1000)
    st.plotly_chart(fig_bar_3)

    return aguyqs


#map_ins_year
def  map_insu_y(df,year):

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Users_count","Total_amount"]].sum()
    tacyg.reset_index(inplace=True)


    fig_amount= px.bar(tacyg, x="States",y="Total_amount",title=f"{year} Total Amount",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount)

    fig_count= px.bar(tacyg, x="States",y="Users_count",title=f"{year} USER COUNT",
                    color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
    st.plotly_chart(fig_count)

    return tacy

#map_insu_state

def map_insur_dist(df,state):
    tacy =df[df["States"] == state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg= tacy.groupby("Districts")[["Users_count","Total_amount"]].sum()
    tacyg.reset_index(inplace = True)

    fig_bar_1 =px.bar(data_frame= tacyg, y= "Districts", x= "Total_amount",
                         title=f"{state.upper()} DISTRICTS TOTAL AMOUNT", orientation="h" )
    st.plotly_chart(fig_bar_1)

    fig_bar_2 =px.bar(data_frame= tacyg, y= "Districts", x= "Users_count",
                         title=f"{state.upper} DISTRICTS USER COUNT", orientation="h")
    st.plotly_chart(fig_bar_2)

# map_insurance_quarter

def  map_insura_quarter(df, quarter):

    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Users_count","Total_amount"]].sum()
    tacyg.reset_index(inplace=True)


    fig_amount= px.bar(tacyg, x="States",y="Total_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION Amount",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount)

    fig_count= px.bar(tacyg, x="States",y="Users_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
    st.plotly_chart(fig_count)
    return tacy

#map_transaction_year
def  map_trans_y(df,year):

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)



    fig_amount= px.bar(tacyg, x="States",y="Transaction_amount",title=f"{year} TRANSACTION Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount)


    fig_count= px.bar(tacyg, x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
    st.plotly_chart(fig_count)

    return tacy

#map_trans_state

def map_trans_dist(df,state):
    tacy =df[df["States"] == state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2=st.columns(2)
    with col1:

        fig_bar_1 =px.bar(data_frame= tacyg, y= "Districts", x= "Transaction_amount",
                            title=f"{state.upper()} DISTRICTS TRANSACTION AMOUNT", orientation="h" )
        st.plotly_chart(fig_bar_1)
    with col2:

        fig_bar_2 =px.bar(data_frame= tacyg, y= "Districts", x= "Transaction_count",
                            title=f"{state.upper()} DISTRICTS TRANSACTION COUNT", orientation="h")
        st.plotly_chart(fig_bar_2)

# map_trans_quarter

def  map_trans_quarter(df, quarter):

    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)



    fig_amount= px.bar(tacyg, x="States",y="Transaction_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount)


    fig_count= px.bar(tacyg, x="States",y="Transaction_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
    st.plotly_chart(fig_count)

    return tacy


#map_user_year

def map_user_plot_1(df,year):
    mguy=df[df["Years"]== year]
    mguy.reset_index(drop=True, inplace=True)

    mguyg= mguy.groupby("States")[["Registered_Users", "App_Opens"]].sum()
    mguyg.reset_index(inplace=True)

    fig_bar_1=px.line(mguyg, x="States", y=["Registered_Users","App_Opens" ], title=f"{year} BRANDS AND TRANSACTION COUNT",
                        width=1000, height= 800,markers=True)
    st.plotly_chart(fig_bar_1)
    return mguy

#map_user_year_quarter

def map_user_plot_2(df,quarter):
    mguyq=df[df["Quarter"]== quarter]
    mguyq.reset_index(drop=True, inplace=True)

    mguyqg= mguyq.groupby("States")[["Registered_Users", "App_Opens"]].sum()
    mguyqg.reset_index(inplace=True)

    fig_bar_1=px.line(mguyqg, x="States", y=["Registered_Users","App_Opens" ], title=f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                        width=1000, height= 800,markers=True)
    st.plotly_chart(fig_bar_1)

    return mguyq

#map_user_year_quarter_state 

def map_user_plot_3(df,state):
    mguyqs=df[df["States"]==state ]
    mguyqs.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_bar_1=px.bar(mguyqs, x="Registered_Users", y="Districts", title=f"{state.upper()} REGISTERED USER ",
                    height=800, color_discrete_sequence=px.colors.sequential.Blugrn_r, orientation="h")
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2=px.bar(mguyqs, x="App_Opens", y="Districts", title=f"{state.upper()} APP_OPENS",
                    height=800, color_discrete_sequence=px.colors.sequential.Magenta_r, orientation="h")
        st.plotly_chart(fig_bar_2)

#top_insurance_year
def  top_insura_y(df,year):

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Insurance_count","Total_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States",y="Total_amount",title=f"{year} TOTAL Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)
        
    with col2:

        fig_count= px.bar(tacyg, x="States",y="Insurance_count",title=f"{year} INSURANCE COUNT",
                        color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1=json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations="States", featureidkey="properties.ST_NM",
                                color= "Total_amount", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Total_amount"].min(),tacyg["Total_amount"].max()),
                                hover_name= "States",title = f"{year} TOTAL AMOUNT", fitbounds= "locations",
                                height=650,width=600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(tacyg, geojson= data1, locations="States", featureidkey="properties.ST_NM",
                                color= "Insurance_count", color_continuous_scale= "Rainbow",
                                range_color= (tacyg["Insurance_count"].min(),tacyg["Insurance_count"].max()),
                                hover_name= "States",title = f"{year} INSURANCE COUNT", fitbounds= "locations",
                                height=650,width=600)
        
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy

#top_insurance_state
def top_ins_state(df,state):
    tigs=df[df["States"]== state]
    tigs.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_ins_bar_1=px.bar(tigs, x="Quarter", y="Insurance_count", title=f"{state.upper()} INSURANCE COUNT",hover_name="Dis_Pincode",
                    height=650,width=600, color_discrete_sequence=px.colors.sequential.Blugrn_r)
        st.plotly_chart(fig_ins_bar_1)

    with col2:

        fig_ins_bar_2=px.bar(tigs, x="Quarter", y="Total_amount", title=f"{state.upper()} TOTAL AMOUNT",hover_name="Dis_Pincode",
                    height=650,width=600, color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_ins_bar_2)

    return tigs

# top_insu_quarter

def  top_insu_quarter(df, quarter):

    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Insurance_count","Total_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States",y="Total_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TOTAL Amount",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count= px.bar(tacyg, x="States",y="Insurance_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER INSURANCE COUNT",
                        color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
        st.plotly_chart(fig_count)

    return tacy

#top_trans_year

def  top_trans_y(df,year):

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Trans_count","Trans_amount"]].sum()
    tacyg.reset_index(inplace=True)


    fig_amount= px.bar(tacyg, x="States",y="Trans_amount",title=f"{year} TRANSACTION Amount",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount)

    fig_count= px.bar(tacyg, x="States",y="Trans_count",title=f"{year} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
    st.plotly_chart(fig_count)

    return tacy

#top_transaction_state
def top_transi_state(df,state):
    tigs=df[df["States"]== state]
    tigs.reset_index(drop=True, inplace=True)

    fig_ins_bar_1=px.bar(tigs, x="Quarter", y="Trans_count", title=f"{state.upper()} TRANSACTION COUNT",hover_data="Dis_Pincode",
                  height=800, color_discrete_sequence=px.colors.sequential.Blugrn_r)
    st.plotly_chart(fig_ins_bar_1)

    fig_ins_bar_2=px.bar(tigs, x="Quarter", y="Trans_amount", title=f"{state.upper()} TRANSACTION AMOUNT",hover_data="Dis_Pincode",
                  height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_ins_bar_2)

    return tigs

# top_trans_quarter

def  top_transa_quarter(df, quarter):

    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=tacy.groupby("States")[["Trans_count","Trans_amount"]].sum()
    tacyg.reset_index(inplace=True)


    fig_amount= px.bar(tacyg, x="States",y="Trans_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION Amount",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount)

    fig_count= px.bar(tacyg, x="States",y="Trans_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Burgyl_r,height=650,width=600)
    st.plotly_chart(fig_count)

    return tacy

#top_user_year

def  top_user_y(df,year):

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop= True,inplace=True)

    tacyg=pd.DataFrame(tacy.groupby(["States", "Quarter"])["Registered_Users"].sum())
    tacyg.reset_index(inplace=True)


    fig_amount= px.bar(tacyg, x="States",y="Registered_Users",title=f"{year} REGISTERED USER",color="Quarter",
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,height=800,width=1000,hover_name="States")
    st.plotly_chart(fig_amount)

    return tacy

#top_user_state
def top_trans_state(df,state):
    tigs=df[df["States"]== state]
    tigs.reset_index(drop=True, inplace=True)

    fig_ins_bar_1=px.bar(tigs, x="Quarter", y="Registered_Users", title=f"{state.upper()} REGISTERED USER, PINCODE, QUARTER",   
                   hover_name="Dis_Pincode",height=800, width=1000, 
                   color="Registered_Users", color_discrete_sequence=px.colors.sequential.Blugrn_r)
    st.plotly_chart(fig_ins_bar_1)

    return tigs

#top_10_amount_analysis of aggregated_ins
def top_chart_transaction_amount(table_name):
    mydb= psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port="5432",
                        database="phonepe_data",
                        password= "Peni@2315")
    cursor= mydb.cursor()

    #plot_1

    query1= f'''SELECT states, SUM(insurance_camount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states", "transaction_amount"))
    
    col1,col2=st.columns(2)

    with col1:

        fig_amount= px.bar(df_1, x="states",y="transaction_amount",title=" Top 10 of Transaction Amount",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount)

    #plot_2

    query2= f'''SELECT states, SUM(insurance_camount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount 
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states", "transaction_amount"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states",y="transaction_amount",title="Bottom 10 of Transaction Amount",
                            color_discrete_sequence=px.colors.sequential.Magenta_r,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount_2)

    #plot_3

    query3= f'''SELECT states, AVG(insurance_camount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''


    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="states",x="transaction_amount",title="Average of Transaction Amount",
                        color_discrete_sequence=px.colors.sequential.Cividis,height=850,width=1000,hover_name="states",
                        orientation='h')
    st.plotly_chart(fig_amount_3)

#aggregated_insur_count

def top_chart_transaction_count(table_name):
    #plot_1
    query1= f'''SELECT states, SUM(insurance_count) AS insurance_count
                FROM {table_name}
                GROUP BY states
                ORDER BY insurance_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states", "insurance_count"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states",y="insurance_count",title="Top 10 of Insurance Count",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount)

    #plot_2

    query2= f'''SELECT states, SUM(insurance_count) AS insurance_count
                FROM {table_name}
                GROUP BY states
                ORDER BY insurance_count
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states", "insurance_count"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states",y="insurance_count",title="Bottom 10 of Insurance Count",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount_2)

    #plot_3

    query3= f'''SELECT states, AVG(insurance_count) AS insurance_count
                FROM {table_name}
                GROUP BY states
                ORDER BY insurance_count;'''


    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states", "insurance_count"))

    fig_amount_3= px.bar(df_3, y="states",x="insurance_count",title="Average of Insurance Count",
                        color_discrete_sequence=px.colors.sequential.Greens_r,height=800,width=1000,hover_name="states",
                        orientation='h')
    st.plotly_chart(fig_amount_3)


def top_chart_total_amount(table_name):
    #plot_1
    query1= f'''SELECT states, SUM(total_amount) AS total_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY total_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states", "total_amount"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states",y="total_amount",title=" Top 10 of Total Amount",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount)

    #plot_2

    query2= f'''SELECT states, SUM(total_amount) AS total_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY total_amount
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states", "total_amount"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states",y="total_amount",title="Bottom 10 of Total Amount",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount_2)

    #plot_3

    query3= f'''SELECT states, AVG(total_amount) AS total_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY total_amount;'''


    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states", "total_amount"))

    fig_amount_3= px.bar(df_3, y="states",x="total_amount",title="Average of Total Amount",
                        color_discrete_sequence=px.colors.sequential.Greens_r,height=800,width=1000,hover_name="states",
                        orientation='h')
    st.plotly_chart(fig_amount_3)

def top_chart_user_count(table_name):
    #plot_1
    query1= f'''SELECT states, SUM(users_count) AS users_count
                FROM {table_name}
                GROUP BY states
                ORDER BY users_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states", "users_count"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states",y="users_count",title=" Top 10 of Total Count",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount)

    #plot_2

    query2= f'''SELECT states, SUM(users_count) AS users_count
                FROM {table_name}
                GROUP BY states
                ORDER BY users_count
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states", "users_count"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states",y="users_count",title="Bottom 10 of Total Count",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount_2)

    #plot_3

    query3= f'''SELECT states, AVG(users_count) AS users_count
                FROM {table_name}
                GROUP BY states
                ORDER BY users_count;'''


    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states", "users_count"))

    fig_amount_3= px.bar(df_3, y="states",x="users_count",title="Average of Total Count",
                        color_discrete_sequence=px.colors.sequential.Greens_r,height=800,width=1000,hover_name="states",
                        orientation='h')
    st.plotly_chart(fig_amount_3)

def top_chart_trans_count(table_name):
    #plot_1
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states", "transaction_count"))
    col1,col2=st.columns(2)

    with col1:

        fig_amount= px.bar(df_1, x="states",y="transaction_count",title=" Top 10 of Total Count",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount)

    #plot_2

    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY transaction_count
                    LIMIT 10;'''
                                

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states", "transaction_count"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states",y="transaction_count",title="Bottom 10 of Total Count",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount_2)

    #plot_3

    query3= f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''


    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="states",x="transaction_count",title="Average of Total Count",
                        color_discrete_sequence=px.colors.sequential.Greens_r,height=800,width=1000,hover_name="states",
                        orientation='h')
    st.plotly_chart(fig_amount_3)

def top_chart_trans_amount(table_name):
    #plot_1
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states", "transaction_amount"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states",y="transaction_amount",title=" Top 10 of Total Amount",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount)

    #plot_2

    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''
                                

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states", "transaction_amount"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states",y="transaction_amount",title="Bottom 10 of Total Amount",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount_2)

    #plot_3

    query3= f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''


    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="states",x="transaction_amount",title="Average of Total Amount",
                        color_discrete_sequence=px.colors.sequential.Greens_r,height=800,width=1000,hover_name="states",
                        orientation='h')
    st.plotly_chart(fig_amount_3)


def top_chart_transact_amount(table_name):
    #plot_1
    query1= f'''SELECT states, SUM(trans_amount) AS trans_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY trans_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states", "trans_amount"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states",y="trans_amount",title=" Top 10 of Total Amount",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount)

    #plot_2

    query2= f'''SELECT states, SUM(trans_amount) AS trans_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY trans_amount
                LIMIT 10;'''
                                

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states", "trans_amount"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states",y="trans_amount",title="Bottom 10 of Total Amount",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount_2)

    #plot_3

    query3= f''' SELECT states, AVG(trans_amount) AS trans_amount
                    FROM {table_name}
                    GROUP BY states
                    ORDER BY trans_amount;'''


    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states", "trans_amount"))

    fig_amount_3= px.bar(df_3, y="states",x="trans_amount",title="Average of Total Amount",
                        color_discrete_sequence=px.colors.sequential.Greens_r,height=800,width=1000,hover_name="states",
                        orientation='h')
    st.plotly_chart(fig_amount_3)


def top_chart_transacti_count(table_name):
    #plot_1
    query1= f'''SELECT states, SUM(trans_count) AS trans_count
                FROM {table_name}
                GROUP BY states
                ORDER BY trans_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("states", "trans_count"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states",y="trans_count",title=" Top 10 of Total Count",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount)

    #plot_2

    query2= f'''SELECT states, SUM(trans_count) AS trans_count
                FROM {table_name}
                GROUP BY states
                ORDER BY trans_count
                LIMIT 10;'''
                                

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("states", "trans_count"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states",y="trans_count",title="Bottom 10 of Total Count",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=500,hover_name="states")
        st.plotly_chart(fig_amount_2)

    #plot_3

    query3= f'''SELECT states, AVG(trans_count) AS trans_count
                FROM {table_name}
                GROUP BY states
                ORDER BY trans_count;'''


    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("states", "trans_count"))

    fig_amount_3= px.bar(df_3, y="states",x="trans_count",title="Average of Total Count",
                        color_discrete_sequence=px.colors.sequential.Greens_r,height=800,width=1000,hover_name="states",
                        orientation='h')
    st.plotly_chart(fig_amount_3)


#Streamlit part

st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:

    select= option_menu("MAIN MENU",["HOME","DATA EXPLORATION","TOP CHARTS"])
    
if select =="HOME":
   
    col1,col2=st.columns(2)
    with col1:
       st.header("PHONEPE")
       st.subheader("India's Best Transaction App")
    
    with col2:
       st.image(r"C:\Users\HP\Desktop\phonepeproject\PhonePe-Logo.png")

elif select =="DATA EXPLORATION":

    tab1, tab2, tab3= st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        method=st.radio("Select The Method",["Insurance Analysis","Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
    

                years= st.selectbox("Select The Year",Aggre_insurance["Years"].unique())
                tac_Y=Transaction_amount_count_Y(Aggre_insurance,years) 
           
        
                quarters= st.slider("Select The Quarter",tac_Y["Quarter"].min(), tac_Y["Quarter"].max(),
                            tac_Y["Quarter"].min(),)
                Transaction_amount_count_Y_Q(tac_Y, quarters)
               

        elif method == "Transaction Analysis":

            col1,col2 = st.columns(2) 

            with col1:  

                years= st.selectbox("Select The Year_T",Aggre_transaction["Years"].unique())
            Aggre_tran_tac_Y=Trans_amount_count_Y(Aggre_transaction,years)

            col1,col2 = st.columns(2)

            with col1:
                states= st.selectbox("Select The State_t", Aggre_tran_tac_Y["States"].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2= st.columns(2)
            with col1:
               quarters= st.slider("Select The Quarter_t",Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(),
                            Aggre_tran_tac_Y["Quarter"].min(),)
            tac_quarter = Agree_transa_quarter(Aggre_tran_tac_Y, quarters)

            col1,col2 = st.columns(2)

            with col1:
                states= st.selectbox("Select The State_Ty", tac_quarter["States"].unique())
            Aggre_Tran_Transaction_type(tac_quarter,states)


        elif method == "User Analysis":
          
            col1,col2 = st.columns(2) 

            with col1:  

                years= st.selectbox("Select The Year_Pu",Aggre_user["Years"].unique())
            Aggre_user_y=Aggre_user_plot_1(Aggre_user,years)

            col1,col2= st.columns(2)

            with col1:
               quarters= st.slider("Select The Quarter_o",Aggre_user_y["Quarter"].min(), Aggre_user_y["Quarter"].max(),
                            Aggre_user_y["Quarter"].min())
            Aggre_user_y_Q=Aggre_user_plot_2(Aggre_user_y, quarters)

            col1,col2 = st.columns(2)

            with col1:
                states= st.selectbox("Select The State_P", Aggre_user_y_Q["States"].unique())
            Aggre_user_plot_3(Aggre_user_y_Q,states)

    

    with tab2:
        method_2=st.radio("Select The Method",["Map Insurance","Map Transaction","Map User"])

        if method_2 == "Map Insurance":
            col1,col2 = st.columns(2) 
            with col1:  

                years= st.slider("Select The Years_PO",Map_insurance["Years"].min(), Map_insurance["Years"].max(),
                            Map_insurance["Years"].min(),)
            mca_y= map_insu_y(Map_insurance,years) 

            col1,col2 = st.columns(2)

            with col1:
                states= st.selectbox("Select The State_Pi", mca_y["States"].unique())
            map_insur_dist(mca_y,states)

            col1,col2= st.columns(2)

            with col1:
               quarters= st.slider("Select The Quarter_o",mca_y["Quarter"].min(), mca_y["Quarter"].max(),
                            mca_y["Quarter"].min())
            maq=map_insura_quarter(mca_y, quarters)

            col1,col2 = st.columns(2)

            with col1:
                states= st.selectbox("Select The State_P", maq["States"].unique())
            map_insur_dist(maq,"West Bengal")



        elif method_2 == "Map Transaction":
            col1,col2 = st.columns(2) 
            with col1:  

                years= st.slider("Select The Years",Map_transaction["Years"].min(), Map_transaction["Years"].max(),
                            Map_transaction["Years"].min(),)
            map_transa_year=map_trans_y(Map_transaction,2018)

            col1,col2 = st.columns(2)
            with col1:

                states= st.selectbox("Select The states", map_transa_year["States"].unique())
            map_trans_dist(map_transa_year,states)

            with col1:
               quarters= st.slider("Select The Quarter_P",map_transa_year["Quarter"].min(), map_transa_year["Quarter"].max(),
                            map_transa_year["Quarter"].min())
            map_transa_quarter=map_trans_quarter(map_transa_year,quarters)

            col1,col2 = st.columns(2)

            with col1:
                states= st.selectbox("Select The State", map_transa_quarter["States"].unique())
            map_trans_dist(map_transa_quarter,states)

        elif method_2 == "Map User":
         
            col1,col2 = st.columns(2)  
            with col1:  

                years= st.slider("Select The Years",Map_user["Years"].min(), Map_user["Years"].max(),
                            Map_user["Years"].min(),)
                Map_user_year=map_user_plot_1(Map_user,years)

            col1,col2 = st.columns(2)  
            with col1:  
            
                quarters= st.slider("Select The Quarter",Map_user_year["Quarter"].min(), Map_user_year["Quarter"].max(),
                                Map_user_year["Quarter"].min(),)
                Map_user_year_quar=map_user_plot_2(Map_user_year,quarters)

            col1,col2 = st.columns(2)

            with col1:
                states= st.selectbox("Select The State", Map_user_year_quar["States"].unique())
            map_user_plot_3(Map_user_year_quar,states)


    with tab3:
        method_3=st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])

        if method_3 == "Top Insurance":
            col1,col2 = st.columns(2) 
            with col1:  

                years= st.slider("Select The Years_IN",Top_insurance["Years"].min(), Top_insurance["Years"].max(),
                            Top_insurance["Years"].min(),)
            top_insu_year=top_insura_y(Top_insurance,years)

            col1,col2 = st.columns(2)

            with col1:
                states= st.selectbox("Select The State_I", top_insu_year["States"].unique())
            top_ins_state(top_insu_year,states)

            col1,col2= st.columns(2)
            with col1:
               quarters= st.slider("Select The Quarter_ti",top_insu_year["Quarter"].min(), top_insu_year["Quarter"].max(),
                            top_insu_year["Quarter"].min(),)
            top_insu_y_q=top_insu_quarter(top_insu_year,quarters)


        elif method_3 == "Top Transaction":
            col1,col2 = st.columns(2) 
            with col1:  

                years= st.selectbox("Select The Years_IN",Top_transaction["Years"].unique())
            top_transa_year=top_trans_y(Top_transaction,years)

            col1,col2= st.columns(2)
            with col1:
               quarters= st.slider("Select The Quarter_ti",top_transa_year["Quarter"].min(), top_transa_year["Quarter"].max(),
                            top_transa_year["Quarter"].min(),)
            top_trans_quarter=top_transa_quarter(top_transa_year, quarters)

            col1,col2 = st.columns(2)

            with col1:
                states= st.selectbox("Select The State_tt", top_transa_year["States"].unique())
            top_transi_state(top_transa_year,states)
        
        

        elif method_3 == "Top User":
            col1,col2 = st.columns(2) 
            with col1:  

                years= st.slider("Select The Years_IN",Top_user["Years"].min(), Top_user["Years"].max(),
                            Top_user["Years"].min(),)
            top_user_year=top_user_y(Top_user,years)

            col1,col2 = st.columns(2)

            with col1:
                states= st.selectbox("Select The State_tt", top_user_year["States"].unique())
            top_trans_state(top_user_year,states)
        
elif select =="TOP CHARTS":
    question= st.selectbox("Select the Question",["1. Transaction amount and count of Aggregated Insurance",
                                                  "2. Transaction amount and count of Map Insurance",
                                                  "3. Transaction amount and count of Top Insurance",
                                                  "4. Transaction amount and count of Aggregated Transaction",
                                                  "5. Transaction amount and count of Map Transaction",
                                                  "6. Transaction amount and count of Top Transaction",
                                                  "7. Transaction count of Aggregated User",
                                                    ])

    if question == "1. Transaction amount and count of Aggregated Insurance":
                
                st.subheader("TRANSACTION AMMOUNT")
                top_chart_transaction_amount("aggregated_insurance")

                st.subheader("INSURANCE COUNT")
                top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction amount and count of Map Insurance":
                
                st.subheader("TRANSACTION AMMOUNT")
                top_chart_total_amount("map_insurance")

                st.subheader("INSURANCE COUNT")
                top_chart_user_count("map_insurance")

    elif question == "3. Transaction amount and count of Top Insurance":
        
                st.subheader("TRANSACTION AMMOUNT")   
                top_chart_total_amount("top_insurance")

                st.subheader("INSURANCE COUNT")
                top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction amount and count of Aggregated Transaction":
                
                st.subheader("TRANSACTION AMMOUNT")   
                top_chart_trans_amount("aggregated_transaction")

                st.subheader("INSURANCE COUNT")
                top_chart_trans_count("aggregated_transaction")

    elif question == "5. Transaction amount and count of Map Transaction":
                
                st.subheader("TRANSACTION AMMOUNT")   
                top_chart_trans_amount("map_transaction")

                st.subheader("INSURANCE COUNT")
                top_chart_trans_count("map_transaction")
    
    elif question == "6. Transaction amount and count of Top Transaction":
                
                st.subheader("TRANSACTION AMMOUNT")   
                top_chart_transact_amount("top_transaction")

                st.subheader("INSURANCE COUNT")
                top_chart_transacti_count("top_transaction")

    elif question == "7. Transaction count of Aggregated User":

                st.subheader("INSURANCE COUNT")
                top_chart_trans_count("aggregated_user")





