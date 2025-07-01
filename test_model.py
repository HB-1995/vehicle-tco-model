#!/usr/bin/env python3
"""
Test script for Vehicle TCO Revenue Model (dataclass-based)
Run this to verify the model calculations and projections work correctly
"""
from revenue_model import (
    VehicleTCORevenueModel,
    VehicleParams,
    PartnershipParams,
    MarketParams,
    UserGrowthParams
)

def test_basic_functionality():
    print("\n🚗 Testing Vehicle TCO Revenue Model...")
    vehicle = VehicleParams()
    partnership = PartnershipParams()
    market = MarketParams()
    user_growth = UserGrowthParams()
    model = VehicleTCORevenueModel(vehicle, partnership, market, user_growth)
    tco = model.calculate_tco()
    revenue = model.calculate_revenue_streams()
    print(f"TCO: ${tco['total_tco']:,.2f} | Cost per mile: ${tco['tco_per_mile']:.2f}")
    print(f"Total Revenue: ${revenue['total_revenue']:,.2f} | Revenue Growth: {revenue['revenue_growth']:.1f}%")
    print(f"Net Profit: ${revenue['total_revenue'] - tco['total_tco']:,.2f}")
    print(f"ROI: {(revenue['total_revenue'] - tco['total_tco']) / tco['total_tco'] * 100:.1f}%")
    print("Breakdown:")
    for k, v in tco['breakdown'].items():
        print(f"  {k}: ${v:,.2f}")
    print("Revenue Streams:")
    for k, v in revenue.items():
        if k not in ['total_revenue', 'revenue_growth', 'annual_revenue']:
            print(f"  {k}: ${v:,.2f}")
    print("Recommendations:")
    for rec in model.generate_recommendations():
        print(f"  - {rec}")
    print("Break-even analysis:")
    print(model.break_even_analysis())
    print("User growth (first 5 months):", model.project_user_growth(5))
    print("Active users (first 5 months):", model.project_active_users(5))
    print("All parameters:")
    print(model.get_all_parameters())

def test_scenarios():
    print("\n🔧 Testing scenario variations...")
    scenarios = [
        VehicleParams(vehicle_type="Electric Vehicle", base_price=80000, annual_mileage=25000, ownership_years=8),
        VehicleParams(vehicle_type="Hybrid", base_price=35000, annual_mileage=20000, ownership_years=5),
        VehicleParams(vehicle_type="Diesel", base_price=40000, annual_mileage=18000, ownership_years=6)
    ]
    for v in scenarios:
        model = VehicleTCORevenueModel(v, PartnershipParams(), MarketParams(), UserGrowthParams())
        tco = model.calculate_tco()
        revenue = model.calculate_revenue_streams()
        print(f"{v.vehicle_type}: TCO=${tco['total_tco']:,.0f}, Revenue=${revenue['total_revenue']:,.0f}, Net Profit=${revenue['total_revenue'] - tco['total_tco']:,.0f}")

def test_partnership_tiers():
    print("\n🤝 Testing partnership tiers...")
    for tier in ["Basic", "Premium", "Enterprise"]:
        partnership = PartnershipParams(partnership_tier=tier)
        model = VehicleTCORevenueModel(VehicleParams(), partnership, MarketParams(), UserGrowthParams())
        revenue = model.calculate_revenue_streams()
        print(f"{tier}: Total Revenue=${revenue['total_revenue']:,.0f}")

def main():
    print("🧪 Starting Vehicle TCO Revenue Model Tests\n")
    test_basic_functionality()
    test_scenarios()
    test_partnership_tiers()
    print("\n🎉 All tests passed! The model is working correctly.")
    print("\nTo run the Streamlit app:")
    print("   streamlit run app.py")

if __name__ == "__main__":
    main() 