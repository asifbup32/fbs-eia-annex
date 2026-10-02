from pathlib import Path
import shutil, zipfile, re, base64, html, json
from PIL import Image, ImageOps, ImageDraw
src=Path('F:/Enivornmental Audiiting/ANNEX')
out=Path(__file__).parent/'dist'
assets=out/'assets'
assets.mkdir(exist_ok=True)
docs=[('fire','Fire Extinguisher and Fire house cabinet.docx','Fire protection equipment'),('interviews','Interview_and Questionnaire_Survey Time.docx','Interviews & questionnaire survey'),('washroom','washroom.docx','Washroom observations')]
galleries={}
for key,name,title in docs:
 shutil.copy2(src/name,assets/name)
 images=[]
 with zipfile.ZipFile(src/name) as z:
  for n in z.namelist():
   if n.startswith('word/media/'):
    dest=assets/(key+'-'+Path(n).name); dest.write_bytes(z.read(n)); images.append(dest.name)
 galleries[key]=images
shutil.copy2(src/'FBS_EIA_Survey_Analysis_Template.xlsx',assets/'FBS_EIA_Survey_Analysis_Template.xlsx')
figs=['animation_right_fire_left_stair_only_all_1680_preview.png','animation_two_stairs_all_1680_preview.png','crowd_occupancy.png','evacuation_curves.png','floor_clearance.png','sensitivity.png']
for n in figs: shutil.copy2(src/'fbs_evacuation_results'/n,assets/n)
# Externalize the original embedded animation frames without changing their pixels or timing.
animation=src/'fbs_evacuation_results/animation_right_fire_left_stair_only_all_1680.html'
t=animation.read_text(encoding='utf-8'); frame_count=0
(assets/'frames').mkdir(exist_ok=True)
def replace_frame(m):
 global frame_count
 data=re.sub(r'\\\s*','',m.group(1)); data=re.sub(r'\s+','',data)
 name=f'frames/frame-{frame_count:03d}.png'; (assets/name).write_bytes(base64.b64decode(data)); frame_count+=1
 return name
t=re.sub(r'data:image/png;base64,([A-Za-z0-9+/=\s\\]+)',replace_frame,t)
(assets/'evacuation-animation.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Right-side fire evacuation animation</title><style>body{margin:0}img{max-width:100%;height:auto}.animation{max-width:100%}</style></head><body>'+t+'</body></html>',encoding='utf-8')
shutil.copy2(src/'fbs_evacuation_results/README.txt',assets/'model-notes.txt')
def gallery(key):
 return '<div class="gallery">'+''.join(f'<a href="assets/{n}" target="_blank" rel="noopener"><img src="assets/{n}" loading="lazy" alt="{dict((a,c) for a,b,c in docs)[key]} — source photograph {i+1}"><span>Photograph {i+1:02d} · View full size</span></a>' for i,n in enumerate(galleries[key]))+'</div>'
