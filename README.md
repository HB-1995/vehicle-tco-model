# 🚗 Vehicle TCO Revenue Model

A comprehensive Streamlit application for analyzing vehicle Total Cost of Ownership (TCO) and projecting revenue streams from partnerships, services, and user growth.

## 📊 Features

### Vehicle Cost Analysis
- **Multiple Vehicle Types**: Electric Vehicle, Hybrid, Gasoline, Diesel
- **Comprehensive TCO Calculation**: Depreciation, Fuel/Electricity, Maintenance, Insurance, Registration
- **Inflation Modeling**: All costs adjusted for inflation over ownership period
- **Age-Progressive Costs**: Maintenance costs increase with vehicle age

### Revenue Projections
- **Partnership Tiers**: Basic, Premium, Enterprise with different revenue multipliers
- **Multiple Revenue Streams**: Service providers, insurance, parts retailers, fuel, financial, data, enterprise SaaS, user SaaS
- **User Growth Modeling**: Churn, engagement, and growth rates
- **Growth Modeling**: 15% annual revenue growth with market expansion
- **Scalable Revenue**: Revenue scales with partner count, user base, and vehicle complexity

### Interactive Dashboard
- **Real-time Calculations**: Instant updates as parameters change
- **Visual Analytics**: Pie charts, line graphs, and sensitivity analysis
- **Key Metrics**: TCO, Revenue, Net Profit, ROI at a glance
- **Strategic Recommendations**: AI-powered insights for optimization

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📁 Project Structure

```
vehicle-tco-model/
├── app.py                 # Main Streamlit application
├── revenue_model.py       # Business logic and calculations (dataclass-based)
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── test_model.py         # Model test script
└── README.md             # This file
```

## 🎯 How to Use

### 1. Configure Vehicle & Market Parameters
- Select vehicle type (EV, Hybrid, Gasoline, Diesel)
- Set base price, annual mileage, and ownership period
- Adjust fuel prices and electricity rates

### 2. Set Partnership & User Growth Parameters
- Choose partnership tier (Basic, Premium, Enterprise)
- Set number of partners
- User growth, churn, and engagement are modeled in the backend (can be exposed in UI)

### 3. Analyze Results
- View key metrics in the dashboard
- Explore cost breakdown with interactive charts
- Review revenue projections and growth
- Check sensitivity analysis for key parameters

### 4. Export Results
- Download comprehensive analysis as CSV
- Use for presentations or further analysis

## 📈 Business Logic

### Cost Calculations
- **Depreciation**: Vehicle-specific rates with inflation adjustment
- **Fuel/Electricity**: Realistic consumption models for each vehicle type
- **Maintenance**: Progressive costs based on vehicle age and type
- **Insurance**: Value-based rates with depreciation considerations
- **Registration**: State/federal tax calculations

### Revenue Projections
- **Service Providers**: Jiffy Lube, mechanics, dealerships, tire centers
- **Insurance Partnerships**: Policy referrals, claims processing
- **Parts Retailers**: AutoZone, Amazon, RockAuto
- **Fuel Partnerships**: Shell, GasBuddy
- **Financial Services**: Plaid, credit cards, QuickBooks
- **Data Providers**: Jato, KBB, CARFAX
- **Enterprise Solutions**: Dealership SaaS, fleet management
- **User SaaS**: Revenue from active user base
- **User Growth**: Modeled with churn and engagement rates

### Key Assumptions
- 15% annual revenue growth
- Inflation adjustment for all costs and revenues
- Age-progressive maintenance costs
- Partner count and user base scaling effects

## 🛠️ Customization

### Adding New Revenue Streams or Vehicle Types
- Update dataclasses in `revenue_model.py`
- Add new logic to `VehicleTCORevenueModel`
- Update UI in `app.py` if you want to expose new parameters

### Modifying User Growth
- Adjust `UserGrowthParams` dataclass or expose in the sidebar

### Styling Changes
- Modify CSS in `app.py` for visual changes
- Update `.streamlit/config.toml` for theme changes
- Customize chart colors and layouts

## 📊 Example Scenarios

### Electric Vehicle with Enterprise Partnerships
- **Vehicle**: $80,000 Electric Vehicle
- **Usage**: 25,000 miles/year for 8 years
- **Partnerships**: 30 Enterprise tier partners
- **Result**: High revenue from enterprise and user SaaS, lower TCO due to reduced fuel costs

### High-Mileage Hybrid with Basic Partnerships
- **Vehicle**: $35,000 Hybrid
- **Usage**: 20,000 miles/year for 5 years
- **Partnerships**: 5 Basic tier partners
- **Result**: Balanced TCO and revenue, strong service provider revenue

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Plotly**: Interactive visualizations

### Performance
- Real-time calculations with instant updates
- Efficient data structures for large parameter ranges
- Optimized chart rendering for smooth interactions

## 📞 Support

For questions or customization requests:
1. Review the business logic in `revenue_model.py`
2. Check the interactive dashboard in `app.py`
3. Modify parameters to test different scenarios

## 🚀 Future Enhancements

Potential improvements:
- Database integration for historical data
- Machine learning for predictive analytics
- Additional vehicle types and configurations
- Advanced sensitivity analysis
- Integration with external APIs for real-time pricing 