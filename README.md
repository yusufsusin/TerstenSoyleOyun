# Tersten Söyle

Tarayıcıda çalışan, tek dosyalık bir ses oyunu. Mikrofona bir kelime ya da cümle söylersin, uygulama sesi tersine çevirir ve geri çalar.

## Nasıl Çalışır?

1. **Kaydet** — mikrofona konuş
2. **Tersine Çevir** — ses tamponu ters sırayla işlenir
3. **Çal** — tersine çevrilmiş ses oynatılır

Tüm işlem tarayıcı içinde, Web Audio API ile gerçekleşir; sunucuya hiçbir şey gönderilmez.

## Kullanım

`tersten-soyle.html` dosyasını doğrudan tarayıcıda aç — kurulum veya bağımlılık gerekmez.

## Teknoloji

- Vanilla JS
- Web Audio API (`AudioContext`, `MediaRecorder`)
- Google Fonts (Bricolage Grotesque, IBM Plex Mono)
