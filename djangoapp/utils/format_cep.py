import re
import brazilcep


def format_cep(cep):
    # Remover qualquer caractere que não seja número
    cep_numeric = re.sub(r'\D', '', cep)

    # Adicionar o hífen na posição correta
    cep_formated = f'{cep_numeric[:5]}-{cep_numeric[5:]}'

    return brazilcep.get_address_from_cep(cep_formated)
