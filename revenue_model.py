import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class UserBase:
    """User base metrics for financial modeling"""
    active_users: int = 25000
    monthly_growth_rate: float = 0.08  # 8% monthly growth
    engagement_rate: float = 0.65  # % of users engaging with revenue features
    churn_rate: float = 0.03  # 3% monthly churn

@dataclass
class ServiceProviders:
    """Service provider partnership revenue parameters"""
    avg_commission_rate: float = 0.12  # 12% average commission
    bookings_per_1k_users: int = 25  # Monthly bookings per 1K users
    avg_service_value: float = 200.0  # Average service booking value
    major_partners: int = 15  # Number of major service partners
    
@dataclass
class Insurance:
    """Insurance partnership revenue parameters"""
    referral_commission: float = 75.0  # Average referral commission
    conversion_rate: float = 0.035  # 3.5% of users get quotes
    claims_processing_fee: float = 15.0  # Fee per claim processed
    claims_per_1k_users: int = 8  # Monthly claims per 1K users
    policy_retention_bonus: float = 25.0  # Bonus for retained policies

@dataclass
class PartsRetail:
    """Parts and retail partnership revenue parameters"""
    commission_rate: float = 0.08  # 8% average commission
    orders_per_1k_users: int = 45  # Monthly orders per 1K users
    avg_order_value: float = 125.0  # Average order value
    return_rate: float = 0.05  # 5% return rate
    major_retailers: int = 8  # Number of major retail partners

@dataclass
class FinancialServices:
    """Financial services partnership revenue parameters"""
    monthly_fee_per_user: float = 2.50  # Monthly fee per connected user
    connection_rate: float = 0.45  # 45% of users connect financial accounts
    transaction_fee: float = 0.25  # Fee per transaction categorized
    transactions_per_user: int = 12  # Monthly transactions per user
    premium_upgrade_rate: float = 0.15  # % who upgrade to premium financial features

@dataclass
class DataServices:
    """Data services and API revenue parameters"""
    vehicle_data_fee: float = 0.50  # Fee per vehicle data query
    queries_per_user: int = 8  # Monthly queries per user
    valuation_fee: float = 3.0  # Fee per vehicle valuation
    valuations_per_1k_users: int = 15  # Monthly valuations per 1K users
    api_licensing_monthly: float = 2500.0  # Monthly API licensing revenue

@dataclass
class VehicleParams:
    """Parameters for the vehicle configuration."""
    vehicle_type: str = "Electric Vehicle"
    base_price: float = 45000
    annual_mileage: int = 15000
    ownership_years: int = 5

@dataclass
class PartnershipParams:
    """Parameters for partnership and revenue streams."""
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
    """Parameters for market conditions."""
    fuel_price: float = 3.50
    electricity_rate: float = 0.12
    inflation_rate: float = 2.5

@dataclass
class UserGrowthParams:
    """Parameters for user growth modeling."""
    initial_users: int = 1000
    monthly_growth_rate: float = 0.04  # 4% monthly
    monthly_churn_rate: float = 0.01   # 1% monthly
    engagement_rate: float = 0.7       # 70% of users are active

