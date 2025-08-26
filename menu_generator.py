#!/usr/bin/env python3
# coding: utf-8
"""
Script para gerar um cardápio semanal de segunda a sexta e enviar as sugestões por e-mail. O cardápio inclui pratos variados inspirados em cozinhas de diferentes regiões. Por exemplo, saladas de macarrão são servidas frias ou em temperatura ambiente e podem incluir massas, vegetais, queijos ou carne, temperadas com vinagre, azeite ou maionese:contentReference[oaicite:0]{index=0}. Bowls mexicanos podem incluir arroz integral, feijão preto, milho, alface, tomate e guacamole:contentReference[oaicite:1]{index=1}. Chana masala é um curry de grão‑de‑bico cozido em molho de tomate com especiarias:contentReference[oaicite:2]{index=2}. Buddha bowls combinam grãos como quinoa ou arroz integral com leguminosas e vegetais:contentReference[oaicite:3]{index=3}. Este script seleciona aleatoriamente cinco pratos para compor o cardápio semanal.
"""
import os
import random
import smtplib
from email.message import EmailMessage
from datetime import date, timedelta

MENU_OPTIONS = [
    {"name": "Salada de frango mediterrânea com quinoa", "description": "Frango grelhado servido sobre quinoa com legumes e molho de limão e azeite."},
    {"name": "Stir‑fry asiático de tofu com legumes e macarrão de arroz", "description": "Tofu salteado com brócolis, pimentões e cenoura ao molho de soja."},
    {"name": "Burrito bowl mexicano com arroz integral, feijão preto e legumes", "description": "Tigela inspirada em burrito com arroz integral, feijão, milho, alface, tomate e guacamole."},
    {"name": "Salada de macarrão fria ao estilo italiano", "description": "Salada fria de macarrão fusilli com tomates‑cereja, muçarela de búfala e manjericão."},
    {"name": "Chana masala com arroz integral e naan", "description": "Curry de grão‑de‑bico cozido em molho de tomate e especiarias, servido com arroz integral e pão naan."},
    {"name": "Buddha bowl de quinoa com grão‑de‑bico e legumes assados", "description": "Quinoa servida com grão‑de‑bico, legumes assados e molho de tahine."},
    {"name": "Quinoa com legumes e peixe grelhado", "description": "Quinoa colorida com pimentão, pepino e filé de peixe grelhado."},
    {"name": "Wrap de frango com pesto e legumes grelhados", "description": "Tortilla recheada com frango grelhado, pesto e legumes grelhados."},
    {"name": "Taco bowl de carne magra com arroz de couve‑flor", "description": "Bowl mexicano de carne magra com arroz de couve‑flor, feijão preto, pico de gallo e alface."},
    {"name": "Curry tailandês de vegetais com leite de coco", "description": "Curry de vegetais variados com leite de coco e arroz jasmim."}
]

def generate_weekly_menu() -> list[str]:
    """Gera uma lista de cinco pratos aleatórios a partir de MENU_OPTIONS."""
    return random.sample([item["name"] for item in MENU_OPTIONS], 5)

def compose_email(menu_lines: list[str]) -> tuple[str, str]:
    """Compõe o assunto e o corpo do e‑mail com o cardápio da semana seguinte."""
    today = date.today()
    days_until_monday = (7 - today.weekday()) % 7 or 7
    next_monday = today + timedelta(days=days_until_monday)
    next_friday = next_monday + timedelta(days=4)
    subject = f"Cardápio semanal de {next_monday.strftime('%d/%m')} a {next_friday.strftime('%d/%m')}"
    body = "Olá!\n\nAqui está o cardápio sugerido para a próxima semana:\n\n"
    for i, dish in enumerate(menu_lines, start=1):
        body += f"{i}. {dish}\n"
    body += "\nBom apetite!\n"
    return subject, body

def send_email(subject: str, body: str) -> None:
    """Envia o e‑mail com o cardápio usando credenciais SMTP fornecidas via variáveis de ambiente."""
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SENDER_EMAIL", smtp_user)
    recipient = os.getenv("RECIPIENT_EMAIL")
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
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
    except smtplib.SMTPAuthenticationError as e:
        raise RuntimeError("Falha de autenticação SMTP. Verifique usuário, senha ou senha de aplicativo.") from e

def main() -> None:
    """Gera o cardápio e envia o e‑mail."""
    menu_lines = generate_weekly_menu()
    subject, body = compose_email(menu_lines)
    send_email(subject, body)

if __name__ == "__main__":
    main()

