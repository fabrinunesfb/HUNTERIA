import streamlit as st
import json
import time
import PyPDF2 # Importa a nova biblioteca de PDF
import io

# --- Mockup (Simulação) das Funções do Back-end ---
# No produto real, isso faz chamadas de API para o Módulo 1 e 3.

def mock_parse_cv(cv_text):
    """
    Simula o Módulo 3 (Parser de CV) que testamos.
    Agora ele reage ao texto extraído do PDF.
    """
    # Gatilho para o seu perfil (o mais importante)
    if "Fabrício Nunez" in cv_text or "iGaming" in cv_text or "SeuBet" in cv_text:
        return {
            "profile_summary": "CMO | Head de Marketing, Branding & Growth com +17 anos de experiência.",
            "hard_skills": ["Branding", "Growth", "Marketing de Performance", "Gestão de P&L", "Rebranding", "Análise de Dados", "Geração de Leads", "SEO"],
            "soft_skills": ["Liderança Executiva", "Liderança de Times Multidisciplinares", "Visão Estratégica", "Visão de Negócio"],
            "domain_expertise": ["iGaming", "Fintech", "Tech (Startups)", "SaaS", "Varejo"]
        }
    
    # Perfil genérico para outros testes (ex: PDF de um Dev)
    if "Python" in cv_text or "SQL" in cv_text:
        return {
            "profile_summary": "Desenvolvedor de Software",
            "hard_skills": ["Python", "SQL", "AWS", "FastAPI"],
            "soft_skills": ["Comunicação", "Scrum"],
            "domain_expertise": ["Tech", "SaaS"]
        }
    
    # Perfil padrão se não achar nada
    return {
        "profile_summary": "Usuário de Teste",
        "hard_skills": ["Pacote Office"],
        "soft_skills": ["Proatividade"],
        "domain_expertise": ["Geral"]
    }

def mock_get_matches(profile_json):
    """
    Simula os Módulos 1 (Gupy + Google) e o Matcher.
    """
    vagas_db = [
        {
            "id": "v1",
            "title": "Head de Growth & Branding",
            "company": "FintechConfia (via Gupy)",
            "location": "São Paulo (Híbrido)",
            "url": "https://www.google.com/search?q=vaga+head+growth+branding+fintechconfia", # Link Simulado
            "fit_score": 92,
            "justification": {
                "match": "Match Forte: Fintech, Branding, Growth, Liderança de Times.",
                "gap": "Gap Identificado: A vaga cita HubSpot e Salesforce."
            }
        },
        {
            "id": "v2",
            "title": "Head of Marketing and Growth",
            "company": "Mova (Startup SaaS - Site Próprio)",
            "location": "Remoto (Brasil)",
            "url": "https://www.google.com/search?q=vaga+head+marketing+growth+mova+saas", # Link Simulado
            "fit_score": 88,
            "justification": {
                "match": "Match Forte: SaaS, Geração de Leads (B2B), Otimização de CAC.",
                "gap": "Gap de Foco: A vaga é 100% focada em Growth; Branding não é mencionado."
            }
        },
        {
            "id": "v3",
            "title": "CMO (Chief Marketing Officer)",
            "company": "iGaming Solutions (via Google)",
            "location": "Remoto",
            "url": "https://www.google.com/search?q=vaga+cmo+igaming+solutions", # Link Simulado
            "fit_score": 85,
            "justification": {
                "match": "Match Forte: iGaming, Liderança Executiva, Gestão de P&L.",
                "gap": "Gap Identificado: Exige experiência com regulação de mercados europeus."
            }
        }
    ]
    
    # Filtra vagas baseadas no perfil (simples)
    profile_domains = profile_json.get("domain_expertise", [])
    matches = []
    
    if "iGaming" in profile_domains or "Fintech" in profile_domains:
        matches.append(vagas_db[0]) # Vaga Fintech
        matches.append(vagas_db[2]) # Vaga iGaming
    if "SaaS" in profile_domains or "Tech" in profile_domains:
         matches.append(vagas_db[1]) # Vaga SaaS
    
    if not matches: # Se for um perfil genérico
        return vagas_db # Retorna tudo
        
    return matches

