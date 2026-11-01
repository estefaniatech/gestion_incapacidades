from core.models import Incapacidad, Notificacion


class RepositorioIA:
    def resumen(self):
        items = Incapacidad.query.all()
        return {
            "total": len(items),
            "por_estado": _contar(items, "estado"),
            "por_tipo": _contar(items, "tipo"),
            "por_entidad": _contar(items, "entidad"),
            "valor_eps_pendiente": sum(i.valor_eps or 0 for i in items if i.estado not in {"pagada", "archivada", "dada_de_baja"}),
            "rechazos": [i for i in items if i.estado == "rechazada"],
            "avisos": Notificacion.query.order_by(Notificacion.enviada_en.desc()).limit(20).all(),
        }


def _contar(items, campo):
    acc = {}
    for i in items:
        clave = getattr(i, campo) or "N/A"
        acc[clave] = acc.get(clave, 0) + 1
    return acc
