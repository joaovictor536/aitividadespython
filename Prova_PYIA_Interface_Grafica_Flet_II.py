import flet as flet

def main(app: flet.Page):
    app.title = "Formulário de Contato"

   
    campo_nome = flet.TextField(label="Nome")
    campo_email = flet.TextField(label="Email")
    campo_mensagem = flet.TextField(
        label="Mensagem",
        multiline=True
    )

    mensagem_confirmacao = flet.Text("")

   
    def enviar_formulario(e):
        if campo_nome.value and campo_email.value and campo_mensagem.value:
            mensagem_confirmacao.value = "Formulário enviado com sucesso!"
            mensagem_confirmacao.color = "green"
        else:
            mensagem_confirmacao.value = "Preencha todos os campos."
            mensagem_confirmacao.color = "red"

        app.update()

   
    botao_enviar = flet.Button(
        text="Enviar",
        on_click=enviar_formulario
    )

  
    app.add(
        campo_nome,
        campo_email,
        campo_mensagem,
        botao_enviar,
        mensagem_confirmacao
    )


flet.app(target=main)
