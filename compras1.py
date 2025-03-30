import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import os
import json
import time
from github import Github

# Configurações da página
st.set_page_config(
    page_title="Sistema de Compras",
    page_icon="🛒",
    layout="wide"
)

# Constantes
LOCAL_FILENAME = "formularios_compras.csv"
CONFIG_FILE = "github_config.json"
SENHA_CONFIG = "king@joe123"  # Senha para acessar configurações

# Configurações padrão do GitHub
DEFAULT_REPO = "vilelarobson0971/compras"
DEFAULT_FILEPATH = "formularios_compras.csv"

# Variáveis globais para configuração do GitHub
GITHUB_REPO = None
GITHUB_FILEPATH = None
GITHUB_TOKEN = None

# Funções auxiliares
def carregar_config():
    """Carrega as configurações do GitHub do arquivo config.json"""
    global GITHUB_REPO, GITHUB_FILEPATH, GITHUB_TOKEN
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                config = json.load(f)
                GITHUB_REPO = config.get('github_repo', DEFAULT_REPO)
                GITHUB_FILEPATH = config.get('github_filepath', DEFAULT_FILEPATH)
                GITHUB_TOKEN = config.get('github_token')
    except Exception as e:
        st.error(f"Erro ao carregar configurações: {str(e)}")

def inicializar_arquivos():
    """Garante que todos os arquivos necessários existam e estejam válidos"""
    # Carregar configurações do GitHub
    carregar_config()
    
    # Inicializar arquivo de formulários de compras
    if not os.path.exists(LOCAL_FILENAME) or os.path.getsize(LOCAL_FILENAME) == 0:
        if GITHUB_REPO and GITHUB_FILEPATH and GITHUB_TOKEN:
            if not baixar_do_github():
                criar_arquivo_local()
        else:
            criar_arquivo_local()

def criar_arquivo_local():
    """Cria um novo arquivo CSV local com estrutura padrão"""
    with open(LOCAL_FILENAME, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Status", "Data Solicitação", "Solicitante", "Centro Custo",
            "Itens", "Quantidades", "Justificativa", "Local Entrega",
            "Aprovador", "Comprador", "Fornecedores", "Preços Unitários",
            "Preços Totais"
        ])

def baixar_do_github():
    """Baixa o arquivo do GitHub se estiver mais atualizado"""
    global GITHUB_REPO, GITHUB_FILEPATH, GITHUB_TOKEN
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        contents = repo.get_contents(GITHUB_FILEPATH)
        
        # Decodificar conteúdo
        file_content = contents.decoded_content.decode('utf-8')
        
        # Salvar localmente
        with open(LOCAL_FILENAME, 'w') as f:
            f.write(file_content)
            
        return True
    except Exception as e:
        st.error(f"Erro ao baixar do GitHub: {str(e)}")
        return False

def enviar_para_github():
    """Envia o arquivo local para o GitHub"""
    global GITHUB_REPO, GITHUB_FILEPATH, GITHUB_TOKEN
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        
        with open(LOCAL_FILENAME, 'r') as f:
            content = f.read()
        
        # Verifica se o arquivo já existe no GitHub
        try:
            contents = repo.get_contents(GITHUB_FILEPATH)
            repo.update_file(contents.path, "Atualização automática do sistema de compras", content, contents.sha)
        except:
            repo.create_file(GITHUB_FILEPATH, "Criação inicial do arquivo de compras", content)
            
        return True
    except Exception as e:
        st.error(f"Erro ao enviar para GitHub: {str(e)}")
        return False

def carregar_dados():
    """Carrega os dados do CSV local com tratamento de erros"""
    colunas_necessarias = [
        "ID", "Status", "Data Solicitação", "Solicitante", "Centro Custo",
        "Itens", "Quantidades", "Justificativa", "Local Entrega",
        "Aprovador", "Comprador", "Fornecedores", "Preços Unitários",
        "Preços Totais"
    ]
    
    try:
        if os.path.exists(LOCAL_FILENAME) and os.path.getsize(LOCAL_FILENAME) > 0:
            df = pd.read_csv(LOCAL_FILENAME)
            
            # Verifica se todas as colunas necessárias existem
            for coluna in colunas_necessarias:
                if coluna not in df.columns:
                    df[coluna] = ""
            
            return df
        else:
            return pd.DataFrame(columns=colunas_necessarias)
    except Exception as e:
        st.error(f"Erro ao ler arquivo local: {str(e)}")
        return pd.DataFrame(columns=colunas_necessarias)

