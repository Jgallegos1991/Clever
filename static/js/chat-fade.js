// Chat fade lifecycle (extracted from inline script)
// Why: Manage ephemeral chat bubble injection + timed fade without inline <script> (CSP compliance)
// Where: Loaded by templates/index.html after main.js so MutationObserver sees appended messages
// How: Observe #chat-log for new .message nodes, schedule fade-out + removal.
(function(){
  const AUTO_HIDE_MS = 9000;
  function scheduleFade(node){
    setTimeout(()=>{
      node.classList.add('fade-out');
      setTimeout(()=> node.remove(), 1400);
    }, AUTO_HIDE_MS);
  }
  const log = document.getElementById('chat-log');
  if(!log) return;
  const observer = new MutationObserver(muts => {
    muts.forEach(m => m.addedNodes.forEach(n => {
      if(!(n instanceof HTMLElement)) return;
      if(!n.classList.contains('message')) return;
      scheduleFade(n);
    }));
  });
  observer.observe(log, { childList:true });
})();
