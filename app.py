import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime
import base64
import traceback

# Import the financial model
from revenue_model import (
    VehicleTCORevenueModel,
    VehicleParams,
    PartnershipParams,
    MarketParams,
    UserGrowthParams
)

# Page configuration
st.set_page_config(
    page_title="Vehicle TCO Revenue Model",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for financial modelling interface
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
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

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = VehicleTCORevenueModel()

if 'scenario' not in st.session_state:
    st.session_state.scenario = 'moderate'

# Scenario Presets
SCENARIO_PRESETS = {
    "Conservative": dict(vehicle_type="Hybrid", base_price=35000, annual_mileage=12000, ownership_years=5, partnership_tier="Basic", partner_count=5, fuel_price=3.00, electricity_rate=0.10, inflation_rate=2.0),
    "Balanced": dict(vehicle_type="Electric Vehicle", base_price=45000, annual_mileage=15000, ownership_years=5, partnership_tier="Premium", partner_count=10, fuel_price=3.50, electricity_rate=0.12, inflation_rate=2.5),
    "Aggressive": dict(vehicle_type="Electric Vehicle", base_price=60000, annual_mileage=20000, ownership_years=7, partnership_tier="Enterprise", partner_count=20, fuel_price=4.00, electricity_rate=0.15, inflation_rate=3.0),
    "Enterprise": dict(vehicle_type="Electric Vehicle", base_price=80000, annual_mileage=25000, ownership_years=8, partnership_tier="Enterprise", partner_count=30, fuel_price=4.50, electricity_rate=0.18, inflation_rate=3.5)
}

def create_header():
    """Create the main header for financial modelling"""
    st.markdown("""
    <div class="main-header">
        <h1>🚗 Vehicle TCO Revenue Model</h1>
        <p>Comprehensive Total Cost of Ownership Analysis with Partnership Revenue Projections</p>
    </div>
    """, unsafe_allow_html=True)

def create_scenario_controls():
    """Create scenario preset controls"""
    st.sidebar.markdown("### 🎯 Scenario Presets")
    for name, params in SCENARIO_PRESETS.items():
        if st.sidebar.button(f"📊 {name}", key=f"preset_{name}"):
            st.session_state.update(params)
            st.success(f"✅ Applied {name} scenario!")
            st.rerun()

def create_input_controls():
    """Create detailed input controls for financial parameters"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚗 Vehicle Configuration")
    
    vehicle_type = st.sidebar.selectbox("Vehicle Type", ["Electric Vehicle", "Hybrid", "Gasoline", "Diesel"], index=0, key="vehicle_type")
    base_price = st.sidebar.number_input("Base Vehicle Price ($)", 20000, 150000, 45000, 1000, key="base_price")
    annual_mileage = st.sidebar.number_input("Annual Mileage", 5000, 50000, 15000, 1000, key="annual_mileage")
    ownership_years = st.sidebar.slider("Ownership Period (Years)", 1, 15, 5, key="ownership_years")
    
    st.sidebar.markdown("### 🤝 Partnership Revenue")
    partnership_tier = st.sidebar.selectbox("Partnership Tier", ["Basic", "Premium", "Enterprise"], 1, key="partnership_tier")
    partner_count = st.sidebar.number_input("Number of Partners", 1, 100, 10, 1, key="partner_count")
    
    st.sidebar.markdown("### 📈 Market Conditions")
    fuel_price = st.sidebar.number_input("Fuel Price ($/gallon)", 1.0, 10.0, 3.50, 0.1, key="fuel_price")
    electricity_rate = st.sidebar.number_input("Electricity Rate ($/kWh)", 0.05, 0.50, 0.12, 0.01, key="electricity_rate")
    inflation_rate = st.sidebar.slider("Annual Inflation Rate (%)", 0.0, 15.0, 2.5, 0.1, key="inflation_rate")
    
    return dict(vehicle_type=vehicle_type, base_price=base_price, annual_mileage=annual_mileage, ownership_years=ownership_years, partnership_tier=partnership_tier, partner_count=partner_count, fuel_price=fuel_price, electricity_rate=electricity_rate, inflation_rate=inflation_rate)

def apply_scenario(scenario_type):
    """Apply predefined financial scenarios"""
    st.session_state.scenario = scenario_type
    model = st.session_state.model
    
    if scenario_type == 'conservative':
        model.user_base.monthly_growth_rate = 0.04
        model.user_base.engagement_rate = 0.50
        model.service_providers.avg_commission_rate = 0.08
        model.insurance.conversion_rate = 0.025
        model.parts_retail.commission_rate = 0.05
        model.financial_services.connection_rate = 0.30
    
    elif scenario_type == 'moderate':
        model.user_base.monthly_growth_rate = 0.08
        model.user_base.engagement_rate = 0.65
        model.service_providers.avg_commission_rate = 0.12
        model.insurance.conversion_rate = 0.035
        model.parts_retail.commission_rate = 0.08
        model.financial_services.connection_rate = 0.45
    
    elif scenario_type == 'aggressive':
        model.user_base.monthly_growth_rate = 0.15
        model.user_base.engagement_rate = 0.80
        model.service_providers.avg_commission_rate = 0.18
        model.insurance.conversion_rate = 0.06
        model.parts_retail.commission_rate = 0.12
        model.financial_services.connection_rate = 0.65

def create_revenue_summary(results):
    """Create revenue summary cards"""
    latest = results.iloc[-1]
    
    st.markdown(f"""
    <div class="revenue-card">
        <div class="revenue-value">${latest['total_monthly_revenue']:,.0f}</div>
        <div class="revenue-label">Projected Monthly Revenue</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-number">${latest['service_revenue']:,.0f}</div>
            <div class="metric-desc">Service Provider Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-number">${latest['insurance_revenue']:,.0f}</div>
            <div class="metric-desc">Insurance Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-number">${latest['parts_revenue']:,.0f}</div>
            <div class="metric-desc">Parts & Retail Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-item">
            <div class="metric-number">${latest['financial_revenue']:,.0f}</div>
            <div class="metric-desc">Financial Services Revenue</div>
        </div>
        """, unsafe_allow_html=True)

def create_revenue_flow_chart(results):
    """Create a waterfall chart showing revenue flow"""
    latest = results.iloc[-1]
    
    # Revenue categories for waterfall
    categories = ['Service Providers', 'Insurance', 'Parts & Retail', 'Financial Services', 'Total']
    values = [
        latest['service_revenue'],
        latest['insurance_revenue'],
        latest['parts_revenue'],
        latest['financial_revenue'],
        latest['total_monthly_revenue']
    ]
    
    # Create waterfall chart
    fig = go.Figure(go.Waterfall(
        name="Revenue Flow",
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=categories,
        textposition="outside",
        text=[f"${v:,.0f}" for v in values],
        y=values,
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#667eea"}},
        decreasing={"marker": {"color": "#ff6b6b"}},
        totals={"marker": {"color": "#2ecc71"}}
    ))
    
    fig.update_layout(
        title="💰 Revenue Flow Breakdown",
        showlegend=False,
        height=400,
        yaxis_title="Revenue ($)",
        yaxis_tickformat="$,.0f"
    )
    
    return fig

def create_growth_projection_chart(results):
    """Create growth projection chart"""
    fig = go.Figure()
    
    # Total revenue line
    fig.add_trace(go.Scatter(
        x=results['month'],
        y=results['total_monthly_revenue'],
        mode='lines+markers',
        name='Total Revenue',
        line=dict(width=4, color='#667eea'),
        marker=dict(size=8)
    ))
    
    # Individual revenue streams
    revenue_streams = [
        ('Service Providers', results['service_revenue'], '#ff6b6b'),
        ('Insurance', results['insurance_revenue'], '#4ecdc4'),
        ('Parts & Retail', results['parts_revenue'], '#45b7d1'),
        ('Financial Services', results['financial_revenue'], '#96ceb4')
    ]
    
    for name, data, color in revenue_streams:
        fig.add_trace(go.Scatter(
            x=results['month'],
            y=data,
            mode='lines',
            name=name,
            line=dict(width=2, color=color),
            stackgroup='one'
        ))
    
    fig.update_layout(
        title="📈 Revenue Growth Projection",
        xaxis_title="Month",
        yaxis_title="Monthly Revenue ($)",
        height=500,
        hovermode='x unified',
        yaxis_tickformat="$,.0f"
    )
    
    return fig

def create_metrics_dashboard(results):
    """Create key metrics dashboard"""
    latest = results.iloc[-1]
    first = results.iloc[0]
    
    # Calculate key metrics
    total_growth = ((latest['total_monthly_revenue'] / first['total_monthly_revenue']) - 1) * 100
    revenue_per_user = latest['total_monthly_revenue'] / latest['active_users']
    annual_run_rate = latest['total_monthly_revenue'] * 12
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "📊 Total Revenue Growth",
            f"{total_growth:.1f}%",
            delta=f"vs Month 0"
        )
    
    with col2:
        st.metric(
            "💰 Revenue per User",
            f"${revenue_per_user:.2f}",
            delta="per month"
        )
    
    with col3:
        st.metric(
            "🎯 Annual Run Rate",
            f"${annual_run_rate/1000000:.1f}M",
            delta="projected annually"
        )

def main():
    """Main application function"""
    # Create header
    create_header()
    
    # Create scenario controls
    create_scenario_controls()
    
    # Create input controls
    params = create_input_controls()
    
    # Apply parameters to model
    apply_scenario(params['scenario'])
    
    # Run financial projections
    with st.spinner("🔄 Calculating financial projections..."):
        results = st.session_state.model.run_projection(params['projection_params']['months'])
    
    # Display revenue summary
    st.markdown("### 💰 Revenue Overview")
    create_revenue_summary(results)
    
    # Display key metrics
    st.markdown("### 📊 Key Financial Metrics")
    create_metrics_dashboard(results)
    
    # Display charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Growth Projection")
        growth_chart = create_growth_projection_chart(results)
        st.plotly_chart(growth_chart, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Revenue Flow")
        flow_chart = create_revenue_flow_chart(results)
        st.plotly_chart(flow_chart, use_container_width=True)
    
    # Sensitivity Analysis (if enabled)
    if params['projection_params']['sensitivity']:
        st.markdown("### 🎯 Sensitivity Analysis")
        create_sensitivity_analysis()
    
    # Data export
    st.markdown("### 📁 Export Financial Model")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = results.to_csv(index=False)
        st.download_button(
            "📊 Download Financial Data (CSV)",
            data=csv,
            file_name=f"vehicle_tco_model_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        model_data = {
            'scenario': st.session_state.scenario,
            'parameters': params,
            'results': results.to_dict('records'),
            'generated_at': datetime.now().isoformat()
        }
        json_str = json.dumps(model_data, indent=2)
        st.download_button(
            "⚙️ Download Model Configuration (JSON)",
            data=json_str,
            file_name=f"vehicle_tco_config_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7f8c8d; font-size: 0.9rem;'>
        Vehicle TCO Revenue Model • Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

def create_sensitivity_analysis():
    """Create sensitivity analysis section"""
    st.markdown("#### Key Parameter Sensitivity")
    
    # Sensitivity ranges for key parameters
    base_growth = st.session_state.model.user_base.monthly_growth_rate
    growth_range = [base_growth * 0.5, base_growth * 0.75, base_growth, base_growth * 1.25, base_growth * 1.5]
    
    base_commission = st.session_state.model.service_providers.avg_commission_rate
    commission_range = [base_commission * 0.7, base_commission * 0.85, base_commission, base_commission * 1.15, base_commission * 1.3]
    
    # Calculate sensitivity
    sensitivity_results = []
    
    for growth in growth_range:
        for commission in commission_range:
            # Temporarily adjust parameters
            original_growth = st.session_state.model.user_base.monthly_growth_rate
            original_commission = st.session_state.model.service_providers.avg_commission_rate
            
            st.session_state.model.user_base.monthly_growth_rate = growth
            st.session_state.model.service_providers.avg_commission_rate = commission
            
            # Calculate 12-month projection
            temp_results = st.session_state.model.run_projection(12)
            final_revenue = temp_results.iloc[-1]['total_monthly_revenue']
            
            sensitivity_results.append({
                'growth_rate': growth * 100,
                'commission_rate': commission * 100,
                'final_revenue': final_revenue
            })
            
            # Restore original parameters
            st.session_state.model.user_base.monthly_growth_rate = original_growth
            st.session_state.model.service_providers.avg_commission_rate = original_commission
    
    # Create sensitivity heatmap
    sensitivity_df = pd.DataFrame(sensitivity_results)
    pivot_df = sensitivity_df.pivot(index='growth_rate', columns='commission_rate', values='final_revenue')
    
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Commission Rate (%)", y="Growth Rate (%)", color="Revenue ($)"),
        title="Revenue Sensitivity Analysis (12-Month Projection)",
        color_continuous_scale="Blues"
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()