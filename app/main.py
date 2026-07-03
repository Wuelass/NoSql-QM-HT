from flask import Flask, jsonify, render_template, request
from app.seed import seed_database
import app.queries as q

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/seed", methods=["POST", "GET"])
def seed():
    return jsonify(seed_database())


@app.route("/api/users")
def users():
    return jsonify(q.get_users())


@app.route("/api/assets")
def assets():
    return jsonify(q.get_assets())


@app.route("/api/portfolios/value")
def portfolios_value():
    return jsonify(q.all_portfolios_value())


@app.route("/api/portfolio/<portfolio_id>/summary")
def portfolio_summary(portfolio_id):
    return jsonify(q.portfolio_summary(portfolio_id))


@app.route("/api/portfolio/<portfolio_id>/allocation/type")
def allocation_type(portfolio_id):
    return jsonify(q.allocation_by_type(portfolio_id))


@app.route("/api/portfolio/<portfolio_id>/allocation/sector")
def allocation_sector(portfolio_id):
    return jsonify(q.allocation_by_sector(portfolio_id))


@app.route("/api/portfolio/<portfolio_id>/transactions")
def transactions(portfolio_id):
    limit = request.args.get("limit", 10)
    return jsonify(q.transactions_by_portfolio(portfolio_id, limit))


@app.route("/api/portfolio/<portfolio_id>/average-buy-price")
def average_buy_price(portfolio_id):
    return jsonify(q.average_buy_price(portfolio_id))


@app.route("/api/investments/monthly")
def monthly_investments():
    return jsonify(q.monthly_investments())


@app.route("/api/assets/top")
def top_assets():
    return jsonify(q.top_assets_global())


@app.route("/api/asset/<asset_id>/prices")
def price_history(asset_id):
    return jsonify(q.price_history(asset_id))


@app.route("/api/assets/search")
def search_assets():
    keyword = request.args.get("q", "")
    return jsonify(q.search_assets(keyword))


@app.route("/api/alerts/active")
def active_alerts():
    user_id = request.args.get("user_id")
    return jsonify(q.active_alerts(user_id))


@app.route("/api/alerts/triggered")
def triggered_alerts():
    return jsonify(q.triggered_alerts())


@app.route("/api/users/risk-profiles")
def users_risk_profiles():
    return jsonify(q.users_by_risk_profile())


@app.route("/api/portfolio/<portfolio_id>/diversification")
def diversification(portfolio_id):
    return jsonify(q.diversification_score(portfolio_id))


@app.route("/api/portfolios/above/<min_value>")
def portfolios_above(min_value):
    return jsonify(q.portfolios_above_value(min_value))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
