import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os
from PIL import Image
import io

from translations import TRANSLATIONS

st.set_page_config(
    page_title="Espécies Invasoras · Isla Navarino",
    page_icon="🦫",
    layout="wide"
)

# ============================================================
# SISTEMA DE IDIOMAS (10 idiomas)
# ============================================================
LANGS = [
    ("pt", "🇧🇷", "PT"), ("en", "🇺🇸", "EN"), ("es", "🇪🇸", "ES"),
    ("it", "🇮🇹", "IT"), ("fr", "🇫🇷", "FR"), ("de", "🇩🇪", "DE"),
    ("zh", "🇨🇳", "ZH"), ("ar", "🇸🇦", "AR"), ("el", "🇬🇷", "EL"),
    ("af", "🇿🇦", "AF"),
]
CODES = [c for c, _, _ in LANGS]
FLAGS = {c: f"{flag} {label}" for c, flag, label in LANGS}

DECIMAL = {"pt": ",", "en": ".", "es": ",", "it": ",", "fr": ",", "de": ",", "zh": ".", "ar": ".", "el": ",", "af": ","}
PLOTLY_SEP = {"pt": ",.", "en": ".,", "es": ",.", "it": ",.", "fr": ", ", "de": ",.", "zh": ".,", "ar": ".,", "el": ",.", "af": ", "}

def _initial_lang():
    q = st.query_params.get("lang")
    if isinstance(q, list):
        q = q[0] if q else None
    return q if q in CODES else "pt"

if "lang" not in st.session_state:
    st.session_state.lang = _initial_lang()

def render_lang_selector():
    try:
        escolha = st.pills(
            "Language", CODES, selection_mode="single",
            default=st.session_state.lang, format_func=lambda c: FLAGS[c],
            key="lang_pick", label_visibility="collapsed",
        )
    except AttributeError:
        escolha = st.radio(
            "Language", CODES, index=CODES.index(st.session_state.lang),
            format_func=lambda c: FLAGS[c], horizontal=True,
            key="lang_pick", label_visibility="collapsed",
        )
    if escolha and escolha != st.session_state.lang:
        st.session_state.lang = escolha
        st.query_params["lang"] = escolha
        st.rerun()

render_lang_selector()
LANG = st.session_state.lang
T = TRANSLATIONS[LANG]
RTL = LANG == "ar"

def fmt(x, nd=1):
    return f"{x:.{nd}f}".replace(".", DECIMAL[LANG])

def plot(fig):
    fig.update_layout(separators=PLOTLY_SEP[LANG])
    try:
        st.plotly_chart(fig, use_container_width=True)
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)

