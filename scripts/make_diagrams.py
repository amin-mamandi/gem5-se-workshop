#!/usr/bin/env python3
"""Edit labels/colors here, then regenerate presentation SVG assets."""
from pathlib import Path
from html import escape
R=Path(__file__).resolve().parents[1]/'assets/diagrams'
R.mkdir(parents=True,exist_ok=True)
BLUE='#008eae'; DARK='#153347'; SOFT='#e4f3f7'; ORANGE='#d88335'; GRAY='#526b79'
def wrap(body):
 return ('<svg xmlns="http://www.w3.org/2000/svg" width="1060" height="410" viewBox="0 0 1060 410" role="img">'
         '<rect width="1060" height="410" fill="#f9fbfc"/>'
         '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#008eae"/></marker></defs>'
         +body+'</svg>')
def text(x,y,t,size=28,color=DARK,weight='normal',anchor='middle'):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial,sans-serif" font-weight="{weight}" font-size="{size}" text-anchor="{anchor}">{escape(t)}</text>'
def box(x,y,w,h,label,fill=SOFT,sub=None):
 s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{BLUE}" stroke-width="3"/>'
 s+=text(x+w/2,y+h/2+(0 if sub else 10),label,24 if len(label)>8 else 31,DARK,'bold')
 if sub:s+=text(x+w/2,y+h/2+34,sub,20,GRAY)
 return s
def line(x1,y1,x2,y2,color=BLUE,dash=''):
 dash_attribute = 'stroke-dasharray="10 10"' if dash else ''
 return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="5" {dash_attribute} marker-end="url(#arrow)"/>'
def save(name,s): (R/(name+'.svg')).write_text(wrap(s))
def flow(name, labels, captions=None):
 captions=captions or ['']*len(labels)
 n=len(labels); w=min(205,(980-55*(n-1))/n); gap=(980-n*w)/(n-1) if n>1 else 0
 y=142;s=''
 for i,(lab,sub) in enumerate(zip(labels,captions)):
  x=40+i*(w+gap);s+=box(x,y,w,120,lab,sub=sub if sub else None)
  if i<n-1:s+=line(x+w+5,y+60,x+w+gap-12,y+60)
 save(name,s)
# A request path, not a chain of loosely related ideas. An earlier hit stops it.
flow('cpu-l1-l2-dram',['CPU','L1 data','L2','DRAM'],
     ['asks for A[5]','first lookup','next lookup','last resort'])
# Compilation and execution are different actions. Label the arrows.
s=box(57,147,246,122,'C program',sub='c = a + b')
s+=box(417,147,246,122,'x86 instructions',sub='compiled machine code')
s+=box(776,147,227,122,'x86 CPU',sub='executes them')
s+=line(309,209,401,209)+line(669,209,760,209)
s+=text(355,164,'compile',22,GRAY)+text(715,164,'execute',22,GRAY)
save('isa',s)
# Two independent inputs feed gem5; the statistics are the output.
s=box(55,72,282,109,'Program',sub='what runs')
s+=box(55,239,282,109,'Hardware settings',sub='what machine?')
s+=box(472,151,207,122,'gem5',sub='simulates')
s+=box(782,151,221,122,'stats.txt',sub='what happened?')
s+=line(342,126,454,188)+line(342,294,454,235)+line(685,212,764,212)
save('gem5-workflow',s)
s=box(52,132,240,130,'CPU',sub='needs A[5]')+box(410,132,240,130,'Cache',sub='A[5] is here')+line(295,197,395,197)
s+=text(800,188,'HIT',65,BLUE,'bold')+text(800,235,'nearby data',27,GRAY)
save('cache-hit',s)
s=box(40,132,220,130,'CPU',sub='needs A[5]')+box(347,132,220,130,'Cache',sub='A[5] absent')+box(770,132,230,130,'DRAM',sub='fetch line')
s+=line(260,197,328,197)+line(570,197,750,197)+text(663,148,'MISS',29,ORANGE,'bold')
save('cache-miss',s)
s=''
for i in range(8):
 x=78+114*i;s+=box(x,148,100,100,f'A[{i}]', '#b9e6ed' if i==0 else SOFT)
s+=text(530,100,'One request can bring neighboring elements',30,DARK,'bold')
s+=text(530,315,'Illustration: 64-byte line, eight 8-byte values',23,GRAY)
save('cache-line',s)
s=''
for i in range(8):
 x=80+114*i;s+=box(x,134,98,90,str(i), '#b9e6ed')
 if i<7:s+=line(x+99,180,x+111,180)
