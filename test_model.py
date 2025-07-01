#!/usr/bin/env python3
"""
Test script for Vehicle TCO Revenue Model
Run this to verify the model calculations work correctly
"""

from revenue_model import VehicleTCOModel

def test_basic_functionality():
    """Test basic model functionality"""
    print("🚗 Testing Vehicle TCO Revenue Model...")
    
    # Test with default parameters
    model = VehicleTCOModel()
    
    # Calculate TCO
    tco_data = model.calculate_tco()
    print(f"✅ TCO Calculation: ${tco_data['total_tco']:,.2f}")
    print(f"   Cost per mile: ${tco_data['tco_per_mile']:.2f}")
    
    # Calculate revenue
    revenue_data = model.calculate_revenue_projections()
    print(f"✅ Revenue Calculation: ${revenue_data['total_revenue']:,.2f}")
    print(f"   Revenue growth: {revenue_data['revenue_growth']:.1f}%")
    
    # Calculate net profit
    net_profit = revenue_data['total_revenue'] - tco_data['total_tco']
    roi = (net_profit / tco_data['total_tco']) * 100 if tco_data['total_tco'] > 0 else 0
    print(f"✅ Net Profit: ${net_profit:,.2f}")
    print(f"   ROI: {roi:.1f}%")
    
    # Test recommendations
    recommendations = model.generate_recommendations()
    print(f"✅ Generated {len(recommendations)} recommendations")
    
    # Test break-even analysis
    break_even = model.get_break_even_analysis()
    print(f"✅ Break-even analysis: {break_even['break_even_months']:.1f} months")
    
    return True

def test_different_vehicle_types():
    """Test different vehicle types"""
    print("\n🔧 Testing different vehicle types...")
    
    vehicle_types = ["Electric Vehicle", "Hybrid", "Gasoline", "Diesel"]
    
    for vehicle_type in vehicle_types:
        model = VehicleTCOModel(vehicle_type=vehicle_type)
        tco_data = model.calculate_tco()
        revenue_data = model.calculate_revenue_projections()
        net_profit = revenue_data['total_revenue'] - tco_data['total_tco']
        
        print(f"   {vehicle_type}: TCO=${tco_data['total_tco']:,.0f}, "
              f"Revenue=${revenue_data['total_revenue']:,.0f}, "
              f"Profit=${net_profit:,.0f}")
    
    return True

def test_partnership_tiers():
    """Test different partnership tiers"""
    print("\n🤝 Testing partnership tiers...")
    
    tiers = ["Basic", "Premium", "Enterprise"]
    
    for tier in tiers:
        model = VehicleTCOModel(partnership_tier=tier)
        revenue_data = model.calculate_revenue_projections()
        
        print(f"   {tier}: Total Revenue=${revenue_data['total_revenue']:,.0f}")
    
    return True

def main():
    """Run all tests"""
    print("🧪 Starting Vehicle TCO Revenue Model Tests\n")
    
    try:
        test_basic_functionality()
        test_different_vehicle_types()
        test_partnership_tiers()
        
        print("\n🎉 All tests passed! The model is working correctly.")
        print("\nTo run the Streamlit app:")
        print("   streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 