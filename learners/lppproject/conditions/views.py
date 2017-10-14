from django.shortcuts import render
from .models import condPost,rulePost
from operator import eq, ne, ge, gt, le, lt
from django.contrib import messages
from datetime import date, datetime

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y/%m/%d')
        return True
    except ValueError:
        return False

def cond_index(request):
    return render(request, 'conditions/index.html')

def go_admin(request):
    return render(request)

def cond_home(request):
    return render(request, 'conditions/index.html')

def cond_enq(request):
    fields = condPost.objects.order_by().values_list('field',flat=True).distinct()
    opers = condPost.objects.order_by().values_list('oper', flat=True).distinct()
    values = condPost.objects.order_by().values_list('valuetext', flat=True).distinct()
    ruleList = {}
    pfield = ""
    poper = ""
    pvalue = ""
    if request.method == "POST":
        field=request.POST.get('fieldDrp','')
        oper=request.POST.get('operDrp','')
        value = request.POST.get('valDrp','')
        fbutton = request.POST.get('filBtn','')
        ebutton = request.POST.get('editBtn', '')
        eobtn = request.POST.get('edtBtn', '')
        newrte30 = ''
        newrte60 = ''
        newrte90 = ''
        ruledata = ''

        if field > '': pfield = field
        if oper > '': poper = oper
        if value > '': pvalue = value


        condName = field + oper + value
        ruleList = {}
        rules = rulePost.objects.all()

        for rule in rules:
            if fbutton == 'Show rules with above condition' :
                condList = rule.ruletext.split(" ")
                if condName in condList:
                    ruleList[rule.ruletext] = [rule.intge30,rule.intge60,rule.intge90]
            elif fbutton == 'Show all rules' :
                ruleList[rule.ruletext] = [rule.intge30, rule.intge60, rule.intge90]

        ruleText = ruledata
        intrte30 = newrte30
        intrte60 = newrte60
        intrte90 = newrte90

        if ebutton > ' ':
            ruleText = ebutton
            ruleData = rulePost.objects.get(ruletext = ruleText)
            intrte30 = ruleData.intge30
            intrte60 = ruleData.intge60
            intrte90 = ruleData.intge90
            return render(request, 'conditions/edit.html', {'ruleText': ruleText, 'intrte30': intrte30, 'intrte60': intrte60, 'intrte90': intrte90})

        if eobtn == "Update":
            comments = request.POST.get('comments', '')
            ruledata = request.POST.get('ruledata', '')
            newrte30 = request.POST.get('intrte30', '')
            newrte60 = request.POST.get('intrte60', '')
            newrte90 = request.POST.get('intrte90', '')
            ruleObj = rulePost.objects.get(ruletext=ruledata.strip())
            ruleObj.comments = comments
            try:
                ruleObj.intge30 = int(newrte30)
                ruleObj.intge60 = int(newrte60)
                ruleObj.intge90 = int(newrte90)
                ruleObj.save()
                upmsg = "Update is successful"
            except ValueError:
                upmsg = "Please enter proper interest rate"

            ruleText = ruledata
            intrte30 = newrte30
            intrte60 = newrte60
            intrte90 = newrte90

            return render(request, 'conditions/edit.html',{'ruleText':ruleText,'intrte30':intrte30,'intrte60':intrte60,'intrte90':intrte90,'upmsg':upmsg})

        if eobtn == "Delete":
            ruledata = request.POST.get('ruledata', '')
            ruleObj = rulePost.objects.get(ruletext=ruledata.strip())
            ruleObj.delete()

            upmsg = "This rule is deleted"

            ruleText = ruledata
            intrte30 = newrte30
            intrte60 = newrte60
            intrte90 = newrte90

            return render(request, 'conditions/edit.html',{'ruleText':ruleText,'intrte30':intrte30,'intrte60':intrte60,'intrte90':intrte90,'upmsg':upmsg})

    return render(request, 'conditions/enquire.html',
                          {'fields': fields, 'opers': opers, 'values': values, 'pfield': pfield, 'poper': poper, 'pvalue': pvalue,'ruleList': ruleList})