s+=text(530,295,'Next address, next address, next address',31,DARK)
save('sequential',s)
s=''
for i in range(8): s+=box(80+114*i,134,98,90,str(i),SOFT)
for idx,y in enumerate([0,5,1,7]):
 s+=text(220+idx*225,308,str(y),36,ORANGE,'bold')
 if idx<3:s+=line(251+idx*225,295,372+idx*225,295)
s+=text(530,375,'A repeatable scrambled order visits each location once',25,GRAY)
save('permuted',s)
s='<rect x="85" y="154" width="900" height="85" rx="18" fill="'+SOFT+'"/>'
s+=text(164,193,'WORK',25,DARK,'bold')+text(525,193,'WAIT FOR DATA',31,ORANGE,'bold')+text(892,193,'WORK',25,DARK,'bold')
s+='<rect x="95" y="210" width="165" height="20" fill="'+BLUE+'"/><rect x="265" y="210" width="607" height="20" fill="'+ORANGE+'"/><rect x="878" y="210" width="97" height="20" fill="'+BLUE+'"/>'
s+=text(530,316,'Illustrative timeline, not to scale',24,GRAY)
save('cpu-wait',s)
s=''
for y,label,c in [(90,'Bank 0',SOFT),(215,'Bank 1',SOFT)]:
 s+=box(86,y,220,95,label,c)
 for j in range(3):
  s+=box(390+j*202,y+4,178,80,f'Row {j}', '#b9e6ed' if j==0 else SOFT)
s+=text(530,365,'A bank keeps one row open at a time',25,GRAY)
save('dram-banks',s)
s=box(60,130,260,120,'Request',sub='read from row 4')
s+=box(755,130,248,120,'Bank 0',sub='row 4 open')
s+=line(328,195,737,195)+text(530,155,'ROW HIT',36,BLUE,'bold')
save('row-hit',s)
s=box(60,130,260,120,'Request',sub='read from row 9')
s+=box(755,130,248,120,'Bank 0',sub='row 4 open')
s+=line(328,195,737,195)+text(530,145,'CLOSE 4, OPEN 9',28,ORANGE,'bold')
s+=text(530,309,'Same bank, different row: extra work',26,GRAY)
save('row-conflict',s)
s=box(80,145,280,110,'B[k,j]',sub='columnwise in ijk')+box(700,145,280,110,'B[k,j]',sub='rowwise in ikj')
s+=line(385,199,670,199)+text(530,135,'Change the loop order',30,BLUE,'bold')
save('matrix-order',s)

# The three structural views start at the familiar CPU and open one box at a time.
s='<rect x="65" y="56" width="930" height="294" rx="22" fill="#f0f8fa" stroke="'+BLUE+'" stroke-width="4"/>'
s+=text(530,105,'CPU',38,DARK,'bold')
for x,label,sub in [(126,'Control','chooses actions'),(412,'Registers','hold current values'),(698,'Arithmetic','does the addition')]:
 s+=box(x,145,236,133,label,sub=sub)
s+=text(530,325,'These are parts of one CPU core, not steps in a pipeline',23,GRAY)
save('cpu-structure',s)
s=box(68,126,210,136,'CPU',sub='asks for A[5]')
s+=box(383,102,310,190,'Cache',sub='copies of nearby data')
s+=box(786,126,205,136,'DRAM',sub='more data')
s+=line(284,198,360,198)+line(698,198,767,198)
for i in range(4):
 s+=f'<rect x="{415+i*62}" y="256" width="54" height="18" rx="4" fill="{BLUE if i==1 else "#b9dce5"}"/>'
s+=text(530,352,'Cache is organized into lines (blocks of bytes)',23,GRAY)
save('cache-structure',s)
s=box(60,114,270,163,'Memory',sub='controller')
s+=line(337,195,409,195)
s+=f'<rect x="432" y="71" width="563" height="268" rx="20" fill="{SOFT}" stroke="{BLUE}" stroke-width="3"/>'
s+=text(714,113,'DRAM',34,DARK,'bold')
for i,(x,label) in enumerate(((456,'Bank 0'),(727,'Bank 1'))):
 s+=box(x,135,245,187,label,sub='rows inside')
 for j in range(3):
  color='#63bed0' if j==1 else '#bddfe8'
  s+=f'<rect x="{x+33}" y="{278+j*15}" width="176" height="9" rx="3" fill="{color}"/>'
