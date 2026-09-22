# Caso mock: john.smith@example.com

**Todo es ficticio.** Los servicios, fechas y registros están inventados para la demo.
No se consultó ninguna fuente real. Autorización: ejercicio simulado.

## Resultados "devueltos" por las fuentes (simulados)

| # | Fuente | Breach atribuido | Fecha del breach | Campos | Notas |
|---|---|---|---|---|---|
| 1 | HIBP (mock) | ForoTechGlobal | 2014-06 | email, username `jsmith_88`, IP de signup, hash MD5 sin sal | Verificado y atribuido. IP de signup en un proveedor de hosting |
| 2 | HIBP (mock) | StreamBox | 2018-11 | email, nombre, fecha de nacimiento `1990-01-01`, hash bcrypt | Verificado y atribuido |
| 3 | Servicio comercial (mock) | "MegaCombo-2020" | 2020 | par email:contraseña | Combolist sin procedencia. La contraseña es `football1` |
| 4 | Servicio comercial (mock) | "ShopExpress" | 2023-02 | email, nombre, dirección, teléfono | La tienda niega el incidente. Sin datos de pedidos. La dirección aparece en un data broker |

## Interpretación esperada

| # | Grado | Razón |
|---|---|---|
| 1 | Probable | Atribuido a un servicio concreto y con campos coherentes. No llega a Confirmed porque nada lo corrobora con un segundo selector independiente |
| 2 | Probable | Atribuido y coherente. La fecha de nacimiento del 1 de enero de un año redondo se considera probablemente falsa |
| 3 | Unconfirmed | Combolist sin procedencia: no dice de qué servicio salió. La contraseña es común y no vincula a nadie |
| 4 | Rejected | Sin incidente reconocido, sin columnas de pedidos y con la misma dirección en un data broker. Scrape relabelado |
