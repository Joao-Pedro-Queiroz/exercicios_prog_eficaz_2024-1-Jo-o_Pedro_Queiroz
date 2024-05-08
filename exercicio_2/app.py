from flask import Flask, request
from flask_pymongo import PyMongo
import os

app = Flask("nome_da_minha_aplicacao")
app.config["MONGO_URI"] = os.getenv("string_conexao_MongoDB_biblioteca")
mongo = PyMongo(app)


@app.route('/usuarios', methods=['POST'])
def adicionar_usuario():
    usuario = request.json
    id = usuario.get("id", "")
    nome = usuario.get("nome", "")
    cpf = usuario.get("cpf", "")
    data_nascimento = usuario.get("data_nascimento", "")

    if not id or not nome or not cpf or not data_nascimento:
        return {"error": "Id, nome, cpf e data de nascimento são obrigatórios"}, 400
    
    if mongo.db.usuarios_aps_5.find_one(filter={"id": id}):
        return {"error": "Id já existe"}, 409
    
    if mongo.db.usuarios_aps_5.find_one(filter={"cpf": cpf}):
        return {"error": "CPF já existe"}, 409
    
    novo_usuario = {
        "id": id,
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento
    }

    try:
        mongo.db.usuarios_aps_5.insert_one(novo_usuario)
    except:
        return {"error": "Dados inválidos"}, 400

    return {"mensagem": "Usuário adicionado com sucesso"}, 201


@app.route('/usuarios', methods=['GET'])
def get_all_users():
    try:
        filtro = {}
        projecao = {"_id": 0}
        dados_usuarios = mongo.db.usuarios_aps_5.find(filtro, projecao)
    except:
        return {"error": "Erro no sistema"}, 500

    resp = {
        "usuarios": list(dados_usuarios)
    }

    return resp, 200


@app.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    try:
        filtro = {"id": id}
        projecao = {"_id": 0}
        dados_usuario = list(mongo.db.usuarios_aps_5.find(filtro, projecao))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_usuario:
            return {"usuarios": list(dados_usuario)}, 200
        else:
            return {"erro": "Usuário não encontrado"}, 404


@app.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    try:
        filtro = {"id": id}
        cursor = mongo.db.usuarios_aps_5.find(filtro)
        dados_usuarios = list(cursor)
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if len(dados_usuarios) == 0:
            return {"erro": "Usuário não encontrado"}, 404
        else:
            data = request.json
            nome = data.get("nome", "")
            cpf = data.get("cpf", "")
            data_nascimento = data.get("data_nascimento", "")
            dados = {}
            
            if nome:
                dados["nome"] = nome

            if cpf:
                dados["cpf"] = cpf

            if data_nascimento:
                dados["data_nascimento"] = data_nascimento

            novos_dados = {
                "$set": dados
            }

            try:
                mongo.db.usuarios_aps_5.update_one(filtro, novos_dados)
            except:
                return {"erro": "Dados inválidos"}, 400

            return {"mensagem": "Usuário atualizado com sucesso"}, 200


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    try:
        filtro = {"id": id}
        dados_usuario = list(mongo.db.usuarios_aps_5.find(filtro))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_usuario:
            try:
                mongo.db.usuarios_aps_5.delete_one(filtro)
            except:
                return {"erro": "Dados inválidos"}, 400
            
            return {"mensagem": "Usuário deletado com sucesso"}, 200
        else:
            return {"erro": "Usuário não encontrado"}, 404

#CRUD BIKES

@app.route('/bikes', methods=['POST'])
def adicionar_bicicleta():
    bicicleta = request.json
    id = bicicleta.get("id")
    marca = bicicleta.get("marca", "")
    modelo = bicicleta.get("modelo", "")
    cidade_alocada = bicicleta.get("cidade_alocada", "")
    status = "disponível"

    if not id or not marca or not modelo or not cidade_alocada:
        return {"error": "Id, marca, modelo e cidade alocada são obrigatórios"}, 400
    
    if mongo.db.bicicletas_aps_5.find_one({"id": id}):
        return {"error": "Id já existe"}, 409
    
    nova_bicicleta = {
        "id": id,
        "marca": marca,
        "modelo": modelo,
        "cidade_alocada": cidade_alocada,
        "status": status
    }

    try:
        mongo.db.bicicletas_aps_5.insert_one(nova_bicicleta)
    except:
        return {"error": "Dados inválidos"}, 400

    return {"mensagem": "Bicicleta adicionado com sucesso"}, 201


@app.route('/bikes', methods=['GET'])
def get_all_bikes():
    try:
        filtro = {}
        projecao = {"_id": 0}
        dados_bicicletas = mongo.db.bicicletas_aps_5.find(filtro, projecao)
    except:
        return {"error": "Erro no sistema"}, 500
    
    resp = {
        "bicicletas": list(dados_bicicletas)
    }

    return resp, 200

