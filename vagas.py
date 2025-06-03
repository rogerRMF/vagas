import os  # Importação do módulo os
import pandas as pd
import streamlit as st
import datetime as dt
from PIL import Image
import altair as alt
from streamlit_option_menu import option_menu

# Configuração da página principal
st.set_page_config(
    page_title='CONTROLE CAJAMAR RH',
    page_icon='$',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'https://www.meuoutrosite.com.br',
        'About': 'Este app foi desenvolvido para RH ID Logistics Cajamar.'
    }
)

selecao = option_menu(
    menu_title="RH-Cajamar",
    options=["Cadastro de Vagas", "Dashboard de Vagas", "HeadCount", "Dashboard HeadCount"],
    
    icons=["person", "bar-chart","clipboard-data"],
    menu_icon="cast",
   orientation="horizontal"
)

# Função principal de cadastro de vagas
# ... [código anterior mantido]

# Função principal de cadastro de vagas
def main():
    st.title("CONTROLE DE GERENCIAMENTO DE VAGAS RH-CAJAMAR")
    data_cadastro = st.date_input("Data do Cadastro", value=dt.datetime.now())
    data_formatada = data_cadastro.strftime("%d/%m/%Y")
    st.write("Data selecionada atual:", data_formatada)

    # Filtros que estavam no sidebar movidos para esta página
    st.subheader("Filtros para Análise")
    with st.expander("🔍 Filtros de Visualização", expanded=True):
        if os.path.exists('cadastro_vagas.xlsx'):
            df_filtros = pd.read_excel('cadastro_vagas.xlsx')
                        
        else:
            st.info("Nenhum dado disponível ainda para aplicar filtros.")

    # Formulário de cadastro
    with st.form(key='vacancy_form'):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Site", value="Zara", disabled=True)
        with col2:
            st.text_input("Nome Requisitante", value="Fábio Souza", disabled=True)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            status = st.selectbox("Status", options=["Aberta", "Fechada"])
        with col2:
            data_abertura = st.date_input("Data da Abertura").strftime("%d/%m/%Y")
        with col3:
            data_limite_contratacao = st.date_input("Data Limite de Contratação").strftime("%d/%m/%Y")
        with col4:
            tipo = st.selectbox("Tipo", options=["Efetivo", "Temporário"])
        with col5:
            adm = st.number_input("ADM", min_value=0)

        # Colunas para turnos
        col6, col7, col8 = st.columns(3)
        with col6:
            turno1 = st.number_input("Turno 1", min_value=0)
        with col7:
            turno2 = st.number_input("Turno 2", min_value=0)
        with col8:
            turno3 = st.number_input("Turno 3", min_value=0)

        funcao_selecionada = st.selectbox("Função", options=[
            "-","LIDER OPERACIONAL", "JOVEM APRENDIZ", "AUXILIAR OPERACIONAL II",
            "CONFERENTE", "ANALISTA DE PLANEJAMENTO",
            "TÉCNICO SEGURANÇA DO TRABALHO", "LIDER QUALIDADE"
        ], index=0)
        
        submit_button = st.form_submit_button(label='Salvar Cadastro')
        if submit_button:
            data = {
                'Site': ['Zara'],
                'Nome Requisitante': ['Fábio Souza'],
                'Função': [funcao_selecionada],
                'Data Cadastro': [data_cadastro.strftime("%d/%m/%Y")],
                'Status': [status],
                'Data da Abertura': [data_abertura],
                'Data Limite de Contratação': [data_limite_contratacao],
                'Tipo': [tipo],
                'Turno 1': [turno1],
                'Turno 2': [turno2],
                'Turno 3': [turno3],
                'ADM': [adm],
                'Total': [turno1 + turno2 + turno3 + adm]
            }

            df = pd.DataFrame(data)

            if os.path.exists('cadastro_vagas.xlsx'):
                existing_df = pd.read_excel('cadastro_vagas.xlsx')
                updated_df = pd.concat([existing_df, df], ignore_index=True)
                updated_df.to_excel('cadastro_vagas.xlsx', index=False)
            else:
                df.to_excel('cadastro_vagas.xlsx', index=False)

            st.success('Cadastro salvo com sucesso!')

    if os.path.exists('cadastro_vagas.xlsx'):
        st.subheader('Registros Existentes')
        existing_data = pd.read_excel('cadastro_vagas.xlsx')
        st.dataframe(existing_data)

    
