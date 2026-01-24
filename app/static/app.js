const statusEl = document.getElementById("bot-status");
const modeEl = document.getElementById("bot-mode");
const lastActionEl = document.getElementById("last-action");
const logListEl = document.getElementById("log-list");
const accountsCountEl = document.getElementById("accounts-count");
const quoteListEl = document.getElementById("quote-list");

async function fetchStatus() {
  const response = await fetch("/api/status");
  const data = await response.json();
  statusEl.textContent = data.running ? "Running" : "Stopped";
  modeEl.textContent = data.mode;
  lastActionEl.textContent = data.last_action || "No actions yet";
}

async function fetchLogs() {
  const response = await fetch("/api/bot/logs");
  const data = await response.json();
  logListEl.innerHTML = data.logs
    .slice()
    .reverse()
    .map((log) => `<div>${log}</div>`)
    .join("");
}

async function refreshAccounts() {
  try {
    const response = await fetch("/api/accounts");
    const data = await response.json();
    accountsCountEl.textContent = data.accounts.length;
  } catch (error) {
    accountsCountEl.textContent = "!";
  }
}

async function loadQuotes() {
  const symbols = document.getElementById("symbols-input").value;
  if (!symbols.trim()) {
    quoteListEl.innerHTML = "<div class=\"muted\">Enter symbols to load quotes.</div>";
    return;
  }
  try {
    const response = await fetch(`/api/quotes?symbols=${encodeURIComponent(symbols)}`);
    const data = await response.json();
    if (!data.quotes || data.quotes.length === 0) {
      quoteListEl.innerHTML = "<div class=\"muted\">No quotes returned.</div>";
      return;
    }
    quoteListEl.innerHTML = data.quotes
      .map(
        (quote) => `
        <div class="quote-item">
          <span>${quote.symbol || "--"}</span>
          <span>${quote.lastTradePrice ?? "--"}</span>
        </div>`
      )
      .join("");
  } catch (error) {
    quoteListEl.innerHTML = "<div class=\"muted\">Unable to load quotes.</div>";
  }
}

async function startBot() {
  await fetch("/api/bot/start", { method: "POST" });
  await fetchStatus();
  await fetchLogs();
}

async function stopBot() {
  await fetch("/api/bot/stop", { method: "POST" });
  await fetchStatus();
  await fetchLogs();
}

document.getElementById("start-btn").addEventListener("click", startBot);
document.getElementById("stop-btn").addEventListener("click", stopBot);
document.getElementById("refresh-accounts").addEventListener("click", refreshAccounts);
document.getElementById("load-quotes").addEventListener("click", loadQuotes);

fetchStatus();
fetchLogs();
