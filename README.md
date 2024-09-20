<p align="center">
  <img src="./docs/image/General_Motors_(2021).svg" alt="Logo GM"  width="300" height="100">
</p>

# API-VEICULOS

<h1 style="font-family: 'Arial'; text-align: left;">Índice</h1>

<ol style="font-family: 'Georgia'; font-size: 18px; text-align: left;">
  <li><a href="#introducao"><strong>Introdução</strong></a></li>
  <li><a href="#como usar"><strong>Como Usar</strong></a></li>
  <li><a href="#como-instalar-na-sua-maquina"><strong>Como instalar na sua máquina</strong></a></li>
  <li>
    <a href="#endpoints"><strong>Endpoints</strong></a>
    <ul>
      <li><a href="#users">3.1 <strong>Users</strong></a></li>
      <li><a href="#token">3.2 <strong>Obtendo Token</strong></a></li>
      <li><a href="#veiculo">3.3 <strong>Veiculos</strong></a></li>
    </ul>
  </li>
  <li><a href="#contato">📑 <strong>Referências</strong></a></li>
</ol>




# introducao

API-VEICULOS é um projeto feito em FastAPI, um poderoso framework 
em python para desenvolvimento de APIs. 

Através dela é possível realizar um CRUD completo (Create, Read, Update, Delete) diretamente com uma base MySql, através dos endpoints 
referentes a cada uma dos tipos de tabelas.


# como usar

