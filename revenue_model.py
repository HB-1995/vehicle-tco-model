from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
try:
    import numpy as np
except ImportError:
    # If numpy is not installed, instruct the user to install it
    raise ImportError("Please install numpy: pip install numpy")
import math

# --- Data Classes for Parameters ---
@dataclass
class VehicleParams:
    vehicle_type: str = "Electric Vehicle"
    base_price: float = 45000
    annual_mileage: int = 15000
    ownership_years: int = 5

@dataclass
class PartnershipParams:
    partnership_tier: str = "Premium"
    partner_count: int = 10
    service_providers: List[str] = field(default_factory=lambda: ["Jiffy Lube", "Mechanics", "Dealerships", "Tire Centers"])
    insurance_partners: List[str] = field(default_factory=lambda: ["Policy Referrals", "Claims Processing"])
    parts_retailers: List[str] = field(default_factory=lambda: ["AutoZone", "Amazon", "RockAuto"])
    fuel_partners: List[str] = field(default_factory=lambda: ["Shell", "GasBuddy"])
    financial_services: List[str] = field(default_factory=lambda: ["Plaid", "Credit Cards", "QuickBooks"])
    data_providers: List[str] = field(default_factory=lambda: ["Jato", "KBB", "CARFAX"])
    enterprise_solutions: List[str] = field(default_factory=lambda: ["Dealership SaaS", "Fleet Management"])

@dataclass
class MarketParams:
    fuel_price: float = 3.50
    electricity_rate: float = 0.12
    inflation_rate: float = 2.5

@dataclass
class UserGrowthParams:
    initial_users: int = 1000
    monthly_growth_rate: float = 0.04  # 4% monthly
    monthly_churn_rate: float = 0.01   # 1% monthly
    engagement_rate: float = 0.7       # 70% of users are active

