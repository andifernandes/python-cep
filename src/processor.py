import random

PREFIXOS_VALIDOS = ["010", "020", "030", "040", "050"]  # SP

def gerar_cep():
    prefixo = random.choice(PREFIXOS_VALIDOS)
    sufixo = random.randint(0, 9999)
    return f"{prefixo}{sufixo:04d}"