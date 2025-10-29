const $ = (sel) => document.querySelector(sel);

function prettyPrint(target, data) {
  target.textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
}

async function getJSON(url, options) {
  const res = await fetch(url, options);
  const contentType = res.headers.get("content-type") || "";
  if (!res.ok) {
    const errText = await res.text().catch(() => res.statusText);
    throw new Error(`${res.status} ${res.statusText} - ${errText}`);
  }
  if (contentType.includes("application/json")) return res.json();
  return res.text();
}

document.addEventListener("DOMContentLoaded", () => {
  const healthBtn = $("#healthBtn");
  const healthOut = $("#healthOut");
  const echoForm = $("#echoForm");
  const echoOut = $("#echoOut");
  const year = $("#year");

  year.textContent = String(new Date().getFullYear());

  healthBtn.addEventListener("click", async () => {
    try {
      prettyPrint(healthOut, "Loading...");
      const data = await getJSON("/api/health");
      prettyPrint(healthOut, data);
    } catch (err) {
      prettyPrint(healthOut, String(err));
    }
  });

  echoForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const message = $("#message").value.trim();
    if (!message) return;
    try {
      prettyPrint(echoOut, "Loading...");
      const data = await getJSON("/api/echo", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ message }),
      });
      prettyPrint(echoOut, data);
    } catch (err) {
      prettyPrint(echoOut, String(err));
    }
  });
});


