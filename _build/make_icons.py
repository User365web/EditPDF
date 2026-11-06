from PIL import Image, ImageDraw, ImageFont
import os
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
def P(*a): return os.path.join(ROOT,*a)

def grad(w,h):
    img=Image.new('RGB',(w,h)); px=img.load()
    a=(98,84,232); b=(52,120,246)
    for y in range(h):
        for x in range(w):
            t=(x/w+y/h)/2
            px[x,y]=tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
    return img

def icon(size, radius_ratio=0.235):
    s=size*4; k=s/64
    base=grad(s,s).convert('RGBA'); d=ImageDraw.Draw(base)
    d.polygon([(18*k,9*k),(38*k,9*k),(48*k,19*k),(48*k,54*k),(45*k,57*k),(18*k,57*k),(15*k,54*k),(15*k,12*k)],fill='white')
    d.polygon([(38*k,9*k),(48*k,19*k),(38*k,19*k)],fill=(201,197,255))
    c=(85,71,216); x0,y0=23*k,26*k
    d.rectangle([x0,y0,x0+4*k,y0+19*k],fill=c)
    d.rectangle([x0,y0,x0+14*k,y0+4*k],fill=c)
    d.rectangle([x0,y0+7.5*k,x0+11*k,y0+11.5*k],fill=c)
    d.rectangle([x0,y0+15*k,x0+14*k,y0+19*k],fill=c)
    d.rounded_rectangle([22*k,49*k,42*k,51*k],radius=k,fill=(141,134,237))
    mask=Image.new('L',(s,s),0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,s-1,s-1],radius=int(s*radius_ratio),fill=255)
    out=Image.new('RGBA',(s,s),(0,0,0,0)); out.paste(base,(0,0),mask)
    return out.resize((size,size),Image.LANCZOS)

icon(192).save(P('img','icon-192.png'))
icon(512).save(P('img','icon-512.png'))
icon(180,0.0).convert('RGB').save(P('img','apple-touch-icon.png'))
icon(256).save(P('favicon.ico'),sizes=[(16,16),(32,32),(48,48),(64,64)])
icon(64).save(P('favicon.png'))

W,H=1200,630
og=grad(W,H); d=ImageDraw.Draw(og)
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
ic=icon(150); og.paste(ic,(80,88),ic)
d.text((255,112),"EditPDF",font=ImageFont.truetype(bold,84),fill='white')
d.text((80,265),"Free online PDF tools",font=ImageFont.truetype(bold,50),fill='white')
f3=ImageFont.truetype(reg,32)
d.text((80,335),"Merge · Split · Compress · Rotate · Image to PDF",font=f3,fill=(226,224,255))
d.text((80,400),"Fast, free, and private — right in your browser.",font=f3,fill=(226,224,255))
d.rounded_rectangle([80,500,520,566],radius=16,fill='white')
d.text((110,517),"No account. No install.",font=ImageFont.truetype(bold,30),fill=(85,71,216))
og.save(P('img','og-image.png'),optimize=True)
print('icons ok')
