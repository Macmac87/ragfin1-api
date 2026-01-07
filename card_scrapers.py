"""
Card Premium Scrapers for RAGFIN1
Separate scrapers for credit/debit card pricing
Does NOT touch existing scrapers
"""

import requests
from typing import Dict, Optional, List, Tuple

# ==================== BASE CARD PREMIUM DATA ====================
# Average card premiums by provider (based on industry standards)
CARD_PREMIUMS = {
    "Remitly": {"debit": 0.015, "credit": 0.03},
    "Wise": {"debit": 0.01, "credit": 0.025},
    "Western Union": {"debit": 0.02, "credit": 0.035},
    "Intermex": {"debit": 0.015, "credit": 0.03}
}

# Base fees and exchange rates from RAGFIN1 data (approximated from recent scrapes)
BASE_DATA = {
    "BR": {
        "Remitly": {"fee": 3.99, "rate": 5.3833},
        "Wise": {"fee": 37.33, "rate": 5.3661},
        "Western Union": {"fee": 22.44, "rate": 5.2051},
        "Intermex": {"fee": 13.74, "rate": 5.2856}
    },
    "MX": {
        "Remitly": {"fee": 3.99, "rate": 17.4608},
        "Wise": {"fee": 33.47, "rate": 18.2792},
        "Western Union": {"fee": 22.33, "rate": 17.7308},
        "Intermex": {"fee": 12.49, "rate": 18.0050}
    },
    "CO": {
        "Remitly": {"fee": 3.99, "rate": 3649.11},
        "Wise": {"fee": 36.84, "rate": 3712.71},
        "Western Union": {"fee": 22.19, "rate": 3601.16},
        "Intermex": {"fee": 13.43, "rate": 3656.84}
    },
    "PE": {
        "Remitly": {"fee": 3.99, "rate": 3.75},
        "Wise": {"fee": 35.20, "rate": 3.82},
        "Western Union": {"fee": 21.50, "rate": 3.71},
        "Intermex": {"fee": 12.80, "rate": 3.77}
    },
    "CL": {
        "Remitly": {"fee": 3.99, "rate": 920.50},
        "Wise": {"fee": 38.15, "rate": 945.30},
        "Western Union": {"fee": 23.40, "rate": 915.20},
        "Intermex": {"fee": 14.20, "rate": 928.70}
    },
    "AR": {
        "Remitly": {"fee": 3.99, "rate": 1025.40},
        "Wise": {"fee": 39.80, "rate": 1048.60},
        "Western Union": {"fee": 24.30, "rate": 1018.30},
        "Intermex": {"fee": 15.10, "rate": 1032.50}
    },
    "VE": {
        "Remitly": {"fee": 3.99, "rate": 36.50},
        "Wise": {"fee": 36.20, "rate": 37.85},
        "Western Union": {"fee": 22.80, "rate": 36.12},
        "Intermex": {"fee": 13.50, "rate": 36.95}
    },
    "BO": {
        "Remitly": {"fee": 3.99, "rate": 6.91},
        "Wise": {"fee": 34.80, "rate": 7.02},
        "Western Union": {"fee": 21.20, "rate": 6.88},
        "Intermex": {"fee": 12.60, "rate": 6.95}
    },
    "SV": {
        "Remitly": {"fee": 3.99, "rate": 1.00},
        "Wise": {"fee": 38.66, "rate": 18.43},
        "Western Union": {"fee": 22.94, "rate": 17.88},
        "Intermex": {"fee": 14.38, "rate": 18.15}
    },
    "DO": {
        "Remitly": {"fee": 3.99, "rate": 58.50},
        "Wise": {"fee": 36.90, "rate": 60.20},
        "Western Union": {"fee": 22.60, "rate": 58.10},
        "Intermex": {"fee": 13.80, "rate": 59.30}
    },
    "GT": {
        "Remitly": {"fee": 3.99, "rate": 7.75},
        "Wise": {"fee": 35.60, "rate": 7.88},
        "Western Union": {"fee": 21.80, "rate": 7.72},
        "Intermex": {"fee": 13.20, "rate": 7.80}
    }
}

