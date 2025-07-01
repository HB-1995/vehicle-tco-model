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
import plotly.io as pio

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

# --- Professional Financial Dashboard CSS ---
st.markdown('''
<style>
/* Header */
.fin-header {
    background: linear-gradient(90deg, #1f4e79 0%, #2563eb 100%);
    color: #fff;
    padding: 2.2rem 2rem 1.2rem 2rem;
    border-radius: 0 0 18px 18px;
    box-shadow: 0 4px 24px rgba(31,78,121,0.08);
    margin-bottom: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.fin-header .brand {
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: 1px;
    font-family: 'Inter', Arial, sans-serif;
    margin-right: 2rem;
}
.fin-header .subtitle {
    font-size: 1.1rem;
    font-weight: 400;
    opacity: 0.85;
    margin-top: 0.3rem;
}
.fin-header .nav {
    font-size: 1.1rem;
    font-weight: 500;
    display: flex;
    gap: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] > div:first-child {
    background: #f8fafc;
    border-radius: 0 18px 18px 0;
    box-shadow: 2px 0 16px rgba(31,78,121,0.06);
    padding-top: 1.5rem;
}
.sidebar-card {
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 2px 12px rgba(31,78,121,0.07);
    border: 1px solid #e5e7eb;
    margin-bottom: 1.2rem;
    padding: 1.2rem 1rem 1rem 1rem;
    transition: box-shadow 0.2s;
}
.sidebar-card:hover {
    box-shadow: 0 4px 24px rgba(31,78,121,0.13);
}
.sidebar-section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1f4e79;
    margin-bottom: 0.7rem;
    letter-spacing: 0.5px;
}
.stSlider > div {
    background: #e5e7eb;
    border-radius: 8px;
}
.stNumberInput input {
    background: #f3f4f6;
    border-radius: 6px;
    border: 1px solid #e5e7eb;
    font-size: 1.1rem;
}
.stNumberInput input:focus {
    border: 1.5px solid #2563eb;
}

/* Collapsible sections */
.collapsible {
    cursor: pointer;
    padding: 0.5rem 0;
    border: none;
    outline: none;
    background: none;
    font-size: 1.1rem;
    font-weight: 600;
    color: #2563eb;
    transition: color 0.2s;
    margin-bottom: 0.2rem;
}
.collapsible:hover {
    color: #1f4e79;
}
.collapse-content {
    max-height: 1000px;
    overflow: hidden;
    transition: max-height 0.4s cubic-bezier(0.4,0,0.2,1);
}
.collapse-content.closed {
    max-height: 0;
    padding: 0;
}

/* Main content grid */
.fin-main-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 2.2rem;
    margin-bottom: 2rem;
}
@media (min-width: 900px) {
    .fin-main-grid {
        grid-template-columns: 1fr 1fr;
    }
}

/* Card containers */
.fin-card {
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 2px 12px rgba(31,78,121,0.08);
    border: 1px solid #e5e7eb;
    padding: 2rem 1.5rem 1.5rem 1.5rem;
    margin-bottom: 0.5rem;
    transition: box-shadow 0.2s;
    position: relative;
}
.fin-card:hover {
    box-shadow: 0 4px 24px rgba(31,78,121,0.13);
}

/* Chart containers */
.fin-chart-container {
    background: #f8fafc;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 12px rgba(31,78,121,0.07);
    padding: 1.5rem 1.2rem 1.2rem 1.2rem;
    margin-bottom: 1.2rem;
}

</style>
''', unsafe_allow_html=True)

# --- Custom Header ---
def create_fin_header():
    st.markdown('''
    <div class="fin-header">
        <div>
            <span class="brand">💼 Partnership Revenue Financial Modeller</span>
            <div class="subtitle">Comprehensive Financial Analysis for Partnership Revenue Streams</div>
        </div>
        <div class="nav">
            <!-- Add navigation links if needed -->
        </div>
    </div>
    ''', unsafe_allow_html=True)