def salvar_dados(df):
    """Salva o DataFrame no arquivo CSV local e no GitHub"""
    try:
        # Garante que todas as colunas necessárias existam
        colunas_necessarias = [
            "ID", "Status", "Data Solicitação", "Solicitante", "Centro Custo",
            "Itens", "Quantidades", "Justificativa", "Local Entrega",
            "Aprovador", "Comprador", "Fornecedores", "Preços Unitários",
            "Preços Totais"
        ]
        
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                df[coluna] = ""
        
        df.to_csv(LOCAL_FILENAME, index=False)
        
        # Se configurado, envia para o GitHub
        if GITHUB_REPO and GITHUB_FILEPATH and GITHUB_TOKEN:
            enviar_para_github()
            
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {str(e)}")
        return False

def gerar_id(df):
    """Gera ID no formato 0001-2025 (sequencial-ano)"""
    ano_atual = datetime.now().year
    
    if not df.empty and 'ID' in df.columns:
        try:
            ids = []
            for row in df['ID']:
                if isinstance(row, str) and '-' in row:
                    try:
                        ids.append(int(row.split('-')[0]))
                    except ValueError:
                        continue
            ultimo_id = max(ids) if ids else 0
        except:
            ultimo_id = 0
    else:
        ultimo_id = 0

    novo_numero = ultimo_id + 1
    return f"{novo_numero:04d}-{ano_atual}"

# Páginas do sistema
def pagina_inicial():
    st.title("🛒 Sistema de Compras")
    st.markdown("""
    ### Bem-vindo ao Sistema de Gestão de Compras
    **Funcionalidades disponíveis:**
    - 📝 **Novo Formulário** - Cadastro de novas solicitações de compra
    - 📋 **Completar Formulário** - Adicionar cotações e completar formulários pendentes
    - 🔍 **Buscar Formulários** - Consulta avançada de formulários cadastrados
    """)

    # Mostra status de sincronização com GitHub
    if GITHUB_REPO and GITHUB_FILEPATH and GITHUB_TOKEN:
        st.success(f"✅ Sincronização ativa com: {GITHUB_REPO}/{GITHUB_FILEPATH}")
    else:
        st.warning("⚠️ Sincronização com GitHub não configurada")

def novo_formulario():
    st.header("📝 Novo Formulário de Compra")
    df = carregar_dados()
    
    # Gerar ID e data automaticamente
    form_id = gerar_id(df)
    data_solicitacao = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Mostrar ID e data no topo (atualizável)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**ID do Formulário:** `{form_id}`")
    with col2:
        st.markdown(f"**Data de Solicitação:** `{data_solicitacao}`")
    
    with st.form("novo_formulario", clear_on_submit=True):
        # Campos do formulário
        nome_solicitante = st.text_input("Nome do Solicitante*")
        centro_custo = st.text_input("Centro de Custo*")
        justificativa = st.text_area("Justificativa da Compra*")
        local_entrega = st.text_input("Local de Entrega*")
        nome_aprovador = st.text_input("Nome do Aprovador*")
        
        # Seção de Itens
        st.subheader("Itens Solicitados")
        
        if 'itens_temp' not in st.session_state:
            st.session_state.itens_temp = []
        
        col1, col2 = st.columns(2)
        with col1:
            novo_item = st.text_input("Descrição do Item", key="novo_item")
        with col2:
            nova_qtd = st.text_input("Quantidade", key="nova_qtd")
        
        # Botão para adicionar item
        add_item = st.form_submit_button("Adicionar Item")
        
        # Mostrar itens adicionados
        for idx, (item, qtd) in enumerate(st.session_state.itens_temp):
            col1, col2, col3 = st.columns([4, 2, 1])
            with col1:
                st.markdown(f"- {item}")
            with col2:
                st.markdown(f"Quantidade: {qtd}")
            with col3:
                if st.button("❌", key=f"del_item_{idx}"):
                    st.session_state.itens_temp.pop(idx)
                    st.rerun()
        
        # Botão principal de submit
        submitted = st.form_submit_button("Submeter Formulário")
        
        if add_item:
            if novo_item and nova_qtd:
                st.session_state.itens_temp.append((novo_item, nova_qtd))
                st.rerun()
        
        if submitted:
            if not nome_solicitante or not centro_custo or not justificativa or not local_entrega or not nome_aprovador:
                st.error("Preencha todos os campos obrigatórios (*)")
            elif not st.session_state.itens_temp:
                st.error("Adicione pelo menos um item")
            else:
                # Preparar dados para CSV
                itens_desc = ";".join([item[0] for item in st.session_state.itens_temp])
                itens_qtd = ";".join([item[1] for item in st.session_state.itens_temp])
                
                nova_linha = pd.DataFrame([{
                    "ID": form_id,
                    "Status": "Pendente",
                    "Data Solicitação": data_solicitacao,
                    "Solicitante": nome_solicitante,
                    "Centro Custo": centro_custo,
                    "Itens": itens_desc,
                    "Quantidades": itens_qtd,
                    "Justificativa": justificativa,
                    "Local Entrega": local_entrega,
                    "Aprovador": nome_aprovador,
                    "Comprador": "",
                    "Fornecedores": "",
                    "Preços Unitários": "",
                    "Preços Totais": ""
                }])
                
                df = pd.concat([df, nova_linha], ignore_index=True)
                if salvar_dados(df):
                    st.success("Formulário submetido com sucesso!")
                    st.session_state.itens_temp = []
                    time.sleep(1)
                    st.rerun()

