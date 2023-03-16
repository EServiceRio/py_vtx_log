
from pymodbus.client.sync import ModbusSerialClient as ModbusSerial
from pymodbus.client.sync import ModbusTcpClient as ModbusTcp
from .models import Gateway, Hist, Node, NodeSetup, Evento
from time import sleep
from threading import Thread
from datetime import datetime, timedelta

try:
    gate = Gateway.objects.all()
    print(gate[0])
    devices = Node.objects.all()
    print(devices[0])

except Exception as ex:
    print(f'falha: {str(ex)}')

class Servico():
    __controleRead = True
    statusTcp = 'OffLine'
    statusScript = 'ok'
    execSetup = False
    lendo = False

    def __init__(self, gateway, nodes,):
        self.gate = gateway
        self.nodes = nodes

    def ler(self):
        try:
            for n in self.nodes:
                setup = NodeSetup.objects.get(id=n.id)
                X = self.dxm.read_holding_registers(setup.addrVibraX-1,1,unit=setup.address).registers[0]
                n.vibraX = X
                Z = self.dxm.read_holding_registers(setup.addrVibraZ-1,1,unit=setup.address).registers[0]
                n.vibraZ = Z
                Tp = self.dxm.read_holding_registers(setup.addrTemp-1,1,unit=setup.address).registers[0]
                n.temp = Tp
                mA = self.dxm.read_holding_registers(setup.addrCorrente-1,1,unit=setup.address).registers[0]
                n.corrente = mA
                if n.vibraX == None:
                    e = Evento(node=n,descricao="Gateway OffLine", tipo="Falha")
                    e.save()
                else:
                    if n.vibraX==65535:
                        n.estado = "Desconectado"
                        if n.online:
                            e = Evento(node=n,descricao="Node OffLine", tipo="Falha")
                            e.save()
                        n.online = False
                    else:
                        n.estado = "OK"
                        if n.online == False:
                            e = Evento(node=n,descricao="Node Restabelecido", tipo="Evento")
                            e.save()
                        n.online = True
                    if n.estado!="falha":     
                        alertaVX = setup.alertVibraX*1000   
                        alertaVZ = setup.alertVibraZ*1000 
                        alertaVX2 = setup.alertVibraX2*1000   
                        alertaVZ2 = setup.alertVibraZ2*1000  
                        alertaVXNv2 = setup.alertVibraXNv2*1000   
                        alertaVZNv2 = setup.alertVibraZNv2*1000 
                        alertaVX2Nv2 = setup.alertVibraX2Nv2*1000   
                        alertaVZ2Nv2 = setup.alertVibraZ2Nv2*1000   
                        alertaT = setup.alertTemp*20
                        alertaT2 = setup.alertTempNv2*20
                        alertaC = setup.alertCorrente*100
                        alertaCNv2 = setup.alertCorrenteNv2*100
                        if n.vibraX>alertaVX or n.vibraZ>alertaVZ or n.vibraX>alertaVX2 or n.vibraZ>alertaVZ2 or n.temp>alertaT or n.corrente>alertaC:
                            if n.vibraX>alertaVXNv2 or n.vibraZ>alertaVZNv2 or n.vibraX>alertaVX2Nv2 or n.vibraZ>alertaVZ2Nv2 or n.temp>alertaT2 or n.corrente>alertaCNv2:
                                n.estado = "falha"
                            else:
                                n.estado = "alerta"
                        else:
                            n.estado = "OK"
                        n.save()
            self.gate = Gateway.objects.all()[0]
            self.gate.online = True
            self.gate.save()
            sleep(1)
            return True
        except Exception as ex:
            print(f'falha na leitura 2 - {str(ex)}')
            self.gate = Gateway.objects.all()[0]
            self.gate.online = False
            self.gate.save()
            sleep(2)
            return False

    def _readTCP(self):
        while self.__controleRead== True:
            if self.ler():
                self.statusTcp = 'dxm OnLine'
            else:
                self.statusTcp = 'dxm OffLine'
                sleep(5)
       
    def _setupTCP(self):
        print('setupTcp...')
        self.__controleRead = False
        sleep(4)
        try:
            if self.gate.port.find(".")>0:
                self.dxm = ModbusTcp(host=self.gate.port, port=502)
            else:
                self.dxm = ModbusSerial(method="rtu", port=self.gate.port, timeout=1, boudrate=self.gate.boudrate)
            self.dxm.connect()
            retorno = self.dxm.read_holding_registers(0,1,unit=1)
            if retorno:
                self.statusTcp = 'dxm OnLine'
                self.__controleRead = True
                self.th = Thread(target=self._readTCP)
                self.th.start()    
            else:
                self.statusTcp = 'dxm OffLine'
                sleep(3)
                #if not self.lendo:
                self.__controleRead = True
                self.th = Thread(target=self._readTCP)
                self.th.start()
        except Exception as ex:
            self.statusTcp = 'dxm OffLine'
            print(f'falha no setup:  {str(ex)}')
            sleep(3)
            #if not self.lendo:
            self.__controleRead = True
            self.th = Thread(target=self._readTCP)
            self.th.start()
                
    
    def close(self):
        self.__controleRead = False 
        self.dxm.close()

