const form = document.getElementById('setup-form');
const output = document.getElementById('output');
const list = document.getElementById('recommendations');
const promptBox = document.getElementById('llm_prompt');

const csvToArray = (value) =>
  value
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = {
    car: document.getElementById('car').value.trim(),
    track: document.getElementById('track').value.trim(),
    weather: document.getElementById('weather').value,
    time_of_day: document.getElementById('time_of_day').value,
    custom_parts: csvToArray(document.getElementById('custom_parts').value),
    struggles: csvToArray(document.getElementById('struggles').value),
  };

  const response = await fetch('/api/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  list.innerHTML = '';

  data.recommendations.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = `[${item.area}] ${item.adjustment} — ${item.reason}`;
    list.appendChild(li);
  });

  promptBox.textContent = data.llm_prompt;
  output.classList.remove('hidden');
});
