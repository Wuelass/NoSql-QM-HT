# FinanceTrack — Projet MongoDB NoSQL

Projet scolaire sur le thème : **Applications de finance et d'investissement**.

## Fonctionnalités

- Base MongoDB avec utilisateurs, portefeuilles, actifs, transactions, prix de marché et alertes.
- Script de remplissage de la base.
- API Flask avec plus de 15 endpoints.
- Page web simple pour tester les requêtes.
- Rapport complet dans `docs/rapport_projet.md`.

## Installation avec Docker

```bash
docker compose up --build
```

Puis ouvrir :

```txt
http://localhost:5000
```

Cliquer sur **Remplir la base** avant de tester les requêtes.

## Installation sans Docker

Il faut avoir MongoDB installé et lancé localement.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed
python -m app.main
```

Sur Linux/Mac :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed
python -m app.main
```

## Endpoints principaux

```txt
GET  /api/users
GET  /api/assets
GET  /api/portfolios/value
GET  /api/portfolio/p001/summary
GET  /api/portfolio/p001/allocation/type
GET  /api/portfolio/p001/allocation/sector
GET  /api/portfolio/p001/transactions
GET  /api/portfolio/p001/average-buy-price
GET  /api/investments/monthly
GET  /api/assets/top
GET  /api/asset/btc/prices
GET  /api/assets/search?q=btc
GET  /api/alerts/active
GET  /api/alerts/triggered
GET  /api/users/risk-profiles
GET  /api/portfolio/p001/diversification
GET  /api/portfolios/above/8000
```

## Structure

```txt
finance_investment_nosql_project/
├── app/
│   ├── db.py
│   ├── main.py
│   ├── queries.py
│   ├── seed.py
│   ├── static/style.css
│   └── templates/index.html
├── docs/rapport_projet.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Démonstration orale rapide

1. Expliquer le thème : application de finance et d'investissement.
2. Expliquer pourquoi MongoDB : documents souples, holdings imbriqués, API JSON.
3. Montrer les collections MongoDB.
4. Montrer la page web.
5. Cliquer sur plusieurs requêtes.
6. Montrer une requête d'agrégation dans `app/queries.py`.
7. Conclure sur l'intérêt de NoSQL.
