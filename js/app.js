(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const yearEl = $('#year'); if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Home page: tool search + category filter ---------- */
  const grid = $('#toolGrid');
  if (grid) {
    const search = $('#toolSearch'); let activeCategory = 'All tools';
    const filterTools = () => {
      const q = (search?.value || '').trim().toLowerCase(); let visible = 0;
      grid.querySelectorAll('.tool-card').forEach(card => {
        const okQ = card.textContent.toLowerCase().includes(q);
        const okC = activeCategory === 'All tools' || card.dataset.category === activeCategory;
        card.hidden = !(okQ && okC); if (!card.hidden) visible++;
      });
      const empty = $('#emptySearch'); if (empty) empty.hidden = visible !== 0;
    };
    search?.addEventListener('input', filterTools);
    document.querySelectorAll('.category-pill').forEach(pill => pill.addEventListener('click', () => {
      document.querySelectorAll('.category-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active'); activeCategory = pill.textContent.trim(); filterTools();
    }));
  }

  /* ---------- Tool pages ---------- */
  const panel = $('#toolPanel'); if (!panel) return;
  const key = panel.dataset.tool;
  const PDF_ACCEPT = '.pdf,application/pdf';
  const IMG_ACCEPT = 'image/jpeg,image/png,image/webp,.jpg,.jpeg,.png,.webp';
  const toolInfo = {
    compress: { action: 'Compress PDF', accept: PDF_ACCEPT, multiple: false },
    image:    { action: 'Create PDF', accept: IMG_ACCEPT, multiple: true },
    merge:    { action: 'Merge PDFs', accept: PDF_ACCEPT, multiple: true },
    split:    { action: 'Extract pages', accept: PDF_ACCEPT, multiple: false },
    rotate:   { action: 'Rotate PDF', accept: PDF_ACCEPT, multiple: false },
    pages:    { action: 'Count pages', accept: PDF_ACCEPT, multiple: false },
    info:     { action: 'Show information', accept: PDF_ACCEPT, multiple: false }
  };
  const info = toolInfo[key]; if (!info) return;
  const fields = $('#toolFields'), status = $('#statusMessage'), runBtn = $('#runTool'), resultLink = $('#resultLink');
  let files = [], lastUrl = null;
  class UserError extends Error {}

  if (window.pdfjsLib) pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

  const setStatus = (m, kind = '') => { status.textContent = m; status.className = 'status-message' + (kind ? ' ' + kind : ''); };
  const formatBytes = n => n < 1024 ? n + ' B' : n < 1048576 ? (n / 1024).toFixed(1) + ' KB' : (n / 1048576).toFixed(2) + ' MB';
  const setRunLabel = () => { runBtn.innerHTML = ''; runBtn.append(info.action + ' '); const a = document.createElement('span'); a.textContent = '→'; runBtn.append(a); };

  function buildFields() {
    const multi = info.multiple;
    let html = `<label class="field-label" for="fileInput">${multi ? 'Choose your files' : 'Choose a file'}</label>
      <label class="file-drop" id="dropZone"><span class="upload-symbol" aria-hidden="true">↑</span><strong>Click to select ${multi ? 'files' : 'a file'} or drag and drop</strong><small>${key === 'image' ? 'JPG, PNG or WebP images' : 'PDF files only'} · processed on your device</small><input id="fileInput" type="file" accept="${info.accept}" ${multi ? 'multiple' : ''}></label>
      <ul class="file-list" id="fileList" aria-live="polite"></ul><div class="file-empty" id="fileEmpty">No files selected yet.</div>`;
    if (key === 'split') html += '<label class="field-label" for="pagesInput">Pages to extract</label><input class="field-input" id="pagesInput" type="text" inputmode="numeric" placeholder="Example: 1,3-5"><div class="field-help">Page numbers start at 1. Ranges are inclusive, for example 1,3-5 keeps pages 1, 3, 4 and 5.</div>';
    if (key === 'rotate') html += '<label class="field-label" for="rotateAngle">Rotation angle</label><select class="field-select" id="rotateAngle"><option value="90">90° clockwise</option><option value="180">180°</option><option value="270">270° clockwise (90° counter-clockwise)</option></select>';
    if (key === 'compress') html += '<label class="field-label" for="quality">Compression level</label><select class="field-select" id="quality"><option value="0.48">Strong compression — smallest file, lower quality</option><option value="0.65" selected>Balanced — recommended</option><option value="0.82">High quality — larger file</option></select><div class="field-help">This creates an image-based PDF. Text will no longer be selectable or searchable.</div>';
    if (key === 'image') html += '<label class="field-label" for="pageSize">PDF page size</label><select class="field-select" id="pageSize"><option value="a4">A4</option><option value="letter">US Letter</option><option value="fit">Fit page to each image</option></select><div class="field-help">Images are centred and scaled proportionally. Use the arrows to change the page order.</div>';
    if (key === 'merge') html += '<div class="field-help">Use the arrows to set the order. The first file in the list becomes the first pages of the merged PDF.</div>';
    fields.innerHTML = html; setRunLabel(); runBtn.disabled = false;
    const input = $('#fileInput'), drop = $('#dropZone');
    input.addEventListener('change', () => { addFiles([...input.files]); input.value = ''; });
    ['dragenter', 'dragover'].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.add('drag'); }));
    ['dragleave', 'drop'].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove('drag'); }));
    drop.addEventListener('drop', e => addFiles([...(e.dataTransfer?.files || [])]));
  }

  function acceptable(f) {
    const n = f.name.toLowerCase();
    if (key === 'image') return /^image\/(jpeg|png|webp)$/.test(f.type) || /\.(jpe?g|png|webp)$/.test(n);
    return f.type === 'application/pdf' || n.endsWith('.pdf');
  }
  function addFiles(list) {
    const ok = list.filter(acceptable); const bad = list.length - ok.length;
    if (!ok.length && bad) { setStatus(key === 'image' ? 'Please choose JPG, PNG or WebP images.' : 'Please choose PDF files.', 'error'); return; }
    files = info.multiple ? files.concat(ok) : ok.slice(0, 1);
    setStatus(bad ? `${bad} file(s) were skipped because the type is not supported.` : ''); hideResult(); renderList();
  }
  function renderList() {
    const ul = $('#fileList'); ul.innerHTML = ''; $('#fileEmpty').hidden = files.length > 0;
    files.forEach((f, i) => {
      const li = document.createElement('li');
      const nm = document.createElement('span'); nm.className = 'fname'; nm.textContent = `${i + 1}. ${f.name}`; nm.title = f.name;
      const sz = document.createElement('span'); sz.className = 'fsize'; sz.textContent = formatBytes(f.size);
      li.append(nm, sz);
      const mk = (label, aria, disabled, fn) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = label; b.setAttribute('aria-label', aria); b.disabled = disabled; b.addEventListener('click', fn); return b; };
      if (info.multiple && files.length > 1) {
        li.append(mk('↑', 'Move up', i === 0, () => { [files[i - 1], files[i]] = [files[i], files[i - 1]]; renderList(); }));
        li.append(mk('↓', 'Move down', i === files.length - 1, () => { [files[i + 1], files[i]] = [files[i], files[i + 1]]; renderList(); }));
      }
      li.append(mk('✕', 'Remove file', false, () => { files.splice(i, 1); hideResult(); renderList(); }));
      ul.append(li);
    });
  }

  function hideResult() { resultLink.classList.remove('show'); }
  function deliver(blob, name) {
    if (lastUrl) URL.revokeObjectURL(lastUrl);
    lastUrl = URL.createObjectURL(blob);
    resultLink.href = lastUrl; resultLink.download = name; resultLink.textContent = 'Download again: ' + name; resultLink.classList.add('show');
    const a = document.createElement('a'); a.href = lastUrl; a.download = name; document.body.appendChild(a); a.click(); a.remove();
  }
  const safeName = (file, suffix = '') => (file.name.replace(/\.[a-z0-9]+$/i, '').replace(/[^a-z0-9-_]+/gi, '_') || 'document') + suffix + '.pdf';

  runBtn.addEventListener('click', async () => {
    if (!files.length) { setStatus('Please choose a file first.', 'error'); return; }
    runBtn.disabled = true; runBtn.textContent = 'Working…'; setStatus('Preparing your document…'); hideResult();
    try {
      if (key === 'merge') await mergePdfs(files);
      else if (key === 'split') await splitPdf(files[0]);
      else if (key === 'rotate') await rotatePdf(files[0]);
      else if (key === 'pages' || key === 'info') await inspectPdf(files[0]);
      else if (key === 'image') await imagesToPdf(files);
      else if (key === 'compress') await compressPdf(files[0]);
    } catch (err) {
      console.error(err);
      setStatus(err instanceof UserError ? err.message : ((err && err.message ? err.message + ' ' : '') + 'The file may be password-protected, damaged, or too large for your device.'), 'error');
    } finally { runBtn.disabled = false; setRunLabel(); }
  });

  const needLib = (ok, name) => { if (!ok) throw new UserError(`The ${name} library did not load. Check your internet connection and reload the page.`); };
  const loadPdf = async f => PDFLib.PDFDocument.load(await f.arrayBuffer());

  async function mergePdfs(list) {
    needLib(window.PDFLib, 'PDF'); if (list.length < 2) throw new UserError('Select at least two PDF files to merge.');
    setStatus(`Merging ${list.length} documents…`); const merged = await PDFLib.PDFDocument.create();
    for (const f of list) { const doc = await loadPdf(f); const pages = await merged.copyPages(doc, doc.getPageIndices()); pages.forEach(p => merged.addPage(p)); }
    deliver(new Blob([await merged.save({ useObjectStreams: true })], { type: 'application/pdf' }), 'merged_document.pdf');
    setStatus(`Done! ${list.length} PDFs were combined into one file.`, 'success');
  }
  async function splitPdf(file) {
    needLib(window.PDFLib, 'PDF'); const doc = await loadPdf(file); const total = doc.getPageCount();
    const raw = ($('#pagesInput').value || '').trim(); if (!raw) throw new UserError('Enter the page numbers to extract, such as 1,3-5.');
    const selected = new Set();
    for (const part of raw.split(',')) {
      const p = part.trim(); const r = p.match(/^(\d+)\s*-\s*(\d+)$/);
      if (r) { let a = +r[1], b = +r[2]; if (a > b) [a, b] = [b, a]; if (a < 1 || b > total) throw new UserError(`Page range must be between 1 and ${total}.`); for (let i = a; i <= b; i++) selected.add(i - 1); }
      else if (/^\d+$/.test(p)) { const n = +p; if (n < 1 || n > total) throw new UserError(`Page number must be between 1 and ${total}.`); selected.add(n - 1); }
      else throw new UserError('Use page numbers like 1,3-5.');
    }
    setStatus('Extracting pages…'); const out = await PDFLib.PDFDocument.create();
    (await out.copyPages(doc, [...selected].sort((a, b) => a - b))).forEach(p => out.addPage(p));
    deliver(new Blob([await out.save({ useObjectStreams: true })], { type: 'application/pdf' }), safeName(file, '_split'));
    setStatus(`Done! Extracted ${selected.size} page(s) from ${total}.`, 'success');
  }
  async function rotatePdf(file) {
    needLib(window.PDFLib, 'PDF'); const doc = await loadPdf(file); const angle = Number($('#rotateAngle').value);
    doc.getPages().forEach(pg => pg.setRotation(PDFLib.degrees((pg.getRotation().angle + angle) % 360)));
    deliver(new Blob([await doc.save({ useObjectStreams: true })], { type: 'application/pdf' }), safeName(file, '_rotated'));
    setStatus(`Done! Rotated ${doc.getPageCount()} page(s) by ${angle}°.`, 'success');
  }
  async function inspectPdf(file) {
    needLib(window.PDFLib, 'PDF'); const doc = await loadPdf(file); const n = doc.getPageCount();
    if (key === 'pages') { setStatus(`This PDF contains ${n} page${n === 1 ? '' : 's'}.\nFile size: ${formatBytes(file.size)}.`, 'success'); return; }
    const first = doc.getPage(0).getSize(); const dim = `${Math.round(first.width)} × ${Math.round(first.height)} pt (page 1)`;
    const nv = v => v || 'Not specified';
    const d = x => x ? x.toLocaleString() : 'Not specified';
    setStatus([`File: ${file.name}`, `Size: ${formatBytes(file.size)}`, `Pages: ${n}`, `Page size: ${dim}`, `Title: ${nv(doc.getTitle())}`, `Author: ${nv(doc.getAuthor())}`, `Subject: ${nv(doc.getSubject())}`, `Creator: ${nv(doc.getCreator())}`, `Producer: ${nv(doc.getProducer())}`, `Created: ${d(doc.getCreationDate())}`, `Modified: ${d(doc.getModificationDate())}`].join('\n'), 'success');
  }

  const readAsDataURL = f => new Promise((res, rej) => { const r = new FileReader(); r.onload = () => res(r.result); r.onerror = () => rej(new Error('Could not read an image file.')); r.readAsDataURL(f); });
  const loadImage = src => new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = () => rej(new Error('Could not decode one of the images.')); i.src = src; });
  async function prepImage(file) {
    const dataUrl = await readAsDataURL(file); const img = await loadImage(dataUrl);
    const w = img.naturalWidth, h = img.naturalHeight;
    if (file.type === 'image/jpeg') return { dataUrl, fmt: 'JPEG', w, h };
    if (file.type === 'image/png') return { dataUrl, fmt: 'PNG', w, h };
    const c = document.createElement('canvas'); c.width = w; c.height = h; const ctx = c.getContext('2d');
    ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, w, h); ctx.drawImage(img, 0, 0);
    return { dataUrl: c.toDataURL('image/jpeg', 0.92), fmt: 'JPEG', w, h };
  }
  async function imagesToPdf(list) {
    needLib(window.jspdf, 'PDF creation'); const { jsPDF } = window.jspdf; const mode = $('#pageSize').value; let pdf = null;
    for (let i = 0; i < list.length; i++) {
      setStatus(`Adding image ${i + 1} of ${list.length}…`); const im = await prepImage(list[i]);
      const orientation = im.w > im.h ? 'landscape' : 'portrait';
      let fmt = mode === 'letter' ? 'letter' : 'a4';
      if (mode === 'fit') fmt = [Math.max(72, im.w * 0.75), Math.max(72, im.h * 0.75)];
      if (!pdf) pdf = new jsPDF({ orientation, unit: 'pt', format: fmt, compress: true }); else pdf.addPage(fmt, orientation);
      const pw = pdf.internal.pageSize.getWidth(), ph = pdf.internal.pageSize.getHeight(); const m = mode === 'fit' ? 0 : 18;
      const s = Math.min((pw - m * 2) / im.w, (ph - m * 2) / im.h); const w = im.w * s, h = im.h * s;
      pdf.addImage(im.dataUrl, im.fmt, (pw - w) / 2, (ph - h) / 2, w, h, undefined, 'FAST');
    }
    deliver(pdf.output('blob'), 'images_to_pdf.pdf'); setStatus(`Done! Created a PDF from ${list.length} image(s).`, 'success');
  }
  async function compressPdf(file) {
    needLib(window.pdfjsLib && window.jspdf, 'PDF rendering');
    const quality = Number($('#quality').value); setStatus('Opening PDF for image-based compression…');
    const src = await pdfjsLib.getDocument({ data: await file.arrayBuffer() }).promise; const { jsPDF } = window.jspdf; let out = null;
    for (let i = 1; i <= src.numPages; i++) {
      setStatus(`Compressing page ${i} of ${src.numPages}…`); const page = await src.getPage(i); const base = page.getViewport({ scale: 1 });
      const maxW = quality < 0.55 ? 1050 : quality < 0.75 ? 1400 : 1800; const scale = Math.min(maxW / base.width, 2); const vp = page.getViewport({ scale: Math.max(0.6, scale) });
      const canvas = document.createElement('canvas'); canvas.width = Math.ceil(vp.width); canvas.height = Math.ceil(vp.height);
      const ctx = canvas.getContext('2d', { alpha: false }); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, canvas.width, canvas.height);
      await page.render({ canvasContext: ctx, viewport: vp }).promise;
      const image = canvas.toDataURL('image/jpeg', quality); const orient = base.width > base.height ? 'landscape' : 'portrait';
      if (!out) out = new jsPDF({ orientation: orient, unit: 'pt', format: [base.width, base.height], compress: true }); else out.addPage([base.width, base.height], orient);
      out.addImage(image, 'JPEG', 0, 0, base.width, base.height, undefined, 'FAST'); canvas.width = 0; canvas.height = 0;
    }
    const blob = out.output('blob'); deliver(blob, safeName(file, '_compressed'));
    const delta = file.size - blob.size; const pct = file.size ? Math.round((delta / file.size) * 100) : 0;
    setStatus(`Done! Original: ${formatBytes(file.size)}. New file: ${formatBytes(blob.size)}. ` + (delta > 0 ? `Size reduced by ${pct}%.` : `The result is ${formatBytes(-delta)} larger than the original, so keep your original file.`) + ' Note: the new PDF has no selectable text.', 'success');
  }

  buildFields(); renderList();
})();
