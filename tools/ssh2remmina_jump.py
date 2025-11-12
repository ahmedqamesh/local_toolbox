#!/usr/bin/env python3
import os, re
from pathlib import Path

ssh_config = Path.home() / ".ssh" / "config"
if not ssh_config.exists():
    raise SystemExit("❌ No ~/.ssh/config found")

remmina_dir = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")) / "remmina"
remmina_dir.mkdir(parents=True, exist_ok=True)

def write_remmina(name, host, user=None, port=None, identity=None, proxyjump=None):
    fn = re.sub(r'[^A-Za-z0-9._-]', '_', name) + ".remmina"
    fp = remmina_dir / fn
    lines = [
        "[remmina]",
        f"name={name}",
        "protocol=SSH",
        f"server={host}",
    ]
    if user: lines.append(f"username={user}")
    if port: lines.append(f"ssh_port={port}")
    if identity:
        identity = os.path.expanduser(identity)
        lines.append(f"ssh_key_file={identity}")
        lines.append(f"identityfile={identity}")
    if proxyjump:
        lines.append(f"ssh_proxycommand=ssh -W %h:%p {proxyjump}")
    lines += ["group=", "notes="]
    fp.write_text("\n".join(lines) + "\n")
    print("✅ Created", fp)

hosts, cur = [], {}
with open(ssh_config) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        key = parts[0].lower()
        val = " ".join(parts[1:])
        if key == "host":
            if cur: hosts.append(cur)
            cur = {"Host": val}
        elif cur:
            cur[key.capitalize()] = val
    if cur: hosts.append(cur)

for h in hosts:
    name = h.get("Host")
    if not name or "*" in name:
        continue
    host = h.get("Hostname", name)
    user = h.get("User")
    port = h.get("Port")
    identity = h.get("Identityfile")
    proxy = h.get("Proxyjump")
    write_remmina(name, host, user, port, identity, proxy)

print(f"\n🎉 Done. Files saved in {remmina_dir}")
print("Open Remmina → you’ll see your imported servers.")