# --- Sidebar with Card-Based, Collapsible Sections ---
def create_sidebar_controls():
    with st.sidebar:
        with st.expander("👥 User Base Metrics", expanded=True):
            active_users = st.number_input("Initial Active Users", 100, 1000000, 25000, 1000, key="active_users")
            monthly_growth_rate = st.slider("Monthly Growth Rate (%)", 0.0, 20.0, 8.0, 0.1, key="monthly_growth_rate") / 100
            engagement_rate = st.slider("Engagement Rate (%)", 0.0, 100.0, 65.0, 1.0, key="engagement_rate") / 100
            churn_rate = st.slider("Monthly Churn Rate (%)", 0.0, 20.0, 3.0, 0.1, key="churn_rate") / 100

        with st.expander("🛠️ Service Provider Revenue", expanded=False):
            avg_commission_rate = st.slider("Avg. Commission Rate (%)", 0.0, 50.0, 12.0, 0.1, key="avg_commission_rate") / 100
            bookings_per_1k_users = st.number_input("Bookings per 1K Users", 0, 100, 25, 1, key="bookings_per_1k_users")
            avg_service_value = st.number_input("Avg. Service Value ($)", 0, 10000, 200, 10, key="avg_service_value")

        with st.expander("🛡️ Insurance Revenue", expanded=False):
            referral_commission = st.number_input("Referral Commission ($)", 0, 1000, 75, 5, key="referral_commission")
            conversion_rate = st.slider("Conversion Rate (%)", 0.0, 20.0, 3.5, 0.1, key="conversion_rate") / 100
            claims_processing_fee = st.number_input("Claims Processing Fee ($)", 0, 100, 15, 1, key="claims_processing_fee")
            claims_per_1k_users = st.number_input("Claims per 1K Users", 0, 100, 8, 1, key="claims_per_1k_users")
            policy_retention_bonus = st.number_input("Policy Retention Bonus ($)", 0, 100, 25, 1, key="policy_retention_bonus")

        with st.expander("🏪 Parts & Retail Revenue", expanded=False):
            commission_rate = st.slider("Commission Rate (%)", 0.0, 50.0, 8.0, 0.1, key="commission_rate") / 100
            orders_per_1k_users = st.number_input("Orders per 1K Users", 0, 200, 45, 1, key="orders_per_1k_users")
            avg_order_value = st.number_input("Avg. Order Value ($)", 0, 1000, 125, 5, key="avg_order_value")
            return_rate = st.slider("Return Rate (%)", 0.0, 50.0, 5.0, 0.1, key="return_rate") / 100

        with st.expander("💳 Financial Services Revenue", expanded=False):
            monthly_fee_per_user = st.number_input("Monthly Fee per User ($)", 0.0, 100.0, 2.5, 0.1, key="monthly_fee_per_user")
            connection_rate = st.slider("Connection Rate (%)", 0.0, 100.0, 45.0, 1.0, key="connection_rate") / 100
            transaction_fee = st.number_input("Transaction Fee ($)", 0.0, 10.0, 0.25, 0.01, key="transaction_fee")
            transactions_per_user = st.number_input("Transactions per User", 0, 100, 12, 1, key="transactions_per_user")
            premium_upgrade_rate = st.slider("Premium Upgrade Rate (%)", 0.0, 100.0, 15.0, 1.0, key="premium_upgrade_rate") / 100

        with st.expander("⚙️ Projection Settings", expanded=False):
            months = st.slider("Projection Period (Months)", 6, 60, 24, 1, key="months")

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

# --- Professional Plotly Theme ---
pio.templates["finpro"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, Arial, sans-serif", size=15, color="#374151"),
        paper_bgcolor="#fff",
        plot_bgcolor="#f8fafc",
        colorway=["#2563eb", "#1f4e79", "#52c41a", "#6b7280", "#10b981", "#374151"],
        xaxis=dict(
            gridcolor="#e5e7eb",
            zerolinecolor="#e5e7eb",
            linecolor="#6b7280",
            tickfont=dict(color="#374151"),
            title=dict(font=dict(color="#374151")),
        ),
        yaxis=dict(
            gridcolor="#e5e7eb",
            zerolinecolor="#e5e7eb",
            linecolor="#6b7280",
            tickfont=dict(color="#374151"),
            title=dict(font=dict(color="#374151")),
        ),
        legend=dict(
            bgcolor="#fff",
            bordercolor="#e5e7eb",
            borderwidth=1,
            font=dict(color="#374151", size=13),
        ),
        hoverlabel=dict(
            bgcolor="#2563eb",
            font_size=14,
            font_family="Inter, Arial, sans-serif",
            bordercolor="#fff"
        ),
        margin=dict(l=30, r=30, t=50, b=30),
        transition=dict(duration=500, easing="cubic-in-out"),
    )
)

