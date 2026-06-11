/* Liturgical Calendar — client-side scripts */

// ---------------------------------------------------------------------------
// Scripture popup — fetches text from BibleGateway via a proxy-free approach:
// opens BibleGateway in a sandboxed iframe if possible; otherwise falls back
// to showing the reference and a direct link.
// ---------------------------------------------------------------------------

function getTranslationPref() {
  return localStorage.getItem('lcms_translation') || 'ESV';
}

function showScripture(event, ref, bgUrl) {
  if (event) event.preventDefault();
  const modal   = document.getElementById('scripture-modal');
  const refEl   = document.getElementById('modal-ref');
  const bodyEl  = document.getElementById('modal-body');
  const linkEl  = document.getElementById('modal-link');

  const trans = getTranslationPref();
  bgUrl = bgUrl.replace(/version=[A-Za-z]+/, 'version=' + trans);

  refEl.textContent  = ref + (trans !== 'ESV' ? ' (' + trans + ')' : '');
  bodyEl.textContent = '';
  linkEl.href        = bgUrl;
  modal.style.display = 'flex';

  if (trans === 'KJV') {
    // KJV is public domain — bible-api.com serves it without a key
    fetch('https://bible-api.com/' + encodeURIComponent(ref) + '?translation=kjv')
      .then(r => { if (!r.ok) throw new Error('unavailable'); return r.json(); })
      .then(data => {
        if (data.text) bodyEl.textContent = data.text.trim();
        else showFallback(bodyEl, ref, bgUrl);
      })
      .catch(() => showFallback(bodyEl, ref, bgUrl));
    return;
  }

  // Try ESV API (free key — replace with your own from api.esv.org)
  const ESV_API_KEY = '146f3dcaf64091437ccf1e1268b999e901c6c4c8';
  const apiUrl = `https://api.esv.org/v3/passage/text/?q=${encodeURIComponent(ref)}&include-headings=false&include-footnotes=false&include-verse-numbers=true&include-short-copyright=false`;

  fetch(apiUrl, {
    headers: { 'Authorization': `Token ${ESV_API_KEY}` }
  })
  .then(r => {
    if (!r.ok) throw new Error('API unavailable');
    return r.json();
  })
  .then(data => {
    const passages = data.passages;
    if (passages && passages.length > 0) {
      bodyEl.textContent = passages[0].trim();
    } else {
      showFallback(bodyEl, ref, bgUrl);
    }
  })
  .catch(() => {
    showFallback(bodyEl, ref, bgUrl);
  });
}

function showFallback(bodyEl, ref, bgUrl) {
  bodyEl.innerHTML =
    `<em>Scripture preview requires an ESV API key.<br>` +
    `Click the link below to read <strong>${escHtml(ref)}</strong> at BibleGateway.</em>`;
}

function escHtml(text) {
  return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function closeScripture() {
  document.getElementById('scripture-modal').style.display = 'none';
}

// Close modal on backdrop click
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('scripture-modal');
  if (modal) {
    modal.addEventListener('click', e => {
      if (e.target === modal) closeScripture();
    });
  }
  // Point BibleGateway hrefs at the preferred translation
  const trans = getTranslationPref();
  if (trans !== 'ESV') {
    document.querySelectorAll('a.scripture-link[href*="biblegateway"]').forEach(a => {
      a.href = a.href.replace(/version=[A-Za-z]+/, 'version=' + trans);
    });
  }
});

// Close on Escape key
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeScripture();
});
