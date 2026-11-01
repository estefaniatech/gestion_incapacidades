"""Punto de entrada del sistema de gestión de incapacidades."""

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from config import settings
from config.estados import Rol
from core.database import db, init_db
from core.models import Incapacidad, Usuario
from core.seguridad import login_requerido
from modulos.archivo.interfaz import bp as bp_archivo
from modulos.ausentismo.interfaz import bp as bp_ausentismo
from modulos.cartera.interfaz import bp as bp_cartera
from modulos.conciliacion.interfaz import bp as bp_conciliacion
from modulos.ia.interfaz import bp as bp_ia
from modulos.juridico.interfaz import bp as bp_juridico
from modulos.liquidacion.interfaz import bp as bp_liquidacion
from modulos.monitoreo.interfaz import bp as bp_monitoreo
from modulos.nomina.interfaz import bp as bp_nomina
from modulos.recepcion.interfaz import bp as bp_recepcion
from modulos.seguimiento_cobro.interfaz import bp as bp_cobro
from modulos.transcripcion.interfaz import bp as bp_transcripcion
from modulos.verificacion.interfaz import bp as bp_verificacion


def crear_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    init_db(app)

    for blueprint in [
        bp_recepcion,
        bp_verificacion,
        bp_transcripcion,
        bp_liquidacion,
        bp_monitoreo,
        bp_cobro,
        bp_cartera,
        bp_juridico,
        bp_conciliacion,
        bp_nomina,
        bp_ausentismo,
        bp_archivo,
        bp_ia,
    ]:
        app.register_blueprint(blueprint)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            usuario = Usuario.query.filter_by(usuario=request.form["usuario"], activo=True).first()
            if usuario and check_password_hash(usuario.password_hash, request.form["password"]):
                session["usuario"] = usuario.usuario
                session["nombre"] = usuario.nombre
                session["rol"] = usuario.rol
                return redirect(url_for("inicio"))
            flash("Credenciales inválidas.", "danger")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/")
    @login_requerido
    def inicio():
        items = Incapacidad.query.order_by(Incapacidad.fecha_recepcion.desc()).limit(15).all()
        conteo = {}
        for i in Incapacidad.query.all():
            conteo[i.estado] = conteo.get(i.estado, 0) + 1
        return render_template("inicio.html", items=items, conteo=conteo)

    @app.route("/usuarios", methods=["GET", "POST"])
    @login_requerido
    def usuarios():
        if session.get("rol") != Rol.ADMIN.value:
            flash("Solo el administrador puede gestionar usuarios.", "danger")
            return redirect(url_for("inicio"))
        if request.method == "POST":
            fila = Usuario(
                usuario=request.form["usuario"],
                nombre=request.form["nombre"],
                email=request.form["email"],
                rol=request.form["rol"],
                password_hash=generate_password_hash(request.form["password"]),
                activo=True,
            )
            db.session.add(fila)
            db.session.commit()
            flash("Usuario creado.", "success")
            return redirect(url_for("usuarios"))
        return render_template("usuarios.html", usuarios=Usuario.query.all(), roles=list(Rol))

    @app.errorhandler(403)
    def prohibido(_e):
        return render_template("error.html", mensaje="No tiene permiso para este módulo."), 403

    return app


app = crear_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
