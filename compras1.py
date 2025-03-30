import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import os
import json
import time
import hashlib
import dotenv
from github import Github, GithubException
from typing import Dict, List, Optional, Tuple
import logging
from fpdf import FPDF
import unicodedata
import re
from pathlib import Path

# Configuração inicial
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações da página
st.set_page_config(
    page_title="Sistema de Compras",
    page_icon="🛒",
    layout="wide"
)

# Constantes
LOCAL_FILENAME = "formularios_compras.csv"
BACKUP_FOLDER = "backups"
CONFIG_FILE = "github_config.json"
MAX_BACKUPS = 5
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Configurações padrão do GitHub
DEFAULT_REPO = "vilelarobson0971/compras"
DEFAULT_FILEPATH = "formularios_compras.csv"

# Variáveis globais para configuração do GitHub
GITHUB_REPO = None
GITHUB_FILEPATH = None
GITHUB_TOKEN = None

# Modelos de dados
class FormularioCompra:
    def __init__(self, data: Dict):
        self.id = data.get("ID", "")
        self.status = data.get("Status", "Pendente")
        self.data_solicitacao = data.get("Data Solicitação", "")
        self.solicitante = data.get("Solicitante", "")
        self.centro_custo = data.get("Centro Custo", "")
        self.itens = data.get("Itens", "").split(';') if data.get("Itens") else []
        self.quantidades = data.get("Quantidades", "").split(';') if data.get("Quantidades") else []
        self.justificativa = data.get("Justificativa", "")
        self.local_entrega = data.get("Local Entrega", "")
        self.aprovador = data.get("Aprovador", "")
        self.comprador = data.get("Comprador", "")
        self.fornecedores = data.get("Fornecedores", "").split(';') if data.get("Fornecedores") else []
        self.precos_unitarios = data.get("Preços Unitários", "").split(';') if data.get("Preços Unitários") else []
        self.precos_totais = data.get("Preços Totais", "").split(';') if data.get("Preços Totais") else []

# Utilitários
def criar_backup():
    """Cria um backup do arquivo atual"""
    try:
        os.makedirs(BACKUP_FOLDER, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_FOLDER, f"{LOCAL_FILENAME}.{timestamp}.bak")
        
        with open(LOCAL_FILENAME, 'rb') as original, open(backup_file, 'wb') as backup:
            backup.write(original.read())
            
        # Limitar número de backups
        backups = sorted(Path(BACKUP_FOLDER).glob(f"{LOCAL_FILENAME}.*.bak"))
        if len(backups) > MAX_BACKUPS:
            for old_backup in backups[:-MAX_BACKUPS]:
                old_backup.unlink()
                
        return True
    except Exception as e:
        logger.error(f"Erro ao criar backup: {e}")
        return False

def hash_senha(senha: str) -> str:
    """Gera hash SHA-256 de uma senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_email(email: str) -> bool:
    """Valida formato de e-mail"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validar_data(data: str) -> bool:
    """Valida formato de data DD/MM/YYYY"""
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def normalizar_texto(texto: str) -> str:
    """Normaliza texto removendo acentos e caracteres especiais"""
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto.upper()

