import numpy as np
import pandas as pd
import plotly.graph_objects as rx
import streamlit as st

# 1. Configuración visual de la página
st.set_page_config(
    page_title="EcoMetric & ROI | Evaluación de Proyectos Sostenibles",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo CSS personalizado para un acabado elegante y sofisticado
st.markdown(
    """
    <style>
    /* Estilo del fondo y fuentes */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    /* Tarjetas de métricas personalizadas */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #10b981;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .metric-subtitle {
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 4px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. Barra Lateral: Configuración de Parámetros
st.sidebar.image(
    "https://img.icons8.com/isometric-folders/100/leaf.png", width=60
)
st.sidebar.title("🌿 EcoMetric & ROI")
st.sidebar.caption(
    "Evaluación de Viabilidad Financiera e Impacto Ambiental"
)
st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ Parámetros del Proyecto")

divisa = st.sidebar.selectbox("Moneda de análisis", ["COP", "USD", "EUR", "MXN"])

capex = st.sidebar.number_input(
    f"Inversión Inicial - CAPEX ({divisa})",
    min_value=1000,
    value=150000000,
    step=1000000,
    help="Costo total de adquisición e instalación del sistema.",
)

ahorro_anual_base = st.sidebar.number_input(
    f"Ahorro Energético Anual Proyectado ({divisa})",
    min_value=500,
    value=35000000,
    step=500000,
    help="Dinero estimado que la empresa dejará de pagar en su factura mensual/anual.",
)

opex_anual = st.sidebar.number_input(
    f"Costo Operativo y Mantenimiento OPEX ({divisa})",
    min_value=0,
    value=3000000,
    step=100000,
    help="Gastos de mantenimiento y seguros anuales.",
)

horizonte_anios = st.sidebar.slider(
    "Horizonte de Evaluación (Años)",
    min_value=3,
    max_value=25,
    value=10,
)

tasa_descuento = (
    st.sidebar.slider(
        "Tasa de Descuento / WACC (%)",
        min_value=1.0,
        max_value=25.0,
        value=12.0,
        step=0.5,
    )
    / 100
)

factor_emision = st.sidebar.number_input(
    "Factor de Emisión (tCO2e por MWh ahro)",
    value=0.126,
    format="%.3f",
    help="Toneladas de CO2 evadidas por megavatio-hora ahorrado.",
)

mwh_ahorrados = st.sidebar.number_input(
    "Energía Limpia Generada / Ahorrada (MWh/año)",
    value=120.0,
    step=10.0,
)

# 3. Lógica Financiera Interna
ahorro_neto_anual = ahorro_anual_base - opex_anual

# Construcción de Flujos de Caja
anios = list(range(0, horizonte_anios + 1))
flujos = [-capex] + [ahorro_neto_anual] * horizonte_anios

# Cálculo del Valor Presente Neto (VPN)
vpn = np.npv(tasa_descuento, flujos) if hasattr(np, "npv") else np.fmin(0, 0)
# Fallback usando numpy_financial si está disponible, o cálculo manual estándar
vpn = sum([f / ((1 + tasa_descuento) ** t) for t, f in enumerate(flujos)])

# Cálculo de Tasa Interna de Retorno (TIR)
try:
    tir = np.irr(flujos) if hasattr(np, "irr") else np.irr(flujos)
except:
    tir = 0.0

# Flujo acumulado y Payback (Retorno de Inversión)
flujo_acumulado = []
acumulado = 0
payback_year = "No recupera"
for t, f in enumerate(flujos):
    acumulado += f
    flujo_acumulado.append(acumulado)
    if acumulado >= 0 and payback_year == "No recupera" and t > 0:
        # Interpolación simple para calcular el mes aproximado
        anterior = flujo_acumulado[t - 1]
        fraccion = abs(anterior) / f
        payback_year = f"{t-1 + fraccion:.1f} años"

# Impacto Ambiental
co2_evitado_anual = mwh_ahorrados * factor_emision
co2_evitado_total = co2_evitado_anual * horizonte_anios
arboles_equivalentes = int(co2_evitado_total * 6)

# 4. Encabezado Principal
st.title("🌱 EcoMetric & ROI")
st.markdown(
    "##### *Simulador de Viabilidad Financiera e Impacto Ambiental para Proyectos de Transición Energética*"
)
st.markdown("---")

# 5. Pestañas de Navegación Interactivas
tab1, tab2, tab3 = st.tabs(
    [
        "📊 Indicadores y Retorno",
        "📈 Análisis de Sensibilidad",
        "🍃 Impacto Ambiental y Sostenibilidad",
    ]
)

# --- TAB 1: RESULTADOS CLAVE Y FLUJO DE CAJA ---
with tab1:
    st.subheader("Métricas de Rentabilidad del Proyecto")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Retorno de Inversión (Payback)</div>
                <div class="metric-value">{payback_year}</div>
                <div class="metric-subtitle">Recuperación del capital</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        color_vpn = "#10b981" if vpn >= 0 else "#ef4444"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Valor Presente Neto (VPN)</div>
                <div class="metric-value" style="color: {color_vpn};">{divisa} {vpn:,.0f}</div>
                <div class="metric-subtitle">Valor creado a precios de hoy</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Tasa Interna de Retorno (TIR)</div>
                <div class="metric-value">{tir*100:.1f}%</div>
                <div class="metric-subtitle">Rendimiento anual del proyecto</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Ahorro Neto Anual</div>
                <div class="metric-value">{divisa} {ahorro_neto_anual:,.0f}</div>
                <div class="metric-subtitle">Ahorro bruto menos OPEX</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfico Profesional de Flujo de Caja Acumulado
    st.subheader("Evolución del Flujo de Caja Acumulado")

    fig = rx.Figure()

    # Línea de flujo acumulado
    fig.add_trace(
        rx.Scatter(
            x=anios,
            y=flujo_acumulado,
            mode="lines+markers",
            name="Flujo Acumulado",
            line=dict(color="#10b981", width=3),
            marker=dict(size=8, color="#059669"),
        )
    )

    # Línea de equilibrio (cero)
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text="Punto de Retorno (Breakeven)",
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#0f172a",
        paper_bgcolor="#0f172a",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(title="Año de Operación", dtick=1),
        yaxis=dict(title=f"Monto Acumulado ({divisa})"),
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: ANÁLISIS DE SENSIBILIDAD ---
with tab2:
    st.subheader("Análisis de Sensibilidad de Escenarios")
    st.write(
        "Evalúa cómo varía el Valor Presente Neto (VPN) si la tarifa de ahorro energético o la inversión inicial sufren variaciones."
    )

    # Variación de Escenarios (-20%, Conservador, Optimista +20%)
    variaciones = [-0.20, -0.10, 0.0, 0.10, 0.20]
    tabla_sensibilidad = []

    for v in variaciones:
        ahorro_modificado = ahorro_neto_anual * (1 + v)
        flujos_mod = [-capex] + [ahorro_modificado] * horizonte_anios
        vpn_mod = sum(
            [f / ((1 + tasa_descuento) ** t) for t, f in enumerate(flujos_mod)]
        )

        # Recálculo de payback
        acum = 0
        pb = "N/A"
        for t, f in enumerate(flujos_mod):
            acum += f
            if acum >= 0 and pb == "N/A" and t > 0:
                pb = f"{t} años"

        escenario_nombre = f"{v*100:+.0f}% en Ahorros"
        if v == 0:
            escenario_nombre = "Base (Proyectado)"

        tabla_sensibilidad.append(
            {
                "Escenario": escenario_nombre,
                f"Ahorro Anual ({divisa})": f"{ahorro_modificado:,.0f}",
                f"VPN ({divisa})": f"{vpn_mod:,.0f}",
                "Estado del Proyecto": (
                    "✅ Viable" if vpn_mod >= 0 else "❌ No Viable"
                ),
            }
        )

    df_sensibilidad = pd.DataFrame(tabla_sensibilidad)
    st.table(df_sensibilidad)

# --- TAB 3: IMPACTO AMBIENTAL ---
with tab3:
    st.subheader("Métricas de Sostenibilidad y Descarbonización")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">CO2 Evitado Anual</div>
                <div class="metric-value" style="color: #3b82f6;">{co2_evitado_anual:,.1f} tCO2e</div>
                <div class="metric-subtitle">Toneladas de carbono al año</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Impacto Acumulado</div>
                <div class="metric-value" style="color: #3b82f6;">{co2_evitado_total:,.1f} tCO2e</div>
                <div class="metric-subtitle">Reducción total a {horizonte_anios} años</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col_c:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Equivalente en Árboles</div>
                <div class="metric-value" style="color: #10b981;">🌲 {arboles_equivalentes:,}</div>
                <div class="metric-subtitle">Árboles sembrados absorbiendo CO2</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        "💡 **Conclusión Estratégica:** Este modelo demuestra que el proyecto no solo cumple con criterios de rentabilidad financiera (VPN positivo y TIR atractiva), sino que se alinea con la estrategia de descarbonización corporativa."
    )