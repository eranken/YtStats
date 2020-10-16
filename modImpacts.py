#!/usr/bin/env python
import ROOT
import math
import json
import argparse
import CombineHarvester.CombineTools.plotting as plot
import CombineHarvester.CombineTools.combine.rounding as rounding

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.AddDirectory(0)

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='input json file')
parser.add_argument('--output', '-o', help='name of the output file to create')
parser.add_argument('--translate', '-t', help='JSON file for remapping of parameter names')
parser.add_argument('--units', default=None, help='Add units to the best-fit parameter value')
parser.add_argument('--per-page', type=int, default=36, help='Number of parameters to show per page')
parser.add_argument('--cms-label', default='Internal', help='Label next to the CMS logo')
parser.add_argument('--transparent', action='store_true', help='Draw areas as hatched lines instead of solid')
parser.add_argument('--checkboxes', action='store_true', help='Draw an extra panel with filled checkboxes')
parser.add_argument('--blind', action='store_true', help='Do not print best fit signal strength')
parser.add_argument('--color-groups', default=None, help='Comma separated list of GROUP=COLOR')
parser.add_argument("--pullDef",  default=None, help="Choose the definition of the pull, see HiggsAnalysis/CombinedLimit/python/calculate_pulls.py for options")
parser.add_argument('--POI', default=None, help='Specify a POI to draw')
args = parser.parse_args()

if args.transparent:
    print 'plotImpacts.py: --transparent is now always enabled, the option will be removed in a future update'

externalPullDef = False
if args.pullDef is not None:
    externalPullDef = True
    import HiggsAnalysis.CombinedLimit.calculate_pulls as CP


def Translate(name, ndict):
#	if name not in ndict:
#		return namei
	mainname = name
	nameend = ''
	if name.endswith('_corr'):
		mainname = name[:-5]
		nameend = name[-5:]
		print name,mainname,nameend
	if '_1' in name:
		mainname = name[:-3]
		nameend=name[-3:]
		print name,mainname,nameend
	if name.startswith('JES'):
		JESnames = name.split('_')
		JESname=JESnames[1]
		mainname = 'Jet energy #font[12]{'+JESname+'}'
	if name.startswith('pdf') and '_as' not in name:
		pdfnames = name.split('_')
		pdfnum = pdfnames[0][3:]
		mainname = 'NNPDF variation '+pdfnum
	if mainname in ndict:
		mainname = ndict[mainname]
	return mainname+nameend
#    return ndict[name] if name in ndict else name


def GetRounded(nom, e_hi, e_lo):
    if e_hi < 0.0:
        e_hi = 0.0
    if e_lo < 0.0:
        e_lo = 0.0
    rounded = rounding.PDGRoundAsym(nom, e_hi if e_hi != 0.0 else 1.0, e_lo if e_lo != 0.0 else 1.0)
    s_nom = rounding.downgradePrec(rounded[0],rounded[2])
    s_hi = rounding.downgradePrec(rounded[1][0][0],rounded[2]) if e_hi != 0.0 else '0'
    s_lo = rounding.downgradePrec(rounded[1][0][1],rounded[2]) if e_lo != 0.0 else '0'
    return (s_nom, s_hi, s_lo)

# Dictionary to translate parameter names
translate = {'fs':'ME factorization scale',
'bfrag':'b fragmentation',
'tune':'UE tune',
'rs':'ME renormalization scale',
'pu':'Pileup',
'murec':'Muon reconstruction efficiency',
'mutrg':'Muon Trigger Efficiency',
'elrec':'Electron reconstuction efficiency',
'eltrg':'Electron trigger efficiency',
'mtop':'Top quark mass',
'hd':'MC hdamp',
'fsr':'Final state radiation scale',
'isr':'Initial state radiation scale',
'JER':'Jet energy resolution',
'JES':'Jet energy corrections',
'bdec':'b decay',
'flatsys':'flat systematics',
'tt_norm':'t#bar{t} normalization',
'st_norm':'Single top normalization',
'vj_norm':'Drell#kern[0.1]{#font[122]{-}}Yan normalization',
'pdf_as':'NNPDF #alpha_{s} variation',
'btag':'b tagging efficiency',
'ltag':'b tagging miss-ID efficiency',
'EWunc':'Electroweak correction uncertainty',
}

if args.translate is not None:
    with open(args.translate) as jsonfile:
        translate = json.load(jsonfile)

