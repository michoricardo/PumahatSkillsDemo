# PumahatSkillsDemo
Demostración de cómo usar y modificar skills como investigador OSINT

## Contenido

- `.claude/skills/what-leaked-about-you/`: skill para interpretar exposición en filtraciones. Incluye `scripts/variants.py` (variantes de correo, usuario y teléfono, sin red) y `scripts/intelx_search.py` (búsqueda en IntelX con tope de créditos, solo metadatos).
- `.claude/skills/platform-skill-check/`: skill para verificar si un username existe en otras plataformas (GitHub, GitLab, Hacker News, Lichess, Dev.to, Keybase, Telegram, Steam, Strava), vía `scripts/username_check.py`. Cada sitio está calibrado contra una cuenta real y una inventada — ver `reference/site-coverage.md` para el método por sitio y qué plataformas quedaron fuera a propósito (Reddit, Chess.com, y todo lo renderizado por JS). También documenta Epieos como pivote manual para verificar cuentas de Google ligadas a un correo.
- `cases/mock-*.md`: casos ficticios para practicar sin consultar nada real.
- `ETHICS.md`: alcance autorizado. Solo auto-auditoría o casos con autorización.

## Uso

1. Copia `.env.example` a `.env` y pon tu clave de IntelX. `.env` nunca se sube a git.
2. Abre Claude Code en esta carpeta e invoca `/what-leaked-about-you` con un caso mock o con un selector tuyo, o `/platform-skill-check` con un username para ver dónde más está registrado.
3. Guarda cualquier caso con datos reales en `cases/real/`, que está en `.gitignore`.
