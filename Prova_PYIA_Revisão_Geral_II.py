import os

print("Rodando...")
print("Diretório atual:", os.getcwd())
print("Conteúdo:")

for item in os.listdir():
    print("-", item)
