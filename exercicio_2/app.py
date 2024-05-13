from flask import Flask, request
from flask_pymongo import PyMongo
import os

app = Flask("nome_da_minha_aplicacao")
app.config["MONGO_URI"] = os.getenv("string_conexao_MongoDB_biblioteca")
mongo = PyMongo(app)

#aNOTAÇÕES SOBRE ENBEDING MONGODB

@app.route('/clientes', methods=['POST'])
def adicionar_cliente():
    usuario = request.json
    nome = usuario.get("nome", "")
    email = usuario.get("email", "")
    cpf = usuario.get("cpf", "")
    senha = usuario.get("senha", "")

    if not nome or not email or not cpf or not senha:
        return {"error": "Id, nome, cpf e data de nascimento são obrigatórios"}, 400
    
    if mongo.db.clientes_exemplo.find_one(filter={"cpf": cpf}):
        return {"error": "CPF já existe"}, 409
    
    novo_usuario = {
        "nome": nome,
        "email": email,
        "cpf": cpf,
        "senha": senha
    }

    try:
        mongo.db.clientes_exemplo.insert_one(novo_usuario)
    except:
        return {"error": "Dados inválidos"}, 400

    return {"mensagem": "Usuário adicionado com sucesso"}, 201


#CRUD PEDIDOS

@app.route('/pedidos/<string:nome_cliente>', methods=['POST'])
def cadastrar_pedidos(nome_cliente):
    emprestimo = request.json
    nome_cliente = nome_cliente
    data_hora = emprestimo.get("data_hora", "")
    valortotal = emprestimo.get("valortotal", "")
    status = emprestimo.get("status", "")

    if not data_hora or not valortotal or not status:
        return {"error": "Id, id do usuário, id da bicicleta e data do aluguel são obrigatórios"}, 400
    
    novo_emprestimo = {
        "data_hora": data_hora,
        "valortotal": valortotal,
        "status": status
    }

    try:
        if "pedidos" in mongo.db.clientes_exemplo.find_one({"nome": nome_cliente}):
            mongo.db.clientes_exemplo.update_one({"nome": nome_cliente}, {"$push": {"pedidos": novo_emprestimo}})
        else:
            mongo.db.clientes_exemplo.update_one({"nome": nome_cliente}, {"$addToSet": {"pedidos": novo_emprestimo}})

        mongo.db.pedidos_exemplo.insert_one(novo_emprestimo)
    except:
        return {"error": "Dados inválidos"}, 400

    return {"mensagem": "Bicicleta adicionado com sucesso"}, 201


@app.route('/pedidos/<string:data_hora>', methods=['DELETE'])
def deletar_pedido(data_hora):
    try:
        filtro = {"data_hora": data_hora}
        dados_emprestimo = list(mongo.db.pedidos_exemplo.find(filtro))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_emprestimo:
            try:
                mongo.db.pedidos_exemplo.delete_one(filtro)
                mongo.db.clientes_exemplo.update_one({'pedidos.data_hora': data_hora}, {'$pull': {'pedidos':{'data_hora': data_hora}}})
            except:
                return {"erro": "Dados inválidos"}, 400
    
            return {"mensagem": "Empréstimo deletado com sucesso"}, 200
        else:
            return {"erro": "Empréstimo não encontrada"}, 404

# Para atualizar um pedido dentro de um enbeding usamos update_one({id: id, pedido.id: id_pedido}, {$set: {pedido.$.data_hora: nova_data_hora}})

if __name__ == '__main__':
    app.run(debug=True)