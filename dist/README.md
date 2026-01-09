# PasswordMe — Quick Start

**Includes**
- `dist/PasswordMe.app` — macOS app bundle  
- `dist/Dmg_version/PasswordMe.dmg` — macOS installer DMG (RECOMMENDED)
- `dist/PasswordMe.exe` — Windows executable

---

## macOS (from repo root)
- From the app bundle: Double‑click `dist/PasswordMe.app`.  
  - If blocked: Control‑click → **Open** → **Open** to allow it.  
- Terminal:
  - Open: `open dist/PasswordMe.app`
  - Remove quarantine (if needed): `xattr -d com.apple.quarantine dist/PasswordMe.app`
  - Run binary for runtime output: `dist/PasswordMe.app/Contents/MacOS/PasswordMe`

### macOS (DMG installer)
- The macOS installer is located at `dist/Dmg_version/PasswordMe.dmg`.
- Double‑click the `.dmg` to mount it, then drag `PasswordMe.app` to `/Applications` (or follow the on-screen installer).
- On first run, macOS may prompt you to enter your password to grant PasswordMe access to the Keychain — enter your password to allow the app to access the Keychain when prompted.

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
- macOS / Linux: `shasum -a 256 dist/Dmg_version/PasswordMe.dmg`
- PowerShell: `Get-FileHash .\dist\PasswordMe.exe -Algorithm SHA256`

---

**Notes:** Built with PyInstaller; OS security prompts are expected. Use at your own risk—allow only if you trust the source.
