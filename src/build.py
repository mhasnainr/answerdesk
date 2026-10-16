import json,csv,os,html,sys
sys.path.insert(0,"data"); from vendors import V,D
BASE="https://mhasnainr.github.io/answerdesk"
PFX="/answerdesk"
GSC_TOKEN=""  # set to your Google Search Console token to emit the verification tag on the homepage
O="site"; os.makedirs(O,exist_ok=True)
json.dump(V,open("data/vendors.json","w"),indent=1)
with open("data/vendors.csv","w",newline="") as f:
  w=csv.writer(f); w.writerow(["slug","vendor","kind","plan","price_usd_month","unit","included","overage_usd","note","integrations","trades_mentioned","free_trial","affiliate","source_url","date_checked"])
  for v in V:
    for p in v["plans"]:
      w.writerow([v["slug"],v["name"],v["kind"],p["name"],p["price_usd_month"] if p["price_usd_month"] is not None else "unknown",p["unit"] or "unknown",p["included"] if p["included"] is not None else "unknown",p["overage_usd"] if p["overage_usd"] is not None else "unknown",p["note"],"; ".join(v["integrations"]),"; ".join(v["trades"]),v["free_trial"],v["affiliate"],v["url"],v["date_checked"]])
e=html.escape
CSS="body{font:16px/1.5 system-ui,sans-serif;max-width:960px;margin:auto;padding:0 16px;color:#1a1a1a}header{display:flex;gap:16px;align-items:center;padding:12px 0;border-bottom:1px solid #ddd;flex-wrap:wrap}header a{color:#0b5;text-decoration:none;font-weight:600}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #eee;padding:6px;text-align:left;font-size:14px}.card{border:1px solid #ddd;border-radius:8px;padding:16px;margin:16px 0}.btn{background:#0b5;color:#fff;padding:8px 14px;border-radius:6px;border:0;text-decoration:none}input,select{padding:6px;margin:4px}small{color:#666}footer{margin:40px 0;color:#666;font-size:13px}"
TR={"plumbing":["plumb"],"hvac":["hvac"],"dental":["dental","dentist"],"salons":["salon","spa","nail","lash","barber"],"law":["law","legal"],"roofing":["roof"],"landscaping":["landscap"],"cleaning":["cleaning"],"pest-control":["pest"],"garage-door":["garage door"],"auto-repair":["auto repair"],"property-management":["property management"],"handyman":["handyman"]}
TN={"plumbing":"Plumbers","hvac":"HVAC Companies","dental":"Dental Practices","salons":"Salons","law":"Law Firms","roofing":"Roofers","landscaping":"Landscapers","cleaning":"Cleaning Services","pest-control":"Pest Control Companies","garage-door":"Garage Door Companies","auto-repair":"Auto Repair Shops","property-management":"Property Managers","handyman":"Handymen"}
pages=[]
def page(path,title,desc,body):
  url=f"{BASE}/{path}".replace("index.html","")
  doc=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{{GSC}}<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><style>{CSS}</style></head><body><header><a href="/">AnswerDesk Index</a><a href="/calculator.html">Cost calculator</a><a href="/trades/plumbing.html">Plumbing</a><a href="/trades/hvac.html">HVAC</a><a href="/trades/dental.html">Dental</a><a href="/trades/salons.html">Salons</a><a href="/trades/law.html">Law</a><a href="/guides/">Guides</a><a href="/get-featured.html">Get featured</a></header><main>{body}</main>{NL}<footer>Prices are taken from each vendor's public pricing page and were last checked {D}. "unknown" means we could not verify it. Confirm with the vendor before you buy. Affiliate disclosure: some links on this site are affiliate links. We may earn a commission if you buy, at no extra cost to you. It never changes our prices or rankings.</footer></body></html>"""
  doc=doc.replace('{GSC}',f'<meta name="google-site-verification" content="{e(GSC_TOKEN)}">' if (GSC_TOKEN and path=='index.html') else '')
  doc=doc.replace('href="/','href="'+PFX+'/').replace("href='/","href='"+PFX+"/")
  fp=os.path.join(O,path); os.makedirs(os.path.dirname(fp),exist_ok=True); open(fp,"w").write(doc); pages.append(url)
