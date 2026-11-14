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

// Tradition : les bandes de photos glissent à l'horizontale pendant le défilement
const reelRows = [...document.querySelectorAll('.reel-row')];
if (reelRows.length) {
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (still) {
    reelRows.forEach((r) => { r.querySelector('.reel-strip').style.overflowX = 'auto'; });
  } else {
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) e.target.classList.add('seen'); }), { threshold: 0.25 });
      reelRows.forEach((r) => { r.classList.add('anim'); io.observe(r); });
    }
    let tick = false;
    const slide = () => {
      tick = false;
      const vh = window.innerHeight;
      reelRows.forEach((row) => {
        const strip = row.querySelector('.reel-strip');
        const track = row.querySelector('.reel-track');
        const r = strip.getBoundingClientRect();
        const p = Math.min(1, Math.max(0, (vh - r.top) / (vh + r.height)));
        const travel = Math.max(0, track.scrollWidth - strip.clientWidth);
        const x = row.classList.contains('rev') ? -travel * (1 - p) : -travel * p;
        track.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)';
      });
    };
    window.addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(slide); } }, { passive: true });
    window.addEventListener('resize', slide);
    window.addEventListener('load', slide);
    slide();
  }
}

// Trompe-l'œil : pièces flottantes en arc de cercle, à faire glisser
const arc = document.querySelector('.arc');
if (arc) {
  const items = [...arc.querySelectorAll('.arc-item')];
  const nomEl = document.querySelector('.arc-nom');
  const n = items.length;
  const calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let pos = 0;      // position courante (peut être décimale pendant le geste)
  let goal = 0;     // position visée
  let raf = 0;
  let size = 0;
  let centre = -1;
  arc.classList.add('arc-js');

  const measure = () => { size = items[0].offsetWidth; };
  const render = () => {
    const step = size * 0.94;
    let best = 0;
    let bestD = 99;
    items.forEach((el, i) => {
      // écart au centre, ramené entre -n/2 et n/2 pour boucler à l'infini
      let d = ((i - pos) % n + n) % n;
      if (d > n / 2) d -= n;
      const a = Math.abs(d);
      if (a < bestD) { bestD = a; best = i; }
      const x = step * d * (1 - 0.055 * a);
      const y = size * 0.05 * d * d;                 // l'arc : le centre en haut, les côtés redescendent
      const sc = Math.max(0.3, 1 - 0.21 * a);        // profondeur : plus loin = plus petit
      const op = a <= 2.4 ? 1 : Math.max(0, 1 - (a - 2.4) / 0.9);
      el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px) rotate(' + (d * 7).toFixed(2) + 'deg) scale(' + sc.toFixed(3) + ')';
      el.style.opacity = op.toFixed(2);
      el.style.zIndex = String(100 - Math.round(a * 10));
      el.style.visibility = op === 0 ? 'hidden' : 'visible';
    });
    if (best !== centre) { centre = best; nomEl.textContent = items[best].dataset.nom; }
  };
  const tick = () => {
    pos += (goal - pos) * (calm ? 1 : 0.11);
    if (Math.abs(goal - pos) < 0.002) pos = goal;
    render();
    raf = pos === goal ? 0 : requestAnimationFrame(tick);
  };
  const glide = (g) => { goal = g; if (!raf) raf = requestAnimationFrame(tick); };

  document.querySelector('.arc-prev').addEventListener('click', () => glide(Math.round(goal) - 1));
  document.querySelector('.arc-next').addEventListener('click', () => glide(Math.round(goal) + 1));
  arc.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); glide(Math.round(goal) + 1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); glide(Math.round(goal) - 1); }
  });

  // Glisser à la souris ou au doigt, avec un peu d'élan au lâcher
  let down = false;
  let x0 = 0;
  let p0 = 0;
  let moved = 0;
  let lastX = 0;
  let lastT = 0;
  let vel = 0;
  arc.addEventListener('pointerdown', (e) => {
    if (e.button) return;
    down = true; moved = 0; vel = 0;
    x0 = lastX = e.clientX; lastT = e.timeStamp; p0 = pos;
    cancelAnimationFrame(raf); raf = 0;
  });
  arc.addEventListener('pointermove', (e) => {
    if (!down) return;
    const dx = e.clientX - x0;
    moved = Math.max(moved, Math.abs(dx));
    if (moved > 6 && !arc.classList.contains('is-drag')) {
      arc.classList.add('is-drag');
      try { arc.setPointerCapture(e.pointerId); } catch (err) { /* sans capture, le geste reste suivi dans la zone */ }
    }
    const dt = e.timeStamp - lastT;
    if (dt > 0) vel = 0.7 * vel + 0.3 * ((e.clientX - lastX) / dt);
    lastX = e.clientX; lastT = e.timeStamp;
    pos = goal = p0 - dx / (size * 0.94);
    render();
  });
  const release = (e) => {
    if (!down) return;
    down = false;
    arc.classList.remove('is-drag');
    if (moved <= 6) {
      // simple clic : on amène au centre la pièce visée
      const hit = items.find((el) => {
        const r = el.getBoundingClientRect();
        return el.style.visibility !== 'hidden' && e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
      });
      const order = items.filter((el) => el.style.visibility !== 'hidden').sort((a, b) => b.style.zIndex - a.style.zIndex);
      const top = order.find((el) => {
        const r = el.getBoundingClientRect();
        return e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
      }) || hit;
      if (top) {
        let d = ((items.indexOf(top) - pos) % n + n) % n;
        if (d > n / 2) d -= n;
        glide(Math.round(pos + d));
      }
      return;
    }
    const throwBy = Math.max(-2.5, Math.min(2.5, (-vel * 260) / (size * 0.94)));
    glide(Math.round(pos + throwBy));
  };
  arc.addEventListener('pointerup', release);
  arc.addEventListener('pointercancel', () => { if (down) { down = false; arc.classList.remove('is-drag'); glide(Math.round(pos)); } });
  arc.addEventListener('dragstart', (e) => e.preventDefault());

  window.addEventListener('resize', () => { measure(); render(); });
  measure();
  render();
}
