from typing import Optional
from pydantic import BaseModel, Field


class VeiculosInsert(BaseModel):
    """
    Modelo base para dados para inserção de veiculos na API.

    Attributes:
        categoria (str): Categoria do veiculo.
        marca (str): Categoria do veiculo.
        nome (str): Nome do veiculo.
        ano (str): Ano do veiculo.
        status (str): Status "CONECTADO" ou "DESCONECTADO"

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """
    categoria: Optional[str] = Field(None, alias="categoria")
    marca: Optional[str] = Field(None, alias="marca")
    nome: Optional[str] = Field(None, alias="nome")
    ano: Optional[str] = Field(None, alias="ano")
    status: Optional[str] = Field(None, alias="status")


class VeiculosBase(VeiculosInsert):
    """
    Modelo base para retorno de dados de veiculos na API.

    Attributes:
        id (int, optional): ID único da entrada.

    Fields:
        Todos os campos possuem apelidos que correspondem aos nomes dos atributos.
    """

    id: Optional[int] = None
