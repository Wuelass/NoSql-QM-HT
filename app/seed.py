from datetime import datetime, timedelta, timezone
import random

from app.db import get_db

UTC = timezone.utc
RNG = random.Random(42)


ASSETS = [
    {"_id": "aapl", "symbol": "AAPL", "name": "Apple", "type": "action", "sector": "Technologie", "currency": "USD", "base_price": 210.00},
    {"_id": "msft", "symbol": "MSFT", "name": "Microsoft", "type": "action", "sector": "Technologie", "currency": "USD", "base_price": 455.00},
    {"_id": "googl", "symbol": "GOOGL", "name": "Alphabet", "type": "action", "sector": "Technologie", "currency": "USD", "base_price": 185.00},
    {"_id": "amzn", "symbol": "AMZN", "name": "Amazon", "type": "action", "sector": "Consommation", "currency": "USD", "base_price": 195.00},
    {"_id": "nvda", "symbol": "NVDA", "name": "Nvidia", "type": "action", "sector": "Semi-conducteurs", "currency": "USD", "base_price": 125.00},
    {"_id": "meta", "symbol": "META", "name": "Meta Platforms", "type": "action", "sector": "Communication", "currency": "USD", "base_price": 520.00},
    {"_id": "tsla", "symbol": "TSLA", "name": "Tesla", "type": "action", "sector": "Automobile", "currency": "USD", "base_price": 240.00},
    {"_id": "air", "symbol": "AIR", "name": "Airbus", "type": "action", "sector": "Industrie", "currency": "EUR", "base_price": 160.00},
    {"_id": "mc", "symbol": "MC", "name": "LVMH", "type": "action", "sector": "Luxe", "currency": "EUR", "base_price": 720.00},
    {"_id": "or", "symbol": "OR", "name": "L'Oreal", "type": "action", "sector": "Consommation", "currency": "EUR", "base_price": 430.00},
    {"_id": "san", "symbol": "SAN", "name": "Sanofi", "type": "action", "sector": "Sante", "currency": "EUR", "base_price": 92.00},
    {"_id": "bn", "symbol": "BN", "name": "Danone", "type": "action", "sector": "Consommation", "currency": "EUR", "base_price": 65.00},
    {"_id": "ttek", "symbol": "TTE", "name": "TotalEnergies", "type": "action", "sector": "Energie", "currency": "EUR", "base_price": 61.00},
    {"_id": "asml", "symbol": "ASML", "name": "ASML Holding", "type": "action", "sector": "Semi-conducteurs", "currency": "EUR", "base_price": 920.00},
    {"_id": "sap", "symbol": "SAP", "name": "SAP", "type": "action", "sector": "Logiciels", "currency": "EUR", "base_price": 190.00},
    {"_id": "btc", "symbol": "BTC", "name": "Bitcoin", "type": "crypto", "sector": "Crypto", "currency": "USD", "base_price": 68000.00},
    {"_id": "eth", "symbol": "ETH", "name": "Ethereum", "type": "crypto", "sector": "Crypto", "currency": "USD", "base_price": 3500.00},
    {"_id": "sol", "symbol": "SOL", "name": "Solana", "type": "crypto", "sector": "Crypto", "currency": "USD", "base_price": 150.00},
    {"_id": "bnb", "symbol": "BNB", "name": "BNB", "type": "crypto", "sector": "Crypto", "currency": "USD", "base_price": 610.00},
    {"_id": "xrp", "symbol": "XRP", "name": "XRP", "type": "crypto", "sector": "Crypto", "currency": "USD", "base_price": 0.58},
    {"_id": "ada", "symbol": "ADA", "name": "Cardano", "type": "crypto", "sector": "Crypto", "currency": "USD", "base_price": 0.45},
    {"_id": "cw8", "symbol": "CW8", "name": "Amundi MSCI World", "type": "etf", "sector": "ETF Monde", "currency": "EUR", "base_price": 470.00},
    {"_id": "ewld", "symbol": "EWLD", "name": "Lyxor MSCI World", "type": "etf", "sector": "ETF Monde", "currency": "EUR", "base_price": 31.00},
    {"_id": "sp500", "symbol": "SP500", "name": "ETF S&P 500", "type": "etf", "sector": "ETF USA", "currency": "EUR", "base_price": 510.00},
    {"_id": "nasdaq100", "symbol": "NDX", "name": "ETF Nasdaq 100", "type": "etf", "sector": "ETF Technologie", "currency": "EUR", "base_price": 890.00},
    {"_id": "emerging", "symbol": "EM", "name": "ETF Marches Emergents", "type": "etf", "sector": "ETF Emergents", "currency": "EUR", "base_price": 24.00},
    {"_id": "stoxx50", "symbol": "SX5E", "name": "ETF Euro Stoxx 50", "type": "etf", "sector": "ETF Europe", "currency": "EUR", "base_price": 52.00},
    {"_id": "gold", "symbol": "GOLD", "name": "Or", "type": "matiere_premiere", "sector": "Metaux", "currency": "USD", "base_price": 2350.00},
    {"_id": "silver", "symbol": "SILVER", "name": "Argent", "type": "matiere_premiere", "sector": "Metaux", "currency": "USD", "base_price": 29.00},
    {"_id": "oil", "symbol": "OIL", "name": "Petrole Brent", "type": "matiere_premiere", "sector": "Energie", "currency": "USD", "base_price": 83.00},
    {"_id": "frbond", "symbol": "FRBOND", "name": "Obligation Etat France", "type": "obligation", "sector": "Obligations", "currency": "EUR", "base_price": 102.00},
    {"_id": "usbond", "symbol": "USBOND", "name": "Obligation Etat USA", "type": "obligation", "sector": "Obligations", "currency": "USD", "base_price": 98.00},
]


