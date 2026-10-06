(() => {
  const search = document.getElementById('page-search');
  const category = document.getElementById('category-filter');
  const families = [...document.querySelectorAll('.family')];
  const status = document.getElementById('results-count');
  const empty = document.getElementById('empty-state');
  const expand = document.getElementById('expand-all');
  const originalStatus = status.textContent;
  const normalize = text => text.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  let expandAllRequested = false;

  function syncExpandButton() {
    const details = families.filter(family => !family.hidden).flatMap(family => [...family.querySelectorAll('details')]);
    const expanded = details.length > 0 && details.every(detail => detail.open);
    expand.hidden = details.length === 0;
    expand.setAttribute('aria-pressed', String(expanded));
    expand.textContent = expanded ? 'Collapse all types −' : 'Expand all types +';
  }

  function filter() {
    const terms = normalize(search.value).split(' ').filter(Boolean);
    const selected = category.value;
    let visible = 0;
    families.forEach(family => {
      const familyName = normalize(family.dataset.familyName);
      const groupMatches = terms.every(term => familyName.includes(term));
      const rows = [...family.querySelectorAll('li[data-page-title]')];
      let matchingTypes = 0;
      rows.forEach(row => {
        const text = `${familyName} ${normalize(row.dataset.pageTitle)}`;
        const match = terms.every(term => text.includes(term));
        row.hidden = !match;
        if (match) matchingTypes++;
      });
      const allowed = selected === 'all' || selected === family.dataset.category;
      family.hidden = !allowed || !(groupMatches || matchingTypes > 0);
      if (!family.hidden) visible++;
      const details = family.querySelector('details');
      if (details) {
        details.hidden = matchingTypes === 0;
        details.open = !family.hidden && (terms.length > 0 || selected !== 'all' || expandAllRequested);
      }
    });
    empty.hidden = visible !== 0;
    status.textContent = !terms.length && selected === 'all' ? originalStatus : `${visible} ${visible === 1 ? 'category' : 'categories'} shown`;
    syncExpandButton();
  }

  function clear() {
    search.value = '';
    category.value = 'all';
    expandAllRequested = false;
    filter();
    search.focus({ preventScroll: true });
  }

  search.addEventListener('input', filter);
  category.addEventListener('change', filter);
  document.getElementById('clear-filters').addEventListener('click', clear);
  document.getElementById('empty-reset').addEventListener('click', clear);
  expand.addEventListener('click', () => {
    const expanded = expand.getAttribute('aria-pressed') !== 'true';
    expandAllRequested = expanded;
    families.filter(family => !family.hidden).forEach(family => {
      const details = family.querySelector('details');
      if (details) details.open = expanded;
    });
    syncExpandButton();
  });
  families.forEach(family => family.querySelector('details')?.addEventListener('toggle', syncExpandButton));
  document.getElementById('directory-controls').hidden = false;
  expand.hidden = false;
  filter();
})();
