#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import csv
import random
import os
from PIL import Image

# ----------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------
st.set_page_config(
    page_title="Jornada da Fé",
    page_icon="📖",
    layout="wide"
)
st.markdown("""
<style>
/* Texto geral */
html, body, [class*="css"]  {
    font-size: 18px !important;
}

/* Botões */
.stButton>button {
    font-size: 18px !important;
    padding: 12px 18px;
}

/* Títulos */
h1 { font-size: 40px !important; }
h2 { font-size: 30px !important; }
h3 { font-size: 24px !important; }
</style>
""", unsafe_allow_html=True)

ASSETS_DIR = "personagens"
CAMINHO_CSV = "desafios60.csv"


# ----------------------------
# FUNÇÕES AUXILIARES
# ----------------------------
def carregar_dados_csv():
    dados = []
    try:
        with open(CAMINHO_CSV, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                linha_limpa = {}
                for k, v in row.items():
                    if k is None:
                        k = "coluna_extra"
                    else:
                        k = k.strip()

                    if isinstance(v, list):
                        v = " ".join(v)
                    elif v is None:
                        v = ""
                    else:
                        v = v.strip()

                    linha_limpa[k] = v

                dados.append(linha_limpa)

        return dados

    except FileNotFoundError:
        st.error("Erro: Arquivo desafios60.csv não encontrado!")
        return []
    except Exception as e:
        st.error(f"Erro inesperado ao carregar CSV: {e}")
        return []


def iniciar_estado():
    if "tela" not in st.session_state:
        st.session_state.tela = "abertura"

    if "nome_personagem" not in st.session_state:
        st.session_state.nome_personagem = ""

    if "amor" not in st.session_state:
        st.session_state.amor = 0
    if "bondade" not in st.session_state:
        st.session_state.bondade = 0
    if "orgulho" not in st.session_state:
        st.session_state.orgulho = 0
    if "egoismo" not in st.session_state:
        st.session_state.egoismo = 0
    if "maldade" not in st.session_state:
        st.session_state.maldade = 0

    if "indice_desafio" not in st.session_state:
        st.session_state.indice_desafio = 0

    if "lista_desafios" not in st.session_state:
        st.session_state.lista_desafios = []

    if "dados_desafios" not in st.session_state:
        st.session_state.dados_desafios = carregar_dados_csv()

    if "mensagem_reflexao" not in st.session_state:
        st.session_state.mensagem_reflexao = ""


def aplicar_efeito(efeito):
    partes = efeito.split(",")

    for p in partes:
        p = p.strip()
        bonus = random.choice([0, 1])

        if "+1 Amor" in p:
            st.session_state.amor += (1 + bonus)
        elif "+1 Bondade" in p:
            st.session_state.bondade += (1 + bonus)
        elif "+1 Orgulho" in p:
            st.session_state.orgulho += (1 + bonus)
        elif "+1 Egoísmo" in p or "+1 Egoismo" in p:
            st.session_state.egoismo += (1 + bonus)
        elif "+1 Maldade" in p:
            st.session_state.maldade += (1 + bonus)


def barra_status():
    st.markdown("### 📌 Status do Personagem")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("Jovem", st.session_state.nome_personagem)
    col2.metric("Amor", st.session_state.amor)
    col3.metric("Bondade", st.session_state.bondade)
    col4.metric("Orgulho", st.session_state.orgulho)
    col5.metric("Egoísmo", st.session_state.egoismo)
    col6.metric("Maldade", st.session_state.maldade)

    st.divider()


def finalizar_jogo(titulo):
    st.session_state.tela = "final"
    st.session_state.titulo_final = titulo


# ----------------------------
# TELAS DO JOGO
# ----------------------------
def tela_abertura():
    st.title("📖 JORNADA DA FÉ: DESAFIOS DO CORAÇÃO")

    contexto = (
        "No cotidiano de um jovem cristão, as maiores batalhas não são travadas com espadas, "
        "mas nas escolhas invisíveis do coração.\n\n"
        "Entre os corredores da escola, as conversas em família e as interações nas redes sociais, "
        "cada decisão molda quem você é diante de Deus.\n\n"
        "Nesta jornada, você enfrentará situações reais onde o Amor e a Bondade lutarão contra "
        "as inclinações do Orgulho, do Egoísmo e da Maldade.\n\n"
        "**“Lâmpada para os meus pés é tua palavra e luz, para o meu caminho.” (Salmo 119:105)**"
    )

    st.markdown(contexto)

    if st.button("🚀 Iniciar Caminhada"):
        st.session_state.tela = "selecao"
        st.rerun()


def tela_selecao():
    st.title("👤 Escolha seu personagem")
    st.write("Reflita a luz de Cristo em suas decisões!")

    personagens_info = {
        "Lucas": {"img": "menino.png", "descricao": "Dedicado e prestativo."},
        "Sara": {"img": "menina.png", "descricao": "Reflexiva e corajosa."}
    }

    col1, col2 = st.columns(2)

    for col, (nome, info) in zip([col1, col2], personagens_info.items()):
        with col:
            st.subheader(nome)
            st.caption(info["descricao"])

            img_path = os.path.join(ASSETS_DIR, info["img"])
            if os.path.exists(img_path):
                st.image(Image.open(img_path), width=250)
            else:
                st.warning("Imagem não encontrada.")

            if st.button(f"Selecionar {nome}"):
                st.session_state.nome_personagem = nome
                st.session_state.personagem_img = info["img"]
                st.session_state.amor = 0
                st.session_state.bondade = 0
                st.session_state.orgulho = 0
                st.session_state.egoismo = 0
                st.session_state.maldade = 0

                st.session_state.lista_desafios = list(st.session_state.dados_desafios)
                random.shuffle(st.session_state.lista_desafios)

                st.session_state.indice_desafio = 0
                st.session_state.tela = "fase"
                st.rerun()


def tela_fase():
    if st.session_state.indice_desafio >= len(st.session_state.lista_desafios):
        finalizar_jogo("JORNADA CONCLUÍDA")
        st.rerun()

    barra_status()

    dados = st.session_state.lista_desafios[st.session_state.indice_desafio]

    col1, col2 = st.columns([1, 2])

    with col1:
        img_path = os.path.join(ASSETS_DIR, st.session_state.get("personagem_img", ""))
        if os.path.exists(img_path):
            st.image(Image.open(img_path), width=250)

    with col2:
        st.header(f"📍 Cenário: {dados.get('Contexto', 'Geral')}")
        st.markdown(f"**Situação:** {dados.get('Cenario', '...')}")
    
    

    st.divider()

    opcoes = [
        (dados.get("Opcao_A", ""), dados.get("Efeito_A", "")),
        (dados.get("Opcao_B", ""), dados.get("Efeito_B", "")),
        (dados.get("Opcao_C", ""), dados.get("Efeito_C", ""))
    ]

    for texto_opc, efeito in opcoes:
        if texto_opc:
            if st.button(texto_opc):
                aplicar_efeito(efeito)

                msg_biblica = (
                    f"📌 **Referência:** {dados.get('Referencia_Biblica','')}\n\n"
                    f"{dados.get('Interpretacao_Presbiteriana','')}"
                )

                st.session_state.mensagem_reflexao = msg_biblica
                st.session_state.tela = "reflexao"
                st.rerun()

    st.divider()

    if st.button("🛑 Terminar o jogo e ver resultados"):
        finalizar_jogo("JORNADA INTERROMPIDA")
        st.rerun()


def tela_reflexao():
    barra_status()

    st.title("📖 Reflexão Bíblica")
    st.markdown(st.session_state.mensagem_reflexao)

    if st.button("➡️ Próximo desafio"):
        st.session_state.indice_desafio += 1
        st.session_state.tela = "fase"
        st.rerun()


def tela_final():
    barra_status()

    titulo = st.session_state.get("titulo_final", "RESULTADO FINAL")
    st.title(titulo)

    virtudes = st.session_state.amor + st.session_state.bondade
    inclinacoes = st.session_state.orgulho + st.session_state.egoismo + st.session_state.maldade

    st.subheader("📊 Relatório de Caráter")
    st.write(f"**Virtudes (Amor/Bondade):** {virtudes}")
    st.write(f"**Inclinações (Orgulho/Egoísmo/Maldade):** {inclinacoes}")

    vitoria_espiritual = virtudes > inclinacoes

    if st.session_state.maldade > 3:
        desempenho = (
            "⚠️ **Alerta:** Suas escolhas revelaram um coração endurecido. "
            "Busque arrependimento e renovação pela Palavra."
        )
    elif vitoria_espiritual:
        desempenho = (
            "✅ **Excelente caminhada!** Você buscou agir com misericórdia e amor, "
            "refletindo o Fruto do Espírito."
        )
    elif (st.session_state.orgulho + st.session_state.egoismo) > 5:
        desempenho = (
            "⚠️ **Cuidado com o 'Eu':** orgulho e egoísmo influenciaram muitas decisões. "
            "A humildade é o caminho para a verdadeira sabedoria cristã."
        )
    else:
        desempenho = (
            "📌 **Uma jornada de aprendizado:** altos e baixos fazem parte do crescimento espiritual. "
            "Continue perseverando na fé."
        )

    st.markdown(desempenho)

    st.divider()

    versiculos_finais = [
        "Combati o bom combate, acabei a carreira, guardei a fé. (2 Timóteo 4:7)",
        "Mas o fruto do Espírito é: amor, gozo, paz, longanimidade, benignidade... (Gálatas 5:22)",
        "Não te deixes vencer do mal, mas vence o mal com o bem. (Romanos 12:21)",
        "Lâmpada para os meus pés é tua palavra e luz, para o meu caminho. (Salmo 119:105)"
    ]

    st.info(random.choice(versiculos_finais))

    if st.button("🔄 Jogar novamente"):
        st.session_state.tela = "abertura"
        st.session_state.nome_personagem = ""
        st.session_state.indice_desafio = 0
        st.session_state.lista_desafios = []
        st.rerun()


# ----------------------------
# MAIN
# ----------------------------
iniciar_estado()

if st.session_state.tela == "abertura":
    tela_abertura()
elif st.session_state.tela == "selecao":
    tela_selecao()
elif st.session_state.tela == "fase":
    tela_fase()
elif st.session_state.tela == "reflexao":
    tela_reflexao()
elif st.session_state.tela == "final":
    tela_final()

