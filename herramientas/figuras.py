"""Genera las figuras del libro (SVG) en figuras/.

Uso, desde la raíz del libro:   python3 herramientas/figuras.py [--png]
Paleta categórica validada (orden fijo): azul, naranja, aguamarina, amarillo, magenta.
"""
import pathlib, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OUT = RAIZ / "figuras"; OUT.mkdir(exist_ok=True)

S = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
TINTA, TINTA2, GRIS, SUP = "#0b0b0b", "#52514e", "#d9d8d4", "#ffffff"
CAJA, CAJA2 = "#eef0f6", "#c9cfe0"

plt.rcParams.update({
    "font.family": ["Inter", "DejaVu Sans"], "font.size": 11,
    "svg.fonttype": "path", "figure.facecolor": SUP, "axes.facecolor": SUP,
})


def lienzo(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off")
    return fig, ax


def guardar(fig, nombre):
    fig.savefig(OUT / nombre, format="svg", bbox_inches="tight", pad_inches=0.15)
    if "--png" in sys.argv:
        pathlib.Path("/tmp/figpng").mkdir(exist_ok=True)
        fig.savefig(pathlib.Path("/tmp/figpng") / nombre.replace(".svg", ".png"), dpi=100, bbox_inches="tight")
    plt.close(fig); print("ok", nombre)


def caja(ax, x, y, w, h, texto, fc=CAJA, ec=CAJA2, tc=TINTA, fs=10, r=0.08, lw=1.2, peso="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if texto:
        ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, color=tc,
                linespacing=1.2, fontweight=peso)


def flecha(ax, a, b, color=TINTA2, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color=color, lw=1.3,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))


def pagina(ax, x, y, w, h, titulo):
    caja(ax, x, y, w, h, None, fc=SUP, ec=TINTA2, r=0.06)
    ax.add_patch(FancyBboxPatch((x, y + h - 0.35), w, 0.35, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=CAJA, ec=TINTA2, lw=1.2))
    ax.text(x + 0.15, y + h - 0.175, titulo, ha="left", va="center", fontsize=9, color=TINTA2)
    for i in range(5):
        ax.plot([x + 0.2, x + w - 0.2 - (0.5 if i % 2 else 0)], [y + h - 0.7 - i * 0.32] * 2,
                color=GRIS, lw=3, solid_capstyle="round")


# ------------------------------------------------------------------ U1
def u1_lateral():
    fig, ax = lienzo(9, 4.4, (0, 12), (0, 5.8))
    ax.text(2, 5.5, "Lectura vertical", ha="center", fontsize=12, fontweight="bold", color=TINTA)
    pagina(ax, 0.6, 1.2, 2.8, 3.6, "web-desconocida.com")
    flecha(ax, (3.7, 4.5), (3.7, 1.4), color=S[1])
    ax.text(2, 0.6, "Se analiza solo la propia página:\ndiseño, «quiénes somos», tono", ha="center",
            va="center", fontsize=9, color=TINTA2)

    ax.plot([5.0, 5.0], [0.3, 5.6], color=GRIS, lw=1)
    ax.text(8.5, 5.5, "Lectura lateral", ha="center", fontsize=12, fontweight="bold", color=TINTA)
    pagina(ax, 5.6, 1.6, 2.4, 3.0, "web-desconocida.com")
    destinos = [("¿Qué dicen otros\nde la fuente?", 4.0), ("¿Qué dicen otras\nfuentes de lo mismo?", 2.7),
                ("¿Cuál es la fuente\noriginal?", 1.4)]
    for i, (t, y) in enumerate(destinos):
        caja(ax, 9.0, y - 0.5, 2.9, 1.0, t, fc=SUP, ec=S[i if i < 2 else 2], lw=1.8, fs=9)
        flecha(ax, (8.0, 3.1), (9.0, y), color=S[i if i < 2 else 2])
    ax.text(8.5, 0.6, "Se sale de la página para contrastarla", ha="center", va="center", fontsize=9, color=TINTA2)
    guardar(fig, "u1_lateral.svg")