def extract_text_from_pdf(pdf_file):
    """
    Função real para ler o texto de um PDF.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Erro ao ler o PDF: {e}")
        return None

# --- Configuração da Página (Front-End) ---
st.set_page_config(
    page_title="HunterDash v1.0",
    page_icon="🎯",
    layout="wide"
)

# --- Armazenamento da Sessão ---
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'saved_jobs' not in st.session_state:
    st.session_state.saved_jobs = {} 

# --- Renderização do Front-End (O App) ---

st.title("🎯 HunterDash v1.0")
st.caption("Seu Agente de Vagas Autônomo")

# --- Visão 1: Upload do CV (Se ainda não foi feito) ---
if st.session_state.profile is None:
    st.header("Passo 1: Ative seu Agente de IA")
    
    # (SPRINT 6) - Trocamos o text_area por file_uploader
    uploaded_file = st.file_uploader(
        "Faça o upload do seu CV em PDF para análise:",
        type=["pdf"]
    )
    
    st.markdown("---")
    st.markdown("*(Obs: Links do LinkedIn não são suportados nesta versão de teste)*")
    
    if uploaded_file is not None:
        with st.spinner("Seu Agente está lendo seu PDF..."):
            cv_text = extract_text_from_pdf(uploaded_file)
            
        if cv_text:
            st.success("PDF lido com sucesso!")
            with st.spinner("Analisando seu perfil... (Módulo 3)"):
                time.sleep(1) # Simula o parse
                st.session_state.profile = mock_parse_cv(cv_text)
            
            with st.spinner("Seu Agente está varrendo o mercado... (Módulo 1)"):
                time.sleep(2) # Simula a busca
                st.session_state.matches = mock_get_matches(st.session_state.profile)
            
            st.success("Perfil analisado e vagas encontradas! Recarregando...")
            time.sleep(1)
            st.rerun() # Comando corrigido

# --- Visão 2: O Dashboard (Se o perfil já existe) ---
else:
    # Definindo as abas (Sprint 4)
    tab_feed, tab_saved = st.tabs(["🔥 Feed de Matches", f"💾 Vagas Salvas ({len(st.session_state.saved_jobs)})"])

    # --- Aba 1: Feed de Matches ---
    with tab_feed:
        st.subheader("Novas Vagas com Alto 'Fit Score'")
        st.caption(f"Olá! Seu Agente encontrou {len(st.session_state.matches)} vagas compatíveis.")
        
        if not st.session_state.matches:
            st.info("Nenhuma vaga nova encontrada no momento. O Agente rodará novamente em breve.")
            
        for vaga in st.session_state.matches:
            job_id = vaga["id"]
            if job_id not in st.session_state.saved_jobs: # Só mostra se não foi salva
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"<h4>{vaga['title']}</h4>", unsafe_allow_html=True)
                        st.markdown(f"**Empresa:** {vaga['company']} | **Local:** {vaga['location']}")
                    
                    with col2:
                        st.metric(label="Fit Score", value=f"{vaga['fit_score']}%")

                    with st.expander(f"Ver Justificativa da IA (Por que {vaga['fit_score']}%)"):
                        st.success(f"✅ {vaga['justification']['match']}")
                        st.warning(f"⚠️ {vaga['justification']['gap']}")
                    
                    # Botões (Sprint 2)
                    col_btn1, col_btn2 = st.columns(2)
                    col_btn1.link_button("Ver Vaga (Link Externo)", vaga['url'], use_container_width=True)
                    
                    # Botão "Salvar" (Sprint 4)
                    if col_btn2.button("Salvar Vaga", key=f"save_{job_id}", use_container_width=True):
                        st.session_state.saved_jobs[job_id] = vaga
                        st.toast(f"Vaga '{vaga['title']}' salva!")
                        time.sleep(1)
                        st.rerun() # Recarrega para mover o card
                    
                    st.divider()

    # --- Aba 2: Vagas Salvas ---
    with tab_saved:
        st.subheader("Suas Vagas Salvas para Aplicação")
        
        if not st.session_state.saved_jobs:
            st.info("Você ainda não salvou nenhuma vaga. Clique em 'Salvar Vaga' no Feed.")
            
        for job_id, vaga in st.session_state.saved_jobs.items():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"<h4>{vaga['title']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"**Empresa:** {vaga['company']} | **Local:** {vaga['location']}")
                with col2:
                    st.metric(label="Fit Score", value=f"{vaga['fit_score']}%")
                
                col_btn1, col_btn2 = st.columns(2)
                col_btn1.link_button("Ir para a Vaga (Aplicar)", vaga['url'], use_container_width=True)
                
                if col_btn2.button("Remover", key=f"remove_{job_id}", use_container_width=True):
                    del st.session_state.saved_jobs[job_id]
                    st.toast("Vaga removida.")
                    st.rerun()
                st.divider()
