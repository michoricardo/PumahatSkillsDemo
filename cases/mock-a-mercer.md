# Caso mock: a.mercer@example.com

**Todo es ficticio.** Sirve para demostrar la interpretación del skill sin consultar
ningún servicio real ni tocar datos de nadie. Autorización: auto-auditoría simulada.

Objetivo: auditar la exposición del cliente ficticio Ada Mercer.

## Resultados "devueltos" por las fuentes

| # | Fuente | Breach atribuido | Fecha del breach | Data classes / campos | Notas |
|---|---|---|---|---|---|
| 1 | HIBP | ForoJuegosMX | 2016-03 | email, username (`merce_ada`), IP, hash MD5 sin sal | Verificado y atribuido. Username que el cliente había olvidado |
| 2 | HIBP | AppFitnessLatam | 2019-08 | email, nombre, fecha de nacimiento, hash bcrypt | Verificado. bcrypt: las contraseñas no circularon en masa |
| 3 | HIBP | Paste anónimo | 2021-01 | email | Sin breach nombrado. Solo aparición en un paste |
| 4 | Servicio comercial (mock) | "TiendaRetail" | 2022-05 | email, nombre, dirección postal | La tienda nunca reconoció un incidente. Columnas sin datos de pedidos. La misma dirección aparece en dos data brokers |

## Datos adicionales para la demo

- Handle recuperado del registro 1: `merce_ada`. Seguiría a `hunt-a-handle`, que no está incluido en este repo.
- Contraseña de prueba para el paso de Pwned Passwords: `password123`. Es un ejemplo público y notoriamente común, no pertenece a nadie.

## Qué debería producir el skill

- Registros 1 y 2: **Confirmed** o **Probable**, con la lista de servicios como mapa de cuentas.
- Registro 3: **Unconfirmed**. Existe la aparición, pero no hay atribución.
- Registro 4: **Rejected**. Scrape de agregador relabelado como breach, con el razonamiento anotado.
- Ninguna credencial usada en ningún sitio.
