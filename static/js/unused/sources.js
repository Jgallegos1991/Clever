(async function(){
  const listEl = document.getElementById('list');
  const qEl = document.getElementById('q');
  const titleEl = document.getElementById('title');
  const contentEl = document.getElementById('content');
  const params = new URLSearchParams(window.location.search);
  const selectId = params.get('select');

  async function fetchSources(q){
    const url = q ? '/sources?search=' + encodeURIComponent(q) : '/sources';
    const res = await fetch(url);
    return await res.json();
  }
  async function renderList(items){
    listEl.innerHTML = '';
    items.forEach(it => {
      const div = document.createElement('div');
      div.className = 'msg assistant';
      div.style.cursor='pointer';
      div.textContent = `#${it.id} • ${it.filename} • ${Math.floor((it.size||0)/1024)} KB`;
      div.onclick = async ()=>{
        const res = await fetch(`/sources/${it.id}?content=true`);
        const full = await res.json();
        titleEl.textContent = `${full.filename}`;
        contentEl.textContent = full.content || '';
      };
      listEl.appendChild(div);
    });
    // auto open selected item if requested
    if (selectId){
      const target = items.find(x => String(x.id) === String(selectId));
      if (target){
        const res = await fetch(`/sources/${target.id}?content=true`);
        const full = await res.json();
        titleEl.textContent = `${full.filename}`;
        contentEl.textContent = full.content || '';
      }
    }
  }
  const data = await fetchSources('');
  await renderList(data);
  let t;
  qEl.addEventListener('input', async ()=>{
    clearTimeout(t);
    t = setTimeout(async ()=>{
      const data = await fetchSources(qEl.value.trim());
      await renderList(data);
    }, 200);
  });
})();
