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

pdfmetrics.registerFontFamily('Body',normal='Body',bold='Title')
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

def rich(c,s,x,top,w,maxh,size=9):

    s=escape(s)

    s=re.sub(r'\{hex:(\d+)\}',r'\1 hex',s)

    for word,key in [('Attack dice','attack-dice'),('Attack die','attack-dice'),('Defense die','defense'),('Defense','defense'),('Move','move'),('Fortified','fortified'),('Enraged','enraged'),('Dazed','dazed'),('Focus','focus'),('Poison','poison'),('HP','health')]:

        s=re.sub(r'\b'+word+r'\b',lambda m:'<img src="'+str(ICONS/(key+'.webp'))+'" width="11" height="11" valign="middle"/>',s)

    p=Paragraph(s,ParagraphStyle('rich',fontName='Body',fontSize=size,leading=size*1.3,textColor=HexColor(INK)))

    _,ph=p.wrap(w,maxh)

    if ph>maxh:raise ValueError('Card text overflow: '+s)

    p.drawOn(c,x,top-ph)

def character_frame(c,w=180,h=252):

    paper(c,0,0,w,h);border(c,2,2,w-4,h-4)

    border(c,7,89,w-14,22)

    border(c,7,8,w-14,77)

def hero(c,h,w,ht):

    if 'id' in h:return recruit(c,h,w,ht)

    character_frame(c,w,ht)

    text(c,h['Name'],10,233,12,'Title')

    text(c,h['Primary class'].title()+' / '+h['Secondary class'].title(),10,219,8)

    img(c,next((ASSETS/'heroes/current').glob(h['ID']+'-*.png')),43,126,94,86,True)

    for key,val,y in [('move',re.search(r'\d+',str(h['Move']))[0],175),('defense',h['Defense dice'],145)]:

        icon(c,key,10,y,24);text(c,val,22,y+7,11,'Title',True)

    for i in range(int(h['HP'])):icon(c,'health',151,194-i*14,14)

    text(c,h['Region'],10,115,7)

    icon(c,'pp',144,113,13);text(c,h['PP cost'],164,115,8,'Title')

    ranged=h['Range rule'].lower()!='melee'

    icon(c,'ranged' if ranged else 'melee',64,93,17)

    text(c,str(h['Attack dice'])+(' ('+re.search(r'\d+',str(h['Attack range']))[0]+')' if ranged else ''),86,98,11,'Title')

    icon(c,'assigned-element',11,67,13)

    text(c,h['Unique ability'],28,72,9,'Title')

    rich(c,h['Ability effect'],12,61,w-24,48,8.5)


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

    for key,val,x in [('move',3,30),('melee',2,78),('defense',2,126)]:

        icon(c,key,x,65,20);text(c,val,x+23,70,11,'Title')


def equipment(c,e,w,h):

    paper(c,0,0,w,h);text(c,e['Name'],w/2,h-21,11,'Title',True)

    if e['ID'] in ['boots','shield','weapon','lens']:

        img(c,ASSETS/'equipment'/(e['ID']+'-v2.png'),8,66,w-16,h-95,True)

    rich(c,e['Card text'],12,61,w-24,40,9)

    icon(c,'pp',w/2-18,9,16);text(c,str(e['Copies / cost']).replace(' PP',''),w/2+3,13,10,'Title')

