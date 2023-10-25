
import pandas as pd
import streamlit as st
import altair as alt
import time as time
import datetime as datetime
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy import select
import pyodbc


## Conexão com banco de dados ##

# String de conexão
connection_url = URL.create(
    "mssql+pyodbc",
    username="dafonte",
    password="@d123",
    host="10.0.1.5",
    database="DBDafonte",
    query={
        "driver": "SQL Server",
        "LongAsMax": "Yes",
    },
)

## Engenharia de conexão ##
engine = create_engine(
    connection_url
    )

## Query banco ##
consulta_sql = '''

            SELECT 
            LOJA as Loja,
            TRIM(MEDIDA) AS Medida,
            EPRCOD as Cod, 
            TRIM(EPRDESCRICAO) as Pneus,
            TRIM(ESGDESCR) as Familia,
            TRIM(FABRICANTE) as Marca,
            EPRSALDO as Estoque,
            EPRREFCUST as CustoRef,
            EPRMEDCUST as CustoMéd,
            VLRVENDA1 AS PrecoVenda,
            CASE 	
                when EPRREFCUST = 0 or VLRVENDA1 = 0 then 0
                else round((VLRVENDA1-EPRREFCUST)/VLRVENDA1,4) 
            END as MGB,
            EPRULT_AQUIS as DataEntrada, 
            EPRULT_SAIDA as DataSaída,
            CASE 
                WHEN EPRULT_SAIDA IS NULL THEN DATEDIFF(DAY , EPRULT_AQUIS, GETDATE())
                ELSE DATEDIFF(DAY , EPRULT_SAIDA, GETDATE())
            END AS DiasSemSaída
            FROM DbDafonte.dbo.VW_ESTOQUE_SALDO
            WHERE EGRDES = 'PNEUS NOVOS'

              '''
## Conversão em DataFrame ##
df = pd.read_sql(sql=consulta_sql, con=engine)

df2 = pd.DataFrame(df,columns=['Loja','Medida','Cod','Pneus','Familia','Marca','Estoque','CustoRef','PrecoVenda'])

df2['1']  = df2.loc[(df2['Loja'] == 'LOJA_01')]['Estoque'].sum()
df2['5']  = df2.loc[(df2['Loja'] == 'LOJA_05')]['Estoque'].sum()
df2['6']  = df2.loc[(df2['Loja'] == 'LOJA_06')]['Estoque'].sum()
df2['17']  = df2.loc[(df2['Loja'] == 'LOJA_17')]['Estoque'].sum()
df2['4']  = df2.loc[(df2['Loja'] == 'LOJA_04')]['Estoque'].sum()
df2['19']  = df2.loc[(df2['Loja'] == 'LOJA_19')]['Estoque'].sum()
df2['2']  = df2.loc[(df2['Loja'] == 'LOJA_02')]['Estoque'].sum()
df2['9']  = df2.loc[(df2['Loja'] == 'LOJA_09')]['Estoque'].sum()
df2['16']  = df2.loc[(df2['Loja'] == 'LOJA_16')]['Estoque'].sum()
df2['3']  = df2.loc[(df2['Loja'] == 'LOJA_03')]['Estoque'].sum()
df2['7']  = df2.loc[(df2['Loja'] == 'LOJA_07')]['Estoque'].sum()
df2['8']  = df2.loc[(df2['Loja'] == 'LOJA_08')]['Estoque'].sum()
df2['20']  = df2.loc[(df2['Loja'] == 'LOJA_20')]['Estoque'].sum()
df2['13']  = df2.loc[(df2['Loja'] == 'LOJA_13')]['Estoque'].sum()
df2['15']  = df2.loc[(df2['Loja'] == 'LOJA_15')]['Estoque'].sum()
df2['14']  = df2.loc[(df2['Loja'] == 'LOJA_14')]['Estoque'].sum()



st.header('Posição Estoque Pneus"', divider='rainbow')
