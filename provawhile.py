

numero_secreto = 7
tentativas = 0
limite_tentativas = 3

while tentativas < limite_tentativas:
    palpite = int(input("Tente adivinhar o número (entre 1 e 10): "))
    tentativas += 1

    if palpite == numero_secreto:
        print(" Parabéns Você acertou o número!")
        break
else:
    print("Suas tentativas acabaram. O número era 7. Tente novamente na próxima!")