# ------------------------------------------------------------------ U2
def u2_booleanos():
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4))
    titulos = ["A Y B", "A O B", "A NO B"]
    for k, ax in enumerate(axes):
        ax.set_xlim(-2.1, 2.1); ax.set_ylim(-1.7, 1.75); ax.set_aspect("equal"); ax.axis("off")
        import numpy as np
        xs, ys = np.meshgrid(np.linspace(-2.1, 2.1, 500), np.linspace(-1.7, 1.75, 420))
        a = (xs + 0.55) ** 2 + ys ** 2 <= 1.1 ** 2
        b = (xs - 0.55) ** 2 + ys ** 2 <= 1.1 ** 2
        m = [a & b, a | b, a & ~b][k]
        ax.contourf(xs, ys, m.astype(float), levels=[0.5, 1.5], colors=[S[0]], alpha=0.55)
        for cx in (-0.55, 0.55):
            ax.add_patch(Circle((cx, 0), 1.1, fill=False, ec=TINTA2, lw=1.4))
        ax.text(-1.15, 0, "A", ha="center", va="center", fontsize=13, fontweight="bold", color=TINTA)
        ax.text(1.15, 0, "B", ha="center", va="center", fontsize=13, fontweight="bold", color=TINTA)
        ax.text(0, 1.45, titulos[k], ha="center", fontsize=12, fontweight="bold", color=TINTA)
        ax.text(0, -1.5, ["intersección: menos resultados", "unión: más resultados",
                          "diferencia: excluye B"][k], ha="center", fontsize=9, color=TINTA2)
    guardar(fig, "u2_booleanos.svg")


