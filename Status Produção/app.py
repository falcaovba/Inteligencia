
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
    
                SELECT
                LOJA as Loja,
                LEFT(DATAENTRADAPROD,3) as Mes,
                CONVERT(varchar, PV) as PV, 
                CONVERT(varchar, COLETA) as Coleta,
                CASE
                	when Trim(SUBSTRING(DESCRMEDIDA, 1, CHARINDEX(' ', DESCRMEDIDA)-1)) = 'REC.' THEN 'RECAPAGEM'
                	WHEN Trim(SUBSTRING(DESCRMEDIDA, 1, CHARINDEX(' ', DESCRMEDIDA)-1)) = 'VULC.' THEN 'VULCANIZAÇÃO'
                	ELSE Trim(SUBSTRING(DESCRMEDIDA, 1, CHARINDEX(' ', DESCRMEDIDA)-1))
                END as TipoServiço,
                DESCRMEDIDA as Serviço,
                CLIENTE as Cliente,
                SEQUENCIA as Pneu,
                --ROW_NUMBER() OVER(PARTITION BY COLETA ORDER BY DATAENTRADAPROD ASC) AS Ordem,
                LOCALIZACAO as Esteira,
                MIN(DATAENTRADAPROD) OVER(PARTITION BY COLETA) AS Entrada, 
                MAX(DATAENTRADAPROD) OVER(PARTITION BY COLETA) AS Saída,
                DATEDIFF(hour,Min(DATAENTRADAPROD) OVER(PARTITION BY COLETA),Max(DATAENTRADAPROD) OVER(PARTITION BY COLETA)) as SLA,
                LIBERACAO AS Liberaçao,
                PLANOPAGT as PlanoPgto,
                PRIORIDADE as Prioridade,
                VENDEDOR as Vendedor
                --CPFCNPJ
                FROM DbDafonte.dbo.VW_KPI_VISAO_PNEU_LOCALIZACAO
                where YEAR (CONVERT(date, DATAENTRADAPROD, 101)) = YEAR(GETDATE())
                AND CLIENTE NOT LIKE '%DAFONTE - LOJA%'
    
                  '''
    ## Conversão em DataFrame ##
    df = pd.read_sql(sql=consulta_sql, con=engine)
    return df

## Carregamento do DataFrame
df = load_data()

#baixar_aquivo = df.to_excel('LinhaDeProdução.xlsx', sheet_name='Produção', engine='openpyxl', index=False)




#logo_teste = Image.open('C:/Inteligencia/imagens/LogoDafonte.jpg')
#st.image(logo_teste, width=200)

## Configuração da Página
st.set_page_config(
    page_title="Status Produção",
    page_icon="🪛",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

tab1, tab2 = st.tabs(["Esteira Produção","Coleta"])

# Primeira Página
with tab1:
    ## Logo e Cabeçalho
    #logo_teste = Image.open('C:/Inteligencia/imagens/LogoDafonte.jpg')
    #st.image(
    #    logo_teste,
    #    width=150
    #)
    st.header(
        ':blue[Status linha de Produção] :screwdriver:',
        divider='blue'
    )


    # Tipo de Filtros
    with st.sidebar:
        st.subheader(
            'Filtros 🔍',
            divider='blue'
        )
        floja = st.selectbox(
            ":classical_building: Selecione a Loja:",
            options=[1, 3, 4, 6, 7, 13, 14, 15, 16, 19]
        )
        st.markdown("---")
        fmes = st.selectbox(
            ':date: Selecione o Mês:',
            options=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        )
        st.markdown("---")
        fcoleta = st.number_input(
            ":memo: Inserir a Coleta",
            value=0,
            placeholder="Digite a coleta..."
        )
        st.markdown("---")
        freforma = st.selectbox(
            ':spiral_note_pad: Selecione a Reforma:',
            options=['RECAPAGEM', 'RECAUCHUTAGEM', 'VULCANIZAÇÃO']
        )
        st.markdown("---")
        fstatus = st.selectbox(
            ":screwdriver: Selecione o status",
            options=df['Esteira'].unique(),
            index=None,
            placeholder="Select contact method...",
        )
        st.markdown("---")


    ## Fitro Coleta
    if fcoleta > 0:
        df = df.loc[(df['Loja'] == floja) & (df['Mes'] == fmes) & (df['Coleta'] == fcoleta) & (df['TipoServiço'] == freforma)]
    elif fcoleta == 0:
        df = df.loc[(df['Loja'] == floja) & (df['Mes'] == fmes) & (df['TipoServiço'] == freforma)]

    ## Filtro Status
    if fstatus == None:
        if fcoleta > 0:
            df = df.loc[(df['Loja'] == floja) & (df['Mes'] == fmes) & (df['Coleta'] == fcoleta) & (df['TipoServiço'] == freforma)]
        elif fcoleta == 0:
            df = df.loc[(df['Loja'] == floja) & (df['Mes'] == fmes) & (df['TipoServiço'] == freforma)]
    else:
        df = df.loc[(df['Loja'] == floja) & (df['Mes'] == fmes) & (df['Esteira'] == fstatus) & (df['TipoServiço'] == freforma)]


    ## Cards
    if fstatus == None:
        col1, col2, col3 = st.columns(3)
        col1.metric("Pneus", df['Cliente'].count())
        col2.metric("Loja", floja)
        col3.metric("Mês", fmes)
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Pneus", df['Cliente'].count())
        col2.metric("Loja", floja)
        col3.metric("Mês", fmes)
        col4.metric("Status", fstatus)

    ## Linha divisória
    st.header('',divider='blue')

    ## Tabela
    st.dataframe(
        df,
        use_container_width=True,
        width=600,
        hide_index=True,
        column_config={
            "widgets": st.column_config.Column(
                width="medium"
            )
        }
    )

    st.markdown("---")

    ## Butão de download
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="📥 Download do aquivo em CSV",
        data=csv,
        file_name='sample_df.csv')

# Segunda página
    with tab2:
        st.header("Em desenvolvimento 👷🏼")

