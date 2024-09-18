import streamlit as st
import pandas as pd
from datetime import datetime
import time
dff= pd.read_csv("table.csv")
dff.set_index("Players",inplace=True)
dff.sort_values(["Ratings","Won","APD"],inplace=True,ascending = False)
hq = pd.read_csv("head.csv")
hq.set_index("Players",inplace=True)
with st.spinner(st.image("logo.gif")):
    time.sleep(5)
#st.title("Badminton Boys:badminton_racquet_and_shuttlecock:")
st.divider()
st.subheader("Table :sports_medal:")
st.write(dff)
##recent matches
st.subheader("Recent Matches :fire:")
mat = st.columns(6)
with open("recent.txt","r") as f1:
    for i in range(6):
        mat[i] = mat[i].container(border=True)
        mat[i].caption(f1.readline())
        for j in range(2):
            mat[i].write(f1.readline())
##Ratings chart
st.subheader("Ratings")
st.bar_chart(dff) 
#st.bar_chart(dff,y=dff["Won"]/dff["Played"],color=['#0390fc'])
st.subheader("Update Values")
## update table
p = st.columns(2)
PLY = []
with open("PLAYERS.txt","r") as f1:
    lines = f1.readlines()
    for line in lines:
        PLY.append(line.strip())
PLAYERS = tuple(PLY)
p1 = p[0].selectbox("Select player1 name",PLAYERS)
p2 = p[1].selectbox("Select player2 name",PLAYERS)
s1 = p[0].number_input(p1+"'s score",min_value=0,max_value=30,key=1)
s2 = p[1].number_input(p2+"'s score",min_value=0,max_value=30,key=2)
pswd = st.number_input("Enter 4 digit pin",min_value=0,max_value=9999)
if st.button("Update",type="primary"):
    if pswd==st.secrets.pin:
        if p1==p2:
            st.info("Playing against the wall is not counted XD")
        else:    
            st.info("Updated Successfully")
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
                hq.loc[p1,p2]+=1
                hq.loc[p1,"Won"]+=1
            elif s2>s1:
                dff.loc[p2,"APD"]= (dff.loc[p2,"Played"]*dff.loc[p2,"APD"]+diff)/(dff.loc[p2,"Played"]+1)
                dff.loc[p1,"APD"]= (dff.loc[p1,"Played"]*dff.loc[p1,"APD"]-diff)/(dff.loc[p1,"Played"]+1)
                dff.loc[p2,"Won"]+=1
                dff.loc[p1,"Lost"]+=1
                dff.loc[p1,"Ratings"]-=(32*E1)
                dff.loc[p2,"Ratings"]+=(32*E1)
                hq.loc[p2,p1]+=1
                hq.loc[p2,"Won"]+=1
            dff.loc[p1,"Played"]+=1
            dff.loc[p2,"Played"]+=1
            dff.sort_values(["Ratings","Won","APD"],inplace=True,ascending = False)
            hq.to_csv("head.csv",index=True)
            dff.to_csv("table.csv",index=True)
            with open("recent.txt","r") as f1:
                lines = f1.read()
                ptr = 4
                with open("recent.txt","w") as f2:
                    now = datetime.today()
                    f2.write(now.strftime("%d")+"/"+now.strftime("%m")+"/"+now.strftime("%Y")+now.strftime(" %H:%M")+"\n")
                    f2.write(str(p1)+"-"+str(s1)+"\n")
                    f2.write(str(p2)+"-"+str(s2)+"\n")
                    for line in lines:
                        if ptr<=18:
                            f2.write(line)
                        else:
                            break
            st.rerun()
    else:
        st.image("wait-a-minute-who-are-you.gif")
st.subheader("New Player")
name = st.text_input("Enter player name")
ssc = st.number_input("Enter security pin",min_value=0,max_value=10000)
if st.button("Add",type="secondary") and ssc==st.secrets["pin"]:
    dat = {
        'Players': [name],
        'Played':[0],
        'Won':[0],
        'Lost':[0],
        'APD':[0],
        'Ratings':[1000]
    }
    np =  pd.DataFrame(dat)
    np.to_csv("table.csv",mode='a',index=False,header=False)
    with open("PLAYERS.txt","a") as f1:
        f1.write("\n"+name)
    st.info("New player added Successfully")
st.title("Head to Head :vs:")
st.write(hq)
