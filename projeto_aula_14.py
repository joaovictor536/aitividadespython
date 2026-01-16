import flet as ft
import re
from datetime import datetime, date


# =========================
# CLASSES
# =========================

class Pessoa:
    def __init__(self, nome, telefone, email):
        self.nome = nome.strip()
        self.telefone = telefone.strip()
        self.email = email.strip().lower()

    def get_nome(self):
        return self.nome


class Cliente(Pessoa):
    contador_id = 1

    def __init__(self, nome, telefone, email):
        super().__init__(nome, telefone, email)
        self.id = Cliente.contador_id
        Cliente.contador_id += 1

    def get_id(self):
        return self.id

    def atualizar(self, nome, telefone, email):
        self.nome = nome.strip()
        self.telefone = telefone.strip()
        self.email = email.strip().lower()


class Quarto:
    def __init__(self, numero, tipo, preco_diaria):
        self.numero = numero
        self.tipo = tipo
        self.preco = preco_diaria
        self.disponivel = True

    def esta_disponivel(self):
        return self.disponivel

    def reservar(self):
        self.disponivel = False


class Reserva:
    def __init__(self, cliente, quarto, checkin, checkout, dias, total):
        self.cliente = cliente
        self.quarto = quarto
        self.checkin = checkin
        self.checkout = checkout
        self.dias = dias
        self.total = total


class GerenciadorDeReservas:
    def __init__(self):
        self.clientes = []
        self.quartos = []
        self.reservas = []

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def adicionar_quarto(self, quarto):
        self.quartos.append(quarto)

    def confirmar_reserva(self, reserva):
        reserva.quarto.reservar()
        self.reservas.append(reserva)

    def get_cliente_por_id(self, id_cliente):
        return next((c for c in self.clientes if c.get_id() == id_cliente), None)

    def get_quarto_por_numero(self, numero):
        return next((q for q in self.quartos if q.numero == numero), None)


# =========================
# CORES TEMA VERDE ESCURO
# =========================

VERDE_ESCURO = "#2E7D32"
VERDE_MEDIO = "#4CAF50"
VERDE_CLARO = "#81C784"
VERDE_FUNDO = "#E8F5E8"


# =========================
# FUNÇÃO PRINCIPAL
# =========================

