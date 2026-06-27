// MALICIOUS FIXTURE, do not use. Proves source_scanner + behaviour_scanner.
// Expected findings: eval, obfuscation, document.cookie, atob.
export function mount(el) {
  const payload = atob("YWxlcnQoMSk=");
  // dynamic code execution
  eval(payload);
  // obfuscated marker
  const x = "\x68\x65\x6c\x6c\x6f\x77\x6f\x72\x6c\x64";
  // exfiltrates cookies
  const c = document.cookie;
  el.dataset.x = x + c;
}
