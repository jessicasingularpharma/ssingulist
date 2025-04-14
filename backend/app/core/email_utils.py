import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def enviar_email(destinatario: str, codigo_funcionario: int, senha: str):
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_USER
    msg["To"] = destinatario
    msg["Subject"] = "Bem-vindo(a) ao Sistema de Suprimentos"

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <h2 style="color: #4CAF50;">Cadastro realizado com sucesso! 🎉</h2>
            <p>Olá,</p>
            <p>Seu cadastro no <strong>sistema de controle de suprimentos</strong> foi concluído com sucesso.</p>
            <p>Aqui estão seus dados de acesso:</p>
            <ul style="list-style: none; padding-left: 0;">
                <li><strong>Código do Funcionário:</strong> {codigo_funcionario}</li>
                <li><strong>Senha de Acesso:</strong> <code style="background-color:#eee; padding: 4px 8px; border-radius: 4px;">{senha}</code></li>
            </ul>
            <p style="color: #888;">Recomendamos que você altere sua senha após o primeiro login.</p>
            <br>
            <p>Atenciosamente,</p>
            <p><strong>Equipe de Suprimentos</strong></p>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_content, "html"))

    try:
        # ✅ Conexão segura com STARTTLS
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()  # Estabelece conexão
            server.starttls()  # Converte para TLS
            server.ehlo()  # Reestabelece após STARTTLS
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        raise Exception(f"Erro ao enviar e-mail: {str(e)}")
