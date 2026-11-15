"""Build the "GitHub activity" card for the profile README, in the same style as the rest of the page.

Reads public data for one user and writes profile/activity.svg and profile/activity-dark.svg:
  commits (search API), pull requests and merge rate (search API), languages of owned public repositories,
  and the contribution calendar with a snake moving across it (SMIL, so it animates in every browser).

Environment: GITHUB_TOKEN (required for the contribution calendar and languages), LOGIN (default: repo owner).
Run locally without a token with --demo to render sample data.
"""
import base64
import json
import os
import sys
import urllib.request

LOGIN = os.environ.get("LOGIN", "17tuanphamanh")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

W, TOP = 952, 44
CELL, GAP = 14, 3
PITCH = CELL + GAP
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

THEMES = {
    "light": dict(card="#FFFFFF", line="#E4E6EE", line_op=1, ink="#1C2033", ink2="#4A5068", ink3="#646B82", acc="#5654D4",
                  track="#ECEEF4", ramp=["#ECEEF4", "#D4D3F8", "#A9A7F0", "#6F6CE0", "#3F3CB8"], snake="#0E8C82", head="#0B5E57",
                  shadow=("#1C2033", 0.07),
                  langs={"Python": "#3776AB", "TypeScript": "#3178C6", "Java": "#C7591A", "JavaScript": "#C9A227",
                         "HTML": "#E34C26", "CSS": "#663399", "Other": "#9AA0B4"}),
    "dark": dict(card="#1A1D2B", line="#FFFFFF", line_op=0.08, ink="#ECEEF5", ink2="#B7BCCE", ink3="#959CB2", acc="#9496F5",
                 track="#262A3A", ramp=["#1F2333", "#2C2F6E", "#4547B8", "#7577E8", "#B4B5FA"], snake="#4CC4B7", head="#FFFFFF",
                 shadow=("#000000", 0.35),
                 langs={"Python": "#5B9BD5", "TypeScript": "#5A8EE0", "Java": "#F08A4B", "JavaScript": "#E6CC5A",
                        "HTML": "#F07A5A", "CSS": "#9A7BD0", "Other": "#6B7187"}),
}

# advance widths in em for the two fonts whose text length decides the layout
ADV = {"sg600":{" ":0.255,"!":0.287,"\"":0.492,"#":0.634,"$":0.608,"%":0.761,"&":0.594,"'":0.284,"(":0.393,")":0.387,"*":0.535,"+":0.62,",":0.284,"-":0.438,".":0.287,"/":0.384,"0":0.646,"1":0.444,"2":0.596,"3":0.607,"4":0.633,"5":0.6,"6":0.617,"7":0.556,"8":0.606,"9":0.617,":":0.287,";":0.287,"<":0.62,"=":0.62,">":0.62,"?":0.579,"@":1.017,"A":0.633,"B":0.663,"C":0.643,"D":0.665,"E":0.556,"F":0.535,"G":0.661,"H":0.656,"I":0.259,"J":0.606,"K":0.622,"L":0.543,"M":0.878,"N":0.668,"O":0.674,"P":0.603,"Q":0.674,"R":0.632,"S":0.608,"T":0.588,"U":0.671,"V":0.618,"W":0.892,"X":0.642,"Y":0.621,"Z":0.576,"[":0.352,"\\":0.384,"]":0.352,"^":0.62,"_":0.62,"`":0.292,"a":0.577,"b":0.639,"c":0.589,"d":0.639,"e":0.581,"f":0.437,"g":0.639,"h":0.615,"i":0.261,"j":0.263,"k":0.558,"l":0.261,"m":0.855,"n":0.615,"o":0.613,"p":0.639,"q":0.639,"r":0.391,"s":0.525,"t":0.457,"u":0.615,"v":0.546,"w":0.788,"x":0.592,"y":0.615,"z":0.519,"{":0.458,"|":0.253,"}":0.458,"~":0.62,"·":0.21,"–":0.59,"—":0.894,"’":0.284},"inter400":{" ":0.2812,"!":0.2876,"\"":0.4658,"#":0.6333,"$":0.6416,"%":0.9819,"&":0.644,"'":0.2998,"(":0.3647,")":0.3647,"*":0.501,"+":0.6616,",":0.2881,"-":0.46,".":0.2881,"/":0.3604,"0":0.6309,"1":0.4067,"2":0.6099,"3":0.6177,"4":0.646,"5":0.5933,"6":0.6201,"7":0.5659,"8":0.6187,"9":0.6201,":":0.2881,";":0.3018,"<":0.6616,"=":0.6616,">":0.6616,"?":0.5112,"@":0.9658,"A":0.6899,"B":0.6543,"C":0.7305,"D":0.7217,"E":0.6011,"F":0.5903,"G":0.7461,"H":0.7432,"I":0.2686,"J":0.5708,"K":0.6719,"L":0.5654,"M":0.9033,"N":0.7534,"O":0.7646,"P":0.6387,"Q":0.7646,"R":0.6436,"S":0.6416,"T":0.6455,"U":0.7441,"V":0.6899,"W":0.9854,"X":0.6821,"Y":0.6787,"Z":0.6289,"[":0.3647,"\\":0.3604,"]":0.3647,"^":0.4712,"_":0.4561,"`":0.3228,"a":0.5615,"b":0.6123,"c":0.5713,"d":0.6123,"e":0.583,"f":0.3701,"g":0.6133,"h":0.5913,"i":0.2422,"j":0.2422,"k":0.5488,"l":0.2422,"m":0.876,"n":0.5908,"o":0.5996,"p":0.6123,"q":0.6123,"r":0.3765,"s":0.5278,"t":0.3271,"u":0.5913,"v":0.562,"w":0.8184,"x":0.5459,"y":0.562,"z":0.5522,"{":0.4263,"|":0.3325,"}":0.4263,"~":0.6616,"·":0.2881,"–":0.5,"—":1.0,"’":0.2607}}


