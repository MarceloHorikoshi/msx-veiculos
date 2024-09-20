from sqlalchemy import Column, Integer, String, Float
from src.dependencies.database import Base


class Veiculos(Base):
    """
    Modelo de dados para a tabela 'veiculos', representando dados de veiculos.

    Attributes:
        id (int): ID único da entrada.
        categoria (str): Categoria do veiculo.
        marca (str): Categoria do veiculo.
        nome (str): Nome do veiculo.
        ano (str): Ano do veiculo.
        status (str): Status "CONECTADO" ou "DESCONECTADO"
    """

    __tablename__ = 'veiculos'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    categoria = Column(String(50))
    marca = Column(String(50))
    nome = Column(String(50))
    ano = Column(String(50))
    status = Column(String(50))


class User(Base):
    """
    Modelo de dados para a tabela 'users', representando dados de de usuarios.

    Attributes:
        id (int): ID único da entrada.
        username (str): Nome do usuario.
        hashed_password (str): Senha hasheada.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement='auto')
    username = Column(String(50), unique=True)
    hashed_password = Column(String(100))
