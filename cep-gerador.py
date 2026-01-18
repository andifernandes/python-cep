from src.processor import gerar_cep
from src.database import inserir_cep

for _ in range(10):
    cep = gerar_cep()
    inserir_cep(cep)
