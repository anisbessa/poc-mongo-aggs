from datetime import datetime, timezone
from pymongo import MongoClient
import json

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['poc']
collection = db['tradeHisto10']

# Votre nouvelle agrégation
aggregation_pipeline = [
    {
        '$project': {
            'classification': '$classificationMap.classification1.levelClass1',
            'lastFlow': {
                '$arrayElemAt': [
                    {
                        '$filter': {
                            'input': {
                                '$sortArray': {
                                    'input': '$flows',
                                    'sortBy': {
                                        'flowDate': -1
                                    }
                                }
                            },
                            'cond': {
                                '$lt': [
                                    '$$flow.flowDate', datetime(2024, 12, 4, 15, 53, 32, tzinfo=timezone.utc)
                                ]
                            },
                            'as': 'flow',
                            'limit': 1
                        }
                    }, 0
                ]
            }
        }
    }, {
        '$group': {
            '_id': '$classification',
            'totalRemainingNominal': {
                '$sum': '$lastFlow.remainingNominal'
            }
        }
    }
]

# Mesurer le temps d'exécution
start_time = datetime.now()

# Exécution de l'agrégation
result = list(collection.aggregate(aggregation_pipeline))

# Calculer le temps d'exécution en millisecondes
execution_time = (datetime.now() - start_time).total_seconds() * 1000

# Fermeture de la connexion à la base de données MongoDB
client.close()

# Écriture du résultat dans un fichier de sortie
output_file_path = 'output.json'
with open(output_file_path, 'w') as output_file:
    json.dump(result, output_file, default=str, indent=2)

# Impression du temps d'exécution sur la sortie standard
print(f"Résultat de l'agrégation écrit dans {output_file_path}")
print(f"Temps d'exécution : {execution_time} ms")