s+=text(530,380,'The controller uses an address to select a bank and row',23,GRAY)
save('dram-structure',s)
s=box(45,89,285,215,'CPU',sub='needs a value')
s+=box(388,89,285,215,'Cache',sub='checks nearby copy')
s+=box(731,89,285,215,'DRAM',sub='supplies on a miss')
s+=line(337,171,376,171)+line(680,171,719,171)
s+=line(376,239,337,239)+line(719,239,680,239)
s+=text(530,359,'Top arrows: request; bottom arrows: data returning',22,GRAY)
save('cpu-cache-dram-structure',s)
s=''
for i,(label,sub) in enumerate([('Performance','How long to get data?'),('Capacity','How much fits?'),('Scaling','Can we keep adding it?')]):
 x=40+345*i
 s+=box(x,113,300,160,label,sub=sub)
s+=text(530,339,'Three reasons memory affects system design',23,GRAY)
save('why-memory',s)
s=box(64,95,435,207,'SRAM',sub='6 transistors per typical cell')
s+=box(561,95,435,207,'DRAM',sub='1 transistor + 1 capacitor')
s+=text(280,352,'fast · low density · costly per bit',23,GRAY)
s+=text(778,352,'dense · slower · cheaper per bit',23,GRAY)
save('sram-vs-dram',s)
s=box(78,115,210,150,'Registers',sub='tiny, closest')+box(389,115,265,150,'Caches',sub='small, fast')+box(751,115,230,150,'DRAM',sub='larger, farther')
s+=text(530,354,'Left to right: more capacity, usually longer to reach',25,GRAY)
save('memory-tradeoff',s)


s=text(530,85,'Five integers, four bytes each',32,DARK,'bold')
for i in range(5):
 x=76+i*195
 s+=box(x,138,170,110,f'item {i}',sub='4 bytes')
s+=text(530,326,'5 × 4 bytes = 20 bytes in this x86 example',29,BLUE,'bold')
save('five-integers',s)


# A deliberately simplified DRAM storage cell; no circuit timing is implied.
s=text(530,75,'One DRAM bit: a switch and a tiny charge store',30,DARK,'bold')
s+=box(97,134,246,138,'Transistor',sub='select switch')
s+=line(354,203,470,203)
s+='<path d="M488 136 L488 270 M527 136 L527 270" stroke="'+BLUE+'" stroke-width="8"/>'
s+=text(508,320,'Capacitor',31,DARK,'bold')
s+=text(794,202,'charge = bit',31,BLUE,'bold')
s+=text(530,375,'Refresh restores charge as it leaks away',23,GRAY)
save('dram-cell',s)

# CPU walkthrough: every arrow names a physical or logical action.
s=f'<rect x="70" y="38" width="920" height="330" rx="23" fill="{SOFT}" stroke="{BLUE}" stroke-width="4"/>'
s+=text(530,86,'RAM holds bytes at addresses',34,DARK,'bold')
s+=box(120,110,365,230,'Program instructions',sub='next instruction address')
s+=text(303,306,'LOAD  ·  ADD  ·  JUMP IF',24,GRAY)
s+=box(575,110,365,230,'Program data',sub='array values')
s+=text(758,306,'cells[0] = 10     cells[1] = 20',23,GRAY)
save('instructions-and-data',s)

s=box(38,147,255,150,'CPU',sub='asks for cells[0]')
s+=box(768,147,255,150,'RAM',sub='holds the value 10')
s+=line(303,175,748,175)+line(303,228,748,228)+line(748,277,303,277)
s+=text(530,154,'ADDRESS: cells[0]',22,GRAY,'bold')
s+=text(530,210,'READ command',22,GRAY,'bold')
s+=text(530,323,'DATA: 10 returns',22,GRAY,'bold')
s+=text(530,381,'Simple wiring model; caches and controller omitted',22,GRAY)
save('ram-read-wires',s)

s=box(40,152,260,117,'Program counter',sub='next instruction address')
s+=box(401,152,252,117,'Instruction bytes',sub='fetched from memory')
s+=box(755,152,270,117,'Control',sub='decodes instruction')
s+=line(307,210,382,210)+line(661,210,736,210)
s+=text(346,183,'address',20,GRAY)
s+=text(701,183,'bits',20,GRAY)
s+=text(530,355,'After a jump, the program counter holds the target address',23,GRAY)
save('fetch-instruction',s)

s=box(48,135,296,158,'Memory',sub='cells[0] = 10')
s+=box(715,135,296,158,'CPU registers',sub='a = 10, sum = 30')
s+=line(353,185,695,185)+line(695,251,353,251)
s+=text(530,161,'LOAD: 10 travels in',24,BLUE,'bold')
s+=text(530,302,'STORE: 30 travels out',24,ORANGE,'bold')
s+=text(530,365,'The cache can supply or accept either access',22,GRAY)
save('load-and-store',s)