@app.route('/bikes/<int:id>', methods=['GET'])
def obter_bicicleta(id):
    try:
        filtro = {"id": id}
        projecao = {"_id": 0}
        dados_bicicleta = list(mongo.db.bicicletas_aps_5.find(filtro, projecao))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_bicicleta:
            return {"bicicletas": list(dados_bicicleta)}, 200
        else:
            return {"erro": "Bicicleta não encontrada"}, 404

@app.route('/bikes/<int:id>', methods=['PUT'])
def editar_bicicleta(id):
    try:
        filtro = {"id": id}
        cursor = mongo.db.bicicletas_aps_5.find(filtro)
        dados_bicicletas = list(cursor)
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if len(dados_bicicletas) == 0:
            return {"erro": "Bicicleta não encontrada"}, 404
        else:
            data = request.json
            marca = data.get("marca", "")
            modelo = data.get("modelo", "")
            cidade_alocada = data.get("cidade_alocada", "")
            status = data.get("status", "")
            dados = {}
            
            if marca:
                dados["marca"] = marca

            if modelo:
                dados["modelo"] = modelo

            if cidade_alocada:
                dados["cidade_alocada"] = cidade_alocada

            if status == "disponível" or status == "em uso":
                dados["status"] = status
            else:
                return {"erro": "Status inválido"}, 400

            novos_dados = {
                "$set": dados
            }

            try:
                mongo.db.bicicletas_aps_5.update_one(filtro, novos_dados)
            except:
                return {"erro": "Dados inválidos"}, 400

            return {"mensagem": "Bicicleta atualizada com sucesso"}, 200


@app.route('/bikes/<int:id>', methods=['DELETE'])
def deletar_bicicleta(id):
    try:
        filtro = {"id": id}
        dados_bicicleta = list(mongo.db.bicicletas_aps_5.find(filtro))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_bicicleta:
            try:
                mongo.db.bicicletas_aps_5.delete_one(filtro)
            except:
                return {"erro": "Dados inválidos"}, 400
            
            return {"mensagem": "Bicicleta deletada com sucesso"}, 200
        else:
            return {"erro": "Bicicleta não encontrada"}, 404
        
#CRUD EMPRÈSTIMOS

@app.route('/emprestimos/usuarios/<int:id_usuario>/bikes/<int:id_bike>', methods=['POST'])
def cadastrar_emprestimp(id_usuario, id_bike):
    emprestimo = request.json
    id = emprestimo.get("id")
    id_usuario = id_usuario
    id_bicicleta = id_bike
    data_alugado = emprestimo.get("data_alugado", "")

    if not id or not id_usuario or not id_bicicleta or not data_alugado:
        return {"error": "Id, id do usuário, id da bicicleta e data do aluguel são obrigatórios"}, 400
    
    if mongo.db.emprestimos_aps_5.find_one({"id": id}):
        return {"error": "Id já existe"}, 409
    
    if mongo.db.emprestimos_aps_5.find_one({"id_bicicleta": id_bicicleta}):
        return {"error": "Bicicleta já possui um empréstimo"}, 409
    
    if not mongo.db.usuarios_aps_5.find_one({"id": id_bicicleta}):
        return {"error": "Usuário não encontrado"}, 404

    if not mongo.db.bicicletas_aps_5.find_one({"id": id_bicicleta}):
        return {"error": "Bicicleta não encontrada"}, 404

    novo_emprestimo = {
        "id": id,
        "id_usuario": id_usuario,
        "id_bicicleta": id_bicicleta,
        "data_alugado": data_alugado
    }

    try:
        mongo.db.emprestimos_aps_5.insert_one(novo_emprestimo)
    except:
        return {"error": "Dados inválidos"}, 400

    return {"mensagem": "Bicicleta adicionado com sucesso"}, 201


@app.route('/emprestimos', methods=['GET'])
def get_all_emprestimos():
    id_usuario = request.args.get('id_usuario', '')
    id_bicicleta = request.args.get('id_bicicleta', '')

    try:
        filtro = {}
        projecao = {"_id": 0, "data_alugado": 0}

        if id_usuario:
            filtro["id_usuario"] = int(id_usuario)
        
        if id_bicicleta:
            filtro["id_bicicleta"] = int(id_bicicleta)

        dados_emprestimos = mongo.db.emprestimos_aps_5.find(filtro, projecao)
    except:
        return {"error": "Erro no sistema"}, 500

    resp = {
        "emprestimos": list(dados_emprestimos)
    }

    return resp, 200


@app.route('/emprestimos/<int:id>', methods=['DELETE'])
def deletar_emprestimo(id):
    try:
        filtro = {"id": id}
        dados_emprestimo = list(mongo.db.emprestimos_aps_5.find(filtro))
    except:
        return {"erro": "Erro no sistema"}, 500
    else:
        if dados_emprestimo:
            try:
                mongo.db.emprestimos_aps_5.delete_one(filtro)
            except:
                return {"erro": "Dados inválidos"}, 400
    
            return {"mensagem": "Empréstimo deletado com sucesso"}, 200
        else:
            return {"erro": "Empréstimo não encontrada"}, 404


if __name__ == '__main__':
    app.run(debug=True)