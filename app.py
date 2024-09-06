import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

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
    'ABDÔMEN',
    'AEROBICO',
]

EXERCICIOS_PEITO = [
    'SUPINO RETO',
    'SUPINO INCLINADO',
    'CRUCIFIXO',
    'VOADOR',
]

EXERCICIOS_TRICEPS = [
    'PULLEY CORDA',
    'PULLEY INVERTIDO',
    'PULLEY BARRA RETA',
    'COICE',
]

EXERCICIOS_PERNAS = [
    'LEG PRESS',
    'AGACHAMENTO MAQUINA',
    'FLEXORA',
    'EXTENSORA',
    'PANTURRILHA',
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
    'REMADA ALTA',
    'REMADA FRENTE',
    'SERROTE',
    'CAVALO',
]

EXERCICIOS_BICEPS = [
    'ROSCA DIRETA',
    'ROSCA ALTERNADA',
    'ROSCA SCOTT',
    'ROSCA MARTELO',
]

EXERCICIOS_ABDOMEM = [
    'ABDOMINAL',
    'PRANCHA',
    'ABDOMINAL MAQUINA',
]

EXERCICIOS_AEROBICO = [
    'CORRIDA',
    'BIKE',
    'ESTEIRA',
]

#================================================================================================

def mostrar_exercicios(treino, atleta):
    if treino is not None:
        st.write(f"Confira as cargas atuais para o treino de: {treino}")
        
        # Determina a quantidade de exercícios conforme o treino selecionado
        if treino == 'PEITO':
            qtd_exercicios = len(EXERCICIOS_PEITO)
        elif treino == 'TRÍCEPS':
            qtd_exercicios = len(EXERCICIOS_TRICEPS)
        elif treino == 'PERNAS':
            qtd_exercicios = len(EXERCICIOS_PERNAS)
        elif treino == 'OMBROS':
            qtd_exercicios = len(EXERCICIOS_OMBROS)
        elif treino == 'COSTAS':
            qtd_exercicios = len(EXERCICIOS_COSTAS)
        elif treino == 'BÍCEPS':
            qtd_exercicios = len(EXERCICIOS_BICEPS)
        elif treino == 'ABDÔMEN':
            qtd_exercicios = len(EXERCICIOS_ABDOMEM)
        elif treino == 'AEROBICO':
            qtd_exercicios = len(EXERCICIOS_AEROBICO)

        # Filtra o DataFrame para o treino e atleta selecionados
        ultimo_registro = df_cargas[(df_cargas['TREINO'] == treino) & (df_cargas['ATLETA'] == atleta)].iloc[-qtd_exercicios:]
        
        # Exibe o registro mais recente
        st.write(ultimo_registro)

        # df_cargas = pd.DataFrame(conn.read(worksheet='cargas'))
        # print('CARGAS ATUAIS:')
        # print(df_cargas)
        # print("=====================================")

        exercicios = []
        if treino == 'PEITO':
            exercicios = EXERCICIOS_PEITO
        elif treino == 'TRÍCEPS':
            exercicios = EXERCICIOS_TRICEPS
        elif treino == 'PERNAS':
            exercicios = EXERCICIOS_PERNAS
        elif treino == 'OMBROS':
            exercicios = EXERCICIOS_OMBROS
        elif treino == 'COSTAS':
            exercicios = EXERCICIOS_COSTAS
        elif treino == 'BÍCEPS':
            exercicios = EXERCICIOS_BICEPS
        elif treino == 'ABDÔMEN':
            exercicios = EXERCICIOS_ABDOMEM
        elif treino == 'AEROBICO':
            exercicios = EXERCICIOS_AEROBICO

        # Collect all exercise data in a list of dictionaries
        dados_de_carga_list = []

        with st.form(key="train_form"):
            for i, exercicio in enumerate(exercicios):
                col1, col2, col3 = st.columns([2, 1, 2])  # Adjust column sizes
                with col1:
                    carga = st.number_input(f'Carga para {exercicio}', key=f'{treino.lower()}_{i}_carga', min_value=0, step=1)
                with col2:
                    rodadas = st.number_input('Rodadas', key=f'{treino.lower()}_{i}_rodadas', min_value=0, step=1)
                with col3:
                    repeticoes = st.number_input('Repetições', key=f'{treino.lower()}_{i}_repeticoes', min_value=0, step=1)

                # Append input values for each exercise
                dados_de_carga_list.append({
                    'ATLETA': atleta,
                    'TREINO': treino,
                    'EXERCICIO': exercicio,
                    'CARGA': carga,
                    'RODADAS': rodadas,
                    'REPETICOES': repeticoes,
                    'DATA': hoje
                })

            # Convert list to DataFrame
            dados_de_carga = pd.DataFrame(dados_de_carga_list)

            if treino is not None:
                pass
                # cargas = conn.read(worksheet='cargas')
                # cargas = cargas.dropna(how="all")
                # new_loads = pd.DataFrame(cargas)
                # print(" ")
                # print('CARGAS ATUALIZADAS 2:')
                # print(new_loads)
                # print("=====================================")
            else:
                st.write("Selecione um treino para visualizar os exercícios.")

            # Botão para registrar o treino
            submit_button = st.form_submit_button(label='Registrar treino')
            if submit_button:
                #le os dados novamente
                # df_treinos = pd.DataFrame(conn.read(worksheet='treinos'))
                #df_cargas = pd.DataFrame(conn.read(worksheet='cargas'))
                # cargas = conn.read(worksheet='cargas')
                # cargas = cargas.dropna(how="all")
                # new_loads = pd.DataFrame(cargas)
                # print(" ")
                # print('CARGAS ATUALIZADAS:')
                # print(new_loads)
                # print("=====================================")
                # Adiciona novo treino
                dados_do_treino = pd.DataFrame(
                    [{
                        'ATLETA': atleta,
                        'TREINO': ', '.join(teste),  # Convert treino list to string
                        'DATA': hoje,
                    }]
                )

                # Atualiza a aba de treinos (adicione apenas uma nova linha)
                updated_df_treinos = pd.concat([df_treinos, dados_do_treino], ignore_index=True)
                conn.update(worksheet='treinos', data=updated_df_treinos)

                # Atualiza a aba de cargas (adicione apenas as novas linhas)
                updated_df_cargas = pd.concat([df_cargas, dados_de_carga], ignore_index=True)
                conn.update(worksheet='cargas', data=updated_df_cargas)

                print("MUDOU")
                print(df_cargas)

                st.success('Treino registrado com sucesso!')
                st.cache_data.clear()
                st.rerun() #reload page
                
        #st.rerun()
    else:
        pass

# #================================================================================================

st.title('Treino dos Guris')
st.write(f'Hoje é {today}')

st.subheader('O que vamos treinar hoje?')
atleta = st.selectbox('Selecione o atleta', ATLETAS, key='atletas_multiselect', placeholder='Selecione um atleta')
TREINOS = ['PEITO', 'TRÍCEPS', 'PERNAS', 'OMBROS', 'COSTAS', 'BÍCEPS', 'ABDÔMEN', 'AEROBICO']
treino = st.multiselect('Selecione os treinos do dia', TREINOS, key='treino_multiselect', placeholder='Selecione um ou mais treinos')

teste = treino
#teste = ', '.join(teste)
start = st.selectbox('Por qual vamos começar?', treino, key='treino_selectbox', placeholder='Escolha um para registrar')

mostrar_exercicios(start, atleta)