# Desafio de Web Services RESTful com Flask, MongoDB no Mongo Atlas, e Streamlit

## Contexto e Objetivo
Você foi contratado por uma startup que deseja construir um sistema de vendas online avançado, capaz de gerenciar clientes, produtos, estoques, carrinhos de compras e pedidos. Seu desafio é desenvolver uma API RESTful usando Flask e MongoDB no Mongo Atlas, seguindo os princípios do Nível 2 do Modelo de Maturidade de Richardson. Adicionalmente, você criará uma interface de usuário com Streamlit que inclui painéis distintos para usuários e administradores. Este projeto combina back-end e front-end com práticas modernas de desenvolvimento web.

## Requisitos do Sistema

### Estrutura do Projeto
O projeto deve ser organizado nas seguintes partes:
- `app.py`: Arquivo principal da Flask API.
- `streamlit_app.py`: Arquivo principal para a interface do Streamlit.
- `models.py`: Definições dos modelos de dados do MongoDB.
- `auth.py`: Implementação da autenticação básica.
- Coleção Postman (`postman_collection.json`): Para testar a API.
- Documentação da API: Recomenda-se usar Markdown ou Swagger.

### Modelagem de Dados com MongoDB
Estruture as seguintes coleções e documentos com relacionamentos embutidos:
- **Clientes**: Inclui `nome`, `email`, `cpf`, `senha` e uma lista embutida de `pedidos`.
- **Produtos**: Contém `nome`, `descricao`, `preco`, `estoque`, e uma lista de `fornecedores` (nome, email, cnpj), além de um campo opcional para `url_imagem`.
- **Pedidos**: Compreende `data_hora`, `valor_total`, `status` e itens do pedido (`produto_id`, `quantidade`).

### Implementação da API RESTful
#### Endpoints e Verbos HTTP
- **Clientes**
  - `GET /clientes`: Lista todos os clientes.
  - `POST /clientes`: Cadastra um novo cliente.
  - `GET /clientes/{id}`: Retorna detalhes de um cliente específico.
  - `PUT /clientes/{id}`: Atualiza dados de um cliente.
  - `DELETE /clientes/{id}`: Remove um cliente.

- **Produtos**
  - `GET /produtos`: Lista todos os produtos.
  - `POST /produtos`: Adiciona um novo produto (com opção de upload de imagem).
  - `GET /produtos/{id}`: Detalhes de um produto.
  - `PUT /produtos/{id}`: Atualiza dados de um produto.
  - `DELETE /produtos/{id}`: Exclui um produto.

- **Pedidos**
  - `GET /pedidos`: Lista todos os pedidos de um cliente.
  - `POST /pedidos`: Cria um novo pedido.
  - `GET /pedidos/{id}`: Detalhes de um pedido.

#### Autenticação
Use Basic Authentication para proteger as rotas administrativas, especialmente as de modificação.

### Interface de Usuário com Streamlit
Desenvolva dois painéis:
- **Painel do Usuário**: Visualização e interação com produtos e pedidos.
- **Painel Administrativo**: Gestão de clientes, produtos e pedidos, incluindo funcionalidades para upload de imagens.

### Opções de Deploy
- **Heroku**: Para a API e a interface Streamlit.
- **Render**: Como opção alternativa para deploy.

### Funcionalidades Opcionais
- **Gerenciamento de Imagens**: Permita o upload de imagens para produtos, armazenando em um sistema de arquivos (como um bucket S3 ou diretório local), e guarde a URL no documento do produto.

## Tutoriais e Recursos
(Aqui, inclua links para documentação do MongoDB, Flask, Streamlit, Mongo Atlas, Postman, e plataformas de deploy como Heroku e Render.)

## Conclusão
Este projeto não apenas fortalece suas habilidades em desenvolvimento full-stack, mas também o prepara para implementações complexas em ambientes de produção real. Esperamos que você encontre este desafio educativo e estimulante. Boa sorte!