def completar_formulario():
    st.header("📋 Completar Formulário")
    df = carregar_dados()
    
    # Verifica se a coluna Status existe
    if 'Status' not in df.columns:
        st.warning("Nenhum formulário cadastrado ou estrutura inválida")
        return
    
    # Filtrar formulários pendentes e completos
    tab1, tab2 = st.tabs(["Formulários Pendentes", "Formulários Completos"])
    
    with tab1:
        st.subheader("Formulários Pendentes")
        pendentes = df[df['Status'] == 'Pendente'] if 'Status' in df.columns else pd.DataFrame()
        
        if pendentes.empty:
            st.warning("Nenhum formulário pendente encontrado")
        else:
            # Selecionar formulário para completar
            form_id = st.selectbox("Selecione o formulário para completar", pendentes['ID'])
            form_data = df[df['ID'] == form_id].iloc[0].to_dict()
            
            mostrar_detalhes_formulario(form_data, True)
    
    with tab2:
        st.subheader("Formulários Completos")
        completos = df[df['Status'] == 'Completo'] if 'Status' in df.columns else pd.DataFrame()
        
        if completos.empty:
            st.warning("Nenhum formulário completo encontrado")
        else:
            # Selecionar formulário para visualizar
            form_id = st.selectbox("Selecione o formulário para visualizar", completos['ID'])
            form_data = df[df['ID'] == form_id].iloc[0].to_dict()
            
            mostrar_detalhes_formulario(form_data, False)

