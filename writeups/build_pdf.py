# Builds a writeup's PDF from its Markdown, e.g.  python3 writeups/build_pdf.py writeups/01-camouflage-and-moods.md
# Needs the markdown package (pip install markdown) and Chrome or Chromium, which prints the page to PDF
# (set CHROME to its path if it isn't found).
import os
import shutil
import subprocess
import sys
import markdown

CSS = """
@page { size: A4; margin: 18mm 20mm; }
body { font-family: "DejaVu Serif", Georgia, serif; font-size: 10.5pt; line-height: 1.5; color: #0b0b0b; }
h1, h2, h3 { font-family: "DejaVu Sans", "Helvetica Neue", Arial, sans-serif; line-height: 1.25; break-after: avoid; }
h1 { font-size: 21pt; margin: 0 0 2pt; }
h2 { font-size: 13.5pt; margin: 20pt 0 6pt; }
h3 { font-size: 11pt; margin: 14pt 0 4pt; }
p, li { orphans: 3; widows: 3; }
em { color: #52514e; }
a { color: #1c5cab; text-decoration: none; }
table { border-collapse: collapse; font-family: "DejaVu Sans", Arial, sans-serif; font-size: 8.8pt; margin: 10pt 0 4pt; break-inside: avoid; }
th, td { border-bottom: 1px solid #e1e0d9; padding: 3pt 9pt 3pt 0; text-align: left; font-variant-numeric: tabular-nums; vertical-align: top; }
th { border-bottom: 1.2px solid #52514e; font-weight: bold; }
code { font-family: "DejaVu Sans Mono", Menlo, monospace; font-size: 0.86em; background: #f3f2ee; padding: 0 2pt; border-radius: 2pt; }
img { display: block; width: 86%; margin: 10pt auto 2pt; }
p:has(> img) { break-inside: avoid; break-after: avoid; } /* (keeps each figure with its caption) */
blockquote { border-left: 3px solid #e1e0d9; margin: 10pt 0; padding: 1pt 12pt; color: #52514e; }
hr { border: none; border-top: 1px solid #e1e0d9; margin: 16pt 0; }
"""

def find_chrome():
    candidates = [os.environ.get("CHROME"), "chromium", "chromium-browser", "google-chrome", "google-chrome-stable",
                  "/opt/pw-browsers/chromium", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  "/Applications/Chromium.app/Contents/MacOS/Chromium"]
    for candidate in candidates:
        if candidate and shutil.which(candidate): return shutil.which(candidate)
        if candidate and os.path.exists(candidate): return candidate
    sys.exit("couldn't find Chrome or Chromium; set CHROME to its path")

def build(md_path):
    md_path = os.path.abspath(md_path)
    with open(md_path, encoding = "utf-8") as f:
        body = markdown.markdown(f.read(), extensions = ["tables", "fenced_code"])
    title = os.path.splitext(os.path.basename(md_path))[0]
    page = f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"
    html_path = os.path.splitext(md_path)[0] + ".tmp.html" # next to the Markdown, so its image paths still work
    pdf_path = os.path.splitext(md_path)[0] + ".pdf"
    with open(html_path, "w", encoding = "utf-8") as f:
        f.write(page)
    try:
        subprocess.run([find_chrome(), "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf_path}", "file://" + html_path], check = True, capture_output = True, timeout = 120)
    finally:
        os.remove(html_path)
    print("wrote", pdf_path)

if __name__ == "__main__":
    for path in sys.argv[1:]:
        build(path)