NL='<section class="card"><h3>Get the weekly price-change email</h3><p>We email you when AI receptionist prices or plans change. Free, and you can unsubscribe anytime.</p><form action="https://app.kit.com/forms/10053970/subscriptions" method="post" data-uid="97a62db4f4"><label for="ea" style="position:absolute;left:-9999px">Email address</label><input id="ea" type="email" name="email_address" required autocomplete="email" placeholder="you@business.com"><button class="btn" type="submit">Subscribe</button></form><small>Powered by Kit. You will get a confirmation email.</small></section>'
def fmt(x): return "unknown" if x is None else (f"${x:,.2f}".replace(".00",""))
def row(v): return f'<tr><td><a href="/vendors/{v["slug"]}.html">{e(v["name"])}</a></td><td>{v["kind"]}</td><td>{fmt(v["price_from"])}</td><td>{e(", ".join(v["integrations"]))}</td><td>{e(v["free_trial"])}</td></tr>'
TH="<table><tr><th>Vendor</th><th>Type</th><th>From /mo</th><th>Integrations</th><th>Trial</th></tr>"
srt=sorted(V,key=lambda v:(v["price_from"] is None,v["price_from"] or 0))
page("index.html","AnswerDesk Index: Compare AI Receptionists & Answering Services (2026 prices)","Compare "+str(len(V))+" AI receptionists and answering services by price, trade and integrations (Jobber, ServiceTitan, Housecall Pro, Clio). Prices checked "+D+".",
 f"<h1>Compare AI receptionists by trade, price and integrations</h1><p>{len(V)} AI and human answering services. Every price links to the vendor's own pricing page. Last checked {D}.</p><p><a class='btn' href='/calculator.html'>What would it cost me?</a></p>"+TH+"".join(row(v) for v in srt)+"</table><h2>Browse by trade</h2><p>{TRL}</p><h2>Buyer guides</h2><ul>{GD}</ul><h2>Head-to-head</h2><ul>"+"{VS}"+"</ul>")
for v in V:
  pl="".join(f"<tr><td>{e(p['name'])}</td><td>{fmt(p['price_usd_month'])}</td><td>{p['included'] if p['included'] is not None else 'unknown'} {p['unit'] or ''}</td><td>{fmt(p['overage_usd'])}</td><td>{e(p['note'])}</td></tr>" for p in v["plans"])
  page(f"vendors/{v['slug']}.html",f"{v['name']} Pricing, Plans & Integrations ({D[:4]})",f"{v['name']} pricing starts at {fmt(v['price_from'])}/mo. Plans, overage, integrations and trades, checked {D}.",
   f"<h1>{e(v['name'])}: pricing and plans</h1><p>Type: {v['kind']} · Trial: {e(v['free_trial'])}</p><table><tr><th>Plan</th><th>$/mo</th><th>Included</th><th>Overage</th><th>Notes</th></tr>{pl}</table><p><b>Integrations mentioned:</b> {e(', '.join(v['integrations']))}</p><p><b>Trades mentioned on vendor site:</b> {e(', '.join(v['trades']))}</p><p>Source: <a href='{v['url']}' rel='nofollow'>{e(v['url'])}</a> (checked {v['date_checked']})</p>")
for t,keys in TR.items():
  m=[v for v in srt if any(k in x.lower() for x in v["trades"] for k in keys)]
  page(f"trades/{t}.html",f"Best AI Receptionists for {TN[t]} ({D[:4]} Prices Compared)",f"{len(m)} AI receptionists and answering services that mention {TN[t].lower()}, compared by price and integrations.",
   f"<h1>AI receptionists for {TN[t].lower()}</h1><p>{len(m)} services mention {TN[t].lower()} on their own site. We have not tested them. This list compares published facts only.</p>"+TH+"".join(row(v) for v in m)+"</table>")
