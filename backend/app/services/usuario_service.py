from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.auth.auth_handler import criar_hash_senha
from app.auth.auth_firebird import verificar_funcionario_firebird


def criar_usuario(db: Session, dados: UsuarioCreate) -> Usuario:
    """
    Cria um novo usuário no banco local, com base no CDFUN.
    """
    funcionario = verificar_funcionario_firebird(dados.codigo_funcionario)
    if not funcionario:
        raise ValueError("Funcionário não encontrado ou inativo no Firebird")

    usuario = Usuario(
        codigo_funcionario=dados.codigo_funcionario,
        nome=funcionario["nome"],
        ativo=True,
        # email=funcionario["email"],  # pode usar se quiser
        hashed_password=criar_hash_senha(dados.senha)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def buscar_usuario_por_codigo(db: Session, codigo_funcionario: int) -> Usuario:
    return db.query(Usuario).filter(Usuario.codigo_funcionario == codigo_funcionario).first()