from src.models import models_db as models
import os

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from src.models.models_db import Veiculos
from src.dependencies.database import SessionLocal
from src.models.api.model_veiculos import VeiculosBase, VeiculosInsert
from src.services.authentication import get_current_user

from dotenv import load_dotenv
load_dotenv()

router = APIRouter(
    tags=['Veiculos'],
    dependencies=[Depends(get_current_user)],
    responses={401: {'detail': os.environ.get('ERRO_401')}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


@router.get('/veiculo/{id_veiculo}', status_code=status.HTTP_200_OK)
async def veiculo_id(
        id_veiculo: int,
        db: db_dependency
):
    """
    Obtém um item da tabela de veiculos pelo ID.

    Args:
        id_veiculo (int): O ID do veiculo.
        db: Sessão do banco de dados.

    Returns:
        veiculo: O objeto veiculo correspondente ao ID,
            ou gera HTTP_404_NOT_FOUND se não encontrado.
    """

    veiculo = db.query(models.Veiculos).filter(models.Veiculos.id == id_veiculo).first()

    if veiculo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')

    return veiculo


@router.get('/veiculo', status_code=status.HTTP_200_OK)
async def veiculos(db: db_dependency):
    """
    Obtém todos os dados da tabela de veiculos.

    Args:
        db: Sessão do banco de dados.

    Returns:
        list[Veiculos]: Uma lista de objetos Veiculos.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao obter os dados.
    """
    try:
        # retorna todas as linhas da tabela
        return db.query(models.Veiculos).all()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Erro ao obter os dados da tabela")


@router.post('/veiculo', status_code=status.HTTP_201_CREATED)
async def insere_veiculo(
        veiculo: VeiculosInsert,
        db: db_dependency
):
    """
    Insere dados de na tabela de veiculos com base nos critérios fornecidos.
    Necessário passar pelo menos um dos parâmetros para retornar algo.

    Args:
        veiculo (VeiculosBase): Objeto com os critérios de filtro.
            Os campos para inserção são:
            * categoria (str, optional): Categoria do veiculo.
            * marca (str, optional): Categoria do veiculo.
            * nome (str): Nome do veiculo.
            * ano (str): Ano do veiculo.
            * status (float, optional): Status do veiculo que por default é 'DESCONECTADO'.
        db: Sessão do banco de dados.

    Returns:
        ID[int]: Retorna o ID inserido.

    Raises:
        HTTPException: Com status code 500 se houver um erro ao inserir os dados.
    """

    if isinstance(veiculo.status, str):
        veiculo.status = str(veiculo.status).upper()

    create_veiculo_model = Veiculos(
        categoria=veiculo.categoria,
        marca=veiculo.marca,
        nome=veiculo.nome,
        ano=veiculo.ano,
        status=veiculo.status
    )

    db.add(create_veiculo_model)
    db.commit()

    db.refresh(create_veiculo_model)

    return {'id': create_veiculo_model.id}


@router.put('/veiculo/{id_veiculo}', status_code=status.HTTP_204_NO_CONTENT)
async def altera_veiculo(
        id_veiculo: int,
        veiculo_insert: VeiculosInsert,
        db: db_dependency
):
    """
    Altera os dados referentes a um item existente na tabela de veiculos.
    Args:
        id_veiculo (int): O ID de veiculo a ser alterada.
        veiculo_insert (VeiculosInsert): Objeto com os novos dados de veiculo.
            Os campos que podem ser alterados são:
            * categoria (str, optional): Categoria do veiculo.
            * marca (str, optional): Categoria do veiculo.
            * nome (str, optional): Nome do veiculo.
            * ano (str, optional): Ano do veiculo.
            * status (str, optional): CONECTADO ou DESCONECTADO.
        db: Sessão do banco de dados.

    Returns:
        None: Retorna um status HTTP 204 No Content em caso de sucesso.

    Raises:
        HTTPException: Com status code 404 Not Found se o veiculo não for encontrada.
        :param veiculo_insert:
    """
    # Busca o item no banco de dados pelo ID
    veiculo_model = db.query(Veiculos).filter(Veiculos.id == id_veiculo).first()
    if veiculo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    # Atualiza os campos do objeto com os novos valores
    if veiculo_insert.categoria is not None:
        veiculo_model.categoria = veiculo_insert.categoria

    if veiculo_insert.marca is not None:
        veiculo_model.marca = veiculo_insert.marca

    if veiculo_insert.nome is not None:
        veiculo_model.nome = veiculo_insert.nome

    if veiculo_insert.ano is not None:
        veiculo_model.ano = veiculo_insert.ano

    if veiculo_insert.status is not None:
        veiculo_model.status = veiculo_insert.status.upper()

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None


@router.delete('/veiculo/{id_veiculo}', status_code=status.HTTP_204_NO_CONTENT)
async def deleta_veiculo(
        id_veiculo: int,
        db: db_dependency
):
    """
    Deleta um item da tabela de veiculos pelo ID.

    Args:
        id_veiculo (int): O ID de veiculo a ser deletada.
        db: Sessão do banco de dados.

    Returns:
        None: Retorna um status HTTP 204 No Content em caso de sucesso.

    Raises:
        HTTPException: Com status code 404 Not Found se o veiculo não for encontrada.
    """

    # Busca o item no banco de dados pelo ID
    veiculo_model = db.query(Veiculos).filter(Veiculos.id == id_veiculo).first()
    if veiculo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=os.environ.get('ERRO_404'))

    db.delete(veiculo_model)

    # Realiza o commit para persistir as alterações no banco de dados
    db.commit()

    # Retorna o status 204 No Content, indicando sucesso sem conteúdo na resposta
    return None

