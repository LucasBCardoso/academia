import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import time


#page title
st.set_page_config(page_title="Treino dos Guris 4.1", page_icon="💪", initial_sidebar_state="collapsed")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            sidebar {visibility: hidden;}
            [data-testid="collapsedControl"] {
                display: none
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Autenticação =================================================================================================

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
treinos = conn.read(worksheet='treinos')
treinos = treinos.dropna(how="all")

cargas = conn.read(worksheet='cargas')
cargas = cargas.dropna(how="all")

df_treinos = pd.DataFrame(treinos) #(data[1:], columns=data[0])
df_cargas = pd.DataFrame(cargas) #(data[1:], columns=data[0])

#================================================================================================

#get current date
today = datetime.date.today()
hoje = today.strftime("%d/%m/%Y")
format = "%d/%m/%Y"
weekdays = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']
today = weekdays[today.weekday()] + ', ' + today.strftime(format)

#================================================================================================

ATLETAS = [
    'Lucas',
    'Bruno',
    'David',
]

TREINOS = [
    'PEITO',
    'COSTAS',
    'BÍCEPS',
    'TRÍCEPS',
    'OMBROS',
    'PERNAS',
    'AEROBICO',
]

EXERCICIOS_PEITO = [
    'SUPINO RETO',
    'SUPINO INCLINADO',
    'CROSSOVER',
    'CRUCIFIXO',
    'VOADOR',
]

EXERCICIOS_TRICEPS = [
    'PULLEY CORDA',
    'PULLEY INVERTIDO',
    'PULLEY BARRA RETA',
    'COICE',
    'TRICEPS TESTA',
    'TRICEPS BANCO',
    'TRICEPS POLIA',
]

EXERCICIOS_PERNAS = [
    'LEG PRESS',
    'AGACHAMENTO HACK',
    'FLEXORA',
    'EXTENSORA',
    'PANTURRILHA',
    'ADUTOR',
    'ABDUTOR',
    'AGACHAMENTO LIVRE',
    'SUMO',
    'AFUNDO',
    'STIFF',

]

EXERCICIOS_OMBROS = [
    'DESENVOLVIMENTO MAQUINA',
    'ELEVAÇÃO FRONTAL',
    'ELEVAÇÃO LATERAL',
    'REMADA ALTA',
    'ARNOLD PRESS',
    'ENCOLHIMENTO',
]

EXERCICIOS_COSTAS = [
    'PUXADA ALTA',
    'REMADA BAIXA',
    'SERROTE',
    'CAVALO',
    'REMADA CURVADA',
]

EXERCICIOS_BICEPS = [
    'ROSCA DIRETA',
    'ROSCA ALTERNADA',
    'ROSCA SCOTT',
    'ROSCA MARTELO',
    'POLIA',
]

# EXERCICIOS_ABDOMEM = [
#     'ABDOMINAL',
#     'PRANCHA',
#     'ABDOMINAL MAQUINA',
# ]

EXERCICIOS_AEROBICO = [
    'SIT UP',
    'REMADOR',
    'KNEE UP',
    'ABDOMINAL ALTERNADO',
]

#================================================================================================

# def mostrar_exercicios(treino, atleta):
#     if treino is not None:
#         st.write(f"Confira as cargas atuais para o treino de: {treino}")

#         # cargas = conn.read(worksheet='cargas')
#         # cargas = cargas.dropna(how="all")
#         # df_cargas = pd.DataFrame(cargas)
        
#         # Determina a quantidade de exercícios conforme o treino selecionado
#         if treino == 'PEITO':
#             qtd_exercicios = len(EXERCICIOS_PEITO)
#         elif treino == 'TRÍCEPS':
#             qtd_exercicios = len(EXERCICIOS_TRICEPS)
#         elif treino == 'PERNAS':
#             qtd_exercicios = len(EXERCICIOS_PERNAS)
#         elif treino == 'OMBROS':
#             qtd_exercicios = len(EXERCICIOS_OMBROS)
#         elif treino == 'COSTAS':
#             qtd_exercicios = len(EXERCICIOS_COSTAS)
#         elif treino == 'BÍCEPS':
#             qtd_exercicios = len(EXERCICIOS_BICEPS)
#         # elif treino == 'ABDÔMEN':
#         #     qtd_exercicios = len(EXERCICIOS_ABDOMEM)
#         elif treino == 'AEROBICO':
#             qtd_exercicios = len(EXERCICIOS_AEROBICO)

#         # Filtra o DataFrame para o treino e atleta selecionados
#         ultimo_registro = df_cargas[(df_cargas['TREINO'] == treino) & (df_cargas['ATLETA'] == atleta)].iloc[-qtd_exercicios:]
        
#         # Exibe o registro mais recente
#         st.write(ultimo_registro)

#         # df_cargas = pd.DataFrame(conn.read(worksheet='cargas'))
#         # print('CARGAS ATUAIS:')
#         # print(df_cargas)
#         # print("=====================================")

#         exercicios = []
#         if treino == 'PEITO':
#             exercicios = EXERCICIOS_PEITO
#         elif treino == 'TRÍCEPS':
#             exercicios = EXERCICIOS_TRICEPS
#         elif treino == 'PERNAS':
#             exercicios = EXERCICIOS_PERNAS
#         elif treino == 'OMBROS':
#             exercicios = EXERCICIOS_OMBROS
#         elif treino == 'COSTAS':
#             exercicios = EXERCICIOS_COSTAS
#         elif treino == 'BÍCEPS':
#             exercicios = EXERCICIOS_BICEPS
#         # elif treino == 'ABDÔMEN':
#         #     exercicios = EXERCICIOS_ABDOMEM
#         elif treino == 'AEROBICO':
#             exercicios = EXERCICIOS_AEROBICO

#         # Collect all exercise data in a list of dictionaries
#         dados_de_carga_list = []

#         with st.form(key="train_form"):
#             for i, exercicio in enumerate(exercicios):
#                 col1, col2, col3 = st.columns([1, 1, 1])  # Adjust column sizes
#                 with col1:
#                     carga = st.number_input(f'Carga para {exercicio}', key=f'{treino.lower()}_{i}_carga', min_value=0, step=1, value=None, placeholder=0)
#                     if carga == None:
#                         carga = 0
#                 with col2:
#                     rodadas = st.number_input('Rodadas', key=f'{treino.lower()}_{i}_rodadas', min_value=0, step=1, value=None, placeholder=0)
#                     if rodadas == None:
#                         rodadas = 0
#                 with col3:
#                     repeticoes = st.number_input('Repetições', key=f'{treino.lower()}_{i}_repeticoes', min_value=0, step=1, value=None, placeholder=0)
#                     if repeticoes == None:
#                         repeticoes = 0
                
#                 #add blank space
#                 st.write(" ")
#                 st.write(" ")



#                 # Append input values for each exercise
#                 dados_de_carga_list.append({
#                     'ATLETA': atleta,
#                     'TREINO': treino,
#                     'EXERCICIO': exercicio,
#                     'CARGA': carga,
#                     'RODADAS': rodadas,
#                     'REPETICOES': repeticoes,
#                     'DATA': hoje
#                 })

#             # Convert list to DataFrame
#             dados_de_carga = pd.DataFrame(dados_de_carga_list)

#             if treino is not None:
#                 pass
#                 # cargas = conn.read(worksheet='cargas')
#                 # cargas = cargas.dropna(how="all")
#                 # new_loads = pd.DataFrame(cargas)
#                 # print(" ")
#                 # print('CARGAS ATUALIZADAS 2:')
#                 # print(new_loads)
#                 # print("=====================================")
#             else:
#                 st.write("Selecione um treino para visualizar os exercícios.")

#             # Botão para registrar o treino
#             submit_button = st.form_submit_button(label='Registrar treino')
#             if submit_button:
#                 #le os dados novamente
#                 # df_treinos = pd.DataFrame(conn.read(worksheet='treinos'))
#                 #df_cargas = pd.DataFrame(conn.read(worksheet='cargas'))
#                 # cargas = conn.read(worksheet='cargas')
#                 # cargas = cargas.dropna(how="all")
#                 # df_cargas = pd.DataFrame(cargas)
#                 # new_loads = pd.DataFrame(cargas)
#                 # print(" ")
#                 # print('CARGAS ATUALIZADAS:')
#                 # print(new_loads)
#                 # print("=====================================")


#                 # Adiciona novo treino
#                 # dados_do_treino = pd.DataFrame(
#                 #     [{
#                 #         'ATLETA': atleta,
#                 #         'TREINO': ', '.join(teste),  # Convert treino list to string
#                 #         'DATA': hoje,
#                 #     }]
#                 # )

#                 # # Atualiza a aba de treinos (adicione apenas uma nova linha)
#                 # updated_df_treinos = pd.concat([df_treinos, dados_do_treino], ignore_index=True)
#                 # conn.update(worksheet='treinos', data=updated_df_treinos)

#                 # Atualiza a aba de cargas (adicione apenas as novas linhas)
#                 updated_df_cargas = pd.concat([df_cargas, dados_de_carga], ignore_index=True)
#                 conn.update(worksheet='cargas', data=updated_df_cargas)

#                 # print("MUDOU")
#                 # print(df_cargas)
#                 # print("NOVO")
#                 # print(updated_df_cargas)

#                 st.success('Treino registrado com sucesso!')
#                 st.cache_data.clear()
#                 st.rerun() #reload page
                
#         #st.rerun()
#     else:
#         pass

# #================================================================================================

#st.title('Treino dos Guris 💪')
#make the title be upwards of the page
st.markdown("<h1 style='text-align: center; color: white;'>Treino dos Guris 💪</h1>", unsafe_allow_html=True)
#add margin top and bottom to the title
st.markdown("<style>h1{margin-top: -80px;}</style>", unsafe_allow_html=True)
#center the date below the title
st.markdown("<h6 style='text-align: center; color: white;'>Hoje é " + today + "</h6>", unsafe_allow_html=True)
st.markdown("<style>h6{margin-top: -20px;}</style>", unsafe_allow_html=True)
#st.write(f'Hoje é {today}')

#st.subheader('O que vamos treinar hoje?')
atleta = st.selectbox('Selecione o atleta', ATLETAS, key='atletas_multiselect', placeholder='Selecione um atleta')
#mostrar o nome e data do ultimo treino do atleta escolhido pegando dados da planilha treinos e mostrando em um dataframe
#treino_recente = df_treinos[df_treinos['ATLETA'] == atleta].iloc[-1:]

#if today is thursday 12/09/2024, monday is 09/09/2024, so the first day of the week is 09/09/2024 and the last day is 15/09/2024, based on that filter all treinos from the current week
df_treinos['DATA'] = pd.to_datetime(df_treinos['DATA'], format='%d/%m/%Y')
df_treinos['SEMANA'] = df_treinos['DATA'].dt.isocalendar().week
df_treinos['ANO'] = df_treinos['DATA'].dt.isocalendar().year
df_treinos['DIA'] = df_treinos['DATA'].dt.isocalendar().day
df_treinos['DIA DA SEMANA'] = df_treinos['DATA'].dt.day_name()
df_treinos['DATA'] = df_treinos['DATA'].dt.strftime('%d/%m/%Y')

#get today's week number and show only the treinos from the current week
current_week = df_treinos['SEMANA'].max()
current_year = df_treinos['ANO'].max()
treinos_atleta = df_treinos[(df_treinos['ATLETA'] == atleta) & (df_treinos['SEMANA'] == current_week) & (df_treinos['ANO'] == current_year)]
#show weekday on pt-br
treinos_atleta['DIA DA SEMANA'] = treinos_atleta['DIA DA SEMANA'].map({'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta', 'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'})
treinos_atleta = treinos_atleta.drop(columns=['SEMANA', 'ANO', 'DIA'])
treinos_atleta = treinos_atleta.rename(columns={'DIA DA SEMANA': 'DIA'})
treinos_atleta = treinos_atleta.reset_index(drop=True)

#if the week ends and another begins with no registered trainings, show the last training
if treinos_atleta.empty:
    treinos_atleta = df_treinos[(df_treinos['ATLETA'] == atleta)].iloc[-1:]
    treinos_atleta = treinos_atleta.reset_index(drop=True)


#get all treinos from atleta selected and show the total of treinos in a new column in the df treino_recente called 'TOTAL'
#treinos_atleta = df_treinos[df_treinos['ATLETA'] == atleta]
# treinos_atleta.loc[:, 'TREINOS REGISTRADOS'] = treinos_atleta.groupby('ATLETA')['ATLETA'].transform('count')
#show only the last treino
# treinos_atleta = treinos_atleta.iloc[-3:] #if number of treinos is less than 3, show all
# treinos_atleta = treinos_atleta.drop_duplicates(subset=['ATLETA', 'TREINO', 'DATA'], keep='last')
#================================================================================================


st.write(f"Últimos treinos de {atleta}:")
st.write(treinos_atleta)

# edit = st.button('Clique aqui para editar o último treino', type='primary')
# if edit:
#     st.session_state['atleta'] = atleta
#     st.switch_page("pages/editar.py")

st.divider()

st.markdown("<h3 style='text-align: center; color: white;'>Bora Treinar!</h3>", unsafe_allow_html=True)
st.markdown("<style>h3{margin-bottom: -30px;}</style>", unsafe_allow_html=True)

TREINOS = ['PEITO', 'TRÍCEPS', 'PERNAS', 'OMBROS', 'COSTAS', 'BÍCEPS', 'AEROBICO']
treino = st.multiselect('Selecione os treinos do dia', TREINOS, key='treino_multiselect', placeholder='Selecione um ou mais treinos')
teste = treino

start_train = st.button('Iniciar treino')
if start_train:
    treinos = conn.read(worksheet='treinos')
    treinos = treinos.dropna(how="all")
    df_treinos = pd.DataFrame(treinos)
    dados_do_treino = pd.DataFrame(
                    [{
                        'ATLETA': atleta,
                        'TREINO': ', '.join(teste),  # Convert treino list to string
                        'DATA': hoje,
                    }]
                )
    print(treinos)
    # Atualiza a aba de treinos (adicione apenas uma nova linha)
    updated_df_treinos = pd.concat([df_treinos, dados_do_treino], ignore_index=True)
    print(updated_df_treinos)
    conn.update(worksheet='treinos', data=updated_df_treinos)

    with st.spinner('Iniciando seu treino...'):
        st.cache_data.clear()
        time.sleep(2)

        #on button click, redirect to another page
        st.session_state['treino'] = treino
        st.session_state['atleta'] = atleta
        st.switch_page("pages/treino.py")


# start = st.selectbox('Por qual vamos começar?', treino, key='treino_selectbox', placeholder='Escolha um para registrar')
# if start:
#     mostrar_exercicios(start, atleta)