def download(name,label): return f'<a class="download" href="assets/{html.escape(name)}" download>{label} <span>Download</span></a>'
team=[('Md. Imam Hussain','23532007020'),('Jareen Saba','23532007026'),('Shadman Sakeeb Rizvee','23532007028'),('Jefer Mahmud','23532007032'),('Md. Asif Ekbal Khan','23532007032')]
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="ENV4102 Group 4 academic annex: survey materials, field photographs and illustrative evacuation results."><title>ENV4102 | Group 4 Annex</title><link rel="stylesheet" href="style.css"></head><body>
<a class="skip" href="#main">Skip to annex</a><header><a class="brand" href="#main"><span class="mark">E / A</span><span>ENV4102<span class="brand-sub">FIELDWORK ANNEX</span></span></a><span class="header-meta">SECTION B <b>/</b> GROUP 4</span></header>
<div class="layout"><aside><p class="eyebrow">ANNEX INDEX</p><nav aria-label="Annex sections"><a href="#overview">00 <span>Overview</span></a><a href="#survey">01 <span>Survey workbook</span></a><a href="#interviews">02 <span>Interviews & survey</span></a><a href="#fire">03 <span>Fire protection</span></a><a href="#washroom">04 <span>Washroom observations</span></a><a href="#evacuation">05 <span>Evacuation analysis</span></a><a href="#submission">06 <span>Submitted by</span></a></nav><div class="aside-note">Environmental Impact Assessment and Auditing<br><strong>Session 2022–2023</strong></div></aside>
<main id="main"><section id="overview" class="overview"><p class="eyebrow">ENVIRONMENTAL IMPACT ASSESSMENT AND AUDITING</p><h1>The fieldwork<br><em>annex.</em></h1><p class="intro">Supporting materials for the FBS building assessment: survey records, site photographs and preliminary evacuation scenarios.</p><div class="facts"><div><span>COURSE CODE</span><strong>ENV4102</strong></div><div><span>CLASS & TEAM</span><strong>Section B · Group 4</strong></div><div><span>ACADEMIC SESSION</span><strong>2022–2023</strong></div></div><div class="directory"><a href="#survey"><b>01—04</b><span>Field evidence & documents</span><small>Workbook, interviews and observations</small></a><a href="#evacuation"><b>05</b><span>Evacuation scenarios</span><small>Animation and six supplied figures</small></a></div></section>
<section id="survey"><div class="section-top"><span class="number">01</span><div><p class="eyebrow">DATA & QUESTIONNAIRES</p><h2>Survey workbook</h2></div><span class="type">XLSX</span></div><p>The supplied workbook contains a Summary sheet with questionnaire items and response labels for the FBS building assessment.</p><p class="note">This version contains no response-count or percentage tables. Download the workbook to view its supplied questionnaire content.</p>'''+download('FBS_EIA_Survey_Analysis_Template.xlsx','FBS EIA Survey Analysis Template · XLSX')+'''</section>
<section id="interviews"><div class="section-top"><span class="number">02</span><div><p class="eyebrow">FIELD DOCUMENTATION</p><h2>Interviews & questionnaire survey</h2></div><span class="type">4 PHOTOS</span></div><p>Photographic material extracted from the supplied interview and questionnaire survey document, in source order.</p>'''+gallery('interviews')+download(docs[1][1],'Interview and Questionnaire Survey Time · DOCX')+'''</section>
<section id="fire"><div class="section-top"><span class="number">03</span><div><p class="eyebrow">SITE EQUIPMENT</p><h2>Fire protection</h2></div><span class="type">2 PHOTOS</span></div><p>The source document identifies CO₂ and ABC dry chemical extinguishers, a manual fire alarm pull station, a fire hose cabinet and a fire protection riser.</p>'''+gallery('fire')+download(docs[0][1],'Fire Extinguisher and Fire house cabinet · DOCX')+'''</section>
<section id="washroom"><div class="section-top"><span class="number">04</span><div><p class="eyebrow">SANITATION OBSERVATIONS</p><h2>Washroom conditions</h2></div><span class="type">5 PHOTOS</span></div><p>The supplied document captions identify the lower FBS washroom beside Amitie and note that hand wash was not refilled on time. Photographs are presented in source order.</p>'''+gallery('washroom')+download(docs[2][1],'Washroom observations · DOCX')+'''</section>
<section id="evacuation"><div class="section-top"><span class="number">05</span><div><p class="eyebrow">PRELIMINARY SCENARIO ANALYSIS</p><h2>Evacuation, illustrated</h2></div></div><p>A queue model of 1,680 occupants across ground level to level 13, comparing assumed stair and exit availability.</p><div class="note"><strong>Illustrative model · not field-validated</strong><br>Times begin at a common alert, not ignition. Capacities, widths, response delays and exit layout are assumed. These results do not establish actual clearance time, safety or compliance.</div>
<div class="animation-panel"><div><p class="eyebrow">INTERACTIVE ANIMATION</p><h3>Right-side fire. Left stair only.</h3><p>All 1,680 occupants remain visible as the right stair is blocked and routes are reassigned to the left. Dot positions are schematic, not pedestrian trajectories.</p><button id="load-animation">Load animation</button><a class="text-link" href="assets/evacuation-animation.html" target="_blank" rel="noopener">Open animation in a separate tab</a><small>The animation contains 120 original frames. Loading may take a moment.</small></div><img src="assets/animation_right_fire_left_stair_only_all_1680_preview.png" alt="Preview of the right-side fire evacuation scenario at 40 seconds"></div><div id="animation-host"></div>
<div class="figure-grid">'''
captions=[('animation_right_fire_left_stair_only_all_1680_preview.png','A05.1','Right stair blocked','At 40 seconds: 86 outside, 1,266 on floors, 268 in stairs and 60 in the lobby.'),('animation_two_stairs_all_1680_preview.png','A05.2','Two-stair baseline','At 35 seconds: 83 outside, 991 on floors, 546 in stairs and 60 in the lobby.'),('crowd_occupancy.png','A05.3','Crowd occupancy','Assumed stair storage reaches 546 occupants within 35 seconds in the base scenario.'),('evacuation_curves.png','A05.4','Evacuation curves','Illustrative clearance curves for two stairs, a blocked right stair and one final door; one seed per curve.'),('floor_clearance.png','A05.5','Floor-group clearance','Time until each origin floor’s last person reaches outside. Level 13: 9.46 minutes in the base scenario.'),('sensitivity.png','A05.6','Sensitivity to assumptions','Mean and min–max across five random seeds under fixed inputs; ranges are not confidence intervals.')]
for n,num,title,cap in captions:
 page+=f'<figure><a href="assets/{n}" target="_blank" rel="noopener"><img loading="lazy" src="assets/{n}" alt="{html.escape(title+": "+cap)}"></a><figcaption><span>{num}</span><h3>{title}</h3><p>{cap}</p><a href="assets/{n}" target="_blank" rel="noopener">View full figure</a></figcaption></figure>'
page+='''</div><details><summary>Model assumptions & interpretation</summary><p>The model represents finite stair storage, merging queues and a shared lobby. The fire-side overlay indicates route unavailability; it does not simulate fire, smoke, heat or tenability. Assisted evacuation and a safe/unsafe threshold are not included. Animation positions indicate compartment membership and are not to scale.</p><p>Five-seed ranges describe random variation under fixed inputs, not uncertainty in actual geometry or behaviour. Replace assumptions with site measurements before using results for planning.</p><a href="assets/model-notes.txt">Read the supplied model notes</a></details></section>
<section id="submission"><div class="section-top"><span class="number">06</span><div><p class="eyebrow">ENV4102 · SECTION B · GROUP 4</p><h2>Submitted by</h2></div></div><div class="team">'''+''.join(f'<div><span>{name}</span><strong>{sid}</strong></div>' for name,sid in team)+'''</div><p class="session">Session: 2022–2023</p></section><footer><span>ENVIRONMENTAL IMPACT ASSESSMENT AND AUDITING</span><span>Group 4 / Annex</span></footer></main></div><script src="app.js"></script></body></html>'''
(out/'index.html').write_text(page,encoding='utf-8')
# Contact sheet for checking the actual source photos.
thumbs=[]
for key,items in galleries.items():
 for n in items:
  im=ImageOps.contain(Image.open(assets/n).convert('RGB'),(260,190)); tile=Image.new('RGB',(280,225),'white');tile.paste(im,((280-im.width)//2,0));ImageDraw.Draw(tile).text((8,198),n,fill='black');thumbs.append(tile)
sheet=Image.new('RGB',(1120,225*((len(thumbs)+3)//4)), '#dddddd')
for i,tile in enumerate(thumbs): sheet.paste(tile,((i%4)*280,(i//4)*225))
sheet.save(Path(__file__).parent/'photo-review.jpg')
print(json.dumps({'frames':frame_count,'photos':sum(map(len,galleries.values())),'html_bytes':(out/'index.html').stat().st_size}))
