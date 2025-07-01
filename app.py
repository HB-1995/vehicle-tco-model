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

# Import the correct financial model
from revenue_model import PartnershipRevenueModel

# Page configuration
st.set_page_config(
    page_title="Partnership Revenue Financial Modeller",
    page_icon="💼",
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

# Initialize session state with the correct model
if 'model' not in st.session_state:
    st.session_state.model = PartnershipRevenueModel()

# Header

def create_header():
    st.markdown("""
    <div class="main-header">
        <h1>💼 Partnership Revenue Financial Modeller</h1>
        <p>Comprehensive Financial Analysis for Partnership Revenue Streams</p>
    </div>
    """, unsafe_allow_html=True)

# Only partnership revenue controls

def create_input_controls():
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👥 User Base Metrics")
    active_users = st.sidebar.number_input("Initial Active Users", 100, 1000000, 25000, 1000, key="active_users")
    monthly_growth_rate = st.sidebar.slider("Monthly Growth Rate (%)", 0.0, 20.0, 8.0, 0.1, key="monthly_growth_rate") / 100
    engagement_rate = st.sidebar.slider("Engagement Rate (%)", 0.0, 100.0, 65.0, 1.0, key="engagement_rate") / 100
    churn_rate = st.sidebar.slider("Monthly Churn Rate (%)", 0.0, 20.0, 3.0, 0.1, key="churn_rate") / 100

    st.sidebar.markdown("### 🛠️ Service Provider Revenue")
    avg_commission_rate = st.sidebar.slider("Avg. Commission Rate (%)", 0.0, 50.0, 12.0, 0.1, key="avg_commission_rate") / 100
    bookings_per_1k_users = st.sidebar.number_input("Bookings per 1K Users", 0, 100, 25, 1, key="bookings_per_1k_users")
    avg_service_value = st.sidebar.number_input("Avg. Service Value ($)", 0, 10000, 200, 10, key="avg_service_value")

    st.sidebar.markdown("### 🛡️ Insurance Revenue")
    referral_commission = st.sidebar.number_input("Referral Commission ($)", 0, 1000, 75, 5, key="referral_commission")
    conversion_rate = st.sidebar.slider("Conversion Rate (%)", 0.0, 20.0, 3.5, 0.1, key="conversion_rate") / 100
    claims_processing_fee = st.sidebar.number_input("Claims Processing Fee ($)", 0, 100, 15, 1, key="claims_processing_fee")
    claims_per_1k_users = st.sidebar.number_input("Claims per 1K Users", 0, 100, 8, 1, key="claims_per_1k_users")
    policy_retention_bonus = st.sidebar.number_input("Policy Retention Bonus ($)", 0, 100, 25, 1, key="policy_retention_bonus")

    st.sidebar.markdown("### 🏪 Parts & Retail Revenue")
    commission_rate = st.sidebar.slider("Commission Rate (%)", 0.0, 50.0, 8.0, 0.1, key="commission_rate") / 100
    orders_per_1k_users = st.sidebar.number_input("Orders per 1K Users", 0, 200, 45, 1, key="orders_per_1k_users")
    avg_order_value = st.sidebar.number_input("Avg. Order Value ($)", 0, 1000, 125, 5, key="avg_order_value")
    return_rate = st.sidebar.slider("Return Rate (%)", 0.0, 50.0, 5.0, 0.1, key="return_rate") / 100

    st.sidebar.markdown("### 💳 Financial Services Revenue")
    monthly_fee_per_user = st.sidebar.number_input("Monthly Fee per User ($)", 0.0, 100.0, 2.5, 0.1, key="monthly_fee_per_user")
    connection_rate = st.sidebar.slider("Connection Rate (%)", 0.0, 100.0, 45.0, 1.0, key="connection_rate") / 100
    transaction_fee = st.sidebar.number_input("Transaction Fee ($)", 0.0, 10.0, 0.25, 0.01, key="transaction_fee")
    transactions_per_user = st.sidebar.number_input("Transactions per User", 0, 100, 12, 1, key="transactions_per_user")
    premium_upgrade_rate = st.sidebar.slider("Premium Upgrade Rate (%)", 0.0, 100.0, 15.0, 1.0, key="premium_upgrade_rate") / 100

    st.sidebar.markdown("### ⚙️ Projection Settings")
    months = st.sidebar.slider("Projection Period (Months)", 6, 60, 24, 1, key="months")

    return dict(
        active_users=active_users,
        monthly_growth_rate=monthly_growth_rate,
        engagement_rate=engagement_rate,
        churn_rate=churn_rate,
        avg_commission_rate=avg_commission_rate,
        bookings_per_1k_users=bookings_per_1k_users,
        avg_service_value=avg_service_value,
        referral_commission=referral_commission,
        conversion_rate=conversion_rate,
        claims_processing_fee=claims_processing_fee,
        claims_per_1k_users=claims_per_1k_users,
        policy_retention_bonus=policy_retention_bonus,
        commission_rate=commission_rate,
        orders_per_1k_users=orders_per_1k_users,
        avg_order_value=avg_order_value,
        return_rate=return_rate,
        monthly_fee_per_user=monthly_fee_per_user,
        connection_rate=connection_rate,
        transaction_fee=transaction_fee,
        transactions_per_user=transactions_per_user,
        premium_upgrade_rate=premium_upgrade_rate,
        months=months
    )

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

def create_animated_revenue_chart(results):
    # Prepare traces for each revenue stream
    streams = [
        ("Service Revenue", 'service_revenue', '#ff6b6b'),
        ("Insurance Revenue", 'insurance_revenue', '#4ecdc4'),
        ("Parts & Retail Revenue", 'parts_revenue', '#45b7d1'),
        ("Financial Services Revenue", 'financial_revenue', '#96ceb4'),
        ("Data Revenue", 'data_revenue', '#f9c846'),
    ]
    months = results['month']
    fig = go.Figure()
    # Total revenue area fill
    fig.add_trace(go.Scatter(
        x=months,
        y=results['total_monthly_revenue'],
        mode='lines',
        name='Total Revenue',
        line=dict(width=4, color='#667eea'),
        fill='tozeroy',
        hoverinfo='x+y',
        hovertemplate='<b>Total Revenue</b>: $%{y:,.0f}<br>Month: %{x}'
    ))
    # Add each revenue stream as a line
    for name, col, color in streams:
        if col in results:
            fig.add_trace(go.Scatter(
                x=months,
                y=results[col],
                mode='lines+markers',
                name=name,
                line=dict(width=2, color=color),
                hovertemplate=f'<b>{name}</b>: $%{{y:,.0f}}<br>Month: %{{x}}'
            ))
    # Animation frames
    frames = [
        go.Frame(
            data=[
                go.Scatter(x=months[:k+1], y=results['total_monthly_revenue'][:k+1]),
                *[go.Scatter(x=months[:k+1], y=results[col][:k+1]) for _, col, _ in streams if col in results]
            ],
            name=str(k)
        ) for k in range(len(months))
    ]
    fig.frames = frames
    # Play/Pause buttons
    fig.update_layout(
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {'label': 'Play', 'method': 'animate', 'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True}]},
                {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]}
            ],
            'x': 1.1, 'y': 1.15
        }],
        title="📈 Animated Revenue Growth Over Time",
        xaxis_title="Month",
        yaxis_title="Monthly Revenue ($)",
        hovermode='x unified',
        yaxis_tickformat="$,.0f",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    # Add click event (Streamlit limitation: use st.session_state to show details)
    st.plotly_chart(fig, use_container_width=True)
    st.info("Click any point in the chart to see a detailed breakdown below.")
    clicked = st.session_state.get('clicked_point', None)
    if clicked is not None:
        month = int(clicked)
        breakdown = results[results['month'] == month].iloc[0]
        st.write(f"#### Detailed Breakdown for Month {month}")
        st.json(breakdown.to_dict())

