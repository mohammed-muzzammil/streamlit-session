import streamlit as st
import pandas as pd
import base64
import xlrd
import xlsxwriter
import cx_Oracle

import os
from io import BytesIO

# Enter the path here where all the temporary files will be stored
temp='\\temp.csv'
#os.chdir(r'C:\Users\MOHAMMED MUZZAMMIL\Desktop\streamlit')
path=os.getcwd()
path=path+temp
#path=(r"C:\Users\MOHAMMED MUZZAMMIL\Desktop\streamlit\temp.csv")


st.write("Hello")

st.sidebar.write("Sidebar")

st.write("Data import")

file_option = [".CSv",".Xlsx","Jpg","Oracle"]

file_select = st.sidebar.radio("Please select a file type",file_option)


def upload_xlsx(uploaded_file):
    
    try:
        
    
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            st.dataframe(df)
            df.to_csv(path, index=False)
            return df
    
    except Exception as e:
        st.write("Oops!", e.__class__, "occurred.")
        return df

def upload_csv(uploaded_file):
    
    try:
        
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
            df.to_csv(path, index=False)
            return df

    
    except Exception as e:
        st.write("Oops!", e.__class__, "occurred.")
        return df



if file_select == ".CSv":
    
    file = st.file_uploader("Please select file",type = "csv")
    

    if file:

        if st.button('Upload File'):
            df=upload_csv(file)


if file_select == ".Xlsx":
    
    file = st.file_uploader("Please select file",type = "xlsx")
    

    if file:

        if st.button('Upload File'):
            df = upload_xlsx(file)
            
            
if file_select == "Jpg":
    
    file = st.file_uploader("Please Select", type = "jpg")
    if file:
        if st.button('Upload'):
            img = file.read()
            st.image(img)
            
            

if file_select == "Oracle":
    
    
    st.info("Enter Oracle Database information")

    user=st.text_input("Enter User name ")
    passwd=st.text_input("Enter Password ", type="password")
    host=st.text_input("Enter Host Address")
    port=st.text_input("Enter Port number")
    query =st.text_input("Enter the query for the desired data")


    if st.button("Connect"):
        

        #muzzammil/123@localhost:99/ORCL


        con_query="{}/{}@{}:{}/ORCL".format(user,passwd,host,port)

        con=cx_Oracle.connect(con_query)

        if con!=None:
            st.info("Connection Established Successfully")
            df = pd.read_sql(query,con)
            st.dataframe(df)
            df.to_csv(path, index=False)
            #return df


            #query =st.text_input("Fire the query for the desired data")
            #if st.button("Fire"):
             #   df = pd.read_sql(query,state.con)
              #  st.dataframe(df)
               # df.to_csv(r'C:\Users\MOHAMMED MUZZAMMIL\Desktop\streamlit\temp.csv', index=False)
                #return df





li = ["mean","median","mode"]            
m = st.sidebar.radio("please choose ",li)


def mean():
    df=pd.read_csv(path)
    clean_df=(df.fillna(df.mean()))
    st.dataframe(clean_df)
    clean_df.to_csv(path)
    



def data_export():
    
    st.sidebar.write("Data Export")
    
    export_list = ["Xlsx","Csv","Oracle"]
    
    export_select = st.sidebar.radio("Please select a export type",export_list)
    
    if export_select == "Csv":
        if st.sidebar.button("Download csv"):
            df=pd.read_csv(path)
            st.sidebar.markdown(get_table_download_link_csv(df), unsafe_allow_html=True)
            
    if export_select=="Xlsx":
        if st.sidebar.button("Download Xlsx"):
            df=pd.read_csv(path)
            st.sidebar.markdown(get_table_download_link_xlsx(df), unsafe_allow_html=True)
            
            
    if export_select == "Oracle":
        
        
        
        st.info("Enter Oracle Database information")

        users=st.text_input("Enter Users name ")
        passwd=st.text_input("Enter Password ", type="password")
        host=st.text_input("Enter Host Address")
        port=st.text_input("Enter Port number")
        table=st.text_input("Enter the name of table to create, if table exist it'll be replaced")
        if st.button("Connect"):
            df = pd.read_csv(path)
            conn = create_engine('oracle+cx_oracle://{}:{}@{}:{}/ORCL'.format(users,passwd,host,port))
            df.to_sql('{}'.format(table), conn, if_exists='replace')
            #con_query="{}/{}@{}:{}/ORCL".format(user,passwd,host,port)
            #con=cx_Oracle.connect(con_query)
            if conn!=None:
                st.info("Connection Established Successfully and Table Inserted")



            
    
def get_table_download_link_csv(df):
    try:
        
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframes
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(
            csv.encode()
        ).decode()  # some strings <-> bytes conversions necessary here
        return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'
    
    except Exception as e:
        st.write("Oops!", e.__class__, "occurred.")
        return df
    

def to_excel(df):
    try:
        
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer)
        writer.save()
        processed_data = output.getvalue()
        return processed_data
    
    
    except Exception as e:
        st.write("Oops!", e.__class__, "occurred.")
        return df



def get_table_download_link_xlsx(df):
    try:
        
        
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        val = to_excel(df)
        b64 = base64.b64encode(val)  # val looks like b'...'
        return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="dataprep.xlsx">Download xlsx file</a>' # decode b'abc' => abc
    

    
    
    
    
    
    except Exception as e:
        st.write("Oops!", e.__class__, "occurred.")
        return df


    


            
data_export()           
            
            