# ------------------------------------------------------------------ U4
def u4_apa():
    partes = [("Bates, M. J.", "autora", S[0]), (" (1989). ", "año", S[1]),
              ("The design of browsing and berrypicking techniques…", "título del artículo", S[2]),
              ("Online Review", "revista", S[3]), (", 13", "volumen", S[4]),
              ("(5)", "número", S[0]), (", 407-424.", "páginas", S[1]),
              (" https://doi.org/10.1108/eb024320", "DOI", S[2])]
    fig, ax = plt.subplots(figsize=(11, 2.9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    r = fig.canvas.get_renderer()
    filas = [partes[:3], partes[3:]]
    for f, fila in enumerate(filas):
        x = 0.01; y = 0.78 - f * 0.48
        for i, (txt, et, c) in enumerate(fila):
            estilo = "italic" if et in ("revista", "volumen") else "normal"
            t = ax.text(x, y, txt, fontsize=12, color=TINTA, va="center", style=estilo)
            bb = t.get_window_extent(renderer=r).transformed(ax.transData.inverted())
            ax.plot([bb.x0 + 0.003, bb.x1 - 0.003], [y - 0.09] * 2, color=c, lw=3, solid_capstyle="round")
            dy = 0.3 if et == "número" else 0.2
            if et == "número":
                ax.plot([(bb.x0 + bb.x1) / 2] * 2, [y - 0.11, y - 0.25], color=c, lw=1)
            ax.text((bb.x0 + bb.x1) / 2, y - dy, et, ha="center", fontsize=9, color=TINTA2)
            x = bb.x1
    guardar(fig, "u4_apa.svg")


# ------------------------------------------------------------------ U5
def u5_alucinacion():
    fig, ax = lienzo(10, 3.6, (0, 13.4), (0, 4.6))
    piezas = [("Un apellido\nfrecuente en el área", S[0]), ("Una revista real\ndel tema", S[1]),
              ("Un título con las\npalabras de la pregunta", S[2])]
    for i, (t, c) in enumerate(piezas):
        y = 3.4 - i * 1.25
        caja(ax, 0.2, y, 2.9, 0.95, t, fc=SUP, ec=c, lw=1.8, fs=9)
        flecha(ax, (3.1, y + 0.47), (4.2, 2.2), color=c)
    caja(ax, 4.0, 1.25, 4.3, 1.9, "García, L., y Pérez, M. (2021).\nEvaluación de fuentes en\n"
         "estudiantes universitarios.\nRevista Española de Documentación\nCientífica, 44(2). doi:10.xxxx/…",
         fs=8.5)
    ax.text(6.15, 3.4, "Referencia verosímil generada", ha="center", fontsize=9.5, color=TINTA2)
    flecha(ax, (8.1, 2.2), (9.2, 2.2))
    caja(ax, 9.2, 1.45, 2.3, 1.5, "Verificación en\nCrossref, OpenAlex\no la base de datos", fs=9,
         fc=SUP, ec=TINTA2)
    flecha(ax, (11.5, 2.2), (12.1, 2.2))
    ax.add_patch(Circle((12.7, 2.2), 0.55, fc="#fde5e1", ec="#c0392b", lw=1.8))
    ax.text(12.7, 2.2, "✕", ha="center", va="center", fontsize=18, color="#a52a1a", fontweight="bold")
    ax.text(12.7, 1.25, "No encontrada", ha="center", fontsize=9.5, color=TINTA)
    ax.text(6.15, 0.55, "Ejemplo inventado a propósito para esta figura", ha="center", fontsize=8.5,
            color=TINTA2, style="italic")
    guardar(fig, "u5_alucinacion.svg")


# ------------------------------------------------------------------ U6
def u6_declaracion():
    fig, ax = lienzo(10, 2.9, (0, 13.2), (0, 3.6))
    tarjetas = [("1", "¿Qué herramienta?", "nombre y versión"), ("2", "¿Para qué?", "revisar, resumir,\nproponer ideas…"),
                ("3", "¿En qué partes?", "apartados, tablas,\nfiguras"), ("4", "¿Cómo se revisó?", "qué aceptaste,\nqué comprobaste")]
    for i, (n, t, d) in enumerate(tarjetas):
        x = 0.2 + i * 3.3
        caja(ax, x, 1.05, 2.9, 2.2, None, fc=SUP, ec=S[i], lw=1.8)
        ax.add_patch(Circle((x + 0.45, 2.8), 0.27, fc=S[i], ec="none"))
        ax.text(x + 0.45, 2.8, n, ha="center", va="center", fontsize=11, color=TINTA, fontweight="bold")
        ax.text(x + 1.45, 2.25, t, ha="center", va="center", fontsize=10.5, color=TINTA, fontweight="bold")
        ax.text(x + 1.45, 1.6, d, ha="center", va="center", fontsize=9, color=TINTA2)
        if i < 3:
            flecha(ax, (x + 2.92, 2.15), (x + 3.28, 2.15))
    ax.text(6.6, 0.45, "La responsabilidad del trabajo es siempre de quien lo firma.", ha="center",
            fontsize=10, color=TINTA)
    guardar(fig, "u6_declaracion.svg")



# ------------------------------------------------------------------ U1 (2)
def u1_fuentes():
    fig, ax = lienzo(9.5, 4.2, (0, 13), (0, 5.4))
    niveles = [("Terciarias", "catálogos, bases de datos,\nenciclopedias: ayudan a encontrar", S[2]),
               ("Secundarias", "revisiones, manuales, noticias:\nanalizan o resumen", S[1]),
               ("Primarias", "artículos de investigación, datos,\nleyes, entrevistas: información original", S[0])]
    for i, (t, d, c) in enumerate(niveles):
        y = 3.6 - i * 1.5; ancho = 3 + i * 1.6; x0 = 3.2 - ancho / 2 + 0.5
        caja(ax, x0, y, ancho, 1.2, t, fc=c, ec=c, tc=TINTA, fs=11, peso="bold")
        ax.text(7.2, y + 0.6, d, va="center", fontsize=9.5, color=TINTA2)
        if i < 2: flecha(ax, (x0 + ancho / 2, y), (x0 + ancho / 2, y - 0.28))
    ax.text(0.1, 0.15, "Las flechas indican el camino que debes recorrer: de la fuente que encuentras a la original.", fontsize=9, color=TINTA2, style="italic")
    guardar(fig, "u1_fuentes.svg")


# ------------------------------------------------------------------ U2 (2)
def u2_precision():
    import numpy as np
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
    casos = [("Búsqueda estrecha (muchos AND)", 0.35, "alta precisión,\nbaja exhaustividad"),
             ("Búsqueda amplia (muchos OR)", 0.95, "baja precisión,\nalta exhaustividad")]
    rng = np.random.default_rng(3)
    pts = rng.uniform(-1, 1, size=(160, 2)); pert = (pts[:, 0] + 0.2) ** 2 + pts[:, 1] ** 2 < 0.35
    for ax, (t, r, nota) in zip(axs, casos):
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.4, 1.2); ax.set_aspect("equal"); ax.axis("off")
        rec = (pts[:, 0] - 0.0) ** 2 + (pts[:, 1]) ** 2 < r ** 2
        ax.add_patch(Circle((0, 0), r, fill=True, fc="#eaf1fb", ec=S[0], lw=1.8))
        ax.scatter(pts[pert, 0], pts[pert, 1], s=22, c=S[1], marker="o", label="pertinente", zorder=3)
        ax.scatter(pts[~pert, 0], pts[~pert, 1], s=14, c="#a3a29e", marker="x", label="no pertinente", zorder=3)
        tp, fp, fn = (rec & pert).sum(), (rec & ~pert).sum(), (~rec & pert).sum()
        ax.set_title(t, fontsize=11, color=TINTA)
        ax.text(0, -1.32, f"{nota}: P = {tp/(tp+fp):.2f} · E = {tp/(tp+fn):.2f}", ha="center", fontsize=9, color=TINTA2)
    fig.legend(*axs[0].get_legend_handles_labels(), loc="lower center", ncol=2, fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.12))
    fig.text(0.5, -0.02, "El círculo azul es lo que recupera la búsqueda. P = precisión; E = exhaustividad.", ha="center", fontsize=9, color=TINTA2)
    guardar(fig, "u2_precision.svg")


# ------------------------------------------------------------------ U3 (2)
def u3_espectro():
    fig, ax = lienzo(10, 2.8, (0, 13.4), (0, 3.4))
    pasos = [("Copia literal\nsin cita", "#c0392b"), ("Mosaico", "#e8663a"), ("Paráfrasis\nsin cita", "#eda100"),
             ("Paráfrasis\ncon cita", "#7fbf7b"), ("Cita textual\ncon referencia", "#1baf7a"), ("Ideas propias\ndistinguidas", "#0f8a5f")]
    for i, (t, c) in enumerate(pasos):
        caja(ax, 0.2 + i * 2.2, 1.2, 2.0, 1.3, t, fc=c, ec=c, tc=TINTA, fs=9.5, peso="bold")
    flecha(ax, (0.2, 0.8), (13.2, 0.8))
    ax.text(0.2, 0.35, "Plagio", fontsize=10, color=TINTA, fontweight="bold")
    ax.text(13.2, 0.35, "Uso ético", fontsize=10, color=TINTA, fontweight="bold", ha="right")
    ax.text(6.7, 2.95, "Del plagio al uso ético de las fuentes", ha="center", fontsize=11, color=TINTA)
    guardar(fig, "u3_espectro.svg")


def u3_licencias():
    filas = ["CC BY", "CC BY-SA", "CC BY-ND", "CC BY-NC", "CC BY-NC-SA", "CC BY-NC-ND"]
    cols = ["Copiar y\ndistribuir", "Uso\ncomercial", "Obras\nderivadas", "Misma\nlicencia"]
    m = [[1, 1, 1, 0], [1, 1, 1, 2], [1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 1, 2], [1, 0, 0, 0]]
    fig, ax = plt.subplots(figsize=(8, 4.2)); ax.axis("off"); ax.set_xlim(0, 6.2); ax.set_ylim(0, 7.4)
    for j, c in enumerate(cols): ax.text(2.4 + j * 1.0, 6.9, c, ha="center", va="center", fontsize=9.5, color=TINTA, fontweight="bold")
    for i, f in enumerate(filas):
        y = 5.9 - i * 0.95
        ax.add_patch(FancyBboxPatch((0.05, y - 0.4), 6.0, 0.8, boxstyle="round,pad=0,rounding_size=0.05", fc=CAJA if i % 2 == 0 else SUP, ec="none"))
        ax.text(0.2, y, f, va="center", fontsize=10.5, color=TINTA, fontweight="bold")
        for j, v in enumerate(m[i]):
            simb, col = {1: ("✓ sí", "#0f6b45"), 0: ("✗ no", "#a52a1a"), 2: ("obligatoria", "#7a5a00")}[v]
            if j == 3 and v == 0: simb, col = ("no exige", TINTA2)
            ax.text(2.4 + j * 1.0, y, simb, ha="center", va="center", fontsize=9.5, color=col)
    ax.text(0.05, 0.05, "Todas exigen reconocer la autoría (BY). SA: compartir igual · NC: no comercial · ND: sin obras derivadas.", fontsize=8.5, color=TINTA2)
    guardar(fig, "u3_licencias.svg")


# ------------------------------------------------------------------ U5 (2)
def u5_siguiente():
    fig, ax = lienzo(10, 3.4, (0, 13.4), (0, 4.4))
    caja(ax, 0.2, 1.7, 4.6, 1.0, "«La biblioteca ofrece …»", fc=SUP, ec=TINTA2, fs=11)
    flecha(ax, (4.8, 2.2), (5.8, 2.2))
    caja(ax, 5.8, 1.6, 2.2, 1.2, "Modelo de\nlenguaje", fs=10.5, peso="bold")
    flecha(ax, (8.0, 2.2), (8.8, 2.2))
    cands = [("libros", 0.46), ("acceso", 0.31), ("servicios", 0.15), ("café", 0.05), ("dragones", 0.03)]
    for i, (w, p) in enumerate(cands):
        y = 4.0 - i * 0.6
        ax.text(9.0, y, w, va="center", fontsize=10, color=TINTA)
        ax.add_patch(FancyBboxPatch((10.5, y - 0.18), 2.6 * p / 0.46, 0.36, boxstyle="round,pad=0,rounding_size=0.04", fc=S[0], ec="none"))
        ax.text(10.55 + 2.6 * p / 0.46, y, f" {int(p*100)} %", va="center", fontsize=9, color=TINTA2)
    ax.text(6.7, 0.3, "El modelo no consulta hechos: estima qué fragmento es más probable y repite el proceso.\nProbabilidades inventadas para ilustrar la idea.",
            ha="center", fontsize=9, color=TINTA2)
    guardar(fig, "u5_siguiente.svg")


# ------------------------------------------------------------------ U6 (2)
def u6_riesgos():
    fig, ax = lienzo(9.5, 4.6, (0, 13), (0, 5.8))
    niveles = [("Inaceptable", "prohibido: puntuación social, manipulación dañina", "#c0392b"),
               ("Alto", "requisitos estrictos: educación, empleo, servicios esenciales", "#e8663a"),
               ("Transparencia", "informar: asistentes conversacionales, deepfakes", "#eda100"),
               ("Mínimo", "sin obligaciones específicas: filtros de spam, videojuegos", "#1baf7a")]
    for i, (t, d, c) in enumerate(niveles):
        y = 4.5 - i * 1.25; ancho = 2.6 + i * 1.1; x0 = 3.0 - ancho / 2
        ax.add_patch(FancyBboxPatch((x0, y), ancho, 1.05, boxstyle="round,pad=0,rounding_size=0.06", fc=c, ec=SUP, lw=2))
        ax.text(3.0, y + 0.52, t, ha="center", va="center", fontsize=10.5, color=TINTA, fontweight="bold")
        ax.text(6.6, y + 0.52, d, va="center", fontsize=9.5, color=TINTA2)
    ax.text(0.2, 0.05, "Reglamento (UE) 2024/1689: las obligaciones crecen con el riesgo.", fontsize=9, color=TINTA2, style="italic")
    guardar(fig, "u6_riesgos.svg")


def u1_sift():
    fig, ax = lienzo(10, 3.2, (0, 16), (0, 5))
    pasos = [("Stop", "Para y pregúntate\nqué sabes de la fuente"), ("Investigate", "Investiga quién\npublica (lectura lateral)"), ("Find", "Busca mejor\ncobertura"), ("Trace", "Rastrea la afirmación\nhasta el original")]
    for i, (t, st) in enumerate(pasos):
        x = 0.3 + i * 4
        ax.add_patch(FancyBboxPatch((x, 0.5), 3.4, 3.9, boxstyle="round,pad=0,rounding_size=0.15", fc=S[i], ec="none", alpha=0.18))
        ax.text(x + 1.7, 3.6, t[0], ha="center", fontsize=26, fontweight="bold", color=S[i] if i != 3 else "#9a6a00")
        ax.text(x + 1.7, 2.65, t, ha="center", fontsize=11.5, fontweight="bold", color=TINTA)
        ax.text(x + 1.7, 1.45, st, ha="center", va="center", fontsize=9.5, color=TINTA2, linespacing=1.2)
        if i < 3: flecha(ax, (x + 3.45, 2.45), (x + 3.95, 2.45))
    guardar(fig, "u1_sift.svg")


def u3_parafrasis():
    fig, ax = lienzo(10, 2.8, (0, 16), (0, 4.4))
    pasos = [("1. Leer", "y comprender\nel original"), ("2. Cerrar", "el texto\noriginal"), ("3. Escribir", "de memoria con tu\nestructura y palabras"), ("4. Comparar", "significado y\nredacción"), ("5. Citar", "siempre\nla fuente")]
    for i, (t, st) in enumerate(pasos):
        x = 0.25 + i * 3.15
        caja(ax, x, 0.6, 2.7, 3.0, "", fc="#d6e6f8" if i < 4 else "#d3efe3")
        ax.text(x + 1.35, 2.7, t, ha="center", fontsize=11.5, fontweight="bold", color=TINTA)
        ax.text(x + 1.35, 1.5, st, ha="center", va="center", fontsize=9.5, color=TINTA2, linespacing=1.2)
        if i < 4: flecha(ax, (x + 2.72, 2.1), (x + 3.13, 2.1))
    guardar(fig, "u3_parafrasis.svg")


if __name__ == "__main__":
    u1_lateral(); u2_booleanos(); u4_apa(); u5_alucinacion(); u6_declaracion()
    u1_fuentes(); u2_precision(); u3_espectro(); u3_licencias(); u5_siguiente(); u6_riesgos(); u1_sift(); u3_parafrasis()
