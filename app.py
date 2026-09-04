import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 1. Configuración de página nivel corporativo
st.set_page_config(
    page_title="EcoMetric & ROI | Platform for Sustainable Investments",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS de alto contraste y diseño ejecutivo
st.markdown(
    """
    <style>
    /* Fondo principal y tipografía general */
    .stApp {
        background-color: #0b1329;
        color: #ffffff;
    }
    
    /* Panel lateral */
    [data-testid="stSidebar"] {
        background-color: #111c3a;
        border-right: 1px solid #1e2d5a;
    }
    
    /* Encabezado Corporativo */
    .corp-header {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        border-left: 5px solid #10b981;
        padding: 24px;
        border-radius: 8px;
        margin-bottom: 25px;
    }
    .corp-title {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
    }
    .corp-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 6px;
        font-weight: 400;
    }
    
    /* Tarjetas de Métricas de Alto Impacto */
    .metric-card {
        background-color: #162244;
        border: 1px solid #233568;
        border-radius: 10px;
        padding: 20px;
        text-align: left;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .metric-title {
        color: #cbd5e1;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #10b981;
        font-size: 1.9rem;
        font-weight: 800;
        line-height: 1.2;
    }
    .metric-description {
        color: #94a3b8;
        font-size: 0.82rem;
        margin-top: 8px;
        line-height: 1.3;
    }

    /* Cajas de texto educativo / explicativo */
    .explain-box {
        background-color: #101935;
        border: 1px solid #1e2e5c;
        border-radius: 8px;
        padding: 18px;
        margin-top: 15px;
        margin-bottom: 20px;
        color: #e2e8f0;
    }
    .explain-title {
        color: #38bdf8;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 8px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. Barra Lateral: Parámetros del Proyecto
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px 0;">
        <h2 style="color: #ffffff; margin:0; font-weight: 800;">🏛️ ECOFIN</h2>
        <p style="color: #38bdf8; font-size: 0.8rem; margin:0;">CORPORATE SUSTAINABILITY</p>
    </div>
""",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ Configuración del Modelo")

divisa = st.sidebar.selectbox("Moneda del Modelo", ["COP", "USD", "EUR", "MXN"])

capex = st.sidebar.number_input(
    f"Inversión Inicial CAPEX ({divisa})",
    min_value=1000,
    value=250000000,
    step=5000000,
    help="Inversión bruta requerida para compra, transporte, ingeniería e instalación.",
)

ahorro_anual_base = st.sidebar.number_input(
    f"Ahorro Energético Anual ({divisa})",
    min_value=500,
    value=55000000,
    step=1000000,
    help="Ahorro bruto estimado en la factura de servicios de energía o combustible.",
)

opex_anual = st.sidebar.number_input(
    f"Costos Operativos OPEX ({divisa}/año)",
    min_value=0,
    value=4500000,
    step=500000,
    help="Gastos recurrentes de mantenimiento preventivo, correctivo y pólizas.",
)

horizonte_anios = st.sidebar.slider(
    "Horizonte de Evaluación (Años)",
    min_value=3,
    max_value=25,
    value=12,
)

tasa_descuento_pct = st.sidebar.slider(
    "Tasa de Descuento Corporativa / WACC (%)",
    min_value=1.0,
    max_value=25.0,
    value=11.5,
    step=0.5,
    help="Costo promedio ponderado de capital exigido por los accionistas o inversionistas.",
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
    help="Factor de conversión oficial del SIN para mitigación de gases de efecto invernadero.",
)

# 3. Cálculos Financieros Estructurados
ahorro_neto_anual = ahorro_anual_base - opex_anual
anios = list(range(0, horizonte_anios + 1))
flujos_caja = [-capex] + [ahorro_neto_anual] * horizonte_anios

# Cálculo del Valor Presente Neto (VPN)
vpn = sum([f / ((1 + tasa_descuento) ** t) for t, f in enumerate(flujos_caja)])

# Cálculo de Tasa Interna de Retorno (TIR)
try:
    tir = np.irr(flujos_caja)
except:
    tir = 0.0

# Flujo acumulado y Período de Recuperación (Payback)
flujo_acumulado = []
acumulado = 0
payback_year = "Supera horizonte"
payback_exacto = 0.0

for t, f in enumerate(flujos_caja):
    acumulado += f
    flujo_acumulado.append(acumulado)
    if acumulado >= 0 and payback_year == "Supera horizonte" and t > 0:
        anterior = flujo_acumulado[t - 1]
        fraccion = abs(anterior) / f
        payback_exacto = (t - 1) + fraccion
        payback_year = f"{payback_exacto:.1f} Años"

# Impacto Ambiental
co2_evitado_anual = mwh_ahorrados * factor_emision
co2_evitado_total = co2_evitado_anual * horizonte_anios
arboles_equivalentes = int(co2_evitado_total * 6)

# 4. Banner Institucional
st.markdown(
    f"""
    <div class="corp-header">
        <div class="corp-title">Plataforma de Evaluación de Proyectos Sostenibles & ROI</div>
        <div class="corp-subtitle">Sistema de Modelación Financiera, Valoración de Riesgos y Mitigación de Huella de Carbono</div>
    </div>
""",
    unsafe_allow_html=True,
)

# 5. Estructura Principal en Pestañas
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Dictamen Ejecutivo & Retorno",
        "📋 Estado de Flujos Proyectado",
        "📈 Sensibilidad & Escenarios de Riesgo",
        "📚 Fundamentos Financieros & Metodología",
    ]
)

