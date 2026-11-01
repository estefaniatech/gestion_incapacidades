"""Conexión SQLAlchemy y creación de tablas."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        from core import models  # noqa: F401

        db.create_all()
        _sembrar_admin()


def _sembrar_admin():
    from werkzeug.security import generate_password_hash

    from config.estados import Rol
    from core.models import Usuario

    if Usuario.query.filter_by(usuario="admin").first():
        return
    admin = Usuario(
        usuario="admin",
        nombre="Administrador del sistema",
        email="admin@empresa.com",
        rol=Rol.ADMIN.value,
        password_hash=generate_password_hash("admin123"),
        activo=True,
    )
    db.session.add(admin)
    db.session.commit()