s=box(386,25,286,103,'Control',sub='selects ADD')
s+=box(55,179,292,142,'Registers',sub='a = 10, b = 20')
s+=box(746,179,260,142,'ALU',sub='adds the inputs')
s+=line(680,113,749,169)+line(356,225,730,225)+line(730,286,356,286)
s+=text(710,105,'ADD',23,BLUE,'bold')
s+=text(539,198,'10 and 20',24,GRAY)
s+=text(539,323,'result: 30',24,ORANGE,'bold')
save('alu-add-control',s)

s=box(50,129,275,140,'Register',sub='loaded value: 30')
s+=box(391,129,275,140,'ALU',sub='compare with 30')
s+=box(734,129,275,140,'Condition',sub='equal = yes')
s+=line(333,200,374,200)+line(674,200,718,200)
s+=text(530,353,'COMPARE records whether the two values match',26,GRAY)
save('compare-equal',s)

s=box(387,48,286,107,'Equal condition?',sub='from COMPARE')
s+=box(62,246,373,115,'Print sum = 30',sub='equal path')
s+=box(625,246,373,115,'Print unexpected',sub='other path')
s+=line(446,162,305,235)+line(614,162,753,235)
s+=text(297,180,'yes',25,BLUE,'bold')+text(767,180,'no',25,ORANGE,'bold')
save('jump-if-equal',s)

s=box(21,139,237,144,'CPU',sub='requests cells[0]')
s+=box(290,139,237,144,'Cache',sub='checks nearby copy')
s+=box(560,139,237,144,'Controller',sub='drives DRAM on miss')
s+=box(830,139,215,144,'DRAM',sub='more data')
for x1,x2 in ((264,279),(534,550),(804,819)):
 s+=line(x1,185,x2,185)
for x1,x2 in ((819,804),(550,534),(279,264)):
 s+=line(x1,247,x2,247)
s+=text(396,105,'lookup',22,GRAY)+text(667,105,'on a miss',22,GRAY)
s+=text(530,365,'Upper arrows: request    Lower arrows: data returning',23,GRAY)
save('cpu-cache-controller-dram',s)

# Cache lookup: a conceptual two-way set with explicit tags and valid bits.
s=text(530,72,'Example address for A[5]',34,DARK,'bold')
for x,w,label,sub in ((75,300,'TAG','Which line?'),(402,255,'SET INDEX','Which set?'),(684,302,'OFFSET','Which bytes in the line?')):
 s+=box(x,123,w,140,label,sub=sub)
s+=text(530,354,'Bit widths depend on the cache design',25,GRAY)
save('cache-address-parts',s)

s=box(57,24,257,90,'Request tag X')
s+=box(74,137,465,92,'Way 0',sub='valid = 1   stored tag = X')
s+=box(74,266,465,92,'Way 1',sub='valid = 1   stored tag = Y')
s+=box(608,137,182,92,'Compare',sub='X = X?')
s+=box(608,266,182,92,'Compare',sub='Y = X?')
s+=f'<path d="M314 69 H574 V289" fill="none" stroke="{ORANGE}" stroke-width="3"/>'
s+=f'<path d="M574 159 H593 M574 289 H593" fill="none" stroke="{ORANGE}" stroke-width="3"/>'
s+=line(545,184,590,184)+line(545,313,590,313)
s+=text(905,178,'HIT',29,BLUE,'bold')
s+=text(905,214,'select way 0 data',19,GRAY)
s+=text(895,312,'no match',24,GRAY)
s+=text(530,392,'Both ways belong to one selected set',23,GRAY)
save('cache-tag-compare',s)

s=box(70,131,320,155,'L2',sub='has the requested line')
s+=box(645,131,330,155,'L1 data cache',sub='write tag + line bytes')
s+=line(398,206,627,206)
s+=text(517,170,'copy line',24,BLUE,'bold')
s+=text(530,350,'L1 can now return A[5] to the CPU',27,DARK,'bold')
save('cache-line-fill',s)

# DRAM bank and command visuals. Row buffers belong to individual banks.
s=text(530,62,'Two banks, two independent open-row states',31,DARK,'bold')
for x,title,open_row in ((65,'Bank 0','row 4'),(550,'Bank 1','row 2')):
 s+=f'<rect x="{x}" y="86" width="445" height="296" rx="16" fill="{SOFT}" stroke="{BLUE}" stroke-width="3"/>'
 s+=text(x+222,122,title,30,DARK,'bold')
 for j,row in enumerate(('row 0','row 2','row 4')):
  y=143+j*42
  col='#b9e6ed' if row==open_row else '#f9fbfc'
  s+=f'<rect x="{x+36}" y="{y}" width="372" height="34" rx="7" fill="{col}" stroke="{BLUE}" stroke-width="2"/>'
  s+=text(x+222,y+25,row,23,DARK,'bold' if row==open_row else 'normal')
 s+=f'<rect x="{x+36}" y="291" width="372" height="56" rx="7" fill="#b9e6ed" stroke="{BLUE}" stroke-width="3"/>'
 s+=text(x+222,327,'row buffer: '+open_row,23,DARK,'bold')
