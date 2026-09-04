import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="EcoMetric & ROI | Evaluación de Proyectos Sostenibles",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS de Máximo Contraste (Texto 100% Blanco y Azul Neón)
st.markdown(
    """
    <style>
    /* Fondo principal de la App */
    .stApp {
        background-color: #0b132a;
        color: #ffffff !important;
    }
    
    /* Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #111c3a;
        border-right: 2px solid #1e2d5a;
    }
    
    /* Textos, labels y desplegables en el Sidebar */
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Encabezado Principal */
    .corp-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 6px solid #10b981;
        padding: 24px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    .corp-title {
        color: #ffffff !important;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
    }
    .corp-subtitle {
        color: #38bdf8 !important;
        font-size: 1.1rem;
        margin-top: 6px;
        font-weight: 600;
    }
    
    /* Tarjetas de Métricas */
    .metric-card {
        background-color: #162244;
        border: 2px solid #233568;
        border-radius: 12px;
        padding: 22px;
        text-align: left;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
    }
    .metric-title {
        color: #38bdf8 !important;
        font-size: 0.95rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #10b981 !important;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.2;
    }
    .metric-description {
        color: #ffffff !important;
        font-size: 0.9rem;
        margin-top: 10px;
        line-height: 1.4;
    }

    /* Cajas Explicativas Generales */
    .explain-box {
        background-color: #101935;
        border: 2px solid #1e2e5c;
        border-radius: 10px;
        padding: 20px;
        margin-top: 18px;
        margin-bottom: 22px;
        color: #ffffff !important;
    }
    .explain-title {
        color: #38bdf8 !important;
        font-weight: 800;
        font-size: 1.15rem;
        margin-bottom: 10px;
    }
    .explain-box p, .explain-box li, .explain-box td, .explain-box th {
        color: #ffffff !important;
        font-size: 0.98rem;
        line-height: 1.6;
    }

    /* Títulos de Pestañas y Tablas */
    div[data-baseweb="tab"] p {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }
    button[aria-selected="true"] p {
        color: #38bdf8 !important;
    }
    
    /* Tablas de Streamlit en blanco */
    [data-testid="stTable"] td, [data-testid="stTable"] th {
        color: #ffffff !important;
        background-color: #101935 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. Barra Lateral: Lista Extensa de Monedas Latinoamericanas
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px 0;">
        <h2 style="color: #ffffff; margin:0; font-weight: 800;">🍃 EcoMetric & ROI</h2>
        <p style="color: #38bdf8; font-size: 0.85rem; margin:0;">EVALUACIÓN DE PROYECTOS SOSTENIBLES</p>
    </div>
""",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ Configuración del Modelo")

divisas_latam = [
    "COP (Peso Colombiano)",
    "USD (Dólar Estadounidense)",
    "VED (Bolívar Digital - Venezuela)",
    "VES (Bolívar Soberano - Venezuela)",
    "VEF (Bolívar Fuerte - Venezuela)",
    "EUR (Euro)",
    "MXN (Peso Mexicano)",
    "BRL (Real Brasileño)",
    "ARS (Peso Argentino)",
    "CLP (Peso Chileno)",
    "PEN (Sol Peruano)",
    "CRC (Colón Costarricense)",
    "DOP (Peso Dominicano)",
    "GTQ (Quetzal Guatemalteco)",
    "HNL (Lempira Hondureño)",
    "NIO (Córdoba Nicaragüense)",
    "PAB (Balboa Panameño)",
    "PYG (Guaraní Paraguayo)",
    "UYU (Peso Uruguayo)",
    "BOB (Boliviano)",
]

divisa_seleccionada = st.sidebar.selectbox("Moneda de Análisis", divisas_latam)
divisa = divisa_seleccionada.split(" ")[0]

capex = st.sidebar.number_input(
    f"Inversión Inicial CAPEX ({divisa})",
    min_value=1000,
    value=250000000,
    step=5000000,
)

ahorro_anual_base = st.sidebar.number_input(
    f"Ahorro Energético Anual ({divisa})",
    min_value=500,
    value=55000000,
    step=1000000,
)

opex_anual = st.sidebar.number_input(
    f"Costos Operativos OPEX ({divisa}/año)",
    min_value=0,
    value=4500000,
    step=500000,
)

horizonte_anios = st.sidebar.slider(
    "Horizonte de Evaluación (Años)",
    min_value=3,
    max_value=25,
    value=12,
)

tasa_descuento_pct = st.sidebar.slider(
    "Tasa de Descuento / WACC (%)",
    min_value=1.0,
    max_value=25.0,
    value=11.5,
    step=0.5,
)
tasa_descuento = tasa_descuento_pct / 100

st.sidebar.markdown("---")
st.sidebar.subheader("🍃 Factor Ambiental")

mwh_ahorrados = st.sidebar.number_input(
    "Energía Limpia Generada (MWh/año)",
    value=180.0,
    step=10.0,
)

factor_emision = st.sidebar.number_input(
    "Factor de Emisión (tCO2e por MWh)",
    value=0.126,
    format="%.3f",
)

# 3. Lógica Financiera
ahorro_neto_anual = ahorro_anual_base - opex_anual
anios = list(range(0, horizonte_anios + 1))
flujos_caja = [-capex] + [ahorro_neto_anual] * horizonte_anios

vpn = sum([f / ((1 + tasa_descuento) ** t) for t, f in enumerate(flujos_caja)])

try:
    tir = np.irr(flujos_caja)
except:
    tir = 0.0

flujo_acumulado = []
acumulado = 0
payback_year = "Supera horizonte"

for t, f in enumerate(flujos_caja):
    acumulado += f
    flujo_acumulado.append(acumulado)
    if acumulado >= 0 and payback_year == "Supera horizonte" and t > 0:
        anterior = flujo_acumulado[t - 1]
        fraccion = abs(anterior) / f
        payback_year = f"{t-1 + fraccion:.1f} Años"

co2_evitado_anual = mwh_ahorrados * factor_emision
co2_evitado_total = co2_evitado_anual * horizonte_anios

# 4. Encabezado de la Aplicación
st.markdown(
    f"""
    <div class="corp-header">
        <div class="corp-title">EcoMetric & ROI — Plataforma de Evaluación de Proyectos Sostenibles</div>
        <div class="corp-subtitle">Modelación Financiera Multidivisa, Análisis de Riesgos y Descarbonización ESG</div>
    </div>
""",
    unsafe_allow_html=True,
)

# 5. Pestañas Principales
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Dictamen Ejecutivo & Retorno",
        "⚙️ Guía del Panel Izquierdo",
        "📋 Estado de Flujos Proyectados",
        "📈 Sensibilidad & Escenarios",
        "🔬 Bases Científicas y Metodología",
    ]
)

