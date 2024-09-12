from app import *

#st.set_page_config(page_title="Treino dos Guris 3.1", page_icon="💪", initial_sidebar_state="collapsed")
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

#recarregar o dataframe
cargas = conn.read(worksheet='cargas')
cargas = cargas.dropna(how="all")
df_cargas = pd.DataFrame(cargas)
# print('DATAFRAME ATUAL')
# print(df_cargas)
#================================================================================================

#função de conexão com o google sheets
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
        # elif treino == 'ABDÔMEN':
        #     qtd_exercicios = len(EXERCICIOS_ABDOMEM)
        elif treino == 'AEROBICO':
            qtd_exercicios = len(EXERCICIOS_AEROBICO)

        # Filtra o DataFrame para o treino e atleta selecionados
        ultimo_registro = df_cargas[(df_cargas['TREINO'] == treino) & (df_cargas['ATLETA'] == atleta)].iloc[-qtd_exercicios:]
        
        # Exibe o registro mais recente
        st.write(ultimo_registro)

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
        # elif treino == 'ABDÔMEN':
        #     exercicios = EXERCICIOS_ABDOMEM
        elif treino == 'AEROBICO':
            exercicios = EXERCICIOS_AEROBICO

        # Collect all exercise data in a list of dictionaries
        dados_de_carga_list = []

        with st.form(key="train_form"):
            for i, exercicio in enumerate(exercicios):
                col1, col2, col3 = st.columns([1, 1, 1])  # Adjust column sizes
                with col1:
                    carga = st.number_input(f'Carga para {exercicio}', key=f'{treino.lower()}_{i}_carga', min_value=0, step=1, value=None, placeholder=0)
                    if carga == None:
                        carga = 0
                with col2:
                    rodadas = st.number_input('Rodadas', key=f'{treino.lower()}_{i}_rodadas', min_value=0, step=1, value=None, placeholder=0)
                    if rodadas == None:
                        rodadas = 0
                with col3:
                    repeticoes = st.number_input('Repetições', key=f'{treino.lower()}_{i}_repeticoes', min_value=0, step=1, value=None, placeholder=0)
                    if repeticoes == None:
                        repeticoes = 0
                
                #add blank space
                st.write(" ")
                st.write(" ")

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

            else:
                st.write("Selecione um treino para visualizar os exercícios.")

            # Botão para registrar o treino
            submit_button = st.form_submit_button(label='Registrar treino')
            if submit_button:

                # Atualiza a aba de cargas (adicione apenas as novas linhas
                updated_df_cargas = pd.concat([df_cargas, dados_de_carga], ignore_index=True)
                conn.update(worksheet='cargas', data=updated_df_cargas)

                # print("MUDOU")
                # print(df_cargas)
                # print("NOVO")
                # print(updated_df_cargas)

                st.success('Treino registrado com sucesso! Aguarde a página recarregar.')

                # Clear the cache to reload the page
                st.cache_data.clear()
                time.sleep(3)
                st.rerun() #reload page
                
        #st.rerun()
    else:
        pass


# Check if 'treino' and 'atleta' exist in session state
if 'treino' in st.session_state and 'atleta' in st.session_state:
    treino = st.session_state['treino']
    atleta = st.session_state['atleta']

    
    st.markdown("<h1 style='text-align: center; color: white;'>BIRLLLLL 💪</h1>", unsafe_allow_html=True)
    st.markdown("<style>h1{margin-top: -10px;}</style>", unsafe_allow_html=True)
    st.markdown(f"<h6 style='text-align: center; color: white;'>Treinos selecionados: {', '.join(treino)}</h6>", unsafe_allow_html=True)
    st.markdown("<style>h6{margin-top: -20px;}</style>", unsafe_allow_html=True)
    #st.write(f"Treinos selecionados: {', '.join(treino)}")

    st.write(" ")
    st.write(" ")
    start = st.selectbox('Por qual vamos começar?', treino, key='treino_selectbox', placeholder='Escolha um para registrar')
    if start:
        mostrar_exercicios(start, atleta)

    # Display the data
    # st.write(f"Treino do atleta {atleta}:")
else:
    st.error("Dados de treino não encontrados, volte para a página inicial.")
    st.write(f'''
        <a target="_self" href="https://treinodosguris.streamlit.app">
            <button>
                VOLTAR A PAGINA INICIAL
            </button>
        </a>
        ''',
        unsafe_allow_html=True
    )