VSP=[("goodcall","rosie"),("dialzara","upfirst"),("smith-ai","ruby"),("pickupbell","oncrew"),("abby-connect","ruby"),("my-ai-front-desk","goodcall")]
B={v["slug"]:v for v in V}; vs=[]
for a,b in VSP:
  A,Bv=B[a],B[b]; s=f"{a}-vs-{b}"
  def col(x): return "<td>"+ "<br>".join(f"{e(p['name'])}: {fmt(p['price_usd_month'])} ({p['included'] if p['included'] is not None else 'unknown'} {p['unit'] or ''})" for p in x["plans"])+"</td>"
  page(f"compare/{s}.html",f"{A['name']} vs {Bv['name']}: Pricing & Features ({D[:4]})",f"{A['name']} vs {Bv['name']} compared on price, included usage, overage and integrations. Checked {D}.",
   f"<h1>{e(A['name'])} vs {e(Bv['name'])}</h1><table><tr><th></th><th>{e(A['name'])}</th><th>{e(Bv['name'])}</th></tr><tr><td>From</td><td>{fmt(A['price_from'])}</td><td>{fmt(Bv['price_from'])}</td></tr><tr><td>Plans</td>{col(A)}{col(Bv)}</tr><tr><td>Integrations</td><td>{e(', '.join(A['integrations']))}</td><td>{e(', '.join(Bv['integrations']))}</td></tr><tr><td>Trial</td><td>{e(A['free_trial'])}</td><td>{e(Bv['free_trial'])}</td></tr></table><p>Want to compare at your own call volume? Try the <a href='/calculator.html'>cost calculator</a>.</p>")
  vs.append(f'<li><a href="{PFX}/compare/{s}.html">{e(A["name"])} vs {e(Bv["name"])}</a></li>')
ip=os.path.join(O,"index.html"); _s=open(ip).read(); open(ip,"w").write(_s.replace("{VS}","".join(vs)))

