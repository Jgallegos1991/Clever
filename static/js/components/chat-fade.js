// Chat fade lifecycle (extracted from inline script)
// Why: Manage ephemeral chat bubble injection + timed fade without inline <script> (CSP compliance)
// Where: Loaded by templates/index.html after main.js so MutationObserver sees appended messages
// How: Observe #chat-log for new .message nodes, schedule fade-out + removal.
(function(){
  const AUTO_HIDE_MS = 18000; // Slowed down from 9000ms to 18000ms for more comfortable reading
  function scheduleFade(node){
    setTimeout(()=>{
      node.classList.add('fade-out');
      setTimeout(()=> node.remove(), 2800); // Slowed down fade duration from 1400ms to 2800ms
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