Para poder utilizar todas as funcionalidades da API, basta dispor de uma ferramenta _'API Client'_ 
como o **POSTMAN** ou o **INSOMNIA**, acrescentar a url referente a cada um dos endpoints e selecionar o tipo de 
requisição, _GET, POST, PUT OU DELETE_.
Também é possível acessar as funcionalidades através do endereço [SWAGGER](http://127.0.0.1:8000/docs), que possibilita uma 
visualização bem clara da documentação de cada um dos endpoints com descrição de cada parametro e 
body para enviar. 

# como-instalar-na-sua-maquina

Para instalar na sua máquina local basta realizar o clone do repositório em um diretório local e 
instalar as bibliotecas dentro do arquivo [requirements.txt](./requirements.txt).
Também é importante configurar um arquivo __.env__ ou criar variaveis de ambiente da lista abaixo:

```bash
USER_DB=usuario do banco de dados
PASSWORD_DB=senha do banco de dados
URL_DB=endereço do banco, se for local é 127.0.0.1
PORT_DB=3306 geralmente é o padrão
SCHEMA_DB=nome do schema do banco de dados

SECRET_KEY=valor
ALGORITHM=valor

ERRO_401=descricao do erro
ERRO_404=descricao do erro

```

Para executar basta utilizar um comando da biblioteca uvicorn como no exemplo abaixo:
```bash
uvicorn main:app --reload
```

Para acessar os **Endpoints** da sua máquina local, por padrão o endereço é este http://127.0.0.1:8000/
e basta acrescer '/nome do endpoint'

# endpoints

## users

### POST
Antes de utilizar a API é importante ter em mãos um token de autenticação, para este projeto foi 
escolhido o método de autentificação JWT, portanto é necessário que seja criado um usuário e senha 
para que possa ser gerado um token de autenticação que deve ser usado em todos as outras requisições.
Para criar um usuário basta realizar um _POST_ na url http://127.0.0.1:8000/auth/users/ e passar como
 payload um nome de usuário e uma senha **(criptografada na base de dados)**.

###### Observação: Não é possível criar dois ou mais usuários com o mesmo nome

#### Exemplo de requisição no python
```py
import requests
import json

url = "http://127.0.0.1:8000/auth/users/"

payload = json.dumps({
  "username": "teste",
  "password": "teste1234"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
#### Exemplo de resposta
````python
{
    "id": 1
}
````

### GET

Caso já tenha o [token](#token) retorna informações do usuário atual.

###### Observação: Sem o token é esperado um erro 401.


#### Exemplo de requisição no python
```py
import requests

url = "http://127.0.0.1:8000/auth/users"

payload={}
headers = {
  'Authorization': 'Bearer TOKEN'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

#### Exemplo de resposta
````python
{
    "User": {
        "username": "teste",
        "id": 1
    }
}
````

### GET

Caso já tenha o [token](#token) de usuário é possível acessar dados de um unico usuário pelo id 
criados com o método _GET_.

###### Observação: Sem o token é esperado um erro 401.


#### Exemplo de requisição no python
```py
import requests

url = "http://127.0.0.1:8000/auth/users/1"

payload={}
headers = {
  'Authorization': 'Bearer TOKEN'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

#### Exemplo de resposta
````python
{
    "username": "teste",
    "hashed_password": "$2b$12$GZr1lEmhaVgX.79U8UA7F.u92o2KHZePFeZge.91sFJgMqFKm/OjO",
    "id": 1
}
````

### PUT

Caso já tenha o [token](#token) de usuário é possível acessar dados de um unico usuário pelo id 
criados para possíveis alterações através do método _PUT_.

###### Observação: Sem o token é esperado um erro 401.


#### Exemplo de requisição no python
```py
import requests
import json

url = "http://127.0.0.1:8000/auth/users/1"

payload = json.dumps({
  "username": "teste1",
  "password": "teste1234"
})
headers = {
  'Authorization': 'Bearer TOKEN',  
 'Content-Type': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
```

Não retorna nada, apenas o código __204__ em caso de sucesso.


### DELETE

Caso já tenha o [token](#token) de usuário é possível deletar um usuário através do id com o método _DELETE_.

###### Observação: Sem o token é esperado um erro 401.


#### Exemplo de requisição no python
```py
import requests

url = "http://127.0.0.1:8000/auth/users/3"

payload={}
headers = {
  'Authorization': 'Bearer TOKEN'
}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)


```

Não retorna nada, apenas o código __204__ em caso de sucesso.


## token

### POST

Caso já tenha criado um usuário é necessário obter o **TOKEN**  para poder usufruir de todas as 
funcionalidades e para isso basta utilizar o método _POST_.

###### Observação: Sem usuário e senha validos é esperado um erro 401.


#### Exemplo de requisição no python
```py
import requests

url = "http://127.0.0.1:8000/auth/token"

payload='username=<NOME_USUARIO>&password=<SENHA>'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
#### Exemplo de resposta
```py
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZSIsImlkIjoxLCJleHAiOjE3Mjc2NDkwODB9.TY5Robd2ke42_Wmss88Q8ESKXqj8muesQB4Yrbvr-w8",
    "token_type": "bearer"
}
```

## veiculo

### POST
Caso já tenha o [token](#token) de usuário é possível inserir novos dados dentro da tabela 
veiculo através do método _POST_.

###### Observação: Sem o token é esperado um erro 401.

#### Exemplo de requisição no python
```py
import requests
import json

url = "http://127.0.0.1:8000/veiculo"

payload = json.dumps({
    "categoria": "hatch",
    "marca": "GM",
    "nome": "Celta",
    "ano": "2005",
    "status": "CONECTADO"
})
headers = {
  'Authorization': 'Bearer TOKEN',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```

#### Exemplo de resposta
```py
{
    "id": 4
}
```

### GET

Caso já tenha o [token](#token) de usuário é possível acessar todos os dados da tabela veiculos.
com o método _GET_.

###### Observação: Sem o token é esperado um erro 401.


#### Exemplo de requisição no python
```py
import requests

url = "http://127.0.0.1:8000/veiculo"

payload={}
headers = {
  'Authorization': 'Bearer TOKEN'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

#### Exemplo de resposta
```py
[
    {
        "marca": "GM",
        "categoria": "hatch",
        "nome": "Celta",
        "id": 1,
        "ano": "2005",
        "status": "DESCONECTADO"
    },
    {
        "marca": "Ford",
        "categoria": "sedan",
        "nome": "Fusion",
        "id": 2,
        "ano": "2010",
        "status": "DESCONECTADO"
    },
    {
        "marca": "GM",
        "categoria": "hatch",
        "nome": "Celta",
        "id": 4,
        "ano": "2005",
        "status": "CONECTADO"
    }
]
```

### GET

Caso já tenha o [token](#token) de usuário é possível acessar dados de um unico item de 
veiculo pelo id com o método _GET_.

###### Observação: Sem o token é esperado um erro 401.


#### Exemplo de requisição no python
```py
import requests

url = "http://127.0.0.1:8000/veiculo/1"

payload={}
headers = {
  'Authorization': 'Bearer TOKEN'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```

#### Exemplo de resposta
```py

   {
       "marca": "GM",
       "categoria": "hatch",
       "nome": "Celta",
       "id": 1,
       "ano": "2005",
       "status": "DESCONECTADO"
   }
```

### PUT

Caso já tenha o [token](#token) de usuário é possível acessar dados de um unico item da tabela veiculo 
pelo id para possíveis alterações através do método _PUT_.

###### Observação: Sem o token é esperado um erro 401.


#### Exemplo de requisição no python
```py
import requests
import json

url = "http://127.0.0.1:8000/veiculo/1"

payload = json.dumps({
    "status": "conectado"
})
headers = {
  'Authorization': 'Bearer TOKEN',
  'Content-Type': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
```

Não retorna nada, apenas o código __204__ em caso de sucesso.

### DELETE

Caso já tenha o [token](#token) de usuário é possível deletar um item da tabela veiculo 
através do id com o método _DELETE_.

###### Observação: Sem o token é esperado um erro 401.


#### Exemplo de requisição no python
```py
import requests

url = "http://127.0.0.1:8000/veiculo/1"

payload={}
headers = {
  'Authorization': 'Bearer TOKEN'
}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)
```

Não retorna nada, apenas o código __204__ em caso de sucesso.

#contato:

Em caso de dúvidas ou mesmo para demonstrar o funcionamento do código, pode entrar em contato comigo através do linkedin abaixo:

[Linkedin-Marcelo](https://www.linkedin.com/in/marcelohorikoshi/)