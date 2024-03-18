from flask import Flask, request
import psycopg2
import json

app = Flask("nome_da_minha_aplicacao")

conn = psycopg2.connect(
    dbname="dwdcnoty",
    user="dwdcnoty",
    password="OcTpYT7PvUGbihzCP2gPuHGbyUVDdOqV",
    host="silly.db.elephantsql.com"
)


@app.route('/')
def web_service():
    return "Web service em adamento!"


# Cadastrar cliente
@app.route('/clientes', methods=['POST'])
def cadastro_cliente():
    dic_cliente = request.json
    # Recuperando os dados do json que chegou via requisição 
    nome = dic_cliente.get('nome', "")
    email = dic_cliente.get('email', "")
    cpf = dic_cliente.get('cpf', "")
    senha = dic_cliente.get('senha', "")

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO clientes (titulo, autor, ano_publicacao, genero) VALUES (%s, %s, %s, %s)",
                    (nome, email, cpf, senha))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()  # Reverte a transação atual
        # Resposta de erro
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    # Resposta de sucesso
    resp = {
        "mensagem": "Cliente cadastrado",
        "livro": dic_cliente
    }

    return resp, 201


# Listar clientes
@app.route('/clientes', methods=['GET'])
def lista_clientes():
    # Recuperando parâmetros de filtro da url
    nome = request.args.get('nome', '')
    email = request.args.get('email', "")
    cpf = request.args.get('cpf', "")
    senha = request.args.get('senha', "")

    cur = conn.cursor()

    try:
        if nome:
            cur.execute(f"SELECT * FROM clientes WHERE nome = '{nome}'")
            clientes = cur.fetchall()
        elif email:
            cur.execute(f"SELECT * FROM clientes WHERE email = '{email}'")
            clientes = cur.fetchall()
        elif cpf:
            cur.execute(f"SELECT * FROM clientes WHERE cpf = '{cpf}'")
            clientes = cur.fetchall()
        elif senha:
            cur.execute(f"SELECT * FROM clientes WHERE senha = '{senha}'")
            clientes = cur.fetchall()
        else:
            cur.execute("SELECT * FROM clientes")
            clientes = cur.fetchall()
            
            
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    clientes_lista = []
    for cliente in clientes:
        clientes_lista.append({
            "id": cliente[0],
            "nome": cliente[1],
            "email": cliente[2],
            "cpf": cliente[3],
            "senha": cliente[4]
        })

    return clientes_lista, 200


# Informações do cliente
@app.route('/clientes/<int:id>', methods=['GET'])
def lista_cliente(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM clientes WHERE id = {id}")
        clientes = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    if clientes == []:
        return {"erro": "Cliente não encontrado"}, 404
    else:
        dados_cliente = []
        for cliente in clientes:
            dados_cliente.append({
                "id": cliente[0],
                "nome": cliente[1],
                "email": cliente[2],
                "cpf": cliente[3],
                "senha": cliente[4]
            })

    return dados_cliente, 200


# Atualizar cliente
@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM clientes WHERE id = {id}")
        clientes = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    else:
        if clientes == []:
            return {"erro": "Cliente não encontrado"}, 404
        else:
            dic_cliente = request.json
            # Recuperando os dados do json que chegou via requisição 
            nome = dic_cliente.get('nome', "")
            email = dic_cliente.get('email', "")
            cpf = dic_cliente.get('cpf', "")
            senha = dic_cliente.get('senha', "")

            try:
                if nome:
                    cur.execute(f"UPDATE clientes SET nome = '{nome}' WHERE id = {id}")
                    conn.commit()

                if email:
                    cur.execute(f"UPDATE clientes SET email = '{email}' WHERE id = {id}")
                    conn.commit()

                if cpf:
                    cur.execute(f"UPDATE clientes SET cpf = '{cpf}' WHERE id = {id}")
                    conn.commit()

                if senha:
                    cur.execute(f"UPDATE clientes SET senha = '{senha}' WHERE id = {id}")
                    conn.commit()

            except psycopg2.Error as e:
                conn.rollback()  # Reverte a transação atual
                #Resposta de erro
                return {"Erro": str(e)}, 400
            finally:
                cur.close()

            # Resposta de sucesso
            resp = {
                "mensagem": "Cliente atualizado",
            }

    return resp, 200


# Deletar cliente
@app.route('/clientes/<int:id>', methods=['DELETE'])
def apagar_livro(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM clientes WHERE id = {id}")
        livros = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    else:
        if livros == []:
            return {"erro": "Cliente não encontrado"}, 404
        else:
            try:
                cur.execute(f"DELETE FROM clientes WHERE id = {id}")
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()  # Reverte a transação atual
                #Resposta de erro
                return {"erro": str(e)}, 400
            finally:
                cur.close()

            # Resposta de sucesso
            resp = {
                "mensagem": "Cliente deletado",
            }

    return resp, 200


@app.route('/usuario', methods=['POST'])
def cadastro_usuario():
    dic_usuario = request.json
    # Recuperando os dados do json que chegou via requisição 
    nome = dic_usuario.get('nome', "")
    email = dic_usuario.get('email', "")
    data_cadastro = dic_usuario.get('data_cadastro', "")

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nome, email, data_cadastro) VALUES (%s, %s, %s)",
                    (nome, email, data_cadastro))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()  # Reverte a transação atual
        #Resposta de erro
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    # Resposta de sucesso
    resp = {
        "mensagem": "Usuario cadastrado",
        "usuário": dic_usuario
    }
    return resp, 201


