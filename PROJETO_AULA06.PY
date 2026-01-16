tarefas = []

def adicionar_tarefa():
    nome = input("Nome da tarefa: ")
    descricao = input("Descrição: ")
    prioridade = int(input("Prioridade (1 = alta, 2 = média, 3 = baixa): "))
    categoria = input("Categoria: ")

    tarefa = {
        "nome": nome,
        "descricao": descricao,
        "prioridade": prioridade,
        "categoria": categoria,
        "concluida": False
    }

    tarefas.append(tarefa)
    print("✅ Tarefa adicionada com sucesso!\n")


def listar_tarefas():
    if not tarefas:
        print("⚠️ Nenhuma tarefa cadastrada.\n")
        return

    for i, tarefa in enumerate(tarefas):
        status = "✔️ Concluída" if tarefa["concluida"] else "❌ Pendente"
        print(f"{i} - {tarefa['nome']} | Prioridade: {tarefa['prioridade']} | Categoria: {tarefa['categoria']} | {status}")
    print()


def marcar_concluida():
    listar_tarefas()
    indice = int(input("Digite o número da tarefa concluída: "))

    if 0 <= indice < len(tarefas):
        tarefas[indice]["concluida"] = True
        print("🎉 Tarefa marcada como concluída!\n")
    else:
        print("❌ Índice inválido.\n")


def filtrar_por_prioridade():
    prioridade = int(input("Digite a prioridade (1, 2 ou 3): "))
    for tarefa in tarefas:
        if tarefa["prioridade"] == prioridade:
            print(tarefa["nome"], "-", tarefa["categoria"])
    print()


def filtrar_por_categoria():
    categoria = input("Digite a categoria: ")
    for tarefa in tarefas:
        if tarefa["categoria"].lower() == categoria.lower():
            print(tarefa["nome"], "- Prioridade:", tarefa["prioridade"])
    print()


def menu():
    while True:
        print("📋 GERENCIADOR DE TAREFAS")
        print("1 - Adicionar tarefa")
        print("2 - Listar tarefas")
        print("3 - Marcar tarefa como concluída")
        print("4 - Filtrar por prioridade")
        print("5 - Filtrar por categoria")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_tarefa()
        elif opcao == "2":
            listar_tarefas()
        elif opcao == "3":
            marcar_concluida()
        elif opcao == "4":
            filtrar_por_prioridade()
        elif opcao == "5":
            filtrar_por_categoria()
        elif opcao == "0":
            print("👋 Saindo do programa...")
            break
        else:
            print("❌ Opção inválida.\n")


menu()
