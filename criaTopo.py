from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.node import Node

from mininet.cli import CLI

import time

class LinuxRouter( Node ):
	"Habilitando o forwarding"
	
	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	def terminate ( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self ).terminate()
		

class MyTopo( Topo ):
    def __init__( self ):

        # Initialize topology
        Topo.__init__( self )
	 	
        roteadorEsquerda = self.addNode( 'r0', cls=LinuxRouter, ip='10.0.1.1/24' )
	
	roteadorDireita = self.addNode( 'r1', cls=LinuxRouter, ip='10.0.2.1/24' )
	
	# Criacao dos hosts      
	hostDireita1 = self.addHost( 'Hd1', ip='10.0.1.2/24', defaultRoute='via 10.0.1.1' )
	hostDireita2 = self.addHost( 'Hd2', ip='10.0.1.3/24', defaultRoute='via 10.0.1.1' )
    	hostDireita3 = self.addHost( 'Hd3', ip='10.0.1.4/24', defaultRoute='via 10.0.1.1' )
	
	hostEsquerda1 = self.addHost( 'He1', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1' )
	hostEsquerda2 = self.addHost( 'He2', ip='10.0.2.3/24', defaultRoute='via 10.0.2.1' )
	hostEsquerda3 = self.addHost( 'He3', ip='10.0.2.4/24', defaultRoute='via 10.0.2.1' )         

        # Criacao dos switches
        switchDireita = self.addSwitch( 'S1' )
        switchEsquerda = self.addSwitch( 'S2' )

        # Adicao dos links da direita
        self.addLink( hostDireita1, switchDireita )
        self.addLink( hostDireita2, switchDireita )
        self.addLink( hostDireita3, switchDireita )        

        # Adicao dos links da esquerda
        self.addLink( hostEsquerda1, switchEsquerda )
        self.addLink( hostEsquerda2, switchEsquerda )
        self.addLink( hostEsquerda3, switchEsquerda )

	
	# adicao do link entre os switches e os roteadores     

	self.addLink ( switchEsquerda, roteadorEsquerda, intfName2='r0-eth1', maxq=15 )
	self.addLink ( switchDireita, roteadorDireita, intfName2='r1-eth1', maxq=20 )

        
	# link entre os roteadores
	self.addLink ( roteadorEsquerda, roteadorDireita, intfName1='r0-eth0', intfName2='r1-eth0', bw=0.2, delay='50ms' )
	
def criaTeste():
	"Cria a rede de testes"
	topo = MyTopo()
	#rede = Mininet(topo)
	rede = Mininet(topo, link=TCLink)
	#rede = Mininet( topo, link=TCLink, autoStaticArp=True )
	rede.start()
	
	rede[ 'r0' ].cmd('ifconfig r0-eth1 10.0.2.1 broadcast 10.0.2.255 netmask 255.255.255.0')
	rede[ 'r1' ].cmd('ifconfig r1-eth1 10.0.1.1 broadcast 10.0.1.255 netmask 255.255.255.0')

	rede[ 'r0' ].cmd('ifconfig r0-eth0 10.0.3.1 broadcast 10.0.3.255 netmask 255.255.255.0')
	rede[ 'r1' ].cmd('ifconfig r1-eth0 10.0.3.2 broadcast 10.0.3.255 netmask 255.255.255.0')


	rede[ 'r0' ].cmd( 'ip route add to 10.0.1.0/24 via 10.0.3.2' )
	rede[ 'r1' ].cmd( 'ip route add to 10.0.2.0/24 via 10.0.3.1' )
	
	
	# porta reno
	rede[ 'Hd1' ].cmd( 'iperf -s -p 5050 &' )
	
	# porta vegas 
	rede[ 'Hd1' ].cmd( 'iperf -s -p 3030 &')
	
	rede[ 'He3' ].cmd( 'modprobe tcp-vegas' )
	
	# tranferencia 1 RENO / RENO
	saida1_arq300 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 5050 -F arq300 -Z reno -f K' )
	saida1_arq1 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 3030 -F arq1 -Z reno -f K' )
	
	time.sleep(1.25)

	# transferencia 2 RENO / VEGAS
	saida2_arq300 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 5050 -F arq300 -Z reno -f K' )
	saida2_arq1 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 3030 -F arq1 -Z vegas -f K' )
	
	time.sleep(1.25)

	# transferencia 3 VEGAS / RENO
	saida3_arq300 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 5050 -F arq300 -Z vegas -f K' )
	saida3_arq1 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 3030 -F arq1 -Z reno -f K' )

	time.sleep(1.25)

	# transferencia 4 VEGAS / VEGAS
	saida4_arq300 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 5050 -F arq300 -Z vegas -f K' )
	saida4_arq1 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 3030 -F arq1 -Z vegas -f K' ) 
	
	
	f = open("saida1_arq300.txt", "a")
	f.write(saida1_arq300)
	f.close()

	f = open("saida1_arq1.txt", "a")
	f.write(saida1_arq1)
	f.close()



	f = open("saida2_arq300.txt", "a")
	f.write(saida2_arq300)
	f.close()
	
	f =open("saida2_arq1.txt", "a")
	f.write(saida2_arq1)
	f.close()



	f = open("saida3_arq300.txt", "a")
	f.write(saida3_arq300)
	f.close()
	
	f = open("saida3_arq1.txt", "a")
	f.write(saida3_arq1)
	f.close()



	f = open("saida4_arq300.txt", "a")
	f.write(saida4_arq300)
	f.close()
	
	f = open("saida4_arq1.txt", "a")
	f.write(saida4_arq1)
	f.close()

# invertendo a ordem de envio
# tranferencia 1 RENO / RENO
	saida1_invertida_arq1 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 5050 -F arq1 -Z reno -f K' )
	saida1_invertida_arq300 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 3030 -F arq300 -Z reno -f K' )
	
	time.sleep(1.25)

	# transferencia 2 RENO / VEGAS
	saida2_invertida_arq1 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 5050 -F arq1 -Z reno -f K' )
	saida2_invertida_arq300 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 3030 -F arq300 -Z vegas -f K' )
	
	time.sleep(1.25)

	# transferencia 3 VEGAS / RENO
	saida3_invertida_arq1 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 5050 -F arq1 -Z vegas -f K' )
	saida3_invertida_arq300 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 3030 -F arq300 -Z reno -f K' )

	time.sleep(1.25)

	# transferencia 4 VEGAS / VEGAS
	saida4_invertida_arq1 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 5050 -F arq1 -Z vegas -f K' )
	saida4_invertida_arq300 = rede[ 'He3' ].cmd( 'iperf -c 10.0.1.2 -p 3030 -F arq300 -Z vegas -f K' ) 
	
	
	f = open("saida1_invertida_arq300.txt", "a")
	f.write(saida1_invertida_arq300)
	f.close()

	f = open("saida1_invertida_arq1.txt", "a")
	f.write(saida1_invertida_arq1)
	f.close()



	f = open("saida2_invertida_arq300.txt", "a")
	f.write(saida2_invertida_arq300)
	f.close()
	
	f =open("saida2_invertida_arq1.txt", "a")
	f.write(saida2_invertida_arq1)
	f.close()



	f = open("saida3_invertida_arq300.txt", "a")
	f.write(saida3_invertida_arq300)
	f.close()
	
	f = open("saida3_invertida_arq1.txt", "a")
	f.write(saida3_invertida_arq1)
	f.close()



	f = open("saida4_invertida_arq300.txt", "a")
	f.write(saida4_invertida_arq300)
	f.close()
	
	f = open("saida4_invertida_arq1.txt", "a")
	f.write(saida4_invertida_arq1)
	f.close()

	CLI( rede )
	
	rede.stop()
	
if __name__ == '__main__':
	setLogLevel('info')
	criaTeste()