# Load the json output of combineTool.py -M Impacts
data = {}
with open(args.input) as jsonfile:
    data = json.load(jsonfile)

adidata = {}
asidataname = 'impactsB.json'
with open(asidataname) as asifile:
    asidata = json.load(asifile)

print asidata

#print data
# Set the global plotting style
plot.ModTDRStyle(l=0.4, b=0.10, width=(900 if args.checkboxes else 700))

# We will assume the first POI is the one to plot
POIs = [ele['name'] for ele in data['POIs']]
POI = POIs[0]
if args.POI:
    POI = args.POI

for ele in data['POIs']:
    if ele['name'] == POI:
        POI_info = ele
        break

POI_fit = POI_info['fit']

# Sort parameters by largest absolute impact on this POI
#data['params'].pop('r')
print data['params'][0]['name']

for i in range(len(data['params'])):
    if data['params'][i]['name']=='r' or data['params'][i]['name']=='pdf_as_17':
	data['params'].pop(i)
	break


for i in range(len(data['params'])):
    if data['params'][i]['name']=='pdf_as_18':
	data['params'][i]['name']='pdf_as_corr'
for i in range(len(asidata['params'])):
    if asidata['params'][i]['name']=='pdf_as_18':
	asidata['params'][i]['name']='pdf_as_corr'

data['params'].sort(key=lambda x: abs(x['impact_%s' % POI]), reverse=True)

if args.checkboxes:
    cboxes = data['checkboxes']

# Set the number of parameters per page (show) and the number of pages (n)
show = args.per_page
n = int(math.ceil(float(len(data['params'])) / float(show)))

colors = {
    'Gaussian': 1,
    'Poisson': 8,
    'AsymmetricGaussian': 9,
    'Unconstrained': 39,
    'Unrecognised': 2
}
color_hists = {}
color_group_hists = {}

if args.color_groups is not None:
    color_groups = {
        x.split('=')[0]: int(x.split('=')[1]) for x in args.color_groups.split(',')
    }

seen_types = set()

for name, col in colors.iteritems():
    color_hists[name] = ROOT.TH1F()
    plot.Set(color_hists[name], FillColor=col, Title=name)

if args.color_groups is not None:
    for name, col in color_groups.iteritems():
        color_group_hists[name] = ROOT.TH1F()
        plot.Set(color_group_hists[name], FillColor=col, Title=name)

