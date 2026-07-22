import re, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
counts = {"dash": 0, "old_img": 0}

for f in glob.glob(os.path.join(ROOT, "blog_dev", "*", "en.mdx")) + \
         glob.glob(os.path.join(ROOT, "blog_dev", "*", "vi.mdx")) + \
         glob.glob(os.path.join(ROOT, "blog_dev", "*", "jp.mdx")):
  with open(f) as fh:
    t = fh.read()
  orig = t

  # Fix 1: broken closer ]--- → ]\n---
  t2 = re.sub(r'\]\s*---\s*(?=\n)', ']\n---', t)
  if t2 != t:
    counts["dash"] += 1
    t = t2

  # Fix 2: remove old inline <Image ... /> components that use stale imgbed URLs
  t2 = re.sub(
    r'\n<Image\s+src="https://imgbed\.locionic\.com/file/[^"]+\.jpg"'
    r'\s+alt="[^"]*"\s+width=\{1200\}\s+height=\{675\}'
    r'\s+className="[^"]*"\s*/>\n?',
    '', t
  )
  if t2 != t:
    counts["old_img"] += 1
    t = t2

  if t != orig:
    with open(f, 'w') as fh:
      fh.write(t)

print("Fixed:", counts)
