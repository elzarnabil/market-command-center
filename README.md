# 📊 Market Command Center

Dashboard financiero autónomo que actualiza datos de mercado automáticamente usando **GitHub Actions** y **Yahoo Finance** (100% gratuito, sin API key).

## 🚀 Cómo desplegarlo en 5 minutos

### 1. Crear el repositorio en GitHub
```bash
git init
git add .
git commit -m "🚀 Initial commit — Market Command Center"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/market-command-center.git
git push -u origin main
```

### 2. Activar GitHub Pages
1. Ve a tu repositorio → **Settings** → **Pages**
2. En **Source** selecciona: `Deploy from a branch`
3. Branch: `gh-pages` / Folder: `/ (root)`
4. Haz clic en **Save**

### 3. Dar permisos al workflow
1. Ve a **Settings** → **Actions** → **General**
2. En *Workflow permissions* selecciona: ✅ **Read and write permissions**
3. Haz clic en **Save**

### 4. Lanzar primer fetch manual
1. Ve a **Actions** → `📊 Actualizar Datos de Mercado`
2. Haz clic en **Run workflow** → **Run workflow**
3. Espera ~60 segundos

¡Listo! Tu dashboard estará disponible en:
```
https://TU_USUARIO.github.io/market-command-center/
```

---

## ⚙️ Cómo funciona

```
┌─────────────────────────────────────────────────────┐
│  GitHub Actions (cron automático)                   │
│                                                     │
│  Lunes-Viernes cada 30 min, 7:00–23:00 UTC         │
│       ↓                                             │
│  scripts/fetch_data.py                              │
│  → Yahoo Finance API (gratuita, sin clave)          │
│  → Guarda en data/market.json                       │
│  → Commit + push al repo                            │
│  → Deploy a GitHub Pages                            │
└─────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────┐
│  Usuario visita la web                              │
│  index.html carga data/market.json (instantáneo)   │
│  Si quiere datos más frescos → botón "ACTUALIZAR"  │
│  (hace fetch live a Yahoo Finance via proxies CORS) │
└─────────────────────────────────────────────────────┘
```

## 📁 Estructura de archivos

```
market-command-center/
├── index.html                  ← Dashboard principal
├── data/
│   └── market.json             ← Datos auto-generados por GitHub Actions
├── scripts/
│   └── fetch_data.py           ← Script Python que obtiene datos
├── .github/
│   └── workflows/
│       └── update-market.yml   ← Automatización (cron schedule)
└── README.md
```

## 🔄 Frecuencia de actualización

| Horario | Frecuencia |
|---------|-----------|
| Lun-Vie 7:00–23:00 UTC | Cada 30 minutos |
| Sáb-Dom | 2 veces al día (cripto) |
| Manual | Siempre disponible via "Run workflow" |

## 💡 Fuentes de datos (todas gratuitas)

| Activo | Fuente |
|--------|--------|
| S&P 500, NASDAQ, IBEX, VIX | Yahoo Finance (sin key) |
| BTC/USD | Yahoo Finance (sin key) |
| Oro, WTI, EUR/USD, DXY | Yahoo Finance (sin key) |
| UST 10Y, UST 2Y | Yahoo Finance (sin key) |
| Análisis IA | Claude API (requiere tu key en el frontend) |

## ⚠️ Notas importantes

- **Yahoo Finance** puede cambiar su API sin previo aviso. Si los datos dejan de funcionar, abre un issue.
- El análisis IA con Claude **requiere** que el usuario tenga su API key configurada en el código (o uses un backend propio). Los datos de mercado son 100% gratuitos.
- GitHub Actions tiene **2.000 minutos gratuitos/mes** en repos públicos (ilimitados). Para repos privados, son 2.000 min/mes en el plan free.

## 🛠️ Personalización

Para añadir más activos, edita `SYMBOLS` en `scripts/fetch_data.py` y en `index.html`:
```python
# scripts/fetch_data.py
SYMBOLS = {
    "aapl": "AAPL",      # Apple
    "msft": "MSFT",      # Microsoft
    # ...
}
```
