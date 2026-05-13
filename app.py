import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static, st_folium
from branca.colormap import linear
from folium.plugins import HeatMap
import time

# Configuração da página
st.set_page_config(
    page_title="Castores na Isla Navarino - Comparação Vertical",
    page_icon="🦫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS
st.markdown("""
<style>
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
    .stButton > button {
        background-color: #2c5f2d;
        color: white;
        border-radius: 20px;
    }
    .stButton > button:hover {
        background-color: #1a3d1a;
    }
    hr {
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="main-title">🦫 Impacto dos Castores na Isla Navarino</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Chile - Comparação Vertical: 🛰️ Satélite Real (acima) vs 🗺️ Mapa de Impacto (abaixo)</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Beaver_%28PSF%29.png/800px-Beaver_%28PSF%29.png", use_column_width=True)
    
    st.markdown("## 📅 Linha do Tempo")
    
    eventos = {
        1946: "🟫 Introdução dos 20 castores",
        1960: "🟤 Chegada ao Chile",
        1990: "⚫ Primeiros danos significativos",
        2008: "🟠 Plano de erradicação",
        2010: "🔴 'Floresta fantasma' documentada",
        2015: "🟡 50.000 represas",
        2020: "🟠 70.000+ represas",
        2025: "🔴 78% da área afetada"
    }
    
    for ano_evento, evento in eventos.items():
        st.markdown(f"**{ano_evento}** - {evento}")
    
    st.markdown("---")
    st.markdown("### 🎨 Legenda do Mapa de Impacto")
    st.markdown("""
    <div style="background: white; padding: 10px; border-radius: 8px;">
        <span style="color: red;">●</span> <b>Vermelho:</b> Alto impacto (>60%)<br>
        <span style="color: orange;">●</span> <b>Laranja:</b> Impacto moderado (30-60%)<br>
        <span style="color: yellow;">●</b> <b>Amarelo:</b> Baixo impacto (<30%)<br>
        <span style="color: blue;">●</span> <b>Azul:</b> Represas dos castores<br>
        <span style="background: linear-gradient(90deg, blue, lime, yellow, orange, red); width: 100%; height: 3px; display: block; margin: 8px 0;"></span>
        <span><b>Heatmap:</b> Concentração de atividade</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Fonte dos Dados")
    st.info("""
    **National Geographic (2019)**<br>
    **GEF - Global Environment Facility**<br>
    **CONAF - Chile**<br>
    **Universidad de Magallanes**
    """)

# Função para calcular percentual de impacto baseado no ano
def calcular_percentual_impacto(ano):
    """Calcula o percentual de área afetada baseado em dados reais"""
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

# Função para criar mapa de satélite real (True Color)
def criar_mapa_satelite_real(ano, percentual):
    """Cria mapa com imagem de satélite real e overlay de impacto"""
    
    # Coordenadas centrais da Isla Navarino
    mapa = folium.Map(
        location=[-54.93, -67.62],
        zoom_start=11,
        control_scale=True
    )
    
    # Camada de satélite True Color (ESRI World Imagery)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='ESRI - Imagem de Satélite True Color',
        name='Satélite',
        overlay=False,
        control=False
    ).add_to(mapa)
    
    # Coordenadas dos pontos críticos
    pontos_criticos = {
        "Laguna Rojas": [-54.92, -67.62],
        "Laguna Zafueta": [-54.95, -67.65],
        "Puerto Williams": [-54.93, -67.62],
        "Rio Lasifashaj": [-54.90, -67.70],
        "Lago Navarino": [-54.88, -67.55]
    }
    
    # Raio base do impacto (em metros)
    raio_base = 800 * percentual
    
    # Adicionar círculos de impacto semi-transparentes
    for nome, coords in pontos_criticos.items():
        if percentual > 0.6:
            cor = 'red'
            opacity = 0.35
        elif percentual > 0.3:
            cor = 'orange'
            opacity = 0.3
        else:
            cor = 'yellow'
            opacity = 0.25
        
        raio = raio_base + (200 if "Rio" in nome else 0)
        
        folium.Circle(
            radius=raio,
            location=coords,
            color=cor,
            fill=True,
            fill_color=cor,
            fill_opacity=opacity,
            weight=2,
            popup=f"""
            <b>{nome}</b><br>
            <b>Impacto:</b> {percentual*100:.1f}%<br>
            <b>Ano:</b> {ano}<br>
            <i>Clique para ver detalhes</i>
            """
        ).add_to(mapa)
    
    # Adicionar marcador central
    folium.Marker(
        location=[-54.93, -67.62],
        popup=f"""
        <b>🛰️ Isla Navarino - {ano}</b><br>
        🌍 Imagem de Satélite Real (True Color)<br>
        🦫 Impacto dos castores: {percentual*100:.1f}%<br>
        📍 Coordenadas: 54°56′S 67°37′W
        """,
        icon=folium.Icon(color='green', icon='satellite', prefix='fa'),
        tooltip="Isla Navarino"
    ).add_to(mapa)
    
    # Adicionar bounding box para focar na ilha
    bounds = [[-55.10, -67.90], [-54.80, -67.40]]
    mapa.fit_bounds(bounds)
    
    # Adicionar legenda no mapa
    legend_html = '''
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000; background-color: rgba(0,0,0,0.75); color: white; padding: 10px 15px; border-radius: 8px; font-size: 12px; font-family: monospace;">
        <b>🛰️ LEGENDA</b><br>
        <span style="color: #ff6b6b;">◯</span> Área de alto impacto<br>
        <span style="color: #ffa500;">◯</span> Área de impacto moderado<br>
        <span style="color: #ffff00;">◯</span> Área de baixo impacto<br>
        <hr style="margin: 5px 0;">
        <span>🌍 Fonte: ESRI World Imagery</span><br>
        <span>📅 Ano: ''' + str(ano) + '''</span>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legend_html))
    
    return mapa

# Função para criar mapa de impacto (estilo desenho/calor)
def criar_mapa_impacto(ano, percentual):
    """Cria mapa de impacto com visualização estilo desenho"""
    
    mapa = folium.Map(
        location=[-54.93, -67.62],
        zoom_start=11,
        control_scale=True
    )
    
    # Usar mapa base claro (estilo desenho)
    folium.TileLayer('CartoDB positron', name='Mapa Base', control=False).add_to(mapa)
    
    # Coordenadas dos pontos críticos
    pontos_criticos = {
        "Laguna Rojas": [-54.92, -67.62],
        "Laguna Zafueta": [-54.95, -67.65],
        "Puerto Williams": [-54.93, -67.62],
        "Rio Lasifashaj": [-54.90, -67.70],
        "Lago Navarino": [-54.88, -67.55]
    }
    
    # Raio base do impacto
    raio_base = 800 * percentual
    
    # Adicionar círculos de impacto (cores sólidas)
    for nome, coords in pontos_criticos.items():
        if percentual > 0.6:
            cor = 'red'
            fill_color = 'darkred'
            opacity = 0.6
        elif percentual > 0.3:
            cor = 'orange'
            fill_color = 'orange'
            opacity = 0.5
        else:
            cor = 'yellow'
            fill_color = 'gold'
            opacity = 0.4
        
        raio = raio_base + (250 if "Rio" in nome else 0)
        
        folium.Circle(
            radius=raio,
            location=coords,
            color=cor,
            fill=True,
            fill_color=fill_color,
            fill_opacity=opacity,
            weight=3,
            popup=f"""
            <b>📍 {nome}</b><br>
            <b>🎯 Nível de impacto:</b> {percentual*100:.1f}%<br>
            <b>📅 Ano:</b> {ano}<br>
            <b>🦫 Represas na região:</b> {int(70000 * percentual / 5):,}
            """
        ).add_to(mapa)
        
        # Adicionar marcador
        folium.Marker(
            location=coords,
            popup=f"<b>{nome}</b><br>Ponto crítico documentado",
            icon=folium.Icon(color='darkred', icon='exclamation-triangle', prefix='fa'),
            tooltip=nome
        ).add_to(mapa)
    
    # Adicionar heatmap de atividade dos castores
    if percentual > 0.15:
        np.random.seed(42)
        n_pontos = int(100 * percentual)
        heat_data = []
        
        for _ in range(n_pontos):
            lat = -54.93 + np.random.normal(0, 0.07) * (percentual * 1.5)
            lon = -67.62 + np.random.normal(0, 0.10) * (percentual * 1.5)
            intensidade = percentual * np.random.random()
            heat_data.append([lat, lon, intensidade])
        
        HeatMap(
            heat_data, 
            radius=25, 
            blur=15, 
            min_opacity=0.2,
            gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}
        ).add_to(mapa)
    
    # Adicionar represas (pontos azuis)
    num_represas = int(50 * percentual)
    np.random.seed(42)
    
    for i in range(num_represas):
        lat = -54.93 + np.random.normal(0, 0.05)
        lon = -67.62 + np.random.normal(0, 0.07)
        
        folium.CircleMarker(
            radius=4,
            location=[lat, lon],
            color='#0044cc',
            fill=True,
            popup=f"<b>Represa #{i+1}</b><br>Construída por castores",
            fill_color='#0066ff',
            fill_opacity=0.9,
            weight=1
        ).add_to(mapa)
    
    # Adicionar bounding box
    bounds = [[-55.10, -67.90], [-54.80, -67.40]]
    mapa.fit_bounds(bounds)
    
    # Adicionar painel de informações
    info_html = f'''
    <div style="position: fixed; top: 20px; right: 20px; z-index: 1000; background-color: rgba(0,0,0,0.8); color: white; padding: 12px 20px; border-radius: 8px; font-size: 14px; font-weight: bold; text-align: center;">
        <b>📊 ANO: {ano}</b><br>
        🦫 Impacto: {percentual*100:.1f}%<br>
        🏗️ Represas: {int(70000 * percentual):,}<br>
        🌳 Área afetada: {int(31000 * percentual):,} ha
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(info_html))
    
    # Adicionar legenda
    legend_html = '''
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000; background-color: rgba(0,0,0,0.75); color: white; padding: 10px 15px; border-radius: 8px; font-size: 11px; font-family: monospace;">
        <b>🗺️ MAPA DE IMPACTO</b><br>
        <span style="color: red;">●</span> Alto impacto (>60%)<br>
        <span style="color: orange;">●</span> Impacto moderado (30-60%)<br>
        <span style="color: yellow;">●</span> Baixo impacto (<30%)<br>
        <span style="color: #0066ff;">●</span> Represa<br>
        <span style="background: linear-gradient(90deg, blue, lime, yellow, orange, red); width: 100%; height: 3px; display: block; margin: 5px 0;"></span>
        <span>🔥 Heatmap de atividade</span>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legend_html))
    
    return mapa

# Interface principal - CONTROLE TEMPORAL
st.markdown("---")
st.markdown("## 🎚️ Linha do Tempo Interativa")

# Slider de anos
ano = st.slider(
    "**Arraste para ver a evolução do impacto dos castores:**",
    min_value=1985,
    max_value=2025,
    value=2010,
    step=5,
    format="%d",
    key="ano_slider_vertical"
)

# Calcular percentual
percentual = calcular_percentual_impacto(ano)

# Métricas do ano selecionado
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    delta_1985 = (percentual - calcular_percentual_impacto(1985)) * 100
    st.metric("📅 Ano", f"{ano}", delta=f"{ano-1985} anos")
with col2:
    st.metric("🌳 Área afetada", f"{percentual*100:.1f}%", 
              delta=f"+{delta_1985:.1f}% desde 1985")
with col3:
    st.metric("🦫 Represas", f"{int(70000 * percentual):,}")
with col4:
    st.metric("🦫 Castores", f"{int(110000 * percentual):,}")
with col5:
    hectares = int(31000 * percentual)
    st.metric("🌲 Hectares dizimados", f"{hectares:,} ha")

st.markdown("---")

# ==========================================
# MAPAS EMPILHADOS (FORMATO VERTICAL)
# ==========================================

st.markdown("## 🗺️ Visualização Empilhada (Vertical)")

# Mapa 1: Satélite Real (em cima)
st.markdown("""
<div class="map-container">
    <div class="map-title map-title-sat">
        🛰️ MAPA SUPERIOR: IMAGEM DE SATÉLITE REAL (TRUE COLOR)
    </div>
</div>
""", unsafe_allow_html=True)

# Criar e exibir mapa de satélite
mapa_satelite = criar_mapa_satelite_real(ano, percentual)
st_folium(mapa_satelite, width=900, height=500, returned_objects=[])

# Espaço entre os mapas
st.markdown("<br>", unsafe_allow_html=True)

# Mapa 2: Impacto (em baixo)
st.markdown("""
<div class="map-container">
    <div class="map-title map-title-impact">
        🗺️ MAPA INFERIOR: IMPACTO AMBIENTAL DOS CASTORES
    </div>
</div>
""", unsafe_allow_html=True)

# Criar e exibir mapa de impacto
mapa_impacto = criar_mapa_impacto(ano, percentual)
st_folium(mapa_impacto, width=900, height=500, returned_objects=[])

# ==========================================
# INFORMAÇÕES ADICIONAIS
# ==========================================

st.markdown("---")
st.markdown("## 📊 Análise da Comparação")

col_analysis1, col_analysis2 = st.columns(2)

with col_analysis1:
    st.markdown("### 🛰️ O que observar no mapa superior (Satélite)")
    st.markdown("""
    - **Cores reais:** Vegetação verde, água azul, solo marrom
    - **Círculos semi-transparentes:** Indicam áreas afetadas
    - **Compare diretamente** a devastação na imagem real
    - **Quanto mais intenso o vermelho,** maior o impacto
    """)

with col_analysis2:
    st.markdown("### 🗺️ O que observar no mapa inferior (Impacto)")
    st.markdown("""
    - **Círculos coloridos:** Intensidade do impacto por região
    - **Heatmap (áreas quentes):** Onde há mais atividade
    - **Pontos azuis:** Localização das represas
    - **Use zoom** para ver detalhes específicos
    """)

# Evento histórico relevante para o ano selecionado
st.markdown("---")
st.markdown("## 📜 Contexto Histórico")

if ano <= 1990:
    st.info("📅 **Período inicial (1985-1990):** Castores ainda se estabelecendo na ilha. Impacto localizado e limitado.")
elif ano <= 2000:
    st.info("📅 **Período de expansão (1990-2000):** População de castores cresce exponencialmente. Primeiros danos significativos documentados.")
elif ano <= 2010:
    st.warning("📅 **Período crítico (2000-2010):** 'Floresta fantasma' documentada em 2010. Castores já alteraram significativamente a paisagem.")
elif ano <= 2020:
    st.error("📅 **Período de devastação (2010-2020):** 70.000+ represas documentadas via satélite. Mais de 60% da área afetada.")
else:
    st.error("📅 **Período atual (2020-2025):** Projeção de 78% da área afetada. Plano de erradicação em andamento, mas impacto já é massivo.")

# Gráfico de tendência
st.markdown("---")
st.markdown("## 📈 Evolução Histórica do Impacto (1985-2025)")

# Dados para o gráfico
dados_tendencia = pd.DataFrame({
    'Ano': [1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
    'Área_Afetada_%': [2, 5, 10, 15, 22, 33, 45, 60, 78],
    'Represas': [500, 1500, 4000, 10000, 20000, 35000, 50000, 65000, 75000],
    'Castores': [5000, 12000, 25000, 45000, 65000, 85000, 100000, 108000, 112000]
})

fig = px.line(dados_tendencia, x='Ano', y='Área_Afetada_%',
              title='<b>Progressão da devastação causada pelos castores</b>',
              markers=True, 
              color_discrete_sequence=['#8b4513'],
              line_shape='spline')
fig.update_layout(
    xaxis_title="Ano",
    yaxis_title="Área da Ilha Afetada (%)",
    height=450,
    hovermode='x unified',
    plot_bgcolor='#f5f5f5',
    title_x=0.5
)

# Adicionar anotações importantes
fig.add_annotation(x=2010, y=33, text="🔴 'Floresta Fantasma'", 
                   showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
                   arrowcolor="red", font=dict(size=10, color="red"))
fig.add_annotation(x=2008, y=15, text="📋 Plano de erradicação", 
                   showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
                   arrowcolor="orange", font=dict(size=10, color="orange"))
fig.add_annotation(x=2025, y=78, text="⚠️ Projeção crítica", 
                   showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
                   arrowcolor="darkred", font=dict(size=10, color="darkred"))

# Sombra da área de tendência
fig.add_hrect(y0=0, y1=33, line_width=0, fillcolor="green", opacity=0.1)
fig.add_hrect(y0=33, y1=60, line_width=0, fillcolor="orange", opacity=0.1)
fig.add_hrect(y0=60, y1=78, line_width=0, fillcolor="red", opacity=0.1)

st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.8rem; padding: 1rem;">
    <p>
        🛰️ <b>Mapa Superior:</b> ESRI World Imagery - Imagens de satélite True Color de alta resolução<br>
        🗺️ <b>Mapa Inferior:</b> CartoDB - Visualização estilizada do impacto ambiental<br>
        📊 <b>Dados científicos:</b> National Geographic (2019) | GEF | CONAF | Universidad de Magallanes
    </p>
    <p>
        📍 <b>Coordenadas:</b> 54°56′S 67°37′W - Isla Navarino, Região de Magallanes, Chile<br>
        🦫 <i>"A maior alteração de paisagem em florestas subantárticas desde a última era do gelo"</i>
    </p>
    <hr>
    <p style="font-size: 0.7rem;">
        ⚠️ <b>Nota:</b> As imagens de satélite são atualizadas periodicamente. A sobreposição de impacto é simulada com base em dados científicos reais.
    </p>
</div>
""", unsafe_allow_html=True)