def gerar_relatorio_pdf(formulario: FormularioCompra):
    """Gera relatório em PDF para um formulário"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Cabeçalho
    pdf.cell(200, 10, txt="Relatório de Solicitação de Compra", ln=1, align='C')
    pdf.ln(10)
    
    # Dados básicos
    pdf.cell(200, 10, txt=f"ID: {formulario.id}", ln=1)
    pdf.cell(200, 10, txt=f"Data: {formulario.data_solicitacao}", ln=1)
    pdf.cell(200, 10, txt=f"Solicitante: {formulario.solicitante}", ln=1)
    pdf.cell(200, 10, txt=f"Centro de Custo: {formulario.centro_custo}", ln=1)
    pdf.ln(5)
    
    # Itens
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(200, 10, txt="Itens Solicitados:", ln=1)
    pdf.set_font("Arial", size=10)
    
    for item, qtd in zip(formulario.itens, formulario.quantidades):
        pdf.cell(200, 10, txt=f"- {qtd}x {item}", ln=1)
    
    pdf.ln(5)
    
    # Cotações (se existirem)
    if formulario.status == "Completo":
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Cotações:", ln=1)
        pdf.set_font("Arial", size=10)
        
        for idx, (fornecedor, unit, total) in enumerate(zip(formulario.fornecedores, 
                                                          formulario.precos_unitarios, 
                                                          formulario.precos_totais)):
            pdf.cell(200, 10, txt=f"Cotação {idx+1}: {fornecedor}", ln=1)
            pdf.cell(200, 10, txt=f"Preço Unitário: R$ {unit}", ln=1)
            pdf.cell(200, 10, txt=f"Preço Total: R$ {total}", ln=1)
            pdf.ln(3)
    
    # Salva o PDF temporariamente
    pdf_file = f"relatorio_{formulario.id}.pdf"
    pdf.output(pdf_file)
    
    return pdf_file

# Funções principais
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
                
                # Verifica se há token no .env que sobrescreve o config
                env_token = os.getenv("GITHUB_TOKEN")
                if env_token:
                    GITHUB_TOKEN = env_token
                    
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar arquivo de configuração: {e}")
        st.error("Arquivo de configuração corrompido. Recriando com padrões.")
        criar_arquivo_config()
    except Exception as e:
        logger.error(f"Erro ao carregar configurações: {e}")
        st.error(f"Erro ao carregar configurações: {str(e)}")

def criar_arquivo_config():
    """Cria arquivo de configuração padrão"""
    try:
        config = {
            'github_repo': DEFAULT_REPO,
            'github_filepath': DEFAULT_FILEPATH,
            'github_token': None
        }
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
            
        return True
    except Exception as e:
        logger.error(f"Erro ao criar arquivo de configuração: {e}")
        return False

def inicializar_arquivos():
    """Garante que todos os arquivos necessários existam e estejam válidos"""
    # Carregar configurações do GitHub
    carregar_config()
    
    # Verificar e criar arquivo de configuração se necessário
    if not os.path.exists(CONFIG_FILE):
        criar_arquivo_config()
    
    # Inicializar arquivo de formulários de compras
    if not os.path.exists(LOCAL_FILENAME) or os.path.getsize(LOCAL_FILENAME) == 0:
        if GITHUB_REPO and GITHUB_FILEPATH and GITHUB_TOKEN:
            if not baixar_do_github():
                criar_arquivo_local()
        else:
            criar_arquivo_local()
    else:
        # Verificar tamanho do arquivo para evitar ataques de negação de serviço
        if os.path.getsize(LOCAL_FILENAME) > MAX_FILE_SIZE:
            st.error("Arquivo de dados muito grande. Recriando arquivo vazio.")
            criar_backup()
            criar_arquivo_local()

def criar_arquivo_local():
    """Cria um novo arquivo CSV local com estrutura padrão"""
    try:
        with open(LOCAL_FILENAME, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "ID", "Status", "Data Solicitação", "Solicitante", "Centro Custo",
                "Itens", "Quantidades", "Justificativa", "Local Entrega",
                "Aprovador", "Comprador", "Fornecedores", "Preços Unitários",
                "Preços Totais"
            ])
        return True
    except Exception as e:
        logger.error(f"Erro ao criar arquivo local: {e}")
        st.error(f"Erro ao criar arquivo local: {str(e)}")
        return False

def baixar_do_github() -> bool:
    """Baixa o arquivo do GitHub se estiver mais atualizado"""
    global GITHUB_REPO, GITHUB_FILEPATH, GITHUB_TOKEN
    
    try:
        if not all([GITHUB_REPO, GITHUB_FILEPATH, GITHUB_TOKEN]):
            raise ValueError("Configurações do GitHub incompletas")
            
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        contents = repo.get_contents(GITHUB_FILEPATH)
        
        # Verificar se o arquivo local existe e é mais novo
        if os.path.exists(LOCAL_FILENAME):
            local_mtime = datetime.fromtimestamp(os.path.getmtime(LOCAL_FILENAME))
            remote_mtime = contents.last_modified
            
            if isinstance(remote_mtime, str):
                remote_mtime = datetime.strptime(remote_mtime, "%a, %d %b %Y %H:%M:%S %Z")
            
            if local_mtime > remote_mtime:
                logger.info("Arquivo local mais recente que o remoto. Mantendo local.")
                return True
        
        # Criar backup antes de atualizar
        criar_backup()
        
        # Decodificar conteúdo
        file_content = contents.decoded_content.decode('utf-8')
        
        # Validar conteúdo antes de salvar
        try:
            pd.read_csv(pd.compat.StringIO(file_content))
        except Exception as e:
            raise ValueError(f"Conteúdo do GitHub não é um CSV válido: {str(e)}")
        
        # Salvar localmente
        with open(LOCAL_FILENAME, 'w', encoding='utf-8') as f:
            f.write(file_content)
            
        logger.info("Arquivo baixado do GitHub com sucesso")
        return True
    
    except GithubException as e:
        logger.error(f"Erro na API do GitHub: {e}")
        st.error(f"Erro na API do GitHub: {str(e)}")
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        st.error(str(e))
    except Exception as e:
        logger.error(f"Erro ao baixar do GitHub: {e}")
        st.error(f"Erro ao baixar do GitHub: {str(e)}")
        
    return False

def enviar_para_github() -> bool:
    """Envia o arquivo local para o GitHub"""
    global GITHUB_REPO, GITHUB_FILEPATH, GITHUB_TOKEN
    
    try:
        if not all([GITHUB_REPO, GITHUB_FILEPATH, GITHUB_TOKEN]):
            raise ValueError("Configurações do GitHub incompletas")
            
        # Validar arquivo local antes de enviar
        try:
            df = pd.read_csv(LOCAL_FILENAME)
            if df.empty:
                raise ValueError("Arquivo local está vazio")
        except Exception as e:
            raise ValueError(f"Arquivo local inválido: {str(e)}")
            
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        
        with open(LOCAL_FILENAME, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se o arquivo já existe no GitHub
        try:
            contents = repo.get_contents(GITHUB_FILEPATH)
            repo.update_file(contents.path, "Atualização automática do sistema de compras", content, contents.sha)
        except GithubException:
            repo.create_file(GITHUB_FILEPATH, "Criação inicial do arquivo de compras", content)
            
        logger.info("Arquivo enviado para GitHub com sucesso")
        return True
    
    except GithubException as e:
        logger.error(f"Erro na API do GitHub: {e}")
        st.error(f"Erro na API do GitHub: {str(e)}")
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        st.error(str(e))
    except Exception as e:
        logger.error(f"Erro ao enviar para GitHub: {e}")
        st.error(f"Erro ao enviar para GitHub: {str(e)}")
        
    return False

def carregar_dados() -> pd.DataFrame:
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
    except pd.errors.EmptyDataError:
        logger.error("Arquivo de dados está vazio ou corrompido")
        criar_backup()
        criar_arquivo_local()
        return pd.DataFrame(columns=colunas_necessarias)
    except Exception as e:
        logger.error(f"Erro ao ler arquivo local: {e}")
        st.error(f"Erro ao ler arquivo local: {str(e)}")
        return pd.DataFrame(columns=colunas_necessarias)

def salvar_dados(df: pd.DataFrame) -> bool:
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
        
        # Criar backup antes de salvar
        criar_backup()
        
        # Salvar localmente
        df.to_csv(LOCAL_FILENAME, index=False)
        
        # Se configurado, envia para o GitHub
        if GITHUB_REPO and GITHUB_FILEPATH and GITHUB_TOKEN:
            enviar_para_github()
            
        logger.info("Dados salvos com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        st.error(f"Erro ao salvar dados: {str(e)}")
        return False

def gerar_id(df: pd.DataFrame) -> str:
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
    - ⚙️ **Configurações** - Configurações do sistema e sincronização
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
        nome_solicitante = st.text_input("Nome do Solicitante*", max_chars=100)
        centro_custo = st.text_input("Centro de Custo*", max_chars=50)
        justificativa = st.text_area("Justificativa da Compra*", max_chars=500)
        local_entrega = st.text_input("Local de Entrega*", max_chars=100)
        nome_aprovador = st.text_input("Nome do Aprovador*", max_chars=100)
        
        # Seção de Itens
        st.subheader("Itens Solicitados")
        
        if 'itens_temp' not in st.session_state:
            st.session_state.itens_temp = []
        
        col1, col2 = st.columns(2)
        with col1:
            novo_item = st.text_input("Descrição do Item", key="novo_item", max_chars=200)
        with col2:
            nova_qtd = st.text_input("Quantidade*", key="nova_qtd")
        
        # Botão para adicionar item
        add_item = st.form_submit_button("➕ Adicionar Item")
        
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
        submitted = st.form_submit_button("✅ Submeter Formulário")
        
        if add_item:
            if novo_item and nova_qtd:
                try:
                    # Validar quantidade
                    float(nova_qtd.replace(",", "."))
                    st.session_state.itens_temp.append((novo_item, nova_qtd))
                    st.rerun()
                except ValueError:
                    st.error("Quantidade deve ser um número válido")
        
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
            form_obj = FormularioCompra(form_data)
            
            mostrar_detalhes_formulario(form_obj, True)
    
    with tab2:
        st.subheader("Formulários Completos")
        completos = df[df['Status'] == 'Completo'] if 'Status' in df.columns else pd.DataFrame()
        
        if completos.empty:
            st.warning("Nenhum formulário completo encontrado")
        else:
            # Selecionar formulário para visualizar
            form_id = st.selectbox("Selecione o formulário para visualizar", completos['ID'])
            form_data = df[df['ID'] == form_id].iloc[0].to_dict()
            form_obj = FormularioCompra(form_data)
            
            mostrar_detalhes_formulario(form_obj, False)

def mostrar_detalhes_formulario(formulario: FormularioCompra, editavel: bool):
    """Mostra os detalhes de um formulário com opção de edição"""
    st.markdown("---")
    st.subheader("Dados do Formulário")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**ID:** {formulario.id}")
        st.markdown(f"**Solicitante:** {formulario.solicitante}")
        st.markdown(f"**Centro de Custo:** {formulario.centro_custo}")
        st.markdown(f"**Local de Entrega:** {formulario.local_entrega}")
    with col2:
        st.markdown(f"**Data de Solicitação:** {formulario.data_solicitacao}")
        st.markdown(f"**Status:** {formulario.status}")
        st.markdown(f"**Aprovador:** {formulario.aprovador}")
        if formulario.status == 'Completo':
            st.markdown(f"**Comprador:** {formulario.comprador}")
    
    st.markdown(f"**Justificativa:** {formulario.justificativa}")
    
    # Mostrar itens
    st.subheader("Itens Solicitados")
    for item, qtd in zip(formulario.itens, formulario.quantidades):
        st.markdown(f"- {qtd}x {item}")
    
    if formulario.status == "Completo":
        st.markdown("---")
        st.subheader("Cotações")
        
        for idx, (fornecedor, unit, total) in enumerate(zip(formulario.fornecedores, 
                                                          formulario.precos_unitarios, 
                                                          formulario.precos_totais)):
            st.markdown(f"**Cotação {idx+1}:**")
            st.markdown(f"- Fornecedor: {fornecedor}")
            st.markdown(f"- Preço Unitário: R$ {unit}")
            st.markdown(f"- Preço Total: R$ {total}")
    
    # Gerar relatório PDF
    if formulario.status == "Completo":
        st.markdown("---")
        st.subheader("Relatório")
        if st.button("📄 Gerar Relatório PDF"):
            pdf_file = gerar_relatorio_pdf(formulario)
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="⬇️ Baixar Relatório",
                    data=f,
                    file_name=f"relatorio_compra_{formulario.id}.pdf",
                    mime="application/pdf"
                )
            os.remove(pdf_file)
    
    if editavel:
        st.markdown("---")
        st.subheader("Completar Cotações")
        
        # Seção de cotações
        if 'cotacoes_temp' not in st.session_state:
            st.session_state.cotacoes_temp = []
        
        col1, col2, col3 = st.columns(3)
        with col1:
            novo_fornecedor = st.text_input("Fornecedor*", key="novo_fornecedor", max_chars=100)
        with col2:
            novo_preco_unit = st.text_input("Preço Unitário*", key="novo_preco_unit")
        with col3:
            novo_preco_total = st.text_input("Preço Total", key="novo_preco_total", disabled=True)
        
        # Calcular preço total automaticamente
        if novo_preco_unit and st.session_state.get("novo_preco_unit_prev") != novo_preco_unit:
            try:
                qtd_total = sum([float(q.replace(",", ".")) for q in formulario.quantidades 
                               if q.replace(".", "").replace(",", "").isdigit()])
                preco_total = float(novo_preco_unit.replace(",", ".")) * qtd_total
                st.session_state.novo_preco_total = f"{preco_total:.2f}"
                st.session_state.novo_preco_unit_prev = novo_preco_unit
                st.rerun()
            except ValueError:
                st.error("Digite um valor numérico válido para o preço unitário")
        
        # Botão para adicionar cotação
        if st.button("➕ Adicionar Cotação"):
            if novo_fornecedor and novo_preco_unit:
                try:
                    # Validar preço unitário
                    float(novo_preco_unit.replace(",", "."))
                    st.session_state.cotacoes_temp.append((
                        novo_fornecedor, 
                        novo_preco_unit, 
                        st.session_state.novo_preco_total
                    ))
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
        nome_comprador = st.text_input("Nome do Comprador*", max_chars=100)
        
        # Botão para completar formulário
        if st.button("✅ Completar Formulário"):
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
                
                df.loc[df['ID'] == formulario.id, 'Status'] = 'Completo'
                df.loc[df['ID'] == formulario.id, 'Comprador'] = nome_comprador
                df.loc[df['ID'] == formulario.id, 'Fornecedores'] = fornecedores
                df.loc[df['ID'] == formulario.id, 'Preços Unitários'] = precos_unit
                df.loc[df['ID'] == formulario.id, 'Preços Totais'] = precos_total
                
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
    
    with st.expander("🔎 Filtros de Busca Avançada"):
        col1, col2, col3 = st.columns(3)
        with col1:
            status_options = ["Todos"] + list(df['Status'].unique()) if 'Status' in df.columns else ["Todos"]
            filtro_status = st.selectbox("Status", status_options)
        with col2:
            filtro_solicitante = st.text_input("Solicitante")
        with col3:
            filtro_id = st.text_input("ID do Formulário")
    
    # Aplicar filtros
    if filtro_status != "Todos":
        df = df[df['Status'] == filtro_status]
    if filtro_solicitante:
        df = df[df['Solicitante'].str.contains(filtro_solicitante, case=False, na=False)]
    if filtro_id:
        df = df[df['ID'].str.contains(filtro_id, case=False, na=False)]
    
    # Mostrar tabela com opções de edição/exclusão
    if not df.empty:
        st.dataframe(
            df, 
            use_container_width=True,
            column_config={
                "Justificativa": st.column_config.TextColumn(width="large"),
                "Itens": st.column_config.TextColumn(width="large")
            }
        )
        
        # Adicionar opções de edição/exclusão para cada linha
        st.subheader("🛠️ Ações")
        form_id = st.selectbox("Selecione o formulário para ação", df['ID'])
        form_data = df[df['ID'] == form_id].iloc[0].to_dict()
        form_obj = FormularioCompra(form_data)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✏️ Editar Formulário"):
                editar_formulario(form_obj)
        with col2:
            if st.button("🗑️ Excluir Formulário"):
                confirmar_exclusao(form_obj)
        with col3:
            if form_obj.status == "Completo":
                if st.button("📄 Gerar Relatório"):
                    pdf_file = gerar_relatorio_pdf(form_obj)
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            label="⬇️ Baixar Relatório",
                            data=f,
                            file_name=f"relatorio_compra_{form_obj.id}.pdf",
                            mime="application/pdf"
                        )
                    os.remove(pdf_file)
    else:
        st.warning("Nenhum formulário encontrado com os filtros aplicados")

def editar_formulario(formulario: FormularioCompra):
    """Página de edição de formulário"""
    st.header(f"✏️ Editando Formulário {formulario.id}")
    
    df = carregar_dados()
    form_index = df[df['ID'] == formulario.id].index[0]
    
    with st.form(f"editar_form_{formulario.id}"):
        col1, col2 = st.columns(2)
                with col1:
            novo_solicitante = st.text_input("Solicitante*", value=formulario.solicitante, max_chars=100)
            novo_centro_custo = st.text_input("Centro de Custo*", value=formulario.centro_custo, max_chars=50)
            novo_local_entrega = st.text_input("Local de Entrega*", value=formulario.local_entrega, max_chars=100)
        with col2:
            novo_aprovador = st.text_input("Aprovador*", value=formulario.aprovador, max_chars=100)
            novo_comprador = st.text_input("Comprador", value=formulario.comprador, max_chars=100)
        
        nova_justificativa = st.text_area("Justificativa*", value=formulario.justificativa, max_chars=500)
        
        # Edição de itens
        st.subheader("Itens Solicitados")
        if 'itens_editados' not in st.session_state:
            st.session_state.itens_editados = list(zip(formulario.itens, formulario.quantidades))
        
        for idx, (item, qtd) in enumerate(st.session_state.itens_editados):
            col1, col2, col3 = st.columns([4, 2, 1])
            with col1:
                novo_item = st.text_input(f"Item {idx+1}", value=item, key=f"item_{idx}")
            with col2:
                nova_qtd = st.text_input(f"Qtd {idx+1}", value=qtd, key=f"qtd_{idx}")
            with col3:
                if st.button("❌", key=f"remove_{idx}"):
                    st.session_state.itens_editados.pop(idx)
                    st.rerun()
            
            # Atualiza os valores na lista
            if novo_item != item or nova_qtd != qtd:
                st.session_state.itens_editados[idx] = (novo_item, nova_qtd)
        
        # Adicionar novo item
        col1, col2 = st.columns(2)
        with col1:
            novo_item = st.text_input("Novo Item", key="novo_item_edit")
        with col2:
            nova_qtd = st.text_input("Quantidade", key="nova_qtd_edit")
        
        if st.button("➕ Adicionar Item"):
            if novo_item and nova_qtd:
                try:
                    float(nova_qtd.replace(",", "."))  # Valida se é número
                    st.session_state.itens_editados.append((novo_item, nova_qtd))
                    st.rerun()
                except ValueError:
                    st.error("Quantidade deve ser um número válido")
        
        # Seção para editar cotações (se formulário estiver completo)
        if formulario.status == "Completo":
            st.subheader("Cotações")
            if 'cotacoes_editadas' not in st.session_state:
                st.session_state.cotacoes_editadas = list(zip(
                    formulario.fornecedores,
                    formulario.precos_unitarios,
                    formulario.precos_totais
                ))
            
            for idx, (fornecedor, unit, total) in enumerate(st.session_state.cotacoes_editadas):
                st.markdown(f"**Cotação {idx+1}**")
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    novo_fornecedor = st.text_input(f"Fornecedor {idx+1}", value=fornecedor, key=f"forn_{idx}")
                with col2:
                    novo_unit = st.text_input(f"Unitário {idx+1}", value=unit, key=f"unit_{idx}")
                with col3:
                    novo_total = st.text_input(f"Total {idx+1}", value=total, key=f"total_{idx}", disabled=True)
                with col4:
                    if st.button("❌", key=f"del_cot_{idx}"):
                        st.session_state.cotacoes_editadas.pop(idx)
                        st.rerun()
                
                # Atualizar total se unitário mudar
                if novo_unit != unit:
                    try:
                        qtd_total = sum([float(q.replace(",", ".")) for q in [i[1] for i in st.session_state.itens_editados]])
                        novo_total = float(novo_unit.replace(",", ".")) * qtd_total
                        st.session_state.cotacoes_editadas[idx] = (novo_fornecedor, novo_unit, f"{novo_total:.2f}")
                        st.rerun()
                    except ValueError:
                        st.error("Preço unitário inválido")
        
        # Botões de ação
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.form_submit_button("💾 Salvar Alterações"):
                # Validar campos obrigatórios
                if (not novo_solicitante or not novo_centro_custo or not novo_local_entrega or 
                    not novo_aprovador or not nova_justificativa or not st.session_state.itens_editados):
                    st.error("Preencha todos os campos obrigatórios (*)")
                else:
                    # Atualizar DataFrame
                    df.at[form_index, "Solicitante"] = novo_solicitante
                    df.at[form_index, "Centro Custo"] = novo_centro_custo
                    df.at[form_index, "Local Entrega"] = novo_local_entrega
                    df.at[form_index, "Aprovador"] = novo_aprovador
                    df.at[form_index, "Comprador"] = novo_comprador
                    df.at[form_index, "Justificativa"] = nova_justificativa
                    
                    # Atualizar itens
                    itens = ";".join([i[0] for i in st.session_state.itens_editados])
                    qtds = ";".join([i[1] for i in st.session_state.itens_editados])
                    df.at[form_index, "Itens"] = itens
                    df.at[form_index, "Quantidades"] = qtds
                    
                    # Atualizar cotações se existirem
                    if formulario.status == "Completo" and st.session_state.cotacoes_editadas:
                        fornecedores = ";".join([c[0] for c in st.session_state.cotacoes_editadas])
                        units = ";".join([c[1] for c in st.session_state.cotacoes_editadas])
                        totais = ";".join([c[2] for c in st.session_state.cotacoes_editadas])
                        df.at[form_index, "Fornecedores"] = fornecedores
                        df.at[form_index, "Preços Unitários"] = units
                        df.at[form_index, "Preços Totais"] = totais
                    
                    if salvar_dados(df):
                        st.success("Formulário atualizado com sucesso!")
                        time.sleep(1)
                        st.session_state.pop("itens_editados", None)
                        st.session_state.pop("cotacoes_editadas", None)
                        st.rerun()
        
        with col2:
            if st.form_submit_button("❌ Cancelar"):
                st.session_state.pop("itens_editados", None)
                st.session_state.pop("cotacoes_editadas", None)
                st.rerun()
        
        with col3:
            if formulario.status == "Pendente" and st.session_state.cotacoes_editadas:
                if st.form_submit_button("✅ Completar Formulário"):
                    if not novo_comprador:
                        st.error("Informe o nome do comprador para completar o formulário")
                    else:
                        df.at[form_index, "Status"] = "Completo"
                        df.at[form_index, "Comprador"] = novo_comprador
                        fornecedores = ";".join([c[0] for c in st.session_state.cotacoes_editadas])
                        units = ";".join([c[1] for c in st.session_state.cotacoes_editadas])
                        totais = ";".join([c[2] for c in st.session_state.cotacoes_editadas])
                        df.at[form_index, "Fornecedores"] = fornecedores
                        df.at[form_index, "Preços Unitários"] = units
                        df.at[form_index, "Preços Totais"] = totais
                        
                        if salvar_dados(df):
                            st.success("Formulário marcado como completo!")
                            time.sleep(1)
                            st.session_state.pop("itens_editados", None)
                            st.session_state.pop("cotacoes_editadas", None)
                            st.rerun()

def confirmar_exclusao(formulario: FormularioCompra):
    """Página de confirmação de exclusão"""
    st.warning(f"⚠️ Tem certeza que deseja excluir o formulário {formulario.id}?")
    st.write(f"Solicitante: {formulario.solicitante}")
    st.write(f"Data: {formulario.data_solicitacao}")
    st.write(f"Itens: {', '.join(formulario.itens[:3])}{'...' if len(formulario.itens) > 3 else ''}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Sim, Excluir"):
            df = carregar_dados()
            df = df[df['ID'] != formulario.id]
            if salvar_dados(df):
                st.success("Formulário excluído com sucesso!")
                time.sleep(1)
                st.rerun()
    with col2:
        if st.button("❌ Não, Cancelar"):
            st.rerun()

def configuracao():
    st.header("⚙️ Configurações")
    
    # Verificação de senha
    if 'autenticado' not in st.session_state:
        st.session_state.autenticado = False
    
    if not st.session_state.autenticado:
        senha = st.text_input("Digite a senha de acesso:", type="password")
        if senha and hash_senha(senha) == hash_senha(os.getenv("ADMIN_PASSWORD", "default_password")):
            st.session_state.autenticado = True
            st.rerun()
        elif senha:
            st.error("Senha incorreta!")
        return
    
    global GITHUB_REPO, GITHUB_FILEPATH, GITHUB_TOKEN
    
    st.success("🔓 Acesso autorizado às configurações")
    
    tab1, tab2, tab3 = st.tabs(["GitHub", "Backup", "Sistema"])
    
    with tab1:
        st.subheader("🔗 Configuração do GitHub")
        
        with st.form("github_config"):
            # Mostra configurações atuais
            st.info(f"Repositório atual: {GITHUB_REPO or DEFAULT_REPO}")
            st.info(f"Arquivo atual: {GITHUB_FILEPATH or DEFAULT_FILEPATH}")
            
            # Campos para edição
            novo_repo = st.text_input("Repositório GitHub (user/repo)", value=GITHUB_REPO or DEFAULT_REPO)
            novo_caminho = st.text_input("Caminho do arquivo no repositório", value=GITHUB_FILEPATH or DEFAULT_FILEPATH)
            token = st.text_input("Token de acesso GitHub*", type="password", value=GITHUB_TOKEN or "")
            
            submitted = st.form_submit_button("💾 Salvar Configurações")
            
            if submitted:
                if token:
                    try:
                        # Testa o token com as configurações
                        g = Github(token)
                        repo = g.get_repo(novo_repo)
                        
                        # Tenta acessar o arquivo
                        try:
                            repo.get_contents(novo_caminho)
                        except:
                            # Se não existir, cria o arquivo
                            with open(LOCAL_FILENAME, 'r') as f:
                                content = f.read()
                            repo.create_file(
                                novo_caminho,
                                "Criação inicial do arquivo de compras",
                                content
                            )
                        
                        # Salva as configurações
                        config = {
                            'github_repo': novo_repo,
                            'github_filepath': novo_caminho,
                            'github_token': token
                        }
                        
                        with open(CONFIG_FILE, 'w') as f:
                            json.dump(config, f)
                        
                        # Atualiza variáveis globais
                        GITHUB_REPO = novo_repo
                        GITHUB_FILEPATH = novo_caminho
                        GITHUB_TOKEN = token
                        
                        st.success("✅ Configurações salvas e validadas com sucesso!")
                        
                        # Sincroniza os dados
                        if baixar_do_github():
                            st.success("Dados sincronizados com o GitHub!")
                        else:
                            st.warning("Configurações salvas, mas não foi possível sincronizar")
                            
                    except GithubException as e:
                        st.error(f"Erro na API do GitHub: {str(e)}")
                    except Exception as e:
                        st.error(f"Erro ao validar credenciais: {str(e)}")
                else:
                    st.error("Informe o token de acesso")
    
    with tab2:
        st.subheader("🗄️ Gerenciamento de Backup")
        
        # Listar backups disponíveis
        backups = sorted(Path(BACKUP_FOLDER).glob(f"{LOCAL_FILENAME}.*.bak"), reverse=True)
        
        if backups:
            st.write("Backups disponíveis:")
            for backup in backups:
                col1, col2, col3 = st.columns([4, 2, 2])
                with col1:
                    st.write(backup.name)
                with col2:
                    st.write(time.ctime(os.path.getmtime(backup)))
                with col3:
                    if st.button("Restaurar", key=f"rest_{backup.name}"):
                        try:
                            with open(backup, 'rb') as bkp, open(LOCAL_FILENAME, 'wb') as original:
                                original.write(bkp.read())
                            st.success("Backup restaurado com sucesso!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao restaurar backup: {str(e)}")
            
            if st.button("🔄 Criar Backup Agora"):
                if criar_backup():
                    st.success("Backup criado com sucesso!")
                    time.sleep(1)
                    st.rerun()
        else:
            st.warning("Nenhum backup disponível")
            if st.button("🔄 Criar Primeiro Backup"):
                if criar_backup():
                    st.success("Backup criado com sucesso!")
                    time.sleep(1)
                    st.rerun()
    
    with tab3:
        st.subheader("⚙️ Configurações do Sistema")
        
        with st.form("system_config"):
            # Configurações de segurança
            st.write("**Segurança**")
            nova_senha = st.text_input("Alterar Senha de Administração", type="password")
            confirm_senha = st.text_input("Confirmar Nova Senha", type="password")
            
            # Configurações de dados
            st.write("**Dados**")
            limite_backups = st.number_input("Número máximo de backups", min_value=1, max_value=20, value=MAX_BACKUPS)
            
            if st.form_submit_button("💾 Salvar Configurações"):
                if nova_senha and nova_senha == confirm_senha:
                    os.environ["ADMIN_PASSWORD"] = nova_senha
                    st.success("Senha atualizada com sucesso!")
                
                # Atualizar configurações de backup
                global MAX_BACKUPS
                MAX_BACKUPS = limite_backups
                st.success("Configurações salvas!")

# Menu principal
def main():
    # Inicializa arquivos
    inicializar_arquivos()
    
    st.sidebar.title("📋 Menu")
    opcao = st.sidebar.radio(
        "Selecione a opção:",
        ["🏠 Página Inicial", "📝 Novo Formulário", "📋 Completar Formulário", "🔍 Buscar Formulários", "⚙️ Configurações"]
    )
    
    # Mostrar notificação se houver formulários pendentes
    df = carregar_dados()
    if 'Status' in df.columns:
        pendentes = len(df[df['Status'] == 'Pendente'])
        if pendentes > 0:
            st.sidebar.warning(f"⚠️ {pendentes} formulário(s) pendente(s)")
    
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
    
    # Rodapé
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"🔄 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Sincronizar com GitHub se configurado
    if GITHUB_REPO and GITHUB_FILEPATH and GITHUB_TOKEN:
        if st.sidebar.button("🔄 Sincronizar com GitHub"):
            with st.spinner("Sincronizando..."):
                if baixar_do_github():
                    st.sidebar.success("Sincronizado!")
                else:
                    st.sidebar.error("Falha na sincronização")

if __name__ == "__main__":
    main()
