# PasswordMe — Quick Start

**Includes**
- `dist/PasswordMe.app` — macOS app bundle  
- `dist/PasswordMe.exe` — Windows executable

---

## macOS (from repo root)
- Double‑click `dist/PasswordMe.app`.  
- If blocked: Control‑click → **Open** → **Open** to allow it.  
- Terminal:
  - Open: `open dist/PasswordMe.app`
  - Remove quarantine (if needed): `xattr -d com.apple.quarantine dist/PasswordMe.app`
  - Run binary for runtime output: `dist/PasswordMe.app/Contents/MacOS/PasswordMe`

> ⚠️ Notarization: Gatekeeper may warn because it is not notarized.

---

## Windows (from repo root)
- Double‑click `dist\PasswordMe.exe`.  
- If SmartScreen warns: **More info** → **Run anyway**.  
- Command line:
  - PowerShell: `cd .\dist\; .\PasswordMe.exe`
  - CMD: `cd dist && PasswordMe.exe`
- If blocked: Right‑click → **Properties** → check **Unblock** (if present).

---

## Optional: Verify checksum
- macOS / Linux: `shasum -a 256 dist/PasswordMe.exe`
- PowerShell: `Get-FileHash .\dist\PasswordMe.exe -Algorithm SHA256`

---

**Notes:** Built with PyInstaller; OS security prompts are expected. Use at your own risk—allow only if you trust the source.