class PartnershipRevenueModel:
    """Main financial model for partnership revenue streams"""
    
    def __init__(self):
        self.user_base = UserBase()
        self.service_providers = ServiceProviders()
        self.insurance = Insurance()
        self.parts_retail = PartsRetail()
        self.financial_services = FinancialServices()
        self.data_services = DataServices()
    
    def calculate_user_metrics(self, month: int) -> Dict[str, int]:
        """Calculate user base for given month"""
        base_users = self.user_base.active_users
        
        # Apply growth and churn over time
        for m in range(month):
            growth = base_users * self.user_base.monthly_growth_rate
            churn = base_users * self.user_base.churn_rate
            base_users = base_users + growth - churn
        
        engaged_users = int(base_users * self.user_base.engagement_rate)
        
        return {
            'total_users': int(base_users),
            'active_users': int(base_users),
            'engaged_users': engaged_users
        }
    
    def calculate_service_revenue(self, users: Dict[str, int]) -> float:
        """Calculate service provider revenue"""
        engaged_users = users['engaged_users']
        
        # Monthly bookings
        monthly_bookings = (engaged_users / 1000) * self.service_providers.bookings_per_1k_users
        
        # Total booking value
        total_booking_value = monthly_bookings * self.service_providers.avg_service_value
        
        # Commission revenue
        commission_revenue = total_booking_value * self.service_providers.avg_commission_rate
        
        return commission_revenue
    
    def calculate_insurance_revenue(self, users: Dict[str, int]) -> float:
        """Calculate insurance partnership revenue"""
        active_users = users['active_users']
        
        # Policy referrals
        policy_referrals = active_users * self.insurance.conversion_rate
        referral_revenue = policy_referrals * self.insurance.referral_commission
        
        # Claims processing
        monthly_claims = (active_users / 1000) * self.insurance.claims_per_1k_users
        claims_revenue = monthly_claims * self.insurance.claims_processing_fee
        
        # Policy retention bonuses (25% of referrals retain after 6 months)
        retention_bonus = (policy_referrals * 0.25) * self.insurance.policy_retention_bonus
        
        return referral_revenue + claims_revenue + retention_bonus
    
    def calculate_parts_revenue(self, users: Dict[str, int]) -> float:
        """Calculate parts and retail revenue"""
        engaged_users = users['engaged_users']
        
        # Monthly orders
        monthly_orders = (engaged_users / 1000) * self.parts_retail.orders_per_1k_users
        
        # Adjust for returns
        net_orders = monthly_orders * (1 - self.parts_retail.return_rate)
        
        # Total order value
        total_order_value = net_orders * self.parts_retail.avg_order_value
        
        # Commission revenue
        commission_revenue = total_order_value * self.parts_retail.commission_rate
        
        return commission_revenue
    
    def calculate_financial_revenue(self, users: Dict[str, int]) -> float:
        """Calculate financial services revenue"""
        active_users = users['active_users']
        
        # Connected users
        connected_users = active_users * self.financial_services.connection_rate
        
        # Monthly subscription fees
        subscription_revenue = connected_users * self.financial_services.monthly_fee_per_user
        
        # Transaction fees
        total_transactions = connected_users * self.financial_services.transactions_per_user
        transaction_revenue = total_transactions * self.financial_services.transaction_fee
        
        # Premium upgrades
        premium_users = connected_users * self.financial_services.premium_upgrade_rate
        premium_revenue = premium_users * 5.0  # $5 premium fee
        
        return subscription_revenue + transaction_revenue + premium_revenue
    
    def calculate_data_revenue(self, users: Dict[str, int]) -> float:
        """Calculate data services revenue"""
        active_users = users['active_users']
        
        # Vehicle data queries
        monthly_queries = active_users * self.data_services.queries_per_user
        query_revenue = monthly_queries * self.data_services.vehicle_data_fee
        
        # Vehicle valuations
        monthly_valuations = (active_users / 1000) * self.data_services.valuations_per_1k_users
        valuation_revenue = monthly_valuations * self.data_services.valuation_fee
        
        # API licensing (grows with scale)
        api_revenue = self.data_services.api_licensing_monthly * min(active_users / 10000, 5.0)
        
        return query_revenue + valuation_revenue + api_revenue
    
    def calculate_monthly_revenue(self, month: int) -> Dict[str, float]:
        """Calculate total monthly revenue breakdown"""
        users = self.calculate_user_metrics(month)
        
        service_revenue = self.calculate_service_revenue(users)
        insurance_revenue = self.calculate_insurance_revenue(users)
        parts_revenue = self.calculate_parts_revenue(users)
        financial_revenue = self.calculate_financial_revenue(users)
        data_revenue = self.calculate_data_revenue(users)
        
        total_revenue = (service_revenue + insurance_revenue + parts_revenue + 
                        financial_revenue + data_revenue)
        
        return {
            'month': month,
            'total_users': users['total_users'],
            'active_users': users['active_users'],
            'engaged_users': users['engaged_users'],
            'service_revenue': service_revenue,
            'insurance_revenue': insurance_revenue,
            'parts_revenue': parts_revenue,
            'financial_revenue': financial_revenue,
            'data_revenue': data_revenue,
            'total_monthly_revenue': total_revenue
        }
    
    def run_projection(self, months: int = 24) -> pd.DataFrame:
        """Run complete financial projection"""
        results = []
        
        for month in range(months + 1):
            monthly_data = self.calculate_monthly_revenue(month)
            results.append(monthly_data)
        
        return pd.DataFrame(results)
    
    def sensitivity_analysis(self, parameter: str, range_values: List[float], 
                           projection_months: int = 12) -> pd.DataFrame:
        """Perform sensitivity analysis on key parameters"""
        original_value = getattr(self, parameter.split('.')[0])
        results = []
        
        for value in range_values:
            # Update parameter
            if '.' in parameter:
                obj_name, attr_name = parameter.split('.')
                original_attr_value = getattr(getattr(self, obj_name), attr_name)
                setattr(getattr(self, obj_name), attr_name, value)
            
            # Run projection
            projection = self.run_projection(projection_months)
            final_revenue = projection.iloc[-1]['total_monthly_revenue']
            
            results.append({
                'parameter_value': value,
                'final_revenue': final_revenue,
                'revenue_change_pct': ((final_revenue / projection.iloc[0]['total_monthly_revenue']) - 1) * 100
            })
            
            # Restore original value
            if '.' in parameter:
                setattr(getattr(self, obj_name), attr_name, original_attr_value)
        
        return pd.DataFrame(results)
    
    def export_model_config(self) -> Dict:
        """Export current model configuration"""
        return {
            'user_base': {
                'active_users': self.user_base.active_users,
                'monthly_growth_rate': self.user_base.monthly_growth_rate,
                'engagement_rate': self.user_base.engagement_rate,
                'churn_rate': self.user_base.churn_rate
            },
            'service_providers': {
                'avg_commission_rate': self.service_providers.avg_commission_rate,
                'bookings_per_1k_users': self.service_providers.bookings_per_1k_users,
                'avg_service_value': self.service_providers.avg_service_value
            },
            'insurance': {
                'referral_commission': self.insurance.referral_commission,
                'conversion_rate': self.insurance.conversion_rate,
                'claims_processing_fee': self.insurance.claims_processing_fee
            },
            'parts_retail': {
                'commission_rate': self.parts_retail.commission_rate,
                'orders_per_1k_users': self.parts_retail.orders_per_1k_users,
                'avg_order_value': self.parts_retail.avg_order_value
            },
            'financial_services': {
                'monthly_fee_per_user': self.financial_services.monthly_fee_per_user,
                'connection_rate': self.financial_services.connection_rate,
                'transaction_fee': self.financial_services.transaction_fee
            },
            'data_services': {
                'vehicle_data_fee': self.data_services.vehicle_data_fee,
                'valuation_fee': self.data_services.valuation_fee,
                'api_licensing_monthly': self.data_services.api_licensing_monthly
            }
        }

