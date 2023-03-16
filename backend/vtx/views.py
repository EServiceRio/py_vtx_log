from django.shortcuts import render,HttpResponse
from django.views.generic import View
from .drive import *
from .models import Gateway, Node, NodeSetup, Hist, Evento
from django.db.models import Q
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class IndexView(View):
    def get(self,request):
        return render(request,"index.html")

@method_decorator(csrf_exempt, name='dispatch')
def online(request):
    gate = Gateway.objects.all()[0]
    ret = f'{{"dxm_online":"{gate.online}"}}'
    return  HttpResponse(ret)

@method_decorator(csrf_exempt, name='dispatch')
def nodes(request):
    n = Node.objects.all()[0]
    alarm = NodeSetup.objects.all()[0]
    v1=0
    if n.vibraX > alarm.alertVibraX:
        if n.vibraX > alarm.alertVibraXNv2:
            v1 = '2'
        else:
            v1 = '1'
    v2=0
    if n.vibraZ > alarm.alertVibraZ:
        if n.vibraZ > alarm.alertVibraZNv2:
            v2 = '2'
        else:
            v2 = '1'
    v3=0
    if n.vibraX2 > alarm.alertVibraX2:
        if n.vibraX2 > alarm.alertVibraX2Nv2:
            v3 = '2'
        else:
            v3 = '1'
    v4=0
    if n.vibraZ2 > alarm.alertVibraZ2:
        if n.vibraZ2 > alarm.alertVibraZ2Nv2:
            v4 = '2'
        else:
            v4 = '1'
    v5=0
    if n.temp > alarm.alertTemp:
        if n.temp > alarm.alertTempNv2:
            v5 = '2'
        else:
            v5 = '1'
    v6=0
    if n.corrente > alarm.alertCorrente:
        if n.corrente > alarm.alertCorrenteNv2:
            v6 = '2'
        else:
            v6 = '1'
    ret = f'{{"id":{n.id},"name":"{n.name}","estado":"{n.estado}","online":"{n.online}","vibraX":{n.vibraX/1000},"vibraZ":{n.vibraZ/1000},"vibraX2":{n.vibraX2/1000},"vibraZ2":{n.vibraZ2/1000},"temp":{n.temp/20},"corrente":{n.corrente/100},"alerta":[{v1},{v2},{v3},{v4},{v5},{v6}]}}'
    return  HttpResponse(ret)

@method_decorator(csrf_exempt, name='dispatch')
class Filtra(View):
    def post(self,request):
        inis = str(request.POST['ini'])
        fims = str(request.POST['fim'])
        print(f'{inis}')
        print(f'{fims}')
        if inis == '':
            agora = datetime.now()
            inis = f'{agora.year}-{agora.month}-{agora.day}T0:0:0'
            fims = f'{agora.year}-{agora.month}-{agora.day}T23:59:0'
        iniDA=inis.split('T')[0].split('-')
        iniTA=inis.split('T')[1].split(':')
        fimDA=fims.split('T')[0].split('-')
        fimTA=fims.split('T')[1].split(':')
        ini = datetime(int(iniDA[0]),int(iniDA[1]),int(iniDA[2]),int(iniTA[0]),int(iniTA[1]),0)
        fim = datetime(int(fimDA[0]),int(fimDA[1]),int(fimDA[2]),int(fimTA[0]),int(fimTA[1]),0)
        ini += timedelta(hours=3)
        fim += timedelta(hours=3)
        print(f'{ini}')
        print(f'{fim}')
        dadof = Hist.objects.filter(Q(date__gt=ini) & Q(date__lt=fim)).order_by('date')
        strinfy = ""
        
        for hf in dadof:
            hora = int(hf.date.hour)-3
            if hora<0:
                hora+=23  
            hf.date = f'{hora}:{hf.date.minute} {hf.date.day}/{hf.date.month}/{hf.date.year}'
            #strinfy = f'{strinfy}{{"hora":"{hf.date}","X Veloc":{hf.vibraX/1000},"Z Veloc":{hf.vibraZ/1000},"X Acele":{hf.vibraX2/1000},"Z Acele":{hf.vibraZ2/1000},"Temperatura":{hf.temp/20},"Aler X Veloc":{hf.alertVibraX},"Aler Z Veloc":{hf.alertVibraZ},"Aler X Acele":{hf.alertVibraX2},"Aler Z Acele":{hf.alertVibraZ2},"Aler Temper":{hf.alertTemp}}},'
            strinfy = f'{strinfy}{{"hora":"{hf.date}","X Veloc":{hf.vibraX/1000},"Z Veloc":{hf.vibraZ/1000},"Temperatura":{hf.temp/20},"Corrente":{hf.corrente/100},"Aler X Veloc":{hf.alertVibraX},"Aler Z Veloc":{hf.alertVibraZ},"Aler Corrente":{hf.alertCorrente},"Aler Temper":{hf.alertTemp}}},'
        strinfy = "[" + strinfy[:len(strinfy)-1] + "]"
        return HttpResponse(strinfy)
        
@method_decorator(csrf_exempt, name='dispatch')
class Eventos(View):
    def post(self,request):
        inis = str(request.POST['ini'])
        fims = str(request.POST['fim'])
        print(f'{inis}')
        print(f'{fims}')
        if inis == '':
            agora = datetime.now()
            inis = f'{agora.year}-{agora.month}-{agora.day}T0:0:0'
            fims = f'{agora.year}-{agora.month}-{agora.day}T23:59:0'
        iniDA=inis.split('T')[0].split('-')
        iniTA=inis.split('T')[1].split(':')
        fimDA=fims.split('T')[0].split('-')
        fimTA=fims.split('T')[1].split(':')
        ini = datetime(int(iniDA[0]),int(iniDA[1]),int(iniDA[2]),int(iniTA[0]),int(iniTA[1]),0)
        fim = datetime(int(fimDA[0]),int(fimDA[1]),int(fimDA[2]),int(fimTA[0]),int(fimTA[1]),0)
        ini += timedelta(hours=3)
        fim += timedelta(hours=3)
        print(f'{ini}')
        print(f'{fim}')
        dadof = Evento.objects.filter(Q(date__gt=ini) & Q(date__lt=fim)).order_by('date')
        strinfy = ""
        
        for hf in dadof:
            hora = int(hf.date.hour)-3
            if hora<0:
                hora+=23  
            hf.date = f'{hora}:{hf.date.minute} {hf.date.day}/{hf.date.month}/{hf.date.year}'
            strinfy = f'{strinfy}{{"hora":"{hf.date}","Node":"{hf.node}","Tipo":"{hf.tipo}","Evento":"{hf.descricao}"}},'
        strinfy = "[" + strinfy[:len(strinfy)-1] + "]"
        return HttpResponse(strinfy)





def para_dict(obj):
    # Se for um objeto, transforma num dict
    if hasattr(obj, '__dict__'):
        obj = obj.__dict__

    # Se for um dict, lê chaves e valores; converte valores
    if isinstance(obj, dict):
        return { k:para_dict(v) for k,v in obj.items() }
    # Se for uma lista ou tupla, lê elementos; também converte
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [para_dict(e) for e in obj]
    # Se for qualquer outra coisa, usa sem conversão
    else: 
        return obj

class dict_to_obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)

class objectDict(dict):
    def __getattr__(self,name):
        return self.__getitem__(name)
