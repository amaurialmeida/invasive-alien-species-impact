import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static, st_folium
from folium.plugins import HeatMap

# ==================================================
# CONFIGURACIÓN DE IDIOMAS
# ==================================================

# Inicializar idioma en sesión (default: español)
if 'idioma' not in st.session_state:
    st.session_state.idioma = 'es'

# Diccionario de textos por idioma
textos = {
    # Navegación / Navigation
    'nav_portfolio': {'es': 'PORTFOLIO', 'pt': 'PORTFOLIO', 'en': 'PORTFOLIO'},
    'nav_linkedin': {'es': 'LINKEDIN', 'pt': 'LINKEDIN', 'en': 'LINKEDIN'},
    'nav_github': {'es': 'GITHUB', 'pt': 'GITHUB', 'en': 'GITHUB'},
    'nav_email': {'es': 'CORREO', 'pt': 'E-MAIL', 'en': 'E-MAIL'},
    
    # Títulos principales
    'main_title': {'es': '🌳 Impacto de los Castores en Isla Navarino', 
                   'pt': '🌳 Impacto dos Castores na Isla Navarino', 
                   'en': '🌳 Beaver Impact on Isla Navarino'},
    'subtitle': {'es': 'Chile - Comparación Vertical: 🛰️ Satélite Real (arriba) vs 🗺️ Mapa de Impacto (abajo)',
                 'pt': 'Chile - Comparação Vertical: 🛰️ Satélite Real (acima) vs 🗺️ Mapa de Impacto (abaixo)',
                 'en': 'Chile - Vertical Comparison: 🛰️ Real Satellite (top) vs 🗺️ Impact Map (bottom)'},
    
    # Sidebar
    'sidebar_author': {'es': '🇨🇱 Amauri - 2026', 
                       'pt': '🇧🇷 Amauri - 2026', 
                       'en': '🇺🇸 Amauri - 2026'},
    'sidebar_timeline': {'es': '📅 Línea de Tiempo', 
                         'pt': '📅 Linha do Tempo', 
                         'en': '📅 Timeline'},
    'sidebar_legend': {'es': '🎨 Leyenda del Mapa de Impacto',
                       'pt': '🎨 Legenda do Mapa de Impacto',
                       'en': '🎨 Impact Map Legend'},
    'sidebar_sources': {'es': '📊 Fuente de Datos',
                        'pt': '📊 Fonte dos Dados',
                        'en': '📊 Data Sources'},
    
    # Eventos históricos
    'event_1946': {'es': '🇦🇷 Introducción de los 20 castores - Llegada a Tierra del Fuego',
                   'pt': '🇦🇷 Introdução dos 20 castores - Chegada à Tierra del Fuego',
                   'en': '🇦🇷 Introduction of 20 beavers - Arrival to Tierra del Fuego'},
    'event_1960': {'es': '🇨🇱 Llegada a Chile - Cruzaron el Estrecho de Magallanes',
                   'pt': '🇨🇱 Chegada ao Chile - Cruzaram o Estreito de Magalhães',
                   'en': '🇨🇱 Arrival to Chile - Crossed the Strait of Magellan'},
    'event_1990': {'es': '⚠️ Primeros daños significativos documentados',
                   'pt': '⚠️ Primeiros danos significativos documentados',
                   'en': '⚠️ First significant damages documented'},
    'event_2008': {'es': '📋 Plan de erradicación Chile-Argentina',
                   'pt': '📋 Plano de erradicação Chile-Argentina',
                   'en': '📋 Chile-Argentina eradication plan'},
    'event_2010': {'es': '👻 "Bosque fantasma" documentado por Miguel Gallardo',
                   'pt': '👻 "Floresta fantasma" documentada por Miguel Gallardo',
                   'en': '👻 "Ghost forest" documented by Miguel Gallardo'},
    'event_2015': {'es': '💧 50.000 represas estimadas',
                   'pt': '💧 50.000 represas estimadas',
                   'en': '💧 50,000 estimated dams'},
    'event_2020': {'es': '💧💧 70.000+ represas documentadas por satélite',
                   'pt': '💧💧 70.000+ represas documentadas por satélite',
                   'en': '💧💧 70,000+ dams documented by satellite'},
    'event_2025': {'es': '🔴 78% del área afectada (proyección)',
                   'pt': '🔴 78% da área afetada (projeção)',
                   'en': '🔴 78% of affected area (projection)'},
    
    # Legendas do mapa
    'legend_high': {'es': 'Alto impacto (>60%)', 'pt': 'Alto impacto (>60%)', 'en': 'High impact (>60%)'},
    'legend_moderate': {'es': 'Impacto moderado (30-60%)', 'pt': 'Impacto moderado (30-60%)', 'en': 'Moderate impact (30-60%)'},
    'legend_low': {'es': 'Bajo impacto (<30%)', 'pt': 'Baixo impacto (<30%)', 'en': 'Low impact (<30%)'},
    'legend_dams': {'es': 'Represas de castores', 'pt': 'Represas dos castores', 'en': 'Beaver dams'},
    'legend_heatmap': {'es': 'Concentración de actividad', 'pt': 'Concentração de atividade', 'en': 'Activity concentration'},
    
    # Botones de idioma
    'btn_es': {'es': '🇪🇸 ES', 'pt': '🇪🇸 ES', 'en': '🇪🇸 ES'},
    'btn_pt': {'es': '🇧🇷 PT', 'pt': '🇧🇷 PT', 'en': '🇧🇷 PT'},
    'btn_en': {'es': '🇺🇸 EN', 'pt': '🇺🇸 EN', 'en': '🇺🇸 EN'},
    
    # Controles del slider
    'slider_label': {'es': '📅 Arrastre para ver la evolución del impacto de los castores:',
                     'pt': '📅 Arraste para ver a evolução do impacto dos castores:',
                     'en': '📅 Drag to see the evolution of beaver impact:'},
    
    # Métricas
    'metric_year': {'es': '📅 Año', 'pt': '📅 Ano', 'en': '📅 Year'},
    'metric_years': {'es': 'años', 'pt': 'anos', 'en': 'years'},
    'metric_affected': {'es': '🌳 Área afectada', 'pt': '🌳 Área afetada', 'en': '🌳 Affected area'},
    'metric_dams': {'es': '🦫 Represas', 'pt': '🦫 Represas', 'en': '🦫 Dams'},
    'metric_beavers': {'es': '🦫 Castores', 'pt': '🦫 Castores', 'en': '🦫 Beavers'},
    'metric_hectares': {'es': '🌲 Hectáreas devastadas', 'pt': '🌲 Hectares dizimados', 'en': '🌲 Devastated hectares'},
    'since': {'es': 'desde', 'pt': 'desde', 'en': 'since'},
    
    # Títulos de los mapas
    'map_sat_title': {'es': '🛰️ MAPA SUPERIOR: IMAGEN DE SATÉLITE REAL (TRUE COLOR)',
                      'pt': '🛰️ MAPA SUPERIOR: IMAGEM DE SATÉLITE REAL (TRUE COLOR)',
                      'en': '🛰️ TOP MAP: REAL SATELLITE IMAGE (TRUE COLOR)'},
    'map_impact_title': {'es': '🗺️ MAPA INFERIOR: IMPACTO AMBIENTAL DE LOS CASTORES',
                         'pt': '🗺️ MAPA INFERIOR: IMPACTO AMBIENTAL DOS CASTORES',
                         'en': '🗺️ BOTTOM MAP: ENVIRONMENTAL BEAVER IMPACT'},
    
    # Análisis
    'analysis_title': {'es': '📊 Análisis de la Comparación',
                       'pt': '📊 Análise da Comparação',
                       'en': '📊 Comparison Analysis'},
    'analysis_sat': {'es': '🛰️ Qué observar en el mapa superior (Satélite)',
                     'pt': '🛰️ O que observar no mapa superior (Satélite)',
                     'en': '🛰️ What to observe in the top map (Satellite)'},
    'analysis_sat_text': {'es': '- Colores reales: vegetación verde, agua azul, suelo marrón\n- Círculos semitransparentes: indican áreas afectadas\n- Compare directamente la devastación en la imagen real\n- Cuanto más intenso el rojo, mayor el impacto',
                          'pt': '- Cores reais: vegetação verde, água azul, solo marrom\n- Círculos semi-transparentes: indicam áreas afetadas\n- Compare diretamente a devastação na imagem real\n- Quanto mais intenso o vermelho, maior o impacto',
                          'en': '- Real colors: green vegetation, blue water, brown soil\n- Semi-transparent circles: indicate affected areas\n- Directly compare devastation in the real image\n- The more intense the red, the greater the impact'},
    'analysis_impact': {'es': '🗺️ Qué observar en el mapa inferior (Impacto)',
                        'pt': '🗺️ O que observar no mapa inferior (Impacto)',
                        'en': '🗺️ What to observe in the bottom map (Impact)'},
    'analysis_impact_text': {'es': '- Círculos coloreados: intensidad del impacto por región\n- Mapa de calor: dónde hay más actividad\n- Puntos azules: ubicación de las represas\n- Use zoom para ver detalles específicos',
                             'pt': '- Círculos coloridos: intensidade do impacto por região\n- Mapa de calor: onde há mais atividade\n- Pontos azuis: localização das represas\n- Use zoom para ver detalhes específicos',
                             'en': '- Colored circles: impact intensity by region\n- Heatmap: where there is more activity\n- Blue dots: dam locations\n- Use zoom to see specific details'},
    
    # Contexto histórico
    'context_title': {'es': '📜 Contexto Histórico',
                      'pt': '📜 Contexto Histórico',
                      'en': '📜 Historical Context'},
    'context_period1': {'es': 'Período inicial (1985-1990): Castores aún estableciéndose en la isla. Impacto localizado y limitado.',
                        'pt': 'Período inicial (1985-1990): Castores ainda se estabelecendo na ilha. Impacto localizado e limitado.',
                        'en': 'Initial period (1985-1990): Beavers still establishing on the island. Localized and limited impact.'},
    'context_period2': {'es': 'Período de expansión (1990-2000): La población de castores crece exponencialmente. Primeros daños significativos documentados.',
                        'pt': 'Período de expansão (1990-2000): População de castores cresce exponencialmente. Primeiros danos significativos documentados.',
                        'en': 'Expansion period (1990-2000): Beaver population grows exponentially. First significant damages documented.'},
    'context_period3': {'es': 'Período crítico (2000-2010): "Bosque fantasma" documentado en 2010. Los castores ya han alterado significativamente el paisaje.',
                        'pt': 'Período crítico (2000-2010): "Floresta fantasma" documentada em 2010. Castores já alteraram significativamente a paisagem.',
                        'en': 'Critical period (2000-2010): "Ghost forest" documented in 2010. Beavers have already significantly altered the landscape.'},
    'context_period4': {'es': 'Período de devastación (2010-2020): 70.000+ represas documentadas vía satélite. Más del 60% del área afectada.',
                        'pt': 'Período de devastação (2010-2020): 70.000+ represas documentadas via satélite. Mais de 60% da área afetada.',
                        'en': 'Devastation period (2010-2020): 70,000+ dams documented by satellite. Over 60% of affected area.'},
    'context_period5': {'es': 'Período actual (2020-2025): Proyección del 78% del área afectada. Plan de erradicación en marcha, pero el impacto ya es masivo.',
                        'pt': 'Período atual (2020-2025): Projeção de 78% da área afetada. Plano de erradicação em andamento, mas impacto já é massivo.',
                        'en': 'Current period (2020-2025): Projection of 78% of affected area. Eradication plan underway, but impact is already massive.'},
    
    # Relato de Gallardo
    'gallardo_quote': {'es': '👻 RELATO DE MIGUEL GALLARDO (Guarda forestal, 2010):\n\n"Todo estaba blanco porque todo estaba muerto. Parecía un bosque fantasma. Donde antes había un exuberante bosque de hayas, encontré troncos caídos, ramas sin hojas y tocones retorcidos."',
                       'pt': '👻 RELATO DE MIGUEL GALLARDO (Guarda florestal, 2010):\n\n"Estava tudo branco porque tudo estava morto. Parecia uma floresta fantasma. Onde antes havia uma exuberante floresta de faias, encontrei troncos caídos, galhos sem folhas e tocos retorcidos."',
                       'en': '👻 TESTIMONY OF MIGUEL GALLARDO (Forest ranger, 2010):\n\n"Everything was white because everything was dead. It looked like a ghost forest. Where there once was a lush beech forest, I found fallen trunks, leafless branches, and twisted stumps."'},
    
    # Gráfico
    'chart_title': {'es': '📈 Evolución Histórica del Impacto (1985-2025)',
                    'pt': '📈 Evolução Histórica do Impacto (1985-2025)',
                    'en': '📈 Historical Impact Evolution (1985-2025)'},
    'chart_ylabel': {'es': 'Área de la Isla Afectada (%)',
                     'pt': 'Área da Ilha Afetada (%)',
                     'en': 'Island Area Affected (%)'},
    
    # Footer
    'footer_sat': {'es': 'Mapa Superior: ESRI World Imagery - Imágenes satelitales True Color de alta resolución',
                   'pt': 'Mapa Superior: ESRI World Imagery - Imagens de satélite True Color de alta resolução',
                   'en': 'Top Map: ESRI World Imagery - High resolution True Color satellite images'},
    'footer_impact': {'es': 'Mapa Inferior: CartoDB - Visualización estilizada del impacto ambiental',
                      'pt': 'Mapa Inferior: CartoDB - Visualização estilizada do impacto ambiental',
                      'en': 'Bottom Map: CartoDB - Stylized visualization of environmental impact'},
    'footer_coords': {'es': 'Coordenadas: 54°56′S 67°37′W - Isla Navarino, Región de Magallanes, Chile',
                      'pt': 'Coordenadas: 54°56′S 67°37′W - Isla Navarino, Região de Magallanes, Chile',
                      'en': 'Coordinates: 54°56′S 67°37′W - Isla Navarino, Magallanes Region, Chile'},
    'footer_quote': {'es': '"La mayor alteración del paisaje en bosques subantárticos desde la última era del hielo"',
                     'pt': '"A maior alteração de paisagem em florestas subantárticas desde a última era do gelo"',
                     'en': '"The largest landscape alteration in subantarctic forests since the last ice age"'},
    'footer_note': {'es': 'Nota: Las imágenes satelitales se actualizan periódicamente. La superposición de impacto se simula con base en datos científicos reales.',
                    'pt': 'Nota: As imagens de satélite são atualizadas periodicamente. A sobreposição de impacto é simulada com base em dados científicos reais.',
                    'en': 'Note: Satellite images are updated periodically. Impact overlay is simulated based on real scientific data.'},
}

