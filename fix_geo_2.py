import re

def fix_om_sajten():
    path = "/data/workspace/projects/proptech-guide-se/static/om-sajten.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 3 siffror
    siffror = """
    <div class="grid grid-cols-3 gap-4 mb-8">
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm text-center">
            <div class="text-3xl font-extrabold text-sky-600 mb-1">117</div>
            <div class="text-xs text-slate-500 uppercase tracking-wide font-bold">Listade bolag</div>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm text-center">
            <div class="text-3xl font-extrabold text-sky-600 mb-1">100 %</div>
            <div class="text-xs text-slate-500 uppercase tracking-wide font-bold">Oberoende</div>
        </div>
        <div class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm text-center">
            <div class="text-3xl font-extrabold text-sky-600 mb-1">0 kr</div>
            <div class="text-xs text-slate-500 uppercase tracking-wide font-bold">För besökare</div>
        </div>
    </div>
    """

    if '<div class="prose prose-slate max-w-none">' in html:
        html = html.replace('<div class="prose prose-slate max-w-none">', siffror + '\n<div class="prose prose-slate max-w-none">')

    # FAQ schema
    schema = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [{
        "@type": "Question",
        "name": "Är Proptechguiden gratis att använda?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Ja, Proptechguiden är 100 % gratis för besökare och fastighetsägare att använda."
        }
      }, {
        "@type": "Question",
        "name": "Hur många proptech-bolag finns listade?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Vi har i dagsläget över 110 (117) svenska proptech-bolag listade i vår oberoende katalog."
        }
      }]
    }
    </script>
    """
    if '</head>' in html:
        html = html.replace('</head>', schema + '\n</head>')

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Fixat om-sajten.html")

if __name__ == "__main__":
    fix_om_sajten()
