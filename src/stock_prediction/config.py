from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


DEFAULT_IPCA_FILEPATH = "https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA/Serie_Historica/ipca_SerieHist.zip"
DEFAULT_INPC_FILEPATH = "https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/INPC/Serie_Historica/inpc_SerieHist.zip"

class Config(BaseSettings):
    IPCA_FILEPATH: str = Field(default=DEFAULT_IPCA_FILEPATH, env="IPCA_FILEPATH")
    INPC_FILEPATH: str = Field(default=DEFAULT_INPC_FILEPATH, env="INPC_FILEPATH")


load_dotenv()
config = Config()
