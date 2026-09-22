# PumahatSkillsDemo
Demostración de cómo usar y modificar skills como investigador OSINT

## Contenido

- `.claude/skills/what-leaked-about-you/`: skill para interpretar exposición en filtraciones. Incluye `scripts/variants.py` (variantes de correo, usuario y teléfono, sin red) y `scripts/intelx_search.py` (búsqueda en IntelX con tope de créditos, solo metadatos).
- `cases/mock-*.md`: casos ficticios para practicar sin consultar nada real.
- `ETHICS.md`: alcance autorizado. Solo auto-auditoría o casos con autorización.

## Uso

1. Copia `.env.example` a `.env` y pon tu clave de IntelX. `.env` nunca se sube a git.
2. Abre Claude Code en esta carpeta e invoca `/what-leaked-about-you` con un caso mock o con un selector tuyo.
3. Guarda cualquier caso con datos reales en `cases/real/`, que está en `.gitignore`.