def main(page: ft.Page):
    page.title = "Hotel Horizonte Belo 🏨"
    page.window_width = 650
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20
    page.bgcolor = VERDE_FUNDO

    gerenciador = GerenciadorDeReservas()

    # Quartos cadastrados (valores mais caros)
    gerenciador.adicionar_quarto(Quarto(101, "Single", 380))
    gerenciador.adicionar_quarto(Quarto(102, "Double", 520))
    gerenciador.adicionar_quarto(Quarto(103, "Suite", 890))

    # BANNER DO HOTEL (IMAGEM TOPO)
    banner_hotel = ft.Image(
        src="https://images.eu.ctfassets.net/og3b0tarlg4b/2V8VRBdkHdr1Fy5VBqR1Ns/c09d5019c48cb6827071899a628b2794/Eden_Rock.jpg",
        width=600,
        height=250,
        fit=ft.ImageFit.COVER,
        border_radius=ft.border_radius.all(15)
    )

    # IMAGEM DA PISCINA (RODAPÉ)
    imagem_pool = ft.Image(
        src="https://www.ccsiusa.com/wp-content/uploads/2016/06/Hotel-Pool-Resort-Design-Ideas.jpg",
        width=600,
        height=250,
        fit=ft.ImageFit.COVER,
        border_radius=ft.border_radius.all(15)
    )

    # CAMPOS E LISTAS
    nome = ft.TextField(label="Nome Completo", width=500)
    telefone = ft.TextField(label="Telefone", hint_text="(99) 99999-9999", width=500)
    email = ft.TextField(label="Email", width=500)

    clientes_dropdown = ft.Dropdown(label="Selecione Cliente", width=500, options=[])
    quartos_dropdown = ft.Dropdown(label="Quarto Disponível", width=500, options=[])

    checkin_field = ft.TextField(label="Check-in (dd/mm/aaaa)", read_only=True, width=500)
    checkout_field = ft.TextField(label="Check-out (dd/mm/aaaa)", read_only=True, width=500)

    lista_quartos = ft.Column(scroll=ft.ScrollMode.AUTO, height=120)
    lista_reservas = ft.Column(scroll=ft.ScrollMode.AUTO, height=200)

    # CONTROLES PARA GERENCIAR CLIENTES
    lista_clientes = ft.Column(scroll=ft.ScrollMode.AUTO, height=150)
    cliente_nome_edit = ft.TextField(label="Nome", width=500)
    cliente_telefone_edit = ft.TextField(label="Telefone", width=500)
    cliente_email_edit = ft.TextField(label="Email", width=500)
    cliente_selecionado_id = {"id": None}

    data_hoje = date.today()

    # MÁSCARA TELEFONE
    def mascara_telefone(e):
        valor = re.sub(r"\D", "", telefone.value or "")
        if len(valor) <= 11:
            if len(valor) > 6:
                telefone.value = f"({valor[:2]}) {valor[2:7]}-{valor[7:]}"
            elif len(valor) > 2:
                telefone.value = f"({valor[:2]}) {valor[2:]}"
            else:
                telefone.value = valor
        telefone.update()

    telefone.on_change = mascara_telefone

    # DATEPICKERS + VALIDAÇÃO
    def on_checkin(e):
        if e.control.value:
            if e.control.value.date() < data_hoje:
                page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Check-in não pode ser anterior a hoje!")))
                checkin_field.value = ""
            else:
                checkin_field.value = e.control.value.strftime("%d/%m/%Y")
            checkin_field.update()

    def on_checkout(e):
        if e.control.value:
            if e.control.value.date() < data_hoje:
                page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Check-out não pode ser anterior a hoje!")))
                checkout_field.value = ""
            else:
                checkout_field.value = e.control.value.strftime("%d/%m/%Y")
            checkout_field.update()

    checkin_picker = ft.DatePicker(on_change=on_checkin, first_date=data_hoje)
    checkout_picker = ft.DatePicker(on_change=on_checkout, first_date=data_hoje)

    # ATUALIZAR LISTAS DE QUARTOS E RESERVAS
    def atualizar_listas():
        lista_quartos.controls.clear()
        quartos_dropdown.options.clear()

        for quarto in gerenciador.quartos:
            status = "🟢 Disponível" if quarto.esta_disponivel() else "🔴 Ocupado"
            lista_quartos.controls.append(
                ft.Text(f"Quarto {quarto.numero} - {quarto.tipo} | R$ {quarto.preco:.2f}/dia | {status}")
            )
            if quarto.esta_disponivel():
                quartos_dropdown.options.append(
                    ft.dropdown.Option(str(quarto.numero), f"{quarto.numero} - {quarto.tipo}")
                )

        lista_reservas.controls.clear()
        for reserva in gerenciador.reservas[-5:]:
            lista_reservas.controls.append(
                ft.Text(
                    f"👤 {reserva.cliente.get_nome()} | 🛏️ Q{reserva.quarto.numero} | "
                    f"📅 {reserva.checkin} → {reserva.checkout} | 💰 R$ {reserva.total:.2f}"
                )
            )
        page.update()

    # ATUALIZAR LISTA DE CLIENTES
        
    def atualizar_lista_clientes():
        lista_clientes.controls.clear()

        for c in gerenciador.clientes:
            def selecionar_closure(cliente=c):
                def selecionar(_):
                    cliente_selecionado_id["id"] = cliente.get_id()
                    cliente_nome_edit.value = cliente.nome
                    cliente_telefone_edit.value = cliente.telefone
                    cliente_email_edit.value = cliente.email
                    page.update()
                return selecionar

            def excluir_closure(cliente=c):
                def excluir(_):
                    # Remove o cliente da lista
                    if cliente in gerenciador.clientes:
                        gerenciador.clientes.remove(cliente)

                    # Se o cliente excluído estava selecionado, limpa edição
                    if cliente_selecionado_id["id"] == cliente.get_id():
                        cliente_selecionado_id["id"] = None
                        cliente_nome_edit.value = ""
                        cliente_telefone_edit.value = ""
                        cliente_email_edit.value = ""

                    # Atualiza lista visual de clientes
                    atualizar_lista_clientes()

                    # Atualiza dropdown de clientes das reservas
                    clientes_dropdown.options.clear()
                    for cli in gerenciador.clientes:
                        clientes_dropdown.options.append(
                            ft.dropdown.Option(str(cli.get_id()), cli.get_nome())
                        )

                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Cadastro excluído.")))
                    page.update()
                return excluir

            lista_clientes.controls.append(
                ft.Row(
                    [
                        ft.Text(f"ID {c.get_id()} | {c.get_nome()} | {c.telefone} | {c.email}"),
                        ft.TextButton("Editar", on_click=selecionar_closure()),
                        ft.TextButton(
                            "Excluir",
                            on_click=excluir_closure(),
                            style=ft.ButtonStyle(color="red")
                        ),
                    ]
                )
            )

        page.update()


    # CADASTRAR CLIENTE
    def cadastrar_cliente(e):
        if not all([nome.value, telefone.value, email.value]):
            nome.error_text = telefone.error_text = email.error_text = "Preencha todos os campos"
            page.update()
            return

        if not re.match(r"\(\d{2}\)\s?\d{4,5}-\d{4}", telefone.value):
            telefone.error_text = "Formato: (99) 99999-9999"
            page.update()
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email.value):
            email.error_text = "Email inválido"
            page.update()
            return

        for campo in [nome, telefone, email]:
            campo.error_text = None

        cliente = Cliente(nome.value, telefone.value, email.value)
        gerenciador.adicionar_cliente(cliente)

        clientes_dropdown.options.append(
            ft.dropdown.Option(str(cliente.get_id()), cliente.get_nome())
        )

        nome.value = telefone.value = email.value = ""
        page.update()
        atualizar_lista_clientes()

    # SALVAR EDIÇÃO DE CLIENTE
    def salvar_edicao_cliente(e):
        cid = cliente_selecionado_id["id"]

        if cid is None:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Selecione um cliente.")))
            return

        cliente = gerenciador.get_cliente_por_id(cid)
        if not cliente:
            return

        cliente.atualizar(
            cliente_nome_edit.value,
            cliente_telefone_edit.value,
            cliente_email_edit.value
        )

        atualizar_lista_clientes()

        clientes_dropdown.options.clear()
        for c in gerenciador.clientes:
            clientes_dropdown.options.append(
                ft.dropdown.Option(str(c.get_id()), c.get_nome())
            )

        page.show_snack_bar(ft.SnackBar(content=ft.Text("✅ Cliente atualizado")))
        page.update()

    # EXCLUIR ÚLTIMA RESERVA
    def excluir_ultima_reserva(e):
        if not gerenciador.reservas:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Não há reservas para excluir.")))
            return

        ultima = gerenciador.reservas.pop()
        ultima.quarto.disponivel = True
        atualizar_listas()
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Última reserva excluída.")))

    # RESERVA (DIALOG)
    def abrir_dialog_reserva(e):
        if not clientes_dropdown.value:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Cadastre um cliente primeiro!")))
            return
        if not quartos_dropdown.value:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Selecione um quarto disponível!")))
            return
        if not all([checkin_field.value, checkout_field.value]):
            page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Selecione as datas!")))
            return

        try:
            data1 = datetime.strptime(checkin_field.value, "%d/%m/%Y").date()
            data2 = datetime.strptime(checkout_field.value, "%d/%m/%Y").date()

            if data1 < data_hoje:
                page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Check-in não pode ser anterior a hoje!")))
                return
            if data2 < data_hoje:
                page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Check-out não pode ser anterior a hoje!")))
                return
            if data2 <= data1:
                page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Check-out deve ser após check-in!")))
                return

            dias = (data2 - data1).days
            if dias <= 0:
                page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Período inválido!")))
                return

            quarto = gerenciador.get_quarto_por_numero(int(quartos_dropdown.value))
            if not quarto or not quarto.esta_disponivel():
                page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Quarto não disponível!")))
                return

            total = dias * quarto.preco
            cliente = gerenciador.get_cliente_por_id(int(clientes_dropdown.value))

            confirma_dialog = ft.AlertDialog(
                modal=True,
                shape=ft.RoundedRectangleBorder(radius=20),
                title=ft.Text("Confirmar Reserva", size=20),
                content=ft.Column([
                    ft.Text(f"👤 Cliente: {cliente.get_nome()}", size=16),
                    ft.Text(f"🛏️ Quarto: {quarto.numero} ({quarto.tipo})", size=16),
                    ft.Text(f"📅 {checkin_field.value} → {checkout_field.value}", size=16),
                    ft.Divider(),
                    ft.Text(
                        f"📊 {dias} diárias x R$ {quarto.preco:.2f} = R$ {total:.2f}",
                        size=18,
                        weight=ft.FontWeight.BOLD
                    )
                ]),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda _: page.close(confirma_dialog)),
                    ft.ElevatedButton(
                        "Confirmar",
                        on_click=lambda _: (
                            gerenciador.confirmar_reserva(
                                Reserva(cliente, quarto, checkin_field.value, checkout_field.value, dias, total)
                            ),
                            page.close(confirma_dialog),
                            atualizar_listas(),
                            page.show_snack_bar(
                                ft.SnackBar(
                                    content=ft.Text(f"✅ Reserva confirmada! R$ {total:.2f}"),
                                    bgcolor=VERDE_MEDIO
                                )
                            )
                        )
                    )
                ]
            )

            page.open(confirma_dialog)

        except Exception:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("❌ Erro nos dados! Verifique tudo!")))

    # LAYOUT
    page.add(
        banner_hotel,
        ft.Text(
            "Hotel Horizonte Belo",
            size=28,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        ),
        ft.Divider(),

        ft.Text("📋 Quartos Disponíveis", weight=ft.FontWeight.BOLD),
        lista_quartos,

        ft.Divider(),
        ft.Text("👤 Cadastrar Cliente", weight=ft.FontWeight.BOLD),
        nome,
        telefone,
        email,
        ft.ElevatedButton(
            "➕ Cadastrar",
            on_click=cadastrar_cliente,
            width=500,
            bgcolor=VERDE_CLARO,
            color="white"
        ),

        ft.Divider(),
        ft.Text("👥 Gerenciar Clientes", weight=ft.FontWeight.BOLD),
        ft.Text("Lista de clientes cadastrados:"),
        lista_clientes,
        ft.Text("Editar cliente selecionado:", weight=ft.FontWeight.BOLD),
        cliente_nome_edit,
        cliente_telefone_edit,
        cliente_email_edit,
        ft.ElevatedButton(
            "💾 Salvar edição",
            on_click=salvar_edicao_cliente,
            width=500,
            bgcolor=VERDE_CLARO,
            color="white"
        ),

        ft.Divider(),
        ft.Text("📅 Nova Reserva", weight=ft.FontWeight.BOLD),
        clientes_dropdown,
        quartos_dropdown,
        checkin_field,
        ft.ElevatedButton(
            "📅 Check-in",
            on_click=lambda _: page.open(checkin_picker),
            width=500,
            bgcolor=VERDE_CLARO,
            color="white"
        ),
        checkout_field,
        ft.ElevatedButton(
            "📅 Check-out",
            on_click=lambda _: page.open(checkout_picker),
            width=500,
            bgcolor=VERDE_CLARO,
            color="white"
        ),
        ft.ElevatedButton(
            "💳 RESERVA",
            on_click=abrir_dialog_reserva,
            width=500,
            bgcolor=VERDE_ESCURO,
            color="white"
        ),

        ft.Divider(),
        ft.Text("📄 Últimas Reservas", weight=ft.FontWeight.BOLD),
        lista_reservas,
        ft.ElevatedButton(
            "🗑️ Excluir última reserva",
            on_click=excluir_ultima_reserva,
            width=500,
            bgcolor="red",
            color="white"
        ),
        ft.Divider(),
        imagem_pool
    )

    page.overlay.extend([checkin_picker, checkout_picker])
    atualizar_listas()
    atualizar_lista_clientes()


ft.app(target=main)
