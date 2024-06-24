import os
import streamlit as st
import pandas as pd
import dotenv
from dotenv import load_dotenv

from pandasai import Agent
from pandasai.llm.openai import OpenAI
from deep_translator import GoogleTranslator
import matplotlib

matplotlib.use('Agg')


dotenv.load_dotenv(dotenv.find_dotenv())
openai_api_key = st.secrets["OPENAI_API_KEY"]

#openai_api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI(api_token=openai_api_key)


def extract_transform_data():
    df_pessoas = pd.read_csv('df_pessoas.csv')
    df_devedores = pd.read_csv('df_segmentacao_devedores.csv')
    df_final = df_devedores.merge(df_pessoas[['Idade', 'cpf', 'Gênero', 'Bairro PF',
                                           'Cidade PF', 'Bairro PF(2)', 'Cidade PF(2)']],
                                             left_on='documento', right_on='cpf', how='left')
    df_final = df_final.drop(columns=['cpf', 'documento'])
    df_final = df_final[['_id', 'numero_contribuinte', 'nome', 'Montante financeiro', 'Quantidade de débitos', 'Volume financeiro', 'Volume de débitos', 'Bairro PJ',
                         'Cidade PJ', 'tem_divida_pgfn', 'valor_total_divida_pgfn', 'Idade', 'Gênero', 'Bairro PF', 'Cidade PF', 'Bairro PF(2)', 'Cidade PF(2)', 'Prioridade']]


    return df_final

df = extract_transform_data()

st.set_page_config(page_title="App Talk to Data", page_icon=":game_die:", layout="wide")
logo_path = "./logo_inovally.png"
link_inovally = "https://inovally.com.br/"
st.logo("./logo_inovally.png", link=link_inovally)


st.title("App Talk to Data 💬🎲")
st.subheader("🦜🔗 Use o poder da IA Generativa para descobrir insights sobre os devedores!")
st.image("./image.png")


dados = Agent(df, config={"llm": llm, "enable_cache": False})


st.dataframe(df)


st.subheader("No espaço abaixo, escreva o que você gostaria de ver nos dados 👇")
texto_usuario = st.text_area("Ex: qual é o nome com a maior idade? Me mostre um gráfico de linhas com a quantidade de nomes por idade")
texto_usuario = texto_usuario + ', responda em português'
texto_usuario_traduzido = GoogleTranslator(source='auto', target='en').translate(texto_usuario)
texto_usuario_traduzido = texto_usuario_traduzido.replace('\u200b\u200b', '')


if st.button("Gerar resultado"):
    if texto_usuario_traduzido:
        with st.spinner("Gerando resultado..."):
            answer = dados.chat(texto_usuario_traduzido)
            st.success(answer)

            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
    else:
        st.warning("Por favor, informe o que você quer ver nos dados.")
    