def create_revenue_sankey(results):
    # Use the last month for the most recent breakdown
    latest = results.iloc[-1]
    # Define nodes
    labels = [
        "User Base",
        "Service Revenue",
        "Insurance Revenue",
        "Parts & Retail Revenue",
        "Financial Services Revenue",
        "Data Revenue"
    ]
    colors = [
        "#636EFA",  # User Base
        "#FF6B6B",  # Service
        "#4ECDC4",  # Insurance
        "#45B7D1",  # Parts
        "#96CEB4",  # Financial
        "#F9C846"   # Data
    ]
    # Flows from user base to each revenue stream
    values = [
        latest.get('service_revenue', 0),
        latest.get('insurance_revenue', 0),
        latest.get('parts_revenue', 0),
        latest.get('financial_revenue', 0),
        latest.get('data_revenue', 0)
    ]
    sources = [0, 0, 0, 0, 0]  # All from User Base
    targets = [1, 2, 3, 4, 5]
    link_colors = colors[1:]
    # Sankey diagram
    fig = go.Figure(go.Sankey(
        arrangement = "snap",
        node = dict(
            pad = 20,
            thickness = 30,
            line = dict(color = "black", width = 0.5),
            label = labels,
            color = colors
        ),
        link = dict(
            source = sources,
            target = targets,
            value = values,
            color = link_colors,
            hovertemplate = '<b>%{target.label}</b><br>Revenue: $%{value:,.0f}<extra></extra>'
        )
    ))
    fig.update_layout(
        title_text="💸 User Base to Revenue Streams Flow",
        font_size=14,
        margin=dict(l=10, r=10, t=40, b=10),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Adjust the sliders to see real-time flow changes. (Click nodes to highlight, but use sidebar to adjust parameters.)")

def create_revenue_heatmap(results):
    st.markdown("### 🔥 Revenue Streams Heatmap")
    # Sidebar toggle for value/growth
    mode = st.radio("Heatmap Mode", ["Absolute Values", "Growth Rates"], horizontal=True)
    # Prepare data
    streams = [
        ("Service Revenue", 'service_revenue'),
        ("Insurance Revenue", 'insurance_revenue'),
        ("Parts & Retail Revenue", 'parts_revenue'),
        ("Financial Services Revenue", 'financial_revenue'),
        ("Data Revenue", 'data_revenue'),
    ]
    months = results['month']
    data = []
    for name, col in streams:
        if col in results:
            if mode == "Absolute Values":
                values = results[col].values
            else:
                values = results[col].pct_change().fillna(0).values * 100
            for i, month in enumerate(months):
                data.append({
                    'Month': month,
                    'Revenue Stream': name,
                    'Value': values[i]
                })
    df = pd.DataFrame(data)
    # Pivot for heatmap
    heatmap_df = df.pivot(index='Revenue Stream', columns='Month', values='Value')
    # Color scale
    color_continuous_scale = 'Blues' if mode == "Absolute Values" else 'RdBu'
    # Plotly heatmap
    fig = px.imshow(
        heatmap_df,
        aspect="auto",
        color_continuous_scale=color_continuous_scale,
        labels=dict(x="Month", y="Revenue Stream", color="Revenue ($)" if mode=="Absolute Values" else "Growth Rate (%)"),
        text_auto=True
    )
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>Month: %{x}<br>' + ("Revenue: $%{z:,.0f}" if mode=="Absolute Values" else "Growth: %{z:.1f}%")
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue Stream",
        dragmode='select',
        height=400,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Select a range to zoom. Hover over cells for exact values. Toggle between absolute and growth rates above.")

def create_gauge_dashboard(results):
    latest = results.iloc[-1]
    first = results.iloc[0]
    # Metrics
    total_revenue = latest['total_monthly_revenue']
    target_revenue = 50000  # Example target, adjust as needed
    growth_rate = ((latest['total_monthly_revenue'] / first['total_monthly_revenue']) - 1) * 100
    engagement = latest['engaged_users'] / latest['active_users'] * 100 if latest['active_users'] > 0 else 0
    revenue_per_user = latest['total_monthly_revenue'] / latest['active_users'] if latest['active_users'] > 0 else 0

    # Gauge chart helper
    def gauge_fig(value, title, min_v, max_v, steps, unit="", color_zones=None, target=None):
        if color_zones is None:
            color_zones = [(min_v, min_v + (max_v-min_v)*0.4, "#ff4d4f"), (min_v + (max_v-min_v)*0.4, min_v + (max_v-min_v)*0.7, "#faad14"), (min_v + (max_v-min_v)*0.7, max_v, "#52c41a")]
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = value,
            number = {'suffix': unit},
            delta = {'reference': target, 'increasing': {'color': '#52c41a'}, 'decreasing': {'color': '#ff4d4f'}} if target else None,
            gauge = {
                'axis': {'range': [min_v, max_v]},
                'bar': {'color': '#667eea'},
                'steps': [
                    {'range': [z[0], z[1]], 'color': z[2]} for z in color_zones
                ],
                'threshold': {'line': {'color': '#222', 'width': 4}, 'thickness': 0.75, 'value': target} if target else None
            },
            title = {'text': title}
        ))
        fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=260)
        return fig

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.plotly_chart(gauge_fig(total_revenue, "Total Monthly Revenue", 0, target_revenue*2, 5, unit="$", target=target_revenue), use_container_width=True)
    with col2:
        st.plotly_chart(gauge_fig(growth_rate, "Growth Rate", -20, 100, 5, unit="%", color_zones=[(-20, 0, "#ff4d4f"), (0, 20, "#faad14"), (20, 100, "#52c41a")], target=20), use_container_width=True)
    with col3:
        st.plotly_chart(gauge_fig(engagement, "User Engagement", 0, 100, 5, unit="%", color_zones=[(0, 40, "#ff4d4f"), (40, 70, "#faad14"), (70, 100, "#52c41a")], target=70), use_container_width=True)
    with col4:
        st.plotly_chart(gauge_fig(revenue_per_user, "Revenue per User", 0, 10, 5, unit="$", color_zones=[(0, 2, "#ff4d4f"), (2, 5, "#faad14"), (5, 10, "#52c41a")], target=5), use_container_width=True)
    st.markdown("<hr style='margin: 1.5rem 0 2rem 0; border-top: 2px solid #e0e0e0;'>", unsafe_allow_html=True)

