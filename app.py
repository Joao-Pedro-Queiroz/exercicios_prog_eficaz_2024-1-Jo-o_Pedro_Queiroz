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


# Caminho da raiz
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
        cur.execute("INSERT INTO clientes (nome, email, cpf, senha) VALUES (%s, %s, %s, %s)",
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
        "cliente": dic_cliente
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
        clientes = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    else:
        if clientes == []:
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


# Cadastrar produto
@app.route('/produtos', methods=['POST'])
def cadastro_cliente():
    dic_produto = request.json
    # Recuperando os dados do json que chegou via requisição 
    nome = dic_produto.get('nome', "")
    descricao = dic_produto.get('descricao', "")
    preco = dic_produto.get('preco', "")
    estoque = dic_produto.get('estoque', "")

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO produtos (nome, descricao, preco, estoque) VALUES (%s, %s, %s, %s)",
                    (nome, descricao, preco, estoque))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()  # Reverte a transação atual
        # Resposta de erro
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    # Resposta de sucesso
    resp = {
        "mensagem": "Produto cadastrado",
        "livro": dic_produto
    }

    return resp, 201


# Listar produtos
@app.route('/produtos', methods=['GET'])
def lista_clientes():
    # Recuperando parâmetros de filtro da url
    nome = request.args.get('nome', '')
    descricao = request.args.get('descricao', "")
    preco = request.args.get('preco', "")
    estoque = request.args.get('estoque', "")

    cur = conn.cursor()

    try:
        if nome:
            cur.execute(f"SELECT * FROM produtos WHERE nome = '{nome}'")
            clientes = cur.fetchall()
        elif descricao:
            cur.execute(f"SELECT * FROM produtos WHERE descricao = '{descricao}'")
            clientes = cur.fetchall()
        elif preco:
            cur.execute(f"SELECT * FROM produtos WHERE preco = {preco}")
            clientes = cur.fetchall()
        elif estoque:
            cur.execute(f"SELECT * FROM produtos WHERE senha = {estoque}")
            clientes = cur.fetchall()
        else:
            cur.execute("SELECT * FROM produtos")
            clientes = cur.fetchall()
            
            
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    produtos_lista = []
    for cliente in clientes:
        produtos_lista.append({
            "id": cliente[0],
            "nome": cliente[1],
            "descricao": cliente[2],
            "preco": cliente[3],
            "estoque": cliente[4]
        })

    return produtos_lista, 200


# Informações do produto
@app.route('/produtos/<int:id>', methods=['GET'])
def lista_cliente(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM produtos WHERE id = {id}")
        produtos = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    if produtos == []:
        return {"erro": "Produto não encontrado"}, 404
    else:
        dados_produto = []
        for cliente in clientes:
            dados_produto.append({
                "id": cliente[0],
                "nome": cliente[1],
                "descricao": cliente[2],
                "preco": cliente[3],
                "estoque": cliente[4]
            })

    return dados_produto, 200


# Atualizar cliente
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM produtos WHERE id = {id}")
        produtos = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    else:
        if produtos == []:
            return {"erro": "Produto não encontrado"}, 404
        else:
            dic_produto = request.json
            # Recuperando os dados do json que chegou via requisição 
            nome = dic_produto.get('nome', "")
            descricao = dic_produto.get('descricao', "")
            preco = dic_produto.get('preco', "")
            estoque = dic_produto.get('estoque', "")

            try:
                if nome:
                    cur.execute(f"UPDATE produtos SET nome = '{nome}' WHERE id = {id}")
                    conn.commit()

                if descricao:
                    cur.execute(f"UPDATE produtos SET descricao = '{descricao}' WHERE id = {id}")
                    conn.commit()

                if preco:
                    cur.execute(f"UPDATE produtos SET preco = {preco} WHERE id = {id}")
                    conn.commit()

                if estoque:
                    cur.execute(f"UPDATE produtos SET estoque = {estoque} WHERE id = {id}")
                    conn.commit()

            except psycopg2.Error as e:
                conn.rollback()  # Reverte a transação atual
                #Resposta de erro
                return {"Erro": str(e)}, 400
            finally:
                cur.close()

            # Resposta de sucesso
            resp = {
                "mensagem": "Produto atualizado",
            }

    return resp, 200


# Deletar cliente
@app.route('/produtos/<int:id>', methods=['DELETE'])
def apagar_livro(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM produtos WHERE id = {id}")
        produtos = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    else:
        if produtos == []:
            return {"erro": "Produto não encontrado"}, 404
        else:
            try:
                cur.execute(f"DELETE FROM produtos WHERE id = {id}")
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()  # Reverte a transação atual
                #Resposta de erro
                return {"erro": str(e)}, 400
            finally:
                cur.close()

            # Resposta de sucesso
            resp = {
                "mensagem": "Produto deletado",
            }

    return resp, 200


if __name__ == '__main__':
    app.run(debug=True)
