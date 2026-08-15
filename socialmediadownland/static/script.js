const form = document.getElementById('download-form');
const urlInput = document.getElementById('url-input');
const statusEl = document.getElementById('status');
const downloadBtn = document.getElementById('download-btn');

function setStatus(message, isError) {
  statusEl.textContent = message;
  statusEl.className = isError ? 'status error' : 'status';
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const url = urlInput.value.trim();
  const type = document.querySelector('input[name="type"]:checked').value;

  if (!url) {
    setStatus('Lütfen bir link girin.', true);
    return;
  }

  setStatus('İndiriliyor, lütfen bekleyin...', false);
  downloadBtn.disabled = true;

  try {
    const res = await fetch('/api/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, type }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'İndirme başarısız oldu.');
    }

    const disposition = res.headers.get('Content-Disposition') || '';
    const match = disposition.match(/filename\*?=(?:UTF-8'')?"?([^";]+)"?/i);
    const filename = match
      ? decodeURIComponent(match[1])
      : (type === 'audio' ? 'indirilen.mp3' : 'indirilen.mp4');

    const blob = await res.blob();
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);

    setStatus('İndirme tamamlandı.', false);
  } catch (err) {
    setStatus(err.message, true);
  } finally {
    downloadBtn.disabled = false;
  }
});
