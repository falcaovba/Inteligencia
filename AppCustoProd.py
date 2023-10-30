import pandas as pd
import streamlit as st
import altair as alt
import time as time
import datetime as datetime
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy import select
import pyodbc
from PIL import Image
import openpyxl


## Conexão com banco de dados ##
def load_data():
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

    SELECT EMPRESA, VDACOD, PNESEQ, EPRCOD1, EPRDESCRICAO1, EPRCOD2, EPRDESCRICAO2, PneBanQtde, PNEBANCVR, PneBanCusto, VLRCUSBAN, EPRCOD3, EPRDESCRICAO3, PneLigCusto, PneLigCVR, VLRCUSLIG
    FROM DbDafonte.dbo.VW_CUSTO_RECAPAGEM_BAN_APLI
    where VDACOD = 24131
    AND PNESEQ = 1
    AND EMPRESA = 14

                  '''
    ## Conversão em DataFrame ##
    df = pd.read_sql(sql=consulta_sql, con=engine)
    return df


## Carregamento do DataFrame
df_Prod = load_data()


def load_data2():
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

        SELECT EMPRESA, VdaCod, PneSeq, EPRCOD, EPRDESCRICAO, PneMatQtde, PneMatVlr, VLTTOTAL
        FROM DbDafonte.dbo.VW_CUSTO_RECAPAGEM_MAT_APLI
        WHERE VdaCod = 24131
        AND PneSeq = 1
        AND EMPRESA = 14

                  '''
    ## Conversão em DataFrame ##
    df2 = pd.read_sql(sql=consulta_sql, con=engine)
    return df2


## Carregamento do DataFrame
df_insumo = load_data2()

## Configuração da Página
st.set_page_config(
    page_title="Custo de Produção",
    page_icon=" 💡 ",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://api.whatsapp.com/send?phone=5581997518612',
        'Report a bug': "https://api.whatsapp.com/send?phone=5581997518612",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
