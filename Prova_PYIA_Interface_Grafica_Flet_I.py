import flet as ft

def main(page: ft.Page):
    page.title = "Lista de Tarefas"

    
    campo_tarefa = ft.TextField(label="Digite a tarefa")

    
    lista_tarefas = ft.Column()

    
    def adicionar_tarefa(e):
        if campo_tarefa.value != "":
            lista_tarefas.controls.append(
                ft.Text(campo_tarefa.value)
            )
            campo_tarefa.value = ""
            page.update()

    
    botao_adicionar = ft.ElevatedButton(
        text="Adicionar",
        on_click=adicionar_tarefa
    )

    
    page.add(
        campo_tarefa,
        botao_adicionar,
        lista_tarefas
    )


ft.app(target=main)