# Função para exibir gráficos de vagas
def exibir_graficos():
    st.title("Dashboard de Vagas")

    arquivo = 'cadastro_vagas.xlsx'
    if not os.path.exists(arquivo):
        st.warning("Não há dados cadastrados para exibir gráficos.")
        return

    df = pd.read_excel(arquivo)

    funcoes_disponiveis = df['Função'].unique()
    col1, col2 = st.columns([1,1])# 60/40%   funcao_selecionada = st.selectbox("Selecione uma Função para análise", options=funcoes_disponiveis)
    with col1:
        funcao_selecionada = st.selectbox("Selecione uma Função para análise", options=funcoes_disponiveis)
    df_filtrado = df[df['Função'] == funcao_selecionada]
    
    if df_filtrado.empty:
        st.warning("Não há registros para essa função.")
        return

    tipos_disponiveis = df_filtrado['Tipo'].unique()
    with col2:
        tipo_selecionado = st.selectbox("Selecione um Tipo para análise", options=tipos_disponiveis)
  

    df_filtrado = df_filtrado[df_filtrado['Tipo'] == tipo_selecionado]
    if df_filtrado.empty:
        st.warning("Não há registros para essa combinação de função e tipo.")
        return

    total_turno1 = df_filtrado['Turno 1'].sum()
    total_turno2 = df_filtrado['Turno 2'].sum()
    total_turno3 = df_filtrado['Turno 3'].sum()
    adm = df_filtrado['ADM'].sum()
    total_efetivos = total_turno1 + total_turno2 + total_turno3 + adm

    dst1, dst2, dst3, dst4, dst5 = st.columns([1, 1, 1, 1, 1])
    with dst1:
        st.write("Efetivos")
        st.info(f"Qtd: **:green[{total_efetivos}]**")
    with dst2:
        st.write("Turno 1")
        st.info(f"Qtd: {total_turno1}")
    with dst3:
        st.write("Turno 2")
        st.info(f"Qtd: {total_turno2}")
    with dst4:
        st.write("Turno 3")
        st.info(f"Qtd: {total_turno3}")
    with dst5:
        st.write("Administrativo")
        st.info(f"ADM: {adm}")

    st.markdown("------")
    cor_grafico = '#9DD1F1'
    altura_grafico = 400

    df_grafico = pd.DataFrame({
        'Status': ['Turno 1', 'Turno 2', 'Turno 3', 'ADM'],
        'Qtde': [total_turno1, total_turno2, total_turno3, adm]
    })

    grafico_barras = alt.Chart(df_grafico).mark_bar(
        color=cor_grafico,
        cornerRadiusTopLeft=9,
        cornerRadiusTopRight=9,
    ).encode(
        x='Status',
        y='Qtde',
        tooltip=['Status', 'Qtde']
    ).properties(height=altura_grafico, title=alt.TitleParams("Distribuição de Vagas por Turno", anchor='middle')
    ).configure_axis(grid=False).configure_view(strokeWidth=0)

    grafico_donut = alt.Chart(df_grafico).mark_arc(
        innerRadius=100,
        outerRadius=150
    ).encode(
        theta=alt.Theta(field='Qtde', type='quantitative', stack=True),
        color=alt.Color(field='Status', type='nominal', legend=None),
        tooltip=['Status', 'Qtde']
    ).properties(height=500, width=500, title=alt.TitleParams("Distribuição Percentual por Turno", anchor='middle'))

    rot2Ve = grafico_donut.mark_text(radius=210, size=14).encode(text='Qtde')
    rot2Vp = grafico_donut.mark_text(radius=180, size=12).encode(text='Status')

    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(grafico_barras, use_container_width=True)
    with col2:
        st.altair_chart(grafico_donut + rot2Ve + rot2Vp, use_container_width=True)

    st.markdown("------")
    
import streamlit as st
import pandas as pd
import datetime
import os
from openpyxl import load_workbook

