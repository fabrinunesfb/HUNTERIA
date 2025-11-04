import streamlit as st
import json
import time

# --- Mockup (Simulação) das Funções do Back-end ---
# No produto real, isso faz chamadas de API para o Módulo 1 e 3.

def mock_parse_cv(cv_text):
    """
    Simula o Módulo 3 (Parser de CV) que testamos.
    """
    if "Fabrício Nunez" in cv_text:
        return {
            "profile_summary": "CMO | Head de Marketing, Branding & Growth com +17 anos de experiência.",
            "hard_skills": ["Branding", "Growth", "Marketing de Performance", "Gestão de P&L", "Rebranding", "Análise de Dados", "Geração de Leads", "SEO"],
            "soft_skills": ["Liderança Executiva", "Liderança de Times Multidisciplinares", "Visão Estratégica", "Visão de Negócio"],
            "domain_expertise": ["iGaming", "Fintech", "Tech (Startups)", "SaaS", "Varejo"]
        }
    # Perfil genérico para outros testes
    return {
        "profile_summary": "Usuário de Teste",
        "hard_skills": ["Python", "SQL", "AWS"],
        "soft_skills": ["Comunicação", "Scrum"],
        "domain_expertise": ["Tech"]
    }

def mock_get_matches(profile_json):
    """
    Simula os Módulos 1 (Gupy + Google) e o Matcher,
    retornando as vagas que encontramos nos Sprints.
    """
    vagas_db = [
        {
            "id": "v1",
            "title": "Head de Growth & Branding",
            "company": "FintechConfia (via Gupy)",
            "location": "São Paulo (Híbrido)",
            "url": "https://www.gupy.io/", # Link de exemplo
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
            "url": "https://www.google.com/", # Link de exemplo
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
            "url": "https://www.google.com/", # Link de exemplo
            "fit_score": 85,
            "justification": {
                "match": "Match Forte: iGaming, Liderança Executiva, Gestão de P&L.",
                "gap": "Gap Identificado: Exige experiência com regulação de mercados europeus."
            }
        }
    ]
    
    # Filtra vagas baseadas no perfil (simples)
    if "iGaming" in profile_json.get("domain_expertise", []):
        return vagas_db
    else:
        return [vagas_db[1]] # Retorna só a vaga de SaaS

# --- Configuração da Página (Front-End) ---
st.set_page_config(
    page_title="HunterDash v1.0",
    page_icon="🎯",
    layout="wide"
)

# --- Armazenamento da Sessão ---
# Usamos o st.session_state para "lembrar" do usuário (Sprint 4)
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'saved_jobs' not in st.session_state:
    st.session_state.saved_jobs = {} # Usamos um dict para evitar duplicatas

# --- Renderização do Front-End (O App) ---

st.title("🎯 HunterDash v1.0")
st.caption("Seu Agente de Vagas Autônomo")

# --- Visão 1: Upload do CV (Se ainda não foi feito) ---
if st.session_state.profile is None:
    st.header("Passo 1: Ative seu Agente de IA")
    cv_text = st.text_area("Cole seu CV ou perfil do LinkedIn aqui para análise:", height=250)
    
    if st.button("Analisar Perfil e Buscar Vagas"):
        if not cv_text:
            st.error("Por favor, cole seu perfil para análise.")
        else:
            with st.spinner("Seu Agente está analisando seu perfil... (Módulo 3)"):
                time.sleep(1) # Simula o parse
                st.session_state.profile = mock_parse_cv(cv_text)
            
            with st.spinner("Seu Agente está varrendo o mercado... (Módulo 1)"):
                time.sleep(2) # Simula a busca
                st.session_state.matches = mock_get_matches(st.session_state.profile)
            
            st.success("Perfil analisado e vagas encontradas! Recarregando...")
            st.rerun() # Força a recarga da página para a visão de "Matches"

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

                    with st.expander("Ver Justificativa da IA (Por que 92%?)"):
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
