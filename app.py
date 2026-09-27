from datetime import datetime
import os
import pandas as pd
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Marinatur - Controle de Custos", page_icon="🚌", layout="centered"
)

EXCEL_FILE = "custos_viagens_marinatur.xlsx"


# ==========================================
# SIMULAÇÃO DE LOGIN COM CONTA GOOGLE (GMAIL)
# ==========================================
def verificar_autenticacao():
  if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = ""

  if not st.session_state.logado:
    st.title("🚌 Marinatur - Acesso Restrito")
    st.markdown("Faça login com sua conta corporativa do Google para continuar.")

    # Botão simulado de login Google (em ambiente de produção na nuvem, pode ser integrado com OAuth)
    email_google = st.text_input(
        "E-mail corporativo (@marinatur ou Gmail autorizados)"
    )

    if st.button("🔑 Entrar com Google"):
      if email_google and (
          "@gmail.com" in email_google or "@marinatur" in email_google
      ):
        st.session_state.logado = True
        st.session_state.usuario = email_google
        st.rerun()
      else:
        st.error(
            "Por favor, insira um e-mail válido do Google ou da Marinatur."
        )
    return False
  return True


# Executa a verificação de login
if not verificar_autenticacao():
  st.stop()


# ==========================================
# FUNÇÕES DE DADOS
# ==========================================
def carregar_dados():
  if os.path.exists(EXCEL_FILE):
    return pd.read_excel(EXCEL_FILE)
  else:
    return pd.DataFrame(
        columns=[
            "ID",
            "Data",
            "Rota / Cliente",
            "Motorista",
            "KM Total",
            "Combustível (R$)",
            "Pedágio (R$)",
            "Estacionamento (R$)",
            "Hospedagem (R$)",
            "Alimentação (R$)",
            "Manutenção/Borracharia (R$)",
            "Taxas / Outros (R$)",
            "Extras (R$)",
            "Custo Total (R$)",
            "Receita (R$)",
            "Lucro (R$)",
            "Registrado por",
        ]
    )


# Cabeçalho Principal e Botão de Logout
col_logo, col_user = st.columns([3, 1])
with col_logo:
  st.title("🚌 Marinatur - Gestão de Custos")
with col_user:
  st.write(f"👤 **{st.session_state.usuario}**")
  if st.button("Sair / Logout"):
    st.session_state.logado = False
    st.rerun()

st.markdown(
    "Preencha os campos abaixo para registrar os custos detalhados da rota."
)