FIRST_NAMES = [
    "Lina", "Adam", "Sarah", "Hugo", "Emma", "Lucas", "Ines", "Noah", "Chloe", "Leo",
    "Manon", "Nathan", "Camille", "Tom", "Jade", "Nina", "Enzo", "Lea", "Maxime", "Clara",
    "Yanis", "Alice", "Mehdi", "Julie", "Antoine",
]

LAST_NAMES = [
    "Martin", "Bernard", "Petit", "Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefevre", "Michel",
    "Garcia", "Roux", "David", "Bertrand", "Morel", "Fournier", "Girard", "Bonnet", "Dupont", "Lambert",
    "Fontaine", "Rousseau", "Vincent", "Muller", "Faure",
]

RISK_PROFILES = ["prudent", "modere", "equilibre", "dynamique", "agressif"]


PROFILE_WEIGHTS = {
    "prudent": {"etf": 0.45, "obligation": 0.35, "action": 0.15, "matiere_premiere": 0.05, "crypto": 0.00},
    "modere": {"etf": 0.45, "action": 0.30, "obligation": 0.15, "matiere_premiere": 0.07, "crypto": 0.03},
    "equilibre": {"etf": 0.35, "action": 0.35, "crypto": 0.10, "obligation": 0.10, "matiere_premiere": 0.10},
    "dynamique": {"action": 0.45, "etf": 0.25, "crypto": 0.20, "matiere_premiere": 0.07, "obligation": 0.03},
    "agressif": {"crypto": 0.35, "action": 0.40, "etf": 0.15, "matiere_premiere": 0.08, "obligation": 0.02},
}


def dt(days_ago: int) -> datetime:
    return datetime.now(UTC) - timedelta(days=days_ago)


def clean_assets():
    return [{k: v for k, v in asset.items() if k != "base_price"} for asset in ASSETS]


def weighted_asset_choice(risk_profile: str, excluded_ids=None):
    excluded_ids = excluded_ids or set()
    candidates = [asset for asset in ASSETS if asset["_id"] not in excluded_ids]
    weights = [PROFILE_WEIGHTS[risk_profile].get(asset["type"], 0.01) for asset in candidates]
    return RNG.choices(candidates, weights=weights, k=1)[0]