def main():
    create_header()
    params = create_input_controls()
    model = st.session_state.model
    # User Base
    model.user_base.active_users = params['active_users']
    model.user_base.monthly_growth_rate = params['monthly_growth_rate']
    model.user_base.engagement_rate = params['engagement_rate']
    model.user_base.churn_rate = params['churn_rate']
    # Service Providers
    model.service_providers.avg_commission_rate = params['avg_commission_rate']
    model.service_providers.bookings_per_1k_users = params['bookings_per_1k_users']
    model.service_providers.avg_service_value = params['avg_service_value']
    # Insurance
    model.insurance.referral_commission = params['referral_commission']
    model.insurance.conversion_rate = params['conversion_rate']
    model.insurance.claims_processing_fee = params['claims_processing_fee']
    model.insurance.claims_per_1k_users = params['claims_per_1k_users']
    model.insurance.policy_retention_bonus = params['policy_retention_bonus']
    # Parts & Retail
    model.parts_retail.commission_rate = params['commission_rate']
    model.parts_retail.orders_per_1k_users = params['orders_per_1k_users']
    model.parts_retail.avg_order_value = params['avg_order_value']
    model.parts_retail.return_rate = params['return_rate']
    # Financial Services
    model.financial_services.monthly_fee_per_user = params['monthly_fee_per_user']
    model.financial_services.connection_rate = params['connection_rate']
    model.financial_services.transaction_fee = params['transaction_fee']
    model.financial_services.transactions_per_user = params['transactions_per_user']
    model.financial_services.premium_upgrade_rate = params['premium_upgrade_rate']

    # Run projection
    with st.spinner("🔄 Calculating financial projections..."):
        results = model.run_projection(params['months'])

    # Gauge dashboard at the top
    create_gauge_dashboard(results)

    # Checkbox in sidebar to show/hide the table
    show_table = st.sidebar.checkbox("Show Revenue Projection Table", value=False)
    if show_table:
        st.markdown("### 💰 Partnership Revenue Projection")
        st.dataframe(results)

    # Show summary metrics
    st.markdown("### 📊 Key Metrics")
    latest = results.iloc[-1]
    st.metric("Total Monthly Revenue", f"${latest['total_monthly_revenue']:,.0f}")
    st.metric("Active Users", f"{latest['active_users']:,}")
    st.metric("Engaged Users", f"{latest['engaged_users']:,}")

    # Download button
    st.markdown("### 📁 Export Results")
    st.download_button(
        "Download Revenue Projection (CSV)",
        data=results.to_csv(index=False),
        file_name=f"partnership_revenue_projection_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

    # Animated chart
    create_animated_revenue_chart(results)
    # Sankey diagram
    create_revenue_sankey(results)
    # Heatmap
    create_revenue_heatmap(results)

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