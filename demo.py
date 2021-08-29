import streamlit as st
import pandas as pd
import os
import cx_Oracle
from io import BytesIO
import base64

temp='\\temp.csv'

path=os.getcwd()
path=path+temp

st.title("Demo Application")


def to_excel(df):
        
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer)
    writer.save()
    processed_data = output.getvalue()
    return processed_data





# All Functions
def mvt_mean(df):
    
    clean_df=(df.fillna(df.mean()))
    clean_df.fillna(clean_df.select_dtypes(include='object').mode().iloc[0], inplace=True)
    st.dataframe(clean_df)
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
    

    
def upload_xlsx(uploaded_file):
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)
        df.to_csv(path, index=False)
        return df

    
    
def get_table_download_link_xlsx(df):
        

    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="download.xlsx">Download xlsx file</a>' # decode b'abc' => abc
    
        
        
    
def get_table_download_link_csv(df):
        
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframes
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="download.csv">Download csv file</a>'

    





# File Upload 
def file_upload():

        st.sidebar.header("Data Import")                               
        f_option=('.Xlsx','.Csv','Oracle', 'jpg')
        f_select=st.sidebar.radio('Choose a file type',f_option)

        if f_select == '.Xlsx':
            uploaded_file = st.sidebar.file_uploader("Choose a file", type="xlsx")
            if uploaded_file:
                if st.sidebar.button('Upload File'):
                    df=upload_xlsx(uploaded_file)

        elif f_select == ".Csv":
            uploaded_file = st.sidebar.file_uploader("Choose a file ", type="csv")
            if uploaded_file:
                if st.sidebar.button("Upload csv file"):
                    df = upload_csv(uploaded_file)
                    
        elif f_select == "jpg":
             
            file = st.file_uploader("Please Select", type = "jpg")
            if file:
                if st.button('Upload'):
                    img = file.read()
                    st.image(img)


        elif f_select == "Oracle":

            st.info("Enter Oracle Database information")

            user=st.text_input("Enter User name ")
            passwd=st.text_input("Enter Password ", type="password")
            host=st.text_input("Enter Host Address")
            port=st.text_input("Enter Port number")
            query =st.text_input("Enter the query for the desired data")


            if st.button("Connect"):

               # muzzammil/123@46:99/ORCL


                con_query="{}/{}@{}:{}/ORCL".format(user,passwd,host,port)

                con=cx_Oracle.connect(con_query)

                if con!=None:
                    st.info("Connection Established Successfully")
                    df = pd.read_sql(query,con)
                    st.dataframe(df)
                    df.to_csv(path, index=False)

            
# Processing Data
def missing_value_treatment():

        st.sidebar.header("Missing value Treatment")
        missing_value_option = ["mean","median","mode"]
        missing_value = st.sidebar.radio("Choose a method", missing_value_option)

        if missing_value == "mean":
            if st.sidebar.button("Process mean"):
                df = pd.read_csv("temp.csv")
                df = mvt_mean(df)
                df.to_csv(path)

        

# Data Export

def data_export():

    st.sidebar.header("Data Export")

    export_options = ["Xlsx", "Csv", "Oracle"]

    export_value = st.sidebar.radio("Choose an Option to Export", export_options)

    if export_value == "Xlsx":
        if st.sidebar.button("Download xlsx"):
            df = pd.read_csv(path)
            st.sidebar.markdown(get_table_download_link_xlsx(df), unsafe_allow_html=True)

    elif export_value == "Csv":
        if st.sidebar.button("Download Csv"):
            df = pd.read_csv(path)
            st.sidebar.markdown(get_table_download_link_csv(df), unsafe_allow_html = True)

    elif export_value == "Oracle":
        if st.sidebar.button("Export Oracle"):
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
                if conn!=None:
                    st.info("Connection Established Successfully and Table Inserted")

        

    
def main():
    file_upload()
    missing_value_treatment()
    data_export()

main()
        
        








    