# --- TAB 1: DICTAMEN EJECUTIVO ---
with tab1:
    st.markdown(
        "<h3 style='color: #ffffff;'>Indicadores Clave de Rentabilidad del Proyecto</h3>",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Retorno (Payback)</div>
                <div class="metric-value">{payback_year}</div>
                <div class="metric-description">Tiempo exacto para recuperar el 100% del capital inicial invertido (CAPEX).</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        color_vpn = "#10b981" if vpn >= 0 else "#f43f5e"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Valor Presente Neto (VPN)</div>
                <div class="metric-value" style="color: {color_vpn};">{divisa} {vpn:,.0f}</div>
                <div class="metric-description">Riqueza neta adicional generada hoy a la tasa de descuento exigida.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Tasa Interna (TIR)</div>
                <div class="metric-value">{tir*100:.2f}%</div>
                <div class="metric-description">Rendimiento porcentaje efectivo anual del capital invertido.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Flujo Neto Anual</div>
                <div class="metric-value">{divisa} {ahorro_neto_anual:,.0f}</div>
                <div class="metric-description">Ahorro operativo neto (Ahorro Bruto menos OPEX) por período.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='color: #ffffff;'>Curva de Recuperación de Capital</h3>",
        unsafe_allow_html=True,
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=anios,
            y=flujo_acumulado,
            mode="lines+markers",
            name="Flujo Acumulado",
            line=dict(color="#10b981", width=4),
            marker=dict(size=10, color="#38bdf8"),
        )
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="#ffffff",
        annotation_text="Punto de Retorno / Breakeven",
        annotation_position="bottom right",
        annotation_font_color="#ffffff",
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#101935",
        paper_bgcolor="#101935",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            title="Año de Operación",
            dtick=1,
            title_font=dict(color="#ffffff"),
            tickfont=dict(color="#ffffff"),
        ),
        yaxis=dict(
            title=f"Monto Acumulado en {divisa}",
            title_font=dict(color="#ffffff"),
            tickfont=dict(color="#ffffff"),
        ),
        height=420,
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f"""
        <div class="explain-box">
            <div class="explain-title">📌 Conclusión del Diagnóstico Financiero</div>
            <p>Para la ejecución de esta iniciativa se requiere una inversión inicial (CAPEX) de <b>{divisa} {capex:,.0f}</b>. 
            El proyecto genera un ahorro neto de <b>{divisa} {ahorro_neto_anual:,.0f}</b> cada año, obteniendo un 
            <b>Valor Presente Neto (VPN) de {divisa} {vpn:,.0f}</b> y una <b>Tasa Interna de Retorno (TIR) del {tir*100:.2f}%</b>.</p>
            <p>Al comparar la TIR con la tasa de descuento mínima requerida del <b>{tasa_descuento_pct}%</b>, el proyecto demuestra ser 
            <b>FINANCIERAMENTE VIABLE Y ALTAMENTE RENTABLE</b>, garantizando la recuperación de la inversión y generando valor económico real.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

# --- TAB 2: EXPLICACIÓN DE LA BARRA LATERAL ---
with tab2:
    st.markdown(
        "<h3 style='color: #ffffff;'>Explicación de las Variables del Panel Izquierdo</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color: #ffffff; font-size: 1rem;'>A continuación se detalla el significado contable y la fuente técnica de cada parámetro utilizado en el menú izquierdo:</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="explain-box">
            <div class="explain-title">🔹 1. Inversión Inicial (CAPEX - Capital Expenditures)</div>
            <p><b>¿De dónde sale?</b> Se obtiene de las cotizaciones comerciales de los proveedores de tecnología (paneles solares, inversores, maquinaria industrial eficiente) e incluye compra, transporte, licencias e instalación.</p>
            <p><b>¿Qué significa?</b> Es el desembolso de capital que debe realizarse en el "Año 0" para poner en marcha la infraestructura.</p>
        </div>

        <div class="explain-box">
            <div class="explain-title">🔹 2. Ahorro Energético Anual (Ahorro Bruto)</div>
            <p><b>¿De dónde sale?</b> Del análisis de las facturas históricas de energía eléctrica o combustibles de la empresa, multiplicado por el porcentaje de eficiencia proyectado.</p>
            <p><b>¿Qué significa?</b> Es la cantidad de dinero que la organización deja de pagar mes a mes a las comercializadoras de servicios públicos.</p>
        </div>

        <div class="explain-box">
            <div class="explain-title">🔹 3. Costos Operativos y Mantenimiento (OPEX - Operational Expenditures)</div>
            <p><b>¿De dónde sale?</b> De los contratos de mantenimiento preventivo, limpieza técnica, seguros contra todo riesgo y monitoreo del sistema.</p>
            <p><b>¿Qué significa?</b> Es el gasto anual recurrente necesario para mantener la tecnología operando en óptimas condiciones durante su vida útil.</p>
        </div>

        <div class="explain-box">
            <div class="explain-title">🔹 4. Tasa de Descuento / WACC (Weighted Average Cost of Capital)</div>
            <p><b>¿De dónde sale?</b> Es el costo promedio ponderado de capital exigido por la junta directiva o las entidades financieras para aprobar un proyecto.</p>
            <p><b>¿Qué significa?</b> Representa la rentabilidad mínima exigida a la inversión para cubrir el costo del dinero en el tiempo y la inflación.</p>
        </div>

        <div class="explain-box">
            <div class="explain-title">🔹 5. Energía Limpia Generada (MWh/año) y Factor de Emisión (tCO2e/MWh)</div>
            <p><b>¿De dónde sale?</b> La energía producida es estimada por el software de ingeniería (ej. PVSyst). El factor de emisión es tomado de las publicaciones oficiales del Ministerio de Minas y Energía o del sistema eléctrico nacional (XM/UPME).</p>
            <p><b>¿Qué significa?</b> Mide cuántos Megavatios-hora limpios se generan y cuántas toneladas de Dióxido de Carbono equivalente (tCO2e) se dejan de emitir a la atmósfera.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

# --- TAB 3: ESTADO DE FLUJOS ---
with tab3:
    st.markdown(
        "<h3 style='color: #ffffff;'>Estado Proyectado de Flujos de Caja</h3>",
        unsafe_allow_html=True,
    )

    datos_tabla = []
    for t in range(horizonte_anios + 1):
        f_bruto = 0 if t == 0 else ahorro_anual_base
        f_opex = 0 if t == 0 else opex_anual
        f_neto = -capex if t == 0 else ahorro_neto_anual
        f_desc = f_neto / ((1 + tasa_descuento) ** t)

        datos_tabla.append(
            {
                "Año": f"Año {t}",
                f"Ahorro Bruto ({divisa})": f"{f_bruto:,.0f}",
                f"OPEX ({divisa})": f"{f_opex:,.0f}",
                f"Flujo Neto ({divisa})": f"{f_neto:,.0f}",
                f"Flujo Descontado ({divisa})": f"{f_desc:,.0f}",
                f"Acumulado ({divisa})": f"{flujo_acumulado[t]:,.0f}",
            }
        )

    df_flujos = pd.DataFrame(datos_tabla)
    st.dataframe(df_flujos, use_container_width=True)

# --- TAB 4: SENSIBILIDAD ---
with tab4:
    st.markdown(
        "<h3 style='color: #ffffff;'>Análisis de Sensibilidad y Escenarios de Riesgo</h3>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color: #ffffff; font-size: 1rem;'>Esta tabla evalúa cómo cambia el Valor Presente Neto (VPN) si los ahorros reales aumentan o disminuyen respecto al escenario base proyectado:</p>",
        unsafe_allow_html=True,
    )

    variaciones = [-0.20, -0.10, 0.0, 0.10, 0.20]
    matriz_escenarios = []

    for v in variaciones:
        ahorro_mod = ahorro_neto_anual * (1 + v)
        flujos_mod = [-capex] + [ahorro_mod] * horizonte_anios
        vpn_mod = sum(
            [f / ((1 + tasa_descuento) ** t) for t, f in enumerate(flujos_mod)]
        )

        nombre_esc = f"Ahorros {v*100:+.0f}%"
        if v == 0:
            nombre_esc = "Escenario Base (Proyectado)"

        matriz_escenarios.append(
            {
                "Escenario de Mercado": nombre_esc,
                f"Flujo Neto Anual ({divisa})": f"{ahorro_mod:,.0f}",
                f"VPN Resultado ({divisa})": f"{vpn_mod:,.0f}",
                "Estado de Viabilidad": "✅ VIABLE"
                if vpn_mod >= 0
                else "❌ NO VIABLE",
            }
        )

    df_sens = pd.DataFrame(matriz_escenarios)
    st.table(df_sens)

# --- TAB 5: BASES CIENTÍFICAS Y METODOLOGÍA ---
with tab5:
    st.markdown(
        "<h3 style='color: #ffffff;'>Rigor Científico, Normativa y Metodología Internacional</h3>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="explain-box">
            <div class="explain-title">🔬 1. Fundamento Financiero: Metodología de Flujos de Caja Descontados (DCF)</div>
            <p>Las proyecciones financieras de esta plataforma aplican el modelo cuantitativo de <b>Flujos de Caja Descontados (Discounted Cash Flow - DCF)</b>, pilar fundamental de las finanzas corporativas globales normado por las <b>NIIF / IFRS (Normas Internacionales de Información Financiera - NIC 36)</b>.</p>
            <p>El algoritmo descuenta matemáticamente cada flujo futuro aplicando la tasa de actualización WACC mediante la fórmula estandarizada:</p>
            <p style="font-family: monospace; color: #38bdf8; font-size: 1.1rem; font-weight: bold;">VPN = ∑ [ Flujo_t / (1 + WACC)^t ] - CAPEX</p>
        </div>

        <div class="explain-box">
            <div class="explain-title">🌱 2. Fundamento Ambiental: Protocolo GHG e ISO 14064</div>
            <p>La cuantificación del impacto ecológico (toneladas de CO2 evadidas) aplica estrictamente la metodología del <b>GHG Protocol (Greenhouse Gas Protocol)</b> desarrollado por el WRI (World Resources Institute) y el WBCSD, así como la norma <b>ISO 14064</b> para la cuantificación y reporte de emisiones de gases de efecto invernadero.</p>
        </div>

        <div class="explain-box">
            <div class="explain-title">📊 3. Validez de los Factores de Conversión</div>
            <p>El factor de emisión por Megavatio-hora (MWh) utiliza los datos emitidos por el <b>IPCC (Panel Intergubernamental sobre el Cambio Climático)</b> y los entes reguladores de la matriz energética en América Latina (ej. XM / UPME en Colombia), garantizando que los indicadores de descarbonización sean técnicamente verificables para auditorías ESG.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
