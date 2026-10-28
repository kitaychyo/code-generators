const form = document.querySelector('#login-form');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = form.querySelector('button');
  const error = document.querySelector('#error');
  button.disabled = true;
  error.textContent = '';
  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      cache: 'no-store',
      credentials: 'omit',
      body: JSON.stringify({ username: form.username.value, password: form.password.value }),
    });
    const data = await response.json();
    if (!response.ok) {
      error.textContent = data.error || 'Не удалось войти.';
      return;
    }
    form.reset();
    document.querySelector('#code').textContent = data.code;
    document.querySelector('#login-section').hidden = true;
    document.querySelector('#result').hidden = false;
  } catch {
    error.textContent = 'Ошибка соединения. Попробуйте снова.';
  } finally {
    button.disabled = false;
  }
});
// Back/forward cache must not restore the previously displayed code.
window.addEventListener('pageshow', (event) => {
  if (event.persisted) window.location.reload();
});
