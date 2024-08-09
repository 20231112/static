from flask import Flask, render_template, request
import os
import pyodbc
import pandas as pd

app = Flask(__name__)

# DB接続
connection = (
    "Driver={ODBC Driver 18 for SQL Server};Server=tcp:dkato.database.windows.net,1433;"+
    f"Database=mydb;Uid=dkato;Pwd=SQLServer1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)
table="questionnaire"

def insert(string):
    with pyodbc.connect(connection).cursor() as cursor:
        cursor.execute(
            f"""
            INSERT INTO {table} (sex)
            VALUES (?)
            """,
            string
        )

def get_res():
    with pyodbc.connect(connection) as conn:
        df = pd.io.sql.read_sql(fr'select * from {table}', conn)
    return sum(df.sex=="male"), sum(df.sex=="female"), sum(df.sex=="other")
        
@app.route('/', methods=['GET', 'POST'])
def index():

    sex = request.form.get('sex')

    insert(sex)
    male, female, other=get_res()
    return render_template('form.html', male=male, female=female, other=other)



if __name__ == '__main__':
    app.run()