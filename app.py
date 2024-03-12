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
def hello_world():
    return "Hello, World!"


@app.route('/livro', methods=['POST'])
def cadastro_livro():
    dic_livro = request.json
    # Recuperando os dados do json que chegou via requisição 
    titulo = dic_livro.get('titulo', "")
    autor = dic_livro.get('autor', "")
    ano_publicacao = dic_livro.get('ano_publicacao', "")
    genero = dic_livro.get('genero', "")

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO livros (titulo, autor, ano_publicacao, genero) VALUES (%s, %s, %s, %s)",
                    (titulo, autor, ano_publicacao, genero))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()  # Reverte a transação atual
        #Resposta de erro
        return {"erro": str(e)}, 400
    finally:
        cur.close()

    # Resposta de sucesso
    resp = {
        "mensagem": "Livro cadastrado",
        "livro": dic_livro
    }

    return resp, 201


@app.route('/livro', methods=['GET'])
def lista_livros():
    genero = request.args.get('genero', '')
    cur = conn.cursor()

    try:
        if genero == '':
            cur.execute("SELECT * FROM livros")
            livros = cur.fetchall()
        else:
            cur.execute(f"SELECT * FROM livros WHERE genero = '{genero}'")
            livros = cur.fetchall()
            
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    livros_lista = []
    for livro in livros:
        livros_lista.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "ano_publicacao": livro[3],
            "genero": livro[4]
        })

    return livros_lista, 200


@app.route('/livro/<int:id>', methods=['GET'])
def lista_livro(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM livros WHERE id = {id}")
        livros = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    finally:
        cur.close()

    if livros == []:
        return {"erro": "Livro não encontrado"}, 404
    else:
        dados_livro = []
        for livro in livros:
            dados_livro.append({
                "id": livro[0],
                "titulo": livro[1],
                "autor": livro[2],
                "ano_publicacao": livro[3],
                "genero": livro[4]
            })

    return dados_livro, 200


@app.route('/livro/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM livros WHERE id = {id}")
        livros = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    else:
        if livros == []:
            return {"erro": "Livro não encontrado"}, 404
        else:
            dic_livro = request.json
            # Recuperando os dados do json que chegou via requisição 
            titulo = dic_livro.get('titulo', "")
            autor = dic_livro.get('autor', "")
            ano_publicacao = dic_livro.get('ano_publicacao', "")
            genero = dic_livro.get('genero', "")

            try:
                if titulo:
                    cur.execute(f"UPDATE livros SET titulo = '{titulo}' WHERE id = {id}")
                    conn.commit()

                if autor:
                    cur.execute(f"UPDATE livros SET autor = '{autor}' WHERE id = {id}")
                    conn.commit()

                if ano_publicacao:
                    cur.execute(f"UPDATE livros SET ano_publicacao = '{ano_publicacao}' WHERE id = {id}")
                    conn.commit()

                if genero:
                    cur.execute(f"UPDATE livros SET genero = '{genero}' WHERE id = {id}")
                    conn.commit()

            except psycopg2.Error as e:
                conn.rollback()  # Reverte a transação atual
                #Resposta de erro
                return {"erro": str(e)}, 400
            finally:
                cur.close()

            # Resposta de sucesso
            resp = {
                "mensagem": "Livro atualizado",
            }

    return resp, 200


@app.route('/livro/<int:id>', methods=['DELETE'])
def apagar_livro(id):
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM livros WHERE id = {id}")
        livros = cur.fetchall()
    except psycopg2.Error as e:
        return {"erro": str(e)}, 500
    else:
        if livros == []:
            return {"erro": "Livro não encontrado"}, 404
        else:
            try:
                cur.execute(f"DELETE FROM livros WHERE id = {id}")
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()  # Reverte a transação atual
                #Resposta de erro
                return {"erro": str(e)}, 400
            finally:
                cur.close()

            # Resposta de sucesso
            resp = {
                "mensagem": "Livro deletado",
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
