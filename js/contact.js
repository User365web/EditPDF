(() => {
  'use strict';
  const form = document.getElementById('contactForm'); if (!form) return;
  const status = document.getElementById('contactStatus');
  const EMAIL = (form.dataset.email || '').trim();
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (!EMAIL || !EMAIL.includes('@') || EMAIL.includes('REPLACE')) {
      status.textContent = 'The contact email has not been configured yet.'; status.style.color = '#d34d52'; return;
    }
    const d = new FormData(form); const name = String(d.get('name') || '').trim(), email = String(d.get('email') || '').trim();
    const topic = String(d.get('topic') || 'General feedback'), message = String(d.get('message') || '').trim();
    const subject = encodeURIComponent(`[EditPDF] ${topic}`);
    const body = encodeURIComponent(`Name: ${name || 'Not provided'}\nReply email: ${email}\nTopic: ${topic}\n\n${message}`);
    status.textContent = 'Opening your email application. Review the message and press Send there.'; status.style.color = '#19845f';
    window.location.href = `mailto:${EMAIL}?subject=${subject}&body=${body}`;
  });
})();
