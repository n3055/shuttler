import streamlit as st
import pandas as pd
dff= pd.read_csv("table.csv")
dff.set_index("Players",inplace=True)
st.title("Badminton Boys:badminton_racquet_and_shuttlecock::badminton_racquet_and_shuttlecock::badminton_racquet_and_shuttlecock:")
st.divider()
st.subheader("Table")
st.write(dff)
st.subheader("Recent Matches")
one,two,three,four,five,six = st.columns(6)
one = one.container(border=True)
two = two.container(border=True)
three = three.container(border=True)
four = four.container(border=True)
five = five.container(border=True)
six = six.container(border=True)
#one.title("Match-1")
one.caption("18/08/2024")
two.caption("18/08/2024")
three.caption("18/08/2024")
four.caption("18/08/2024")
five.caption("18/08/2024")
six.caption("18/08/2024")
one.write("Sameer-21")
one.write("Rishi-14")
two.write("Deepak-15")
two.write("Harsha-21")
three.write("Deepak-21")
three.write("Rishi-9")
four.write("Sameer-21")
four.write("Harsha-16")
five.write("Sameer-13")
five.write("Deepak-21")
six.write("Harsha-21")
six.write("Rishi-14")
st.subheader("Ratings")
st.bar_chart(dff,y="Ratings",color=['#f58b27']) 
st.subheader("Update Values")
## update table
p1 = st.text_input("Enter player1 name")
p2 = st.text_input("Enter player2 name")
s1 = st.number_input("Player1's score,",min_value=0,max_value=30)
s2 = st.number_input("Player2's score",min_value=0,max_value=30)
pswd = st.number_input("Enter 4 digit pin",min_value=0,max_value=9999)
if st.button("Update",type="primary"):
    E1 = 1/(1+(pow(10,(float(dff.loc[p2,"Ratings"])-float(dff.loc[p1,"Ratings"]))/400)))
    round(E1,2)
    E2 = 1-E1
    diff = abs(s1-s2)
    if s1>s2:
        dff.loc[p1,"APD"]= (dff.loc[p1,"Played"]*dff.loc[p1,"APD"]+diff)/(dff.loc[p1,"Played"]+1)
        dff.loc[p2,"APD"]= (dff.loc[p2,"Played"]*dff.loc[p2,"APD"]-diff)/(dff.loc[p2,"Played"]+1)
        dff.loc[p1,"Won"]+=1
        dff.loc[p2,"Lost"]+=1
        dff.loc[p1,"Ratings"]+=(32*E2)
        dff.loc[p2,"Ratings"]-=32*E2
    elif s2>s1:
        dff.loc[p2,"APD"]= (dff.loc[p2,"Played"]*dff.loc[p2,"APD"]+diff)/(dff.loc[p2,"Played"]+1)
        dff.loc[p1,"APD"]= (dff.loc[p1,"Played"]*dff.loc[p1,"APD"]-diff)/(dff.loc[p1,"Played"]+1)
        dff.loc[p2,"Won"]+=1
        dff.loc[p1,"Lost"]+=1
        dff.loc[p1,"Ratings"]-=(32*E1)
        dff.loc[p2,"Ratings"]+=(32*E1)
    dff.loc[p1,"Played"]-=1
    dff.loc[p2,"Played"]-=1
    dff.sort_values(["Ratings","Won","APD"],inplace=True,ascending = False)
    if pswd==1000:
        dff.to_csv("table.csv",index=True)