# ── ESTILOS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&family=Noto+Serif:wght@700&family=Noto+Sans:wght@400;500&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Naskh+Arabic:wght@400;700&display=swap');
:root{
  --forest:#1B3A1E;--forest-mid:#2D5A32;--forest-light:#3D7A45;
  --earth:#5C3D1E;--earth-mid:#7A5230;--earth-light:#A06A3A;
  --water:#1A5C8A;--water-light:#2D8FBF;
  --ice:#D4EEF7;--cream:#F5F2EC;--warm-gray:#7A7060;
  --danger:#8B2515;--black:#0D1117;
}
html,body,[class*="css"]{font-family:'DM Sans','Noto Sans','Noto Sans SC','Noto Naskh Arabic',sans-serif;background-color:var(--cream);color:var(--black);}
.hero-wrap{background:linear-gradient(135deg,var(--forest) 0%,var(--forest-mid) 55%,#1A4A20 100%);border-radius:20px;padding:3rem 2.5rem 2rem;margin-bottom:2rem;position:relative;overflow:hidden;}
.hero-wrap::before{content:"🦫";font-size:180px;position:absolute;right:-10px;top:-20px;opacity:0.06;}
.hero-tag{background:#A8D5A2;color:var(--forest);font-family:'DM Mono',monospace;font-size:0.7rem;font-weight:bold;letter-spacing:2px;padding:4px 12px;border-radius:4px;display:inline-block;margin-bottom:1rem;text-transform:uppercase;}
.hero-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:2.8rem;font-weight:900;color:#fff;line-height:1.15;margin-bottom:0.8rem;white-space:pre-line;}
.hero-subtitle{font-size:1rem;color:rgba(255,255,255,0.78);max-width:680px;line-height:1.6;margin-bottom:1.5rem;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.85);font-size:0.72rem;font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;padding:5px 12px;border-radius:20px;letter-spacing:0.5px;}
.badge-forest{background:rgba(168,213,162,0.2);border-color:#A8D5A2;color:#A8D5A2;}
.metric-box{background:white;border-radius:16px;padding:1.4rem 1.2rem;border-top:4px solid var(--forest-light);box-shadow:0 2px 12px rgba(0,0,0,0.06);text-align:center;}
.metric-box.earth{border-top-color:var(--earth-light);}
.metric-box.water{border-top-color:var(--water-light);}
.metric-box.danger{border-top-color:var(--danger);}
.metric-val{font-family:'Playfair Display','Noto Serif',serif;font-size:2.1rem;font-weight:900;color:var(--forest);line-height:1;margin-bottom:0.3rem;}
.metric-label{font-size:0.75rem;color:var(--warm-gray);text-transform:uppercase;letter-spacing:1px;}
.section-label{font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;font-size:0.65rem;color:var(--forest-mid);text-transform:uppercase;letter-spacing:3px;margin-bottom:0.3rem;}
.section-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.9rem;font-weight:700;color:var(--forest);margin-bottom:1.2rem;line-height:1.2;}
.info-card{background:white;border-radius:16px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.05);border-left:4px solid var(--forest-light);margin-bottom:1rem;}
.info-card.earth{border-left-color:var(--earth-light);}
.info-card.water{border-left-color:var(--water-light);}
.info-card.danger{border-left-color:var(--danger);}
.timeline-item{display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid #e8ede8;}
.timeline-year{font-family:'Playfair Display','Noto Serif',serif;font-size:1rem;font-weight:700;color:var(--forest-mid);min-width:80px;}
.timeline-title{font-weight:500;color:var(--forest);margin-bottom:0.2rem;}
.timeline-desc{font-size:0.85rem;color:var(--warm-gray);}
.source-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:0.8rem;}
.source-badge{background:var(--forest);color:white;font-family:'DM Mono',monospace;font-size:0.65rem;padding:4px 10px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;}
.method-step{display:flex;align-items:flex-start;gap:1rem;padding:1rem;background:white;border-radius:12px;margin-bottom:0.8rem;box-shadow:0 1px 6px rgba(0,0,0,0.04);}
.step-num{background:var(--forest-mid);color:white;font-family:'Playfair Display','Noto Serif',serif;font-size:1.1rem;font-weight:700;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step-title{font-weight:500;color:var(--forest);font-size:0.95rem;}
.step-desc{font-size:0.82rem;color:var(--warm-gray);margin-top:0.2rem;}
.discovery-box{background:linear-gradient(135deg,#EEF5EE,#DCF0DC);border:2px solid var(--forest-light);border-radius:16px;padding:1.8rem;margin:0.8rem 0;}
.discovery-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.1rem;font-weight:700;color:var(--forest);margin-bottom:0.5rem;}
.footer-wrap{background:var(--forest);border-radius:20px;padding:2rem;color:rgba(255,255,255,0.8);text-align:center;margin-top:3rem;}
.footer-title{font-family:'Playfair Display','Noto Serif',serif;color:#A8D5A2;font-size:1.2rem;margin-bottom:0.5rem;}
.photo-placeholder{background:#EEF5EE;border:2px dashed var(--forest-light);border-radius:12px;padding:2rem;text-align:center;min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.photo-emoji{font-size:2.5rem;}
.photo-title{font-weight:600;color:var(--forest);margin:0.5rem 0 0.2rem;font-size:0.9rem;}
.photo-desc{font-size:0.78rem;color:var(--warm-gray);line-height:1.5;}
.photo-path{font-size:0.65rem;color:var(--forest-mid);font-family:'DM Mono',monospace;margin-top:0.5rem;background:#DCF0DC;padding:3px 8px;border-radius:4px;direction:ltr;}
.photo-legenda{font-size:0.72rem;color:var(--warm-gray);font-style:italic;padding:0.5rem 0.8rem;background:#f5f5f0;text-align:center;border-top:1px solid #d8e8d8;}
.photo-destaque{border:3px solid var(--forest-light);border-radius:14px;overflow:hidden;box-shadow:0 4px 20px rgba(45,90,50,0.15);}
</style>
""", unsafe_allow_html=True)

if RTL:
    st.markdown("""
<style>
[data-testid="stMain"], [data-testid="stAppViewContainer"] .main { direction: rtl; text-align: right; }
.hero-wrap, .info-card, .method-step, .discovery-box, .timeline-item { direction: rtl; text-align: right; }
.hero-wrap::before { right: auto; left: -20px; }
.info-card, .info-card.earth, .info-card.water, .info-card.danger { border-left: none; border-right: 4px solid var(--forest-light); }
.js-plotly-plot, iframe { direction: ltr; }
body, html, [class*="css"] { font-family: 'Noto Naskh Arabic','DM Sans',sans-serif; }
</style>
""", unsafe_allow_html=True)

# ── DADOS ─────────────────────────────────────────────────────
anos = [1946,1950,1955,1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2020,2025]
castores = [20,120,500,1500,4000,8000,15000,25000,40000,60000,75000,85000,95000,100000,105000,108000,110000]
ha_destruidos = [0,5,20,80,200,500,1200,2500,5000,9000,14000,19000,24000,27000,29000,30500,31000]

heat_data = [
    [-54.93, -67.61, 0.9], [-54.96, -67.58, 0.85], [-55.02, -67.45, 0.7], [-55.10, -67.70, 0.75],
    [-54.88, -67.82, 0.8], [-55.15, -67.52, 0.65], [-54.85, -67.40, 0.6], [-55.20, -67.65, 0.72],
    [-54.78, -67.75, 0.55], [-55.08, -67.30, 0.5], [-55.25, -67.80, 0.68], [-54.95, -67.90, 0.62],
    [-55.18, -67.38, 0.58], [-54.82, -67.55, 0.45], [-55.30, -67.60, 0.7], [-55.05, -68.00, 0.65],
    [-54.90, -68.10, 0.5],
]

pontos_campo = [
    {"nome": "Castoreira 1 — Puerto Williams (mais próxima da cidade)", "lat": -54.930, "lon": -67.612, "tipo": "castoreira", "cor": "orange", "icon": "paw", "desc": "Castoreira mais próxima do centro de Puerto Williams."},
    {"nome": "Castoreira 2 — Próxima à Laguna Rosa", "lat": -54.963, "lon": -67.581, "tipo": "castoreira", "cor": "red", "icon": "paw", "desc": "Segunda castoreira visitada, próxima à Laguna Rosa."},
    {"nome": "Puerto Williams — Base de Observação", "lat": -54.935, "lon": -67.616, "tipo": "base", "cor": "blue", "icon": "home", "desc": "Cidade de Puerto Williams — base dos 8 meses de residência."},
    {"nome": "3ª Conferência CHIC 2025", "lat": -54.934, "lon": -67.617, "tipo": "conferencia", "cor": "green", "icon": "graduation-cap", "desc": "Local da 3ª Conferência Internacional CHIC realizada em 2025."},
]

# ── HERO ──────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-tag">{T['hero_tag']}</div>
  <div class="hero-title">{T['hero_title']}</div>
  <div class="hero-subtitle">{T['hero_subtitle']}</div>
  <div class="hero-badges">
    <span class="badge badge-forest">{T['badge1']}</span>
    <span class="badge badge-forest">{T['badge2']}</span>
    <span class="badge">{T['badge3']}</span>
    <span class="badge">{T['badge4']}</span>
    <span class="badge">{T['badge5']}</span>
  </div>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-box danger"><div class="metric-val">110.000+</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-box earth"><div class="metric-val">70.600</div><div class="metric-label">{T["m2"]}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-box"><div class="metric-val">31.000 ha</div><div class="metric-label">{T["m3"]}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-box water"><div class="metric-val">1946</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ABAS ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([T['tab1'], T['tab2'], T['tab3'], T['tab4'], T['tab5']])

# ── TAB 1: MAPA ───────────────────────────────────────────────
with tab1:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-title" style="font-size:1.3rem">{T["map_title_top"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card">{T["map_hint_top"]}</div>', unsafe_allow_html=True)

    mapa_top = folium.Map(
        location=[-54.95, -67.65], zoom_start=10,
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery'
    )

    icon_map = {"castoreira": ("orange", "paw"), "base": ("blue", "home"), "conferencia": ("green", "graduation-cap")}
    for p in pontos_campo:
        cor, ico = icon_map[p["tipo"]]
        pop_html = f"""<div style='font-family:sans-serif;min-width:220px;padding:10px'>
            <h4 style='color:#1B3A1E;margin:0 0 6px;font-size:13px'>{p['nome']}</h4>
            <p style='font-size:11px;color:#555;margin:0'>{p['desc']}</p>
            <hr style='margin:6px 0;border-color:#eee'>
            <p style='font-size:10px;color:#999;margin:0'>Lat: {p['lat']:.4f} · Lon: {p['lon']:.4f}</p>
        </div>"""
        folium.Marker(
            location=[p["lat"], p["lon"]],
            popup=folium.Popup(pop_html, max_width=260),
            tooltip=p["nome"],
            icon=folium.Icon(color=cor, icon=ico, prefix="fa")
        ).add_to(mapa_top)

    folium_static(mapa_top, width=1100, height=480)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f'<div class="section-title" style="font-size:1.3rem">{T["map_title_heat"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card earth">{T["map_hint_heat"]}</div>', unsafe_allow_html=True)

    try:
        carto_key = st.secrets.get("CARTO_API_KEY", "")
    except Exception:
        carto_key = ""

    mapa_heat = folium.Map(location=[-55.0, -67.6], zoom_start=9, tiles=None, control_scale=True)

    if carto_key:
        folium.TileLayer(
            tiles=("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?key=" + carto_key),
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            name="CARTO Dark Matter", subdomains="abcd", max_zoom=20, overlay=False, control=True,
        ).add_to(mapa_heat)
    else:
        folium.TileLayer(
            "OpenStreetMap", name="OpenStreetMap",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            control=True,
        ).add_to(mapa_heat)
        
    HeatMap(
        data=heat_data, min_opacity=0.4, radius=35, blur=25,
        gradient={0.2: '#1B3A1E', 0.4: '#3D7A45', 0.65: '#F5A623', 0.85: '#E8340A', 1.0: '#FFFFFF'},
        name="Intensidade do Impacto"
    ).add_to(mapa_heat)

    for p in pontos_campo:
        folium.CircleMarker(
            location=[p["lat"], p["lon"]], radius=7, color='white', fill=True, fill_color='white',
            fill_opacity=0.9, weight=2, tooltip=p["nome"]
        ).add_to(mapa_heat)

    folium_static(mapa_heat, width=1100, height=420)

    st.markdown(f"<br><div class='section-label'>{T['chart_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['chart_title']}</div>", unsafe_allow_html=True)

    fig_pop = go.Figure()
    fig_pop.add_trace(go.Scatter(
        x=anos, y=castores, mode='lines+markers',
        line=dict(color='#8B2515', width=3),
        marker=dict(size=8, color='#8B2515', symbol='circle', line=dict(width=1, color='white')),
        fill='tozeroy', fillcolor='rgba(139,37,21,0.08)', name="Castores",
        hovertemplate='<b>%{x}</b><br>%{y:,.0f} castores<extra></extra>'
    ))
    fig_pop.add_vline(x=1946, line_dash="dash", line_color="#A06A3A", annotation_text="  1946: Introdução", annotation_font_color="#A06A3A")
    fig_pop.add_vline(x=2008, line_dash="dash", line_color="#2D5A32", annotation_text="  2008: Acordo de Erradicação", annotation_font_color="#2D5A32")
    fig_pop.add_annotation(x=2025, y=110000, text="🦫 2025: 110.000+", showarrow=False, font=dict(color="#8B2515", size=11, family="DM Mono"), xshift=-5, yshift=15)
    fig_pop.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(27,58,30,0.03)', font=dict(family='DM Sans'), height=360, showlegend=False,
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#e8ede8', title="Nº de castores (estimativa)"), margin=dict(t=30, b=20)
    )
    plot(fig_pop)

    col_a, col_b = st.columns(2)
    with col_a:
        fig_ha = go.Figure()
        fig_ha.add_trace(go.Bar(
            x=anos, y=ha_destruidos,
            marker=dict(color=ha_destruidos, colorscale=[[0,'#A8D5A2'],[0.4,'#3D7A45'],[0.7,'#A06A3A'],[1,'#8B2515']], line=dict(width=0)),
            hovertemplate='<b>%{x}</b><br>%{y:,.0f} ha<extra></extra>',
            text=[f"{v//1000}k" if v >= 1000 else str(v) for v in ha_destruidos], textposition='outside', textfont=dict(size=9, family="DM Mono", color="#5C3D1E")
        ))
        fig_ha.update_layout(
            title=dict(text=T['chart_title2'], font=dict(size=13, family='Playfair Display')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320, font=dict(family='DM Sans'), showlegend=False,
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#e8ede8', title="Hectares acumulados"), margin=dict(t=50, b=20)
        )
        plot(fig_ha)

    with col_b:
        especies = ["Castor<br>canadensis", "Arganazes<br>(muskrat)", "Martas<br>(mink)", "Fauna<br>nativa ⬇"]
        impacto = [100, 65, 45, -80]
        cores_casc = ['#8B2515','#A06A3A','#5C3D1E','#1A5C8A']
        fig_casc = go.Figure()
        for sp, imp, cor in zip(especies, impacto, cores_casc):
            fig_casc.add_trace(go.Bar(
                x=[sp], y=[abs(imp)], marker_color=cor, opacity=0.85, name=sp,
                text=[f"{'↑' if imp > 0 else '↓'} {abs(imp)}%"], textposition='outside', textfont=dict(size=11, color=cor, family="DM Mono"),
                hovertemplate=f'<b>{sp}</b><br>{imp:+d}%<extra></extra>'
            ))
        fig_casc.update_layout(
            title=dict(text=T['chart_title3'], font=dict(size=13, family='Playfair Display')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320, font=dict(family='DM Sans'), showlegend=False,
            xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#e8ede8', title="Impacto relativo (%)"), margin=dict(t=50, b=20)
        )
        plot(fig_casc)

# ── TAB 2: METODOLOGIA ────────────────────────────────────────
with tab2:
    st.markdown(f'<div class="section-label">{T["method_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["method_title"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="discovery-box"><div class="discovery-title">{T["sci_question_title"]}</div><p style="font-size:1.05rem;color:#1B3A1E;line-height:1.7"><em>{T["sci_question"]}</em></p></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["pipeline_label"]}</div>', unsafe_allow_html=True)
    for num, title, desc in T['steps']:
        st.markdown(f'<div class="method-step"><div class="step-num">{num}</div><div class="step-content"><div class="step-title">{title}</div><div class="step-desc">{desc}</div></div></div>', unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f'<div class="info-card"><strong>{T["bio_title"]}</strong><br><br><div style="font-size:0.88rem;line-height:2.1">{T["bio_text"]}</div></div>', unsafe_allow_html=True)
    with col_m2:
        st.markdown(f'<div class="info-card danger"><strong>{T["impact_title"]}</strong><br><br><div style="font-size:0.88rem;line-height:2.1">{T["impact_text"]}</div></div>', unsafe_allow_html=True)

    st.markdown("""<div class="info-card water" style="margin-top:0.5rem;background:linear-gradient(135deg,#EAF4FB,#D0E8F5)">
      <strong style="color:#1A5C8A">📊 Dados Quantitativos Verificados (2025)</strong><br><br>
      <div style="font-family:'DM Mono',monospace;font-size:0.85rem;line-height:2.2;color:#1A3A5C">
        <b>Introdução:</b> 1946 · 10 casais · Manitoba, Canadá → Lago Fagnano, Argentina<br>
        <b>Pop. atual estimada:</b> 70.000–110.000 indivíduos (GEF, 2025)<br>
        <b>Represas mapeadas:</b> 70.600 (estudo satelital 2019, lado argentino)<br>
        <b>Área colonizada:</b> 69.900 km² de Tierra del Fuego + Patagônia continental<br>
        <b>Floresta destruída:</b> ~31.000 hectares (quase 2× Washington D.C.)<br>
        <b>Custo econômico:</b> US$ 66 milhões/ano (apenas para a Argentina)<br>
        <b>Custo erradicação:</b> ~US$ 33 milhões (relatório GEF 2008)
      </div>
      <div style="font-size:0.75rem;color:#7A8A96;margin-top:0.5rem">Fonte: GEF · National Geographic (2019) · Estudo Univ. Texas do Norte (2016) · Artigo Journal of Biogeography (2009)</div>
    </div>""", unsafe_allow_html=True)

# ── TAB 3: DESCOBERTAS ────────────────────────────────────────
with tab3:
    st.markdown(f'<div class="section-label">{T["discovery_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["discovery_title"]}</div>', unsafe_allow_html=True)

    for emoji, titulo, texto in T['discoveries']:
        st.markdown(f'<div class="discovery-box" style="margin-bottom:0.8rem"><div style="display:flex;align-items:flex-start;gap:1rem"><span style="font-size:1.5rem">{emoji}</span><div><div class="discovery-title">{titulo}</div><p style="color:#1B3A1E;line-height:1.65;font-size:0.93rem;margin:0">{texto}</p></div></div></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["conclusion_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card" style="border-left-color:#1B3A1E;background:linear-gradient(135deg,#EEF5EE,#