def queue():

    c=pdf('06-action-queue.pdf',True)

    for n,top,label in [(3,552,'2 PLAYERS'),(4,318,'3-4 PLAYERS')]:

        text(c,label,72,top+20,11,'Title')

        for i,(ap,rap) in enumerate(QUEUE[str(n)]):

            x=72+(i%3)*216;y=top-72-(i//3)*78

            paper(c,x,y,216,72);border(c,x,y,216,72)

            text(c,f'{ap} AP',x+108,y+42,17,'Title',True)

            text(c,f'{rap} RAP',x+108,y+22,12,'Body',True)

            text(c,str(i),x+108,y+7,7,'Sans',True,color=LINE)

    c.save()


def tokens():

    c=pdf('04-tokens.pdf');entries=[]

    for key,name in [('focus','Focus'),('enraged','Enraged'),('fortified','Fortified'),('dazed','Dazed'),('poison','Poison')]:entries += [(key,name)]*10

    entries += [('trap','Trap')]*4+[('moonstone','Moonstone')]*17

    for i,(key,name) in enumerate(entries):

        x=36+i%10*54;y=720-i//10*54;paper(c,x,y,54,54);icon(c,key,x+13,y+18,28);text(c,name,x+27,y+6,6,'Sans',True);border(c,x,y,54,54)

    for i in range(21):

        x=576;step=432/21;y=774-(i+1)*step

        border(c,x,y,24,step);text(c,i,x+12,y+6,9,'Body',True)

    c.save()

def holders():

    items=[{'id':side+' '+e,'side':side,'element':e} for side in ['Concord','Wildmoon'] for e in ['Fire','Water','Earth','Wind']]

    def draw(c,a,w,h):

        paper(c,0,0,w,h)

        c.setStrokeColor(HexColor('#883c51' if a['side']=='Concord' else '#447fa0'));c.setLineWidth(2);c.rect(1,1,w-2,h-2)

        border(c,36,36,90,126)

        icon(c,a['element'].lower(),w/2-28,4,26)

        img(c,ASSETS/'factions'/(a['side'].lower()+'.png'),w/2+3,4,26,26,True)

    grid('05-ownership-holders.pdf',items,draw,162,198,3,3)


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

    c=pdf('00-rules-and-legend.pdf')

    text(c,'MOONFALL TACTICS',30,760,18,'Title')

    bullets=[

    ('Turn','Score scenario VP; check victory. Each friendly poisoned unit takes 1 damage and removes 1 Poison. Choose a hero, capture AP/RAP, move its queue card to slot 0. All slots are usable.'),

    ('Actions','AP pays for the active hero or Recruits; RAP only Recruits. Each hero action separately costs 1/2/3... AP; each Recruit shares one counter across paid actions. Respawn never resets costs.'),

    ('Abilities','Discard a matching assigned-element tactic and pay printed AP. Paid repeats cost +1 AP; card-only repeats stay card-only. Ongoing effects last until the next activation or defeat unless stated otherwise.'),

    ('Movement','Move up to printed allowance through empty legal hexes. Push/Pull changes distance from its fixed source each step. Resolve hazards on entry; stop on defeat. Nothing blocks sight.'),

    ('Combat','Alternate legal boosts or Pass; two passes roll. Cancel only the immediately preceding opponent combat tactic, including Cancel. A boost gives up the earlier cancellation chance.'),

    ('Dice','Highest die wins; compare six counts only when both maxima are 6; attacker wins ties. Zero pool: roll two, keep lower. Attacker may reroll own dice for 1 banked compensation PP each.'),

    ('Damage','Hit: 1 + kept attacker sixes + Enraged + Heavy Attack + declared bonuses; apply Light Attack cap last. Winning defender gains Focus per kept six.'),

    ('Position','Melee: +1 die per qualifying adjacent ally. Ranged: -2 when engaged and -2 beyond normal range, up to double; penalties stack. Exact range never extends.'),

    ('Statuses','Focus: +1 Attack die; Enraged: +1 hit damage. Fortified/Dazed: +1/-1 Defense die. Spend participating stacks after the roll; new tokens survive. Healing restores HP and clears all Poison. A hero reduced from above 1 HP to exactly 1 gains Enraged.'),

    ('Cards','Shared 27-card deck with three elements or 36 with four. Start with 2 tactics; limit 8. Use printed effect OR matching ability payment. Reshuffle shared discards only when needed; no empty-hand refill.'),

    ('Rewards','Only heroes collect Moonstones: 1 tactic + 1 Focus. Hero defeat drops a stone, draws 1 tactic for its owner and moves its queue card to slot 0. Recruits do neither.'),

    ('End turn','Collect stones under friendly heroes; resolve overflow. Claim at most one eligible objective for 1 VP + 1 tactic. Eligibility starts next own turn. Draw an objective only if empty; never reshuffle. Resolve end effects and hazards; pass. Victory interrupts immediately.')

    ]

    y=733

    for title,body in bullets:

        p=Paragraph('• <b>'+title+'.</b> '+escape(body),ParagraphStyle('rule',fontName='Body',fontSize=9,leading=11))

        _,ph=p.wrap(552,700);p.drawOn(c,30,y-ph);y-=ph+6

    text(c,'ICON LEGEND',30,y-8,11,'Title');y-=38

    keys=[('health','HP'),('move','Move'),('distance','Distance'),('melee','Melee'),('ranged','Ranged'),('attack-dice','Attack dice'),('defense','Defense'),('damage','Damage'),('fire','Fire'),('water','Water'),('earth','Earth'),('wind','Wind'),('assigned-element','Assigned element'),('focus','Focus'),('enraged','Enraged'),('fortified','Fortified'),('dazed','Dazed'),('poison','Poison'),('ap','AP'),('recruit-ap','RAP'),('pp','PP'),('rp','RP'),('vp','VP'),('moonstone','Moonstone'),('trap','Trap'),('objective','Objective')]

    for i,(key,label) in enumerate(keys):

        x=30+i%4*140;yy=y-i//4*24

        icon(c,key,x,yy,19);text(c,label,x+24,yy+6,8)

    for i,side in enumerate(['concord','wildmoon']):

        x=310+i*140;yy=y-6*24

        img(c,ASSETS/'factions'/(side+'.png'),x,yy,19,19,True);text(c,side.title(),x+24,yy+6,8)

    if y-6*24<20:raise ValueError('Legend overflow')

    c.save()


def remake_characters():
    c=canvas.Canvas(str(PRINT/'character-card-template.pdf'),pagesize=(180,252))
    character_frame(c);c.save()
    for h in HEROES:
        target=PRINT/'cards'/(h['ID']+'.pdf')
        c=canvas.Canvas(str(target),pagesize=(180,252));hero(c,h,180,252);c.save()
        doc=pdfium.PdfDocument(str(target))
        im=doc[0].render(scale=10/3).to_pil()
        im.save(PRINT/'cards'/(h['ID']+'.png'))
        im.save(GAME/'public/cards'/(h['ID']+'.png'))
        doc.close();target.unlink()
def main():
    remake_characters()

    rules();queue()

    grid('01-tableau-cards.pdf',HEROES+[{'id':'Concord'},{'id':'Wildmoon'}],hero)

    grid('02-portrait-cards.pdf',HEROES,portrait,90,126,6,6);standees()

    tactics=[t for t in rows('Tactics') for _ in range(int(t['Copies in shared deck']))]

    grid('03-tactics.pdf',tactics,tactic);tokens();holders()

    grid('07-objectives.pdf',[dict(o,index=i) for i,o in enumerate(rows('Objectives'))],objective)

    upgrades=[{'ID':'recruit-'+k,'Name':'Recruit '+n,'Copies / cost':str(cost)+' PP','Card text':'All friendly Recruits gain +1 '+stat+'.'} for k,n,cost,stat in [('boots','Boots',2,'Move'),('shield','Shields',3,'Defense'),('weapon','Weapons',3,'Attack')]]

    grid('09-equipment.pdf',(rows('Equipment')+upgrades)*2,equipment,180,144,3,5);map_pdf()

    writer=PdfWriter()

    for f in FILES:writer.append(OUT/f)

    writer.write(OUT/'Moonfall-Tactics-print-and-play.pdf')

    manifest={'date':SOURCE['date'],'files':FILES,'pages':len(writer.pages),'queue_ap_rap':QUEUE,'section_inches':[3,1],'track_page_inches':[11,8.5],'starting_tactics':2,'objective_tactics':1,'heroes':[h['ID'] for h in HEROES],'tactic_cards':len(tactics),'objectives':6,'placements':PLACEMENTS,'source_sha256':hashlib.sha256((ROOT/'source-snapshot.json').read_bytes()).hexdigest()}

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

