import random

def obter_cartas():
    cartas_jogador = input("Digite as cartas do jogador separadas por espaço: ").split()
    cartas_mesa = input("Digite as cartas da mesa separadas por espaço: ").split()
    return cartas_jogador, cartas_mesa

def valor_carta(carta):
    if carta in ['J', 'Q', 'K']:
        return 10
    elif carta == 'A':
        return 11
    else:
        return int(carta)

def pontuacao(mao, carta_mesa_virada_para_cima=True):
    pontos = sum([valor_carta(carta) for carta in mao])
    num_as = mao.count('A')
    
    # Se a carta da mesa está virada para cima, incluí-la no cálculo apenas se for a pontuação do jogador
    if carta_mesa_virada_para_cima and mao is not cartas_mesa:
        pontos += valor_carta(mao[-1])  # Use a última carta da mão, que é a última adicionada
        if mao[-1] == 'A':
            num_as += 1
    
    while pontos > 21 and num_as:
        pontos -= 10
        num_as -= 1
        
    return pontos

def risco(pontos_mesa):
    if pontos_mesa >= 17 and pontos_mesa <= 21:
        return 0  # Não há risco se a mesa já tem uma pontuação segura
    elif pontos_mesa > 21:
        return 100  # Risco máximo se a mesa já estourou
    else:
        return 40  # Risco moderado se a mesa está entre 17 e 21

def probabilidade_melhorar_mao(cartas_jogador):
    cartas_possiveis = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    cartas_na_mao = [carta for carta in cartas_jogador if carta in cartas_possiveis]
    cartas_restantes = [carta for carta in cartas_possiveis if carta not in cartas_na_mao]
    
    # Calcular a pontuação atual
    pontuacao_atual = pontuacao(cartas_jogador)
    
    # Filtrar apenas as cartas que melhoram a pontuação
    cartas_que_melhoram = [carta for carta in cartas_restantes if pontuacao_atual + valor_carta(carta) <= 21]

    return cartas_que_melhoram

def decidir_jogada(pontos_jogador, pontos_mesa, cartas_jogador):
    cartas_possiveis = probabilidade_melhorar_mao(cartas_jogador)

    if pontos_mesa >= pontos_jogador and risco(pontos_mesa) < 40:
        return "Pedir mais uma carta", cartas_possiveis
    elif cartas_possiveis and risco(pontos_mesa) > 40:
        return "Pedir mais uma carta", cartas_possiveis
    else:
        return "Parar", cartas_possiveis

def mostrar_cartas_possiveis(cartas_possiveis):
    print("Cartas que pode tirar para não estourar os 21:", cartas_possiveis)

def menu_continuar_jogando():
    resposta = input("\nDeseja continuar jogando? (s/n): ")
    return resposta.lower() == 's'

# Exemplo de uso
while True:
    cartas_jogador, cartas_mesa = obter_cartas()

    pontos_jogador = pontuacao(cartas_jogador)
    pontos_mesa = pontuacao(cartas_mesa, carta_mesa_virada_para_cima=False)  # A carta da mesa está virada para baixo

    decisao, cartas_possiveis = decidir_jogada(pontos_jogador, pontos_mesa, cartas_jogador)

    print("\nPontuação do jogador:", pontos_jogador)
    print("Pontuação da mesa:", pontos_mesa)
    print("Decisão sugerida:", decisao)
    if decisao == "Parar":
        mostrar_cartas_possiveis(cartas_possiveis)
    if decisao == "Pedir mais uma carta":
        cartas_possiveis.append('A')  # Sempre adicionar 'A' às cartas possíveis
        print("Cartas que não estouram os 21:", cartas_possiveis)

    if not menu_continuar_jogando():
        break