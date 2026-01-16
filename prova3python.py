
produtos = {}


for i in range(5):
    nome = input(f"Digite o nome do produto {i+1}: ")
    preco = float(input(f"Digite o preço do produto {nome}: "))
    produtos[nome] = preco


total = sum(produtos.values())


print(f"O valor total da compra é: R$ {total:.2f}")