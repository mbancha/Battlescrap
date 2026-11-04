"""Current kit from verified sheet data and approved visuals; no legacy builder."""
from pathlib import Path
import json, re, hashlib, io
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader, PdfWriter
import pypdfium2 as pdfium

ROOT=Path(__file__).resolve().parent
GAME=ROOT.parent
OUT=ROOT/'current'
ASSETS=GAME/'assets'
PRINT=ASSETS/'print'
ICONS=PRINT/'icons'
OUT.mkdir(exist_ok=True)
for n,f in [('Body','georgia.ttf'),('Title','georgiab.ttf'),('Sans','arial.ttf')]:
    pdfmetrics.registerFont(TTFont(n,'C:/Windows/Fonts/'+f))
INK='#303c39'; LINE='#69736b'; GOLD='#af8950'
FILES=[]; PLACEMENTS=[]; IMAGE_CACHE={}
SOURCE=json.loads((ROOT/'source-snapshot.json').read_text(encoding='utf8'))
def rows(name):
    data=SOURCE['sheets'][name]
    return [dict(zip(data[0],r)) for r in data[1:]]
HEROES=sorted([h for h in rows('Heroes') if h['Availability']=='Starter'],key=lambda h:(h['Starter side'],h['ID']))
CONFIG=(GAME/'src/data/config.ts').read_text(encoding='utf-8-sig')
QUEUE={str(n):json.loads(re.search(r'queue'+str(n)+r':(\[.*\]),',CONFIG)[1]) for n in [3,4]}
def text(c,s,x,y,size=10,font='Body',center=False,color=INK):
    c.setFillColor(HexColor(color));c.setFont(font,size)
    (c.drawCentredString if center else c.drawString)(x,y,str(s))
def para(c,s,x,top,w,maxh,size=10,align=0):
    s=re.sub(r'\{hex:(\d+)\}',r'\1 hex',s)
    p=Paragraph(escape(s),ParagraphStyle('body',fontName='Body',fontSize=size,leading=size*1.25,textColor=HexColor(INK),alignment=align))
    _,h=p.wrap(w,maxh)
    if h>maxh+.1:raise ValueError(f'Overflow {h}>{maxh}: {s}')
    p.drawOn(c,x,top-h)
    return h
def img(c,path,x,y,w,h,contain=False):
    if contain:
        im=Image.open(path); iw,ih=im.size; ratio=min(w/iw,h/ih)
        x+=(w-iw*ratio)/2;y+=(h-ih*ratio)/2;w=iw*ratio;h=ih*ratio
    key=(str(path),round(w),round(h))
    if key not in IMAGE_CACHE:
        im=Image.open(path);im.thumbnail((max(1,round(w*300/72)),max(1,round(h*300/72))))
        if im.mode=='RGBA' and im.getextrema()[3][0]<255:
            IMAGE_CACHE[key]=ImageReader(im.copy())
        else:
            buf=io.BytesIO();im.convert('RGB').save(buf,format='JPEG',quality=93);buf.seek(0)
            IMAGE_CACHE[key]=ImageReader(buf)
    c.drawImage(IMAGE_CACHE[key],x,y,w,h,mask='auto')
def icon(c,key,x,y,size):img(c,ICONS/(key+'.webp'),x,y,size,size,True)
def paper(c,x,y,w,h):img(c,PRINT/'action-track-watercolor-paper.png',x,y,w,h)
def border(c,x,y,w,h):
    c.setStrokeColor(HexColor(LINE));c.setLineWidth(.5);c.rect(x,y,w,h)
def pdf(name,landscape=False):
    FILES.append(name)
    c=canvas.Canvas(str(OUT/name),pagesize=(792,612) if landscape else (612,792))
    c.setTitle('Moonfall Tactics | '+name);c.setAuthor('Moonfall Tactics')
    return c
