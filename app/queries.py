from datetime import datetime, timedelta, timezone
from bson import json_util
from app.db import get_db


def serialize(data):
    return json_util.loads(json_util.dumps(data))


def latest_price_stage():
    return [
        {"$lookup": {
            "from": "market_prices",
            "let": {"assetId": "$holdings.asset_id"},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$asset_id", "$$assetId"]}}},
                {"$sort": {"date": -1}},
                {"$limit": 1},
            ],
            "as": "latest_price",
        }},
        {"$unwind": "$latest_price"},
    ]


def get_users():
    return serialize(list(get_db().users.find({}, {"email": 0}).sort("name", 1)))


def get_assets():
    return serialize(list(get_db().assets.find({}).sort("symbol", 1)))


def portfolio_summary(portfolio_id):
    db = get_db()
    pipeline = [
        {"$match": {"_id": portfolio_id}},
        {"$unwind": "$holdings"},
        *latest_price_stage(),
        {"$lookup": {"from": "assets", "localField": "holdings.asset_id", "foreignField": "_id", "as": "asset"}},
        {"$unwind": "$asset"},
        {"$addFields": {
            "line_value": {"$multiply": ["$holdings.quantity", "$latest_price.price"]},
            "invested": {"$multiply": ["$holdings.quantity", "$holdings.average_buy_price"]},
        }},
        {"$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "user_id": {"$first": "$user_id"},
            "cash": {"$first": "$cash"},
            "positions_value": {"$sum": "$line_value"},
            "invested_total": {"$sum": "$invested"},
            "positions": {"$push": {
                "symbol": "$asset.symbol",
                "name": "$asset.name",
                "type": "$asset.type",
                "quantity": "$holdings.quantity",
                "average_buy_price": "$holdings.average_buy_price",
                "current_price": "$latest_price.price",
                "value": "$line_value",
                "unrealized_gain": {"$subtract": ["$line_value", "$invested"]},
            }},
        }},
        {"$addFields": {
            "total_value": {"$add": ["$positions_value", "$cash"]},
            "unrealized_gain_total": {"$subtract": ["$positions_value", "$invested_total"]},
        }},
    ]
    result = list(db.portfolios.aggregate(pipeline))
    return serialize(result[0] if result else {})


def all_portfolios_value():
    db = get_db()
    pipeline = [
        {"$unwind": "$holdings"},
        *latest_price_stage(),
        {"$addFields": {"line_value": {"$multiply": ["$holdings.quantity", "$latest_price.price"]}}},
        {"$group": {"_id": "$_id", "name": {"$first": "$name"}, "user_id": {"$first": "$user_id"}, "cash": {"$first": "$cash"}, "positions_value": {"$sum": "$line_value"}}},
        {"$addFields": {"total_value": {"$add": ["$positions_value", "$cash"]}}},
        {"$sort": {"total_value": -1}},
    ]
    return serialize(list(db.portfolios.aggregate(pipeline)))


def allocation_by_type(portfolio_id):
    db = get_db()
    pipeline = [
        {"$match": {"_id": portfolio_id}},
        {"$unwind": "$holdings"},
        *latest_price_stage(),
        {"$lookup": {"from": "assets", "localField": "holdings.asset_id", "foreignField": "_id", "as": "asset"}},
        {"$unwind": "$asset"},
        {"$addFields": {"value": {"$multiply": ["$holdings.quantity", "$latest_price.price"]}}},
        {"$group": {"_id": "$asset.type", "value": {"$sum": "$value"}}},
        {"$sort": {"value": -1}},
    ]
    return serialize(list(db.portfolios.aggregate(pipeline)))


def allocation_by_sector(portfolio_id):
    db = get_db()
    pipeline = [
        {"$match": {"_id": portfolio_id}},
        {"$unwind": "$holdings"},
        *latest_price_stage(),
        {"$lookup": {"from": "assets", "localField": "holdings.asset_id", "foreignField": "_id", "as": "asset"}},
        {"$unwind": "$asset"},
        {"$addFields": {"value": {"$multiply": ["$holdings.quantity", "$latest_price.price"]}}},
        {"$group": {"_id": "$asset.sector", "value": {"$sum": "$value"}}},
        {"$sort": {"value": -1}},
    ]
    return serialize(list(db.portfolios.aggregate(pipeline)))


def transactions_by_portfolio(portfolio_id, limit=10):
    db = get_db()
    pipeline = [
        {"$match": {"portfolio_id": portfolio_id}},
        {"$lookup": {"from": "assets", "localField": "asset_id", "foreignField": "_id", "as": "asset"}},
        {"$unwind": "$asset"},
        {"$sort": {"date": -1}},
        {"$limit": int(limit)},
        {"$project": {"asset_id": 0}},
    ]
    return serialize(list(db.transactions.aggregate(pipeline)))


