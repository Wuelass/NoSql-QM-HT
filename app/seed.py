from datetime import datetime, timedelta, timezone
from app.db import get_db

UTC = timezone.utc


def dt(days_ago: int) -> datetime:
    return datetime.now(UTC) - timedelta(days=days_ago)


def seed_database():
    db = get_db()
    for name in ["users", "assets", "portfolios", "transactions", "market_prices", "alerts"]:
        db[name].delete_many({})

    users = [
        {
            "_id": "u001",
            "name": "Lina Martin",
            "email": "lina@example.com",
            "risk_profile": "modere",
            "currency": "EUR",
            "created_at": dt(180),
        },
        {
            "_id": "u002",
            "name": "Adam Bernard",
            "email": "adam@example.com",
            "risk_profile": "dynamique",
            "currency": "EUR",
            "created_at": dt(120),
        },
        {
            "_id": "u003",
            "name": "Sarah Petit",
            "email": "sarah@example.com",
            "risk_profile": "prudent",
            "currency": "EUR",
            "created_at": dt(70),
        },
    ]

    assets = [
        {"_id": "aapl", "symbol": "AAPL", "name": "Apple", "type": "action", "sector": "Technologie", "currency": "USD"},
        {"_id": "msft", "symbol": "MSFT", "name": "Microsoft", "type": "action", "sector": "Technologie", "currency": "USD"},
        {"_id": "btc", "symbol": "BTC", "name": "Bitcoin", "type": "crypto", "sector": "Crypto", "currency": "USD"},
        {"_id": "eth", "symbol": "ETH", "name": "Ethereum", "type": "crypto", "sector": "Crypto", "currency": "USD"},
        {"_id": "cw8", "symbol": "CW8", "name": "Amundi MSCI World", "type": "etf", "sector": "ETF Monde", "currency": "EUR"},
    ]

    portfolios = [
        {
            "_id": "p001",
            "user_id": "u001",
            "name": "Portefeuille long terme",
            "cash": 1200.00,
            "base_currency": "EUR",
            "created_at": dt(170),
            "holdings": [
                {"asset_id": "cw8", "quantity": 20, "average_buy_price": 430.00},
                {"asset_id": "aapl", "quantity": 10, "average_buy_price": 170.00},
                {"asset_id": "btc", "quantity": 0.05, "average_buy_price": 55000.00},
            ],
        },
        {
            "_id": "p002",
            "user_id": "u002",
            "name": "Portefeuille croissance",
            "cash": 500.00,
            "base_currency": "EUR",
            "created_at": dt(100),
            "holdings": [
                {"asset_id": "msft", "quantity": 8, "average_buy_price": 390.00},
                {"asset_id": "eth", "quantity": 1.3, "average_buy_price": 3100.00},
                {"asset_id": "btc", "quantity": 0.03, "average_buy_price": 60000.00},
            ],
        },
        {
            "_id": "p003",
            "user_id": "u003",
            "name": "Portefeuille securise",
            "cash": 2500.00,
            "base_currency": "EUR",
            "created_at": dt(60),
            "holdings": [
                {"asset_id": "cw8", "quantity": 7, "average_buy_price": 420.00},
                {"asset_id": "msft", "quantity": 2, "average_buy_price": 370.00},
            ],
        },
    ]

    transactions = [
        {"_id": "t001", "portfolio_id": "p001", "asset_id": "cw8", "type": "buy", "quantity": 20, "price": 430.00, "fees": 2.00, "date": dt(160)},
        {"_id": "t002", "portfolio_id": "p001", "asset_id": "aapl", "type": "buy", "quantity": 10, "price": 170.00, "fees": 1.50, "date": dt(130)},
        {"_id": "t003", "portfolio_id": "p001", "asset_id": "btc", "type": "buy", "quantity": 0.05, "price": 55000.00, "fees": 8.00, "date": dt(90)},
        {"_id": "t004", "portfolio_id": "p002", "asset_id": "msft", "type": "buy", "quantity": 8, "price": 390.00, "fees": 1.70, "date": dt(80)},
        {"_id": "t005", "portfolio_id": "p002", "asset_id": "eth", "type": "buy", "quantity": 1.3, "price": 3100.00, "fees": 7.50, "date": dt(75)},
        {"_id": "t006", "portfolio_id": "p002", "asset_id": "btc", "type": "buy", "quantity": 0.03, "price": 60000.00, "fees": 6.00, "date": dt(50)},
        {"_id": "t007", "portfolio_id": "p003", "asset_id": "cw8", "type": "buy", "quantity": 7, "price": 420.00, "fees": 1.00, "date": dt(45)},
        {"_id": "t008", "portfolio_id": "p003", "asset_id": "msft", "type": "buy", "quantity": 2, "price": 370.00, "fees": 1.20, "date": dt(35)},
        {"_id": "t009", "portfolio_id": "p001", "asset_id": "aapl", "type": "sell", "quantity": 2, "price": 195.00, "fees": 1.30, "date": dt(20)},
    ]

    market_prices = [
        {"_id": "price_cw8", "asset_id": "cw8", "price": 470.00, "currency": "EUR", "date": dt(1)},
        {"_id": "price_aapl", "asset_id": "aapl", "price": 210.00, "currency": "USD", "date": dt(1)},
        {"_id": "price_msft", "asset_id": "msft", "price": 455.00, "currency": "USD", "date": dt(1)},
        {"_id": "price_btc", "asset_id": "btc", "price": 68000.00, "currency": "USD", "date": dt(1)},
        {"_id": "price_eth", "asset_id": "eth", "price": 3500.00, "currency": "USD", "date": dt(1)},
        {"_id": "price_cw8_old", "asset_id": "cw8", "price": 455.00, "currency": "EUR", "date": dt(30)},
        {"_id": "price_btc_old", "asset_id": "btc", "price": 65000.00, "currency": "USD", "date": dt(30)},
    ]

    alerts = [
        {"_id": "al001", "user_id": "u001", "asset_id": "btc", "condition": "price_above", "target_price": 70000, "active": True, "created_at": dt(25)},
        {"_id": "al002", "user_id": "u002", "asset_id": "eth", "condition": "price_below", "target_price": 3000, "active": True, "created_at": dt(15)},
        {"_id": "al003", "user_id": "u003", "asset_id": "cw8", "condition": "price_above", "target_price": 480, "active": False, "created_at": dt(10)},
    ]

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
    db.market_prices.create_index([("asset_id", 1), ("date", -1)])
    db.alerts.create_index([("user_id", 1), ("active", 1)])

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
