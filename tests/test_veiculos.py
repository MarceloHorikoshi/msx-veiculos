import os
import pytest
from fastapi.testclient import TestClient

from main import app  # Importe a instância FastAPI do seu aplicativo


# Inicialize o cliente de teste
client = TestClient(app)

global id_inserted


def get_auth_token():
    """
    Cria um usuário de teste e faz login para obter o token JWT.
    """
    # Criar o usuário de teste
    new_user_data = {'username': 'testuser_veiculo', 'password': 'testpassword'}
    client.post('/auth/users/', json=new_user_data)

    # Fazer login e obter o token
    login_data = {
        'username': 'testuser_veiculo',
        'password': 'testpassword'
    }
    response = client.post('/auth/token', data=login_data)

    assert response.status_code == 200
    token = response.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}


headers = get_auth_token()


@pytest.mark.parametrize("veiculo_insert", [
    {
        "categoria": "hatch",
        "marca": "GM",
        "nome": "Celta",
        "ano": "2005",
        "status": "CONECTADO"
    },
    {
        "categoria": "sedan",
        "marca": "Ford",
        "nome": "Fusion",
        "ano": "2010",
        "status": "DESCONECTADO"
    },
    {
        "categoria": "SUV",
        "marca": "Toyota",
        "nome": "RAV4",
        "ano": "2021",
        "status": "CONECTADO"
    }
])
def test_insere_veiculo_sucesso(veiculo_insert):
    global id_inserted
    response = client.post('/veiculo', headers=headers, json=veiculo_insert)

    id_inserted = response.json()['id']

    assert response.status_code == 201
    assert isinstance(id_inserted, int)


def test_insere_veiculo_sem_token():
    veiculo_insert = {
                        "categoria": "hatch",
                        "marca": "GM",
                        "nome": "Celta",
                        "ano": "2005",
                        "status": "CONECTADO"
                    }
    response = client.post('/veiculo', json=veiculo_insert)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_veiculo_id_sucesso():
    response = client.get('/veiculo/1', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_veiculo_id_sem_token():
    response = client.get('/veiculo/1')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_veiculo_id_item_inexistente():
    response = client.get('/veiculo/99999', headers=headers)
    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_total_veiculo_sucesso():
    response = client.get('/veiculo', headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_total_veiculo_sem_token():
    response = client.get('/veiculo')
    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_veiculo_sucesso():
    veiculo_alteracao = {
                        "categoria": "hatch",
                        "marca": "GM",
                        "nome": "Celta",
                        "ano": "2005",
                        "status": "DESCONECTADO"
                    }

    response = client.put('/veiculo/1', headers=headers, json=veiculo_alteracao)

    assert response.status_code == 204


def test_altera_veiculo_sem_token():
    veiculo_alteracao = {
                        "categoria": "hatch",
                        "marca": "GM",
                        "nome": "Celta",
                        "ano": "2005",
                        "status": "DESCONECTADO"
                    }

    client = TestClient(app)
    response = client.put('/veiculo/1', json=veiculo_alteracao)

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_altera_veiculo_item_inexistente():
    veiculo_alteracao = {
                        "categoria": "hatch",
                        "marca": "GM",
                        "nome": "Celta",
                        "ano": "2005",
                        "status": "DESCONECTADO"
                    }

    client = TestClient(app)
    response = client.put('/veiculo/9999999', headers=headers, json=veiculo_alteracao)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}


def test_deleta_veiculo_sucesso():
    global id_inserted
    client = TestClient(app)
    response = client.delete(f'/veiculo/{id_inserted}', headers=headers)

    assert response.status_code == 204


def test_deleta_veiculo_sem_token():
    client = TestClient(app)
    response = client.delete(f'/veiculo/{id_inserted}')

    assert response.status_code == 401
    assert response.json() == {'detail': os.environ.get('ERRO_401')}


def test_deleta_veiculo_item_inexistente():
    client = TestClient(app)
    response = client.delete(f'/veiculo/9999999', headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': os.environ.get('ERRO_404')}