save('dram-bank-row-buffers',s)

s=box(45,128,284,160,'ACT',sub='open row 4 in bank 0')
s+=box(388,128,284,160,'READ / CAS',sub='select column in row 4')
s+=box(731,128,284,160,'PRE',sub='close row 4')
s+=line(337,207,371,207)+line(680,207,714,207)
s+=text(530,365,'The row can stay open for more than one READ',23,GRAY)
save('dram-command-roles',s)

def timeline_mark(x,cmd):
 return (f'<path d="M{x} 205 V307" stroke="{DARK}" stroke-width="3"/>'
         +text(x,184,cmd,26,DARK,'bold'))
def timing_interval(x,w,name,fill='#b9e6ed'):
 return (f'<rect x="{x}" y="236" width="{w}" height="38" rx="6" fill="{fill}"/>'
         +text(x+w/2,263,name,23,DARK,'bold'))
def timing_axis():
 return f'<path d="M65 308 H1005" stroke="{GRAY}" stroke-width="3" marker-end="url(#arrow)"/>'

s=text(530,71,'Bank 0 already has row 4 open',32,DARK,'bold')
s+=timing_axis()+timeline_mark(153,'READ / CAS')+timeline_mark(839,'first data')
s+=timing_interval(174,645,'tCL: column to data')
s+=text(530,375,'No PRE or ACT is needed for this request',24,GRAY)
save('dram-timeline-hit',s)

s=text(530,71,'Bank 0 starts closed',32,DARK,'bold')
s+=timing_axis()+timeline_mark(128,'ACT row 4')+timeline_mark(528,'READ / CAS')+timeline_mark(901,'first data')
s+=timing_interval(151,357,'tRCD: open row')+timing_interval(550,329,'tCL: column to data')
s+=text(530,375,'ACT opens the requested row before READ',24,GRAY)
save('dram-timeline-closed',s)

s=text(530,71,'Bank 0 has row 4 open; request is for row 9',29,DARK,'bold')
s+=timing_axis()+timeline_mark(104,'PRE row 4')+timeline_mark(371,'ACT row 9')
s+=timeline_mark(654,'READ / CAS')+timeline_mark(945,'first data')
s+=timing_interval(126,220,'tRP','#f2ca9d')
s+=timing_interval(393,236,'tRCD')
s+=timing_interval(676,244,'tCL')
s+=text(530,375,'PRE may first have to wait for tRAS or an earlier READ',23,GRAY)
save('dram-timeline-conflict',s)

# gem5 DDR3_1600_8x8 timing interface: tCL=tRCD=tRP=13.75 ns.
# https://gem5.googlesource.com/public/gem5/+/master/src/python/gem5/components/memory/dram_interfaces/ddr3.py
# Only the idealized minimum command path is added here; this is not a runtime measurement.
t_cl_ns = t_rcd_ns = t_rp_ns = 13.75
s=text(530,49,'Idealized DDR3-1600 command delay to first data',29,DARK,'bold')
bar_defs=[
 (104,'Open-row hit',['tCL'],f'{t_cl_ns:.2f} ns'),
 (205,'Closed-row miss',['tRCD','tCL'],f'{t_rcd_ns+t_cl_ns:.2f} ns'),
 (306,'Conflict miss',['tRP','tRCD','tCL'],f'{t_rp_ns+t_rcd_ns+t_cl_ns:.2f} ns'),
]
bar_colors={'tRP':'#f2ca9d','tRCD':'#b9e6ed','tCL':BLUE}
for y,label,parts,total in bar_defs:
 s+=text(250,y+21,label,24,DARK,'bold','end')
 for j,part in enumerate(parts):
  x=289+j*186
  s+=f'<rect x="{x}" y="{y-13}" width="182" height="48" rx="6" fill="{bar_colors[part]}"/>'
  s+=text(x+91,y+19,part,23,'white' if part=='tCL' else DARK,'bold')
 s+=text(915,y+21,total,25,DARK,'bold')
s+=text(530,397,'Minimum command path; excludes queuing, transfer, and CPU/cache time',22,GRAY)
save('dram-latency-comparison',s)

print('Generated',len(list(R.glob('*.svg'))),'SVG diagrams')
