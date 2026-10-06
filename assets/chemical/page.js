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