def average_buy_price(portfolio_id):
    db = get_db()
    pipeline = [
        {"$match": {"portfolio_id": portfolio_id, "type": "buy"}},
        {"$group": {"_id": "$asset_id", "total_qty": {"$sum": "$quantity"}, "total_cost": {"$sum": {"$multiply": ["$quantity", "$price"]}}}},
        {"$lookup": {"from": "assets", "localField": "_id", "foreignField": "_id", "as": "asset"}},
        {"$unwind": "$asset"},
        {"$project": {"symbol": "$asset.symbol", "average_buy_price": {"$divide": ["$total_cost", "$total_qty"]}, "total_qty": 1, "total_cost": 1}},
        {"$sort": {"symbol": 1}},
    ]
    return serialize(list(db.transactions.aggregate(pipeline)))


def monthly_investments():
    db = get_db()
    pipeline = [
        {"$match": {"type": "buy"}},
        {"$group": {
            "_id": {"year": {"$year": "$date"}, "month": {"$month": "$date"}},
            "amount": {"$sum": {"$multiply": ["$quantity", "$price"]}},
            "fees": {"$sum": "$fees"},
        }},
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]
    return serialize(list(db.transactions.aggregate(pipeline)))


def top_assets_global():
    db = get_db()
    pipeline = [
        {"$unwind": "$holdings"},
        *latest_price_stage(),
        {"$lookup": {"from": "assets", "localField": "holdings.asset_id", "foreignField": "_id", "as": "asset"}},
        {"$unwind": "$asset"},
        {"$addFields": {"value": {"$multiply": ["$holdings.quantity", "$latest_price.price"]}}},
        {"$group": {"_id": "$asset.symbol", "name": {"$first": "$asset.name"}, "total_value": {"$sum": "$value"}, "total_quantity": {"$sum": "$holdings.quantity"}}},
        {"$sort": {"total_value": -1}},
    ]
    return serialize(list(db.portfolios.aggregate(pipeline)))


def price_history(asset_id):
    return serialize(list(get_db().market_prices.find({"asset_id": asset_id}).sort("date", 1)))


def search_assets(keyword):
    regex = {"$regex": keyword, "$options": "i"}
    return serialize(list(get_db().assets.find({"$or": [{"symbol": regex}, {"name": regex}, {"sector": regex}, {"type": regex}]})))


def active_alerts(user_id=None):
    query = {"active": True}
    if user_id:
        query["user_id"] = user_id
    db = get_db()
    pipeline = [
        {"$match": query},
        {"$lookup": {"from": "assets", "localField": "asset_id", "foreignField": "_id", "as": "asset"}},
        {"$unwind": "$asset"},
        {"$lookup": {
            "from": "market_prices",
            "let": {"assetId": "$asset_id"},
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$asset_id", "$$assetId"]}}},
                {"$sort": {"date": -1}},
                {"$limit": 1},
            ],
            "as": "latest_price",
        }},
        {"$unwind": "$latest_price"},
    ]
    return serialize(list(db.alerts.aggregate(pipeline)))


def triggered_alerts():
    alerts = active_alerts()
    triggered = []
    for alert in alerts:
        price = alert["latest_price"]["price"]
        target = alert["target_price"]
        condition = alert["condition"]
        is_triggered = (condition == "price_above" and price >= target) or (condition == "price_below" and price <= target)
        if is_triggered:
            triggered.append(alert)
    return serialize(triggered)


def users_by_risk_profile():
    db = get_db()
    pipeline = [
        {"$group": {"_id": "$risk_profile", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    return serialize(list(db.users.aggregate(pipeline)))


def diversification_score(portfolio_id):
    db = get_db()
    portfolio = db.portfolios.find_one({"_id": portfolio_id})
    if not portfolio:
        return {}
    asset_count = len(portfolio.get("holdings", []))
    types = set()
    sectors = set()
    for holding in portfolio.get("holdings", []):
        asset = db.assets.find_one({"_id": holding["asset_id"]})
        if asset:
            types.add(asset.get("type"))
            sectors.add(asset.get("sector"))
    score = min(100, asset_count * 15 + len(types) * 20 + len(sectors) * 10)
    return serialize({"portfolio_id": portfolio_id, "asset_count": asset_count, "asset_types": list(types), "sectors": list(sectors), "score": score})


def portfolios_above_value(min_value):
    portfolios = all_portfolios_value()
    return serialize([p for p in portfolios if p.get("total_value", 0) >= float(min_value)])
