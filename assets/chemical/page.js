(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const menuToggle = document.getElementById('menu-toggle');
  const menu = document.getElementById('main-nav');
  menuToggle.hidden = false;
  const closeMenu = () => { menuToggle.setAttribute('aria-expanded', 'false'); menu.classList.remove('is-open'); };
  menuToggle.addEventListener('click', () => {
    const open = menuToggle.getAttribute('aria-expanded') !== 'true';
    menuToggle.setAttribute('aria-expanded', String(open)); menu.classList.toggle('is-open', open);
  });
  menu.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') { closeMenu(); menuToggle.focus(); }
  });
  const cards = [...document.querySelectorAll('.stock-card')];
  const toggles = [...document.querySelectorAll('[data-group][aria-pressed]')];
  const search = document.getElementById('inventory-search');
  const category = document.getElementById('category-filter');
  const material = document.getElementById('material-filter');
  const condition = document.getElementById('condition-filter');
  const maker = document.getElementById('manufacturer-filter');
  const equipmentFilters = document.getElementById('equipment-filters');
  const status = document.getElementById('result-count');
  const fullLink = document.getElementById('full-inventory-link');
  let group = 'plants';
  function options(select, attribute, label) {
    const values = [...new Set(cards.filter(card => card.dataset.group === group).map(card => card.dataset[attribute]).filter(Boolean))].sort();
    select.replaceChildren(new Option(label, ''), ...values.map(value => new Option(value, value)));
  }
  function filter() {
    let count = 0;
    const query = search.value.trim().toLocaleLowerCase();
    cards.forEach(card => {
      const match = card.dataset.group === group && (!category.value || category.value === card.dataset.category) &&
        (!query || card.textContent.toLocaleLowerCase().includes(query)) &&
        (group !== 'equipment' || ((!material.value || material.value === card.dataset.material) &&
        (!condition.value || condition.value === card.dataset.condition) && (!maker.value || maker.value === card.dataset.manufacturer)));
      card.hidden = !match;
      if (match) count++;
    });
    const total = cards.filter(card => card.dataset.group === group).length;
    status.textContent = `${count} of ${total} featured ${group === 'plants' ? 'plant' : 'equipment'} listings`;
    document.getElementById('empty-results').hidden = count > 0;
  }
  function reset() { search.value = ''; [category, material, condition, maker].forEach(select => { select.value = ''; }); filter(); }
  function chooseGroup(next) {
    group = next;
    toggles.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.group === group)));
    equipmentFilters.hidden = group !== 'equipment';
    document.querySelector('label[for="category-filter"]').textContent = group === 'plants' ? 'Plant type' : 'Equipment type';
    options(category, 'category', group === 'plants' ? 'All plant types' : 'All equipment types');
    options(material, 'material', 'All materials'); options(condition, 'condition', 'All conditions'); options(maker, 'manufacturer', 'All manufacturers');
    fullLink.href = `https://ims.internationalprocessplants.com/inventory/search/${group}`;
    fullLink.textContent = group === 'plants' ? 'View all plant listings ↗' : 'View all equipment listings ↗';
    reset();
  }
  toggles.forEach(button => button.addEventListener('click', () => chooseGroup(button.dataset.group)));
  search.addEventListener('input', filter);
  [category, material, condition, maker].forEach(select => select.addEventListener('change', filter));
  document.getElementById('reset-filters').addEventListener('click', reset);
  document.getElementById('empty-reset').addEventListener('click', () => { reset(); search.focus(); });
  document.getElementById('inventory-tools').hidden = false;
  document.getElementById('inventory-filters').hidden = false;
  chooseGroup('plants');
})();

// Resources tabs: About Us, FAQs, Blog. Without JavaScript every panel stays visible.
(() => {
  'use strict';
  const list = document.querySelector('.tab-list');
  if (!list) return;
  const tabs = [...list.querySelectorAll('[role="tab"]')];
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
  function select(tab, focus) {
    tabs.forEach((item, index) => {
      const active = item === tab;
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
      panels[index].hidden = !active;
    });
    if (focus) tab.focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => select(tab, false));
    tab.addEventListener('keydown', event => {
      const keys = { ArrowRight: index + 1, ArrowLeft: index - 1, Home: 0, End: tabs.length - 1 };
      if (!(event.key in keys)) return;
      event.preventDefault();
      select(tabs[(keys[event.key] + tabs.length) % tabs.length], true);
    });
  });
  const fromHash = event => {
    const match = tabs.find(tab => '#' + tab.getAttribute('aria-controls') === window.location.hash);
    if (!match) return;
    select(match, false);
    // The browser may already have failed to scroll to the still-hidden panel. Jump on load, glide on hash change.
    const root = document.documentElement;
    const behavior = root.style.scrollBehavior;
    if (!event) root.style.scrollBehavior = 'auto';
    list.closest('section').scrollIntoView();
    root.style.scrollBehavior = behavior;
  };
  list.hidden = false;
  select(tabs[0], false);
  fromHash();
  window.addEventListener('hashchange', fromHash);
})();

// Customer testimonial videos: play inline on click, keep the YouTube link as the no-script fallback.
(() => {
  'use strict';
  document.querySelectorAll('.video-thumb[data-video]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
      event.preventDefault();
      const frame = document.createElement('iframe');
      frame.src = 'https://www.youtube-nocookie.com/embed/' + link.dataset.video + '?autoplay=1&rel=0';
      frame.title = link.dataset.title || 'Customer testimonial video';
      frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      frame.allowFullscreen = true;
      const box = document.createElement('div');
      box.className = 'video-frame';
      box.appendChild(frame);
      link.replaceWith(box);
    });
  });
})();