# --- Main Model Class ---
class VehicleTCORevenueModel:
    def __init__(
        self,
        vehicle: VehicleParams = VehicleParams(),
        partnership: PartnershipParams = PartnershipParams(),
        market: MarketParams = MarketParams(),
        user_growth: UserGrowthParams = UserGrowthParams()
    ):
        self.vehicle = vehicle
        self.partnership = partnership
        self.market = market
        self.user_growth = user_growth
        self.efficiency_params = {
            "Electric Vehicle": {"mpg_equivalent": 100, "kwh_per_mile": 0.3},
            "Hybrid": {"mpg": 50, "kwh_per_mile": 0.1},
            "Gasoline": {"mpg": 25, "kwh_per_mile": 0},
            "Diesel": {"mpg": 30, "kwh_per_mile": 0}
        }
        self.partnership_multipliers = {
            "Basic": 1.0,
            "Premium": 1.5,
            "Enterprise": 2.5
        }

    # --- User Growth Modeling ---
    def project_user_growth(self, months: int = 60) -> List[float]:
        users = [float(self.user_growth.initial_users)]
        for m in range(1, months):
            prev = users[-1]
            growth = prev * self.user_growth.monthly_growth_rate
            churn = prev * self.user_growth.monthly_churn_rate
            users.append(prev + growth - churn)
        return users

    def project_active_users(self, months: int = 60) -> List[float]:
        total_users = self.project_user_growth(months)
        return [u * self.user_growth.engagement_rate for u in total_users]

    # --- Cost Calculations ---
    def calculate_tco(self) -> Dict[str, Any]:
        v = self.vehicle
        m = self.market
        years = v.ownership_years
        inflation = m.inflation_rate / 100
        # Depreciation
        depreciation_rate = {"Electric Vehicle": 0.15, "Hybrid": 0.18, "Gasoline": 0.20, "Diesel": 0.22}.get(v.vehicle_type, 0.20)
        annual_depreciation = []
        remaining_value = v.base_price
        for y in range(years):
            dep = remaining_value * depreciation_rate * (1 + inflation) ** y
            annual_depreciation.append(dep)
            remaining_value -= dep
        # Fuel/Electricity
        eff = self.efficiency_params.get(v.vehicle_type, {"mpg": 25, "kwh_per_mile": 0})
        annual_fuel = []
        for y in range(years):
            fuel_price = m.fuel_price * (1 + inflation) ** y
            elec_rate = m.electricity_rate * (1 + inflation) ** y
            if v.vehicle_type == "Electric Vehicle":
                cost = v.annual_mileage * eff["kwh_per_mile"] * elec_rate
            elif v.vehicle_type == "Hybrid":
                gas = (v.annual_mileage * 0.7 / eff["mpg"]) * fuel_price
                elec = (v.annual_mileage * 0.3 * eff["kwh_per_mile"]) * elec_rate
                cost = gas + elec
            else:
                cost = (v.annual_mileage / eff["mpg"]) * fuel_price
            annual_fuel.append(cost)
        # Maintenance
        maint_rate = {"Electric Vehicle": 0.08, "Hybrid": 0.10, "Gasoline": 0.12, "Diesel": 0.15}.get(v.vehicle_type, 0.12)
        annual_maint = [v.annual_mileage * maint_rate * (1 + y * 0.1) * (1 + inflation) ** y for y in range(years)]
        # Insurance
        ins_rate = {"Electric Vehicle": 0.04, "Hybrid": 0.045, "Gasoline": 0.05, "Diesel": 0.055}.get(v.vehicle_type, 0.05)
        annual_ins = []
        rem_val = v.base_price
        for y in range(years):
            cost = rem_val * ins_rate * (1 + inflation) ** y
            annual_ins.append(cost)
            rem_val *= (1 - depreciation_rate)
        # Registration
        reg_rate = {"Electric Vehicle": 0.01, "Hybrid": 0.012, "Gasoline": 0.015, "Diesel": 0.018}.get(v.vehicle_type, 0.015)
        annual_reg = []
        rem_val = v.base_price
        for y in range(years):
            cost = rem_val * reg_rate * (1 + inflation) ** y
            annual_reg.append(cost)
            rem_val *= (1 - depreciation_rate)
        # Totals
        total_tco = sum(annual_depreciation) + sum(annual_fuel) + sum(annual_maint) + sum(annual_ins) + sum(annual_reg)
        total_miles = v.annual_mileage * years
        tco_per_mile = total_tco / total_miles
        return {
            "total_tco": total_tco,
            "tco_per_mile": tco_per_mile,
            "breakdown": {
                "Depreciation": sum(annual_depreciation),
                "Fuel/Electricity": sum(annual_fuel),
                "Maintenance": sum(annual_maint),
                "Insurance": sum(annual_ins),
                "Registration": sum(annual_reg)
            },
            "annual_breakdown": {
                "depreciation": annual_depreciation,
                "fuel_electricity": annual_fuel,
                "maintenance": annual_maint,
                "insurance": annual_ins,
                "registration": annual_reg
            }
        }

    # --- Revenue Streams ---
    def calculate_revenue_streams(self, months: int = 60) -> Dict[str, Any]:
        p = self.partnership
        tier_mult = self.partnership_multipliers.get(p.partnership_tier, 1.5)
        active_users = self.project_active_users(months)
        # Service Providers
        service_rev = sum([200 for _ in p.service_providers]) * tier_mult * np.mean(active_users)
        # Insurance Partnerships
        insurance_rev = sum([150 for _ in p.insurance_partners]) * tier_mult * np.mean(active_users)
        # Parts Retailers
        parts_rev = sum([100 for _ in p.parts_retailers]) * tier_mult * np.mean(active_users)
        # Fuel Partnerships
        fuel_rev = sum([120 for _ in p.fuel_partners]) * tier_mult * np.mean(active_users)
        # Financial Services
        fin_rev = sum([180 for _ in p.financial_services]) * tier_mult * np.mean(active_users)
        # Data Providers
        data_rev = sum([250 for _ in p.data_providers]) * tier_mult * np.mean(active_users)
        # Enterprise Solutions
        ent_rev = sum([1000 for _ in p.enterprise_solutions]) * tier_mult * p.partner_count
        # Partnership Fees
        base_fee = 1000 * tier_mult * p.partner_count
        # User-based SaaS
        saas_rev = 5 * np.sum(active_users)
        # Total
        total_annual = service_rev + insurance_rev + parts_rev + fuel_rev + fin_rev + data_rev + ent_rev + base_fee + saas_rev
        # Projected growth (15% annual)
        annual_revenue = [total_annual * ((1 + 0.15) ** y) for y in range(self.vehicle.ownership_years)]
        total_revenue = sum(annual_revenue)
        revenue_growth = ((annual_revenue[-1] / annual_revenue[0]) - 1) * 100 if len(annual_revenue) > 1 else 0
        return {
            "total_revenue": total_revenue,
            "revenue_growth": revenue_growth,
            "annual_revenue": annual_revenue,
            "service_providers": service_rev,
            "insurance_partners": insurance_rev,
            "parts_retailers": parts_rev,
            "fuel_partners": fuel_rev,
            "financial_services": fin_rev,
            "data_providers": data_rev,
            "enterprise_solutions": ent_rev,
            "partnership_fees": base_fee,
            "user_saas": saas_rev
        }

    # --- Analysis Methods ---
    def net_profit_projection(self) -> Dict[str, Any]:
        tco = self.calculate_tco()
        revenue = self.calculate_revenue_streams()
        net_profit = revenue['total_revenue'] - tco['total_tco']
        roi = (net_profit / tco['total_tco']) * 100 if tco['total_tco'] > 0 else 0
        return {
            "net_profit": net_profit,
            "roi": roi,
            "tco": tco,
            "revenue": revenue
        }

    def break_even_analysis(self) -> Dict[str, Any]:
        tco = self.calculate_tco()
        revenue = self.calculate_revenue_streams()
        annual_tco = tco['total_tco'] / self.vehicle.ownership_years
        annual_revenue = revenue['total_revenue'] / self.vehicle.ownership_years
        if annual_revenue > annual_tco:
            break_even_months = 12 * (annual_tco / annual_revenue)
        else:
            break_even_months = float('inf')
        return {
            "annual_tco": annual_tco,
            "annual_revenue": annual_revenue,
            "break_even_months": break_even_months,
            "profitable": annual_revenue > annual_tco
        }

    def generate_recommendations(self) -> List[str]:
        tco = self.calculate_tco()
        revenue = self.calculate_revenue_streams()
        net_profit = revenue['total_revenue'] - tco['total_tco']
        roi = (net_profit / tco['total_tco']) * 100 if tco['total_tco'] > 0 else 0
        recs = []
        if roi < 20:
            recs.append("Increase partner count or expand enterprise solutions for higher ROI.")
        if revenue['data_providers'] > revenue['service_providers']:
            recs.append("Data partnerships are outperforming service providers. Consider more data integrations.")
        if revenue['insurance_partners'] < revenue['parts_retailers']:
            recs.append("Expand insurance partnerships for more balanced revenue streams.")
        if self.user_growth.monthly_churn_rate > 0.02:
            recs.append("Reduce churn with better engagement or loyalty programs.")
        if len(recs) == 0:
            recs.append("Current configuration is well balanced. Monitor market trends for new opportunities.")
        return recs

    # --- Utility: Get all parameters as dict ---
    def get_all_parameters(self) -> Dict[str, Any]:
        return {
            "vehicle": self.vehicle.__dict__,
            "partnership": self.partnership.__dict__,
            "market": self.market.__dict__,
            "user_growth": self.user_growth.__dict__
        } 