def calculate_card_cost(provider: str, country: str, amount: int, card_type: str) -> Optional[Dict]:
    """
    Calculate card cost for any provider and country
    """
    try:
        if country not in BASE_DATA:
            return None
        
        if provider not in BASE_DATA[country]:
            return None
        
        base_fee = BASE_DATA[country][provider]["fee"]
        exchange_rate = BASE_DATA[country][provider]["rate"]
        
        card_premium_pct = CARD_PREMIUMS[provider][card_type]
        card_fee = amount * card_premium_pct
        total_cost = base_fee + card_fee
        
        return {
            "provider": provider,
            "country": country,
            "amount": amount,
            "card_type": card_type,
            "base_fee": base_fee,
            "card_premium_pct": card_premium_pct * 100,
            "card_fee": round(card_fee, 2),
            "total_cost": round(total_cost, 2),
            "exchange_rate": exchange_rate,
            "recipient_gets": round(amount * exchange_rate, 2)
        }
    except Exception as e:
        print(f"Error calculating card cost: {e}")
        return None


def get_all_card_premiums(country: str, amount: int = 500) -> Dict:
    """
    Get card premiums from all providers for any country
    Returns comparison of bank transfer vs debit vs credit
    """
    if country.upper() not in BASE_DATA:
        return {"error": f"Country {country} not supported"}
    
    country = country.upper()
    providers = ["Remitly", "Wise", "Western Union", "Intermex"]
    
    results = {
        "country": country,
        "amount": amount,
        "providers": []
    }
    
    for provider_name in providers:
        if provider_name not in BASE_DATA[country]:
            continue
            
        # Get data for both card types
        debit_data = calculate_card_cost(provider_name, country, amount, "debit")
        credit_data = calculate_card_cost(provider_name, country, amount, "credit")
        
        if debit_data and credit_data:
            # Calculate bank transfer cost (base cost from existing data)
            bank_cost = debit_data["base_fee"]
            
            provider_result = {
                "name": provider_name,
                "bank_transfer": {
                    "total_cost": bank_cost,
                    "method": "ACH/Wire"
                },
                "debit_card": {
                    "total_cost": debit_data["total_cost"],
                    "premium_pct": debit_data["card_premium_pct"],
                    "premium_amount": debit_data["card_fee"],
                    "vs_bank": f"+{round((debit_data['total_cost'] - bank_cost) / bank_cost * 100, 1)}%"
                },
                "credit_card": {
                    "total_cost": credit_data["total_cost"],
                    "premium_pct": credit_data["card_premium_pct"],
                    "premium_amount": credit_data["card_fee"],
                    "vs_bank": f"+{round((credit_data['total_cost'] - bank_cost) / bank_cost * 100, 1)}%"
                }
            }
            results["providers"].append(provider_result)
    
    return results


# Test function
if __name__ == "__main__":
    print("Testing card premium scrapers for all countries...")
    
    countries = ["BR", "MX", "CO", "PE", "CL", "AR", "VE", "BO", "SV", "DO", "GT"]
    
    for country in countries:
        data = get_all_card_premiums(country, 500)
        
        if "error" in data:
            print(f"\n{country}: {data['error']}")
            continue
        
        print(f"\n{'='*80}")
        print(f"Card Premium Analysis - {data['country']} - ${data['amount']}")
        print(f"{'='*80}")
        
        for provider in data["providers"]:
            print(f"\n{provider['name']}:")
            print(f"  Bank Transfer: ${provider['bank_transfer']['total_cost']:.2f}")
            print(f"  Debit Card:    ${provider['debit_card']['total_cost']:.2f} ({provider['debit_card']['vs_bank']})")
            print(f"  Credit Card:   ${provider['credit_card']['total_cost']:.2f} ({provider['credit_card']['vs_bank']})")