# --- Professional Metric Card Dashboard ---
def create_metric_card_dashboard(results):
    latest = results.iloc[-1]
    first = results.iloc[0]
    # Metrics
    total_revenue = latest['total_monthly_revenue']
    target_revenue = 50000  # Example target, adjust as needed
    growth_rate = ((latest['total_monthly_revenue'] / first['total_monthly_revenue']) - 1) * 100
    engagement = latest['engaged_users'] / latest['active_users'] * 100 if latest['active_users'] > 0 else 0
    revenue_per_user = latest['total_monthly_revenue'] / latest['active_users'] if latest['active_users'] > 0 else 0
    # Trends (mini-sparklines)
    trend = results['total_monthly_revenue'].pct_change().fillna(0).tail(6).values
    trend_icon = "↗️" if trend[-1] >= 0 else "↘️"
    # Card styles
    card_style = """
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(31, 78, 121, 0.08);
        border: 1px solid #e5e7eb;
        padding: 2rem 1.5rem 1.5rem 1.5rem;
        margin-bottom: 0.5rem;
        min-height: 140px;
        transition: box-shadow 0.2s;
        position: relative;
    """
    icon_style = "font-size: 2.2rem; color: #2563eb; margin-bottom: 0.5rem;"
    title_style = "font-size: 1.1rem; color: #374151; font-weight: 600; margin-bottom: 0.2rem; letter-spacing: 0.5px;"
    value_style = "font-size: 2.1rem; color: #1f4e79; font-weight: 700; margin-bottom: 0.2rem;"
    subtitle_style = "font-size: 0.95rem; color: #6b7280; font-weight: 400; margin-bottom: 0.5rem;"
    bar_bg = "#e5e7eb"
    bar_fg = "linear-gradient(90deg, #2563eb 0%, #1f4e79 100%)"
    bar_height = "12px"
    def progress_bar(value, max_value, color=bar_fg):
        pct = min(max(value / max_value, 0), 1)
        return f'''<div style="background:{bar_bg};border-radius:8px;width:100%;height:{bar_height};overflow:hidden;">
            <div style="background:{color};width:{pct*100:.1f}%;height:{bar_height};transition:width 0.5s;"></div>
        </div>'''
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style='{card_style}' class='metric-card'>
            <div style='{icon_style}'>💰</div>
            <div style='{title_style}'>Total Monthly Revenue</div>
            <div style='{value_style}'>${total_revenue:,.0f} <span style='font-size:1.2rem;'>{trend_icon}</span></div>
            <div style='{subtitle_style}'>Target: ${target_revenue:,.0f}</div>
            {progress_bar(total_revenue, target_revenue*2)}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='{card_style}' class='metric-card'>
            <div style='{icon_style}'>📈</div>
            <div style='{title_style}'>Growth Rate</div>
            <div style='{value_style}'>{growth_rate:.1f}% <span style='font-size:1.2rem;'>{'↗️' if growth_rate >= 0 else '↘️'}</span></div>
            <div style='{subtitle_style}'>Annualized</div>
            {progress_bar(growth_rate, 100)}
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style='{card_style}' class='metric-card'>
            <div style='{icon_style}'>👥</div>
            <div style='{title_style}'>User Engagement</div>
            <div style='{value_style}'>{engagement:.1f}% <span style='font-size:1.2rem;'>{'↗️' if engagement >= 70 else '↘️'}</span></div>
            <div style='font-size:0.98rem;color:#6b7280;margin-bottom:0.2rem;'>
                {int(latest['engaged_users']):,} / {int(latest['total_users']):,} users
            </div>
            <div style='{subtitle_style}'>Engaged Users</div>
            {progress_bar(engagement, 100)}
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style='{card_style}' class='metric-card'>
            <div style='{icon_style}'>🧮</div>
            <div style='{title_style}'>Revenue per User</div>
            <div style='{value_style}'>${revenue_per_user:.2f} <span style='font-size:1.2rem;'>{'↗️' if revenue_per_user >= 5 else '↘️'}</span></div>
            <div style='{subtitle_style}'>Per Active User</div>
            {progress_bar(revenue_per_user, 10)}
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr style='margin: 1.5rem 0 2rem 0; border-top: 2px solid #e0e0e0;'>", unsafe_allow_html=True)

# --- Professional Revenue Charts ---
def create_professional_revenue_charts(results):
    # Revenue over time (line + area)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=results['month'],
        y=results['total_monthly_revenue'],
        mode='lines',
        name='Total Revenue',
        line=dict(width=4, color="#2563eb"),
        fill='tozeroy',
        fillcolor="rgba(37,99,235,0.08)",
        hovertemplate='<b>Total Revenue</b>: $%{y:,.0f}<br>Month: %{x}'
    ))
    # Add individual revenue streams
    streams = [
        ("Service Providers", 'service_revenue', "#1f4e79"),
        ("Insurance", 'insurance_revenue', "#52c41a"),
        ("Parts & Retail", 'parts_revenue', "#6b7280"),
        ("Financial Services", 'financial_revenue', "#10b981")
    ]
    for name, col, color in streams:
        if col in results:
            fig.add_trace(go.Scatter(
                x=results['month'],
                y=results[col],
                mode='lines',
                name=name,
                line=dict(width=2, color=color, dash='solid'),
                hovertemplate=f'<b>{name}</b>: $%{{y:,.0f}}<br>Month: %{{x}}'
            ))
    fig.update_layout(
        template="finpro",
        title="<b>Revenue Growth & Streams</b>",
        xaxis_title="Month",
        yaxis_title="Monthly Revenue ($)",
        height=420,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

def main():
    create_fin_header()
    params = create_sidebar_controls()
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

    # Professional metric card dashboard at the top
    create_metric_card_dashboard(results)
    # Professional revenue charts
    create_professional_revenue_charts(results)

    # Checkbox in sidebar to show/hide the table
    show_table = st.sidebar.checkbox("Show Revenue Projection Table", value=False)
    if show_table:
        st.markdown("### 💰 Partnership Revenue Projection")
        st.dataframe(results)

    # Download button
    st.markdown("### 📁 Export Results")
    st.download_button(
        "Download Revenue Projection (CSV)",
        data=results.to_csv(index=False),
        file_name=f"partnership_revenue_projection_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

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