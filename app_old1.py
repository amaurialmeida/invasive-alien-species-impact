import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os

st.set_page_config(
    page_title="Espécies Invasoras · Isla Navarino",
    page_icon="🦫",
    layout="wide"
)

# ============================================================
# SISTEMA DE IDIOMAS
# ============================================================
if "lang" not in st.session_state:
    st.session_state.lang = "pt"

TRANSLATIONS = {
    "pt": {
        "page_title": "Espécies Invasoras · Isla Navarino",
        "hero_tag": "OBSERVAÇÃO DE CAMPO · PUERTO WILLIAMS · ISLA NAVARINO · MAR–OUT 2025",
        "hero_title": "Impacto das Espécies\nExóticas Invasoras",
        "hero_subtitle": "Observação de campo das castoreiras e do ecossistema subantártico da Isla Navarino durante 8 meses de residência em Puerto Williams, Chile (março–outubro 2025). O maior desastre ecológico de florestas subantárticas desde a última era do gelo.",
        "badge1": "🦫 110.000+ castores",
        "badge2": "🌲 31.000 ha destruídos",
        "badge3": "Puerto Williams · Chile",
        "badge4": "Mar–Out 2025",
        "badge5": "3ª CONF. INT. CHIC 2025",
        "m1": "Castores estimados (2025)",
        "m2": "Represas construídas",
        "m3": "Hectares devastados",
        "m4": "Introdução inicial",
        "tab1": "🗺️ Mapa & Análise",
        "tab2": "🔬 Metodologia & Pipeline",
        "tab3": "💡 O que Descobrimos",
        "tab4": "📷 Em Campo",
        "tab5": "📚 Fontes & Créditos",
        "map_label": "GEOLOCALIZAÇÃO — ISLA NAVARINO",
        "map_title_top": "Mapa de Satélite (True Color) — Isla Navarino & Castoreiras",
        "map_title_heat": "Mapa de Calor — Intensidade do Impacto dos Castores",
        "map_hint_top": "🛰️ <strong>Mapa Superior · True Color:</strong> Visualização de satélite da Isla Navarino com os pontos de avistamento de castoreiras visitados por Amauri durante os trekkings (Mar–Out 2025). Clique nos marcadores para detalhes.",
        "map_hint_heat": "🔥 <strong>Mapa Inferior · Calor:</strong> Distribuição da intensidade do impacto dos castores na Isla Navarino com base nas áreas de maior concentração de represas e danos florestais documentados na literatura científica.",
        "chart_label": "ANÁLISE TEMPORAL DO IMPACTO",
        "chart_title": "Expansão da População de Castores (1946–2025)",
        "chart_title2": "Área de Floresta Destruída por Ano (estimativa acumulada)",
        "chart_title3": "Cascata de Invasão — Espécies em Puerto Williams",
        "method_label": "DOCUMENTAÇÃO CIENTÍFICA",
        "method_title": "Pergunta & Metodologia",
        "sci_question_title": "❓ Pergunta Central da Observação",
        "sci_question": "\"Como a introdução de 20 castores canadenses em 1946 transformou de forma irreversível o ecossistema subantártico da Isla Navarino, e quais são os sinais visíveis desse impacto ao nível do campo, observáveis durante trekkings em Puerto Williams em 2025?\"",
        "pipeline_label": "PIPELINE DE OBSERVAÇÃO",
        "steps": [
            ("1", "Residência Prolongada — Puerto Williams (Mar–Out 2025)",
             "8 meses de residência contínua na cidade de Puerto Williams, Isla Navarino, Chile — o assentamento humano permanente mais austral do mundo. Contato direto com o ecossistema subantártico, comunidade local e pesquisadores visitantes. Base de observação única para documentar o impacto dos castores em tempo real."),
            ("2", "Trekkings e Observação de Castoreiras",
             "Expedições a pé pelas trilhas da Isla Navarino para observação e registro fotográfico das castoreiras. Visita à castoreira mais próxima do centro urbano de Puerto Williams e à segunda castoreira, próxima à Laguna Rosa. Documentação in loco das árvores derrubadas, represas ativas e 'florestas fantasma'."),
            ("3", "3ª Conferência Internacional CHIC 2025 — Como Convidado",
             "Participação como convidado observador na 3ª Conferência Internacional CHIC (Conservación de Humedales y Islas del Cono sur) realizada em Puerto Williams. Acompanhamento das palestras científicas sobre espécies invasoras, ecologia subantártica e estratégias de controle do castor na Patagônia."),
            ("4", "Rede Científica Internacional",
             "Interação com pesquisadores internacionais presentes na Conferência CHIC, incluindo Guilherme (Bélgica) e Nicolas (França), que apresentaram trabalho sobre castores na Isla Navarino. Troca de perspectivas entre observação de campo local e pesquisa científica internacional."),
            ("5", "Análise de Dados Publicados + Observação de Campo",
             "Cruzamento das observações pessoais de campo (2025) com a literatura científica consolidada: National Geographic (2019), estudos GEF, Universidade do Texas do Norte, artigos peer-reviewed sobre cascata de invasão biológica em Navarino. Dados quantitativos: 110.000 castores, 70.600 represas, 31.000 ha destruídos."),
            ("6", "Documentação Fotográfica e Divulgação",
             "Registro fotográfico das castoreiras, encontros científicos e registros pessoais em campo. Publicação como projeto de portfólio de pesquisa ambiental para divulgação científica acessível sobre o impacto de espécies exóticas invasoras em ecossistemas isolados."),
        ],
        "bio_title": "🦫 Biologia do Castor Invasor (Castor canadensis)",
        "bio_text": "• <b>Origem:</b> América do Norte (Manitoba, Canadá)<br>• <b>Introdução:</b> 1946 — Exército Argentino — 10 casais em Tierra del Fuego<br>• <b>Objetivo original:</b> Indústria de pele (fracassou — pele valia US$ 10–20)<br>• <b>Sem predadores naturais</b> na Patagônia (sem lobos, sem grandes felinos)<br>• <b>Árvores sul-americanas</b> não evoluíram defesas contra castores<br>• <b>Comportamento:</b> Derruba faias-lenga, constrói represas, inunda florestas",
        "impact_title": "🌲 Impacto Ecológico em Cascata",
        "impact_text": "• <b>Fase 1:</b> Castores constroem represas → florestas inundadas → árvores morrem<br>• <b>Fase 2:</b> Água parada atrai <b>arganazes</b> (segunda espécie invasora)<br>• <b>Fase 3:</b> Arganazes atraem <b>martas</b> (terceira espécie invasora)<br>• <b>Martas</b> caçam gansos, patos e roedores nativos<br>• <b>Resultado:</b> 'Processo descontrolado de invasão' — Univ. Texas do Norte (2016)",
        "discovery_label": "DESCOBERTAS DO CAMPO",
        "discovery_title": "O que o Campo Revelou",
        "discoveries": [
            ("🦫", "A castoreira mais próxima de Puerto Williams — visível a pé",
             "Durante os trekkings, foi possível observar de perto a castoreira mais próxima ao centro urbano de Puerto Williams. A proximidade com a cidade ilustra a velocidade de expansão dos castores — animais que 'não reconhecem fronteiras' e avançam mesmo em áreas próximas a assentamentos humanos."),
            ("🌲", "Florestas fantasma — a marca visual mais impactante",
             "O sinal mais perturbador observado em campo foi a 'floresta fantasma': extensas áreas com troncos esbranquiçados, galhos sem folhas e tocos retorcidos. Árvores faia-lenga milenares sem qualquer sinal de regeneração — a consequência direta da inundação causada pelas represas dos castores, que substituem água corrente por água parada."),
            ("🌊", "Laguna Rosa — castoreira em área de beleza cênica preservada",
             "A segunda castoreira observada, próxima à Laguna Rosa, demonstra que os castores avançam mesmo em áreas de alto valor paisagístico. A represa ativa próxima à laguna altera o nível e a qualidade da água, com potencial impacto sobre a fauna aquática nativa da ilha."),
            ("🎓", "3ª Conf. CHIC 2025 — a ciência no fim do mundo",
             "A participação como convidado na 3ª Conferência Internacional CHIC em Puerto Williams revelou a dimensão global do problema: pesquisadores de Bélgica, França, Chile, Argentina e outros países reunidos para discutir soluções. A conferência mostrou que Puerto Williams se tornou um polo científico subantártico de referência mundial."),
            ("🔗", "Cascata de invasão — o castor como 'espécie-chave do caos'",
             "A observação de campo confirmou o que a literatura científica descreve: o castor não destrói sozinho. Ao criar lagos de água parada, ele abre espaço para arganazes e martas — duas outras espécies invasoras que completam a cascata de destruição sobre a fauna nativa. Um ecossistema 'hackeado' por uma única decisão humana de 1946."),
            ("📊", "110.000 castores e 70.000 represas — escala impossível de imaginar sem ver",
             "Os dados são conhecidos, mas a experiência de campo em Puerto Williams dá uma dimensão humana aos números. Cada castoreira visitada representa centenas de metros cúbicos de floresta inundada, décadas de crescimento florestal destruídos, e um ecossistema que levará séculos para se recuperar — se algum dia se recuperar completamente."),
        ],
        "conclusion_label": "REFLEXÃO FINAL",
        "conclusion_title": "Uma Decisão de 1946 que Ainda Ecoa",
        "conclusion_text": "Viver 8 meses em Puerto Williams, caminhar pelas castoreiras e assistir pesquisadores do mundo inteiro debaterem soluções para um problema criado por 20 animais soltos em 1946 é uma experiência que redefine a compreensão sobre responsabilidade ecológica. A culpa não é dos castores — é do homem. E a reversão desse erro é o maior desafio de restauração de ecossistemas que a Patagônia já enfrentou.",
        "conclusion_author": "Amauri Almeida · Observação de campo · Puerto Williams, Isla Navarino, Chile · Mar–Out 2025",
        "field_label": "REGISTRO PESSOAL DE CAMPO",
        "field_title": "8 Meses no Fim do Mundo",
        "field_instructions_title": "📁 Como adicionar suas fotos",
        "field_instructions": "Coloque suas fotos na pasta <code>assets/campo/</code> com os nomes exatos abaixo. O sistema detecta automaticamente e substitui o placeholder pela imagem real.",
        "photos": [
            {
                "emoji": "🦫",
                "titulo": "Castoreira 1 — A Mais Próxima de Puerto Williams",
                "desc": "A castoreira mais próxima do centro urbano de Puerto Williams, observada durante trekking a pé pela Isla Navarino. A proximidade com a cidade demonstra a velocidade de avanço dos castores — a represa ativa altera o curso natural das águas e inunda a floresta de faia-lenga adjacente, criando a característica 'floresta fantasma' da ilha.",
                "path": "assets/campo/01_castoreira_pw_centro.jpg",
                "legenda": "Castoreira 1 · Próxima a Puerto Williams · Isla Navarino, Chile · 2025"
            },
            {
                "emoji": "🤳",
                "titulo": "Selfie — Castoreira 1 · Março 2025",
                "desc": "Registro pessoal de Amauri Almeida na primeira castoreira visitada em Puerto Williams, março de 2025. A represa ao fundo mostra a estrutura construída pelos castores canadenses — feita de troncos, galhos e lama — que desvia o curso d'água e inunda hectares de floresta subantártica.",
                "path": "assets/campo/02_selfie_castoreira1_marco2025.jpg",
                "legenda": "Amauri Almeida · Castoreira 1 · Puerto Williams · Março 2025",
                "destaque": True
            },
            {
                "emoji": "🌊",
                "titulo": "Castoreira 2 — Próxima à Laguna Rosa",
                "desc": "Segunda castoreira observada durante trekking, localizada nas proximidades da Laguna Rosa na Isla Navarino. A represa ativa neste ponto demonstra como os castores avançam em direção a áreas de alto valor paisagístico e ecológico, alterando o nível hídrico e a qualidade da água da laguna.",
                "path": "assets/campo/03_castoreira2_laguna_rosa.jpg",
                "legenda": "Castoreira 2 · Próxima à Laguna Rosa · Isla Navarino, Chile · 2025"
            },
            {
                "emoji": "📸",
                "titulo": "Castoreira 2 — Laguna Rosa (Vista 2)",
                "desc": "Segunda perspectiva da castoreira próxima à Laguna Rosa. A extensão da área alagada e os troncos de faia-lenga mortos ao fundo evidenciam o processo de substituição da floresta viva por água parada — condição que favorece espécies invasoras secundárias como arganazes e martas, intensificando a cascata de impacto ecológico.",
                "path": "assets/campo/04_castoreira2_laguna_rosa_v2.jpg",
                "legenda": "Castoreira 2 · Laguna Rosa · Vista da floresta fantasma ao fundo · Isla Navarino · 2025"
            },
            {
                "emoji": "🤳",
                "titulo": "Selfie — Castoreira 2 · Laguna Rosa",
                "desc": "Registro pessoal de Amauri Almeida na castoreira próxima à Laguna Rosa. A imagem captura o contraste entre o turista/observador e a magnitude da transformação da paisagem — faias-lenga milenares destruídas visíveis ao fundo, resultado direto da engenharia ecológica dos castores invasores.",
                "path": "assets/campo/05_selfie_castoreira2_laguna_rosa.jpg",
                "legenda": "Amauri Almeida · Castoreira 2 · Laguna Rosa · Isla Navarino · 2025"
            },
            {
                "emoji": "🎓",
                "titulo": "3ª Conferência Internacional CHIC 2025 — Puerto Williams",
                "desc": "Participação como convidado observador na 3ª Conferência Internacional CHIC (Conservación de Humedales y Islas del Cono sur) realizada em Puerto Williams, 2025. O evento reuniu pesquisadores internacionais para debater espécies invasoras, ecologia subantártica e estratégias binacionais de erradicação dos castores na Patagônia.",
                "path": "assets/campo/06_conferencia_chic_pw.jpg",
                "legenda": "3ª Conferência Internacional CHIC · Puerto Williams, Chile · 2025 · Como convidado observador"
            },
            {
                "emoji": "🔬",
                "titulo": "Guilherme (Bélgica) e Nicolas (França) — Apresentação sobre Castores",
                "desc": "Guilherme (Bélgica) e Nicolas (França) apresentam seu trabalho científico sobre os castores na Isla Navarino durante a 3ª Conferência CHIC em Puerto Williams. A pesquisa dos dois representa a dimensão internacional do problema — pesquisadores europeus dedicados ao estudo de uma espécie invasora introduzida por um governo sul-americano há quase 80 anos.",
                "path": "assets/campo/07_guilherme_nicolas_apresentacao.jpg",
                "legenda": "Guilherme (Bélgica) e Nicolas (França) · Apresentação sobre castores · 3ª CHIC · Puerto Williams · 2025"
            },
            {
                "emoji": "🥂",
                "titulo": "Brinde dos Participantes — Conferência CHIC 2025",
                "desc": "Confraternização entre os participantes da 3ª Conferência Internacional CHIC em Puerto Williams. O encontro no fim do mundo — na cidade mais austral do planeta — reúne cientistas, conservacionistas e observadores de múltiplos países em torno de um problema ecológico urgente que une Argentina e Chile numa das maiores operações de erradicação de espécies invasoras já tentadas.",
                "path": "assets/campo/08_brinde_participantes_chic.jpg",
                "legenda": "Brinde · Participantes da 3ª Conferência CHIC · Puerto Williams, Chile · 2025"
            },
        ],
        "timeline_field_label": "LINHA DO TEMPO — CAMPO E CIÊNCIA",
        "timeline_field_items": [
            ("1946", "20 castores canadenses introduzidos em Tierra del Fuego",
             "Exército Argentino solta 10 casais às margens do Lago Fagnano · Objetivo: indústria de pele · Resultado: catástrofe ecológica"),
            ("1960s", "Castores cruzam para o Chile",
             "Expansão para o lado chileno de Tierra del Fuego · Sem predadores naturais, a população explode"),
            ("1990s", "Avistamentos no continente sul-americano",
             "Castores venceram as correntes do Estreito de Magalhães · Chegaram à Península de Brunswick · Área colonizada: 69.900 km²"),
            ("2008", "Acordo Argentina–Chile para erradicação",
             "Ambos os países reconhecem que controle não basta · Meta: erradicação total · Custo estimado: US$ 33 milhões"),
            ("2016", "Projeto-piloto de erradicação (GEF)",
             "Projetos-piloto na região Esmeralda-Lasifashaj · 204 castores removidos · 70.600 represas mapeadas por satélite"),
            ("Mar 2025", "Amauri chega a Puerto Williams",
             "Início de 8 meses de residência · Primeiros trekkings · Primeiras castoreiras visitadas · Março 2025"),
            ("2025", "3ª Conferência Internacional CHIC",
             "Guilherme (Bélgica) e Nicolas (França) apresentam pesquisa sobre castores · Participação como convidado observador"),
            ("Out 2025", "Encerramento da observação de campo",
             "8 meses de registro · Castoreiras 1 e 2 documentadas · Conferência CHIC acompanhada · Outubro 2025"),
        ],
        "sources_label": "REFERÊNCIAS CIENTÍFICAS",
        "sources_title": "Fontes & Base de Dados",
        "tech_label": "TECNOLOGIAS UTILIZADAS",
        "footer_title": "🦫 Amauri Almeida",
        "footer_desc": "Tecnólogo em Gestão Ambiental · FATEC Jundiaí<br>Pós-Graduação em IA, Machine Learning & Data Science · Ciência de Dados & Big Data<br>Análise e Desenvolvimento de Sistemas · FACINT Maringá",
        "footer_links": "📍 Puerto Williams · Isla Navarino · Chile (Mar–Out 2025) | Fernandópolis · SP · Brasil",
    },

    # ── ESPANHOL ─────────────────────────────────────────────
    "es": {
        "page_title": "Especies Invasoras · Isla Navarino",
        "hero_tag": "OBSERVACIÓN DE CAMPO · PUERTO WILLIAMS · ISLA NAVARINO · MAR–OCT 2025",
        "hero_title": "Impacto de las Especies\nExóticas Invasoras",
        "hero_subtitle": "Observación de campo de las represas de castores y el ecosistema subantártico de Isla Navarino durante 8 meses de residencia en Puerto Williams, Chile (marzo–octubre 2025). El mayor desastre ecológico de bosques subantárticos desde la última era del hielo.",
        "badge1": "🦫 110.000+ castores",
        "badge2": "🌲 31.000 ha destruidos",
        "badge3": "Puerto Williams · Chile",
        "badge4": "Mar–Oct 2025",
        "badge5": "3ª CONF. INT. CHIC 2025",
        "m1": "Castores estimados (2025)",
        "m2": "Represas construidas",
        "m3": "Hectáreas devastadas",
        "m4": "Introducción inicial",
        "tab1": "🗺️ Mapa & Análisis",
        "tab2": "🔬 Metodología & Pipeline",
        "tab3": "💡 Lo que Descubrimos",
        "tab4": "📷 En Campo",
        "tab5": "📚 Fuentes & Créditos",
        "map_label": "GEOLOCALIZACIÓN — ISLA NAVARINO",
        "map_title_top": "Mapa de Satélite (True Color) — Isla Navarino & Represas",
        "map_title_heat": "Mapa de Calor — Intensidad del Impacto de los Castores",
        "map_hint_top": "🛰️ <strong>Mapa Superior · True Color:</strong> Vista satelital de Isla Navarino con los puntos de avistamiento de represas de castores visitados por Amauri durante los trekkings (Mar–Oct 2025).",
        "map_hint_heat": "🔥 <strong>Mapa Inferior · Calor:</strong> Distribución de la intensidad del impacto de los castores en Isla Navarino basada en áreas de mayor concentración de represas y daños forestales.",
        "chart_label": "ANÁLISIS TEMPORAL DEL IMPACTO",
        "chart_title": "Expansión de la Población de Castores (1946–2025)",
        "chart_title2": "Área de Bosque Destruida por Año (estimativa acumulada)",
        "chart_title3": "Cascada de Invasión — Especies en Puerto Williams",
        "method_label": "DOCUMENTACIÓN CIENTÍFICA",
        "method_title": "Pregunta & Metodología",
        "sci_question_title": "❓ Pregunta Central de la Observación",
        "sci_question": "\"¿Cómo la introducción de 20 castores canadienses en 1946 transformó de forma irreversible el ecosistema subantártico de Isla Navarino, y cuáles son las señales visibles de ese impacto a nivel de campo, observables durante trekkings en Puerto Williams en 2025?\"",
        "pipeline_label": "PIPELINE DE OBSERVACIÓN",
        "steps": [
            ("1", "Residencia Prolongada — Puerto Williams (Mar–Oct 2025)", "8 meses de residencia continua en Puerto Williams, Isla Navarino, Chile — el asentamiento humano permanente más austral del mundo. Contacto directo con el ecosistema subantártico, comunidad local e investigadores visitantes."),
            ("2", "Trekkings y Observación de Represas de Castores", "Expediciones a pie por los senderos de Isla Navarino para observación y registro fotográfico de las represas. Visita a la represa más cercana al centro urbano de Puerto Williams y a la segunda, próxima a Laguna Rosa. Documentación in situ de árboles derribados, represas activas y 'bosques fantasma'."),
            ("3", "3ª Conferencia Internacional CHIC 2025 — Como Invitado", "Participación como observador invitado en la 3ª Conferencia Internacional CHIC en Puerto Williams. Seguimiento de las ponencias científicas sobre especies invasoras, ecología subantártica y estrategias de control del castor en la Patagonia."),
            ("4", "Red Científica Internacional", "Interacción con investigadores internacionales en la Conferencia CHIC, incluyendo Guilherme (Bélgica) y Nicolas (Francia), que presentaron trabajo sobre castores en Isla Navarino."),
            ("5", "Análisis de Datos Publicados + Observación de Campo", "Cruce de observaciones personales de campo (2025) con la literatura científica consolidada: National Geographic (2019), estudios GEF, Universidad del Norte de Texas. Datos: 110.000 castores, 70.600 represas, 31.000 ha destruidos."),
            ("6", "Documentación Fotográfica y Divulgación", "Registro fotográfico de las represas, encuentros científicos y registros personales en campo. Publicación como proyecto de portfolio de investigación ambiental para divulgación científica accesible."),
        ],
        "bio_title": "🦫 Biología del Castor Invasor (Castor canadensis)",
        "bio_text": "• <b>Origen:</b> América del Norte (Manitoba, Canadá)<br>• <b>Introducción:</b> 1946 — Ejército Argentino — 10 parejas en Tierra del Fuego<br>• <b>Objetivo original:</b> Industria peletera (fracasó — piel valía US$ 10–20)<br>• <b>Sin depredadores naturales</b> en la Patagonia<br>• <b>Árboles sudamericanos</b> no evolucionaron defensas contra castores<br>• <b>Comportamiento:</b> Derriba lengas, construye represas, inunda bosques",
        "impact_title": "🌲 Impacto Ecológico en Cascada",
        "impact_text": "• <b>Fase 1:</b> Castores construyen represas → bosques inundados → árboles mueren<br>• <b>Fase 2:</b> Agua estancada atrae <b>ratas almizcleras</b> (segunda especie invasora)<br>• <b>Fase 3:</b> Ratas atraen <b>visones</b> (tercera especie invasora)<br>• <b>Visones</b> cazan gansos, patos y roedores nativos<br>• <b>Resultado:</b> 'Proceso descontrolado de invasión' — Univ. Texas del Norte (2016)",
        "discovery_label": "HALLAZGOS DEL CAMPO",
        "discovery_title": "Lo que el Campo Reveló",
        "discoveries": [
            ("🦫", "La represa más cercana a Puerto Williams — visible a pie", "Durante los trekkings, se pudo observar de cerca la represa más próxima al centro urbano de Puerto Williams. La proximidad con la ciudad ilustra la velocidad de expansión de los castores — animales que 'no reconocen fronteras'."),
            ("🌲", "Bosques fantasma — la marca visual más impactante", "La señal más perturbadora observada en campo fue el 'bosque fantasma': extensas áreas con troncos blanquecinos, ramas sin hojas y tocones retorcidos. Lengas milenarias sin señal de regeneración."),
            ("🌊", "Laguna Rosa — represa en área de belleza escénica preservada", "La segunda represa observada, próxima a Laguna Rosa, demuestra que los castores avanzan incluso en áreas de alto valor paisagístico y ecológico."),
            ("🎓", "3ª Conf. CHIC 2025 — la ciencia en el fin del mundo", "La participación como invitado en la 3ª Conferencia CHIC reveló la dimensión global del problema: investigadores de Bélgica, Francia, Chile, Argentina reunidos para discutir soluciones."),
            ("🔗", "Cascada de invasión — el castor como 'especie clave del caos'", "La observación de campo confirmó lo que la literatura describe: el castor no destruye solo. Al crear lagunas de agua estancada, abre espacio para visones y ratas almizcleras."),
            ("📊", "110.000 castores y 70.000 represas — escala imposible sin ver", "Los datos son conocidos, pero la experiencia de campo en Puerto Williams da una dimensión humana a los números. Cada represa visitada representa hectáreas de bosque inundado y décadas de crecimiento forestal destruidos."),
        ],
        "conclusion_label": "REFLEXIÓN FINAL",
        "conclusion_title": "Una Decisión de 1946 que Aún Resuena",
        "conclusion_text": "Vivir 8 meses en Puerto Williams, caminar por las represas y presenciar investigadores de todo el mundo debatir soluciones para un problema creado por 20 animales soltados en 1946 redefine la comprensión sobre responsabilidad ecológica. La culpa no es de los castores — es del hombre.",
        "conclusion_author": "Amauri Almeida · Observación de campo · Puerto Williams, Isla Navarino, Chile · Mar–Oct 2025",
        "field_label": "REGISTRO PERSONAL DE CAMPO",
        "field_title": "8 Meses en el Fin del Mundo",
        "field_instructions_title": "📁 Cómo agregar sus fotos",
        "field_instructions": "Coloque sus fotos en la carpeta <code>assets/campo/</code> con los nombres exactos indicados en cada tarjeta.",
        "photos": [
            {"emoji": "🦫", "titulo": "Represa 1 — La Más Cercana a Puerto Williams", "desc": "La represa más cercana al centro urbano de Puerto Williams, observada durante trekking por Isla Navarino. La proximidad con la ciudad demuestra la velocidad de avance de los castores.", "path": "assets/campo/01_castoreira_pw_centro.jpg", "legenda": "Represa 1 · Cerca de Puerto Williams · Isla Navarino, Chile · 2025"},
            {"emoji": "🤳", "titulo": "Selfie — Represa 1 · Marzo 2025", "desc": "Registro personal de Amauri Almeida en la primera represa visitada en Puerto Williams, marzo 2025.", "path": "assets/campo/02_selfie_castoreira1_marco2025.jpg", "legenda": "Amauri Almeida · Represa 1 · Puerto Williams · Marzo 2025", "destaque": True},
            {"emoji": "🌊", "titulo": "Represa 2 — Cerca de Laguna Rosa", "desc": "Segunda represa observada en trekking, próxima a Laguna Rosa en Isla Navarino.", "path": "assets/campo/03_castoreira2_laguna_rosa.jpg", "legenda": "Represa 2 · Laguna Rosa · Isla Navarino · 2025"},
            {"emoji": "📸", "titulo": "Represa 2 — Laguna Rosa (Vista 2)", "desc": "Segunda perspectiva de la represa próxima a Laguna Rosa. Troncos de lengas muertos al fondo.", "path": "assets/campo/04_castoreira2_laguna_rosa_v2.jpg", "legenda": "Represa 2 · Laguna Rosa · Bosque fantasma al fondo · Isla Navarino · 2025"},
            {"emoji": "🤳", "titulo": "Selfie — Represa 2 · Laguna Rosa", "desc": "Registro personal en la represa próxima a Laguna Rosa. Lengas milenarias destruidas al fondo.", "path": "assets/campo/05_selfie_castoreira2_laguna_rosa.jpg", "legenda": "Amauri Almeida · Represa 2 · Laguna Rosa · Isla Navarino · 2025"},
            {"emoji": "🎓", "titulo": "3ª Conferencia Internacional CHIC 2025 — Puerto Williams", "desc": "Participación como observador invitado en la 3ª Conferencia Internacional CHIC en Puerto Williams, 2025.", "path": "assets/campo/06_conferencia_chic_pw.jpg", "legenda": "3ª Conferencia CHIC · Puerto Williams · 2025 · Como invitado observador"},
            {"emoji": "🔬", "titulo": "Guilherme (Bélgica) y Nicolas (Francia) — Presentación sobre Castores", "desc": "Guilherme y Nicolas presentan su trabajo sobre castores en Isla Navarino en la 3ª Conferencia CHIC.", "path": "assets/campo/07_guilherme_nicolas_apresentacao.jpg", "legenda": "Guilherme (Bélgica) y Nicolas (Francia) · 3ª CHIC · Puerto Williams · 2025"},
            {"emoji": "🥂", "titulo": "Brindis — Conferencia CHIC 2025", "desc": "Confraternización entre participantes de la 3ª Conferencia Internacional CHIC en Puerto Williams.", "path": "assets/campo/08_brinde_participantes_chic.jpg", "legenda": "Brindis · Participantes 3ª CHIC · Puerto Williams · 2025"},
        ],
        "timeline_field_label": "CRONOLOGÍA — CAMPO Y CIENCIA",
        "timeline_field_items": [
            ("1946", "20 castores canadienses introducidos en Tierra del Fuego", "Ejército Argentino suelta 10 parejas junto al Lago Fagnano · Objetivo: industria peletera · Resultado: catástrofe ecológica"),
            ("1960s", "Castores cruzan a Chile", "Expansión al lado chileno · Sin depredadores naturales · La población explota"),
            ("1990s", "Avistamientos en el continente sudamericano", "Cruzaron el Estrecho de Magallanes · Área colonizada: 69.900 km²"),
            ("2008", "Acuerdo Argentina–Chile para erradicación", "Meta: erradicación total · Costo estimado: US$ 33 millones"),
            ("2016", "Proyecto piloto de erradicación (GEF)", "204 castores removidos · 70.600 represas mapeadas por satélite"),
            ("Mar 2025", "Amauri llega a Puerto Williams", "Inicio de 8 meses de residencia · Primeros trekkings · Marzo 2025"),
            ("2025", "3ª Conferencia Internacional CHIC", "Guilherme y Nicolas presentan sobre castores · Participación como invitado"),
            ("Oct 2025", "Fin de la observación de campo", "8 meses de registro · Represas 1 y 2 documentadas · Octubre 2025"),
        ],
        "sources_label": "REFERENCIAS CIENTÍFICAS",
        "sources_title": "Fuentes & Base de Datos",
        "tech_label": "TECNOLOGÍAS UTILIZADAS",
        "footer_title": "🦫 Amauri Almeida",
        "footer_desc": "Tecnólogo en Gestión Ambiental · FATEC Jundiaí<br>Posgrado en IA, Machine Learning & Data Science · Ciencia de Datos & Big Data<br>Análisis y Desarrollo de Sistemas · FACINT Maringá",
        "footer_links": "📍 Puerto Williams · Isla Navarino · Chile (Mar–Oct 2025) | Fernandópolis · SP · Brasil",
    },

    # ── INGLÊS ───────────────────────────────────────────────
    "en": {
        "page_title": "Invasive Species · Isla Navarino",
        "hero_tag": "FIELD OBSERVATION · PUERTO WILLIAMS · ISLA NAVARINO · MAR–OCT 2025",
        "hero_title": "Impact of Invasive\nAlien Species",
        "hero_subtitle": "Field observation of beaver dams and the subantarctic ecosystem of Isla Navarino during 8 months of residence in Puerto Williams, Chile (March–October 2025). The largest ecological transformation of subantarctic forests since the last ice age.",
        "badge1": "🦫 110,000+ beavers",
        "badge2": "🌲 31,000 ha destroyed",
        "badge3": "Puerto Williams · Chile",
        "badge4": "Mar–Oct 2025",
        "badge5": "3rd INT. CONF. CHIC 2025",
        "m1": "Estimated beavers (2025)",
        "m2": "Dams built",
        "m3": "Hectares devastated",
        "m4": "Initial introduction",
        "tab1": "🗺️ Map & Analysis",
        "tab2": "🔬 Methodology & Pipeline",
        "tab3": "💡 What We Found",
        "tab4": "📷 Field Research",
        "tab5": "📚 Sources & Credits",
        "map_label": "GEOLOCATION — ISLA NAVARINO",
        "map_title_top": "Satellite Map (True Color) — Isla Navarino & Beaver Dams",
        "map_title_heat": "Heat Map — Intensity of Beaver Impact",
        "map_hint_top": "🛰️ <strong>Top Map · True Color:</strong> Satellite view of Isla Navarino with beaver dam sighting points visited by Amauri during treks (Mar–Oct 2025). Click markers for details.",
        "map_hint_heat": "🔥 <strong>Bottom Map · Heat:</strong> Distribution of beaver impact intensity on Isla Navarino based on areas of highest dam concentration and documented forest damage.",
        "chart_label": "TEMPORAL IMPACT ANALYSIS",
        "chart_title": "Beaver Population Expansion (1946–2025)",
        "chart_title2": "Forest Area Destroyed per Year (cumulative estimate)",
        "chart_title3": "Invasion Cascade — Species in Puerto Williams",
        "method_label": "SCIENTIFIC DOCUMENTATION",
        "method_title": "Research Question & Methodology",
        "sci_question_title": "❓ Central Observation Question",
        "sci_question": "\"How did the introduction of 20 Canadian beavers in 1946 irreversibly transform the subantarctic ecosystem of Isla Navarino, and what are the visible field signs of that impact, observable during treks in Puerto Williams in 2025?\"",
        "pipeline_label": "OBSERVATION PIPELINE",
        "steps": [
            ("1", "Extended Residence — Puerto Williams (Mar–Oct 2025)", "8 months of continuous residence in Puerto Williams, Isla Navarino, Chile — the world's southernmost permanent human settlement. Direct contact with the subantarctic ecosystem, local community and visiting researchers."),
            ("2", "Treks and Beaver Dam Observation", "On-foot expeditions along Isla Navarino trails for observation and photographic record of beaver dams. Visit to the dam closest to Puerto Williams city center and the second dam near Laguna Rosa. In-situ documentation of felled trees, active dams and 'ghost forests'."),
            ("3", "3rd Int. CHIC Conference 2025 — As Guest Observer", "Participation as observer guest at the 3rd International CHIC Conference in Puerto Williams. Attended scientific talks on invasive species, subantarctic ecology and beaver control strategies in Patagonia."),
            ("4", "International Scientific Network", "Interaction with international researchers at CHIC Conference, including Guilherme (Belgium) and Nicolas (France), who presented work on beavers in Isla Navarino."),
            ("5", "Published Data Analysis + Field Observation", "Cross-referencing personal field observations (2025) with established scientific literature: National Geographic (2019), GEF studies, University of North Texas. Key data: 110,000 beavers, 70,600 dams, 31,000 ha destroyed."),
            ("6", "Photographic Documentation and Science Communication", "Photographic record of beaver dams, scientific meetings and personal field records. Published as an environmental research portfolio project for accessible science communication on invasive species impact."),
        ],
        "bio_title": "🦫 Biology of the Invasive Beaver (Castor canadensis)",
        "bio_text": "• <b>Origin:</b> North America (Manitoba, Canada)<br>• <b>Introduction:</b> 1946 — Argentine Army — 10 pairs in Tierra del Fuego<br>• <b>Original purpose:</b> Fur trade (failed — pelt worth US$ 10–20)<br>• <b>No natural predators</b> in Patagonia<br>• <b>South American trees</b> never evolved defenses against beavers<br>• <b>Behavior:</b> Fells lenga beeches, builds dams, floods forests",
        "impact_title": "🌲 Cascading Ecological Impact",
        "impact_text": "• <b>Phase 1:</b> Beavers build dams → forests flooded → trees die<br>• <b>Phase 2:</b> Stagnant water attracts <b>muskrats</b> (second invasive species)<br>• <b>Phase 3:</b> Muskrats attract <b>mink</b> (third invasive species)<br>• <b>Mink</b> hunt geese, ducks and native rodents<br>• <b>Result:</b> 'Runaway invasion process' — Univ. North Texas (2016)",
        "discovery_label": "FIELD FINDINGS",
        "discovery_title": "What the Field Revealed",
        "discoveries": [
            ("🦫", "The dam closest to Puerto Williams — reachable on foot", "During treks, it was possible to observe up close the beaver dam nearest to Puerto Williams city center. Its proximity to the city illustrates the beavers' expansion speed — animals that 'recognize no borders'."),
            ("🌲", "Ghost forests — the most striking visual mark", "The most disturbing field observation was the 'ghost forest': vast areas of bleached trunks, bare branches and twisted stumps. Ancient lenga beeches with no sign of regeneration."),
            ("🌊", "Laguna Rosa — dam in a scenically preserved area", "The second dam, near Laguna Rosa, shows that beavers advance even into areas of high scenic and ecological value."),
            ("🎓", "3rd CHIC Conf. 2025 — science at the end of the world", "Attending the 3rd CHIC Conference as a guest revealed the global scale of the problem: researchers from Belgium, France, Chile, Argentina gathered to discuss solutions."),
            ("🔗", "Invasion cascade — the beaver as 'keystone of chaos'", "Field observation confirmed what the literature describes: the beaver does not destroy alone. By creating stagnant water, it opens space for muskrats and mink."),
            ("📊", "110,000 beavers and 70,000 dams — a scale impossible to grasp without seeing", "The data are well-known, but field experience in Puerto Williams gives a human dimension to the numbers. Each dam visited represents hectares of flooded forest and decades of forest growth destroyed."),
        ],
        "conclusion_label": "FINAL REFLECTION",
        "conclusion_title": "A 1946 Decision Still Echoing",
        "conclusion_text": "Living 8 months in Puerto Williams, walking through beaver dams and watching researchers from around the world debate solutions to a problem created by 20 animals released in 1946 redefines understanding of ecological responsibility. The beavers are not to blame — humans are.",
        "conclusion_author": "Amauri Almeida · Field observation · Puerto Williams, Isla Navarino, Chile · Mar–Oct 2025",
        "field_label": "PERSONAL FIELD RECORD",
        "field_title": "8 Months at the End of the World",
        "field_instructions_title": "📁 How to add your photos",
        "field_instructions": "Place your photos in the <code>assets/campo/</code> folder with the exact file names shown on each card.",
        "photos": [
            {"emoji": "🦫", "titulo": "Dam 1 — Closest to Puerto Williams", "desc": "The beaver dam nearest to Puerto Williams city center, observed during a trek on Isla Navarino. Proximity to the city illustrates the beavers' expansion speed.", "path": "assets/campo/01_castoreira_pw_centro.jpg", "legenda": "Dam 1 · Near Puerto Williams · Isla Navarino, Chile · 2025"},
            {"emoji": "🤳", "titulo": "Selfie — Dam 1 · March 2025", "desc": "Personal record of Amauri Almeida at the first beaver dam visited in Puerto Williams, March 2025.", "path": "assets/campo/02_selfie_castoreira1_marco2025.jpg", "legenda": "Amauri Almeida · Dam 1 · Puerto Williams · March 2025", "destaque": True},
            {"emoji": "🌊", "titulo": "Dam 2 — Near Laguna Rosa", "desc": "Second dam observed on trek, located near Laguna Rosa on Isla Navarino.", "path": "assets/campo/03_castoreira2_laguna_rosa.jpg", "legenda": "Dam 2 · Laguna Rosa · Isla Navarino · 2025"},
            {"emoji": "📸", "titulo": "Dam 2 — Laguna Rosa (View 2)", "desc": "Second view of the dam near Laguna Rosa. Dead lenga trunks visible in the background.", "path": "assets/campo/04_castoreira2_laguna_rosa_v2.jpg", "legenda": "Dam 2 · Laguna Rosa · Ghost forest in background · Isla Navarino · 2025"},
            {"emoji": "🤳", "titulo": "Selfie — Dam 2 · Laguna Rosa", "desc": "Personal record at the dam near Laguna Rosa. Ancient lengas destroyed in the background.", "path": "assets/campo/05_selfie_castoreira2_laguna_rosa.jpg", "legenda": "Amauri Almeida · Dam 2 · Laguna Rosa · Isla Navarino · 2025"},
            {"emoji": "🎓", "titulo": "3rd International CHIC Conference 2025 — Puerto Williams", "desc": "Participation as observer guest at the 3rd International CHIC Conference in Puerto Williams, 2025.", "path": "assets/campo/06_conferencia_chic_pw.jpg", "legenda": "3rd CHIC Conference · Puerto Williams · 2025 · As observer guest"},
            {"emoji": "🔬", "titulo": "Guilherme (Belgium) & Nicolas (France) — Beaver Presentation", "desc": "Guilherme and Nicolas present their scientific work on beavers at Isla Navarino at the 3rd CHIC Conference.", "path": "assets/campo/07_guilherme_nicolas_apresentacao.jpg", "legenda": "Guilherme (Belgium) & Nicolas (France) · 3rd CHIC · Puerto Williams · 2025"},
            {"emoji": "🥂", "titulo": "Toast — CHIC Conference 2025 Participants", "desc": "Gathering of participants at the 3rd International CHIC Conference in Puerto Williams — scientists and observers from multiple countries.", "path": "assets/campo/08_brinde_participantes_chic.jpg", "legenda": "Toast · 3rd CHIC Conference Participants · Puerto Williams · 2025"},
        ],
        "timeline_field_label": "TIMELINE — FIELD & SCIENCE",
        "timeline_field_items": [
            ("1946", "20 Canadian beavers introduced in Tierra del Fuego", "Argentine Army releases 10 pairs at Lago Fagnano shores · Goal: fur trade · Result: ecological disaster"),
            ("1960s", "Beavers cross to Chile", "Expansion to Chilean side · No natural predators · Population explodes"),
            ("1990s", "Sightings on the South American mainland", "Crossed the Strait of Magellan · Colonized area: 69,900 km²"),
            ("2008", "Argentina–Chile eradication agreement", "Goal: total eradication · Estimated cost: US$ 33 million"),
            ("2016", "GEF eradication pilot project", "204 beavers removed · 70,600 dams satellite-mapped"),
            ("Mar 2025", "Amauri arrives in Puerto Williams", "Start of 8-month residence · First treks · First dam visits · March 2025"),
            ("2025", "3rd International CHIC Conference", "Guilherme & Nicolas present beaver research · Attended as guest observer"),
            ("Oct 2025", "End of field observation", "8 months of records · Dams 1 and 2 documented · October 2025"),
        ],
        "sources_label": "SCIENTIFIC REFERENCES",
        "sources_title": "Sources & Database",
        "tech_label": "TECHNOLOGIES USED",
        "footer_title": "🦫 Amauri Almeida",
        "footer_desc": "Environmental Management Technologist · FATEC Jundiaí<br>Post-Grad in AI, Machine Learning & Data Science · Data Science & Big Data<br>Systems Analysis and Development · FACINT Maringá",
        "footer_links": "📍 Puerto Williams · Isla Navarino · Chile (Mar–Oct 2025) | Fernandópolis · SP · Brazil",
    },
}