def grid(name,items,draw,w=180,h=252,cols=3,rows_per_page=3):
    c=pdf(name)
    for i,item in enumerate(items):
        x=(612-cols*w)/2+(i%cols)*w;y=774-((i//cols)%rows_per_page+1)*h
        c.saveState();c.translate(x,y);draw(c,item,w,h);border(c,0,0,w,h);c.restoreState()
        PLACEMENTS.append({'file':name,'page':i//(cols*rows_per_page)+1,'id':item.get('ID',item.get('id','')),'x':x,'y':y,'width':w,'height':h})
        if i%(cols*rows_per_page)==cols*rows_per_page-1 or i==len(items)-1:c.showPage()
    c.save()
def hero(c,h,w,ht):img(c,PRINT/'cards'/(h['ID']+'.png'),0,0,w,ht)
def portrait(c,h,w,ht):
    paper(c,0,0,w,ht)
    img(c,next((ASSETS/'heroes/current').glob(h['ID']+'-*.png')),3,24,w-6,ht-28,True)
    names=h['Name'].split(' ',1)
    text(c,names[0],w/2,14,8,'Title',True);text(c,names[1],w/2,5,6.5,'Body',True)
    c.setStrokeColor(HexColor('#883c51' if h['Starter side']=='Concord' else '#447fa0'));c.setLineWidth(2);c.rect(1,1,w-2,ht-2)
def tactic(c,t,w,h):
    if not t['ID'].endswith('-cancel'):
        img(c,PRINT/'cards'/(t['ID']+'.png'),0,0,w,h);return
    img(c,ICONS/'tactic-card-template.webp',0,0,w,h)
    icon(c,t['Element'].lower(),w/2-63,105,126)
    para(c,"During combat, cancel the opponent's immediately preceding tactic, including Cancel. Playing a boost instead gives up this chance.",14,79,w-28,68,10,1)
def objective(c,o,w,h):
    img(c,PRINT/'cards'/('objective-'+str(o['index'])+'.png'),0,0,w,h)
    text(c,'1 VP + 1 tactic',w/2,17,9,'Title',True)
def recruit(c,r,w,h):
    paper(c,0,0,w,h);text(c,r['id']+' RECRUITS',w/2,h-27,12,'Title',True)
    img(c,ASSETS/'factions'/(r['id'].lower()+'.png'),w/2-40,h-125,80,80,True)
    for i in range(2):icon(c,'health',w/2-22+i*23,95,22)
    text(c,'Move 3   Attack 2   Defense 2',w/2,72,9,'Body',True)
    para(c,'Melee. Cannot collect Moonstones. Use AP or RAP. Each Recruit has one shared 1 / 2 / 3 ... action-cost counter.',12,55,w-24,46,8,1)
def equipment(c,e,w,h):
    paper(c,0,0,w,h);text(c,e['Name'],w/2,h-21,11,'Title',True)
    if e['ID'] in ['boots','shield','weapon','lens']:
        img(c,ASSETS/'equipment'/(e['ID']+'-v2.png'),8,66,w-16,h-95,True)
    para(c,e['Card text'],12,61,w-24,40,9,1)
    text(c,e['Copies / cost'],w/2,13,10,'Title',True)
def queue():
    c=pdf('06-action-queue.pdf',True)
    text(c,'MOONFALL TACTICS',36,564,22,'Title')
    text(c,'ACTION TRACKS',36,543,10,'Sans',color=LINE)
    for n,y,label in [(3,408,'2 PLAYERS  /  3 HEROES EACH'),(4,246,'3-4 PLAYERS  /  4 HEROES PER FACTION')]:
        text(c,label,36,y+88,11,'Title')
        paper(c,36,y,720,72);border(c,36,y,720,72)
        values=QUEUE[str(n)];sw=720/len(values)
        for i,(ap,rap) in enumerate(values):
            x=36+i*sw
            if i:
                c.setStrokeColor(HexColor(LINE));c.setLineWidth(.8);c.line(x,y,x,y+72)
                c.setFillColor(HexColor(GOLD));p=c.beginPath();p.moveTo(x,y+69);p.lineTo(x-2.5,y+65);p.lineTo(x,y+61);p.lineTo(x+2.5,y+65);p.close();c.drawPath(p,fill=1,stroke=0)
            text(c,f'{ap} AP',x+sw/2,y+42,17,'Title',True)
            text(c,f'{rap} RAP',x+sw/2,y+22,12,'Body',True)
            text(c,str(i),x+sw/2,y+7,6,'Sans',True,color=LINE)
        text(c,'BOTTOM / 0',36,y-15,8,'Sans');text(c,'TOP / '+str(len(values)-1),728,y-15,8,'Sans',True)
    para(c,'Print at 100% / Actual size on US Letter, landscape. Each strip is 10 x 1 inches. Cut around the outer rectangle; do not cut the section breaks.',36,173,720,36,10)
    para(c,'Use one track. Place compact portrait markers below its sections. Read left to right from bottom to top. Capture AP / RAP before moving the chosen hero to slot 0; shift the intervening heroes. Slot 0 is usable.',36,126,720,44,10)
    text(c,'AP: active hero or friendly Recruits.   RAP: friendly Recruits only.   No tactic draws from the track.',36,58,9,'Sans')
    c.save()
def tokens():
    c=pdf('04-tokens.pdf');entries=[]
    for key,name in [('focus','Focus'),('enraged','Enraged'),('fortified','Fortified'),('dazed','Dazed'),('poison','Poison')]:entries += [(key,name)]*10
    entries += [('trap','Trap')]*4+[('moonstone','Moonstone')]*17+[('ongoing','Ability')]*8
    for i,(key,name) in enumerate(entries):
        x=36+i%10*54;y=720-i//10*54;paper(c,x,y,54,54);icon(c,key,x+13,y+18,28);text(c,name,x+27,y+6,6,'Sans',True);border(c,x,y,54,54)
    text(c,'Use red cubes for damage and two spare markers for VP. Print extra tokens for larger stacks.',36,248,9,'Sans')
    text(c,'SETUP TOKEN BACKS - mount 4 traps and 5 starting stones on these identical backs.',36,218,8,'Sans')
    for i in range(9):
        x=36+i*54;paper(c,x,150,54,54);text(c,'?',x+27,169,20,'Title',True);border(c,x,150,54,54)
    text(c,'VICTORY POINTS',36,119,10,'Title')
    for i in range(16):
        x=36+i%8*67.5;y=64-i//8*30;border(c,x,y,67.5,30);text(c,i,x+33.75,y+9,11,'Body',True)
    c.save()
def holders():
    items=[{'id':side+' '+e,'side':side,'element':e} for side in ['Concord','Wildmoon'] for e in ['Fire','Water','Earth','Wind']]
    def draw(c,a,w,h):
        paper(c,0,0,w,h);icon(c,a['element'].lower(),w/2-18,25,36)
        text(c,a['side'],w/2,13,8,'Title',True);text(c,a['element'],w/2,3,7,'Body',True)
        c.setStrokeColor(HexColor('#883c51' if a['side']=='Concord' else '#447fa0'));c.setLineWidth(2);c.rect(1,1,w-2,h-2)
    grid('05-ownership-holders.pdf',items,draw,90,72,4,8)
def standees():
    c=pdf('02-folding-standees.pdf')
    for i,h in enumerate(HEROES):
        x=81+i%5*90;y=36+(1-i//5)*360;path=next((ASSETS/'heroes/current').glob(h['ID']+'-*.png'))
        for flip in [False,True]:
            c.saveState();c.translate(x,y)
            if flip:c.translate(90,360);c.rotate(180)
            img(c,path,4,26,82,145,True);text(c,h['Name'].split()[0],45,17,9,'Title',True);c.restoreState()
        border(c,x,y,90,360);c.setDash(3,3);c.line(x,y+180,x+90,y+180);c.setDash()
    c.save()
def map_pdf():
    im=Image.open(ASSETS/'maps/three-fires-2026-10-21.png');fw=750*im.width/im.height
    c=pdf('10-map.pdf')
    for i in range(2):
        x=(612-fw/2)/2;c.saveState();p=c.beginPath();p.rect(x,21,fw/2,750);c.clipPath(p,stroke=0,fill=0);img(c,ASSETS/'maps/three-fires-2026-10-21.png',x-i*fw/2,21,fw,750);c.restoreState();c.showPage()
    c.save()
def rules():
    name='00-rules-and-legend.pdf';FILES.append(name)
    sty=ParagraphStyle('body',fontName='Body',fontSize=10,leading=12.5,spaceAfter=6,textColor=HexColor(INK))
    heading=ParagraphStyle('heading',parent=sty,fontName='Title',fontSize=14,leading=18,spaceBefore=10,keepWithNext=True)
    flow=[]
    for line in (ROOT/'rules-current.txt').read_text(encoding='utf8').splitlines():
        if not line.strip():continue
        ishead=line.startswith('# ');line=line.removeprefix('# ')
        line=re.sub(r'\{hex:(\d+)\}',r'\1 hex',line)
        flow.append(Paragraph(escape(line),heading if ishead else sty))
    def page(c,d):
        text(c,'MOONFALL TACTICS  /  CURRENT PLAYTEST KIT  /  4 NOVEMBER 2026',36,770,8,'Sans',color=LINE)
        text(c,str(d.page),576,20,9,'Sans',True)
    SimpleDocTemplate(str(OUT/name),pagesize=(612,792),leftMargin=36,rightMargin=36,topMargin=40,bottomMargin=36).build(flow,onFirstPage=page,onLaterPages=page)
def main():
    rules();queue()
    grid('01-tableau-cards.pdf',HEROES,hero)
    grid('02-portrait-cards.pdf',HEROES,portrait,90,126,6,6);standees()
    tactics=[t for t in rows('Tactics') for _ in range(int(t['Copies in shared deck']))]
    grid('03-tactics.pdf',tactics,tactic);tokens();holders()
    grid('07-objectives.pdf',[dict(o,index=i) for i,o in enumerate(rows('Objectives'))],objective)
    grid('08-recruit-reference.pdf',[{'id':'Concord'},{'id':'Wildmoon'}],recruit)
    upgrades=[{'ID':'recruit-'+k,'Name':'Recruit '+n,'Copies / cost':str(cost)+' PP','Card text':'All friendly Recruits gain +1 '+stat+'.'} for k,n,cost,stat in [('boots','Boots',2,'Move'),('shield','Shields',3,'Defense'),('weapon','Weapons',3,'Attack')]]
    grid('09-equipment.pdf',(rows('Equipment')+upgrades)*2,equipment,180,144,3,5);map_pdf()
    writer=PdfWriter()
    for f in FILES:writer.append(OUT/f)
    writer.write(OUT/'Moonfall-Tactics-print-and-play.pdf')
    manifest={'date':SOURCE['date'],'files':FILES,'pages':len(writer.pages),'queue_ap_rap':QUEUE,'track_inches':[10,1],'track_page_inches':[11,8.5],'starting_tactics':2,'objective_tactics':1,'heroes':[h['ID'] for h in HEROES],'tactic_cards':len(tactics),'objectives':6,'placements':PLACEMENTS,'source_sha256':hashlib.sha256((ROOT/'source-snapshot.json').read_bytes()).hexdigest()}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    doc=pdfium.PdfDocument(str(OUT/'Moonfall-Tactics-print-and-play.pdf'));thumbs=[]
    for i in range(len(doc)):
        im=doc[i].render(scale=1).to_pil();im.save(OUT/f'preview-{i+1:02}.png');im.thumbnail((306,396));thumbs.append(im.copy())
    for g in range((len(thumbs)+5)//6):
        contact=Image.new('RGB',(918,840),'#dedede');d=ImageDraw.Draw(contact)
        for j,im in enumerate(thumbs[g*6:g*6+6]):
            x=j%3*306;y=j//3*420;contact.paste(im,(x,y));d.text((x+8,y+398),str(g*6+j+1),fill='black')
        contact.save(OUT/f'contact-{g+1}.png')
    doc=pdfium.PdfDocument(str(OUT/'06-action-queue.pdf'));doc[0].render(scale=1.5).to_pil().save(OUT/'action-track-preview.png')
    print(f'Built {len(writer.pages)} pages; {len(tactics)} tactics; both tracks on one landscape Letter page.')
if __name__=='__main__':main()
