import streamlit as st

def inject_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root{--bg:#0B1020;--side:#111827;--card:#1B2336;--purple:#8B5CF6;--lav:#A78BFA;--blue:#38BDF8;--text:#F8FAFC;--muted:#CBD5E1;--border:#334155}
    html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--text)}
    .stApp{background:var(--bg)} .main .block-container{max-width:1500px;padding:2rem 2.4rem 3rem}
    [data-testid="stSidebar"]{background:var(--side);border-right:1px solid var(--border)} [data-testid="stSidebar"] .block-container{padding:1.5rem 1rem}
    h1,h2,h3{font-family:'Manrope',sans-serif;color:var(--text)!important;letter-spacing:-.02em} h1{font-size:2rem!important} h2{font-size:1.35rem!important}
    p, label, span, div{ } .stCaption, small{color:var(--muted)!important}
    [data-testid="stMetric"]{background:var(--card);border:1px solid var(--border);padding:18px 20px;border-radius:14px}
    [data-testid="stMetricLabel"]{color:var(--muted)!important;font-size:.88rem!important;font-weight:600}
    [data-testid="stMetricValue"]{color:var(--text)!important;font-family:'Manrope',sans-serif;font-size:1.8rem!important;font-weight:800}
    div[data-baseweb="select"]>div, input, [data-baseweb="popover"]{background:#172033!important;color:var(--text)!important;border-color:var(--border)!important}
    [data-baseweb="tag"]{background:#453174!important;color:white!important} [role="option"]{background:#172033!important;color:var(--text)!important}
    button[kind="secondary"],.stButton>button{background:#202a40;color:var(--text);border:1px solid var(--border);border-radius:9px;font-weight:600}
    .stButton>button:hover{border-color:var(--lav);color:white}
    [data-testid="stTabs"] button{color:var(--muted)} [data-testid="stTabs"] button[aria-selected="true"]{color:var(--lav)}
    [data-testid="stDataFrame"]{border:1px solid var(--border);border-radius:10px;overflow:hidden}
    [data-testid="stExpander"]{border-color:var(--border);background:#121a2a;border-radius:10px}
    hr{border-color:var(--border)}
    .brand{font:800 1.7rem 'Manrope',sans-serif;letter-spacing:.13em;color:white;margin:0}.brand em{font-style:normal;color:var(--lav)}
    .eyebrow{color:var(--blue);font-size:.72rem;letter-spacing:.16em;font-weight:700;text-transform:uppercase}
    .subhead{color:var(--muted);margin-top:-.7rem;font-size:.95rem}
    .note{background:#211b35;border:1px solid #57427f;border-left:4px solid var(--lav);border-radius:9px;padding:12px 15px;color:#E9DFFF;font-size:.9rem}
    .section-label{font:700 .75rem 'DM Sans';color:var(--muted);letter-spacing:.1em;text-transform:uppercase;margin:1.2rem 0 .5rem}
    @media(max-width:900px){.main .block-container{padding:1.2rem 1rem}.stMetricValue{font-size:1.4rem!important}}
    </style>""", unsafe_allow_html=True)


