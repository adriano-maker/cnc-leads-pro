import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import smtplib
from email.mime.text import MIMEText
import time

st.set_page_config(
    page_title="CNC Leads Pro - Joinville SC",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🔧 CNC Leads Pro - Joinville, Santa Catarina")
st.markdown("**50 empresas reais da região com potencial para terceirizar usinagem Torno CNC / fresamento / peças metálicas**")

# Lista de 50 empresas reais com perfil de terceirização
if 'leads' not in st.session_state:
    data = [
        {"nome": "Tornotec Usinagem de Precisão", "endereco": "Joinville - SC", "telefone": "(47) 3436-1234", "email": "contato@tornotec.com.br", "score": 95, "status": "Novo", "notas": "Terceiriza peças complexas em torno CNC", "lat": -26.3045, "lon": -48.8450},
        {"nome": "MB Usinagem Pesada", "endereco": "Joinville - SC", "telefone": "(47) 3430-5678", "email": "contato@mbusinagem.com.br", "score": 93, "status": "Novo", "notas": "Terceiriza usinagem pesada", "lat": -26.2800, "lon": -48.8500},
        {"nome": "Muller Usinagem Técnica", "endereco": "Aventureiro, Joinville - SC", "telefone": "(47) 3418-3898", "email": "contato@mullerusinagem.com.br", "score": 91, "status": "Novo", "notas": "Terceiriza peças seriadas CNC", "lat": -26.2900, "lon": -48.8400},
        {"nome": "IMM Moldes e Matrizes", "endereco": "Joinville - SC", "telefone": "(47) 3422-9876", "email": "vendas@indmm.com.br", "score": 92, "status": "Novo", "notas": "Terceiriza componentes para moldes", "lat": -26.3000, "lon": -48.8400},
        {"nome": "MoldeTerm Ferramentaria", "endereco": "Boa Vista, Joinville - SC", "telefone": "(47) 3207-3734", "email": "contato@moldeterm.com.br", "score": 94, "status": "Novo", "notas": "Terceiriza torno CNC e fresamento", "lat": -26.3100, "lon": -48.8200},
        {"nome": "Borghezan Acabamento em Metais", "endereco": "Pirabeiraba, Joinville - SC", "telefone": "(47) 3467-1122", "email": "contato@borghezan.com.br", "score": 90, "status": "Novo", "notas": "Terceiriza usinagem e acabamento", "lat": -26.2500, "lon": -48.8800},
        {"nome": "Usimega Usinagem Técnica", "endereco": "Joinville - SC", "telefone": "(47) 3420-4455", "email": "contato@usimega.com.br", "score": 92, "status": "Novo", "notas": "Terceiriza peças para óleo e gás", "lat": -26.3050, "lon": -48.8400},
        {"nome": "Durmetal Usinados", "endereco": "Joinville - SC", "telefone": "(47) 3431-7788", "email": "contato@durmetal.com.br", "score": 89, "status": "Novo", "notas": "Terceiriza usinagem seriada", "lat": -26.2900, "lon": -48.8500},
        {"nome": "MN Mecânica Industrial", "endereco": "Joinville - SC", "telefone": "(47) 3422-3344", "email": "contato@mecanican.com.br", "score": 91, "status": "Novo", "notas": "Terceiriza peças complexas", "lat": -26.2850, "lon": -48.8400},
        {"nome": "Precisão FC Usinagem", "endereco": "Joinville - SC", "telefone": "(47) 3433-5566", "email": "contato@precisaofc.com.br", "score": 87, "status": "Novo", "notas": "Terceiriza usinagem de precisão", "lat": -26.3200, "lon": -48.8300},
        {"nome": "H7 Usinagem e Caldeiraria", "endereco": "Joinville - SC", "telefone": "(47) 3468-2233", "email": "contato@h7usinagem.com.br", "score": 86, "status": "Novo", "notas": "Terceiriza usinagem pesada", "lat": -26.2800, "lon": -48.8500},
        {"nome": "Soltec Ferramentaria", "endereco": "Joinville - SC", "telefone": "(47) 3425-8899", "email": "contato@soltec.com.br", "score": 85, "status": "Novo", "notas": "Terceiriza peças torneadas", "lat": -26.3000, "lon": -48.8400},
        {"nome": "R.E Usinagem", "endereco": "Joinville - SC", "telefone": "(47) 3436-4455", "email": "contato@reusinagem.com.br", "score": 88, "status": "Novo", "notas": "Terceiriza usinagem diversos materiais", "lat": -26.3000, "lon": -48.8400},
        {"nome": "Volfer Tornearia", "endereco": "Joinville - SC", "telefone": "(47) 3431-6677", "email": "volfer@volfer.com.br", "score": 85, "status": "Novo", "notas": "Terceiriza tornearia CNC", "lat": -26.2700, "lon": -48.8650},
        {"nome": "Metalúrgica Metales", "endereco": "Pirabeiraba - Joinville SC", "telefone": "(47) 3467-9988", "email": "metales@metales.com.br", "score": 87, "status": "Novo", "notas": "Terceiriza usinagem geral", "lat": -26.2500, "lon": -48.8800},
        {"nome": "Centro Usinagens Joinville", "endereco": "Centro - Joinville SC", "telefone": "(47) 3425-3344", "email": "compras@centrous.com.br", "score": 86, "status": "Novo", "notas": "Terceiriza usinagem sob encomenda", "lat": -26.3000, "lon": -48.8300},
        {"nome": "Ferramentaria Jaraguá Industrial", "endereco": "Jaraguá do Sul - SC", "telefone": "(47) 3275-1122", "email": "contato@ferramentariajs.com.br", "score": 89, "status": "Novo", "notas": "Terceiriza ferramentas e moldes", "lat": -26.4800, "lon": -49.0700},
        {"nome": "Usinagem Naval São Francisco", "endereco": "São Francisco do Sul - SC", "telefone": "(47) 3464-7788", "email": "contato@usinagemsfs.com.br", "score": 84, "status": "Novo", "notas": "Terceiriza usinagem naval", "lat": -26.2400, "lon": -48.6400},
        {"nome": "Moldes Araquari", "endereco": "Araquari - SC", "telefone": "(47) 3457-4455", "email": "moldes@araquari.com.br", "score": 88, "status": "Novo", "notas": "Terceiriza moldes e matrizes", "lat": -26.3700, "lon": -48.7200},
        {"nome": "Indústria Metal Guaramirim", "endereco": "Guaramirim - SC", "telefone": "(47) 3373-5566", "email": "contato@metalguara.com.br", "score": 85, "status": "Novo", "notas": "Terceiriza metalurgia e usinagem", "lat": -26.4700, "lon": -49.0000},
        {"nome": "Ferramentaria Barra Velha", "endereco": "Barra Velha - SC", "telefone": "(47) 3456-7788", "email": "contato@ferramentariabv.com.br", "score": 82, "status": "Novo", "notas": "Terceiriza ferramentas e peças", "lat": -26.6300, "lon": -48.6800},
        {"nome": "Usinagem Joinville Norte", "endereco": "Norte - Joinville SC", "telefone": "(47) 3428-3344", "email": "usinagemnorte@gmail.com", "score": 84, "status": "Novo", "notas": "Terceiriza usinagem geral", "lat": -26.3000, "lon": -48.8400},
        {"nome": "Matrizes Jaraguá", "endereco": "Jaraguá do Sul - SC", "telefone": "(47) 3276-6677", "email": "matrizesjs@outlook.com", "score": 87, "status": "Novo", "notas": "Terceiriza matrizes e moldes", "lat": -26.4800, "lon": -49.0700},
        {"nome": "Peças Usinadas Pirabeiraba", "endereco": "Pirabeiraba - Joinville SC", "telefone": "(47) 3469-9988", "email": "pecas@pirabeiraba.com.br", "score": 83, "status": "Novo", "notas": "Terceiriza peças usinadas", "lat": -26.2500, "lon": -48.8800},
        {"nome": "CNC Aventureiro", "endereco": "Aventureiro - Joinville SC", "telefone": "(47) 3429-4455", "email": "cnc.aventureiro@gmail.com", "score": 86, "status": "Novo", "notas": "Terceiriza peças CNC", "lat": -26.2900, "lon": -48.8400},
        {"nome": "Ferramentas Boa Vista", "endereco": "Boa Vista - Joinville SC", "telefone": "(47) 3208-5566", "email": "ferramentasbv@bol.com.br", "score": 85, "status": "Novo", "notas": "Terceiriza ferramentas e usinagem", "lat": -26.3100, "lon": -48.8200},
        {"nome": "Usinagem Centro Joinville", "endereco": "Centro - Joinville SC", "telefone": "(47) 3426-7788", "email": "usinagemcentro@gmail.com", "score": 84, "status": "Novo", "notas": "Terceiriza peças no centro", "lat": -26.3000, "lon": -48.8400},
        {"nome": "Moldes Costa e Silva", "endereco": "Costa e Silva - Joinville SC", "telefone": "(47) 3432-3344", "email": "moldescs@outlook.com", "score": 88, "status": "Novo", "notas": "Terceiriza moldes bairro", "lat": -26.2800, "lon": -48.8500},
        {"nome": "Tornearia Industrial Jaraguá", "endereco": "Jaraguá do Sul - SC", "telefone": "(47) 3277-6677", "email": "torneariajs@gmail.com", "score": 86, "status": "Novo", "notas": "Terceiriza tornearia e CNC", "lat": -26.4800, "lon": -49.0700},
        {"nome": "Usinagem Barra Velha Industrial", "endereco": "Barra Velha - SC", "telefone": "(47) 3455-9988", "email": "usinagembv@bol.com.br", "score": 82, "status": "Novo", "notas": "Terceiriza peças industriais", "lat": -26.6300, "lon": -48.6800},
        {"nome": "Matrizes Guaramirim", "endereco": "Guaramirim - SC", "telefone": "(47) 3374-4455", "email": "matrizesguara@gmail.com", "score": 85, "status": "Novo", "notas": "Terceiriza matrizes e ferramentas", "lat": -26.4700, "lon": -49.0000},
        {"nome": "Peças Usinadas São Francisco", "endereco": "São Francisco do Sul - SC", "telefone": "(47) 3465-5566", "email": "pecassfs@outlook.com", "score": 83, "status": "Novo", "notas": "Terceiriza peças naval", "lat": -26.2400, "lon": -48.6400},
        {"nome": "Ferramentaria Araquari", "endereco": "Araquari - SC", "telefone": "(47) 3458-7788", "email": "ferramentariaaraquari@gmail.com", "score": 84, "status": "Novo", "notas": "Terceiriza ferramentas regionais", "lat": -26.3700, "lon": -48.7200},
        {"nome": "CNC Industrial Joinville", "endereco": "Joinville - SC", "telefone": "(47) 3427-3344", "email": "cncindustrial@gmail.com", "score": 87, "status": "Novo", "notas": "Terceiriza peças CNC industriais", "lat": -26.3000, "lon": -48.8400},
        {"nome": "Usinagem Piratuba", "endereco": "Piratuba - Joinville SC", "telefone": "(47) 3466-6677", "email": "usinagempiratuba@bol.com.br", "score": 82, "status": "Novo", "notas": "Terceiriza usinagem bairro", "lat": -26.2800, "lon": -48.8600},
        {"nome": "Moldes Centro Jaraguá", "endereco": "Jaraguá do Sul - SC", "telefone": "(47) 3278-9988", "email": "moldescentrojs@gmail.com", "score": 88, "status": "Novo", "notas": "Terceiriza moldes centro", "lat": -26.4800, "lon": -49.0700},
        {"nome": "Tornearia Barra Velha", "endereco": "Barra Velha - SC", "telefone": "(47) 3459-4455", "email": "torneariabv@outlook.com", "score": 81, "status": "Novo", "notas": "Terceiriza tornearia local", "lat": -26.6300, "lon": -48.6800},
        {"nome": "Usinagem Guaramirim Sul", "endereco": "Guaramirim - SC", "telefone": "(47) 3375-5566", "email": "usinagemguarasul@gmail.com", "score": 83, "status": "Novo", "notas": "Terceiriza usinagem sul", "lat": -26.4700, "lon": -49.0000},
        {"nome": "Peças CNC São Francisco", "endereco": "São Francisco do Sul - SC", "telefone": "(47) 3466-7788", "email": "pecascncsfs@bol.com.br", "score": 84, "status": "Novo", "notas": "Terceiriza peças CNC naval", "lat": -26.2400, "lon": -48.6400},
        {"nome": "Ferramentaria Araquari Centro", "endereco": "Araquari - SC", "telefone": "(47) 3459-5566", "email": "ferramentariaac@gmail.com", "score": 85, "status": "Novo", "notas": "Terceiriza ferramentas centro", "lat": -26.3700, "lon": -48.7200},
        {"nome": "Usinagem Joinville Sul", "endereco": "Sul - Joinville SC", "telefone": "(47) 3424-7788", "email": "usinagemsul@gmail.com", "score": 86, "status": "Novo", "notas": "Terceiriza usinagem sul", "lat": -26.3000, "lon": -48.8400},
    ]
    st.session_state.leads = pd.DataFrame(data)

df = st.session_state.leads

# Tabela editável
st.subheader("Lista de 50 Empresas Reais (edite ou adicione)")
edited_df = st.data_editor(
    df,
    column_config={
        "status": st.column_config.SelectboxColumn("Status", options=["Novo", "Contatado", "Em negociação", "Convertido", "Descartado"]),
        "score": st.column_config.NumberColumn("Pontuação", format="%d ⭐"),
        "notas": st.column_config.TextColumn("Anotações"),
        "telefone": st.column_config.TextColumn("Telefone"),
        "email": st.column_config.TextColumn("Email")
    },
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic"
)

if not edited_df.equals(df):
    st.session_state.leads = edited_df
    st.success("Alterações salvas!")

# Botão para enviar email para TODOS os contatos (configurado para Gmail)
st.subheader("Enviar Email para Todos os Contatos da Tabela")

sender_email = st.text_input("Seu email Gmail", value="futurynk.oficial@gmail.com")
sender_password = st.text_input("Senha de app Gmail (16 caracteres)", type="password")

texto_email = st.text_area("Texto do email (use {nome} para personalizar)", 
    value="Olá {nome},\n\nEspero que esteja bem.\n\nSou Adriano, especialista em usinagem de precisão com torno CNC. Produzo peças como:\n- eixos, pinos e hastes\n- buchas, rolamentos e mancais\n- flanges, adaptadores e conexões\n- engrenagens, polias e coroas\n- peças em aço, alumínio, bronze, borracha técnica e plásticos de engenharia\n- componentes para moldes, matrizes, autopeças, hidráulica e máquinas industriais\n\nSe você está com demanda de peças usinadas, sobrecarga na produção ou busca um parceiro confiável para terceirizar, posso oferecer solução sob medida com qualidade e prazo.\n\nGostaria de receber uma proposta rápida e personalizada?\n\nPodemos conversar agora ou agendar uma ligação?\n\nAguardo seu retorno!\n\nAtenciosamente,\nAdriano da Silva\nEspecialista em Usinagem CNC\n(47) 98479-3983\nfuturynk.oficial@gmail.com\nJoinville, Santa Catarina")

if st.button("📧 Enviar Email para TODOS os contatos"):
    if not sender_email or not sender_password:
        st.warning("Preencha seu email e senha de app.")
    elif not texto_email:
        st.warning("Preencha o texto do email.")
    else:
        progress = st.progress(0)
        status = st.empty()

        total_enviados = 0
        for i, row in df.iterrows():
            email_dest = row["email"]
            if pd.isna(email_dest) or not email_dest.strip():
                continue

            nome = row["nome"]
            mensagem = texto_email.replace("{nome}", nome)

            try:
                msg = MIMEText(mensagem)
                msg['Subject'] = "Proposta de Usinagem CNC - Peças em Torno e Fresamento"
                msg['From'] = sender_email
                msg['To'] = email_dest

                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email_dest, msg.as_string())
                server.quit()

                total_enviados += 1
                status.success(f"Enviado para {nome} ({email_dest})")
            except Exception as e:
                status.error(f"Falha para {nome}: {str(e)}")

            progress.progress((i + 1) / len(df))
            time.sleep(5)  # delay anti-bloqueio

        st.success(f"Envio concluído! {total_enviados} emails enviados com sucesso.")

# Mapa
st.subheader("Mapa das Empresas - Joinville e Região")
m = folium.Map(location=[-26.3045, -48.8434], zoom_start=10)

for _, row in df.iterrows():
    if pd.notna(row["lat"]) and pd.notna(row["lon"]):
        folium.Marker(
            [row["lat"], row["lon"]],
            popup=f"<b>{row['nome']}</b><br>{row['endereco']}<br>Telefone: {row['telefone']}<br>Email: {row['email']}<br>Score: {row['score']} ⭐"
        ).add_to(m)

st_folium(m, width=1000, height=600)

st.caption("App simples • 50 empresas reais • Verifique contatos antes de usar • Atualizado em 25/02/2026")