for page in xrange(n):
    canv = ROOT.TCanvas(args.output, args.output)
    n_params = len(data['params'][show * page:show * (page + 1)])
    pdata = data['params'][show * page:show * (page + 1)]
    asipdata = asidata["params"]
    print '>> HELLO Doing page %i, have %i parameters' % (page, n_params)
	
    ROOT.gStyle.SetPadBottomMargin(0.12)

    boxes = []
    for i in xrange(n_params):
        y1 = ROOT.gStyle.GetPadBottomMargin()
        y2 = 1. - ROOT.gStyle.GetPadTopMargin()
        h = (y2 - y1) / float(n_params)
        y1 = y1 + float(i) * h
        y2 = y1 + h
        box = ROOT.TPaveText(0, y1, 1, y2, 'NDC')
	plot.Set(box, TextSize=0.02, BorderSize=0, FillColor=0, TextAlign=12, Margin=0.005)
        if i % 2 == 0:
            box.SetFillColor(18)
        box.AddText('%i' % (n_params - i + page * show))
        box.Draw()
        boxes.append(box)

    # Crate and style the pads
    if args.checkboxes:
        pads = plot.MultiRatioSplitColumns([0.54, 0.24], [0., 0.], [0., 0.])
        pads[2].SetGrid(1, 0)
    else:
        pads = plot.MultiRatioSplitColumns([0.7], [0.], [0.])
    pads[0].SetGrid(1, 0)
    pads[0].SetTickx(1)
    pads[1].SetGrid(1, 0)
    pads[1].SetTickx(1)

    h_pulls = ROOT.TH2F("pulls", "pulls", 6, -2.9, 2.9, n_params, 0, n_params)
    g_pulls = ROOT.TGraphAsymmErrors(n_params)
    g_impacts_hi = ROOT.TGraphAsymmErrors(n_params)
    g_impacts_lo = ROOT.TGraphAsymmErrors(n_params)
    g_impactsA_hi = ROOT.TGraphAsymmErrors(n_params)
    g_impactsA_lo = ROOT.TGraphAsymmErrors(n_params)
    g_check = ROOT.TGraphAsymmErrors()
    g_check_i = 0

    max_impact = 0.

    text_entries = []
    redo_boxes = []
    for p in xrange(n_params):
        i = n_params - (p + 1)
	thisname = pdata[p]['name']
	asipnum = -1
	asipnumfound =False
	while not asipnumfound:
		asipnum +=1
		if asipnum >= len(asipdata)-1:
			print "oh shit", thisname,asipnum
			break
       		if asipdata[asipnum]["name"]==thisname:
 			asipnumfound = True
			print "found it", asipnum		
	pre = pdata[p]['prefit']
        fit = pdata[p]['fit']
        tp = pdata[p]['type']
	seen_types.add(tp)
        if pdata[p]['type'] != 'Unconstrained':
            pre_err_hi = (pre[2] - pre[1])
            pre_err_lo = (pre[1] - pre[0])

            if externalPullDef:
                fit_err_hi = (fit[2] - fit[1])
                fit_err_lo = (fit[1] - fit[0])
                pull, pull_hi, pull_lo = CP.returnPullAsym(args.pullDef,fit[1],pre[1],fit_err_hi,pre_err_hi,fit_err_lo,pre_err_lo)
            else:
                pull = fit[1] - pre[1]
                pull = (pull/pre_err_hi) if pull >= 0 else (pull/pre_err_lo)
                pull_hi = fit[2] - pre[1]
                pull_hi = (pull_hi/pre_err_hi) if pull_hi >= 0 else (pull_hi/pre_err_lo)
                pull_hi = pull_hi - pull
                pull_lo = fit[0] - pre[1]
                pull_lo = (pull_lo/pre_err_hi) if pull_lo >= 0 else (pull_lo/pre_err_lo)
                pull_lo =  pull - pull_lo

            g_pulls.SetPoint(i, pull, float(i) + 0.5)
            g_pulls.SetPointError(
                i, pull_lo, pull_hi, 0., 0.)
        else:
            # Hide this point
            g_pulls.SetPoint(i, 0., 9999.)
            y1 = ROOT.gStyle.GetPadBottomMargin()
            y2 = 1. - ROOT.gStyle.GetPadTopMargin()
            x1 = ROOT.gStyle.GetPadLeftMargin()
            h = (y2 - y1) / float(n_params)
            y1 = y1 + ((float(i)+0.5) * h)
            x1 = x1 + (1 - pads[0].GetRightMargin() -x1)/2.
            s_nom, s_hi, s_lo = GetRounded(fit[1], fit[2] - fit[1], fit[1] - fit[0])
            text_entries.append((x1, y1, '%s^{#plus%s}_{#minus%s}' % (s_nom, s_hi, s_lo)))
            redo_boxes.append(i)
        g_impacts_hi.SetPoint(i, 0, float(i) + 0.5)
        g_impacts_lo.SetPoint(i, 0, float(i) + 0.5)
        g_impactsA_hi.SetPoint(i, 0, float(i) + 0.5)
        g_impactsA_lo.SetPoint(i, 0, float(i) + 0.5)
        if args.checkboxes:
            pboxes = pdata[p]['checkboxes']
            for pbox in pboxes:
                cboxes.index(pbox)
                g_check.SetPoint(g_check_i, cboxes.index(pbox) + 0.5, float(i) + 0.5)
                g_check_i += 1
        imp = pdata[p][POI]
        g_impacts_hi.SetPointError(i, 0, imp[2] - imp[1], 0.5, 0.5)
        g_impacts_lo.SetPointError(i, imp[1] - imp[0], 0, 0.5, 0.5)
        max_impact = max(max_impact, abs(imp[1] - imp[0]), abs(imp[2] - imp[1]))
        col = colors.get(tp, 2)
        if args.color_groups is not None and len(pdata[p]['groups']) == 1:
            col = color_groups.get(pdata[p]['groups'][0], 1)
	thisname = pdata[p]['name']
        impA = asipdata[asipnum][POI]
        max_impact = max(max_impact, abs(impA[1] - impA[0]), abs(impA[2] - impA[1]))
	if impA[2]-impA[1]>0:
        	g_impactsA_hi.SetPointError(i, 0, impA[2] - impA[1], 0.0, 0.0)
        	g_impactsA_lo.SetPointError(i, impA[1] - impA[0], 0, 0.0, 0.0)
	else:
        	g_impactsA_hi.SetPointError(i,  impA[1] - impA[2],0, 0.0, 0.0)
        	g_impactsA_lo.SetPointError(i, 0, impA[0] - impA[1],  0.0, 0.0)

	thisname = Translate(thisname,translate)
	thisname = thisname.replace('_16',' (2016)')
	thisname = thisname.replace('_17',' (2017)')
	thisname = thisname.replace('_18',' (2018)')
	thisname = thisname.replace('flatsys','flat')
	thisname = thisname.replace('_corr',' (correlated)')
       	h_pulls.GetYaxis().SetBinLabel(
            i + 1, ('#color[%i]{%s}'% (col, thisname)))
       #	h_pulls.GetYaxis().SetLabelSize(0.5)
    # Style and draw the pulls histo
    if externalPullDef:
        plot.Set(h_pulls.GetXaxis(), TitleSize=0.04, LabelSize=0.03, Title=CP.returnTitle(args.pullDef))
    else:
        plot.Set(h_pulls.GetXaxis(), TitleSize=0.04, LabelSize=0.03, Title='(#hat{#theta}-#theta_{0})/#Delta#theta')

    plot.Set(h_pulls.GetYaxis(), LabelSize=0.03, TickLength=0.0)
    h_pulls.GetYaxis().LabelsOption('v')
    h_pulls.Draw()

    for i in redo_boxes:
        newbox = boxes[i].Clone()
        newbox.Clear()
        newbox.SetY1(newbox.GetY1()+0.005)
        newbox.SetY2(newbox.GetY2()-0.005)
        newbox.SetX1(ROOT.gStyle.GetPadLeftMargin()+0.001)
        newbox.SetX2(0.7-0.001)
        newbox.Draw()
        boxes.append(newbox)
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextFont(42)
    latex.SetTextSize(0.2)
    latex.SetTextAlign(22)
    for entry in text_entries:
        latex.DrawLatex(*entry)

    # Go to the other pad and draw the impacts histo
    pads[1].cd()
    if max_impact == 0.: max_impact = 1E-6  # otherwise the plotting gets screwed up
    if max_impact > .9: max_impact = .5
    h_impacts = ROOT.TH2F(
        "impacts", "impacts", 6, -max_impact * 1.06, max_impact * 1.06, n_params, 0, n_params)
    plot.Set(h_impacts.GetXaxis(), LabelSize=0.03, TitleSize=0.04, Ndivisions=505, Title=
        '#lower[0.2]{#Delta}#hat{#lower[0.2]{Y}}_{t}')
