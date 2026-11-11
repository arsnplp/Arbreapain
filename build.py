#!/usr/bin/env python3
"""Générateur du site L'Arbre à Pain.
Modifier les réglages ci-dessous puis lancer :  python3 build.py
Les pages HTML sont régénérées à la racine du dossier."""
import os, json, html

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- Réglages à compléter ----------
SITE_URL = "https://www.arbreapain.fr"        # domaine final
PHONE = ""                                     # ex. "04 42 00 00 00" (vide = masqué)
EMAIL = ""                                     # ex. "contact@arbreapain.fr" (vide = masqué)
INSTA = "https://www.instagram.com/boulangerie_l_arbre_a_pain/"
INSTA_CHEF = ""                                # Instagram de Béchir Hamed (vide = masqué)
BRAND = "L'Arbre à Pain"
SHOPS = [
    {"ville": "Mimet", "adresse": "Parking Intermarché", "cp": "13105", "maps": "https://www.google.com/maps/search/?api=1&query=L%27Arbre+%C3%A0+Pain+Mimet"},
    {"ville": "Aix-en-Provence", "adresse": "29 rue Espariat", "cp": "13100", "maps": "https://www.google.com/maps/search/?api=1&query=L%27Arbre+%C3%A0+Pain+29+rue+Espariat+Aix-en-Provence"},
]
# ------------------------------------------

e = html.escape


def img(root, name, alt, cls="", eager=False):
    c = f' class="{cls}"' if cls else ""
    l = "" if eager else ' loading="lazy" decoding="async"'
    return f'<img src="{root}images/{name}.jpg" alt="{e(alt)}"{c}{l}>'


def arch(root, name, alt, cls="", eager=False):
    return f'<figure class="arch {cls}">{img(root, name, alt, eager=eager)}</figure>'


NAV = [
    ("trompe-l-oeil.html", "Trompe-l'œil"),
    ("patisserie-evenement.html", "Événements"),
    ("boulangerie-tradition.html", "Tradition"),
    ("bechir-hamed.html", "Béchir Hamed"),
    ("ingredients.html", "Ingrédients"),
    ("journal/", "Recettes"),
]


def layout(path, title, desc, body, root="", cls=""):
    canonical = SITE_URL + "/" + ("" if path == "index.html" else path.replace("index.html", ""))
    nav = "".join(
        f'<a href="{root}{h}"{" aria-current=\"page\"" if path.startswith(h.rstrip("/")) and h != "" else ""}>{t}</a>'
        for h, t in NAV
    )
    ld = {
        "@context": "https://schema.org",
        "@type": "Bakery",
        "name": "Maison L'Arbre à Pain",
        "url": SITE_URL,
        "image": SITE_URL + "/images/trompe-planche.jpg",
        "description": "Pâtisserie fine, trompe-l'œil signature et boulangerie artisanale à Mimet et Aix-en-Provence.",
        "servesCuisine": "Pâtisserie française",
        "priceRange": "€€",
        "sameAs": [INSTA],
        "address": [
            {"@type": "PostalAddress", "streetAddress": s["adresse"], "postalCode": s["cp"], "addressLocality": s["ville"], "addressCountry": "FR"}
            for s in SHOPS
        ],
    }
    if PHONE:
        ld["telephone"] = PHONE
    shops = "".join(
        f'<li><strong>{s["ville"]}</strong><br>{s["adresse"]}, {s["cp"]} {s["ville"]}<br><a href="{s["maps"]}" target="_blank" rel="noopener">Voir l\'itinéraire</a></li>'
        for s in SHOPS
    )
    tel = f'<li><a href="tel:{PHONE.replace(" ", "")}">{PHONE}</a></li>' if PHONE else ""
    mail = f'<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>' if EMAIL else ""
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Maison L'Arbre à Pain">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE_URL}/images/trompe-planche.jpg">
<meta name="theme-color" content="#B4532F">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..700;1,6..96,400..600&family=Jost:wght@300..600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="{cls}">
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="top">
  <a class="brand" href="{root}index.html" aria-label="L'Arbre à Pain, accueil">
    <span class="mono" aria-hidden="true">AP</span>
    <span class="brand-name">L'Arbre à Pain<small>Maison de pâtisserie</small></span>
  </a>
  <button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span><span></span></button>
  <nav id="menu" class="menu" aria-label="Navigation principale">
    {nav}
    <a class="btn btn-gold" href="{root}contact.html">Demander un devis</a>
  </nav>
</header>
<main id="contenu">
{body}
</main>
<footer class="foot">
  <div class="foot-grid">
    <div>
      <p class="foot-brand"><span class="mono" aria-hidden="true">AP</span> L'Arbre à Pain</p>
      <p>Trompe-l'œil signature, pâtisserie fine et boulangerie artisanale. Tout est fait maison, chaque jour.</p>
      <p><a href="{INSTA}" target="_blank" rel="noopener">Instagram @boulangerie_l_arbre_a_pain</a></p>
    </div>
    <div>
      <h2>Nos boutiques</h2>
      <ul class="plain">{shops}</ul>
    </div>
    <div>
      <h2>La maison</h2>
      <ul class="plain">
        <li><a href="{root}trompe-l-oeil.html">Trompe-l'œil</a></li>
        <li><a href="{root}patisserie-evenement.html">Pâtisserie d'événement</a></li>
        <li><a href="{root}boulangerie-tradition.html">Tradition, salé et sucré</a></li>
        <li><a href="{root}bechir-hamed.html">Béchir Hamed</a></li>
        <li><a href="{root}ingredients.html">Nos ingrédients</a></li>
        <li><a href="{root}journal/">Recettes et journal</a></li>
        <li><a href="{root}contact.html">Contact et devis</a></li>
        {tel}{mail}
      </ul>
    </div>
  </div>
  <p class="foot-legal">© 2026 Maison L'Arbre à Pain. <a href="{root}mentions-legales.html">Mentions légales</a>. Fait par <a href="https://acco-lab.fr" target="_blank" rel="noopener">Acco-lab</a>.</p>
</footer>
<div class="lightbox" hidden><button class="lb-close" aria-label="Fermer la photo">Fermer</button><img alt=""></div>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
"""


def cta(root, titre="Une envie, un événement, une idée folle ?", texte="Dites-nous la date, le nombre de convives et ce qui vous ferait plaisir. Nous revenons vers vous avec une proposition et un devis."):
    return f"""<section class="cta">
  <div class="wrap cta-in">
    <div><h2>{titre}</h2><p>{texte}</p></div>
    <div class="cta-actions"><a class="btn btn-gold" href="{root}contact.html">Demander un devis</a><a class="btn btn-line" href="{INSTA}" target="_blank" rel="noopener">Nous écrire sur Instagram</a></div>
  </div>
</section>"""


def gallery(root, items):
    return '<div class="gallery">' + "".join(
        f'<button class="shot" type="button" aria-label="Agrandir : {e(alt)}">{img(root, n, alt)}</button>' for n, alt in items
    ) + "</div>"


def page_hero(root, titre, intro, photo, alt, kicker=""):
    k = f'<p class="kicker">{kicker}</p>' if kicker else ""
    return f"""<section class="phero">
  <div class="wrap phero-in">
    <div class="phero-txt">{k}<h1>{titre}</h1><p class="lead">{intro}</p></div>
    {arch(root, photo, alt, "arch-lg", eager=True)}
  </div>
</section>"""


SEAL = """<svg class="seal" viewBox="0 0 200 200" role="img" aria-label="28 ans d'expérience, pâtisserie premium">
<defs><path id="c" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/><linearGradient id="or" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A47A1E"/><stop offset=".25" stop-color="#F0D272"/><stop offset=".42" stop-color="#FFF6C9"/><stop offset=".58" stop-color="#D4AF37"/><stop offset=".78" stop-color="#9A7016"/><stop offset="1" stop-color="#F3DC86"/></linearGradient></defs>
<circle cx="100" cy="100" r="97" fill="none" stroke="url(#or)" stroke-width="1.6"/>
<circle cx="100" cy="100" r="60" fill="none" stroke="url(#or)" stroke-width="1.6"/>
<text class="seal-ring"><textPath href="#c" startOffset="0" textLength="484" lengthAdjust="spacing">Pâtisserie premium  ✦  Fait maison  ✦  Pâtisserie premium  ✦  Fait maison  ✦</textPath></text>
<text x="100" y="104" text-anchor="middle" class="seal-num">28</text>
<text x="100" y="126" text-anchor="middle" class="seal-sub">ans d'expérience</text>
</svg>"""

pages = {}

# ------------------------------------------------------------------ ACCUEIL
r = ""
pages["index.html"] = layout(
    "index.html",
    "L'Arbre à Pain | Pâtisserie trompe-l'œil à Mimet et Aix-en-Provence",
    "Trompe-l'œil signature, pâtisserie fine pour vos événements et boulangerie artisanale. 28 ans d'expérience, 100 % fait maison, à Mimet et Aix-en-Provence.",
    f"""<section class="hero">
  <div class="hero-txt">
    <h1>L'illusion<br>à regarder,<br>le vrai goût<br><span class="hl">à croquer</span></h1>
    <p class="lead">Trompe-l'œil signature, pâtisserie fine et boulangerie artisanale. Fait maison, à Mimet et à Aix-en-Provence.</p>
    <a class="link" href="trompe-l-oeil.html">Voir les trompe-l'œil</a>
  </div>
  <div class="hero-img">
    {img(r, "hero-plateau", "Plateau de trompe-l'œil et de pâtisseries L'Arbre à Pain : cacahuète, framboise, cabosse, pistache, éclair et entremets", eager=True)}
    {SEAL}
  </div>
  <a class="btn btn-gold hero-cta" href="contact.html">Demander un devis</a>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <h2>Trois savoir-faire, une même exigence</h2>
      <p>Le visuel compte autant que le goût. Chaque création est dessinée, montée et finie à la main dans notre laboratoire.</p>
    </div>
    <div class="trio">
      <a class="trio-card" href="trompe-l-oeil.html">
        {arch(r, "trompe-peche-noisette", "Trompe-l'œil pêche et noisette")}
        <h3>Trompe-l'œil</h3>
        <p>Pêche, citron, mangue, noisette, cacahuète. On s'y trompe au premier regard, on comprend à la première bouchée.</p>
        <span class="more">Découvrir la collection</span>
      </a>
      <a class="trio-card" href="patisserie-evenement.html">
        {arch(r, "entremets-rouge", "Entremets rouge miroir décoré de fruits rouges")}
        <h3>Pâtisserie fine pour événement</h3>
        <p>Anniversaire, mariage, baptême, soirée d'entreprise. Des entremets et pièces sur mesure, pensés pour votre table.</p>
        <span class="more">Préparer un événement</span>
      </a>
      <a class="trio-card" href="boulangerie-tradition.html">
        {arch(r, "eclairs", "Éclairs au chocolat glacés")}
        <h3>Tradition, salé et sucré</h3>
        <p>Éclairs, tartes, viennoiseries, pains, sandwichs et focaccias. Les classiques, faits comme il faut.</p>
        <span class="more">Voir la boutique</span>
      </a>
    </div>
  </div>
</section>

<section class="ribbon-sec" aria-label="En vitrine">
  <div class="wrap"><h2>En vitrine, en ce moment</h2></div>
  <div class="ribbon" tabindex="0">
    {''.join(f'<button class="shot" type="button" aria-label="Agrandir : {e(a)}">{img(r, n, a)}</button>' for n, a in [
      ("vitrine-trompe", "Vitrine de trompe-l'œil colorés"),
      ("tarte-figue", "Tarte aux figues fraîches et crème légère"),
      ("trompe-fruits-brillants", "Trompe-l'œil fruits au glaçage brillant"),
      ("saint-honore", "Saint-honoré à la crème pochée"),
      ("trompe-citron-mangue", "Trompe-l'œil citron et mangue"),
      ("cookie-fruits-rouges-sombre", "Cookie garni de fruits rouges frais"),
      ("entremets-jaune", "Entremets aux fruits exotiques"),
      ("trompe-assortiment", "Assortiment de trompe-l'œil"),
      ("ispahan", "Macaron framboise et crème"),
      ("vitrine-couleurs", "Vitrine de pâtisseries individuelles"),
    ])}
  </div>
</section>

<section class="chef">
  <div class="wrap chef-in">
    {arch(r, "chef-geste", "Béchir Hamed en plein glaçage dans le laboratoire", "arch-lg")}
    <div>
      <h2>Béchir Hamed, 28 ans de pâtisserie dans les mains</h2>
      <p>Derrière chaque vitrine, il y a un artisan présent au quotidien. Pâtissier reconnu à l'international et formateur, Béchir Hamed transmet son métier autant qu'il le pratique. Sa règle n'a pas changé depuis ses débuts : si ce n'est pas beau et bon à la fois, ça ne sort pas du laboratoire.</p>
      <a class="btn btn-gold" href="bechir-hamed.html">Rencontrer le chef</a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div>
      <h2>Le bon produit d'abord</h2>
      <p>Un trompe-l'œil pistache doit avoir le goût de la pistache. Nous choisissons des matières premières de qualité, du chocolat de couverture, de vrais fruits, du beurre et de la crème, et nous fabriquons tout nous-mêmes.</p>
      <a class="link" href="ingredients.html">Ce que nous mettons dans nos pâtisseries</a>
    </div>
    <div class="duo">
      {arch(r, "pistache-mains", "Cookie pistache ouvert à la main, cœur coulant")}
      {arch(r, "chocolat-coule", "Chocolat fondu versé sur le marbre", "down")}
    </div>
  </div>
</section>

<section class="sec sec-tint">
  <div class="wrap">
    <div class="sec-head"><h2>Recettes et coulisses</h2><p>Des recettes à refaire chez vous et quelques secrets de laboratoire.</p></div>
    <div class="posts">
      <a class="post" href="journal/trompe-l-oeil-patisserie-comment-ca-marche.html">{img(r, "trompe-mangue-coupee", "Trompe-l'œil mangue coupé en deux")}<h3>Trompe-l'œil : que cache un fruit qui n'en est pas un ?</h3><p>Coque, mousse, cœur coulant. On ouvre une de nos créations.</p></a>
      <a class="post" href="journal/recette-cookies-fourres-fruits-rouges.html">{img(r, "cookie-fruits-rouges", "Cookie aux fruits rouges")}<h3>Recette : cookies fourrés aux fruits rouges</h3><p>Croustillant dehors, fondant dedans, avec une compotée maison.</p></a>
      <a class="post" href="journal/recette-tarte-figues-creme-vanille.html">{img(r, "tarte-figue", "Tarte aux figues")}<h3>Recette : tarte aux figues, crème légère à la vanille</h3><p>La tarte de fin d'été, simple et très élégante.</p></a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="duo">
      {arch(r, "boutique-aix", "Intérieur de la boutique L'Arbre à Pain à Aix-en-Provence")}
      {arch(r, "vitrine-patisserie", "Vitrine de pâtisseries de la boutique", "down")}
    </div>
    <div>
      <h2>Deux adresses pour venir goûter</h2>
      <ul class="shops">
        {''.join(f'<li><h3>{s["ville"]}</h3><p>{s["adresse"]}, {s["cp"]} {s["ville"]}</p><a class="link" href="{s["maps"]}" target="_blank" rel="noopener">Itinéraire</a></li>' for s in SHOPS)}
      </ul>
    </div>
  </div>
</section>
{cta(r)}""",
    cls="home",
)

# ------------------------------------------------------------- TROMPE-L'OEIL
pages["trompe-l-oeil.html"] = layout(
    "trompe-l-oeil.html",
    "Pâtisserie trompe-l'œil à Aix-en-Provence et Mimet | L'Arbre à Pain",
    "Pêche, citron, mangue, fraise, noisette : nos trompe-l'œil signature sont des desserts plus vrais que nature. À l'unité, en coffret ou en format XL sur commande.",
    page_hero(r, "Le trompe-l'œil, notre signature", "Un citron qui n'est pas un citron. Une cacahuète grande comme la main. Des desserts sculptés pour surprendre l'œil, puis le palais.", "trompe-peches", "Trompe-l'œil pêches à la peau veloutée")
    + f"""
<section class="sec">
  <div class="wrap split">
    <div>
      <h2>Comment naît un trompe-l'œil</h2>
      <p>Tout commence par le fruit lui-même. On observe sa forme, sa peau, ses nuances, puis on le reconstruit en pâtisserie : une mousse légère, un cœur coulant ou croquant, une fine coque et un velours de couleur posé au pistolet.</p>
      <p>Le résultat doit tenir deux promesses. À l'œil, on doit hésiter. En bouche, le goût annoncé doit être là, franc et net : la mangue a le goût de la mangue, la noisette celui de la noisette.</p>
    </div>
    <div class="duo">
      {arch(r, "trompe-mangue-coupee", "Trompe-l'œil mangue ouvert, cœur coulant")}
      {arch(r, "trompe-mains", "Trompe-l'œil présenté dans les mains", "down")}
    </div>
  </div>
</section>
<section class="sec sec-tint">
  <div class="wrap">
    <div class="sec-head"><h2>La collection</h2><p>Elle change avec les saisons et les envies du chef. Voici quelques créations passées en vitrine. Touchez une photo pour l'agrandir.</p></div>
    {gallery(r, [
      ("trompe-fraise", "Trompe-l'œil fraise"), ("trompe-citron-mangue", "Trompe-l'œil citron et mangue"), ("trompe-peche-noisette", "Trompe-l'œil pêche et noisette"),
      ("trompe-cacahuete-framboise", "Trompe-l'œil cacahuète, fève de cacao et framboise"), ("trompe-pomme", "Trompe-l'œil pomme"), ("trompe-fruits-brillants", "Trompe-l'œil fruits brillants"),
      ("trompe-kiwi", "Trompe-l'œil kiwi"), ("trompe-prunes", "Trompe-l'œil prune et mangue"), ("trompe-orange-mangue", "Trompe-l'œil orange"),
      ("trompe-fraise-assiette", "Trompe-l'œil fraise sur assiette"), ("trompe-assortiment", "Assortiment de trompe-l'œil"), ("vitrine-longue", "Vitrine de trompe-l'œil"),
    ])}
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Comment en profiter</h2></div>
    <div class="cols3">
      <div><h3>À l'unité, en boutique</h3><p>La sélection du jour vous attend en vitrine à Mimet et à Aix-en-Provence. Venez tôt le week-end, les favoris partent vite.</p></div>
      <div><h3>En coffret à offrir</h3><p>Un assortiment de plusieurs fruits, à commander à l'avance. Idéal pour un dîner, un remerciement ou un cadeau qui fait parler.</p></div>
      <div><h3>En format XL</h3><p>Le trompe-l'œil à partager, en pièce centrale d'un anniversaire ou d'une réception. Sur commande et sur devis.</p></div>
    </div>
  </div>
</section>
{cta(r, "Envie d'un coffret ou d'un trompe-l'œil XL ?", "Indiquez-nous la date et le nombre de personnes, nous vous disons ce qui est possible.")}""",
)

# ------------------------------------------------------------- EVENEMENTS
pages["patisserie-evenement.html"] = layout(
    "patisserie-evenement.html",
    "Gâteaux sur mesure pour événements à Aix-en-Provence | L'Arbre à Pain",
    "Anniversaire, mariage, baptême, événement d'entreprise : entremets, gâteaux personnalisés et buffets sucrés sur mesure près d'Aix-en-Provence, Gardanne et Marseille. Devis rapide.",
    page_hero(r, "Pâtisserie fine pour vos événements", "Le gâteau, c'est le moment où tout le monde sort son téléphone. Autant qu'il soit à la hauteur, et qu'il soit aussi bon que beau.", "entremets-rouge-design", "Entremets rouge au décor graphique")
    + f"""
<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Ce que nous préparons pour vous</h2></div>
    <div class="cols3">
      <div><h3>Entremets et gâteaux signature</h3><p>Fruits rouges, exotique, chocolat, pistache, vanille. Des entremets à partager de quelques parts à de grandes tablées.</p></div>
      <div><h3>Créations personnalisées</h3><p>Un prénom, un thème, une couleur, une forme. Nous dessinons une pièce unique à partir de votre idée.</p></div>
      <div><h3>Buffets sucrés et mignardises</h3><p>Petits fours, tartelettes, choux, verrines et trompe-l'œil en format bouchée pour vos réceptions.</p></div>
    </div>
  </div>
</section>
<section class="sec sec-tint">
  <div class="wrap">
    <div class="sec-head"><h2>Quelques réalisations</h2><p>Touchez une photo pour l'agrandir.</p></div>
    {gallery(r, [
      ("entremets-rouge", "Entremets rouge miroir aux fruits rouges"), ("gateau-personnalise", "Gâteau personnalisé avec prénom"), ("entremets-coeurs", "Entremets rose décoré de cœurs"),
      ("gateau-fruits-rouges", "Gâteau aux fruits rouges et feuille d'or"), ("entremets-jaune", "Entremets exotique"), ("entremets-citron", "Entremets citron"),
      ("tarte-fruits-rouges", "Grande tarte aux fruits rouges"), ("entremets-vanille", "Entremets vanille"), ("mignardises", "Plateau de mignardises colorées"),
      ("nid-chocolat", "Pièce en chocolat en forme de nid"), ("petits-gateaux", "Petits gâteaux individuels"), ("saint-honore", "Saint-honoré"),
    ])}
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>De votre idée au jour J</h2></div>
    <ol class="steps">
      <li><h3>Vous nous racontez</h3><p>La date, le nombre de convives, l'occasion, vos goûts et, si vous en avez, des photos d'inspiration.</p></li>
      <li><h3>Nous proposons</h3><p>Le chef vous suggère des parfums et un visuel adaptés, avec un devis clair.</p></li>
      <li><h3>Nous fabriquons</h3><p>Votre commande est réalisée au plus près de la date, pour arriver à table au meilleur de sa fraîcheur.</p></li>
      <li><h3>Vous récupérez</h3><p>Retrait dans la boutique de votre choix, à Mimet ou à Aix-en-Provence, dans un emballage prévu pour le transport.</p></li>
    </ol>
    <p class="note">Pour une pièce sur mesure, contactez-nous le plus tôt possible : les week-ends se remplissent vite.</p>
  </div>
</section>
{cta(r, "Parlons de votre événement", "Un message suffit pour démarrer. Nous vous répondons avec des idées et un devis.")}""",
)

# ------------------------------------------------------------- TRADITION
pages["boulangerie-tradition.html"] = layout(
    "boulangerie-tradition.html",
    "Boulangerie pâtisserie artisanale à Mimet et Aix-en-Provence | L'Arbre à Pain",
    "Pains, viennoiseries, éclairs, tartes, sandwichs et focaccias : la boulangerie pâtisserie artisanale de L'Arbre à Pain, 100 % fait maison, à Mimet et Aix-en-Provence.",
    page_hero(r, "La tradition, le salé et le sucré", "Avant d'être une maison de trompe-l'œil, nous sommes une boulangerie pâtisserie. Le pain du matin, l'éclair de quatre heures et le déjeuner sur le pouce comptent autant que le reste.", "baguettes", "Baguettes de tradition sorties du four")
    + f"""
<section class="sec">
  <div class="wrap">
    <div class="rows">
      <article class="row">
        {arch(r, "eclairs", "Éclairs au chocolat")}
        <div><h2>Pâtisserie traditionnelle</h2><p>Éclairs, saint-honorés, tartes aux fruits, flans, macarons garnis. Les classiques français, avec le même soin de finition que nos créations les plus spectaculaires.</p></div>
      </article>
      <article class="row rev">
        {arch(r, "roules-cannelle", "Roulés à la cannelle dorés")}
        <div><h2>Pains et viennoiseries</h2><p>Baguettes de tradition, pains spéciaux, croissants, roulés et palmiers. Façonnés et cuits sur place, tout au long de la journée.</p></div>
      </article>
      <article class="row">
        {arch(r, "focaccia", "Focaccia décorée de légumes et d'herbes")}
        <div><h2>Le salé</h2><p>Sandwichs, focaccias, parts salées et plats du jour pour le déjeuner. À emporter, ou à savourer en terrasse avec un café.</p></div>
      </article>
    </div>
  </div>
</section>
<section class="sec sec-tint">
  <div class="wrap">
    <div class="sec-head"><h2>Un tour en boutique</h2><p>Touchez une photo pour l'agrandir.</p></div>
    {gallery(r, [
      ("pains", "Pains façonnés avant cuisson"), ("tartelettes", "Tartelettes aux fruits"), ("palmiers", "Palmiers et galettes feuilletées"),
      ("sandwichs", "Sandwichs frais"), ("petit-dejeuner", "Petit-déjeuner en terrasse, viennoiseries et café"), ("ispahan", "Macaron framboise"),
      ("cookies-pistache", "Cookies pistache"), ("tartes-vitrine", "Tartes aux fraises en vitrine"), ("choux-chocolat", "Choux au chocolat"),
      ("verrines", "Verrines aux fruits"), ("sandwich", "Sandwich garni"), ("vitrine-gateaux", "Vitrine de pâtisseries"),
    ])}
  </div>
</section>
{cta(r, "Une commande pour le week-end ?", "Pains spéciaux, plateaux salés, tartes et gâteaux : réservez à l'avance et passez simplement les récupérer.")}""",
)

# ------------------------------------------------------------- BECHIR HAMED
chef_insta = f'<p><a class="btn btn-line dark" href="{INSTA_CHEF}" target="_blank" rel="noopener">Suivre Béchir Hamed sur Instagram</a></p>' if INSTA_CHEF else ""
pages["bechir-hamed.html"] = layout(
    "bechir-hamed.html",
    "Béchir Hamed, pâtissier et formateur | L'Arbre à Pain",
    "28 ans d'expérience, une reconnaissance internationale et le goût de transmettre : découvrez Béchir Hamed, le pâtissier formateur derrière les créations de L'Arbre à Pain.",
    page_hero(r, "Béchir Hamed, pâtissier et formateur", "28 ans de métier, des créations reconnues bien au-delà de la Provence, et toujours la même envie : apprendre, refaire, transmettre.", "chef-gateau", "Béchir Hamed présentant un saint-honoré")
    + f"""
<section class="sec">
  <div class="wrap narrow">
    <h2>Un artisan, tous les jours au laboratoire</h2>
    <p>Béchir Hamed n'a jamais quitté le plan de travail. Depuis 28 ans, il pétrit, tempère, poche et glace, avec une idée fixe : une pâtisserie doit donner envie avant même d'être goûtée, et tenir sa promesse à la première bouchée.</p>
    <p>C'est cette exigence qui a donné naissance aux trompe-l'œil de la maison. Des fruits plus vrais que nature, travaillés comme des sculptures, mais pensés d'abord pour le goût.</p>
    <blockquote>« Le visuel attire. Le goût fait revenir. Il faut les deux, sinon ce n'est pas de la pâtisserie. »</blockquote>
  </div>
</section>
<section class="sec sec-tint">
  <div class="wrap split">
    <div class="duo">
      {arch(r, "chef-geste", "Glaçage d'un entremets au laboratoire")}
      {arch(r, "chocolat-coule", "Travail du chocolat sur marbre", "down")}
    </div>
    <div>
      <h2>Le formateur</h2>
      <p>Reconnu à l'international pour son travail, Béchir Hamed partage aujourd'hui son savoir-faire avec des professionnels et des passionnés. Trompe-l'œil, entremets, travail du chocolat, pochage : il enseigne les gestes, mais surtout la méthode et la rigueur qui vont avec.</p>
      <p>Former, pour lui, c'est aussi continuer à apprendre. Chaque technique montrée est d'abord une technique pratiquée chaque jour en boutique.</p>
      {chef_insta}
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2>Ce qui guide son travail</h2></div>
    <div class="cols3">
      <div><h3>Le beau et le bon, ensemble</h3><p>Une création n'entre en vitrine que si elle réussit les deux.</p></div>
      <div><h3>Le fait maison, sans raccourci</h3><p>Crèmes, pâtes, inserts, glaçages : tout est fabriqué sur place.</p></div>
      <div><h3>La création originale</h3><p>Pas de copie. Chaque pièce part d'une idée, d'un fruit, d'une saison.</p></div>
    </div>
  </div>
</section>
{cta(r, "Une formation, une collaboration, une création ?", "Écrivez-nous en quelques lignes, Béchir Hamed vous répondra.")}""",
)

# ------------------------------------------------------------- INGREDIENTS
pages["ingredients.html"] = layout(
    "ingredients.html",
    "Nos ingrédients : des matières premières de qualité | L'Arbre à Pain",
    "Vrais fruits, chocolat de couverture, pistache, beurre et crème : ce que nous mettons dans nos pâtisseries, et ce que nous refusons d'y mettre.",
    page_hero(r, "Ce qu'il y a dans nos pâtisseries", "Une belle pâtisserie avec de mauvais ingrédients, c'est juste un décor. Nous choisissons nos matières premières avant de dessiner quoi que ce soit.", "tarte-pistache", "Tarte à la pistache généreusement garnie")
    + f"""
<section class="sec">
  <div class="wrap">
    <div class="rows">
      <article class="row">
        {arch(r, "tablette-chocolat", "Tablette de chocolat de couverture")}
        <div><h2>Le chocolat</h2><p>Du chocolat de couverture, travaillé et tempéré chez nous pour les coques, les ganaches et les décors. C'est lui qui donne le croquant net d'un trompe-l'œil et la longueur en bouche d'un entremets.</p></div>
      </article>
      <article class="row rev">
        {arch(r, "tarte-figue", "Tarte garnie de figues fraîches")}
        <div><h2>Les fruits</h2><p>Des fruits frais, choisis mûrs, et des purées de fruits sans arôme ajouté. Fraise, framboise, figue, mangue, citron : la carte suit les saisons, parce qu'un fruit hors saison n'a pas de goût.</p></div>
      </article>
      <article class="row">
        {arch(r, "pistache-mains", "Cœur coulant à la pistache")}
        <div><h2>Les fruits secs</h2><p>Pistache, noisette, amande, cacahuète. Nous les torréfions et préparons nos pralinés nous-mêmes pour obtenir ce goût profond, impossible à imiter.</p></div>
      </article>
      <article class="row rev">
        {arch(r, "saint-honore", "Crème pochée sur un saint-honoré")}
        <div><h2>Le beurre, la crème, les œufs</h2><p>Du vrai beurre, de la crème entière et de la vanille en gousse. Pas de préparation en poudre, pas de mélange tout prêt : nos crèmes sont montées chaque jour.</p></div>
      </article>
    </div>
  </div>
</section>
<section class="sec sec-tint">
  <div class="wrap narrow center">
    <h2>100 % fait maison</h2>
    <p>Pâtes, crèmes, inserts, glaçages, pains et viennoiseries : tout ce qui est en vitrine sort de notre laboratoire. C'est plus long, et c'est exactement pour cela que c'est meilleur.</p>
    <p>Une allergie ou un régime particulier ? Demandez conseil en boutique ou par message avant de commander, nous vous indiquerons les créations adaptées.</p>
  </div>
</section>
{cta(r)}""",
)

# ------------------------------------------------------------- CONTACT
shops_c = "".join(f'<li><h3>{s["ville"]}</h3><p>{s["adresse"]}<br>{s["cp"]} {s["ville"]}</p><a class="link" href="{s["maps"]}" target="_blank" rel="noopener">Itinéraire</a></li>' for s in SHOPS)
direct = ""
if PHONE:
    direct += f'<p><a class="btn btn-gold" href="tel:{PHONE.replace(" ", "")}">Appeler le {PHONE}</a></p>'
pages["contact.html"] = layout(
    "contact.html",
    "Contact et devis | L'Arbre à Pain, Mimet et Aix-en-Provence",
    "Demandez un devis pour un gâteau sur mesure, un coffret de trompe-l'œil ou un buffet sucré. Boutiques à Mimet et au 29 rue Espariat à Aix-en-Provence.",
    f"""<section class="phero phero-slim"><div class="wrap"><h1>Contact et devis</h1><p class="lead">Dites-nous ce qui vous ferait plaisir. Plus vous êtes précis, plus notre réponse sera rapide.</p></div></section>
<section class="sec">
  <div class="wrap split top">
    <form class="form" id="devis" data-email="{EMAIL}" data-insta="{INSTA}">
      <h2>Votre demande</h2>
      <div class="f2">
        <label>Votre nom<input name="nom" required autocomplete="name"></label>
        <label>Téléphone<input name="tel" type="tel" required autocomplete="tel"></label>
      </div>
      <div class="f2">
        <label>Type de demande
          <select name="type">
            <option>Gâteau ou entremets sur mesure</option>
            <option>Trompe-l'œil (coffret ou format XL)</option>
            <option>Buffet sucré, mignardises</option>
            <option>Commande boulangerie ou salé</option>
            <option>Formation avec Béchir Hamed</option>
            <option>Autre</option>
          </select>
        </label>
        <label>Boutique de retrait
          <select name="boutique">{''.join(f"<option>{s['ville']}</option>" for s in SHOPS)}</select>
        </label>
      </div>
      <div class="f2">
        <label>Date souhaitée<input name="date" type="date"></label>
        <label>Nombre de personnes<input name="nb" type="number" min="1" inputmode="numeric"></label>
      </div>
      <label>Votre projet<textarea name="msg" rows="5" required placeholder="Occasion, parfums préférés, thème, couleurs, allergies..."></textarea></label>
      <button class="btn btn-gold" type="submit">Préparer ma demande</button>
      <p class="form-out" role="status" aria-live="polite"></p>
    </form>
    <aside class="aside">
      <h2>Nous trouver</h2>
      <ul class="shops">{shops_c}</ul>
      {direct}
      <p><a class="btn btn-line dark" href="{INSTA}" target="_blank" rel="noopener">Nous écrire sur Instagram</a></p>
    </aside>
  </div>
</section>""",
)

# ------------------------------------------------------------- MENTIONS
pages["mentions-legales.html"] = layout(
    "mentions-legales.html",
    "Mentions légales | L'Arbre à Pain",
    "Mentions légales du site de la Maison L'Arbre à Pain.",
    """<section class="phero phero-slim"><div class="wrap"><h1>Mentions légales</h1></div></section>
<section class="sec"><div class="wrap narrow">
<h2>Éditeur du site</h2>
<p>Maison L'Arbre à Pain. Raison sociale, forme juridique, numéro SIRET, adresse du siège et nom du directeur de la publication : à compléter.</p>
<h2>Hébergement</h2>
<p>Hostinger International Ltd, 61 Lordou Vironos Street, 6023 Larnaca, Chypre.</p>
<h2>Conception</h2>
<p>Site réalisé par <a href="https://acco-lab.fr" target="_blank" rel="noopener">Acco-lab</a>.</p>
<h2>Propriété intellectuelle</h2>
<p>Les textes, photographies et créations présentés sur ce site appartiennent à la Maison L'Arbre à Pain. Toute reproduction sans autorisation est interdite.</p>
<h2>Données personnelles</h2>
<p>Les informations saisies dans le formulaire de devis servent uniquement à répondre à votre demande. Elles ne sont ni cédées ni utilisées à des fins publicitaires. Vous pouvez demander leur suppression à tout moment en nous contactant.</p>
<h2>Cookies</h2>
<p>Ce site ne dépose aucun cookie publicitaire.</p>
</div></section>""",
)

# ------------------------------------------------------------- JOURNAL
r2 = "../"
ARTICLES = [
    {
        "slug": "trompe-l-oeil-patisserie-comment-ca-marche",
        "titre": "Trompe-l'œil en pâtisserie : que cache un fruit qui n'en est pas un ?",
        "desc": "Coque, mousse, insert, velours : on vous explique comment est construit un trompe-l'œil et pourquoi il doit être aussi bon que beau.",
        "photo": "trompe-mangue-coupee", "alt": "Trompe-l'œil mangue coupé en deux",
        "date": "2026-10-20", "datef": "20 octobre 2026",
        "corps": """<p>Vu de loin, c'est une mangue. De près, c'est toujours une mangue. Il faut la couper pour comprendre : sous la peau, une mousse légère et un cœur coulant. Le trompe-l'œil est une pâtisserie qui prend la forme exacte de ce dont elle a le goût.</p>
<h2>Quatre couches, un seul fruit</h2>
<ul>
<li><strong>Le cœur.</strong> Un insert de fruit, de praliné ou de caramel, préparé en premier et congelé. C'est la surprise du milieu.</li>
<li><strong>La mousse.</strong> Elle entoure le cœur dans un moule à la forme du fruit. Elle apporte la légèreté et porte le parfum principal.</li>
<li><strong>La coque.</strong> Un trempage fin, souvent à base de chocolat, qui donne le croquant sous la dent.</li>
<li><strong>Le velours.</strong> Un voile de couleur pulvérisé au pistolet. C'est lui qui imite le duvet d'une pêche ou le grain d'un citron.</li>
</ul>
<h2>Pourquoi c'est difficile</h2>
<p>Chaque étape demande une température précise. Une mousse trop chaude ne prend pas, une coque trop épaisse casse la dégustation, un velours appliqué au mauvais moment coule. Une seule pièce demande plusieurs passages au froid et beaucoup de gestes à la main, notamment pour les dégradés de couleur.</p>
<h2>Le goût avant tout</h2>
<p>Un trompe-l'œil raté, c'est une jolie sculpture qui n'a goût de rien. Chez nous, la règle est simple : la forme annonce un parfum, la bouchée doit le confirmer. Une noisette doit sentir la noisette torréfiée, un citron doit être vif.</p>
<h2>Comment le déguster</h2>
<p>Sortez-le du réfrigérateur dix minutes avant, et coupez-le en deux avec un couteau fin. Le moment où l'on découvre l'intérieur fait partie du dessert.</p>""",
    },
    {
        "slug": "recette-cookies-fourres-fruits-rouges",
        "titre": "Recette : cookies fourrés aux fruits rouges",
        "desc": "La recette de cookies moelleux garnis d'une compotée de fruits rouges maison. Ingrédients, étapes et conseils de pâtissier.",
        "photo": "cookie-fruits-rouges", "alt": "Cookie garni de fruits rouges frais",
        "date": "2026-10-06", "datef": "6 octobre 2026",
        "corps": """<p>Un cookie, oui, mais avec un cœur de fruits rouges qui réveille tout. Voici une version maison, simple à réussir. Pour 8 gros cookies.</p>