# ── SELETOR ──────────────────────────────────────────────────
def render_lang_selector():
    c0, c1, c2, c3 = st.columns([8, 1, 1, 1])
    with c1:
        if st.button("🇧🇷 PT", use_container_width=True,
                     type="primary" if st.session_state.lang == "pt" else "secondary"):
            st.session_state.lang = "pt"; st.rerun()
    with c2:
        if st.button("🇪🇸 ES", use_container_width=True,
                     type="primary" if st.session_state.lang == "es" else "secondary"):
            st.session_state.lang = "es"; st.rerun()
    with c3:
        if st.button("🇺🇸 EN", use_container_width=True,
                     type="primary" if st.session_state.lang == "en" else "secondary"):
            st.session_state.lang = "en"; st.rerun()

render_lang_selector()
T = TRANSLATIONS[st.session_state.lang]

# ── ESTILOS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');
:root{
  --forest:#1B3A1E;--forest-mid:#2D5A32;--forest-light:#3D7A45;
  --earth:#5C3D1E;--earth-mid:#7A5230;--earth-light:#A06A3A;
  --water:#1A5C8A;--water-light:#2D8FBF;
  --ice:#D4EEF7;--cream:#F5F2EC;--warm-gray:#7A7060;
  --danger:#8B2515;--black:#0D1117;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--cream);color:var(--black);}
.hero-wrap{
  background:linear-gradient(135deg,var(--forest) 0%,var(--forest-mid) 55%,#1A4A20 100%);
  border-radius:20px;padding:3rem 2.5rem 2rem;margin-bottom:2rem;position:relative;overflow:hidden;
}
.hero-wrap::before{content:"🦫";font-size:180px;position:absolute;right:-10px;top:-20px;opacity:0.06;}
.hero-tag{background:#A8D5A2;color:var(--forest);font-family:'DM Mono',monospace;font-size:0.7rem;font-weight:bold;letter-spacing:2px;padding:4px 12px;border-radius:4px;display:inline-block;margin-bottom:1rem;text-transform:uppercase;}
.hero-title{font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:900;color:#fff;line-height:1.15;margin-bottom:0.8rem;white-space:pre-line;}
.hero-subtitle{font-size:1rem;color:rgba(255,255,255,0.78);max-width:680px;line-height:1.6;margin-bottom:1.5rem;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.85);font-size:0.72rem;font-family:'DM Mono',monospace;padding:5px 12px;border-radius:20px;letter-spacing:0.5px;}
.badge-forest{background:rgba(168,213,162,0.2);border-color:#A8D5A2;color:#A8D5A2;}
.metric-box{background:white;border-radius:16px;padding:1.4rem 1.2rem;border-top:4px solid var(--forest-light);box-shadow:0 2px 12px rgba(0,0,0,0.06);text-align:center;}
.metric-box.earth{border-top-color:var(--earth-light);}
.metric-box.water{border-top-color:var(--water-light);}
.metric-box.danger{border-top-color:var(--danger);}
.metric-val{font-family:'Playfair Display',serif;font-size:2.1rem;font-weight:900;color:var(--forest);line-height:1;margin-bottom:0.3rem;}
.metric-label{font-size:0.75rem;color:var(--warm-gray);text-transform:uppercase;letter-spacing:1px;}
.section-label{font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--forest-mid);text-transform:uppercase;letter-spacing:3px;margin-bottom:0.3rem;}
.section-title{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;color:var(--forest);margin-bottom:1.2rem;line-height:1.2;}
.info-card{background:white;border-radius:16px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.05);border-left:4px solid var(--forest-light);margin-bottom:1rem;}
.info-card.earth{border-left-color:var(--earth-light);}
.info-card.water{border-left-color:var(--water-light);}
.info-card.danger{border-left-color:var(--danger);}
.timeline-item{display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid #e8ede8;}
.timeline-year{font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;color:var(--forest-mid);min-width:80px;}
.timeline-title{font-weight:500;color:var(--forest);margin-bottom:0.2rem;}
.timeline-desc{font-size:0.85rem;color:var(--warm-gray);}
.source-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:0.8rem;}
.source-badge{background:var(--forest);color:white;font-family:'DM Mono',monospace;font-size:0.65rem;padding:4px 10px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;}
.method-step{display:flex;align-items:flex-start;gap:1rem;padding:1rem;background:white;border-radius:12px;margin-bottom:0.8rem;box-shadow:0 1px 6px rgba(0,0,0,0.04);}
.step-num{background:var(--forest-mid);color:white;font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step-title{font-weight:500;color:var(--forest);font-size:0.95rem;}
.step-desc{font-size:0.82rem;color:var(--warm-gray);margin-top:0.2rem;}
.discovery-box{background:linear-gradient(135deg,#EEF5EE,#DCF0DC);border:2px solid var(--forest-light);border-radius:16px;padding:1.8rem;margin:0.8rem 0;}
.discovery-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--forest);margin-bottom:0.5rem;}
.footer-wrap{background:var(--forest);border-radius:20px;padding:2rem;color:rgba(255,255,255,0.8);text-align:center;margin-top:3rem;}
.footer-title{font-family:'Playfair Display',serif;color:#A8D5A2;font-size:1.2rem;margin-bottom:0.5rem;}
.photo-placeholder{background:#EEF5EE;border:2px dashed var(--forest-light);border-radius:12px;padding:2rem;text-align:center;min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.photo-emoji{font-size:2.5rem;}
.photo-title{font-weight:600;color:var(--forest);margin:0.5rem 0 0.2rem;font-size:0.9rem;}
.photo-desc{font-size:0.78rem;color:var(--warm-gray);line-height:1.5;}
.photo-path{font-size:0.65rem;color:var(--forest-mid);font-family:'DM Mono',monospace;margin-top:0.5rem;background:#DCF0DC;padding:3px 8px;border-radius:4px;}
.photo-legenda{font-size:0.72rem;color:var(--warm-gray);font-style:italic;padding:0.5rem 0.8rem;background:#f5f5f0;text-align:center;border-top:1px solid #d8e8d8;}
.photo-destaque{border:3px solid var(--forest-light);border-radius:14px;overflow:hidden;box-shadow:0 4px 20px rgba(45,90,50,0.15);}
</style>
""", unsafe_allow_html=True)

# ── DADOS ─────────────────────────────────────────────────────
anos = [1946,1950,1955,1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2020,2025]
castores = [20,120,500,1500,4000,8000,15000,25000,40000,60000,75000,85000,95000,100000,105000,108000,110000]
ha_destruidos = [0,5,20,80,200,500,1200,2500,5000,9000,14000,19000,24000,27000,29000,30500,31000]

# Pontos de calor na Isla Navarino
# Baseados em concentrações conhecidas de castoreiras
heat_data = [
    [-54.93, -67.61, 0.9],  # Puerto Williams — castoreira 1 (mais próxima)
    [-54.96, -67.58, 0.85], # Laguna Rosa — castoreira 2
    [-55.02, -67.45, 0.7],
    [-55.10, -67.70, 0.75],
    [-54.88, -67.82, 0.8],
    [-55.15, -67.52, 0.65],
    [-54.85, -67.40, 0.6],
    [-55.20, -67.65, 0.72],
    [-54.78, -67.75, 0.55],
    [-55.08, -67.30, 0.5],
    [-55.25, -67.80, 0.68],
    [-54.95, -67.90, 0.62],
    [-55.18, -67.38, 0.58],
    [-54.82, -67.55, 0.45],
    [-55.30, -67.60, 0.7],
    [-55.05, -68.00, 0.65],
    [-54.90, -68.10, 0.5],
]

# Pontos de avistamento pessoal
pontos_campo = [
    {"nome": "Castoreira 1 — Puerto Williams (mais próxima da cidade)", "lat": -54.930, "lon": -67.612,
     "tipo": "castoreira", "cor": "orange", "icon": "paw",
     "desc": "Castoreira mais próxima do centro de Puerto Williams. Visitada durante trekking em 2025. Represa ativa com floresta fantasma adjacente."},
    {"nome": "Castoreira 2 — Próxima à Laguna Rosa", "lat": -54.963, "lon": -67.581,
     "tipo": "castoreira", "cor": "red", "icon": "paw",
     "desc": "Segunda castoreira visitada, próxima à Laguna Rosa. Área de alta beleza cênica com represa ativa alterando o nível hídrico."},
    {"nome": "Puerto Williams — Base de Observação (Mar–Out 2025)", "lat": -54.935, "lon": -67.616,
     "tipo": "base", "cor": "blue", "icon": "home",
     "desc": "Cidade de Puerto Williams — base dos 8 meses de residência. Local da 3ª Conferência Internacional CHIC 2025."},
    {"nome": "3ª Conferência CHIC 2025 — Puerto Williams", "lat": -54.934, "lon": -67.617,
     "tipo": "conferencia", "cor": "green", "icon": "graduation-cap",
     "desc": "Local da 3ª Conferência Internacional CHIC realizada em 2025. Participação como convidado observador."},
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
with c1: st.markdown('<div class="metric-box danger"><div class="metric-val">110.000+</div><div class="metric-label">'+T['m1']+'</div></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="metric-box earth"><div class="metric-val">70.600</div><div class="metric-label">'+T['m2']+'</div></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="metric-box"><div class="metric-val">31.000 ha</div><div class="metric-label">'+T['m3']+'</div></div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="metric-box water"><div class="metric-val">1946</div><div class="metric-label">'+T['m4']+'</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── ABAS ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([T['tab1'], T['tab2'], T['tab3'], T['tab4'], T['tab5']])

# ── TAB 1: MAPA ───────────────────────────────────────────────
with tab1:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)

    # ─ MAPA SUPERIOR: True Color / Satélite ─
    st.markdown(f'<div class="section-title" style="font-size:1.3rem">{T["map_title_top"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card">{T["map_hint_top"]}</div>', unsafe_allow_html=True)

    mapa_top = folium.Map(
        location=[-54.95, -67.65], zoom_start=10,
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery'
    )

    # Marcadores dos pontos
    icon_map = {
        "castoreira": ("orange", "paw"),
        "base": ("blue", "home"),
        "conferencia": ("green", "graduation-cap"),
    }
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

    # ─ MAPA INFERIOR: Heatmap ─
    st.markdown(f'<div class="section-title" style="font-size:1.3rem">{T["map_title_heat"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card earth">{T["map_hint_heat"]}</div>', unsafe_allow_html=True)

    mapa_heat = folium.Map(
        location=[-55.0, -67.6], zoom_start=9,
        tiles='CartoDB dark_matter'
    )
    HeatMap(
        data=heat_data,
        min_opacity=0.4,
        radius=35, blur=25,
        gradient={0.2: '#1B3A1E', 0.4: '#3D7A45', 0.65: '#F5A623', 0.85: '#E8340A', 1.0: '#FFFFFF'},
        name="Intensidade do Impacto"
    ).add_to(mapa_heat)

    # Pontos sobre o heatmap também
    for p in pontos_campo:
        folium.CircleMarker(
            location=[p["lat"], p["lon"]],
            radius=7, color='white', fill=True, fill_color='white',
            fill_opacity=0.9, weight=2,
            tooltip=p["nome"]
        ).add_to(mapa_heat)

    folium_static(mapa_heat, width=1100, height=420)

    # ─ GRÁFICOS ─
    st.markdown(f"<br><div class='section-label'>{T['chart_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['chart_title']}</div>", unsafe_allow_html=True)

    # Gráfico 1: Expansão da população
    fig_pop = go.Figure()
    fig_pop.add_trace(go.Scatter(
        x=anos, y=castores,
        mode='lines+markers',
        line=dict(color='#8B2515', width=3),
        marker=dict(size=8, color='#8B2515', symbol='circle',
                    line=dict(width=1, color='white')),
        fill='tozeroy', fillcolor='rgba(139,37,21,0.08)',
        name="Castores",
        hovertemplate='<b>%{x}</b><br>%{y:,.0f} castores<extra></extra>'
    ))
    fig_pop.add_vline(x=1946, line_dash="dash", line_color="#A06A3A",
                       annotation_text="  1946: Introdução", annotation_font_color="#A06A3A")
    fig_pop.add_vline(x=2008, line_dash="dash", line_color="#2D5A32",
                       annotation_text="  2008: Acordo de Erradicação", annotation_font_color="#2D5A32")
    fig_pop.add_annotation(x=2025, y=110000, text="🦫 2025: 110.000+",
                            showarrow=False, font=dict(color="#8B2515", size=11, family="DM Mono"),
                            xshift=-5, yshift=15)
    fig_pop.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(27,58,30,0.03)',
        font=dict(family='DM Sans'), height=360, showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#e8ede8',
                   title="Nº de castores (estimativa)"),
        margin=dict(t=30, b=20)
    )
    st.plotly_chart(fig_pop, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        fig_ha = go.Figure()
        fig_ha.add_trace(go.Bar(
            x=anos, y=ha_destruidos,
            marker=dict(
                color=ha_destruidos,
                colorscale=[[0,'#A8D5A2'],[0.4,'#3D7A45'],[0.7,'#A06A3A'],[1,'#8B2515']],
                line=dict(width=0)
            ),
            hovertemplate='<b>%{x}</b><br>%{y:,.0f} ha<extra></extra>',
            text=[f"{v//1000}k" if v >= 1000 else str(v) for v in ha_destruidos],
            textposition='outside', textfont=dict(size=9, family="DM Mono", color="#5C3D1E")
        ))
        fig_ha.update_layout(
            title=dict(text=T['chart_title2'], font=dict(size=13, family='Playfair Display')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=320, font=dict(family='DM Sans'), showlegend=False,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#e8ede8', title="Hectares acumulados"),
            margin=dict(t=50, b=20)
        )
        st.plotly_chart(fig_ha, use_container_width=True)

    with col_b:
        # Cascata de invasão
        especies = ["Castor<br>canadensis", "Arganazes<br>(muskrat)", "Martas<br>(mink)", "Fauna<br>nativa ⬇"]
        impacto = [100, 65, 45, -80]
        cores_casc = ['#8B2515','#A06A3A','#5C3D1E','#1A5C8A']
        fig_casc = go.Figure()
        for sp, imp, cor in zip(especies, impacto, cores_casc):
            fig_casc.add_trace(go.Bar(
                x=[sp], y=[abs(imp)],
                marker_color=cor, opacity=0.85,
                name=sp,
                text=[f"{'↑' if imp > 0 else '↓'} {abs(imp)}%"],
                textposition='outside',
                textfont=dict(size=11, color=cor, family="DM Mono"),
                hovertemplate=f'<b>{sp}</b><br>{imp:+d}%<extra></extra>'
            ))
        fig_casc.update_layout(
            title=dict(text=T['chart_title3'], font=dict(size=13, family='Playfair Display')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=320, font=dict(family='DM Sans'), showlegend=False,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#e8ede8', title="Impacto relativo (%)"),
            margin=dict(t=50, b=20)
        )
        st.plotly_chart(fig_casc, use_container_width=True)

# ── TAB 2: METODOLOGIA ────────────────────────────────────────
with tab2:
    st.markdown(f'<div class="section-label">{T["method_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["method_title"]}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="discovery-box">
      <div class="discovery-title">{T['sci_question_title']}</div>
      <p style="font-size:1.05rem;color:#1B3A1E;line-height:1.7"><em>{T['sci_question']}</em></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["pipeline_label"]}</div>', unsafe_allow_html=True)
    for num, title, desc in T['steps']:
        st.markdown(f"""
        <div class="method-step">
          <div class="step-num">{num}</div>
          <div class="step-content">
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
        <div class="info-card">
          <strong>{T['bio_title']}</strong><br><br>
          <div style="font-size:0.88rem;line-height:2.1">{T['bio_text']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="info-card danger">
          <strong>{T['impact_title']}</strong><br><br>
          <div style="font-size:0.88rem;line-height:2.1">{T['impact_text']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card water" style="margin-top:0.5rem;background:linear-gradient(135deg,#EAF4FB,#D0E8F5)">
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
    </div>
    """, unsafe_allow_html=True)

# ── TAB 3: DESCOBERTAS ────────────────────────────────────────
with tab3:
    st.markdown(f'<div class="section-label">{T["discovery_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["discovery_title"]}</div>', unsafe_allow_html=True)

    for emoji, titulo, texto in T['discoveries']:
        st.markdown(f"""
        <div class="discovery-box" style="margin-bottom:0.8rem">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <span style="font-size:1.5rem">{emoji}</span>
            <div>
              <div class="discovery-title">{titulo}</div>
              <p style="color:#1B3A1E;line-height:1.65;font-size:0.93rem;margin:0">{texto}</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["conclusion_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card" style="border-left-color:#1B3A1E;background:linear-gradient(135deg,#EEF5EE,#DCF0DC)">
      <strong style="color:#1B3A1E;font-size:1rem">{T['conclusion_title']}</strong><br><br>
      <p style="color:#1B3A1E;line-height:1.7;font-size:0.93rem">{T['conclusion_text']}</p>
      <p style="color:#3D7A45;font-size:0.82rem;margin-bottom:0"><em>{T['conclusion_author']}</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Gráfico final de impacto
    categorias_f = ["Castores\nestimados (÷1000)", "Represas\nmapeadas (÷1000)", "Hectares\ndestruídos (÷100)", "Custo anual\n(M USD)"]
    valores_f = [110, 70.6, 310, 66]
    cores_f = ['#8B2515','#A06A3A','#5C3D1E','#1A5C8A']
    fig_res = go.Figure()
    for cat, val, cor in zip(categorias_f, valores_f, cores_f):
        fig_res.add_trace(go.Bar(x=[cat], y=[val], marker_color=cor, opacity=0.85, showlegend=False,
                                  text=[f"{val:.0f}"], textposition='outside',
                                  textfont=dict(size=11, color=cor, family="DM Mono"),
                                  hovertemplate=f'<b>{cat}</b><br>{val}<extra></extra>'))
    fig_res.update_layout(
        title=dict(text="Resumo do Impacto — Castores na Patagônia (2025)", font=dict(size=14, family='Playfair Display')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=340, font=dict(family='DM Sans'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#e8ede8'),
        margin=dict(t=50, b=20)
    )
    st.plotly_chart(fig_res, use_container_width=True)

# ── TAB 4: EM CAMPO ───────────────────────────────────────────
with tab4:
    st.markdown(f'<div class="section-label">{T["field_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["field_title"]}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-card earth" style="margin-bottom:1.5rem">
      <strong>{T['field_instructions_title']}</strong><br>
      <div style="font-size:0.88rem;color:#5C3D1E;margin-top:0.4rem">{T['field_instructions']}</div>
    </div>
    """, unsafe_allow_html=True)

    photos = T['photos']
    foto_destaque = next((f for f in photos if f.get("destaque")), None)
    fotos_normais = [f for f in photos if not f.get("destaque")]

    # Grade 3 colunas
    for row_start in range(0, len(fotos_normais), 3):
        row_photos = fotos_normais[row_start:row_start + 3]
        cols = st.columns(len(row_photos))
        for col, foto in zip(cols, row_photos):
            with col:
                exists = os.path.exists(foto['path'])
                if exists:
                    st.image(foto['path'], use_container_width=True)
                else:
                    st.markdown(f"""
                    <div class="photo-placeholder">
                      <div class="photo-emoji">{foto['emoji']}</div>
                      <div class="photo-title">{foto['titulo']}</div>
                      <div class="photo-desc">{foto['desc']}</div>
                      <div class="photo-path">{foto['path']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(f'<div class="photo-legenda">{foto["legenda"]}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Destaque — largura total
    if foto_destaque:
        st.markdown("---")
        st.markdown('<div class="section-label" style="color:#3D7A45">⭐ DESTAQUE — REGISTRO PESSOAL DE CAMPO</div>', unsafe_allow_html=True)
        exists_dest = os.path.exists(foto_destaque['path'])
        if exists_dest:
            st.markdown('<div class="photo-destaque">', unsafe_allow_html=True)
            st.image(foto_destaque['path'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="photo-placeholder" style="min-height:300px">
              <div class="photo-emoji" style="font-size:3rem">{foto_destaque['emoji']}</div>
              <div class="photo-title" style="font-size:1.1rem">{foto_destaque['titulo']}</div>
              <div class="photo-desc" style="max-width:600px">{foto_destaque['desc']}</div>
              <div class="photo-path">{foto_destaque['path']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f'<div class="photo-legenda" style="font-size:0.82rem;padding:0.7rem 1.2rem">{foto_destaque["legenda"]}</div>', unsafe_allow_html=True)

    # Timeline
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="section-label">{T["timeline_field_label"]}</div>', unsafe_allow_html=True)
    for data, titulo, desc in T['timeline_field_items']:
        st.markdown(f"""
        <div class="timeline-item">
          <div class="timeline-year">{data}</div>
          <div style="flex:1">
            <div class="timeline-title">{titulo}</div>
            <div class="timeline-desc">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── TAB 5: FONTES ─────────────────────────────────────────────
with tab5:
    st.markdown(f'<div class="section-label">{T["sources_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["sources_title"]}</div>', unsafe_allow_html=True)

    fontes = [
        ("NAT GEO", "National Geographic Brasil — Haley Cohen Gilliland (2019)",
         "Argentina introduziu castores na Tierra del Fuego, mas não foi uma boa ideia. Publicado em ago/2019, atualizado nov/2020. Fotos: Luján Agusti.", "#1B3A1E"),
        ("GEF CASTOR", "Global Environment Facility (GEF) — Projeto Castor",
         "Parceria internacional Argentina–Chile para controle e erradicação dos castores. gefcastor.mma.gob.cl · 70.000–110.000 castores estimados.", "#3D7A45"),
        ("UNIV. TEXAS", "Universidade do Norte do Texas — Crego, Jiménez & Rozzi (2016)",
         "Biological Invasions · 'Runaway invasion process' em Isla Navarino · Cascata: castor → arganazes → martas → impacto fauna nativa.", "#5C3D1E"),
        ("J. BIOGEOGR.", "Journal of Biogeography (2009)",
         "Classificação do impacto dos castores na Patagônia como 'a maior alteração de paisagem em florestas subantárticas desde a última era do gelo'.", "#A06A3A"),
        ("ISSG/FAO", "ISSG — Invasive Species Specialist Group / FAO Chile",
         "Dados de área colonizada (69.900 km²), custo econômico (US$ 66 mi/ano na Argentina) e viabilidade da erradicação.", "#1A5C8A"),
        ("CHIC 2025", "3ª Conferência Internacional CHIC — Puerto Williams, 2025",
         "Conservación de Humedales y Islas del Cono sur · Participação como convidado observador · Pesquisadores: Guilherme (Bélgica), Nicolas (França) e outros.", "#2D5A32"),
        ("CAMPO", "Observação Pessoal de Campo — Amauri Almeida (2025)",
         "8 meses de residência em Puerto Williams, Isla Navarino (Mar–Out 2025). Trekkings e visitas às castoreiras 1 e 2. Registro fotográfico original.", "#3D7A45"),
    ]

    for sigla, nome, desc, cor in fontes:
        st.markdown(f"""
        <div class="info-card" style="border-left-color:{cor}">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <div style="background:{cor};color:white;font-family:'DM Mono',monospace;font-size:0.6rem;
                 padding:4px 7px;border-radius:4px;white-space:nowrap;flex-shrink:0;margin-top:2px;
                 letter-spacing:0.5px;font-weight:bold;text-align:center;min-width:70px">{sigla}</div>
            <div>
              <div style="font-weight:500;font-size:0.9rem;color:#1B3A1E">{nome}</div>
              <div style="font-size:0.82rem;color:#7A7060;margin-top:0.2rem">{desc}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"<br><div class='section-label'>{T['tech_label']}</div>", unsafe_allow_html=True)
    techs = ["Python 3.11", "Streamlit", "Plotly", "Folium", "Folium HeatMap", "Pandas", "NumPy", "ESRI World Imagery"]
    st.markdown(''.join([f'<span class="source-badge">{t}</span>' for t in techs]), unsafe_allow_html=True)

    st.markdown(f"""
    <div class="footer-wrap" style="margin-top:2rem">
      <div class="footer-title">{T['footer_title']}</div>
      <p style="margin:0.5rem 0;font-size:0.9rem">{T['footer_desc']}</p>
      <p style="margin:1rem 0 0.5rem;font-size:0.85rem;opacity:0.7">
        {T['footer_links']} &nbsp;|&nbsp;
        🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:#A8D5A2">Portfólio</a> &nbsp;|&nbsp;
        🐙 <a href="https://github.com/amaurialmeida" style="color:#A8D5A2">GitHub</a>
      </p>
      <p style="font-size:0.75rem;opacity:0.5;margin:0">© 2025–2026 · Espécies Invasoras · Isla Navarino · Puerto Williams, Chile</p>
    </div>
    """, unsafe_allow_html=True)
