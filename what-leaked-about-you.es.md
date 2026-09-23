# What Leaked About You — traducción al español explicada

> **Traducción y adaptación** del skill `what-leaked-about-you` de [useosint/osint-skills](https://github.com/useosint/osint-skills), publicado bajo licencia **MIT** (© useosint). Se tradujo al español con explicaciones sencillas; los nombres de comandos, rutas de archivo, banderas y bloques de código se dejan igual que en el original.
>
> Fuente: https://skillsagentes.com/skills/useosint/osint-skills/what-leaked-about-you.md

---

## 🧒 Explicado en una frase

Cuando una página web sufre un **hackeo**, los datos de sus usuarios (correo, usuario, contraseña, fecha de registro…) terminan circulando por internet. Este skill le enseña a tu asistente de IA a **revisar si tus datos aparecen en esas filtraciones**, a **entender qué significa cada dato**, y sobre todo a **nunca usar una contraseña filtrada para entrar a ningún lado**.

---

## Ficha rápida

| Dato | Valor |
|---|---|
| Autor | useosint |
| Licencia | MIT |
| Repositorio | https://github.com/useosint/osint-skills |
| Archivos | 3 (todos texto markdown, 24 KB en total) |
| Permisos que pide | ninguno declarado |
| Coste de contexto | 153 tokens instalado, ~3k al activarse, ~6.1k con todos los archivos |

**Archivos del paquete:**

- `SKILL.md` — 12 KB (las instrucciones principales)
- `reference/record-fields.md` — 6 KB (cómo leer cada campo de un registro filtrado)
- `reference/source-catalogue.md` — 6 KB (qué servicio de consulta usar y cuándo)

---

## Instalación

Un skill es solo un conjunto de archivos de texto. Lo único que cambia entre agentes es la carpeta donde se guardan, y eso se indica con la bandera `--agent`. Si agregas `-g`, se instala para todos los proyectos de tu computadora.

```bash
# Claude Code
npx -y skills add useosint/osint-skills --skill what-leaked-about-you --agent claude-code
# Cursor
npx -y skills add useosint/osint-skills --skill what-leaked-about-you --agent cursor
# Codex
npx -y skills add useosint/osint-skills --skill what-leaked-about-you --agent codex
# Gemini CLI
npx -y skills add useosint/osint-skills --skill what-leaked-about-you --agent gemini
# Windsurf
npx -y skills add useosint/osint-skills --skill what-leaked-about-you --agent windsurf
# Cline
npx -y skills add useosint/osint-skills --skill what-leaked-about-you --agent cline
```

> ⚠️ Lee la sección **Análisis de seguridad** al final antes de correr cualquiera de estos comandos.

## Qué hace

- Revisa si un correo, usuario, teléfono o nombre aparece en filtraciones, usando HIBP (Have I Been Pwned), Pwned Passwords, DeHashed, IntelX y Snusbase.
- Explica qué significa cada dato del registro filtrado (servicio, fecha de registro, IP, usuario).
- Califica qué tan confiable es la filtración: **Confirmed**, **Probable**, **Unconfirmed** o **Rejected**.
- Detecta datos "falsos" o reciclados (combolists, filtraciones viejas revendidas, perfiles públicos que se hacen pasar por hackeo).
- Pasa los datos nuevos que encuentre a otros skills, como `hunt-a-handle` o `what-an-email-reveals`.

## Cuándo usarlo

- Para revisar si tu identidad (o la de un cliente que te autorizó) aparece en filtraciones.
- Para saber en qué servicios se registró una cuenta.
- Para interpretar una lista de credenciales filtradas.
- Para auditar datos personales tuyos o de un cliente.

## Frases que lo activan

- "¿Este correo aparece en alguna filtración de datos?"
- "Necesito auditar qué contraseñas mías circulan sin exponerlas"
- "Interpreta este dump de credenciales que encontré"
- "¿Este handle recuperado de una brecha es real o un combolist?"

## Antes de instalar

- Para búsquedas más allá de HIBP necesitas **claves de API de servicios de pago** (DeHashed, IntelX o Snusbase).

---

# SKILL.md (traducido)

## Qué se filtró sobre ti

Los datos de una filtración responden una pregunta que casi nada más responde fácilmente: **¿en qué servicios tenía cuenta esta persona?** Esa lista de servicios casi siempre vale más que las contraseñas del registro. Y las contraseñas son justo la parte que **nunca debes tocar**: usar una contraseña filtrada es acceso no autorizado (un delito), sin importar qué tan pública sea la filtración.

## Qué trae realmente un registro filtrado, y qué importa

Un registro filtrado es simplemente **una fila de la tabla de usuarios** de un servicio. Campos típicos: correo, usuario, contraseña cifrada (hash) o, en casos malos, en texto plano, fecha de registro, último inicio de sesión, IP al registrarse, nombre visible, fecha de nacimiento, dirección, preguntas de seguridad, y lo que sea que ese servicio guardaba.

**Los datos "de contexto" valen más que las contraseñas, siempre:**

| Campo | Por qué importa (en sencillo) |
|---|---|
| Qué servicio | Prueba que la persona tenía cuenta ahí, algo difícil de saber de otra forma |
| Fecha de registro | Ubica a la persona en el tiempo; si abrió varias cuentas en fechas cercanas, probablemente son de la misma persona |
| Usuario en el registro | Un nombre de usuario que no conocías. Se pasa directo a `hunt-a-handle` |
| IP de registro o último acceso | Ubicación aproximada y, más útil, si era una conexión de casa o de un servidor |
| Nombre, fecha de nacimiento, dirección | Datos para comprobar en otras fuentes. **Nunca** los tomes como verdad absoluta |
| *Patrón* de la contraseña | Sirve como pista para relacionar cuentas. **Nunca** para escribirla en un formulario de inicio de sesión |

Explicación campo por campo: [reference/record-fields.md](reference/record-fields.md) (traducido más abajo).

## Qué fuente usar

| Lo que tienes | Usa | Por qué |
|---|---|---|
| Un correo y quieres saber en qué servicios estuvo | Have I Been Pwned | Revisado a mano, sin duplicados, te dice el nombre de la filtración y qué tipo de datos incluía. **No** te da contraseñas |
| Una contraseña que ya tienes (tuya o de alguien que te autorizó) | La API de rango de HIBP Pwned Passwords | Te dice si esa contraseña circula en filtraciones **sin enviarla** |
| Necesitas los valores reales de los campos, o buscar por usuario, teléfono, IP o nombre | Servicios comerciales con clave de API | Es la única forma de "entrar" a los registros en vez de solo saber si existes en ellos |
| Una filtración que está circulando ahora mismo | `find-leaks-in-the-wild` | Sitios de pegado (pastes), foros y canales, antes de que alguien la indexe |

**Have I Been Pwned (HIBP)** es el punto de partida por defecto. Revisan cada filtración antes de cargarla y etiquetan qué tipos de datos contenía, así que si apareces ahí, significa algo. La búsqueda web de un correo es gratis; la API requiere clave y permite revisar muchos correos o un dominio entero. A propósito **no** entrega contraseñas.

**Pwned Passwords** vale la pena entenderlo bien, porque su diseño es lo importante. Funciona así, en sencillo:

1. Tu computadora convierte la contraseña en un "código" (hash SHA-1) **localmente**.
2. Solo se envían los **primeros 5 caracteres** de ese código al servicio.
3. El servicio te regresa **todos** los códigos que empiezan igual, con cuántas veces se ha visto cada uno.
4. Tu computadora compara localmente si el tuyo está en la lista.

El servicio **nunca sabe** qué contraseña consultaste. Por eso es seguro usarlo con contraseñas que legítimamente te pertenecen, y es la herramienta correcta para autoauditarte o para ayudar a un cliente a corregir sus contraseñas.

**Servicios comerciales con clave** — DeHashed, IntelX y Snusbase son los más usados. En qué se diferencian:

- Buscan registro por registro usando muchos tipos de dato (usuario, teléfono, IP, nombre, no solo correo) y te regresan los valores. Son el "motor para saltar" de un dato a otro.
- Amplitud contra calidad: los que tienen más datos también meten más basura (combolists); los más cuidados se pierden cosas. Debes saber de qué lado está tu fuente.
- Algunos indexan documentos, pastes, páginas de la darkweb y archivos filtrados, no solo tablas de usuarios. Se parecen más a un buscador de material filtrado que a una base de datos de filtraciones.

Comparación de acceso y cobertura: [reference/source-catalogue.md](reference/source-catalogue.md) (traducido más abajo).

## La regla que no tiene excepciones

**Nunca uses una credencial filtrada para iniciar sesión en nada.** Ni para "confirmar que la cuenta existe". Ni en una cuenta de prueba. Ni en la cuenta de la persona aunque un cliente te haya dado permiso de palabra. Probar contraseñas robadas (credential stuffing) es acceso no autorizado según las leyes de delitos informáticos de casi todos los países, y que la contraseña sea pública **no te defiende** — ver [../../ETHICS.md](../../ETHICS.md).

Lo mismo aplica a acciones derivadas: no intentes restablecer contraseñas, no uses respuestas de preguntas de seguridad recuperadas, y no pruebes una contraseña recuperada en otro servicio para ver si la reutilizó. La reutilización se **deduce** de datos que ya tienes; nunca se **prueba**.

## Lo realmente útil: hacer la lista de servicios

Usa la lista de filtraciones como un **mapa de cuentas**. Si un correo aparece en un foro de videojuegos, una app de ejercicio y un sitio de citas regional, eso te da tres plataformas para investigar, tres fechas de registro y muchas veces tres nombres de usuario — cada uno es un punto de partida para `hunt-a-handle`. Los propios servicios describen a la persona: su profesión, región, idioma e intereses, cosas que ninguna página de perfil te diría.

Los patrones de contraseña sirven como pista si se manejan bien. Si dos registros de identidades distintas tienen la **misma contraseña rara** (larga, que no es palabra de diccionario, claramente personal), eso es una coincidencia significativa. Lo anotas como observación, **tachando o cifrando la contraseña** en tus notas. Una contraseña común (`password1`, teclas seguidas del teclado, un equipo de fútbol) no relaciona nada: miles de personas la usan. Lo que cuenta es qué tan única es; la prueba es la coincidencia, no la contraseña.

## Descifrar hashes queda fuera

Los registros suelen traer contraseñas cifradas (hashes): MD5 o SHA-1 sin sal en filtraciones viejas, y métodos más seguros en las nuevas. A veces verás contraseñas en texto plano (el servicio no las cifró) o con cifrado reversible (alguien eligió mal).

Anota el **tipo** de hash: indica la época de la filtración y qué tan buena era la seguridad del servicio, lo cual sí es útil en un análisis de riesgo. **Y ahí te detienes.** Descifrar un hash produce una contraseña que no puedes usar, así que ese trabajo no tiene ningún resultado legítimo. La excepción es una autoauditoría o una evaluación de seguridad autorizada donde el dueño de la contraseña es tu cliente, e incluso ahí la API de rango responde la pregunta sin descifrar nada.

## Dónde se suele fallar

- **Contaminación por combolists.** La mayoría de las "grandes filtraciones" son combolists: mezclas de credenciales de muchas fuentes, sin duplicados, revueltas y sin decir de dónde vienen. Aparecer en una solo dice que ese par correo/contraseña salió *en algún lado*, no de qué servicio. Eso destruye el valor principal: saber en qué servicios estuvo la persona.
- **Filtraciones recicladas o inventadas.** Datos viejos se reempaquetan con otro nombre y se venden como nuevos. Algunas "filtraciones" son totalmente falsas, o son perfiles públicos recolectados (scraping) que se venden como hackeo. Revisa si el servicio supuestamente afectado alguna vez reconoció un incidente, y si la estructura del registro tiene sentido para ese servicio.
- **La fecha del hackeo no es la fecha de la filtración.** Hay tres fechas distintas: cuándo se robaron los datos, cuándo empezaron a circular y cuándo tu fuente los cargó. Pueden separarse por años. "Aparece en una filtración de la fecha X" dice que la cuenta existía antes de X, no que estuviera activa entonces.
- **No aparecer no prueba nada.** Puede ser que no hackearon sus servicios, que la filtración nunca se publicó, o que tu fuente no la tiene.
- **Confundir scraping con hackeo.** Un conjunto armado recolectando perfiles públicos no es prueba de que hubo un ataque, y reportarlo así es un error que te quita credibilidad.
- **Datos que ya no son de la misma persona.** Los correos y teléfonos se abandonan y se reasignan. Un registro de hace diez años puede ser de alguien totalmente distinto.
- **Coincidencia entre proveedores que parece confirmación.** Si dos servicios comerciales dicen lo mismo, muchas veces es porque cargaron la misma filtración.

## Cómo calificar la confianza

- **Confirmed** — el registro está en una fuente curada que verificó y atribuyó la filtración, los campos coinciden con el servicio indicado, y otro dato del registro lo confirma de forma independiente.
- **Probable** — está en una base comercial seria, atribuido claramente a un servicio y con campos coherentes.
- **Unconfirmed** — aparece en un combolist, en una filtración sin origen, o es una sola fila sin otro dato que lo confirme. Reporta que existe, pero di claramente que no se sabe de dónde viene.
- **Rejected** — el servicio supuesto nunca tuvo un incidente creíble, los campos no coinciden con lo que ese servicio guarda, o son datos públicos reetiquetados.

Califica **la filtración**, no solo el registro. Una filtración bien atribuida hace más creíble cada fila; una recopilación anónima hace menos creíble cada fila.

## Ejemplo práctico

Autoauditoría para un cliente con el correo `a.mercer@example.com`. HIBP devuelve cuatro filtraciones. Una es de un foro grande de hace varios años, con correos, usuarios, IPs y contraseñas cifradas.

El usuario en esa filtración es `merce_ada`, que el cliente había olvidado. Ese usuario se pasa a `hunt-a-handle` y aparecen dos cuentas activas que el cliente no sabía que seguían públicas. **Ese fue el resultado más valioso, y no tuvo nada que ver con contraseñas.**

El callejón sin salida: un servicio comercial devuelve una quinta "filtración" atribuida a una tienda, con una dirección de casa. La tienda nunca reportó un incidente, los campos no parecen una tabla de pedidos, y la misma dirección aparece en dos registros de brokers de datos. Conclusión: son datos recopilados de brokers disfrazados de filtración. Se excluye del reporte y se anota el porqué.

Corrección: las contraseñas que el cliente todavía usa se revisan con la API de rango de Pwned Passwords, así que **ninguna contraseña sale de la computadora**. No se usa ninguna credencial de ningún registro en ningún lado.

## Siguientes pasos (a qué skill pasar cada dato)

| Dato nuevo | Skill |
|---|---|
| Usuario recuperado de un registro | `hunt-a-handle` |
| Correos adicionales | `what-an-email-reveals` |
| Teléfono en un registro | `whose-number-is-this` |
| IP de registro | `find-exposed-servers` |
| Nombre, fecha de nacimiento, dirección | `find-anyone`, `dig-through-data-brokers` |
| Dominio de empresa en muchos registros | `x-ray-a-company` |
| La filtración misma, circulando | `find-leaks-in-the-wild` |
| Lista de servicios como mapa de relaciones | `graph-the-network` |

## Notas legales y de manejo

Tener datos de filtraciones está regulado, y más estrictamente que casi cualquier otro material de OSINT. Bajo el GDPR (Europa) y la ley de protección de datos de Reino Unido, estos registros son datos personales —muchas veces de categoría especial— y procesarlos requiere una base legal, un plazo de conservación definido y demostrar que solo guardas lo mínimo. En algunos países, **tener** ciertos datos robados ya es delito, sin importar cómo los conseguiste. Varios servicios comerciales limitan por licencia para qué puedes usar sus datos; lee los términos antes de meter resultados en un reporte para un cliente.

En la práctica: saca solo los campos que necesitas, **no guardes contraseñas**, guarda el material del caso cifrado y con registro de quién accede, y bórralo en la fecha que definiste por escrito al inicio. Si trabajas con los datos **de la propia persona y con su permiso**, es la situación más limpia posible, y es la única en la que revisar una contraseña es apropiado.

---

# reference/record-fields.md (traducido)

## Cómo leer un registro filtrado, campo por campo

Un registro es una fila de la tabla de usuarios de alguien, que pudo haber sido copiada y alterada varias veces. Léelo como una fila de base de datos de origen desconocido, no como un hecho.

### Campos de identidad

**Correo.** La "llave" principal para comparar filtraciones. Normalízalo antes de comparar: todo en minúsculas y, en proveedores que los ignoran, quita los puntos y las `+etiquetas`, para que las variantes cuenten como un solo buzón. Dos registros que parecen de personas distintas muchas veces son de una sola. Un correo de empresa también fecha una relación laboral, lo cual suele ser más útil que la cuenta misma.

**Usuario.** Muchas veces el campo más valioso, porque es un dato que no tenías. Pásalo a `hunt-a-handle`. Un usuario de una filtración vieja es especialmente bueno: es de antes de que la persona empezara a cuidarse.

**Nombre visible / nombre real.** Lo escribió la persona al registrarse, nadie lo verificó y a veces es falso a propósito. Confírmalo antes de usarlo. Si un nombre poco común se repite en varias filtraciones sin relación, es una buena señal.

**Fecha de nacimiento.** Muchas veces falsa, sobre todo si el servicio pedía edad mínima: el 1 de enero y los años redondos aparecen demasiado. Una fecha que coincide en filtraciones independientes vale más que cualquier caso aislado.

**Dirección y teléfono.** Tómalos como históricos. Caducan rápido: la gente se muda y los números se reasignan. Pasa el teléfono a `whose-number-is-this`, pero llévate también la fecha.

### Campos de tiempo

**Fecha de registro.** El campo menos aprovechado. Ubica a la persona en el tiempo, indica desde cuándo usa ese servicio y, entre varias filtraciones, muestra "rachas" de registro. La gente abre cuentas en bloque: un trabajo nuevo, un celular nuevo, un interés nuevo. Esas rachas son evidencia de que varias cuentas son de la misma persona.

**Último acceso / última actividad.** Dice si la cuenta estaba viva cuando ocurrió la filtración, lo que separa una cuenta abandonada de una activa.

**Las tres fechas que no debes confundir:**

| Fecha | Qué significa |
|---|---|
| Fecha del hackeo (breach) | Cuándo se robaron los datos del servicio |
| Fecha de publicación / filtración | Cuándo empezaron a circular públicamente |
| Fecha de ingreso | Cuándo tu fuente los cargó |

Suelen estar separadas por años. Un registro de un hackeo de la fecha X prueba que la cuenta existía antes de X. No prueba que estuviera activa en X y no dice nada de hoy.

### Campos de red

**IP de registro / último acceso.** Ubicación aproximada en el mejor caso, y muchas veces errónea en redes móviles o de empresa. Lo más útil es **clasificarla**: ¿es internet de casa, datos móviles, un servidor de hosting, una VPN o Tor? Una IP de hosting al registrarse sugiere automatización u ocultamiento intencional. Más detalle con `find-exposed-servers`.

Dos cuentas con la misma IP poco común en el mismo periodo es una coincidencia importante. Dos cuentas con una IP compartida de operador móvil (CGNAT) no lo es.

### Campos de credenciales

Anota el tipo y **no los toques más**.

| Cómo estaba guardada | Qué te dice |
|---|---|
| Texto plano | El servicio no cifraba contraseñas. Negligencia grave, y dice mucho de la época y calidad del servicio |
| MD5 o SHA-1 sin sal | Viejo, débil y fácil de atacar a gran escala. Común en filtraciones antiguas |
| MD5 / familia SHA con sal | Mejor, pero aún no adecuado para contraseñas |
| Hash hecho para contraseñas (bcrypt, scrypt, Argon2, PBKDF2) | El servicio lo hizo bien. En la práctica, esas contraseñas no terminaron circulando masivamente |
| Cifrado reversible | Usaron cifrado donde debían usar hash. Quien tenga la llave puede recuperarlo todo |

El tipo de hash sí se puede reportar: describe qué tan segura era la plataforma y explica por qué una filtración produjo o no contraseñas utilizables.

Descifrar hashes queda fuera: produce una credencial que no puedes usar, así que no hay resultado legal. Excepción: una evaluación autorizada donde el dueño de la contraseña es tu cliente, y aun así la API de rango responde sin recuperar nada.

**Patrones de contraseña como análisis, nunca como entrada.** Si hay texto plano en material que legítimamente tienes, la *forma* de la contraseña es evidencia: una cadena rara repetida en dos registros de identidades distintas es un vínculo real. Anota la observación, tacha o cifra la contraseña en tus notas, y nunca la escribas en un formulario de acceso. Una contraseña común no vincula nada.

**Preguntas y respuestas de seguridad** son, en la práctica, datos personales permanentes: apellido de la madre, primera escuela, primera mascota. Ayudan a confirmar identidad, y son exactamente lo que un atacante necesita. Trátalas como el campo más sensible de la fila y **nunca** las uses para recuperar una cuenta.

### Campos de estructura y origen

**Fuente / nombre de la filtración.** El campo más importante. Si la fila no se puede atribuir a un servicio, solo tienes un par de credenciales y nada más: sin fecha de registro, sin pista. Las filas de combolists son justo eso, y por eso valen mucho menos de lo que parece.

**Orden de los campos.** Prueba rápida de autenticidad: ¿las columnas coinciden con lo que ese servicio guardaría? Una "filtración" de una tienda sin datos de pedidos, o de un foro con direcciones de casa, es motivo para dudar.

**Duplicados.** La misma identidad repetida en varias filtraciones suele ser una sola filtración reprocesada, no varios incidentes. Quita duplicados antes de contar, y nunca reportes un número de "filtraciones" sin revisar esto.

### Cómo registrar

Extrae solo los campos que necesitas. **No copies contraseñas** en tus notas. Para cada fila anota: nombre de la fuente, fecha de hackeo que esa fuente declara, servicio al que se atribuye, proveedor del que la obtuviste y fecha en que la obtuviste. Sin origen, un registro no es evidencia, y sin origen no puedes justificar tenerlo.

---

# reference/source-catalogue.md (traducido)

## Catálogo de fuentes de filtraciones

Las fuentes se diferencian en cuatro cosas que sí cambian tu resultado: **por qué dato puedes buscar**, **qué te regresan**, **qué tan revisados están los datos** y **qué te permiten sus términos**. Elige por eso, no por publicidad.

Los servicios y sus condiciones cambian. Verifica acceso y licencia antes de usar un resultado en un entregable.

### Los cuatro criterios

**Por qué puedes buscar.** Buscar solo por correo responde "¿se filtró esta dirección?". Buscar por usuario, teléfono, nombre, IP o dominio te permite "entrar" a los registros desde otros datos, y ahí suele estar lo valioso.

**Qué te regresan.** Unos solo dicen en qué filtración apareces y qué tipos de datos tenía. Otros te dan los valores de cada campo. Lo primero basta para hacer la lista de servicios; lo segundo se necesita para recuperar datos de identidad.

**Qué tan revisados están.** Las bases curadas verifican y atribuyen cada filtración antes de cargarla, así que un resultado significa algo y no aparecer también dice algo. Las que agregan todo meten combolists sin origen: encuentran más, pero con mucha menos precisión y sin poder decir de qué servicio vino.

**Acceso y licencia.** Búsqueda web gratis, API con clave, suscripción o licencia restringida a ciertos usos. Algunas licencias prohíben usar los datos para decisiones de empleo, renta o crédito, o exigen ser investigador acreditado. Léelas antes de entregar resultados a un cliente.

### Have I Been Pwned

La primera parada por defecto, y la única fuente popular que es deliberadamente conservadora con lo que entrega.

- Verifica y atribuye filtraciones antes de cargarlas, y etiqueta cada una con sus **tipos de datos** (correos, contraseñas, IPs, fechas de nacimiento, etc.). Los tipos de datos son el metadato más útil: te dicen qué buscar antes de buscarlo.
- Distingue filtraciones públicas de las **sensibles** (donde solo aparecer ya es dañino) y de las **no verificadas**, que marca como tales. Respeta esa diferencia al reportar.
- Búsqueda web gratis para un correo. La API requiere clave y permite búsquedas automatizadas y búsquedas de dominio completo verificadas por el dueño del dominio, que es la vía correcta para que una organización se audite.
- **No** regresa contraseñas ni valores de campos. Es una decisión de diseño, no una falla.
- También indexa pastes, lo que revela exposiciones que nunca se volvieron una filtración con nombre.

### Pwned Passwords y k-anonimato

Es un servicio aparte, y vale la pena entender cómo funciona porque es el modelo de cómo debería hacerse este tipo de consulta.

Conviertes la contraseña en hash SHA-1 **en tu computadora** y envías solo los **primeros 5 caracteres**. El servicio regresa todos los finales de hash que empiezan así y cuántas veces se ha visto cada uno. Tú comparas localmente.

Así el servicio nunca conoce la contraseña, ni el hash completo, ni cuál de los resultados te interesaba (eso es el "k-anonimato"). En la práctica:

- Es seguro usarlo con contraseñas que legítimamente tienes. Es la herramienta correcta para autoauditoría y para ayudar a un cliente.
- El número de apariciones es una señal: una contraseña vista muchas veces es común y no vincula nada; una vista una o dos veces es única.
- Responde "¿esta contraseña circula?", no "¿esta contraseña es de esta cuenta?". No revisa cuentas.
- Aunque no se envía la contraseña, sigues manejando una contraseña real en tu equipo. **No la guardes en logs ni la conserves.**

### Servicios comerciales con datos por registro

Se usan en toda la industria; requieren clave y son de pago. Se mencionan como ejemplos actuales, no como recomendación.

| Servicio | Su fuerte |
|---|---|
| DeHashed | Búsqueda amplia por muchos datos (correo, usuario, nombre, teléfono, IP, dirección, hash) y te regresa los valores. Lo usual cuando quieres partir de algo que no es un correo |
| IntelX | Indexa *material* filtrado, no solo tablas de usuarios: documentos, pastes, páginas de darkweb, capturas históricas. Más parecido a un buscador de fuentes filtradas y poco comunes |
| Snusbase | Búsqueda rápida en una base agregada de filtraciones, incluyendo por hash y campo de contraseña, orientada a sacar registros |

Precauciones para todos:

- **Que coincidan no es confirmación.** Los proveedores cargan las mismas filtraciones públicas. Si dos coinciden, probablemente tienen una sola fuente de origen.
- **La calidad del origen varía por registro**, no por proveedor. Un mismo servicio tiene filtraciones bien atribuidas y combolists anónimos. Revisa la atribución de cada registro.
- **Tus búsquedas quedan registradas.** El proveedor guarda lo que consultas. Asume que cada dato que buscas se conserva, y piensa qué implica eso en un caso delicado.
- **Restricciones de licencia**: muchas veces prohíben justo lo que los clientes quieren hacer con los datos. Revísalo antes de prometer algo.

### Fuentes cercanas

- Sitios de pastes, foros y canales de mensajería tienen filtraciones antes que cualquier indexador, y material que nunca se vuelve una filtración con nombre. Usa `find-leaks-in-the-wild`.
- Los brokers de datos son **otra cosa**: compilan registros públicos y datos comerciales, no hackeos. Útiles, pero nunca los reportes como filtración. Usa `dig-through-data-brokers`.
- Algunos CERT nacionales y reguladores publican avisos de filtraciones con incidente, fecha y tipo de datos. Es la atribución más confiable cuando existe; revísala antes de creer el origen que dice una filtración.

### Elegir rápido

- Lista de servicios a partir de un correo: HIBP.
- Saber si una contraseña tuya circula: API de rango de Pwned Passwords.
- Buscar por usuario, teléfono o nombre: un servicio comercial por registro.
- Saber si una filtración es real: primero el aviso de la propia empresa afectada, luego el del regulador, luego la atribución de una fuente curada, en ese orden.
- Algo que está circulando ahora: `find-leaks-in-the-wild`.

---

# 🔒 Análisis de seguridad

**Veredicto corto:** el skill en sí es **seguro** — son 3 archivos de texto, sin código ejecutable, sin dependencias y sin instrucciones ocultas. Los riesgos reales están en **cómo lo instalas** y en **qué datos le das al agente** cuando lo uses.

## ✅ Lo que revisé y está bien

| Revisión | Resultado |
|---|---|
| Archivos del skill | `SKILL.md`, `reference/record-fields.md` y `reference/source-catalogue.md`: los tres leídos completos. Solo texto markdown |
| Código que se ejecute solo | Ninguno. No hay scripts, hooks, `curl \| bash`, ni comandos que el agente deba correr automáticamente |
| Dependencias | Ninguna. El skill no instala paquetes |
| Instrucciones ocultas / prompt injection | No encontré ninguna. No le pide al agente ignorar reglas, enviar datos a terceros ni leer archivos de tu equipo |
| Permisos | No declara ninguno |
| Postura ética | Buena: prohíbe explícitamente usar contraseñas filtradas, descifrar hashes y recuperar cuentas |
| `install.sh` del repositorio | Revisado: solo crea enlaces simbólicos o copia carpetas a `~/.cursor/skills` o `~/.claude/skills`. No descarga nada, no usa `sudo`, no toca tu `.bashrc` |

## ⚠️ Riesgos a tener en cuenta

**1. El comando `npx -y` ejecuta código de internet sin preguntarte.**
`npx -y skills add ...` descarga y ejecuta el paquete de npm llamado `skills`, y la bandera `-y` salta la confirmación. Ese paquete **no** es de este autor ni forma parte del skill; no revisé su código. Si en algún momento ese paquete se compromete, el comando correría ese código en tu equipo. **Alternativa más segura:** como el skill son solo 3 archivos de texto, cópialos a mano a `~/.claude/skills/what-leaked-about-you/` (o la carpeta de tu agente) y listo.

**2. `install.sh` borra carpetas existentes con el mismo nombre.**
Usa `rm -rf "$dest"` antes de instalar cada skill. Si ya tenías un skill con el mismo nombre (por ejemplo uno tuyo modificado), lo pierde. Además instala **los 28 skills** del repo, no solo este.

**3. Modo symlink = actualizaciones sin revisión.**
Por defecto `install.sh` enlaza a la copia del repo, así que cada `git pull` cambia las instrucciones que sigue tu agente sin que las revises. Es un repositorio pequeño (4 estrellas, 1 autor). Usa `./install.sh --copy` o copia manual si quieres control.

**4. Nunca le pegues tus contraseñas al agente.**
El truco de Pwned Passwords protege tu contraseña frente a HIBP, **no** frente al chat: si escribes tu contraseña en la conversación, queda en el historial del agente. Hazlo tú directamente en https://haveibeenpwned.com/Passwords o con un gestor de contraseñas que tenga esa función.

**5. Tus búsquedas salen de tu equipo.**
Cada correo, teléfono o nombre que consultes se envía a HIBP, DeHashed, IntelX o Snusbase, y el propio skill advierte que los proveedores comerciales **guardan lo que buscas**. Las claves de API de esos servicios, si las configuras, también quedan disponibles para el agente.

**6. Manejar dumps de credenciales es riesgoso (técnica y legalmente).**
Frases como "interpreta este dump que encontré" implican descargar archivos de foros o canales dudosos, que pueden traer malware, y en algunos países tenerlos ya es delito. El skill enlaza a otros (`find-leaks-in-the-wild`, `find-anyone`) que no revisé; solo se activan si también los instalas.

## Recomendación

Si solo quieres saber **qué se filtró de ti**, no necesitas instalar nada: entra a https://haveibeenpwned.com con tu correo. Si sí quieres el skill, cópialo a mano (sin `npx -y` ni `install.sh`), no configures claves de pago a menos que las necesites, y úsalo solo con tus propios datos o los de alguien que te autorizó.

---

*Traducción y análisis basados en el contenido publicado el 22 de septiembre de 2026. Licencia original: MIT, © useosint. Esta traducción se ofrece "tal cual", sin garantía.*
