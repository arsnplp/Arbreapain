// Menu mobile
const burger = document.querySelector('.burger');
const menu = document.getElementById('menu');
if (burger && menu) {
  burger.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
    burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
  });
}

// Visionneuse photo
const lb = document.querySelector('.lightbox');
if (lb) {
  const big = lb.querySelector('img');
  let last = null;
  const close = () => { lb.hidden = true; big.src = ''; if (last) last.focus(); };
  document.querySelectorAll('.shot').forEach((b) => b.addEventListener('click', () => {
    const i = b.querySelector('img');
    big.src = i.src; big.alt = i.alt; lb.hidden = false; last = b;
    lb.querySelector('.lb-close').focus();
  }));
  lb.addEventListener('click', (e) => { if (e.target !== big) close(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !lb.hidden) close(); });
}

// Formulaire de devis : prépare le message, puis l'envoie par e-mail ou le copie pour Instagram
const form = document.getElementById('devis');
if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const d = new FormData(form);
    const out = form.querySelector('.form-out');
    const lines = [
      'Bonjour, je souhaite un devis.',
      'Nom : ' + d.get('nom'),
      'Téléphone : ' + d.get('tel'),
      'Demande : ' + d.get('type'),
      'Boutique de retrait : ' + d.get('boutique'),
      d.get('date') ? 'Date souhaitée : ' + d.get('date').split('-').reverse().join('/') : '',
      d.get('nb') ? 'Nombre de personnes : ' + d.get('nb') : '',
      '',
      d.get('msg'),
    ].filter((l, i) => l !== '' || i === 7).join('\n');
    const email = form.dataset.email;
    if (email) {
      window.location.href = 'mailto:' + email + '?subject=' + encodeURIComponent('Demande de devis : ' + d.get('type')) + '&body=' + encodeURIComponent(lines);
      out.textContent = 'Votre messagerie s\'ouvre avec la demande déjà rédigée. Il ne reste plus qu\'à l\'envoyer.';
      return;
    }
    try {
      await navigator.clipboard.writeText(lines);
      out.innerHTML = 'Votre demande est copiée. <a href="' + form.dataset.insta + '" target="_blank" rel="noopener">Ouvrez notre Instagram</a> et collez-la en message privé.';
    } catch (err) {
      out.innerHTML = 'Envoyez-nous ces informations en message privé sur <a href="' + form.dataset.insta + '" target="_blank" rel="noopener">notre Instagram</a>.';
    }
  });
}

// Accueil : affiche le menu dès qu'on commence à défiler
if (document.body.classList.contains('home')) {
  const onScroll = () => document.body.classList.toggle('scrolled', window.scrollY > 20);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// Ingrédients : sur téléphone les cartes s'empilent ; sur ordinateur, scène fixe avec révélation en iris
const stackEl = document.querySelector('.stack');
const stackCards = [...document.querySelectorAll('.stack-card')];
if (stackEl && stackCards.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const wide = window.matchMedia('(min-width: 861px)');
  const HEAD = 70;
  const clamp = (v) => Math.min(1, Math.max(0, v));
  const ease = (v) => v * v * (3 - 2 * v);

  // Navigation de la scène (ordinateur)
  const nav = document.createElement('nav');
  nav.className = 'stack-nav';
  nav.setAttribute('aria-label', 'Ingrédients');
  const ol = document.createElement('ol');
  const buttons = stackCards.map((card, i) => {
    const li = document.createElement('li');
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = card.querySelector('h2').textContent;
    b.addEventListener('click', () => {
      const top = stackEl.getBoundingClientRect().top + window.scrollY - HEAD;
      const seg = (stackEl.offsetHeight - (window.innerHeight - HEAD)) / (stackCards.length - 1);
      window.scrollTo({ top: top + seg * i, behavior: 'smooth' });
    });
    li.appendChild(b); ol.appendChild(li);
    return b;
  });
  nav.appendChild(ol);
  stackEl.appendChild(nav);

  const reset = () => stackCards.forEach((card) => {
    card.style.transform = ''; card.style.filter = '';
    card.style.removeProperty('--r'); card.style.removeProperty('--t');
    const img = card.querySelector('.stack-photo img');
    if (img) img.style.transform = '';
  });

  const updateMobile = () => {
    const vh = window.innerHeight;
    stackCards.forEach((card, i) => {
      const next = stackCards[i + 1];
      let cover = 0;
      if (next) cover = clamp(1 - (next.getBoundingClientRect().top - HEAD) / (vh - HEAD));
      card.style.transform = 'scale(' + (1 - cover * 0.06) + ')';
      card.style.filter = 'brightness(' + (1 - cover * 0.45) + ')';
      const enter = clamp(1 - (card.getBoundingClientRect().top - HEAD) / (vh - HEAD));
      const img = card.querySelector('.stack-photo img');
      if (img) img.style.transform = 'translateY(' + ((1 - enter) * 5 - cover * 4) + '%) scale(' + (1.08 - enter * 0.08) + ')';
    });
  };

  const updateDesktop = () => {
    const h = window.innerHeight - HEAD;
    const total = stackEl.offsetHeight - h;
    const scrolled = clamp((HEAD - stackEl.getBoundingClientRect().top) / total);
    const pos = scrolled * (stackCards.length - 1);
    let active = 0;
    stackCards.forEach((card, i) => {
      if (i === 0) { card.style.setProperty('--r', 1); card.style.setProperty('--t', 1); }
      else {
        const f = clamp(pos - (i - 1));
        const r = ease(clamp((f - 0.2) / 0.6));
        const t = ease(clamp((f - 0.45) / 0.45));
        card.style.setProperty('--r', r.toFixed(4));
        card.style.setProperty('--t', t.toFixed(4));
        if (r > 0.5) active = i;
      }
    });
    buttons.forEach((b, i) => b.setAttribute('aria-current', i === active));
  };

  let mode = null, ticking = false;
  const update = () => {
    ticking = false;
    const m = wide.matches ? 'd' : 'm';
    if (m !== mode) { reset(); mode = m; }
    (m === 'd' ? updateDesktop : updateMobile)();
  };
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  window.addEventListener('resize', update);
  update();
}