<h2>Ingrédients</h2>
<p><strong>Compotée :</strong> 150 g de fruits rouges (frais ou surgelés), 30 g de sucre, 1 cuillère à café de jus de citron.</p>
<p><strong>Pâte :</strong> 125 g de beurre mou, 100 g de cassonade, 50 g de sucre, 1 œuf, 220 g de farine, 1/2 cuillère à café de levure chimique, 1 pincée de fleur de sel, 100 g de chocolat blanc en morceaux.</p>
<p><strong>Finition :</strong> quelques fruits rouges frais.</p>
<h2>Préparation</h2>
<ol>
<li>Faites cuire les fruits rouges avec le sucre et le citron 8 à 10 minutes à feu moyen, jusqu'à obtenir une compotée épaisse. Laissez refroidir complètement.</li>
<li>Fouettez le beurre mou avec la cassonade et le sucre. Ajoutez l'œuf, puis la farine, la levure et le sel. Incorporez le chocolat blanc.</li>
<li>Formez 8 boules. Aplatissez chacune dans la main, déposez une cuillère à café de compotée au centre et refermez bien.</li>
<li>Placez les boules 30 minutes au réfrigérateur. Préchauffez le four à 170 °C.</li>
<li>Enfournez 11 à 12 minutes. Les bords doivent être dorés et le centre encore tendre.</li>
<li>Laissez tiédir sur la plaque, puis décorez d'un peu de compotée et de fruits frais.</li>
</ol>
<h2>Les conseils du chef</h2>
<p>Le passage au froid est indispensable : il évite que les cookies s'étalent et que la compotée s'échappe. Et sortez-les quand ils vous semblent à peine cuits, ils finissent de se raffermir en refroidissant.</p>""",
    },
    {
        "slug": "recette-tarte-figues-creme-vanille",
        "titre": "Recette : tarte aux figues, crème légère à la vanille",
        "desc": "Une pâte sablée croustillante, une crème légère à la vanille et des figues fraîches : la recette de la tarte de fin d'été, pas à pas.",
        "photo": "tarte-figue", "alt": "Tarte aux figues fraîches et crème à la vanille",
        "date": "2026-09-22", "datef": "22 septembre 2026",
        "corps": """<p>Quand les figues arrivent sur les étals, cette tarte revient en vitrine. Elle se prépare sans cuisson des fruits, pour garder tout leur parfum. Pour 6 à 8 personnes.</p>
<h2>Ingrédients</h2>
<p><strong>Pâte sablée :</strong> 200 g de farine, 100 g de beurre froid, 70 g de sucre glace, 25 g de poudre d'amande, 1 œuf, 1 pincée de sel.</p>
<p><strong>Crème légère :</strong> 250 g de mascarpone, 200 g de crème liquide entière bien froide, 40 g de sucre glace, 1 gousse de vanille.</p>
<p><strong>Garniture :</strong> 6 à 8 figues fraîches, 1 cuillère à soupe de miel.</p>
<h2>Préparation</h2>
<ol>
<li>Sablez du bout des doigts la farine, le beurre en dés, le sucre glace, la poudre d'amande et le sel. Ajoutez l'œuf et formez une boule sans trop travailler. Filmez et laissez reposer 1 heure au frais.</li>
<li>Étalez la pâte, foncez un cercle de 22 cm et piquez le fond. Faites cuire à blanc 20 minutes à 170 °C, jusqu'à une belle couleur dorée. Laissez refroidir.</li>
<li>Fouettez le mascarpone, la crème, le sucre glace et les grains de vanille jusqu'à obtenir une crème ferme.</li>
<li>Garnissez le fond de tarte de crème, à la spatule ou à la poche.</li>
<li>Coupez les figues en quartiers et disposez-les sur la crème. Nappez d'un filet de miel tiédi.</li>
<li>Réservez 1 heure au réfrigérateur avant de servir.</li>
</ol>
<h2>Les conseils du chef</h2>
<p>Choisissez des figues souples sous le doigt, c'est le signe qu'elles sont mûres. Et montez la tarte le jour même : la pâte reste croustillante et la crème bien aérienne.</p>""",
    },
]

cards = "".join(
    f'<a class="post" href="{a["slug"]}.html">{img(r2, a["photo"], a["alt"])}<p class="date">{a["datef"]}</p><h2>{a["titre"]}</h2><p>{a["desc"]}</p></a>'
    for a in ARTICLES
)
pages["journal/index.html"] = layout(
    "journal/index.html",
    "Recettes et journal de pâtisserie | L'Arbre à Pain",
    "Recettes de pâtissier à refaire chez vous, secrets de trompe-l'œil et coulisses du laboratoire de L'Arbre à Pain.",
    f"""<section class="phero phero-slim"><div class="wrap"><h1>Recettes et journal</h1><p class="lead">Des recettes testées au laboratoire, expliquées simplement, et quelques coulisses de la maison.</p></div></section>
<section class="sec"><div class="wrap"><div class="posts">{cards}</div></div></section>
{cta(r2)}""",
    root=r2,
)
for a in ARTICLES:
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["titre"], "datePublished": a["date"],
          "image": f'{SITE_URL}/images/{a["photo"]}.jpg', "author": {"@type": "Person", "name": "Béchir Hamed"},
          "publisher": {"@type": "Organization", "name": "Maison L'Arbre à Pain"}}
    pages[f'journal/{a["slug"]}.html'] = layout(
        f'journal/{a["slug"]}.html',
        a["titre"] + " | L'Arbre à Pain",
        a["desc"],
        f"""<article class="article">
  <header class="phero phero-slim"><div class="wrap narrow"><p class="kicker"><a href="./">Recettes et journal</a></p><h1>{a["titre"]}</h1><p class="date">Publié le {a["datef"]}</p></div></header>
  <div class="wrap narrow">
    <figure class="article-img">{img(r2, a["photo"], a["alt"], eager=True)}</figure>
    <div class="prose">{a["corps"]}</div>
    <p><a class="link" href="./">Toutes les recettes</a></p>
  </div>
</article>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{cta(r2, "Pas envie de pâtisser aujourd'hui ?", "On s'en occupe. Passez en boutique ou commandez votre création sur mesure.")}""",
        root=r2,
    )

# ------------------------------------------------------------- ECRITURE
for path, content in pages.items():
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

urls = "".join(
    f"<url><loc>{SITE_URL}/{'' if p == 'index.html' else p.replace('index.html', '')}</loc></url>\n"
    for p in pages if p != "mentions-legales.html"
)
with open(os.path.join(HERE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
with open(os.path.join(HERE, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
print(len(pages), "pages générées")