def mostrar_detalhes_formulario(form_data, editavel):
    """Mostra os detalhes de um formulário com opção de edição"""
    st.markdown("---")
    st.subheader("Dados do Formulário")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**ID:** {form_data.get('ID', '')}")
        st.markdown(f"**Solicitante:** {form_data.get('Solicitante', '')}")
        st.markdown(f"**Centro de Custo:** {form_data.get('Centro Custo', '')}")
        st.markdown(f"**Local de Entrega:** {form_data.get('Local Entrega', '')}")
    with col2:
        st.markdown(f"**Data de Solicitação:** {form_data.get('Data Solicitação', '')}")
        st.markdown(f"**Status:** {form_data.get('Status', '')}")
        st.markdown(f"**Aprovador:** {form_data.get('Aprovador', '')}")
        if form_data.get('Status') == 'Completo':
            st.markdown(f"**Comprador:** {form_data.get('Comprador', '')}")
    
    st.markdown(f"**Justificativa:** {form_data.get('Justificativa', '')}")
    
    # Mostrar itens
    st.subheader("Itens Solicitados")
    itens = form_data.get('Itens', '').split(';') if pd.notna(form_data.get('Itens')) else []
    quantidades = form_data.get('Quantidades', '').split(';') if pd.notna(form_data.get('Quantidades')) else []
    
    for item, qtd in zip(itens, quantidades):
        st.markdown(f"- {qtd}x {item}")
    
    if form_data.get('Status') == 'Completo':
        st.markdown("---")
        st.subheader("Cotações")
        
        fornecedores = form_data.get('Fornecedores', '').split(';') if pd.notna(form_data.get('Fornecedores')) else []
        precos_unit = form_data.get('Preços Unitários', '').split(';') if pd.notna(form_data.get('Preços Unitários')) else []
        precos_total = form_data.get('Preços Totais', '').split(';') if pd.notna(form_data.get('Preços Totais')) else []
        
        for idx, (fornecedor, unit, total) in enumerate(zip(fornecedores, precos_unit, precos_total)):
            st.markdown(f"**Cotação {idx+1}:**")
            st.markdown(f"- Fornecedor: {fornecedor}")
            st.markdown(f"- Preço Unitário: R$ {unit}")
            st.markdown(f"- Preço Total: R$ {total}")
    
    if editavel:
        st.markdown("---")
        st.subheader("Completar Cotações")
        
        # Seção de cotações
        if 'cotacoes_temp' not in st.session_state:
            st.session_state.cotacoes_temp = []
        
        col1, col2, col3 = st.columns(3)
        with col1:
            novo_fornecedor = st.text_input("Fornecedor")
        with col2:
            novo_preco_unit = st.text_input("Preço Unitário")
        with col3:
            novo_preco_total = st.text_input("Preço Total", disabled=True)
        
        # Botão para adicionar cotação
        if st.button("Adicionar Cotação"):
            if novo_fornecedor and novo_preco_unit:
                try:
                    qtd_total = sum([float(q) for q in quantidades if q.replace('.', '').isdigit()])
                    preco_total = float(novo_preco_unit.replace(",", ".")) * qtd_total
                    st.session_state.cotacoes_temp.append((novo_fornecedor, novo_preco_unit, f"{preco_total:.2f}"))
                    st.rerun()
                except ValueError:
                    st.error("Digite um valor numérico válido para o preço unitário")
        
        # Mostrar cotações adicionadas
        for idx, (fornecedor, preco_unit, preco_total) in enumerate(st.session_state.cotacoes_temp):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.markdown(f"Fornecedor: {fornecedor}")
            with col2:
                st.markdown(f"Unitário: R$ {preco_unit}")
            with col3:
                st.markdown(f"Total: R$ {preco_total}")
            with col4:
                if st.button("❌", key=f"del_cot_{idx}"):
                    st.session_state.cotacoes_temp.pop(idx)
                    st.rerun()
        
        # Campos adicionais
        nome_comprador = st.text_input("Nome do Comprador*")
        
        # Botão para completar formulário
        if st.button("Completar Formulário"):
            if not st.session_state.cotacoes_temp:
                st.error("Adicione pelo menos uma cotação")
            elif not nome_comprador:
                st.error("Informe o nome do comprador")
            else:
                # Atualizar dados do formulário
                df = carregar_dados()
                
                fornecedores = ";".join([c[0] for c in st.session_state.cotacoes_temp])
                precos_unit = ";".join([c[1] for c in st.session_state.cotacoes_temp])
                precos_total = ";".join([c[2] for c in st.session_state.cotacoes_temp])
                
                df.loc[df['ID'] == form_data['ID'], 'Status'] = 'Completo'
                df.loc[df['ID'] == form_data['ID'], 'Comprador'] = nome_comprador
                df.loc[df['ID'] == form_data['ID'], 'Fornecedores'] = fornecedores
                df.loc[df['ID'] == form_data['ID'], 'Preços Unitários'] = precos_unit
                df.loc[df['ID'] == form_data['ID'], 'Preços Totais'] = precos_total
                
                if salvar_dados(df):
                    st.success("Formulário completado com sucesso!")
                    st.session_state.cotacoes_temp = []
                    time.sleep(1)
                    st.rerun()

def buscar_formularios():
    st.header("🔍 Buscar Formulários")
    df = carregar_dados()
    
    if df.empty or 'Status' not in df.columns:
        st.warning("Nenhum formulário cadastrado ou estrutura inválida")
        return
    
    with st.expander("Filtros de Busca"):
        col1, col2 = st.columns(2)
        with col1:
            status_options = ["Todos"] + list(df['Status'].unique()) if 'Status' in df.columns else ["Todos"]
            filtro_status = st.selectbox("Status", status_options)
        with col2:
            filtro_solicitante = st.text_input("Solicitante")
    
    # Aplicar filtros
    if filtro_status != "Todos":
        df = df[df['Status'] == filtro_status]
    if filtro_solicitante:
        df = df[df['Solicitante'].str.contains(filtro_solicitante, case=False, na=False)]
    
    # Mostrar tabela com opções de edição/exclusão
    st.dataframe(df, use_container_width=True)
    
    # Adicionar opções de edição/exclusão para cada linha
    if not df.empty:
        st.subheader("Ações")
        form_id = st.selectbox("Selecione o formulário para ação", df['ID'])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Editar Formulário"):
                editar_formulario(form_id)
        with col2:
            if st.button("🗑️ Excluir Formulário"):
                excluir_formulario(form_id)

