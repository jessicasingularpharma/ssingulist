# backend/app/services/usuario_service.py

from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.auth.auth_handler import gerar_hash_senha
from app.integration.firebird.erp_client import verificar_funcionario_firebird


def buscar_usuario_por_codigo(db: Session, codigo_funcionario: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.codigo_funcionario == codigo_funcionario).first()


def criar_usuario(db: Session, usuario_data: UsuarioCreate) -> Usuario:
    funcionario = verificar_funcionario_firebird(usuario_data.codigo_funcionario)
    if not funcionario:
        raise ValueError("Funcionário não encontrado no sistema ERP (Firebird)")

    usuario_existente = buscar_usuario_por_codigo(db, usuario_data.codigo_funcionario)
    if usuario_existente:
        raise ValueError("Usuário já registrado")

    novo_usuario = Usuario(
        codigo_funcionario=usuario_data.codigo_funcionario,
        nome=usuario_data.nome,
        email=usuario_data.email,
        hashed_password=gerar_hash_senha(usuario_data.senha),
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario