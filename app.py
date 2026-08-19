from flask import Flask, render_template, Response, url_for, request
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)


# =========================================================
# CONFIGURACIÓN PARA PRODUCCIÓN
# =========================================================
# Ayuda a Flask a detectar correctamente HTTPS y el dominio
# cuando la página esté publicada detrás de un hosting/proxy.
# =========================================================

app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1,
    x_host=1
)


# =========================================================
# PÁGINA PRINCIPAL
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


# =========================================================
# ESPAÑOL
# =========================================================

@app.route("/es")
def inicio_es():
    return render_template("inicio_es.html")


@app.route("/es/salinas")
def salinas_es():
    return render_template("salinas_es.html")


@app.route("/es/ojos-del-salar")
def ojos_es():
    return render_template("ojos_es.html")


@app.route("/es/atardecer")
def atardecer_es():
    return render_template("atardecer_es.html")


@app.route("/es/humahuaca")
def humahuaca_es():
    return render_template("humahuaca_es.html")


# =========================================================
# ENGLISH
# =========================================================

@app.route("/en")
def inicio_en():
    return render_template("inicio_en.html")


@app.route("/en/salinas")
def salinas_en():
    return render_template("salinas_en.html")


@app.route("/en/ojos-del-salar")
def ojos_en():
    return render_template("ojos_en.html")


@app.route("/en/sunset")
def atardecer_en():
    return render_template("atardecer_en.html")


@app.route("/en/humahuaca")
def humahuaca_en():
    return render_template("humahuaca_en.html")


# =========================================================
# RELACIÓN ENTRE PÁGINAS ESPAÑOL / INGLÉS
# =========================================================

IDIOMAS = {

    "/": {
        "canonical": "index",
        "es": "inicio_es",
        "en": "inicio_en",
        "default": "index"
    },

    "/es": {
        "canonical": "inicio_es",
        "es": "inicio_es",
        "en": "inicio_en",
        "default": "index"
    },

    "/en": {
        "canonical": "inicio_en",
        "es": "inicio_es",
        "en": "inicio_en",
        "default": "index"
    },


    # =====================================================
    # SALINAS GRANDES
    # =====================================================

    "/es/salinas": {
        "canonical": "salinas_es",
        "es": "salinas_es",
        "en": "salinas_en",
        "default": "salinas_es"
    },

    "/en/salinas": {
        "canonical": "salinas_en",
        "es": "salinas_es",
        "en": "salinas_en",
        "default": "salinas_es"
    },


    # =====================================================
    # OJOS DEL SALAR
    # =====================================================

    "/es/ojos-del-salar": {
        "canonical": "ojos_es",
        "es": "ojos_es",
        "en": "ojos_en",
        "default": "ojos_es"
    },

    "/en/ojos-del-salar": {
        "canonical": "ojos_en",
        "es": "ojos_es",
        "en": "ojos_en",
        "default": "ojos_es"
    },


    # =====================================================
    # ATARDECER
    # =====================================================

    "/es/atardecer": {
        "canonical": "atardecer_es",
        "es": "atardecer_es",
        "en": "atardecer_en",
        "default": "atardecer_es"
    },

    "/en/sunset": {
        "canonical": "atardecer_en",
        "es": "atardecer_es",
        "en": "atardecer_en",
        "default": "atardecer_es"
    },


    # =====================================================
    # HUMAHUACA
    # =====================================================

    "/es/humahuaca": {
        "canonical": "humahuaca_es",
        "es": "humahuaca_es",
        "en": "humahuaca_en",
        "default": "humahuaca_es"
    },

    "/en/humahuaca": {
        "canonical": "humahuaca_en",
        "es": "humahuaca_es",
        "en": "humahuaca_en",
        "default": "humahuaca_es"
    }

}


# =========================================================
# CONFIGURACIÓN GLOBAL AUTOMÁTICA
# =========================================================
# Se agrega automáticamente a todos los HTML.
# NO hace falta modificar cada archivo.
# =========================================================

@app.after_request
def agregar_configuracion_global(response):

    if not response.content_type.startswith("text/html"):
        return response


    html = response.get_data(as_text=True)


    # =====================================================
    # FAVICON + MANIFEST + CONFIGURACIÓN GENERAL
    # =====================================================

    if "site.webmanifest" not in html:

        configuracion_general = f"""

    <!-- ================================================
         SOFITURISMO - CONFIGURACIÓN GLOBAL
    ================================================= -->

    <link
        rel="icon"
        href="{url_for('static', filename='favicon.svg')}"
        type="image/svg+xml"
    >

    <link
        rel="manifest"
        href="{url_for('static', filename='site.webmanifest')}"
    >

    <meta
        name="theme-color"
        content="#082d50"
    >

    <meta
        name="application-name"
        content="Sofiturismo"
    >

    <meta
        name="apple-mobile-web-app-title"
        content="Sofiturismo"
    >

    <meta
        name="apple-mobile-web-app-capable"
        content="yes"
    >

    <meta
        name="apple-mobile-web-app-status-bar-style"
        content="black-translucent"
    >

    <meta
        property="og:site_name"
        content="Sofiturismo"
    >

    <meta
        property="og:type"
        content="website"
    >

    <meta
        property="og:image"
        content="{url_for(
            'static',
            filename='img/portada.png',
            _external=True
        )}"
    >

"""

        html = html.replace(
            "</head>",
            configuracion_general + "\n</head>"
        )


    # =====================================================
    # SEO BILINGÜE
    # =====================================================

    pagina = IDIOMAS.get(request.path)


    if pagina and 'rel="canonical"' not in html:

        canonical_url = url_for(
            pagina["canonical"],
            _external=True
        )

        español_url = url_for(
            pagina["es"],
            _external=True
        )

        ingles_url = url_for(
            pagina["en"],
            _external=True
        )

        default_url = url_for(
            pagina["default"],
            _external=True
        )


        seo_idiomas = f"""

    <!-- ================================================
         SEO BILINGÜE
    ================================================= -->

    <link
        rel="canonical"
        href="{canonical_url}"
    >

    <link
        rel="alternate"
        hreflang="es-AR"
        href="{español_url}"
    >

    <link
        rel="alternate"
        hreflang="en"
        href="{ingles_url}"
    >

    <link
        rel="alternate"
        hreflang="x-default"
        href="{default_url}"
    >

    <meta
        property="og:url"
        content="{canonical_url}"
    >

"""

        html = html.replace(
            "</head>",
            seo_idiomas + "\n</head>"
        )


    # =====================================================
    # IDIOMA PARA OPEN GRAPH
    # =====================================================

    if request.path.startswith("/en"):

        idioma_og = """

    <meta
        property="og:locale"
        content="en_US"
    >

"""

    elif request.path.startswith("/es"):

        idioma_og = """

    <meta
        property="og:locale"
        content="es_AR"
    >

"""

    else:

        idioma_og = ""


    if idioma_og and 'property="og:locale"' not in html:

        html = html.replace(
            "</head>",
            idioma_og + "\n</head>"
        )


    response.set_data(html)

    return response


# =========================================================
# ROBOTS.TXT
# =========================================================

@app.route("/robots.txt")
def robots():

    sitemap_url = url_for(
        "sitemap",
        _external=True
    )


    contenido = f"""User-agent: *
Allow: /

Sitemap: {sitemap_url}
"""


    return Response(
        contenido,
        mimetype="text/plain"
    )


# =========================================================
# SITEMAP.XML
# =========================================================

@app.route("/sitemap.xml")
def sitemap():

    paginas = [

        # PRINCIPAL

        url_for(
            "index",
            _external=True
        ),


        # =================================================
        # ESPAÑOL
        # =================================================

        url_for(
            "inicio_es",
            _external=True
        ),

        url_for(
            "salinas_es",
            _external=True
        ),

        url_for(
            "ojos_es",
            _external=True
        ),

        url_for(
            "atardecer_es",
            _external=True
        ),

        url_for(
            "humahuaca_es",
            _external=True
        ),


        # =================================================
        # ENGLISH
        # =================================================

        url_for(
            "inicio_en",
            _external=True
        ),

        url_for(
            "salinas_en",
            _external=True
        ),

        url_for(
            "ojos_en",
            _external=True
        ),

        url_for(
            "atardecer_en",
            _external=True
        ),

        url_for(
            "humahuaca_en",
            _external=True
        )

    ]


    urls_xml = ""


    for pagina in paginas:

        urls_xml += f"""
    <url>
        <loc>{pagina}</loc>
    </url>
"""


    xml = f"""<?xml version="1.0" encoding="UTF-8"?>

<urlset
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
>

{urls_xml}

</urlset>
"""


    return Response(
        xml,
        mimetype="application/xml"
    )


# =========================================================
# EJECUCIÓN LOCAL
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000,
        load_dotenv=False
    )