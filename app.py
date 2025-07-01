import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from revenue_model import (
    VehicleTCORevenueModel,
    VehicleParams,
    PartnershipParams,
    MarketParams,
    UserGrowthParams
)
import numpy as np
from datetime import datetime
import base64
import traceback

# Page configuration
st.set_page_config(
    page_title="Vehicle TCO Revenue Model",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .kpi-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
    }
    .kpi-card h3 {
        font-size: 0.9rem;
        margin: 0 0 0.5rem 0;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-card .value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .kpi-card .change {
        font-size: 0.8rem;
        opacity: 0.8;
    }
    .scenario-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .scenario-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .export-section {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        .kpi-card .value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Scenario presets
def get_scenario_presets():
    return {
        "Conservative": {
            "vehicle_type": "Hybrid",
            "base_price": 35000,
            "annual_mileage": 12000,
            "ownership_years": 5,
            "partnership_tier": "Basic",
            "partner_count": 5,
            "fuel_price": 3.00,
            "electricity_rate": 0.10,
            "inflation_rate": 2.0
        },
        "Balanced": {
            "vehicle_type": "Electric Vehicle",
            "base_price": 45000,
            "annual_mileage": 15000,
            "ownership_years": 5,
            "partnership_tier": "Premium",
            "partner_count": 10,
            "fuel_price": 3.50,
            "electricity_rate": 0.12,
            "inflation_rate": 2.5
        },
        "Aggressive": {
            "vehicle_type": "Electric Vehicle",
            "base_price": 60000,
            "annual_mileage": 20000,
            "ownership_years": 7,
            "partnership_tier": "Enterprise",
            "partner_count": 20,
            "fuel_price": 4.00,
            "electricity_rate": 0.15,
            "inflation_rate": 3.0
        },
        "Enterprise": {
            "vehicle_type": "Electric Vehicle",
            "base_price": 80000,
            "annual_mileage": 25000,
            "ownership_years": 8,
            "partnership_tier": "Enterprise",
            "partner_count": 30,
            "fuel_price": 4.50,
            "electricity_rate": 0.18,
            "inflation_rate": 3.5
        }
    }

# Error handling decorator
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if st.checkbox("Show error details"):
                st.code(traceback.format_exc())
            return None
    return wrapper

@handle_errors
def initialize_model(params):
    vehicle = VehicleParams(
        vehicle_type=params['vehicle_type'],
        base_price=params['base_price'],
        annual_mileage=params['annual_mileage'],
        ownership_years=params['ownership_years']
    )
    partnership = PartnershipParams(
        partnership_tier=params['partnership_tier'],
        partner_count=params['partner_count']
    )
    market = MarketParams(
        fuel_price=params['fuel_price'],
        electricity_rate=params['electricity_rate'],
        inflation_rate=params['inflation_rate']
    )
    user_growth = UserGrowthParams()
    return VehicleTCORevenueModel(
        vehicle=vehicle,
        partnership=partnership,
        market=market,
        user_growth=user_growth
    )

@handle_errors
def calculate_metrics(model):
    tco_data = model.calculate_tco()
    revenue_data = model.calculate_revenue_streams()
    break_even = model.break_even_analysis()
    recommendations = model.generate_recommendations()
    return {
        'tco': tco_data,
        'revenue': revenue_data,
        'break_even': break_even,
        'recommendations': recommendations
    }

def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>🚗 Vehicle TCO Revenue Model</h1>
        <p>Comprehensive Total Cost of Ownership Analysis with Partnership Revenue Projections</p>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_cards(metrics):
    tco_data = metrics['tco']
    revenue_data = metrics['revenue']
    net_profit = revenue_data['total_revenue'] - tco_data['total_tco']
    roi = (net_profit / tco_data['total_tco']) * 100 if tco_data['total_tco'] > 0 else 0
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Total Cost of Ownership</h3>
            <div class="value">${tco_data['total_tco']:,.0f}</div>
            <div class="change">${tco_data['tco_per_mile']:.2f}/mile</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Total Revenue</h3>
            <div class="value">${revenue_data['total_revenue']:,.0f}</div>
            <div class="change">{revenue_data['revenue_growth']:.1f}% YoY Growth</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Net Profit</h3>
            <div class="value">${net_profit:,.0f}</div>
            <div class="change">{net_profit/tco_data['total_tco']*100:.1f}% Margin</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Return on Investment</h3>
            <div class="value">{roi:.1f}%</div>
            <div class="change">${net_profit:,.0f} Profit</div>
        </div>
        """, unsafe_allow_html=True)

def render_scenario_presets():
    st.sidebar.markdown("### 🎯 Scenario Presets")
    presets = get_scenario_presets()
    for scenario_name, preset_params in presets.items():
        if st.sidebar.button(f"📊 {scenario_name}", key=f"preset_{scenario_name}"):
            st.session_state.update(preset_params)
            st.success(f"✅ Applied {scenario_name} scenario!")
            st.rerun()

def render_sidebar_controls():
    st.sidebar.markdown("### 🚗 Vehicle Configuration")
    vehicle_type = st.sidebar.selectbox(
        "Vehicle Type",
        ["Electric Vehicle", "Hybrid", "Gasoline", "Diesel"],
        index=0,
        key="vehicle_type"
    )
    base_price = st.sidebar.number_input(
        "Base Vehicle Price ($)",
        min_value=20000,
        max_value=150000,
        value=45000,
        step=1000,
        key="base_price"
    )
    annual_mileage = st.sidebar.number_input(
        "Annual Mileage",
        min_value=5000,
        max_value=50000,
        value=15000,
        step=1000,
        key="annual_mileage"
    )
    ownership_years = st.sidebar.slider(
        "Ownership Period (Years)",
        min_value=1,
        max_value=15,
        value=5,
        key="ownership_years"
    )
    st.sidebar.markdown("### 🤝 Partnership Revenue")
    partnership_tier = st.sidebar.selectbox(
        "Partnership Tier",
        ["Basic", "Premium", "Enterprise"],
        index=1,
        key="partnership_tier"
    )
    partner_count = st.sidebar.number_input(
        "Number of Partners",
        min_value=1,
        max_value=100,
        value=10,
        step=1,
        key="partner_count"
    )
    st.sidebar.markdown("### 📈 Market Conditions")
    fuel_price = st.sidebar.number_input(
        "Fuel Price ($/gallon)",
        min_value=1.0,
        max_value=10.0,
        value=3.50,
        step=0.1,
        key="fuel_price"
    )
    electricity_rate = st.sidebar.number_input(
        "Electricity Rate ($/kWh)",
        min_value=0.05,
        max_value=0.50,
        value=0.12,
        step=0.01,
        key="electricity_rate"
    )
    inflation_rate = st.sidebar.slider(
        "Annual Inflation Rate (%)",
        min_value=0.0,
        max_value=15.0,
        value=2.5,
        step=0.1,
        key="inflation_rate"
    )

def render_charts(metrics):
    tco_data = metrics['tco']
    revenue_data = metrics['revenue']
    st.markdown("### 📊 Cost & Revenue Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 💰 TCO Breakdown")
        fig_pie = px.pie(
            values=list(tco_data['breakdown'].values()),
            names=list(tco_data['breakdown'].keys()),
            title="Total Cost of Ownership Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12
        )
        fig_pie.update_layout(
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.markdown("#### 📈 Revenue Growth Projection")
        years = list(range(1, len(revenue_data['annual_revenue']) + 1))
        fig_line = px.line(
            x=years,
            y=revenue_data['annual_revenue'],
            title="Annual Revenue Growth",
            labels={'x': 'Year', 'y': 'Revenue ($)'},
            markers=True
        )
        fig_line.update_traces(
            line_color='#667eea',
            marker_color='#667eea',
            line_width=3,
            marker_size=8
        )
        fig_line.update_layout(
            height=400,
            xaxis=dict(tickmode='linear', tick0=1, dtick=1),
            yaxis=dict(tickformat=',.0f')
        )
        st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("### 💼 Revenue Streams Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📊 Revenue Streams Breakdown")
        revenue_streams = {
            'Service Providers': revenue_data['service_providers'],
            'Insurance Partners': revenue_data['insurance_partners'],
            'Parts Retailers': revenue_data['parts_retailers'],
            'Fuel Partners': revenue_data['fuel_partners'],
            'Financial Services': revenue_data['financial_services'],
            'Data Providers': revenue_data['data_providers'],
            'Enterprise Solutions': revenue_data['enterprise_solutions'],
            'Partnership Fees': revenue_data['partnership_fees'],
            'User SaaS': revenue_data['user_saas']
        }
        fig_revenue = px.bar(
            x=list(revenue_streams.keys()),
            y=list(revenue_streams.values()),
            title="Annual Revenue by Stream",
            color=list(revenue_streams.values()),
            color_continuous_scale='viridis'
        )
        fig_revenue.update_layout(
            height=400,
            xaxis_title="Revenue Stream",
            yaxis_title="Annual Revenue ($)",
            yaxis=dict(tickformat=',.0f')
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    with col2:
        st.markdown("#### 📋 Annual Cost Breakdown")
        annual_data = pd.DataFrame({
            'Year': range(1, len(tco_data['annual_breakdown']['depreciation']) + 1),
            'Depreciation': tco_data['annual_breakdown']['depreciation'],
            'Fuel/Electricity': tco_data['annual_breakdown']['fuel_electricity'],
            'Maintenance': tco_data['annual_breakdown']['maintenance'],
            'Insurance': tco_data['annual_breakdown']['insurance'],
            'Registration': tco_data['annual_breakdown']['registration']
        })
        fig_stack = px.bar(
            annual_data,
            x='Year',
            y=['Depreciation', 'Fuel/Electricity', 'Maintenance', 'Insurance', 'Registration'],
            title="Annual Cost Breakdown",
            barmode='stack'
        )
        fig_stack.update_layout(
            height=400,
            xaxis_title="Year",
            yaxis_title="Cost ($)",
            yaxis=dict(tickformat=',.0f')
        )
        st.plotly_chart(fig_stack, use_container_width=True)

def render_sensitivity_analysis(model_params):
    st.markdown("### 🔍 Sensitivity Analysis")
    sensitivity_params = {
        'Annual Mileage': [10000, 15000, 20000, 25000, 30000],
        'Fuel Price': [2.0, 3.0, 4.0, 5.0, 6.0],
        'Partner Count': [5, 10, 15, 20, 25]
    }
    sensitivity_results = {}
    with st.spinner("Calculating sensitivity analysis..."):
        for param, values in sensitivity_params.items():
            results = []
            for value in values:
                temp_params = model_params.copy()
                if param == 'Annual Mileage':
                    temp_params['annual_mileage'] = value
                elif param == 'Fuel Price':
                    temp_params['fuel_price'] = value
                elif param == 'Partner Count':
                    temp_params['partner_count'] = value
                try:
                    temp_model = VehicleTCORevenueModel(**temp_params)
                    temp_tco = temp_model.calculate_tco()
                    temp_revenue = temp_model.calculate_revenue_streams()
                    results.append(temp_revenue['total_revenue'] - temp_tco['total_tco'])
                except:
                    results.append(0)
            sensitivity_results[param] = results
    fig_sensitivity = go.Figure()
    colors = ['#667eea', '#764ba2', '#f093fb']
    for i, (param, results) in enumerate(sensitivity_results.items()):
        fig_sensitivity.add_trace(go.Scatter(
            x=sensitivity_params[param],
            y=results,
            mode='lines+markers',
            name=param,
            line=dict(width=3, color=colors[i]),
            marker=dict(size=8)
        ))
    fig_sensitivity.update_layout(
        title="Net Profit Sensitivity Analysis",
        xaxis_title="Parameter Value",
        yaxis_title="Net Profit ($)",
        height=500,
        hovermode='x unified',
        yaxis=dict(tickformat=',.0f')
    )
    st.plotly_chart(fig_sensitivity, use_container_width=True)

def render_recommendations(metrics):
    st.markdown("### 💡 Strategic Recommendations")
    recommendations = metrics['recommendations']
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>🎯 Recommendation {i}:</strong> {rec}
        </div>
        """, unsafe_allow_html=True)

def render_export_section(metrics, model_params):
    st.markdown("### 📤 Export Results")
    st.markdown("""
    <div class="export-section">
        <h3>📊 Export Your Analysis</h3>
        <p>Download comprehensive reports and data for further analysis</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 Export Summary Report", use_container_width=True):
            summary_data = {
                'Metric': [
                    'Vehicle Type', 'Base Price', 'Annual Mileage', 'Ownership Years',
                    'Partnership Tier', 'Partner Count', 'Total TCO', 'Total Revenue',
                    'Net Profit', 'ROI', 'Break-even Months'
                ],
                'Value': [
                    model_params['vehicle_type'],
                    f"${model_params['base_price']:,.0f}",
                    f"{model_params['annual_mileage']:,}",
                    model_params['ownership_years'],
                    model_params['partnership_tier'],
                    model_params['partner_count'],
                    f"${metrics['tco']['total_tco']:,.0f}",
                    f"${metrics['revenue']['total_revenue']:,.0f}",
                    f"${metrics['revenue']['total_revenue'] - metrics['tco']['total_tco']:,.0f}",
                    f"{(metrics['revenue']['total_revenue'] - metrics['tco']['total_tco']) / metrics['tco']['total_tco'] * 100:.1f}%",
                    f"{metrics['break_even']['break_even_months']:.1f}"
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            csv = summary_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Summary CSV",
                data=csv,
                file_name=f"vehicle_tco_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    with col2:
        if st.button("📊 Export Detailed Data", use_container_width=True):
            years = range(1, model_params['ownership_years'] + 1)
            detailed_data = {
                'Year': years,
                'Depreciation': metrics['tco']['annual_breakdown']['depreciation'],
                'Fuel_Electricity': metrics['tco']['annual_breakdown']['fuel_electricity'],
                'Maintenance': metrics['tco']['annual_breakdown']['maintenance'],
                'Insurance': metrics['tco']['annual_breakdown']['insurance'],
                'Registration': metrics['tco']['annual_breakdown']['registration'],
                'Total_Cost': [sum(x) for x in zip(*metrics['tco']['annual_breakdown'].values())],
                'Revenue': metrics['revenue']['annual_revenue'],
                'Net_Profit': [r - c for r, c in zip(metrics['revenue']['annual_revenue'], 
                                                   [sum(x) for x in zip(*metrics['tco']['annual_breakdown'].values())])]
            }
            detailed_df = pd.DataFrame(detailed_data)
            csv = detailed_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Detailed CSV",
                data=csv,
                file_name=f"vehicle_tco_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    with col3:
        if st.button("📋 Export Parameters", use_container_width=True):
            params_df = pd.DataFrame(list(model_params.items()), columns=['Parameter', 'Value'])
            csv = params_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Parameters CSV",
                data=csv,
                file_name=f"vehicle_tco_parameters_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

def main():
    if 'initialized' not in st.session_state:
        st.session_state.update(get_scenario_presets()["Balanced"])
        st.session_state.initialized = True
    render_header()
    render_scenario_presets()
    render_sidebar_controls()
    model_params = {
        'vehicle_type': st.session_state.get('vehicle_type', 'Electric Vehicle'),
        'base_price': st.session_state.get('base_price', 45000),
        'annual_mileage': st.session_state.get('annual_mileage', 15000),
        'ownership_years': st.session_state.get('ownership_years', 5),
        'partnership_tier': st.session_state.get('partnership_tier', 'Premium'),
        'partner_count': st.session_state.get('partner_count', 10),
        'fuel_price': st.session_state.get('fuel_price', 3.50),
        'electricity_rate': st.session_state.get('electricity_rate', 0.12),
        'inflation_rate': st.session_state.get('inflation_rate', 2.5)
    }
    with st.spinner("🔄 Calculating metrics..."):
        model = initialize_model(model_params)
        if model:
            metrics = calculate_metrics(model)
            if metrics:
                render_kpi_cards(metrics)
                render_charts(metrics)
                render_sensitivity_analysis(model_params)
                render_recommendations(metrics)
                render_export_section(metrics, model_params)

if __name__ == "__main__":
    main() 