def mcost(v,c,m,u=0.7):
  best=None
  for p in v["plans"]:
    if not p["unit"] or p["price_usd_month"] is None: continue
    if p["unit"]=="flat": k,ok=p["price_usd_month"],1
    else:
      x={"minutes":c*m,"calls":c,"unique":-(-c*u//1),"permin":c*m}[p["unit"]]; over=max(0,x-(p["included"] or 0))
      if over>0 and p["overage_usd"] is None: k,ok=p["price_usd_month"],0
      else: k,ok=p["price_usd_month"]+over*(p["overage_usd"] or 0),1
    if best is None or (ok,-k)>(best[1],-best[0]): best=(k,ok,p["name"])
  return best
G={
 "plumbing":dict(t="Plumbers",c=150,m=3,keys=["ServiceTitan","Jobber","Housecall Pro"],why="Plumbing calls are often urgent and come in after hours. A receptionist that books jobs straight into your field-service software (ServiceTitan, Jobber, Housecall Pro) saves you calling people back.",
   faq=[("Can an AI receptionist handle emergency calls?","Several vendors say they triage urgent calls and pass them to a person. Ask each one how it routes something like a burst pipe at 2am before you sign, and test it with your own calls during the trial."),("Do I need ServiceTitan or Jobber?","No. Many tools only need Google Calendar or work by text message. Booking straight into field-service software is only possible with the vendors we list as integrating with it.")]),
 "hvac":dict(t="HVAC Companies",c=200,m=3,keys=["ServiceTitan","Jobber","Housecall Pro"],why="HVAC call volume jumps in heatwaves and cold snaps. Look at overage pricing as closely as the base price, and at whether bookings go straight into your dispatch software.",
   faq=[("What happens in a busy month?","Most plans include a set number of minutes, calls or callers and charge extra beyond that. Run your peak month through our calculator, not just an average month."),("Per-minute or per-call pricing: which is cheaper?","It depends on how long your calls are. Short calls favour per-minute plans; long calls favour per-call or per-caller plans. The calculator shows both.")]),
 "dental":dict(t="Dental Offices",c=400,m=3,keys=["Dentrix","Open Dental","HIPAA"],why="Dental offices need scheduling, recall calls and careful handling of patient data. In our checks we found few published integrations with practice-management software, so confirm with each vendor.",
   faq=[("Is it HIPAA compliant?","Some vendors mention HIPAA on their sites. A mention is not a guarantee: ask for a signed BAA (business associate agreement) before any patient data is shared."),("Will it book into Dentrix or Open Dental?","We did not find these integrations published on the pricing pages we checked. Ask the vendor directly.")]),
 "salons":dict(t="Salons & Spas",c=200,m=2,keys=["Fresha","Boulevard","Vagaro","Square","Mindbody","Zenoti"],why="Salons book on calendars that are already set up. Booking software with its own AI add-on (Fresha, Boulevard, Zenoti) or a tool that connects to your booking system means no double-booking.",
   faq=[("Should I use my booking software's built-in AI?","If your platform offers one (for example Fresha AI Concierge), it uses your real availability without any setup. Standalone tools can work across several platforms but may charge setup fees."),("Can it take deposits?","Some tools mention deposits (Jvora mentions Stripe deposits). Otherwise deposits depend on your booking system.")]),
 "law":dict(t="Law Firms",c=150,m=4,keys=["Clio","HIPAA"],why="Law firms need intake questions answered, conflict-check details captured, and calls handled professionally. Clio integration and the option of a human backup matter here.",
   faq=[("AI or human receptionist for a law firm?","Human services such as Ruby and Smith.ai's receptionists cost more per minute. AI is cheaper for routine intake. Hybrids like Abby Connect mix both on one plan."),("Does it work with Clio?","In our data, Smith.ai and Upfirst list Clio. Check the vendor's page for details.")]),
}

def FQ(sw): return [("Will it book into "+sw+"?","Only if the vendor lists that integration. Vendors that list it are shown above; for others, ask them or use calendar or text-message hand-off instead."),("Is a flat-rate or per-minute plan better?","If your calls are short and your volume is steady, a per-minute plan can cost less. If volume spikes with the seasons, a flat or unlimited plan is easier to budget. Try both in the calculator.")]
G.update({
 "roofing":dict(t="Roofers",c=150,m=4,keys=["AccuLynx","JobNimbus","ServiceTitan","Jobber"],why="Roofing calls spike after storms, and every caller wants an inspection booked fast. Look at how each plan handles surges, and whether leads land in your CRM (AccuLynx, JobNimbus).",faq=FQ("AccuLynx or JobNimbus")),
 "landscaping":dict(t="Landscapers",c=120,m=3,keys=["Jobber","Housecall Pro","LMN","Aspire"],why="Landscaping is seasonal: spring brings a wave of quote requests while crews are out in the field. A receptionist that captures property details and books estimates keeps that wave from going to voicemail.",faq=FQ("Jobber")),
 "cleaning":dict(t="Cleaning Services",c=100,m=3,keys=["Jobber","ZenMaid","Housecall Pro"],why="Cleaning businesses get booking calls while cleaners are inside clients' homes. Recurring-visit booking, reschedules and capturing property size matter most.",faq=FQ("Jobber or ZenMaid")),
 "pest-control":dict(t="Pest Control Companies",c=150,m=3,keys=["GorillaDesk","PestPac","FieldRoutes","ServiceTitan"],why="Pest control mixes urgent calls (wasps, rodents) with recurring service plans. Triage and booking into your routing software are the key features.",faq=FQ("GorillaDesk, PestPac or FieldRoutes")),
 "garage-door":dict(t="Garage Door Companies",c=150,m=3,keys=["ServiceTitan","Jobber","Housecall Pro"],why="A broken spring is an urgent, high-value call. A receptionist that triages the problem and books a same-day truck matters more than extra features.",faq=FQ("ServiceTitan, Jobber or Housecall Pro")),
 "auto-repair":dict(t="Auto Repair Shops",c=300,m=3,keys=["Shopmonkey","Tekmetric","Mitchell 1"],why="Shops field constant 'is my car ready?' and quote calls while techs are in the bay. Integration with shop management software (Shopmonkey, Tekmetric) is rare, so check it carefully.",faq=FQ("Shopmonkey or Tekmetric")),
 "property-management":dict(t="Property Managers",c=300,m=3,keys=["AppFolio","Buildium","Yardi","Rent Manager"],why="Property managers handle tenant maintenance requests, after-hours emergencies and leasing enquiries. Emergency routing and logging requests into AppFolio or Buildium matter most.",faq=FQ("AppFolio or Buildium")),
 "handyman":dict(t="Handymen",c=80,m=4,keys=["Jobber","Housecall Pro","Google Calendar","Calendly"],why="Handyman calls come with a list of small jobs. A receptionist that captures the whole list, quotes only your set rates and books a long enough visit saves you call-backs from the ladder.",faq=FQ("Jobber")),
})
SL={"roofing":"roofers","landscaping":"landscapers","cleaning":"cleaning-services","pest-control":"pest-control","garage-door":"garage-door-companies","auto-repair":"auto-repair-shops","property-management":"property-managers","handyman":"handymen"}
gd=[]
for t,g in G.items():
  keys=TR[t]; m=[v for v in V if any(k in x.lower() for x in v["trades"] for k in keys)]
  costed=[(mcost(v,g["c"],g["m"]),v) for v in m]; okc=sorted([(c[0],v,c[2]) for c,v in costed if c and c[1]],key=lambda z:z[0])
  integ=[v for v in m if any(k.lower() in " ".join(v["integrations"]).lower() for k in g["keys"])]
  picks=[]
  if okc: picks.append(("Lowest estimated cost at this volume",okc[0][1],f"{fmt(round(okc[0][0],2))}/mo on {okc[0][2]}"))
  for v in integ[:2]: picks.append(("Integrates with "+", ".join(k for k in g["keys"] if k.lower() in " ".join(v["integrations"]).lower()),v,f"from {fmt(v['price_from'])}/mo"))
  fr=[v for v in m if v["price_from"]==0 or "free" in v["free_trial"].lower()]
  if fr: picks.append(("Free plan or free trial to test",fr[0],e(fr[0]["free_trial"])))
  qp="".join(f"<tr><td>{e(a)}</td><td><a href='/vendors/{v['slug']}.html'>{e(v['name'])}</a></td><td>{b}</td></tr>" for a,v,b in picks)
  ct="".join(f"<tr><td><a href='/vendors/{v['slug']}.html'>{e(v['name'])}</a></td><td>{v['kind']}</td><td>{e(p)}</td><td>${k:,.2f}</td></tr>" for k,v,p in okc[:10])
  unk=[v for c,v in costed if not c or not c[1]]
  it="".join(f"<li><a href='/vendors/{v['slug']}.html'>{e(v['name'])}</a>: {e(', '.join(v['integrations']))}</li>" for v in integ) or "<li>None of the vendors we checked list these integrations on their public pages.</li>"
  fq="".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q,a in g["faq"]+[("How current are these prices?",f"We read each vendor's public pricing page on {D}. Prices change, so confirm with the vendor before you buy.")])
  body=f"""<h1>Best AI receptionist for {g['t'].lower()} ({D[:4]})</h1><p>{e(g['why'])}</p>
<h2>Quick picks</h2><table><tr><th>Best for</th><th>Vendor</th><th>Why</th></tr>{qp}</table>
<h2>How we chose</h2><p>We include vendors whose own websites mention {g['t'].lower()} or a closely related trade. We rank them only by published facts: price, what's included, overage and listed integrations. We have not tested these services and we don't use reviews. Sponsored placements, if we ever add them, will be labelled and won't change this order.</p>
<h2>What it costs at a typical volume</h2><p>Assumption: <b>{g['c']} calls a month, averaging {g['m']} minutes each</b> (70% unique callers). Change the numbers in the <a href="/calculator.html">cost calculator</a>.</p><table><tr><th>Vendor</th><th>Type</th><th>Cheapest plan</th><th>Est. $/mo</th></tr>{ct}</table>
<p><small>Excludes one-time setup fees. Not costed because pricing or overage isn't published: {e(', '.join(v['name'] for v in unk)) or 'none'}.</small></p>
<h2>Key integrations: {e(', '.join(g['keys']))}</h2><ul>{it}</ul>
<h2>FAQ</h2>{fq}
<h2>Related</h2><ul><li><a href="/trades/{t}.html">All {g['t'].lower()} vendors</a></li><li><a href="/calculator.html">Cost calculator</a></li><li><a href="/guides/">All guides</a></li></ul>"""
  slug=f"best-ai-receptionist-for-{ {'plumbing':'plumbers','hvac':'hvac','dental':'dental-offices','salons':'salons','law':'law-firms',**SL}[t] }"
  page(f"guides/{slug}.html",f"Best AI Receptionist for {g['t']} ({D[:4]}): Prices & Picks",f"Compare AI receptionists for {g['t'].lower()}: quick picks, estimated cost at {g['c']} calls/month, integrations and FAQ. Prices checked {D}.",body)
  gd.append(f'<li><a href="{PFX}/guides/{slug}.html">Best AI receptionist for {e(g["t"].lower())}</a></li>')
page("guides/index.html","AI Receptionist Buyer Guides by Trade","Guides to choosing an AI receptionist for plumbers, HVAC, dental offices, salons and law firms.","<h1>Buyer guides</h1><ul>"+"".join(x.replace(PFX,"") for x in gd)+"</ul>")
_s=open(os.path.join(O,"index.html")).read(); open(os.path.join(O,"index.html"),"w").write(_s.replace("{GD}","".join(gd)).replace("{TRL}"," · ".join(f'<a href="{PFX}/trades/{t}.html">{e(TN[t])}</a>' for t in TR)))
page("trades/index.html","AI Receptionists by Trade","Browse AI receptionists and answering services by trade.","<h1>Browse by trade</h1><ul>"+"".join(f"<li><a href='/trades/{t}.html'>{e(TN[t])}</a></li>" for t in TR)+"</ul>")
calc=[dict(n=v["name"],s=v["slug"],k=v["kind"],p=[p for p in v["plans"] if p["unit"] and p["price_usd_month"] is not None]) for v in V]
calc=[c for c in calc if c["p"]]
page("calculator.html","AI Receptionist Cost Calculator: Price at Your Call Volume","Enter your monthly calls and average call length to see what each AI receptionist and answering service would cost.",
 """<h1>What would an AI receptionist cost you?</h1><p>Calls per month <input id=c type=number value=150 min=0> Average minutes per call <input id=m type=number value=3 step=0.5> Unique callers % <input id=u type=number value=70> <label><input id=d type=checkbox> Include developer platforms</label></p><p><small>We pick the cheapest published plan for each vendor. "Overage unknown" means the vendor does not publish an extra-usage rate, so the real cost could be higher. Developer platforms show the platform per-minute rate only.</small></p><table id=t></table><script>const D="""+json.dumps(calc)+""";
function cost(p,c,m,u){const x={minutes:c*m,calls:c,unique:Math.ceil(c*u/100),permin:c*m}[p.unit];if(p.unit=='flat')return[p.price_usd_month,1];const over=Math.max(0,x-(p.included||0));if(over>0&&p.overage_usd==null)return[p.price_usd_month,0];return[p.price_usd_month+over*(p.overage_usd||0),1]}
function run(){const c=+document.getElementById('c').value,m=+document.getElementById('m').value,u=+document.getElementById('u').value;const dev=document.getElementById('d').checked;let r=D.filter(v=>dev||v.k!='developer').map(v=>{let b=null;for(const p of v.p){const[k,ok]=cost(p,c,m,u);if(!b||(ok>=b.ok&&k<b.cost)||(ok>b.ok))b={cost:k,ok,p:p.name}}return{...v,...b}}).sort((a,b)=>(b.ok-a.ok)||(a.cost-b.cost));
document.getElementById('t').innerHTML='<tr><th>Vendor</th><th>Best plan</th><th>Est. $/mo</th></tr>'+r.map(v=>`<tr><td><a href="/vendors/${v.s}.html">${v.n}</a> <small>${v.k}</small></td><td>${v.p}</td><td>$${v.cost.toFixed(2)}${v.ok?'':' + overage unknown'}</td></tr>`).join('')}
['c','m','u','d'].forEach(i=>document.getElementById(i).oninput=run);run()</script>""")
page("get-featured.html","Get Featured on AnswerDesk Index","List or feature your AI receptionist or answering service in front of small business owners comparing options by trade.",
 "<h1>Get featured</h1><p>Basic listings are free and based on facts. We check prices on your public pricing page. A featured listing adds a clearly labelled top spot on the trade pages you choose, plus a mention in the newsletter.</p><div class=card><h3>Featured listing: pricing coming soon</h3><p>Paid spots are always marked <b>Sponsored</b>. They never change the facts or the calculator results.</p><p>Contact: <i>(email not set up yet)</i></p></div>")
page("about.html","About AnswerDesk Index & Methodology","How we collect and check AI receptionist pricing.",f"<h1>Methodology</h1><p>We read each vendor's public pricing page. We list only what is published there, mark anything else as unknown, and record the date we checked. Last full check: {D}.</p><p>Download the dataset: <a href='/data/vendors.csv'>CSV</a> · <a href='/data/vendors.json'>JSON</a></p>")
os.makedirs(O+"/data",exist_ok=True); import shutil
for f in ["vendors.csv","vendors.json"]: shutil.copy("data/"+f,O+"/data/"+f)
open(O+"/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{u}</loc><lastmod>{D}</lastmod></url>" for u in pages)+"</urlset>")
open(O+"/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
print(len(V),"vendors",len(pages),"pages")