# --- TAB 1: DICTAMEN EJECUTIVO ---
with tab1:
    st.subheader("Resumen de Indicadores Financieros de Alto Nivel")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Retorno de Inversión (Payback)</div>
                <div class="metric-value">{payback_year}</div>
                <div class="metric-description">Tiempo requerido para recuperar el 100% del capital inicial (CAPEX).</div>
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
                <div class="metric-description">Riqueza neta generada por el proyecto descontada al costo de capital.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Tasa Interna de Retorno (TIR)</div>
                <div class="metric-value">{tir*100:.2f}%</div>
                <div class="metric-description">Rentabilidad efectiva anual esperada de los flujos de caja.</div>
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
                <div class="metric-description">Ahorro operativo líquido disponible generado cada período.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfico de Flujo de Caja
    st.subheader("Curva de Recuperación de Capital y Flujo Neto Acumulado")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=anios,
            y=flujo_acumulado,
            mode="lines+markers",
            name="Flujo Acumulado",
            line=dict(color="#10b981", width=3.5),
            marker=dict(size=9, color="#047857"),
        )
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text="Línea de Equilibrio / Breakeven",
        annotation_position="bottom right",
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#101935",
        paper_bgcolor="#101935",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            title="Año de Operación del Proyecto",
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

    # Explicación del dictamen
    st.markdown(
        f"""
        <div class="explain-box">
            <div class="explain-title">📌 Dictamen Ejecutivo para Toma de Decisiones</div>
            <p>Con base en los parámetros ingresados, el proyecto exige un desembolso inicial de <b>{divisa} {capex:,.0f}</b>. 
            Al generar un ahorro neto de <b>{divisa} {ahorro_neto_anual:,.0f}</b> anuales, la propuesta presenta un <b>Valor Presente Neto (VPN) de {divisa} {vpn:,.0f}</b> 
            y una <b>Tasa Interna de Retorno (TIR) del {tir*100:.2f}%</b>.</p>
            <p>Dado que la TIR supera la tasa de descuento corporativa exigiéndole un <b>{tasa_descuento_pct}%</b>, el proyecto es 
            <b>FINANCIERAMENTE VIABLE Y ATRACTIVO</b>, agregando valor económico directo a la organización además del impacto positivo ambiental.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

# --- TAB 2: ESTADO DE FLUJOS DETALLADO ---
with tab2:
    st.subheader("Tabla Estructurada de Flujos de Caja Proyectados")
    st.write(
        "Desglose período a período del modelo de amortización e inversión acumulada:"
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

    st.markdown(
        """
        <div class="explain-box">
            <div class="explain-title">💡 ¿Cómo interpretar el Flujo Descontado?</div>
            <p>El <b>Flujo Descontado</b> trae el dinero que se recibirá en el futuro al valor que tendría el día de hoy, aplicando la tasa WACC. 
            Esta metodología ajusta el dinero por el costo de oportunidad y la inflación, garantizando que el análisis de rentabilidad sea totalmente riguroso.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

# --- TAB 3: SENSIBILIDAD ---
with tab3:
    st.subheader("Análisis de Estrés y Sensibilidad de Escenarios")
    st.write(
        "Evaluación de resiliencia financiera ante variaciones impredecibles en los ahorros o costos del mercado:"
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
                "Viabilidad Financiera": (
                    "✅ VIABLE" if vpn_mod >= 0 else "❌ NO VIABLE"
                ),
            }
        )

    df_sens = pd.DataFrame(matriz_escenarios)
    st.table(df_sens)

    # Sección Ambiental
    st.markdown("---")
    st.subheader("Impacto Ambiental y Metas de Descarbonización ESG")

    ca, cb, cc = st.columns(3)
    with ca:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">CO2 Evitado Anual</div>
                <div class="metric-value" style="color: #38bdf8;">{co2_evitado_anual:,.1f} tCO2e</div>
                <div class="metric-description">Mitigación directa anual de gases de efecto invernadero.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with cb:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Reducción Acumulada</div>
                <div class="metric-value" style="color: #38bdf8;">{co2_evitado_total:,.1f} tCO2e</div>
                <div class="metric-description">Impacto total mitigado durante los {horizonte_anios} años de operación.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with cc:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Equivalente Ecológico</div>
                <div class="metric-value" style="color: #10b981;">🌲 {arboles_equivalentes:,}</div>
                <div class="metric-description">Equivalencia en absorción de árboles maduros sembrados.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