def cond_updt(request):
    fields = condPost.objects.order_by().values_list('field', flat=True).distinct()
    names = condPost.objects.order_by().values_list('name', flat=True).distinct()
    ruletexts = rulePost.objects.order_by().values_list('ruletext', flat=True).distinct()
    condLists = condPost.objects.all()
    listCond = []
    message = ""
    ruleText = ""
    valMsg = ""
    valsw = "Y"
    pfield =""
    popvl = ""
    psbtn = ""

    if request.method == "POST":
        field = request.POST.get('fieldDrp','')
        newField = request.POST.get('newField','')
        newOper = request.POST.get('operDrp','')
        newValue = request.POST.get('newvalue','')
        rulearea = request.POST.get('ruleArea', '')
        button = request.POST.get('shwBtn', '')
        sbuttons = request.POST.get('shwBtns', '')
        rbutton = request.POST.get('filBtn', '')
        intrst30 = request.POST.get('intge30', '')
        intrst60 = request.POST.get('intge60', '')
        intrst90 = request.POST.get('intge90', '')
        psbtn = request.POST.get('tstvl', '')

        pfield = field
        popvl = newOper

        if sbuttons == '':
            print(psbtn)
            sbuttons = psbtn

        if button == 'Insert above condition':
            condObj = condPost()
            condObj.name = newField.strip() + newOper.strip() + newValue.strip()
            condObj.field = newField.strip()
            condObj.oper = newOper.strip()
            condObj.valuetext = newValue.strip()

            if condObj.field > '' and condObj.valuetext > '':
                if condObj.name in names:
                    message = "Condition already exist"
                elif ' ' in condObj.field:
                    message = "Spaces not allowed"
                else:
                    condObj.save()
                    message = "Condition is inserted"
            else:
                message = "Please insert proper data"

        for condList in condLists:
            if sbuttons == 'Show related conditions':
                psbtn = sbuttons
                if field==condList.field:
                    listCond.append(condList)
            elif sbuttons == 'Show all conditions':
                psbtn = sbuttons
                listCond.append(condList)

        if (rbutton == 'Validate') or (rbutton == 'Insert rule'):
            ruleFields=rulearea.strip().split(" ")
            for ruleField in ruleFields:
                if (ruleField in ['(',')','and','or']) or (ruleField in names):
                    pass
                else:
                    valsw = "N"
            if valsw == "N":
                valMsg = "Please correct the rule"
            else:
                valMsg = "The rule is valid"

            if (rbutton == 'Insert rule') and (valsw == "Y"):
                rulearea = rulearea.strip()
                if rulearea in ruletexts:
                    valMsg = "Rule already exists"
                else:
                    ruleObj = rulePost()
                    ruleObj.ruletext = rulearea
                    try:
                        # ruleObj.ruleInt = int(interest)
                        ruleObj.intge30 = int(intrst30)
                        ruleObj.intge60 = int(intrst60)
                        ruleObj.intge90 = int(intrst90)
                        ruleObj.save()
                        valMsg = "The rule is inserted"
                    except ValueError:
                        valMsg = "Please enter proper interest rate"

        dbutton = request.POST.get('delCBtn', '')
        sbutton = request.POST.get('delTBtn', '')

        if (dbutton == 'Delete selected condition'):
            if sbutton > '':
                condObj = condPost.objects.get(name=sbutton)
                condObj.delete()
                message = "Selected condition is deleted"
            else:
                message = "Please select a condition to delete"

        ruleText = rulearea
    opvls = {"eq":"=","ne":"!=","ge":">=","gt":">","le":"<=","lt":"<"}
    return render(request, 'conditions/update.html',{'psbtn':psbtn,'pfield':pfield,'popvl':popvl,'opvls':opvls,'fields': fields,'listCond':listCond,'message':message,'ruleText':ruleText,'valMsg':valMsg})

def check_condition(lhs, op, rhs):
    return op(lhs, rhs)