# ==========================================
# FORMULÁRIO DE CADASTRO COM BALÕES DE AJUDA
# ==========================================
with st.form("form_viagem", clear_on_submit=True):
  st.subheader("1. Informações Básicas")
  col1, col2 = st.columns(2)

  with col1:
    data_viagem = st.date_input(
        "Data da Viagem",
        datetime.today(),
        help="Selecione a data em que o serviço/viagem foi realizado.",
    )
    motorista = st.selectbox(
        "Motorista Responsável",
        ["Sid", "Aurélio", "Ricardo", "Edson", "Jair", "Éverton", "Outro"],
        help="Selecione o motorista principal escalado para esta rota.",
    )

  with col2:
    rota = st.text_input(
        "Rota / Cliente",
        placeholder="Ex: Fretamento Aeroporto / Gol",
        help=(
            "Informe o nome do cliente principal ou o trecho percorrido (ex: "
            "Florianópolis - Curitiba)."
        ),
    )
    km_total = st.number_input(
        "Distância Total (KM)",
        min_value=0.0,
        format="%.1f",
        help=(
            "Insira a quilometragem total rodada no serviço (KM Final - KM"
            " Inicial)."
        ),
    )

  st.subheader("2. Lançamento de Custos (R$)")
  c1, c2, c3 = st.columns(3)

  with c1:
    combustivel = st.number_input(
        "Combustível",
        min_value=0.0,
        format="%.2f",
        help="Valor total gasto com abastecimento (Diesel/Gasolina) na viagem.",
    )
    pedagio = st.number_input(
        "Pedágio",
        min_value=0.0,
        format="%.2f",
        help=(
            "Soma total dos pedágios pagos no trajeto (seja por TAG automática"
            " ou dinheiro)."
        ),
    )
    estacionamento = st.number_input(
        "Estacionamento",
        min_value=0.0,
        format="%.2f",
        help=(
            "Gastos com estacionamento em aeroportos, hotéis, parques ou locais"
            " de parada."
        ),
    )

  with c2:
    hospedagem = st.number_input(
        "Hospedagem",
        min_value=0.0,
        format="%.2f",
        help=(
            "Valor total gasto com hotéis ou alojamento para os motoristas"
            " pernoitarem."
        ),
    )
    alimentacao = st.number_input(
        "Alimentação / Diárias",
        min_value=0.0,
        format="%.2f",
        help=(
            "Gastos com refeições, marmitas ou vales-alimentação dos motoristas"
            " durante a rota."
        ),
    )
    manutencao = st.number_input(
        "Manutenção / Borracharia",
        min_value=0.0,
        format="%.2f",
        help=(
            "Reparos emergenciais na estrada, troca de lâmpadas, fusíveis ou"
            " serviços de borracharia."
        ),
    )

  with c3:
    taxas = st.number_input(
        "Taxas (Porto/Parque/Outras)",
        min_value=0.0,
        format="%.2f",
        help=(
            "Taxas municipais, de turismo, portuárias, de aeroportos ou"
            " permissões de tráfego."
        ),
    )
    extras = st.number_input(
        "Extras / Lavagem",
        min_value=0.0,
        format="%.2f",
        help=(
            "Despesas imprevistas ou custos com lavagem/limpeza interna e"
            " externa do veículo."
        ),
    )
    receita = st.number_input(
        "Receita da Viagem (Faturamento)",
        min_value=0.0,
        format="%.2f",
        help=(
            "Valor total cobrado do cliente por este serviço (usado para"
            " calcular o lucro líquido)."
        ),
    )

  submitted = st.form_submit_button("💾 Salvar Nova Viagem")

  if submitted:
    custo_total = (
        combustivel
        + pedagio
        + estacionamento
        + hospedagem
        + alimentacao
        + manutencao
        + taxas
        + extras
    )
    lucro = receita - custo_total
    viagem_id = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )  # ID único baseado no timestamp

    novo_registro = {
        "ID": viagem_id,
        "Data": data_viagem.strftime("%d/%m/%Y"),
        "Rota / Cliente": rota,
        "Motorista": motorista,
        "KM Total": km_total,
        "Combustível (R$)": combustivel,
        "Pedágio (R$)": pedagio,
        "Estacionamento (R$)": estacionamento,
        "Hospedagem (R$)": hospedagem,
        "Alimentação (R$)": alimentacao,
        "Manutenção/Borracharia (R$)": manutencao,
        "Taxas / Outros (R$)": taxas,
        "Extras (R$)": extras,
        "Custo Total (R$)": custo_total,
        "Receita (R$)": receita,
        "Lucro (R$)": lucro,
        "Registrado por": st.session_state.usuario,
    }

    df = carregar_dados()
    df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    st.success(
        f"Viagem cadastrada com sucesso! Custo Total: R$ {custo_total:.2f} |"
        f" Lucro: R$ {lucro:.2f}"
    )

# ==========================================
# HISTÓRICO E OPÇÃO DE EXCLUIR VIAGEM
# ==========================================
st.divider()
st.subheader("📊 Histórico de Viagens Registradas & Gerenciamento")
df_atual = carregar_dados()

if not df_atual.empty:
  st.dataframe(df_atual)

  # Seção de exclusão
  st.markdown("### 🗑️ Excluir Viagem Cadastrada")
  with st.form("form_excluir"):
    # Cria uma lista de opções amigáveis mostrando ID, Data e Rota
    opcoes_viagens = [
        f"{row['ID']} - {row['Data']} | {row['Rota / Cliente']} (Motorista: {row['Motorista']})"
        for index, row in df_atual.iterrows()
    ]
    viagem_selecionada = st.selectbox(
        "Selecione a viagem que deseja excluir:",
        opcoes_viagens,
        help="Escolha o registro incorreto ou duplicado para removê-lo da planilha.",
    )

    btn_excluir = st.form_submit_button("❌ Excluir Viagem Selecionada")

    if btn_excluir and opcoes_viagens:
      # Extrai o ID da string selecionada
      id_para_excluir = viagem_selecionada.split(" - ")[0]

      # Filtra o DataFrame removendo o ID correspondente
      df_atual = df_atual[df_atual["ID"].astype(str) != id_para_excluir]
      df_atual.to_excel(EXCEL_FILE, index=False)

      st.success("Viagem excluída com sucesso! Atualize a página.")
      st.rerun()

  # Botão para baixar a planilha atualizada
  with open(EXCEL_FILE, "rb") as f:
    st.download_button(
        label="📥 Baixar Planilha em Excel Atualizada",
        data=f,
        file_name="custos_marinatur.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )
else:
  st.info("Nenhuma viagem cadastrada ainda.")