# Función para obtener texto traducido
def t(key):
    return textos[key][st.session_state.idioma]

# Función para cambiar idioma
def cambiar_idioma(idioma):
    st.session_state.idioma = idioma
    st.rerun()

# ==================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==================================================

st.set_page_config(
    page_title="Castores en Isla Navarino - Impacto Ambiental",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para barra de navegación (fondo blanco) y botones de idioma
st.markdown("""
<style>
    /* Barra de navegación */
    .nav-bar {
        background-color: white;
        padding: 15px 25px;
        border-radius: 0px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        border-bottom: 1px solid #e0e0e0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .nav-links {
        display: flex;
        gap: 25px;
        flex-wrap: wrap;
        align-items: center;
    }
    .nav-link {
        color: #333;
        text-decoration: none;
        font-weight: 500;
        padding: 8px 0px;
        transition: all 0.3s;
        font-size: 0.9rem;
        background: none;
        border: none;
        cursor: pointer;
    }
    .nav-link:hover {
        color: #2c5f2d;
        text-decoration: underline;
    }
    .nav-brand {
        color: #2c5f2d;
        font-weight: 600;
        font-size: 1rem;
        margin-right: 20px;
    }
    
    /* Container dos botões de idioma */
    .lang-container {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        margin-bottom: 15px;
    }
    
    /* Botões de idioma padronizados - todos com mesma largura */
    div[data-testid="column"]:has(button) {
        display: flex;
        justify-content: center;
    }
    
    .stButton button {
        width: 70px !important;
        min-width: 70px !important;
        max-width: 70px !important;
        height: 36px !important;
        padding: 5px 0px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        border-radius: 20px !important;
        background-color: #f0f0f0 !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
        transition: all 0.3s !important;
    }
    
    .stButton button:hover {
        background-color: #2c5f2d !important;
        color: white !important;
        border-color: #2c5f2d !important;
        transform: scale(1.02) !important;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c5f2d;
        text-align: center;
    }
    .subtitle {
        font-size: 1.1rem;
        text-align: center;
        color: #666;
        margin-bottom: 1rem;
    }
    .impact-stat {
        font-size: 2rem;
        font-weight: bold;
        color: #8b4513;
        text-align: center;
    }
    .warning-box {
        background-color: #ffeb3b;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f44336;
        margin: 1rem 0;
    }
    .map-container {
        border-radius: 12px;
        border: 2px solid #2c5f2d;
        overflow: hidden;
        margin: 15px 0;
        background-color: #f9f9f9;
    }
    .map-title {
        background: linear-gradient(90deg, #2c5f2d, #1a3d1a);
        color: white;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        border-radius: 10px 10px 0 0;
    }
    .map-title-sat {
        background: linear-gradient(90deg, #1a5276, #1b4f72);
    }
    .map-title-impact {
        background: linear-gradient(90deg, #8b4513, #a0522d);
    }
    hr {
        margin: 10px 0;
    }
    .sidebar-content {
        padding: 10px;
    }
    .fonte-dados {
        line-height: 1.6;
    }
    .fonte-dados p {
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================
# BARRA DE NAVEGACIÓN SUPERIOR
# ==================================================

# HTML para la barra de navegación
nav_html = f'''
<div class="nav-bar">
    <div class="nav-links">
        <span class="nav-brand">Amauri</span>
        <a href="https://amaurialmeida.github.io/environmental-portfolio/" target="_blank" class="nav-link">{t('nav_portfolio')}</a>
        <a href="https://linkedin.com/in/amauri-almeida26/" target="_blank" class="nav-link">{t('nav_linkedin')}</a>
        <a href="https://github.com/amaurialmeida" target="_blank" class="nav-link">{t('nav_github')}</a>
        <a href="mailto:amauri@tutamail.com" class="nav-link">{t('nav_email')}</a>
    </div>
</div>
'''

st.markdown(nav_html, unsafe_allow_html=True)

# Botões de idioma padronizados (todos com mesmo tamanho)
col_es, col_pt, col_en, col_spacer = st.columns([1, 1, 1, 8])

with col_es:
    if st.button("🇪🇸 ES", key="btn_es", use_container_width=True):
        cambiar_idioma('es')

with col_pt:
    if st.button("🇧🇷 PT", key="btn_pt", use_container_width=True):
        cambiar_idioma('pt')

with col_en:
    if st.button("🇺🇸 EN", key="btn_en", use_container_width=True):
        cambiar_idioma('en')

st.markdown("---")

# ==================================================
# TÍTULOS PRINCIPALES
# ==================================================

st.markdown(f'<div class="main-title">{t("main_title")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{t("subtitle")}</div>', unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown(f"### 👤 {t('sidebar_author')}")
    st.markdown("---")
    
    st.markdown(f"## {t('sidebar_timeline')}")
    
    eventos = {
        1946: t('event_1946'),
        1960: t('event_1960'),
        1990: t('event_1990'),
        2008: t('event_2008'),
        2010: t('event_2010'),
        2015: t('event_2015'),
        2020: t('event_2020'),
        2025: t('event_2025')
    }
    
    for ano_evento, evento in eventos.items():
        st.markdown(f"**{ano_evento}** - {evento}")
    
    st.markdown("---")
    st.markdown(f"### {t('sidebar_legend')}")
    st.markdown(f"""
    <div style="background: white; padding: 10px; border-radius: 8px;">
        <span style="color: red;">●</span> <b>{t('legend_high')}</b><br>
        <span style="color: orange;">●</span> <b>{t('legend_moderate')}</b><br>
        <span style="color: yellow;">●</b> <b>{t('legend_low')}</b><br>
        <span style="color: blue;">●</span> <b>{t('legend_dams')}</b><br>
        <span style="background: linear-gradient(90deg, blue, lime, yellow, orange, red); width: 100%; height: 3px; display: block; margin: 8px 0;"></span>
        <span><b>{t('legend_heatmap')}</b></span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"### {t('sidebar_sources')}")
    st.markdown("""
    <div class="fonte-dados">
        <p>📰 <b>National Geographic</b> (2019)</p>
        <p>🌍 <b>GEF - Global Environment Facility</b></p>
        <p>🇨🇱 <b>CONAF - Chile</b></p>
        <p>🎓 <b>Universidad de Magallanes</b></p>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# FUNCIONES DE MAPAS
# ==================================================

def calcular_percentual_impacto(ano):
    if ano <= 1990:
        percentual = 0.02 + (ano - 1985) * 0.006
    elif ano <= 2000:
        percentual = 0.05 + (ano - 1990) * 0.012
    elif ano <= 2010:
        percentual = 0.15 + (ano - 2000) * 0.018
    elif ano <= 2015:
        percentual = 0.33 + (ano - 2010) * 0.024
    else:
        percentual = 0.45 + (ano - 2015) * 0.025
    return min(percentual, 0.78)

def criar_mapa_satelite_real(ano, percentual):
    mapa = folium.Map(location=[-54.93, -67.62], zoom_start=11, control_scale=True)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='ESRI - Imagen Satelital True Color',
        name='Satélite', overlay=False, control=False
    ).add_to(mapa)
    
    pontos_criticos = {
        "Laguna Rojas": [-54.92, -67.62],
        "Laguna Zafueta": [-54.95, -67.65],
        "Puerto Williams": [-54.93, -67.62],
        "Rio Lasifashaj": [-54.90, -67.70],
        "Lago Navarino": [-54.88, -67.55]
    }
    
    raio_base = 800 * percentual
    
    for nome, coords in pontos_criticos.items():
        if percentual > 0.6:
            cor, opacity = 'red', 0.35
        elif percentual > 0.3:
            cor, opacity = 'orange', 0.3
        else:
            cor, opacity = 'yellow', 0.25
        
        raio = raio_base + (200 if "Rio" in nome else 0)
        folium.Circle(radius=raio, location=coords, color=cor, fill=True,
                     fill_color=cor, fill_opacity=opacity, weight=2,
                     popup=f"{nome}<br>Impacto: {percentual*100:.1f}%<br>Año: {ano}").add_to(mapa)
    
    bounds = [[-55.10, -67.90], [-54.80, -67.40]]
    mapa.fit_bounds(bounds)
    return mapa

def criar_mapa_impacto(ano, percentual):
    mapa = folium.Map(location=[-54.93, -67.62], zoom_start=11, control_scale=True)
    folium.TileLayer('CartoDB positron', name='Mapa Base', control=False).add_to(mapa)
    
    pontos_criticos = {
        "Laguna Rojas": [-54.92, -67.62],
        "Laguna Zafueta": [-54.95, -67.65],
        "Puerto Williams": [-54.93, -67.62],
        "Rio Lasifashaj": [-54.90, -67.70],
        "Lago Navarino": [-54.88, -67.55]
    }
    
    raio_base = 800 * percentual
    
    for nome, coords in pontos_criticos.items():
        if percentual > 0.6:
            cor, fill_color, opacity = 'red', 'darkred', 0.6
        elif percentual > 0.3:
            cor, fill_color, opacity = 'orange', 'orange', 0.5
        else:
            cor, fill_color, opacity = 'yellow', 'gold', 0.4
        
        raio = raio_base + (250 if "Rio" in nome else 0)
        folium.Circle(radius=raio, location=coords, color=cor, fill=True,
                     fill_color=fill_color, fill_opacity=opacity, weight=3,
                     popup=f"{nome}<br>Impacto: {percentual*100:.1f}%").add_to(mapa)
        folium.Marker(location=coords, popup=nome, icon=folium.Icon(color='darkred', icon='exclamation-triangle', prefix='fa')).add_to(mapa)
    
    if percentual > 0.15:
        np.random.seed(42)
        n_pontos = int(100 * percentual)
        heat_data = [[-54.93 + np.random.normal(0, 0.07) * (percentual * 1.5),
                      -67.62 + np.random.normal(0, 0.10) * (percentual * 1.5),
                      percentual * np.random.random()] for _ in range(n_pontos)]
        HeatMap(heat_data, radius=25, blur=15, min_opacity=0.2,
                gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}).add_to(mapa)
    
    num_represas = int(50 * percentual)
    np.random.seed(42)
    for i in range(num_represas):
        lat = -54.93 + np.random.normal(0, 0.05)
        lon = -67.62 + np.random.normal(0, 0.07)
        folium.CircleMarker(radius=4, location=[lat, lon], color='#0044cc', fill=True,
                           fill_color='#0066ff', fill_opacity=0.9,
                           popup=f"Represa #{i+1}").add_to(mapa)
    
    bounds = [[-55.10, -67.90], [-54.80, -67.40]]
    mapa.fit_bounds(bounds)
    
    info_html = f'''
    <div style="position: fixed; top: 20px; right: 20px; z-index: 1000; background-color: rgba(0,0,0,0.8); color: white; padding: 12px 20px; border-radius: 8px; font-size: 14px; font-weight: bold; text-align: center;">
        <b>📊 AÑO: {ano}</b><br>
        🦫 Impacto: {percentual*100:.1f}%<br>
        🏗️ Represas: {int(70000 * percentual):,}<br>
        🌳 Área afectada: {int(31000 * percentual):,} ha
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(info_html))
    return mapa

# ==================================================
# INTERFAZ PRINCIPAL
# ==================================================

st.markdown("---")
st.markdown(f"## 🎚️ {t('slider_label')}")

ano = st.slider("", min_value=1985, max_value=2025, value=2010, step=5, format="%d", key="ano_slider")
percentual = calcular_percentual_impacto(ano)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    delta_1985 = (percentual - calcular_percentual_impacto(1985)) * 100
    st.metric(t('metric_year'), f"{ano}", delta=f"{ano-1985} {t('metric_years')}")
with col2:
    st.metric(t('metric_affected'), f"{percentual*100:.1f}%", delta=f"+{delta_1985:.1f}% {t('since')} 1985")
with col3:
    st.metric(t('metric_dams'), f"{int(70000 * percentual):,}")
with col4:
    st.metric(t('metric_beavers'), f"{int(110000 * percentual):,}")
with col5:
    st.metric(t('metric_hectares'), f"{int(31000 * percentual):,} ha")

st.markdown("---")
st.markdown("## 🗺️ Visualización Vertical")

# Mapa Superior
st.markdown(f"""
<div class="map-container">
    <div class="map-title map-title-sat">
        {t('map_sat_title')}
    </div>
</div>
""", unsafe_allow_html=True)

mapa_satelite = criar_mapa_satelite_real(ano, percentual)
st_folium(mapa_satelite, width=900, height=500, returned_objects=[])

st.markdown("<br>", unsafe_allow_html=True)

# Mapa Inferior
st.markdown(f"""
<div class="map-container">
    <div class="map-title map-title-impact">
        {t('map_impact_title')}
    </div>
</div>
""", unsafe_allow_html=True)

mapa_impacto = criar_mapa_impacto(ano, percentual)
st_folium(mapa_impacto, width=900, height=500, returned_objects=[])

# ==================================================
# ANÁLISIS Y CONTEXTO
# ==================================================

st.markdown("---")
st.markdown(f"## {t('analysis_title')}")

col_analysis1, col_analysis2 = st.columns(2)

with col_analysis1:
    st.markdown(f"### {t('analysis_sat')}")
    st.markdown(t('analysis_sat_text'))

with col_analysis2:
    st.markdown(f"### {t('analysis_impact')}")
    st.markdown(t('analysis_impact_text'))

st.markdown("---")
st.markdown(f"## {t('context_title')}")

if ano <= 1990:
    st.info(f"📅 {t('context_period1')}")
elif ano <= 2000:
    st.info(f"📅 {t('context_period2')}")
elif ano <= 2010:
    st.warning(f"📅 {t('context_period3')}")
    if ano == 2010:
        st.markdown(f"""
        <div class="warning-box">
        <strong>{t('gallardo_quote')}</strong>
        </div>
        """, unsafe_allow_html=True)
elif ano <= 2020:
    st.error(f"📅 {t('context_period4')}")
else:
    st.error(f"📅 {t('context_period5')}")

# ==================================================
# GRÁFICO - COM CORES RESTAURADAS
# ==================================================

st.markdown("---")
st.markdown(f"## {t('chart_title')}")

datos_tendencia = pd.DataFrame({
    'Año': [1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
    'Área_Afectada_%': [2, 5, 10, 15, 22, 33, 45, 60, 78],
})

# Gráfico com cores restauradas - linha marrom com marcadores verdes
fig = px.line(datos_tendencia, x='Año', y='Área_Afectada_%',
              markers=True, 
              color_discrete_sequence=['#8b4513'],  # Cor marrom para a linha
              line_shape='spline')

# Personalizar os marcadores
fig.update_traces(
    marker=dict(
        size=12,
        color='#2c5f2d',  # Cor verde para os marcadores
        symbol='circle',
        line=dict(width=2, color='#1a3d1a')
    ),
    line=dict(width=3, color='#8b4513')
)

fig.update_layout(
    xaxis_title="Año", 
    yaxis_title=t('chart_ylabel'), 
    height=450,
    hovermode='x unified', 
    plot_bgcolor='#f5f5f5', 
    title_x=0.5,
    title_font=dict(size=16, color='#2c5f2d'),
    xaxis=dict(
        tickmode='linear',
        tick0=1985,
        dtick=5,
        gridcolor='#e0e0e0',
        gridwidth=1
    ),
    yaxis=dict(
        gridcolor='#e0e0e0',
        gridwidth=1,
        range=[0, 85]
    )
)

# Adicionar área sombreada abaixo da linha
fig.add_trace(px.area(datos_tendencia, x='Año', y='Área_Afectada_%', 
                      color_discrete_sequence=['rgba(139, 69, 19, 0.2)']).data[0])

# Adicionar anotações
fig.add_annotation(x=2010, y=33, text="🔴 'Bosque Fantasma'", 
                   showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2,
                   arrowcolor="red", font=dict(size=11, color="red", weight="bold"))

fig.add_annotation(x=2008, y=15, text="📋 Plan de erradicación", 
                   showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
                   arrowcolor="orange", font=dict(size=10, color="orange"))

fig.add_annotation(x=2025, y=78, text="⚠️ Proyección crítica", 
                   showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2,
                   arrowcolor="darkred", font=dict(size=11, color="darkred", weight="bold"))

# Áreas de fundo coloridas
fig.add_hrect(y0=0, y1=33, line_width=0, fillcolor="green", opacity=0.05)
fig.add_hrect(y0=33, y1=60, line_width=0, fillcolor="orange", opacity=0.05)
fig.add_hrect(y0=60, y1=85, line_width=0, fillcolor="red", opacity=0.05)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #999; font-size: 0.8rem; padding: 1rem;">
    <p>
        🛰️ <b>{t('footer_sat')}</b><br>
        🗺️ <b>{t('footer_impact')}</b><br>
        📊 <b>{t('sidebar_sources')}</b>
    </p>
    <p>
        📍 <b>{t('footer_coords')}</b><br>
        🧊 <i>{t('footer_quote')}</i>
    </p>
    <hr>
    <p style="font-size: 0.7rem;">
        ⚠️ <b>{t('footer_note')}</b>
    </p>
</div>
""", unsafe_allow_html=True)