# Gestión de incapacidades

Aplicación en Python (Flask + SQLite) del procedimiento de incapacidades médicas de origen común y laboral, licencias de maternidad y paternidad.

## Cómo ejecutar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:5000

- Usuario: `admin`
- Contraseña: `admin123`

## Qué cubre

| Módulo | Numeral / paso | Qué hace |
|---|---|---|
| Recepción | 5.1.1 | Canales, aviso al jefe para reemplazo, registro |
| Verificación | 5.1.2 | Documentos por tipo, 3 días hábiles, segundo llamado |
| Transcripción | 5.2 / 5.2.1 | Plazos por EPS, canal portal o correo |
| Liquidación | 5.5.2 | 100% empresa (1-2), 67% EPS (3-90), 50% EPS (91-180) |
| Monitoreo | 5.5.3 | Hitos 90/120/150/180, rehabilitación, reintegros |
| Cobro | 5.4, pasos 8-11 | Transcrita, cobrada, rechazada, pagada |
| Cartera | 5.4.1, paso 15 | Cobro persuasivo y traslado a jurídica |
| Jurídico | 5.4.2 | Derecho de petición y tutela |
| Conciliación | 5.5 / 5.5.1, 12-13 | Cruce con tesorería y contabilidad |
| Nómina | — | Novedad con valor a cargo de la empresa |
| Ausentismo | paso 6 | Informe a SG-SST |
| Archivo | 5.3, paso 16 | Por entidad y fecha; destrucción de epicrisis |
| IA | cierre del PDF | Alertas y recomendaciones sobre la base |

## Pruebas

```bash
pytest -q
```

La base de datos local queda en `data/` (fuera de Git). Los certificados digitales en `archivos_digitales/`.




activar correo desde powershell:

$env:SMTP_HOST="smtp.gmail.com"
$env:SMTP_PORT="465"
$env:SMTP_USUARIO="tucorreo@gmail.com"
$env:SMTP_CLAVE="contraseña-de-aplicación"
python app.py