class Ciclo():
    def __init__(self,node):
        self.ctl_log = True
        self.node = node
        self.Th = Thread(target=self.cicloLog)
    
    def cicloLog(self):
        sleep(10)
        time = 0
        lastEvenX = False
        lastEvenZ = False
        lastEvenXNv2 = False
        lastEvenZNv2 = False
        lastEvenX2 = False
        lastEvenZ2 = False
        lastEvenX2Nv2 = False
        lastEvenZ2Nv2 = False
        lastEvenTemp = False
        lastEvenTemp2 = False
        while self.ctl_log:
            n = self.node
            setup = NodeSetup.objects.get(id=n.id)
            print(f'time: {time}, alvo:{setup.ciclo}')
            print(f'lastX: {lastEvenX}, lastZ: {lastEvenZ}, lastT: {lastEvenTemp}')
            if time > setup.ciclo and self.node.temp<3000:
                h = Hist(
                    node=self.node,vibraX=self.node.vibraX,
                    vibraZ= self.node.vibraZ, temp= self.node.temp,
                    alertVibraX= setup.alertVibraX, alertVibraZ= setup.alertVibraZ,
                    alertTemp= setup.alertTemp, corrente=self.node.corrente,
                    alertCorrente= setup.alertCorrente
                )      
                h.save()
                if n.vibraX>setup.alertVibraX*1000 and n.estado != "Desconectado":
                    if n.vibraX>setup.alertVibraXNv2*1000:
                        if not lastEvenXNv2:
                            e = Evento(node=n,descricao="X Velocidade Muito Alta", tipo="Falha")
                            e.save()
                            lastEvenX=True
                    else:
                        if not lastEvenX:
                            e = Evento(node=n,descricao="X Velocidade Alta", tipo="Alerta")
                            e.save()
                            lastEvenX=True
                else:
                    if lastEvenX or lastEvenXNv2:
                        e = Evento(node=n,descricao="X Velocidade Normalizada", tipo="Evento")
                        e.save()
                    lastEvenX=False
                    lastEvenXNv2=False
                if n.vibraZ>setup.alertVibraZ*1000 and n.estado != "Desconectado": 
                    if n.vibraZ>setup.alertVibraZNv2*1000:
                         if not lastEvenZNv2:
                            e = Evento(node=n,descricao="Z Velocidade Muito Alta", tipo="Falha")
                            e.save()
                            lastEvenZ=True
                    else:
                        if not lastEvenZ:
                            e = Evento(node=n,descricao="Z Velocidade Alta", tipo="Alerta")
                            e.save()
                            lastEvenZ=True
                else:
                    if lastEvenZ or lastEvenZNv2:
                        e = Evento(node=n,descricao="Z Velocidade Normalizada", tipo="Evento")
                        e.save()
                    lastEvenZ=False
                    lastEvenZNv2=False
                

                if n.vibraX>setup.alertVibraX2*1000 and n.estado != "Desconectado":
                    if n.vibraX>setup.alertVibraX2Nv2*1000:
                        if not lastEvenX2Nv2:
                            e = Evento(node=n,descricao="X Aceleração Muito Alta", tipo="Falha")
                            e.save()
                            lastEvenX2=True
                    else:
                        if not lastEvenX2:
                            e = Evento(node=n,descricao="X Acelereção Alta", tipo="Alerta")
                            e.save()
                            lastEvenX2=True
                else:
                    if lastEvenX2 or lastEvenX2Nv2:
                        e = Evento(node=n,descricao="X Aceleração Normalizada", tipo="Evento")
                        e.save()
                    lastEvenX2=False
                    lastEvenX2Nv2=False
                if n.vibraZ>setup.alertVibraZ2*1000 and n.estado != "Desconectado": 
                    if n.vibraZ>setup.alertVibraZ2Nv2*1000:
                         if not lastEvenZ2Nv2:
                            e = Evento(node=n,descricao="Z Aceleração Muito Alta", tipo="Falha")
                            e.save()
                            lastEvenZ2=True
                    else:
                        if not lastEvenZ2:
                            e = Evento(node=n,descricao="Z Aceleração Alta", tipo="Alerta")
                            e.save()
                            lastEvenZ2=True
                else:
                    if lastEvenZ2 or lastEvenZ2Nv2:
                        e = Evento(node=n,descricao="Z Aceleração Normalizada", tipo="Evento")
                        e.save()
                    lastEvenZ2=False
                    lastEvenZ2Nv2=False


                if n.temp>setup.alertTemp*20 and n.estado != "Desconectado":
                    if n.temp>setup.alertTempNv2*20:
                        if not lastEvenTemp2:
                            e = Evento(node=n,descricao="Temperatura Muito Alta", tipo="Falha")
                            e.save()
                            lastEvenTemp2=True
                    else:
                        if not lastEvenTemp:
                            e = Evento(node=n,descricao="Temperatura Alta", tipo="Alerta")
                            e.save()
                            lastEvenTemp=True
                else:
                    if lastEvenTemp or lastEvenTemp2:
                        e = Evento(node=n,descricao="Temperatura Normalizada", tipo="Evento")
                        e.save()
                    lastEvenTemp=False
                    lastEvenTemp2=False
                time=0 
            time+=1
            sleep(1)

    def start(self):
        self.Th.start()

    def close(self):
        self.ctl_log=False

servico = Servico(gate[0],devices)

ciclos = []
for n in devices:
    ciclos.append(Ciclo(n))

def leitu():
    servico._setupTCP()
    for c in ciclos:
        c.start()
    controle = True
    while controle:
        cmd = input()
        if cmd == 'exit':
            for c in ciclos:
                c.close()
            servico.close()
            controle = False
        if cmd == 'sts':
            print(servico.statusTcp)
    print('fim...')




l = Thread(target=leitu)
l.start()