def get_lpp(request):
    fields = condPost.objects.order_by().values_list('field', flat=True).distinct()
    conds = condPost.objects.all()
    rules = rulePost.objects.all()
    intText = ""
    expr = {}
    fvalue={}
    condValues = {}
    lrcvdte = []
    lfnldte = []
    # rcvdte = "2017/01/01"
    # fnldte = "2017/01/01"
    rcvdte = ""
    fnldte = ""
    prcvdte = ""
    pfnldte = ""
    minamt = 999

    for field in fields:
        fvalue[field] = ""

    if request.method == "POST":
        rcvdte = request.POST.get('rcvdDte','').strip()
        fnldte = request.POST.get('fnlDte', '').strip()

        if validate(rcvdte) and validate(fnldte):
            lrcvdte = rcvdte.split("/")
            lfnldte = fnldte.split("/")

            prcvdte = rcvdte
            pfnldte = fnldte

            rcvdte = date(int(lrcvdte[0]),int(lrcvdte[1]),int(lrcvdte[2]))
            fnldte = date(int(lfnldte[0]),int(lfnldte[1]),int(lfnldte[2]))

            edays = fnldte - rcvdte

            if edays.days >= 0:
                expr[field] = str(edays.days)
                fvalue[field] = str(edays.days)
                valid_sw = True
            else:
                intText = "Recieved date should be less than finalized date"
                valid_sw = False

            if valid_sw:
                for field in fields:
                    expr[field] = request.POST.get(field, '').strip()
                    fvalue[field] = request.POST.get(field, '').strip()

                for cond in conds:
                    lhs = expr[cond.field]
                    op = eval(cond.oper)
                    rhs = cond.valuetext
                    if lhs.isnumeric():
                        lhs = lhs.zfill(5)
                    if rhs.isnumeric():
                        rhs = rhs.zfill(5)
                    condValues[cond.name] = check_condition(lhs, op, rhs)

                for rule in rules:
                    ruleExpList = rule.ruletext.strip().split(" ")
                    ruleExp = ""
                    for ruleExps in ruleExpList:
                        if ruleExps in ["and","or","(",")"]:
                            ruleExp = ruleExp + ruleExps + " "
                        else:
                            ruleExp = ruleExp + "condValues['" + ruleExps + "'] "

                    if eval(ruleExp):
                        if  edays.days >= 90:
                            days90 = edays.days - 90
                            days60 = 30
                            days30 = 30
                        if edays.days >= 60 and edays.days < 90:
                            days90 = 0
                            days60 = edays.days - 60
                            days30 = 30
                        if edays.days >= 30 and edays.days < 60:
                            days90 = 0
                            days60 = 0
                            days30 = edays.days - 30
                        if edays.days < 30:
                            days90 = 0
                            days60 = 0
                            days30 = 0
                        finalamt = days90*rule.intge90/100 + days60*rule.intge60/100 + days30*rule.intge30/100
                        if finalamt < minamt:
                            minamt = finalamt
                            ruletext = rule.ruletext
                            irte30 = rule.intge30
                            irte60 = rule.intge60
                            irte90 = rule.intge90
                            idays30 = days30
                            idays60 = days60
                            idays90 = days90

                if minamt == 999:
                    intText = "This data didnt hit any LPP rule "
                else:
                    if idays90 > 0:
                        intText = "Based on the rule " + ruletext + ", there is no LPP for 1st 30 days, interest is " + str(irte30) + "% for next 30 days,"+ str(irte60) + "% for following 30 days and interest is "+ str(irte90) + "% for last " + str(idays90) + " days."
                    elif idays60 > 0:
                        intText = "Based on the rule " + ruletext + ", there is no LPP for 1st 30 days, interest is " + str(irte30) + "% for next 30 days," + str(irte60) + "% for following " + str(idays60) + " days."
                    elif idays30 > 0:
                        intText = "Based on the rule " + ruletext + ", there is no LPP for 1st 30 days, interest is " + str(irte30) + "% for following " + str(idays30) + " days."
                    else:
                        intText = "There is no LPP for 1st 30 days"
        else:
            intText = "Please enter proper dates"

    return render(request, 'conditions/getlpp.html', {'intText': intText, 'fvalue': fvalue, 'prcvdte':prcvdte, 'pfnldte':pfnldte})