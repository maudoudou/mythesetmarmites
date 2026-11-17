/* ==========================================================================
   Studio Mille Pages — routage, apparitions, formulaire
   ========================================================================== */

/* ---------------------------- Utilitaires ---------------------------- */
const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

/* ---------------------------- Apparitions ---------------------------- */
/* Blocs .rise, et grands titres de section dont la bande de plis se
   déplie à l'apparition (voir « Plis du leporello » dans style.css). */
const APPEAR = '.rise:not(.in), .t-sec:not(.in), .sec-title:not(.in), .plis:not(.in)';
let io;
function observeRise() {
  if (!('IntersectionObserver' in window)) { $$(APPEAR).forEach(e => e.classList.add('in')); return; }
  io = io || new IntersectionObserver(entries => {
    entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  $$(APPEAR).forEach(e => io.observe(e));
}

/* ---------------------------- Routage ---------------------------- */
/* index.html est la coquille : elle contient toutes les sections (source de
   generate-static-pages.py) mais n'en affiche qu'une, l'accueil. Chaque
   route a sa vraie page à sa propre URL — /studio, /parcours, etc. Les anciens liens en #/ y sont renvoyés côté client (le serveur ne
   voit jamais le fragment). */
const IS_SPA_SHELL = $$('.page').length > 1;
const MIGRATED_ROUTES = ['studio', 'jeu', 'parcours', 'contact'];
/* Rubriques retirées : leurs anciens liens mènent au studio. */
const RETIRED_ROUTES = ['ateliers', 'correction'];

function show(page) {
  $$('.page').forEach(s => s.classList.toggle('hide', s.dataset.page !== page));
}

/* Renvoie un ancien lien #/… vers sa vraie URL. true si une redirection
   a été lancée (la requête ?cat=… est conservée). */
function redirectLegacyHash() {
  const raw = (location.hash || '').replace(/^#\/?/, '');
  if (!raw) return false;
  const [path, query] = raw.split('?');
  const parts = path.split('/').filter(Boolean);
  const q = query ? '?' + query : '';
  if (RETIRED_ROUTES.includes(parts[0])) { location.replace('/studio'); return true; }
  if (parts.length === 1 && MIGRATED_ROUTES.includes(parts[0])) { location.replace('/' + parts[0] + q); return true; }
  return false;
}

/* ---------------------------- Menu mobile ---------------------------- */
const burger = $('#burger');
const navLinks = $('#nav-links');
function closeMenu() {
  document.body.classList.remove('menu-open');
  burger.setAttribute('aria-expanded', 'false');
  burger.setAttribute('aria-label', 'Ouvrir le menu');
}
/* L'en-tête actuel (logo centré, deux liens) n'a plus de menu repliable :
   ce code ne s'active que si un bouton #burger est présent. */
if (burger && navLinks) {
  burger.addEventListener('click', () => {
    const open = !document.body.classList.contains('menu-open');
    document.body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
  });
  navLinks.addEventListener('click', e => { if (e.target.closest('a')) closeMenu(); });
  window.addEventListener('hashchange', closeMenu);
  window.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
}

/* ---------------------------- Formulaire ---------------------------- */
/* #form n'existe que sur la page « Contact » (coquille SPA ou page
   statique /contact/) : on protège l'écoute. */
if ($('#form')) $('#form').addEventListener('submit', async e => {
  e.preventDefault();
  const form = e.target;
  const status = $('#form-status');
  const btn = form.querySelector('button[type="submit"]');

  if (!form.checkValidity()) { form.reportValidity(); return; }

  btn.textContent = 'Envoi…';
  btn.disabled = true;
  status.textContent = '';

  try {
    const res = await fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    });
    if (!res.ok) throw new Error('refus du serveur');
    form.reset();
    $('#contact-form').classList.add('hide');
    $('#contact-sent').classList.remove('hide');
    window.scrollTo(0, 0);
  } catch (err) {
    status.textContent = "L'envoi n'a pas abouti. Écrivez-moi directement à bonjour@mythesetmarmites.fr";
    status.style.color = 'var(--encre)';
  } finally {
    btn.textContent = 'Envoyer';
    btn.disabled = false;
  }
});

/* ---------------------------- Démarrage ---------------------------- */
if (IS_SPA_SHELL) {
  /* Coquille (/). Servie à une autre adresse que / (ancien repli
     d'hébergement) ? on renvoie à l'accueil. Sinon on redirige un éventuel
     ancien lien #/… puis on affiche l'accueil. */
  const p = location.pathname.replace(/\/index\.html$/, '').replace(/(.)\/+$/, '$1');
  if (p && p !== '/') {
    location.replace('/');
  } else if (!redirectLegacyHash()) {
    show('accueil');
    window.addEventListener('hashchange', () => { redirectLegacyHash(); });
    observeRise();
  }
} else {
  /* Autre page statique : le contenu est déjà en place. */
  observeRise();
}