# backend/app/services/usuario_service.py

import secrets
import string
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.email_utils import enviar_email
from app.core.security import hash_password
from app.integration.firebird_db.firebird import buscar_funcionario_por_nome
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioRegistro


def buscar_usuario_por_codigo(db: Session, codigo_funcionario: int):
    return (
        db.query(Usuario)
        .filter(Usuario.codigo_funcionario == codigo_funcionario)
        .first()
    )


def registrar_usuario(db: Session, usuario: UsuarioRegistro):
    codigo_funcionario = buscar_funcionario_por_nome(usuario.nome)

    if not codigo_funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    usuario_existente = buscar_usuario_por_codigo(db, codigo_funcionario)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já registrado")

    senha = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(4)
    )
    hashed = hash_password(senha)

    is_admin = usuario.nome.strip().lower() == "admin"

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        codigo_funcionario=codigo_funcionario,
        hashed_password=hashed,
        ativo=True,
        is_admin=is_admin,
        criado_em=datetime.utcnow(),
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    try:
        enviar_email(usuario.email, codigo_funcionario, senha)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Usuário criado, mas erro ao enviar e-mail: {str(e)}",
        )

    return {"mensagem": "Usuário registrado com sucesso", "senha_gerada": senha}


def criar_usuario(db: Session, usuario: UsuarioCreate):
    usuario_existente = buscar_usuario_por_codigo(db, usuario.codigo_funcionario)

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")

    hashed = hash_password(usuario.senha)

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        codigo_funcionario=usuario.codigo_funcionario,
        hashed_password=hashed,
        ativo=True,
        criado_em=datetime.utcnow(),
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


def alterar_senha(db: Session, usuario: Usuario, nova_senha: str):
    if not nova_senha or len(nova_senha) < 4:
        raise HTTPException(
            status_code=400, detail="A senha deve ter ao menos 4 caracteres."
        )

    usuario.hashed_password = hash_password(nova_senha)
    db.commit()
    return {"mensagem": "Senha alterada com sucesso"}
