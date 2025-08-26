#!/usr/bin/env python3
# coding: utf-8
"""
Script para gerar um cardápio semanal de segunda a sexta e enviar as
sugestões por e-mail. O cardápio inclui pratos variados inspirados em
cozinhas de diferentes regiões. Por exemplo, saladas frias de macarrão
são servidas frias ou em temperatura ambiente e podem incluir massas,
vegetais, queijos ou carne, temperadas com vinagre, azeite ou maionese【338744538200116†L162-L185】. Burritos e bowls mexicanos costumam ser
preparados com tortillas ou bowls de arroz e incluem ingredientes como
carne ou frango, arroz, feijão, legumes, queijo e condimentos como
salsa, guacamole e creme de leite【96831322378448†L229-L233】. Pratos indianos como
chana masala são curries de grão‑de‑bico cozidos em molho de tomates com
especiarias【523426067280116†L149-L165】. Saladas buddha bowl reúnem grãos como
quinoa ou arroz integral, leguminosas como grão‑de‑bico ou tofu e
vegetais variados em um prato equilibrado【20003254966233†L127-L133】. O script
seleciona aleatoriamente cinco pratos para formar o cardápio da semana.
"""

import os
import random
import smtplib
from email.message import EmailMessage
from datetime import date, timedelta

# Lista de opções de refeições para almoços de segunda a sexta.
MENU_OPTIONS = [
    {
        "name": "Salada de frango mediterrânea com quinoa",
        "description": "Frango grelhado servido sobre quinoa e folhas verdes com tomates, pepino, azeitonas e molho de limão e azeite."
    },
    {
        "name": "Stir‑fry asiático de tofu com legumes e macarrão de arroz",
        "description": "Tofu salteado em wok com brócolis, pimentões e cenoura, temperado com molho de soja e servido com macarrão de arroz."
    },
    {
        "name": "Burrito bowl mexicano com arroz integral, feijão preto e legumes",
        "description": "Tigela inspirada em burrito com arroz integral, feijão preto, milho, alface, tomate e guacamole."
    },
    {
        "name": "Salada de macarrão fria ao estilo italiano",
        "description": "Salada fria de macarrão fusilli com tomates-cereja, muçarela de bufala, manjericão e azeite de oliva."
    },
    {
        "name": "Chana masala com arroz integral e naan",
        "description": "Curry de grão‑de‑bico cozido em molho de tomates e especiarias, servido com arroz integral e pão naan."
    },
    {
        "name": "Buddha bowl de quinoa com grão‑de‑bico e legumes assados",
        "description": "Quinoa servida com grão‑de‑bico, abacate, legumes assados e molho de tahine."
    },
    {
        "name": "Quinoa com legumes e peixe grelhado",
        "description": "Quinoa colorida com pimentão, pepino e tomate acompanhada de filé de peixe grelhado."
    },
    {
        "name": "Wrap de frango com pesto e legumes grelhados",
        "description": "Tortilla recheada com frango grelhado, pesto de manjericão, berinjela e abobrinha grelhadas e salada."
    },
    {
        "name": "Taco bowl de carne magra com arroz de couve‑flor",
        "description": "Bowl mexicano com carne bovina magra, arroz de couve‑flor, feijão preto, pico de gallo e alface."
    },
    {
        "name": "Curry tailandês de vegetais com leite de coco",
        "description": "Curry de legumes variados cozidos em leite de coco e especiarias tailandesas, servido com arroz jasmine."
    },
]

# Dias da semana para o cardápio (em português)
DAYS = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]

def generate_weekly_menu() -> list:
    """Gera uma lista de cinco pratos aleatórios correspondentes aos dias da semana."""
    options = MENU_OPTIONS.copy()
    random.shuffle(options)
    selected = options[: len(DAYS)]
    menu_lines = []
    for day, item in zip(DAYS, selected):
        menu_lines.append(f"{day}: {item['name']} - {item['description']}")
    return menu_lines

def compose_email(menu_lines: list) -> tuple:
    """Compõe o assunto e corpo do e‑mail a partir do cardápio gerado."""
    today = date.today()
    # Calcular as datas de segunda e sexta para contextualizar o cardápio.
    # O script é executado aos domingos, então a segunda-feira é o dia seguinte.
    monday = today + timedelta(days=1)
    friday = monday + timedelta(days=4)
    subject = f"Cardápio semanal ({monday.strftime('%d/%m/%Y')} - {friday.strftime('%d/%m/%Y')})"
    body_lines = [
        "Olá!",
        "",
        "Segue o cardápio sugerido para a próxima semana:",
        "",
    ]
    body_lines.extend(menu_lines)
    body_lines.append("")
    body_lines.append("Bom apetite!")
    body = "\n".join(body_lines)
    return subject, body

def send_email(subject: str, body: str) -> None:
    """Envia o e‑mail com o cardápio usando credenciais SMTP fornecidas via variáveis de ambiente."""
    ssmtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SENDER_EMAIL", smtp_user)
    recipient = os.getenv("RECIPIENT_EMAIL")
    # Determine if SSL should be used based on port or environment variable
    use_ssl_env = os.getenv("SMTP_USE_SSL", "").lower() in {"1", "true", "yes"}
    if not smtp_host or not smtp_user or not smtp_password or not recipient:
        raise ValueError("Credenciais SMTP ou destinatário não configurados.")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        if smtp_port == 465 or use_ssl_env:
            # Connect using SSL (porta 465)
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        else:
            # Connect using STARTTLS (porta 587 ou outras)
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        raise RuntimeError("Falha de autenticação SMTP. Verifique usuário, senha ou senha de aplicativo.") from except smtplib.SMTPAuthenticationError as e:
        raise RuntimeError("Falha de autenticação SMTP. Verifique usuário, senha ou senha de aplicativo.") from e     server.send_message(msg)

def main() -> None:
    """Função principal para gerar o cardápio e enviar o e‑mail."""
    menu_lines = generate_weekly_menu()
    subject, body = compose_email(menu_lines)
    send_email(subject, body)

if __name__ == "__main__":
    main()