def HeadCount():
    st.title("HeadCount")

    # Caminho do arquivo
    arquivo_excel = "cadastro_vagas.xlsx"
    aba_headcount = "HeadCount"

    # Formulário de entrada
    with st.form("form_headcount"):
        efetivos = st.number_input("Quantidade de Efetivos", min_value=0, step=1)
        temporarios = st.number_input("Quantidade de Temporários", min_value=0, step=1)
        moi = st.number_input("Quantidade de MOI", min_value=0, step=1)
        
        turno_selecionado = st.radio("Selecione o Turno", options=["Turno 1", "Turno 2", "Turno 3", "ADM"])
        
        cadastrar = st.form_submit_button("Cadastrar HeadCount")

        if cadastrar:
            data_hoje = datetime.date.today()
            total_colaboradores = efetivos + temporarios
            total_moi_temp = moi + total_colaboradores

            # Novo registro
            nova_linha = {
                "Data": data_hoje,
                "Efetivos": efetivos,
                "Temporários": temporarios,
                "Total MOD": total_colaboradores,
                "MOI": moi,
                "Total Geral": total_moi_temp,
                "Turno": turno_selecionado  # <- coluna G
            }

            try:
                # Se o arquivo já existe, abre e atualiza
                
                # Create or update the Excel file with proper sheet handling
                if os.path.exists(arquivo_excel):
                    try:
                        # Try to read existing sheet
                        existing_df = pd.read_excel(arquivo_excel, sheet_name=aba_headcount)
                    except:
                        # If sheet doesn't exist, create empty DataFrame
                        existing_df = pd.DataFrame(columns=[
                            "Data", "Efetivos", "Temporários", "Total MOD", 
                            "MOI", "Total Geral", "Turno"
                        ])
                    
                    # Append new data
                    updated_df = pd.concat([existing_df, pd.DataFrame([nova_linha])], ignore_index=True)
                    
                    # Save with all sheets
                    with pd.ExcelWriter(arquivo_excel, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                        # Get all existing sheets
                        book = writer.book
                        if aba_headcount in book.sheetnames:
                            book.remove(book[aba_headcount])
                        updated_df.to_excel(writer, sheet_name=aba_headcount, index=False)
                else:
                    # Create new file with HeadCount sheet
                    df = pd.DataFrame([nova_linha], columns=[
                        "Data", "Efetivos", "Temporários", "Total MOD", 
                        "MOI", "Total Geral", "Turno"
                    ])
                    df.to_excel(arquivo_excel, sheet_name=aba_headcount, index=False)

                st.success("HeadCount salvo na planilha com sucesso!")
    
            except Exception as e:
                st.error(f"Erro ao salvar na planilha: {e}")

    # Exibe os dados já salvos (se houver)
    if os.path.exists(arquivo_excel):
        try:
            df_existente = pd.read_excel(arquivo_excel, sheet_name=aba_headcount)
            st.subheader("Histórico de HeadCount")
            st.dataframe(df_existente)
        except Exception as e:
            st.error(f"Erro ao carregar planilha: {e}")
   
# Navegação entre páginas baseada no option_menu
if selecao == "Cadastro de Vagas":
    main()
elif selecao == "Dashboard de Vagas":
    exibir_graficos()
elif selecao == "HeadCount":
    HeadCount()
elif selecao == "Dashboard HeadCount":
    def dashboard_headcount():
        st.title("Dashboard HeadCount")
        
        # Load data
        arquivo = 'cadastro_vagas.xlsx'
        if not os.path.exists(arquivo):
            st.warning("Não há dados cadastrados para exibir gráficos.")
            return
            
        try:
            df = pd.read_excel(arquivo, sheet_name="HeadCount")
        except:
            st.error("Planilha HeadCount não encontrada")
            return

        # Convert date column if needed
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data']).dt.date
            
        # Filters
        st.sidebar.header("Filtros")
        
        # Date range filter
        min_date = df['Data'].min() if 'Data' in df.columns else None
        max_date = df['Data'].max() if 'Data' in df.columns else None
        
        if min_date and max_date:
            date_range = st.sidebar.date_input(
                "Selecione o período",
                value=[min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                df = df[(df['Data'] >= date_range[0]) & (df['Data'] <= date_range[1])]
        
        # Turno filter
        if 'Turno' in df.columns:
            turnos = df['Turno'].unique()
            turno_selecionado = st.sidebar.selectbox("Selecione o Turno", options=["Todos"] + list(turnos))
            
            if turno_selecionado != "Todos":
                df = df[df['Turno'] == turno_selecionado]
        
        # Show raw data
        st.subheader("Dados Filtrados")
        st.dataframe(df)
        
        # Summary stats
        st.subheader("Resumo")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Efetivos", df['Efetivos'].sum())
        with col2:
            st.metric("Total Temporários", df['Temporários'].sum())
        with col3:
            st.metric("Total MOD", df['Total MOD'].sum())
        with col4:
            st.metric("Total MOI", df['MOI'].sum())
        with col5:
            st.metric("Total Geral", df['Total Geral'].sum())
        
        # Bar charts
        st.subheader("Visualização por Turno")
        
        if 'Turno' in df.columns:
            # Group by Turno
            df_turno = df.groupby('Turno').agg({
                'Efetivos': 'sum',
                'Temporários': 'sum',
                'MOI': 'sum'
            }).reset_index()
            
            # Melt for Altair
            df_melt = df_turno.melt(id_vars=['Turno'], 
                                  value_vars=['Efetivos', 'Temporários', 'MOI'],
                                  var_name='Tipo', 
                                  value_name='Quantidade')                     
            cor_grafico = '#9DD1F1'
            altura_grafico = 400

            # Create bar chart
            grafico_barras = alt.Chart(df_melt).mark_bar(
                color=cor_grafico,
                cornerRadiusTopLeft=9,
                cornerRadiusTopRight=9,
                ).encode(
                x='Turno',
                y='Quantidade',
                color='Tipo:N',
                tooltip=['Turno', 'Tipo', 'Quantidade']
            ).properties(height=altura_grafico, title=alt.TitleParams("", anchor='middle')
            
                
            )
            
            st.altair_chart(grafico_barras, use_container_width=True)
        
        
    dashboard_headcount()