def generate_users():
    users = []
    for i, (first_name, last_name) in enumerate(zip(FIRST_NAMES, LAST_NAMES), start=1):
        risk_profile = RISK_PROFILES[(i - 1) % len(RISK_PROFILES)]
        users.append({
            "_id": f"u{i:03d}",
            "name": f"{first_name} {last_name}",
            "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "risk_profile": risk_profile,
            "currency": "EUR",
            "created_at": dt(RNG.randint(30, 720)),
        })
    return users


def generate_market_prices(days=365):
    market_prices = []
    latest_prices = {}

    for asset in ASSETS:
        price = asset["base_price"] * RNG.uniform(0.82, 1.12)
        volatility = {
            "crypto": 0.045,
            "action": 0.018,
            "etf": 0.010,
            "matiere_premiere": 0.014,
            "obligation": 0.004,
        }.get(asset["type"], 0.012)

        for days_ago in range(days, 0, -1):
            drift = RNG.uniform(-volatility, volatility)
            price = max(0.01, price * (1 + drift))
            market_prices.append({
                "_id": f"price_{asset['_id']}_{days_ago:03d}",
                "asset_id": asset["_id"],
                "price": round(price, 4 if price < 5 else 2),
                "currency": asset["currency"],
                "date": dt(days_ago),
            })
            if days_ago == 1:
                latest_prices[asset["_id"]] = round(price, 4 if price < 5 else 2)

    return market_prices, latest_prices


def generate_portfolios_and_transactions(users, latest_prices):
    portfolios = []
    transactions = []
    transaction_id = 1
    portfolio_id = 1

    for user in users:
        portfolio_count = 2 if user["_id"] != "u001" else 3

        for number in range(1, portfolio_count + 1):
            pid = f"p{portfolio_id:03d}"
            selected_ids = set()
            holdings = []
            risk_profile = user["risk_profile"]
            holding_count = RNG.randint(5, 10)

            if pid == "p001":
                forced_assets = ["cw8", "aapl", "btc", "msft", "eth", "gold", "sp500", "nvda"]
                for asset_id in forced_assets:
                    selected_ids.add(asset_id)
                    current_price = latest_prices[asset_id]
                    if asset_id == "btc":
                        quantity = 0.08
                    elif asset_id == "eth":
                        quantity = 1.5
                    elif current_price > 800:
                        quantity = RNG.randint(2, 8)
                    elif current_price > 200:
                        quantity = RNG.randint(8, 35)
                    else:
                        quantity = RNG.randint(20, 120)
                    holdings.append({
                        "asset_id": asset_id,
                        "quantity": round(quantity, 6),
                        "average_buy_price": round(current_price * RNG.uniform(0.78, 1.08), 2),
                    })
            else:
                while len(holdings) < holding_count:
                    asset = weighted_asset_choice(risk_profile, selected_ids)
                    selected_ids.add(asset["_id"])
                    current_price = latest_prices[asset["_id"]]
                    budget_line = RNG.uniform(400, 4500)
                    quantity = max(0.001, budget_line / current_price)
                    if asset["type"] in ["action", "etf", "obligation"]:
                        quantity = max(1, round(quantity))
                    else:
                        quantity = round(quantity, 6)

                    holdings.append({
                        "asset_id": asset["_id"],
                        "quantity": quantity,
                        "average_buy_price": round(current_price * RNG.uniform(0.75, 1.15), 2),
                    })

            cash = round(RNG.uniform(100, 6000), 2)
            portfolio_name = [
                "Portefeuille long terme",
                "Portefeuille croissance",
                "Portefeuille securise",
                "Portefeuille opportuniste",
                "Portefeuille ETF",
            ][(portfolio_id - 1) % 5]

            portfolios.append({
                "_id": pid,
                "user_id": user["_id"],
                "name": f"{portfolio_name} {number}",
                "cash": cash,
                "base_currency": "EUR",
                "created_at": dt(RNG.randint(60, 700)),
                "holdings": holdings,
            })

            for holding in holdings:
                buy_count = RNG.randint(3, 7)
                remaining_quantity = holding["quantity"]
                for buy_number in range(buy_count):
                    quantity = round(holding["quantity"] / buy_count * RNG.uniform(0.75, 1.25), 6)
                    if buy_number == buy_count - 1:
                        quantity = round(max(0.001, remaining_quantity), 6)
                    remaining_quantity = max(0, remaining_quantity - quantity)
                    transactions.append({
                        "_id": f"t{transaction_id:05d}",
                        "portfolio_id": pid,
                        "asset_id": holding["asset_id"],
                        "type": "buy",
                        "quantity": quantity,
                        "price": round(holding["average_buy_price"] * RNG.uniform(0.92, 1.08), 2),
                        "fees": round(RNG.uniform(0.50, 12.00), 2),
                        "date": dt(RNG.randint(20, 360)),
                    })
                    transaction_id += 1

                if RNG.random() < 0.35:
                    sell_quantity = round(holding["quantity"] * RNG.uniform(0.05, 0.25), 6)
                    transactions.append({
                        "_id": f"t{transaction_id:05d}",
                        "portfolio_id": pid,
                        "asset_id": holding["asset_id"],
                        "type": "sell",
                        "quantity": sell_quantity,
                        "price": round(latest_prices[holding["asset_id"]] * RNG.uniform(0.90, 1.10), 2),
                        "fees": round(RNG.uniform(0.50, 10.00), 2),
                        "date": dt(RNG.randint(1, 90)),
                    })
                    transaction_id += 1

            portfolio_id += 1

    return portfolios, transactions


