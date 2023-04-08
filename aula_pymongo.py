from pprint import pprint
from senha import senha
from pymongo import MongoClient

senha = senha()

client = MongoClient("mongodb+srv://teste:"+senha+"@cluster0.fsqyeqp.mongodb.net/?retryWrites=true&w=majority")
db = client.test

#criando a coleção clientes
'''
def criandoAColecao():


    db.create_collection("clientes")

criandoAColecao()
'''

collection = db.test_collection
print(db.list_collection_names())


# acessa a coleção "clientes"
clientes = db['clientes']
'''
# cria um documento de cliente
cliente = {
    "name": "Guilherme",
    "cpf": "123456789-11",
    "endereco": "Rua de casa",
    "contas": [
        {
            "tipo": "corrente",
            "agencia": "001",
            "numero": 1,
            "saldo": 500.10
        }
    ]
}


clientes.insert_one(cliente)


joao = {
    "name": "João",
    "cpf": "123654987-66",
    "endereco": "Rua B",
    "contas": [
        {
            "tipo": "corrente",
            "agencia": "001",
            "numero": 2,
            "saldo": 600.10
        }
    ]
}

regina = {
    "name": "Regina",
    "cpf": "7895423211-11",
    "endereco": "Rua B",
    "contas": [
        {
            "tipo": "corrente",
            "agencia": "003",
            "numero": 3,
            "saldo": 1500.10
        }
    ]
}

clientes.insert_many([joao, regina])
'''
for cliente in clientes.find():
    print(f' id= {cliente["_id"]} nome = {cliente["name"]}')
