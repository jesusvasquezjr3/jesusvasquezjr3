from PIL import Image, ImageDraw, ImageFont
import math, os

W,H=1600,620
FRAMES=24
FPS=12
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(os.path.dirname(HERE),'assets')

font_display='/usr/share/fonts/opentype/roboto/slab/RobotoSlab-Bold.otf'
font_text='/usr/share/fonts/truetype/lato/Lato-Medium.ttf'
font_light='/usr/share/fonts/truetype/lato/Lato-Light.ttf'
font_mono='/usr/share/fonts/truetype/paratype/PTM55F.ttf'

F_TITLE=ImageFont.truetype(font_display,86)
F_SUB=ImageFont.truetype(font_text,28)
F_META=ImageFont.truetype(font_text,18)
F_MICRO=ImageFont.truetype(font_mono,15)
F_ASCII=ImageFont.truetype(font_mono,19)

chars=' .:-=+*#%@'

def torus_ascii(t):
    cols,rows=54,30
    zbuf=[-1e9]*(cols*rows)
    val=[0.0]*(cols*rows)
    A=0.38+0.08*math.sin(t*0.5)
    B=t*0.55
    for i in range(0,150):
        th=2*math.pi*i/150
        ct,st=math.cos(th),math.sin(th)
        for j in range(0,72):
            ph=2*math.pi*j/72
            cp,sp=math.cos(ph),math.sin(ph)
            R,r=1.55,0.58
            x=(R+r*ct)*cp; y=(R+r*ct)*sp; z=r*st
            y2=y*math.cos(A)-z*math.sin(A); z2=y*math.sin(A)+z*math.cos(A); x2=x
            x3=x2*math.cos(B)-y2*math.sin(B); y3=x2*math.sin(B)+y2*math.cos(B); z3=z2
            zz=z3+4.4
            sx=int(cols/2 + x3/zz*31)
            sy=int(rows/2 - y3/zz*16)
            if 0<=sx<cols and 0<=sy<rows:
                idx=sy*cols+sx
                if z3>zbuf[idx]:
                    zbuf[idx]=z3
                    nx=ct*cp; ny=ct*sp; nz=st
                    ny2=ny*math.cos(A)-nz*math.sin(A); nz2=ny*math.sin(A)+nz*math.cos(A); nx2=nx
                    nx3=nx2*math.cos(B)-ny2*math.sin(B); ny3=nx2*math.sin(B)+ny2*math.cos(B); nz3=nz2
                    l=max(0,min(1,0.62*nx3-0.55*ny3+0.55*nz3))
                    val[idx]=l
    lines=[]
    for y in range(rows):
        row=''
        for x in range(cols):
            idx=y*cols+x
            if zbuf[idx]<-1e8: row+=' '
            else: row+=chars[min(len(chars)-1,int(val[idx]*(len(chars)-1)))]
        lines.append(row.rstrip())
    return lines

def frame(theme,t):
    if theme=='dark':
        bg='#11100E'; fg='#F3EFE5'; muted='#9B9487'; accent='#E55B2D'; hair='#38342E'
    else:
        bg='#F3EFE5'; fg='#171511'; muted='#6C665E'; accent='#C6421D'; hair='#CFC7B8'
    im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
    m=72; gridw=W-2*m; col=gridw/12
    d.line((m,50,W-m,50),fill=hair,width=2)
    d.text((m,20),'JV / 2026',font=F_MICRO,fill=muted)
    right='BIOMEDICAL × ARTIFICIAL INTELLIGENCE'
    bbox=d.textbbox((0,0),right,font=F_MICRO)
    d.text((W-m-(bbox[2]-bbox[0]),20),right,font=F_MICRO,fill=muted)
    d.text((m,112),'JESÚS',font=F_TITLE,fill=fg)
    d.text((m,202),'VÁSQUEZ',font=F_TITLE,fill=fg)
    d.rectangle((m,314,m+150,320),fill=accent)
    d.text((m,350),'Biomedical Engineer',font=F_SUB,fill=fg)
    d.text((m,390),'Artificial Intelligence Engineer',font=F_SUB,fill=fg)
    d.text((m,456),'M.Sc. Data Science & Artificial Intelligence',font=F_META,fill=muted)
    d.text((m,497),'AI · SOFTWARE · EMBEDDED · CAD',font=F_MICRO,fill=muted)
    lines=torus_ascii(t)
    x0=int(m+7.5*col); y0=92
    d.line((x0-26,84,W-m,84),fill=hair,width=1)
    d.line((x0-26,84,x0-26,540),fill=hair,width=1)
    for k,line in enumerate(lines):
        d.text((x0,y0+35+k*15),line,font=F_ASCII,fill=fg)
    d.line((m,586,W-m,586),fill=hair,width=2)
    return im

for theme in ('dark','light'):
    frames=[frame(theme,2*math.pi*i/FRAMES) for i in range(FRAMES)]
    frames[0].save(os.path.join(OUT,f'hero-{theme}.gif'),save_all=True,append_images=frames[1:],duration=int(1000/FPS),loop=0,optimize=True)
    frames[0].save(os.path.join(OUT,f'hero-{theme}.png'))
print('generated')
