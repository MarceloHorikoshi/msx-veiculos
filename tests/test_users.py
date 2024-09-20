from fastapi.testclient import TestClient
from main import app  # Importe a instância FastAPI do seu aplicativo

# Inicialize o cliente de teste
client = TestClient(app)

global id_inserted, headers


def get_auth_token(username, password):
    """
    Cria um usuário de teste e faz login para obter o token JWT.
    """
    # # Criar o usuário de teste
    # new_user_data = {'username': username, 'password': password}
    # client.post('/auth/users/', json=new_user_data)

    # Fazer login e obter o token
    login_data = {
        'username': username,
        'password': password
    }
    response = client.post('/auth/token', data=login_data)

    assert response.status_code == 200
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}


# Exemplo de caso de teste para a rota POST /auth/users/
def test_create_user():
    global id_inserted, headers
     # Obter o token dinâmico

    # Dados para criar um novo usuário
    user = 'testuser2'
    password = 'testpassword2'
    new_user_data = {'username': user, 'password': password}

    # Faça uma solicitação POST para /auth/users/ para criar um novo usuário
    response = client.post('/auth/users/', json=new_user_data)

    headers = get_auth_token(user, password)

    id_inserted = response.json().get('id')

    # Verifique se a resposta é bem-sucedida e o código de status HTTP é 201 (Created)
    assert response.status_code == 201
    assert id_inserted is not None  # Certifique-se de que o ID foi gerado


# Exemplo de caso de teste para a rota GET /auth/users
def test_get_users():
    # headers = get_auth_token()  # Obter o token dinâmico
    response = client.get('/auth/users', headers=headers)
    assert response.status_code == 200  # Verifique se a resposta é bem-sucedida


# Exemplo de caso de teste para a rota GET /auth/users/{user_id}
def test_get_single_user():
    global id_inserted
    # headers = get_auth_token()  # Obter o token dinâmico
    response = client.get(f'/auth/users/{id_inserted}', headers=headers)
    assert response.status_code == 200  # Verifique se a resposta é bem-sucedida


# Exemplo de caso de teste para a rota PUT /auth/users/{user_id}
def test_update_user_password():
    global id_inserted
    # headers = get_auth_token()  # Obter o token dinâmico
    update_data = {
        "username": "new_user_name",
        "password": "newpassword"
    }
    response = client.put(f'/auth/users/{id_inserted}', json=update_data, headers=headers)
    assert response.status_code == 204


def test_delete_user():
    global id_inserted
    # headers = get_auth_token()  # Obter o token dinâmico
    response = client.delete(f'/auth/users/{id_inserted}', headers=headers)
    assert response.status_code == 204  # Verifique se a resposta é bem-sucedida
