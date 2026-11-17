const form = document.querySelector('#scan-form');
const status = document.querySelector('#status');
const button = document.querySelector('#scan-button');
function size(n) {
  const units = ['o', 'Ko', 'Mo', 'Go', 'To']; let i = 0;
  while (n >= 1024 && i < units.length - 1) { n /= 1024; i++; }
  return `${n.toLocaleString('fr-FR', {maximumFractionDigits: 1})} ${units[i]}`;
}
form.addEventListener('submit', async (event) => {
  event.preventDefault(); button.disabled = true; status.textContent = 'Analyse en cours…';
  document.querySelector('#count').textContent = '—';
  document.querySelector('#size').textContent = '—';
  document.querySelector('#files').replaceChildren();
  document.querySelector('#categories').replaceChildren();
  try {
    const response = await fetch('/scan', {method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({path: document.querySelector('#path').value})});
    const report = await response.json();
    if (!response.ok) throw new Error(report.error || 'Analyse impossible.');
    document.querySelector('#count').textContent = report.total_files.toLocaleString('fr-FR');
    document.querySelector('#size').textContent = size(report.total_size_bytes);
    const categories = document.querySelector('#categories'); categories.replaceChildren();
    for (const [name, data] of Object.entries(report.categories)) {
      const line = document.createElement('div'); line.className = 'category';
      line.textContent = `${name} · ${data.count} fichiers · ${size(data.size_bytes)}`;
      categories.append(line);
    }
    const body = document.querySelector('#files'); body.replaceChildren();
    for (const file of report.files) {
      const row = document.createElement('tr');
      for (const value of [file.path, file.category, size(file.size_bytes), file.modified_at.slice(0, 10)]) {
        const cell = document.createElement('td'); cell.textContent = value; row.append(cell);
      }
      body.append(row);
    }
    status.textContent = `${report.total_files ? 'Analyse terminée.' : 'Dossier vide.'} ${report.truncated ? 'Limite atteinte : résultat partiel.' : ''} ${report.warnings.length ? 'Certains éléments sont inaccessibles.' : ''}`;
  } catch (error) { status.textContent = error.message; }
  finally { button.disabled = false; }
});