@app.route('/usuario', methods=['GET'])
def lista_usuarios():
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    usuarios_lista = []
    for usuario in usuarios:
        usuarios_lista.append({
            "id": usuario[0],
            "nome": usuario[1],
            "email": usuario[2],
            "data_cadastro": usuario[3],
        })

    return usuarios_lista, 200


@app.route('/usuario/<int:id>', methods=['GET'])
def lista_usuario(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM usuarios WHERE id = {id}")
        usuarios = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    if usuarios == []:
        return {"erro": "Usuário não encontrado"}, 404
    else:
        dados_usuario = []
        for usuario in usuarios:
            dados_usuario.append({
                "id": usuario[0],
                "nome": usuario[1],
                "email": usuario[2],
                "data_cadastro": usuario[3],
            })

    return dados_usuario, 200


@app.route('/usuario/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM usuarios WHERE id = {id}")
        usuarios = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    else:
        if usuarios == []:
            return {"erro": "Usuário não encontrado"}, 404
        else:
            dic_usuario = request.json
            # Recuperando os dados do json que chegou via requisição 
            nome = dic_usuario.get('nome', "")
            email = dic_usuario.get('email', "")
            data_cadastro = dic_usuario.get('data_cadastro', "")

            try:
                if nome:
                    cur.execute(f"UPDATE usuarios SET nome = '{nome}' WHERE id = {id}")
                    conn.commit()

                if email:
                    cur.execute(f"UPDATE usuarios SET email = '{email}' WHERE id = {id}")
                    conn.commit()

                if data_cadastro:
                    cur.execute(f"UPDATE usuarios SET data_cadastro = '{data_cadastro}' WHERE id = {id}")
                    conn.commit()

            except psycopg2.Error as e:
                conn.rollback()  # Reverte a transação atual
                #Resposta de erro
                return {"erro": str(e)}, 400
            finally:
                cur.close()

            # Resposta de sucesso
            resp = {
                "mensagem": "Usuário atualizado",
            }

    return resp, 200


@app.route('/usuario/<int:id>', methods=['DELETE'])
def apagar_usuario(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM usuarios WHERE id = {id}")
        usuarios = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    else:
        if usuarios == []:
            return {"erro": "Usuário não encontrado"}, 404
        else:
            try:
                cur.execute(f"DELETE FROM usuarios WHERE id = {id}")
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()  # Reverte a transação atual
                #Resposta de erro
                return {"erro": str(e)}, 400
            finally:
                cur.close()

            # Resposta de sucesso
            resp = {
                "mensagem": "Usuário deletado",
            }
    return resp, 200


if __name__ == '__main__':
    app.run(debug=True)
