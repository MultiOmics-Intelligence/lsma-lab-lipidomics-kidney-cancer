import re
AC={'myristoyl':'14:0','myristoleoyl':'14:1','pentadecanoyl':'15:0','palmitoyl':'16:0','palmitoleoyl':'16:1','heptadecanoyl':'17:0','stearoyl':'18:0','oleoyl':'18:1','linoleoyl':'18:2','eicosatrienoyl':'20:3','arachidonoyl':'20:4','arachidonyl':'20:4','docosapentaenoyl':'22:5','docosahexaenoyl':'22:6'}
HG={'glycerophosphocholine':'LPC','glycerophosphoethanolamine':'LPE','glycerophosphoinositol':'LPI','glycerophosphoserine':'LPS'}
CAR={'acetyl':'2:0','propionyl':'3:0','butyryl':'4:0','valeryl':'5:0','hexanoyl':'6:0','octanoyl':'8:0','lauryl':'12:0','myristoyl':'14:0','palmitoyl':'16:0','stearoyl':'18:0','oleoyl':'18:1'}
FIXED={'1-palmitoylplasmenylethanolamine*':'LPE P-16:0','palmitoyl sphingomyelin':'SM d18:1/16:0','sphingosine':'SPH d18:1','sphinganine':'SPH d18:0','phytosphingosine':'SPH t18:0','cholesterol':'cholesterol',
 '15-methylpalmitate (isobar with 2-methylpalmitate)':'FA 17:0 (branched)','13-HODE + 9-HODE':'FA 18:2;O (HODE)','16-hydroxypalmitate':'FA 16:0;O (16-hydroxy)','2-hydroxypalmitate':'FA 16:0;O (2-hydroxy)',
 '3-hydroxydecanoate':'FA 10:0;O (3-hydroxy)','3-hydroxyoctanoate':'FA 8:0;O (3-hydroxy)','5-HETE':'FA 20:4;O (5-HETE)','5-oxoETE':'FA 20:4;O (5-oxo-ETE)',
 'linolenate [alpha or gamma; (18:3n3 or 6)]':'FA 18:3','dihomo-linolenate (20:3n3 or n6)':'FA 20:3','eicosenoate (20:1n9 or 11)':'FA 20:1','docosapentaenoate (n3 DPA; 22:5n3)':'FA 22:5 (n-3)','docosapentaenoate (n6 DPA; 22:5n6)':'FA 22:5 (n-6)'}
def shorthand(name, sub):
    n=name.strip()
    if n in FIXED: return FIXED[n]
    if sub=='Lysolipid':
        m=re.match(r'^([12])-([a-z]+?)(glycerophospho\w+)\*?$',n)
        if m and m.group(2) in AC and m.group(3) in HG:
            c=AC[m.group(2)]; return f"{HG[m.group(3)]} {c}/0:0" if m.group(1)=='1' else f"{HG[m.group(3)]} 0:0/{c}"
    if sub=='Monoacylglycerol':
        m=re.match(r'^([12])-([a-z]+?)glycerol',n)
        if m and m.group(2) in AC:
            c=AC[m.group(2)]; return f"MG {c}/0:0/0:0" if m.group(1)=='1' else f"MG 0:0/{c}/0:0"
    if sub and ('carnitine' in sub.lower() or 'Fatty acid metabolism' in sub):
        m=re.match(r'^([a-z]+)carnitine$',n)
        if m and m.group(1) in CAR: return f"CAR {CAR[m.group(1)]}"
    if sub in ('Long chain fatty acid','Medium chain fatty acid','Essential fatty acid'):
        m=re.search(r'\((?:[A-Za-z ]+; )?(\d+:\d+)(n\d+)?',n)
        if m: return f"FA {m.group(1)}"+(f" (n-{m.group(2)[1:]})" if m.group(2) else '')
    return None
