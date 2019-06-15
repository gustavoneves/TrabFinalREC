from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class MyTopo( Topo ):
    def __init__( self ):

        # Initialize topology
        Topo.__init__( self )

        # Criacao dos hosts
        hostDireita1 = self.addHost( 'Hd1' )
        hostDireita2 = self.addHost( 'Hd2' )
        hostDireita3 = self.addHost( 'Hd3' )
        
        hostEsquerda1 = self.addHost( 'He1' )
        hostEsquerda2 = self.addHost( 'He2' )
        hostEsquerda3 = self.addHost( 'He3' )
        
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
        
        # Adicao do link entre os switches
        #self.addLink( switchEsquerda, switchDireita )
       	self.addLink( switchEsquerda, switchDireita, bw=0.2, delay='50ms' )
	
def criaTeste():
	"Cria a rede de testes"
	topo = MyTopo()
	#rede = Mininet(topo)
	#rede = Mininet(topo, link=TCLink)
	rede = Mininet( topo, link=TCLink, autoStaticArp=True )
	rede.start()

	print "Testando as conexoes dos hosts com os switches"
	dumpNodeConnections(rede.hosts)

	h1, h4 = rede.getNodeByName('Hd1', 'He1')	
	rede.iperf( ( h1, h4 ), l4Type='UDP' )
	#rede.pingAll()
	rede.stop()
	
if __name__ == '__main__':
	setLogLevel('info')
	criaTeste()
#topos = { 'mytopo': ( lambda: MyTopo() ) }

# iperf
# http://mininet.org/api/classmininet_1_1net_1_1Mininet.html