def generate_alerts(users, latest_prices):
    alerts = []
    alert_id = 1

    for user in users:
        alert_count = RNG.randint(3, 6)
        selected_assets = RNG.sample(ASSETS, alert_count)
        for asset in selected_assets:
            condition = RNG.choice(["price_above", "price_below"])
            latest_price = latest_prices[asset["_id"]]

            # Environ 40 % des alertes sont volontairement deja declenchees pour la demo.
            if RNG.random() < 0.40:
                target_price = latest_price * RNG.uniform(0.85, 0.98) if condition == "price_above" else latest_price * RNG.uniform(1.02, 1.20)
            else:
                target_price = latest_price * RNG.uniform(1.02, 1.25) if condition == "price_above" else latest_price * RNG.uniform(0.75, 0.98)

            alerts.append({
                "_id": f"al{alert_id:04d}",
                "user_id": user["_id"],
                "asset_id": asset["_id"],
                "condition": condition,
                "target_price": round(target_price, 4 if target_price < 5 else 2),
                "active": RNG.random() < 0.85,
                "created_at": dt(RNG.randint(1, 180)),
            })
            alert_id += 1

    return alerts


def seed_database():
    db = get_db()
    for name in ["users", "assets", "portfolios", "transactions", "market_prices", "alerts"]:
        db[name].delete_many({})

    users = generate_users()
    assets = clean_assets()
    market_prices, latest_prices = generate_market_prices(days=365)
    portfolios, transactions = generate_portfolios_and_transactions(users, latest_prices)
    alerts = generate_alerts(users, latest_prices)

    db.users.insert_many(users)
    db.assets.insert_many(assets)
    db.portfolios.insert_many(portfolios)
    db.transactions.insert_many(transactions)
    db.market_prices.insert_many(market_prices)
    db.alerts.insert_many(alerts)

    db.users.create_index("email", unique=True)
    db.assets.create_index("symbol", unique=True)
    db.portfolios.create_index("user_id")
    db.transactions.create_index([("portfolio_id", 1), ("date", -1)])
    db.transactions.create_index([("asset_id", 1), ("date", -1)])
    db.market_prices.create_index([("asset_id", 1), ("date", -1)])
    db.alerts.create_index([("user_id", 1), ("active", 1)])
    db.alerts.create_index([("asset_id", 1), ("active", 1)])

    return {
        "users": len(users),
        "assets": len(assets),
        "portfolios": len(portfolios),
        "transactions": len(transactions),
        "market_prices": len(market_prices),
        "alerts": len(alerts),
    }


if __name__ == "__main__":
    print(seed_database())