def editar_formulario(form_id):
    st.session_state.editando_formulario = form_id
    st.rerun()

def excluir_formulario(form_id):
    df = carregar_dados()
    df = df[df['ID'] != form_id]
    if salvar_dados(df):
        st.success(f"Formulário {form_id} excluído com sucesso!")
        time.sleep(1)
        st.rerun()

def configuracao():
    st.header("⚙️ Configurações")
    
    # Verificação de senha
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        senha = st.text_input("Digite a senha de acesso:", type="password")
        if senha == SENHA_CONFIG:
            st.session_state.autenticado = True
            st.rerun()
        elif senha:  # Só mostra erro se o usuário tentou digitar algo
            st.error("Senha incorreta!")
        return
    
    global GITHUB_REPO, GITHUB_FILEPATH, GITHUB_TOKEN
    
    st.success("Acesso autorizado às configurações")
    
    with st.form("github_config"):
        st.subheader("Configuração do GitHub")
        
        # Mostra configurações atuais
        st.info(f"Repositório atual: {GITHUB_REPO or DEFAULT_REPO}")
        st.info(f"Arquivo atual: {GITHUB_FILEPATH or DEFAULT_FILEPATH}")
        
        # Campo para inserção do token
        token = st.text_input("Token de acesso GitHub*", type="password", value=GITHUB_TOKEN or "")
        
        submitted = st.form_submit_button("Salvar Configurações")
        
        if submitted:
            if token:
                try:
                    # Testa o token com as configurações existentes
                    g = Github(token)
                    repo = g.get_repo(GITHUB_REPO if GITHUB_REPO else DEFAULT_REPO)
                    
                    # Verifica se o arquivo existe ou tenta criar
                    try:
                        repo.get_contents(GITHUB_FILEPATH if GITHUB_FILEPATH else DEFAULT_FILEPATH)
                    except:
                        # Se não existir, cria o arquivo
                        with open(LOCAL_FILENAME, 'r') as f:
                            content = f.read()
                        repo.create_file(
                            GITHUB_FILEPATH if GITHUB_FILEPATH else DEFAULT_FILEPATH,
                            "Criação inicial do arquivo de compras",
                            content
                        )
                    
                    # Salva as configurações
                    config = {
                        'github_repo': GITHUB_REPO if GITHUB_REPO else DEFAULT_REPO,
                        'github_filepath': GITHUB_FILEPATH if GITHUB_FILEPATH else DEFAULT_FILEPATH,
                        'github_token': token
                    }
                    
                    with open(CONFIG_FILE, 'w') as f:
                        json.dump(config, f)
                    
                    # Atualiza variáveis globais
                    GITHUB_TOKEN = token
                    GITHUB_REPO = GITHUB_REPO if GITHUB_REPO else DEFAULT_REPO
                    GITHUB_FILEPATH = GITHUB_FILEPATH if GITHUB_FILEPATH else DEFAULT_FILEPATH
                    
                    st.success("Configurações salvas e validadas com sucesso!")
                    
                    # Sincroniza os dados
                    if baixar_do_github():
                        st.success("Dados sincronizados com o GitHub!")
                    else:
                        st.warning("Configurações salvas, mas não foi possível sincronizar")
                        
                except Exception as e:
                    st.error(f"Erro ao validar credenciais: {str(e)}")
            else:
                st.error("Informe o token de acesso")

# Menu principal
def main():
    # Inicializa arquivos
    inicializar_arquivos()
    
    st.sidebar.title("Menu")
    opcao = st.sidebar.radio(
        "Selecione a opção:",
        ["🏠 Página Inicial", "📝 Novo Formulário", "📋 Completar Formulário", "🔍 Buscar Formulários", "⚙️ Configurações"]
    )
    
    if opcao == "🏠 Página Inicial":
        pagina_inicial()
    elif opcao == "📝 Novo Formulário":
        novo_formulario()
    elif opcao == "📋 Completar Formulário":
        completar_formulario()
    elif opcao == "🔍 Buscar Formulários":
        buscar_formularios()
    elif opcao == "⚙️ Configurações":
        configuracao()

if __name__ == "__main__":
    main()
