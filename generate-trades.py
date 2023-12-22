import json
from datetime import datetime, timedelta
from faker import Faker
import random
from pymongo import MongoClient

fake = Faker()

# Remplacez les informations appropriées pour votre base de données MongoDB locale
mongo_uri = "mongodb://localhost:27017/"
database_name = "poc"
collection_name = "tradeHisto12"  # Modification ici

def generate_classification_values():
    return {
        "levelClass1": fake.word(),
        "levelClass2": fake.word(),
        "LevelClass3": fake.word()
    }

def generate_trade(trade_id, classification_map, snapshot_date):
    trade_date = fake.date_between_dates(date_start=datetime.now() - timedelta(days=365), date_end=datetime.now())

    maturity_date = trade_date + timedelta(days=2*365)

    trade = {
        "_id": str(fake.uuid4()),  # Modification ici
        "tradeId": str(trade_id),
        "tradeDate": datetime.combine(trade_date, datetime.min.time()),
        "snapshotDate": datetime.combine(snapshot_date, datetime.min.time()),
        "nominal": random.randint(10000, 100000),
        "companyId": str(fake.uuid4()),  # Modification ici
        "counterpartyId": str(fake.uuid4()),  # Modification ici
        "currency": fake.currency_code(),
        "mirrorTradeId": random.randint(100000, 999999),
        "maturityDate": datetime.combine(maturity_date, datetime.min.time()),
        "classificationMap": {classification_key: generate_classification_values() for classification_key in classification_map},
        "flows": generate_flows(trade_date, maturity_date),
        "riskMetrics": generate_metrics(),
        "liquidityMetrics": generate_metrics()
    }

    return trade

def generate_flows(trade_date, maturity_date):
    flows = []
    remaining_nominal = 0
    num_flows = 7

    for i in range(num_flows):
        flow_date = trade_date + timedelta(days=int((maturity_date - trade_date).days * i / num_flows))

        flow_amount = random.randint(100, 5000)
        remaining_nominal += flow_amount

        flow = {
            "flowDate": datetime.combine(flow_date, datetime.min.time()),
            "flowAmount": flow_amount,
            "remainingNominal": remaining_nominal
        }

        flows.append(flow)

    return flows

def generate_metrics():
    return {
        "_id": str(fake.uuid4()),
        "tradeId": str(fake.uuid4()),
        "metric1": random.uniform(1, 100),
        "metric2": random.uniform(1, 100)
    }

def generate_classification_map():
    classification_map = {}
    num_classifications = 10
    num_levels = 3

    for i in range(1, num_classifications + 1):
        classification_key = f"classification{i}"
        classification_map[classification_key] = {
            "levelClass1": fake.word(),
            "levelClass2": fake.word(),
            "LevelClass3": fake.word()
        }

    return classification_map

def insert_trades_to_mongo(trades, collection):
    collection.insert_many(trades)

def generate_and_insert_trades(snapshot_dates):
    # Générer 200 trades pour chaque snapshotDate
    num_trades = 100000
    classification_map = generate_classification_map()
    trades = []

    for snapshot_date in snapshot_dates:
        snapshot_date = datetime.strptime(snapshot_date, "%Y-%m-%d")
        trades.extend([generate_trade(trade_id, classification_map, snapshot_date) for trade_id in range(1, num_trades + 1)])

    # Connectez-vous à la base de données MongoDB
    client = MongoClient(mongo_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Insérez les trades par bloc de 100
    block_size = 100
    for i in range(0, len(trades), block_size):
        block = trades[i:i + block_size]
        insert_trades_to_mongo(block, collection)
        print(f"Inseré un bloc de {block_size} trades. Total inséré: {i + block_size}/{len(trades)}")

    # Fermez la connexion à la base de données MongoDB
    client.close()

# Générer les snapshotDates pour les 220 derniers jours
today = datetime.now()
snapshot_dates = [(today - timedelta(days=d)).strftime("%Y-%m-%d") for d in range(1)]

# Générer et insérer les trades pour chaque snapshotDate
generate_and_insert_trades(snapshot_dates)
