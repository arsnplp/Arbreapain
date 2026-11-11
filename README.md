# Site L'Arbre à Pain

Site vitrine statique (HTML, CSS, JS), sans dépendance.

## Photos
Dézipper `arbreapain-photos.zip` à la racine de ce dossier : il crée le dossier `images/` avec les 67 photos utilisées par les pages.

## Modifier le site
Les pages sont générées par `build.py`. Réglages en haut du fichier :
- `SITE_URL` : domaine final
- `PHONE`, `EMAIL` : s'affichent dans le pied de page, la page contact et le formulaire dès qu'ils sont remplis
- `INSTA_CHEF` : Instagram de Béchir Hamed
- `SHOPS` : adresses des boutiques

Puis lancer `python3 build.py`.

## À compléter avant mise en ligne
- Téléphone, e-mail, horaires
- Instagram de Béchir Hamed et validation de sa page
- Mentions légales (raison sociale, SIRET, directeur de publication)
- Logo officiel (remplace le monogramme AP dans l'en-tête)