def text_w(s, font, size, spacing=0.0):
    a = ADV[font]
    return sum(a.get(c, 0.6) for c in s) * size + spacing * size * len(s)


# ---------------------------------------------------------------- data

def api(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": LOGIN,
                                          **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def search_count(kind, q):
    return api(f"https://api.github.com/search/{kind}?q={urllib.parse.quote(q)}&per_page=1")["total_count"]


QUERY = """query($login: String!) { user(login: $login) {
  contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { contributionLevel weekday } } } }
  repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
    nodes { languages(first: 20) { edges { size node { name } } } } } } }"""


def fetch():
    commits = search_count("commits", f"author:{LOGIN}")
    prs = search_count("issues", f"author:{LOGIN} type:pr")
    merged = search_count("issues", f"author:{LOGIN} type:pr is:merged")
    user = api("https://api.github.com/graphql", {"query": QUERY, "variables": {"login": LOGIN}})["data"]["user"]
    weeks = [[(LEVEL[d["contributionLevel"]], d["weekday"]) for d in w["contributionDays"]]
             for w in user["contributionsCollection"]["contributionCalendar"]["weeks"]]
    sizes = {}
    for repo in user["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            name = "Python" if e["node"]["name"] == "Jupyter Notebook" else e["node"]["name"]
            sizes[name] = sizes.get(name, 0) + e["size"]
    return dict(commits=commits, prs=prs, merged=merged, weeks=weeks, langs=shares(sizes),
                year=user["contributionsCollection"]["contributionCalendar"]["totalContributions"])


def shares(sizes):
    total = sum(sizes.values()) or 1
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:3]
    pct = [(k, round(v * 100 / total)) for k, v in top]
    other = 100 - sum(p for _, p in pct)
    return pct + ([("Other", other)] if other > 0 else [])


def demo():
    import random
    random.seed(7)
    weeks = [[(random.choice([0, 0, 1, 1, 2, 3, 4]), d) for d in range(7)] for _ in range(53)]
    return dict(commits=920, prs=43, merged=39, weeks=weeks, langs=[("Python", 71), ("TypeScript", 14), ("Java", 11), ("Other", 4)], year=0)


# ---------------------------------------------------------------- drawing

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def font_face():
    out = []
    for fam, f in (("SG", "sg600"), ("IN", "inter400"), ("JB", "jbm400")):
        data = base64.b64encode(open(os.path.join(ROOT, "assets", "fonts", f + ".woff2"), "rb").read()).decode()
        out.append(f'@font-face{{font-family:"{fam}";src:url(data:font/woff2;base64,{data}) format("woff2")}}')
    return "".join(out)


def snake_path(cols):
    c = CELL / 2
    xs, xe = c, (cols - 1) * PITCH + c
    d = f"M{xs} {c}"
    for r in range(7):
        y = r * PITCH + c
        if r:
            d += f" V{y}"
        d += f" H{xe if r % 2 == 0 else xs}"
    return d


def render(data, theme):
    P = THEMES[theme]
    y = lambda v: v + TOP
    rate = round(data["merged"] * 100 / data["prs"]) if data["prs"] else 0
    stats = [(f'{data["commits"]:,}', "", "public commits"), (str(data["merged"]), "", "pull requests merged"), (str(rate), "%", "pull request merge rate")]
    s = []
    # header
    s.append(f'<text x="0" y="{y(11)}" class="k">ACTIVITY</text>')
    s.append(f'<text x="0" y="{y(53)}" class="t">GitHub activity</text>')
    s.append(f'<text x="0" y="{y(85.4)}" class="p">Public contribution data, refreshed daily by a GitHub Action.</text>')
    # card
    ct, ch = y(117.4), 335
    s.append(f'<rect x="0.5" y="{ct + 0.5}" width="{W - 1}" height="{ch - 1}" rx="22" fill="{P["card"]}" stroke="{P["line"]}" '
             f'stroke-opacity="{P["line_op"]}" filter="url(#sh)"/>')
    # counters
    x = 33
    for i, (num, suffix, label) in enumerate(stats):
        nw = text_w(num + suffix, "sg600", 50, -0.03)
        lw = text_w(label, "inter400", 14)
        d = 0.2 + i * 0.15
        s.append(f'<g opacity="0" transform="translate(0 14)"><animate attributeName="opacity" values="0;1" dur="0.9s" begin="{d:.2f}s" fill="freeze"/>'
                 f'<animateTransform attributeName="transform" type="translate" values="0 14;0 0" dur="0.9s" begin="{d:.2f}s" fill="freeze" '
                 f'calcMode="spline" keyTimes="0;1" keySplines=".2 .7 .2 1"/>'
                 f'<text x="{x}" y="{y(213.4)}" class="n">{esc(num)}{esc(suffix)}</text>'
                 f'<text x="{x}" y="{y(241.4)}" class="l">{esc(label)}</text></g>')
        x += max(nw, lw) + 52
    # languages
    for i, (name, pct) in enumerate(data["langs"][:4]):
        dy = i * 26
        col = P["langs"].get(name, P["langs"]["Other"])
        s.append(f'<text x="579" y="{y(163.4 + dy)}" class="b">{esc(name)}</text>')
        s.append(f'<rect x="687" y="{y(154.4 + dy)}" width="182" height="8" rx="4" fill="{P["track"]}"/>')
        bw = max(8, 182 * pct / 100)
        s.append(f'<rect x="687" y="{y(154.4 + dy)}" width="0" height="8" rx="4" fill="{col}">'
                 f'<animate attributeName="width" values="0;{bw:.1f}" dur="1.8s" begin="{0.4 + i * 0.15:.2f}s" fill="freeze" '
                 f'calcMode="spline" keyTimes="0;1" keySplines=".2 .7 .2 1"/></rect>')
        s.append(f'<text x="919" y="{y(163.4 + dy)}" class="b3" text-anchor="end">{pct}%</text>')
    s.append(f'<line x1="33" x2="919" y1="{y(274.4) + 0.5}" y2="{y(274.4) + 0.5}" stroke="{P["line"]}" stroke-opacity="{P["line_op"]}"/>')
    # contribution grid + snake
    weeks = data["weeks"][-53:]
    cols = len(weeks)
    gw = cols * PITCH - GAP
    gx, gy = (W - gw) / 2, y(303.4)
    cells = []
    for wi, week in enumerate(weeks):
        for level, day in week:
            cells.append(f'<rect x="{wi * PITCH}" y="{day * PITCH}" width="{CELL}" height="{CELL}" rx="3" fill="{P["ramp"][level]}"/>')
    path = snake_path(cols)
    segs = []
    n = 9
    for i in range(n):
        col = P["head"] if i == 0 else P["snake"]
        segs.append(f'<rect x="-6" y="-6" width="12" height="12" rx="4" fill="{col}" opacity="{1 - i * 0.07:.2f}">'
                    f'<animateMotion dur="26s" repeatCount="indefinite" begin="{-((n - i) * 0.09 + 2):.2f}s" path="{path}"/></rect>')
    s.append(f'<g transform="translate({gx:.2f} {gy:.2f})">{"".join(cells)}{"".join(segs)}</g>')
    height = y(452.4) + 48
    css = (font_face() +
           f'.k{{font:400 12px "JB",monospace;letter-spacing:.96px;fill:{P["acc"]}}}'
           f'.t{{font:600 34px "SG",sans-serif;letter-spacing:-.68px;fill:{P["ink"]}}}'
           f'.p{{font:400 16px "IN",sans-serif;fill:{P["ink2"]}}}'
           f'.n{{font:600 50px "SG",sans-serif;letter-spacing:-1.5px;fill:{P["ink"]}}}'
           f'.l{{font:400 14px "IN",sans-serif;fill:{P["ink3"]}}}'
           f'.b{{font:400 13.5px "IN",sans-serif;fill:{P["ink2"]}}}'
           f'.b3{{font:400 13.5px "IN",sans-serif;fill:{P["ink3"]}}}'
'')
    shadow = (f'<filter id="sh" x="-5%" y="-5%" width="110%" height="120%"><feDropShadow dx="0" dy="12" stdDeviation="14" '
              f'flood-color="{P["shadow"][0]}" flood-opacity="{P["shadow"][1]}"/></filter>')
    label = (f'GitHub activity for {LOGIN}: {stats[0][0]} public commits, {stats[1][0]} pull requests merged, '
             f'{rate}% merge rate, and the contribution calendar for the last year.')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height:.0f}" viewBox="0 0 {W} {height:.1f}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title><style>{css}</style><defs>{shadow}</defs>{"".join(s)}</svg>')


def main():
    data = demo() if "--demo" in sys.argv else fetch()
    os.makedirs(os.path.join(ROOT, "profile"), exist_ok=True)
    for theme, name in (("light", "activity.svg"), ("dark", "activity-dark.svg")):
        with open(os.path.join(ROOT, "profile", name), "w") as f:
            f.write(render(data, theme))
    print(json.dumps({k: v for k, v in data.items() if k != "weeks"}))


if __name__ == "__main__":
    import urllib.parse  # noqa: E402  (used by search_count)
    main()
