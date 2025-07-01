# 🚗 Vehicle TCO Revenue Model

A comprehensive Streamlit application for analyzing vehicle Total Cost of Ownership (TCO) and projecting revenue streams from partnerships and services.

## 📊 Features

### Vehicle Cost Analysis
- **Multiple Vehicle Types**: Electric Vehicle, Hybrid, Gasoline, Diesel
- **Comprehensive TCO Calculation**: Depreciation, Fuel/Electricity, Maintenance, Insurance, Registration
- **Inflation Modeling**: All costs adjusted for inflation over ownership period
- **Age-Progressive Costs**: Maintenance costs increase with vehicle age

### Revenue Projections
- **Partnership Tiers**: Basic, Premium, Enterprise with different revenue multipliers
- **Multiple Revenue Streams**: Partnership fees, data analytics, maintenance services, insurance partnerships
- **Growth Modeling**: 15% annual revenue growth with market expansion
- **Scalable Revenue**: Revenue scales with partner count and vehicle complexity

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
   pip install -r requirements.txt
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
├── revenue_model.py       # Business logic and calculations
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

## 🎯 How to Use

### 1. Configure Vehicle Parameters
- Select vehicle type (EV, Hybrid, Gasoline, Diesel)
- Set base price, annual mileage, and ownership period
- Adjust fuel prices and electricity rates

### 2. Set Partnership Parameters
- Choose partnership tier (Basic, Premium, Enterprise)
- Set number of partners
- Review revenue projections

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
- **Partnership Fees**: Tier-based with partner count scaling
- **Data Analytics**: Mileage-based revenue from telematics
- **Maintenance Services**: Complexity-based service revenue
- **Insurance Partnerships**: Value-based insurance revenue

### Key Assumptions
- 15% annual revenue growth
- Inflation adjustment for all costs and revenues
- Age-progressive maintenance costs
- Partner count scaling effects

## 🛠️ Customization

### Adding New Vehicle Types
1. Update `efficiency_params` in `revenue_model.py`
2. Add depreciation, maintenance, and insurance rates
3. Update vehicle type selection in `app.py`

### Modifying Revenue Streams
1. Edit `partnership_multipliers` in `revenue_model.py`
2. Adjust growth rates in `calculate_revenue_projections()`
3. Update revenue stream calculations as needed

### Styling Changes
1. Modify CSS in `app.py` for visual changes
2. Update `.streamlit/config.toml` for theme changes
3. Customize chart colors and layouts

## 📊 Example Scenarios

### Electric Vehicle with Premium Partnerships
- **Vehicle**: $45,000 Electric Vehicle
- **Usage**: 15,000 miles/year for 5 years
- **Partnerships**: 10 Premium tier partners
- **Result**: Typically shows lower TCO due to reduced fuel costs and higher revenue from data analytics

### High-Mileage Gasoline Vehicle
- **Vehicle**: $35,000 Gasoline Vehicle
- **Usage**: 25,000 miles/year for 3 years
- **Partnerships**: 5 Basic tier partners
- **Result**: Higher fuel costs but potentially profitable with maintenance service revenue

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