#        '#Delta#hat{%s}' % (Translate(POI, translate)))
    plot.Set(h_impacts.GetYaxis(), LabelSize=0, TickLength=0.0)
    h_impacts.Draw()
    
    pads[0].cd()
    xpos = ROOT.gPad.GetLeftMargin()
    xposR = 1-ROOT.gPad.GetRightMargin()
    ypos = 1.-ROOT.gPad.GetTopMargin()+0.01
    lx = ROOT.TLatex(0., 0., 'Z')
    lx.SetNDC(True)
    lx.SetTextAlign(13)
    lx.SetTextFont(42)
    lx.SetTextSize(0.04)
    lx.SetTextColor(16)
    lx.DrawLatex(0.014, .99, 'arXiv:2009.07123')


    if args.checkboxes:
        pads[2].cd()
        h_checkboxes = ROOT.TH2F(
            "checkboxes", "checkboxes", len(cboxes), 0, len(cboxes), n_params, 0, n_params)
        for i, cbox in enumerate(cboxes):
            h_checkboxes.GetXaxis().SetBinLabel(i+1, Translate(cbox, translate))
        plot.Set(h_checkboxes.GetXaxis(), LabelSize=0.03, LabelOffset=0.002)
        h_checkboxes.GetXaxis().LabelsOption('v')
        plot.Set(h_checkboxes.GetYaxis(), LabelSize=0, TickLength=0.0)
        h_checkboxes.Draw()
        # g_check.SetFillColor(ROOT.kGreen)
        g_check.Draw('PSAME')

    # Back to the first pad to draw the pulls graph
    pads[0].cd()
    plot.Set(g_pulls, MarkerSize=0.8, LineWidth=2)
    g_pulls.Draw('PSAME')

    # And back to the second pad to draw the impacts graphs
    pads[1].cd()
    alpha = 0.7

    lo_color = {
        'default': 38,
        'hesse': ROOT.kOrange - 3,
        'robust': ROOT.kGreen + 1
    }
    hi_color = {
        'default': 46,
        'hesse': ROOT.kBlue,
        'robust': ROOT.kAzure - 5
    }
    method = 'default'
    if 'method' in data and data['method'] in lo_color:
        method = data['method']
    g_impacts_hi.SetFillColor(plot.CreateTransparentColor(hi_color[method], alpha))
    g_impacts_hi.SetLineWidth(0)
    g_impacts_lo.SetLineWidth(0)
    g_impacts_hi.Draw('2SAME')
    g_impacts_lo.SetFillColor(plot.CreateTransparentColor(lo_color[method], alpha))
    g_impacts_lo.Draw('2SAME')
    g_impactsA_hi.SetFillColor(ROOT.kBlack)
    g_impactsA_hi.SetLineWidth(2)
    g_impactsA_hi.SetLineStyle(1)
    g_impactsA_hi.SetMarkerSize(0)
    #g_impactsA_hi.SetLineColor(plot.CreateTransparentColor(hi_color[method], 1))
    g_impactsA_hi.SetLineColor(ROOT.kRed+1)
    g_impactsA_hi.SetFillStyle(3004)
    
    g_impactsA_hi.Draw('E SAME')
    g_impactsA_lo.SetFillColor(ROOT.kBlack)
    g_impactsA_lo.SetLineColor(ROOT.kAzure+4)
    g_impactsA_lo.SetLineStyle(1)
    g_impactsA_lo.SetLineWidth(2)
    g_impactsA_lo.SetMarkerSize(0)
    g_impactsA_lo.SetFillStyle(3004)
    g_impactsA_lo.Draw('E SAME')
    pads[1].RedrawAxis()
    pads[1].RedrawAxis()

    pullLegend = ROOT.TLegend(0.002, 0.045, 0.102, 0.085, '', 'NBNDC')
    legend =     ROOT.TLegend(0.08, 0.005, 0.5, 0.085, '', 'NBNDC')
    legend.SetFillStyle(0)
    
    legend.SetNColumns(2)
    pullLegend.AddEntry(g_pulls, 'Pull', 'LP')
    pullLegend.SetMargin(0.4)
    legend.AddEntry(g_impacts_hi, '+1#sigma Impact', 'F')
    legend.AddEntry(g_impacts_lo, '-1#sigma Impact', 'F')
    legend.AddEntry(g_impactsA_hi, '+1#sigma Impact', 'l')
    legend.AddEntry(g_impactsA_lo, '-1#sigma Impact (expected)', 'l')
    pullLegend.Draw()
    legend.Draw()

    leg_width = pads[0].GetLeftMargin() - 0.01
    if args.color_groups is not None:
        legend2 = ROOT.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
        legend2.SetNColumns(2)
        for name, h in color_group_hists.iteritems():
            legend2.AddEntry(h, Translate(name, translate), 'F')
        legend2.Draw()
    elif len(seen_types) > 1:
        legend2 = ROOT.TLegend(0.01, 0.94, leg_width, 0.99, '', 'NBNDC')
        legend2.SetNColumns(2)
        for name, h in color_hists.iteritems():
            if name == 'Unrecognised': continue
            legend2.AddEntry(h, name, 'F')
        legend2.Draw()

    plot.DrawCMSLogo(pads[0], 'CMS', args.cms_label, 0, 0.25, 0.00, 0.00)
    s_nom, s_hi, s_lo = GetRounded(POI_fit[1], POI_fit[2] - POI_fit[1], POI_fit[1] - POI_fit[0])
    if not args.blind:
        plot.DrawTitle(pads[1], '#hat{%s} = %s^{#plus%s}_{#minus%s}%s' % (
            '#lower[0.2]{Y}_{#lower[-0.1]{t}}', s_nom, s_hi, s_lo,
            #Translate(POI, translate), s_nom, s_hi, s_lo,
            '' if args.units is None else ' '+args.units), 3, 0.27)
    extra = ''
    if page == 0:
        extra = '('
    if page == n - 1:
        extra = ')'
    canv.Print('.pdf%s' % extra)
