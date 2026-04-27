/* Teléfono CL: +56 9 1234 5678 (sólo formatea; backend valida) */
function formatPhone(value) {
  // deja sólo dígitos
  const digits = value.replace(/\D/g, '');
  // si empieza con 56 lo cortamos a 11~12 dígitos máx
  let v = digits;
  if (v.startsWith('56')) v = v.slice(2);
  // estructura: 9 XXXXXXXX -> 9 1234 5678
  if (v.length <= 1) return v;
  const p1 = v.slice(0, 1);        // 9
  const p2 = v.slice(1, 5);        // 1234
  const p3 = v.slice(5, 9);        // 5678
  return `${p1}${p2 ? ' ' + p2 : ''}${p3 ? ' ' + p3 : ''}`.trim();
}

/* RUT: formateo y validación simple (módulo 11) */
function formatRut(raw) {
  let v = raw.replace(/[^\dkK]/g, '').toUpperCase();
  if (v.length <= 1) return v;
  const body = v.slice(0, -1);
  const dv = v.slice(-1);
  // agrega puntos al cuerpo
  const withDots = body.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  return `${withDots}-${dv}`;
}

function rutIsValid(rut) {
  rut = rut.replace(/[.\-]/g, '').toUpperCase();
  if (!/^\d{1,8}[0-9K]$/.test(rut)) return false;
  const body = rut.slice(0, -1);
  const dv = rut.slice(-1);
  let sum = 0, mul = 2;
  for (let i = body.length - 1; i >= 0; i--) {
    sum += parseInt(body[i], 10) * mul;
    mul = mul === 7 ? 2 : mul + 1;
  }
  const res = 11 - (sum % 11);
  const dvCalc = res === 11 ? '0' : res === 10 ? 'K' : String(res);
  return dvCalc === dv;
}

/* Auto-aplicar a inputs por data-attrs */
document.addEventListener('DOMContentLoaded', () => {
  // Teléfono
  document.querySelectorAll('[data-mask="cl-phone"]').forEach(inp => {
    inp.addEventListener('input', (e) => {
      const pos = e.target.selectionStart;
      e.target.value = formatPhone(e.target.value);
      e.target.setSelectionRange(pos, pos);
    });
  });

  // RUT
  document.querySelectorAll('[data-mask="rut"]').forEach(inp => {
    const updateError = (ok) => {
      const help = inp.closest('.col-12, .col-md-5, .col-md-6')?.querySelector('.help-error.front');
      if (!help) return;
      help.textContent = ok ? '' : 'Por favor ingresa un RUT válido';
    };
    inp.addEventListener('input', (e) => {
      const pos = e.target.selectionStart;
      e.target.value = formatRut(e.target.value);
      e.target.setSelectionRange(pos, pos);
      // validación suave mientras escribe (opcional)
      const justDigits = e.target.value.replace(/[.\-]/g, '');
      if (justDigits.length >= 8) updateError(rutIsValid(e.target.value));
      else updateError(true);
    });
    inp.addEventListener('blur', () => updateError(rutIsValid(inp.value)));
    // placeholder bonito
    if (!inp.placeholder) inp.placeholder = '12.345.678-5';
    // lugar para error front
    const container = inp.closest('.col-12, .col-md-5, .col-md-6');
    if (container && !container.querySelector('.help-error.front')) {
      const div = document.createElement('div');
      div.className = 'help-error front';
      container.appendChild(div);
    }
  });
});

export { formatPhone, formatRut, rutIsValid };