class VehicleTCORevenueModel:
    """
    Comprehensive Vehicle TCO and Revenue Model with partnership, service, insurance, parts, fuel, financial, data, and enterprise revenue streams.
    Includes user growth modeling and projection/analysis methods.
    """
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
        """Project total users over time with growth and churn."""
        users = [float(self.user_growth.initial_users)]
        for _ in range(1, months):
            prev = users[-1]
            growth = prev * self.user_growth.monthly_growth_rate
            churn = prev * self.user_growth.monthly_churn_rate
            users.append(prev + growth - churn)
        return users

    def project_active_users(self, months: int = 60) -> List[float]:
        """Project active users over time based on engagement rate."""
        return [u * self.user_growth.engagement_rate for u in self.project_user_growth(months)]

    # --- Cost Calculations ---
    def calculate_tco(self) -> Dict[str, Any]:
        """Calculate total cost of ownership and annual breakdowns."""
        v, m, years = self.vehicle, self.market, self.vehicle.ownership_years
        inflation = m.inflation_rate / 100
        # Depreciation
        depreciation_rate = {"Electric Vehicle": 0.15, "Hybrid": 0.18, "Gasoline": 0.20, "Diesel": 0.22}.get(v.vehicle_type, 0.20)
        annual_depreciation, remaining_value = [], v.base_price
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
        annual_ins, rem_val = [], v.base_price
        for y in range(years):
            cost = rem_val * ins_rate * (1 + inflation) ** y
            annual_ins.append(cost)
            rem_val *= (1 - depreciation_rate)
        # Registration
        reg_rate = {"Electric Vehicle": 0.01, "Hybrid": 0.012, "Gasoline": 0.015, "Diesel": 0.018}.get(v.vehicle_type, 0.015)
        annual_reg, rem_val = [], v.base_price
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
        """Calculate all partnership and user-based revenue streams."""
        p, tier_mult = self.partnership, self.partnership_multipliers.get(self.partnership.partnership_tier, 1.5)
        active_users = self.project_active_users(months)
        # Revenue streams
        service_rev = len(p.service_providers) * 200 * tier_mult * np.mean(active_users)
        insurance_rev = len(p.insurance_partners) * 150 * tier_mult * np.mean(active_users)
        parts_rev = len(p.parts_retailers) * 100 * tier_mult * np.mean(active_users)
        fuel_rev = len(p.fuel_partners) * 120 * tier_mult * np.mean(active_users)
        fin_rev = len(p.financial_services) * 180 * tier_mult * np.mean(active_users)
        data_rev = len(p.data_providers) * 250 * tier_mult * np.mean(active_users)
        ent_rev = len(p.enterprise_solutions) * 1000 * tier_mult * p.partner_count
        base_fee = 1000 * tier_mult * p.partner_count
        saas_rev = 5 * np.sum(active_users)
        total_annual = service_rev + insurance_rev + parts_rev + fuel_rev + fin_rev + data_rev + ent_rev + base_fee + saas_rev
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
        """Return net profit and ROI projections."""
        tco = self.calculate_tco()
        revenue = self.calculate_revenue_streams()
        net_profit = revenue['total_revenue'] - tco['total_tco']
        roi = (net_profit / tco['total_tco']) * 100 if tco['total_tco'] > 0 else 0
        return {"net_profit": net_profit, "roi": roi, "tco": tco, "revenue": revenue}

    def break_even_analysis(self) -> Dict[str, Any]:
        """Return break-even analysis and profitability."""
        tco = self.calculate_tco()
        revenue = self.calculate_revenue_streams()
        annual_tco = tco['total_tco'] / self.vehicle.ownership_years
        annual_revenue = revenue['total_revenue'] / self.vehicle.ownership_years
        break_even_months = 12 * (annual_tco / annual_revenue) if annual_revenue > annual_tco else float('inf')
        return {
            "annual_tco": annual_tco,
            "annual_revenue": annual_revenue,
            "break_even_months": break_even_months,
            "profitable": annual_revenue > annual_tco
        }

    def generate_recommendations(self) -> List[str]:
        """Generate strategic recommendations based on model results."""
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
        if not recs:
            recs.append("Current configuration is well balanced. Monitor market trends for new opportunities.")
        return recs

    def get_all_parameters(self) -> Dict[str, Any]:
        """Return all model parameters as a dictionary."""
        return {
            "vehicle": self.vehicle.__dict__,
            "partnership": self.partnership.__dict__,
            "market": self.market.__dict__,
            "user_growth": self.user_growth.__dict__
        }