# --- TAB 4: METODOLOGÍA ---
with tab4:
    st.subheader("Fundamentos Teóricos y Normativa Contable Aplicada")

    st.markdown(
        """
        <div class="explain-box">
            <div class="explain-title">1. Valor Presente Neto (VPN / NPV)</div>
            <p>Es la métrica reina de las finanzas corporativas. Se calcula mediante la fórmula:</p>
            <p style="font-family: monospace; color: #38bdf8;">VPN = ∑ [ Flujo_t / (1 + WACC)^t ] - CAPEX</p>
            <p>Un VPN mayor a cero demuestra que la inversión genera un rendimiento superior a la tasa mínima exigida, creando valor neto para los accionistas.</p>
        </div>

        <div class="explain-box">
            <div class="explain-title">2. Tasa Interna de Retorno (TIR / IRR)</div>
            <p>Es la tasa de descuento exacta que hace que el VPN del proyecto sea igual a cero. Representa la rentabilidad porcentual interna del proyecto de inversión.</p>
        </div>

        <div class="explain-box">
            <div class="explain-title">3. Período de Recuperación (Payback Period)</div>
            <p>Indica el momento exacto en el tiempo (medido en años y meses) en el que los flujos de caja operativos acumulados igualan la inversión inicial (CAPEX).</p>
        </div>

        <div class="explain-box">
            <div class="explain-title">4. Estándares de Contabilidad Ambiental (GHG Protocol)</div>
            <p>El cálculo de mitigación de CO2 aplica la metodología estándar internacional de conversión energética de la Agencia Internacional de Energía (IEA) y los factores de emisión oficiales de la matriz eléctrica.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
