# -*- coding: utf-8 -*-
"""Check mission metadata XSTR ids for the mismatch that makes FSO skip a mission.

FSO logs "Skipping <mission>.fs2 due to XSTR mismatch" when a metadata XSTR
($Mission Desc / $Cargo) uses an id whose tstrings.tbl entry differs from the
mission's inline default text.

Usage:
  python tools/check_mission_xstr.py <missions_dir> <tstrings.tbl>

Exit code 0 = no fatal mismatch, 1 = at least one fatal mismatch.
Fatal = inline default is a shared placeholder ("Nothing" / "Put mission
description here") and tstrings translated it.  Other translated metadata is
reported as INFO because campaign descriptions are translated on purpose.
"""
import io, os, re, sys

PLACEHOLDERS = {'nothing', 'put mission description here'}

def parse_tbl(path):
    t = io.open(path, encoding='utf-8', errors='ignore', newline='').read()
    d = {}
    for m in re.finditer(r'(?m)^\s*(\d+)\s*,\s*"', t):
        sid = int(m.group(1))
        i = m.end(); buf = []
        while i < len(t):
            c = t[i]
            if c == '\\' and i + 1 < len(t):
                buf.append(t[i:i+2]); i += 2; continue
            if c == '"':
                break
            buf.append(c); i += 1
        d[sid] = ''.join(buf)
    return d

def norm(s):
    s = s.replace('\\r\\n', '\n').replace('\\n', '\n').replace('\\r', '\n')
    return ' '.join(s.split()).strip()

PATTERNS = [
    re.compile(r'\$Mission Desc:\s*XSTR\("((?:[^"\\]|\\.)*)"\s*,\s*(\d+)\s*\)', re.S),
    re.compile(r'\$Cargo\s*\d*:\s*XSTR\("((?:[^"\\]|\\.)*)"\s*,\s*(\d+)\s*\)', re.S),
]

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    missions, tstrings_path = sys.argv[1], sys.argv[2]
    tstrings = parse_tbl(tstrings_path)
    fatal = []
    info = []
    for root, _, files in os.walk(missions):
        for f in sorted(files):
            if not f.lower().endswith('.fs2'):
                continue
            txt = io.open(os.path.join(root, f), encoding='utf-8', errors='ignore').read()
            for pat in PATTERNS:
                for m in pat.finditer(txt):
                    sid = int(m.group(2))
                    if sid == -1 or sid not in tstrings:
                        continue
                    inline = norm(m.group(1))
                    table = norm(tstrings[sid])
                    if inline == table:
                        continue
                    item = (f, sid, inline[:50], table[:50])
                    if inline.lower() in PLACEHOLDERS:
                        fatal.append(item)
                    else:
                        info.append(item)
    print('scanned missions in %s' % missions)
    print('FATAL (shared placeholder translated): %d' % len(fatal))
    for f, sid, inline, table in fatal[:30]:
        print('  %-32s id=%-5d inline=%r table=%r' % (f, sid, inline, table))
    print('INFO (translated metadata, normally safe): %d' % len(info))
    return 1 if fatal else 0

if __name__ == '__main__':
    raise SystemExit(main())
