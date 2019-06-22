from mininet.topo import Topo
from mininet.net import Mininet
#from mininet.link import TCLink
#from mininet.node import CPULimitedHost
#from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.node import Node

#from mininet.cli import CLI

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
	
	#roteador = self.addNode( 'r0', cls=LinuxRouter, ip='10.0.0.1/24' ) 	
        roteador = self.addNode( 'r0', cls=LinuxRouter )
	
	# Criacao dos hosts
        #hostDireita1 = self.addHost( 'Hd1' )
        #hostDireita2 = self.addHost( 'Hd2' )
        #hostDireita3 = self.addHost( 'Hd3' )

	        
	hostDireita1 = self.addHost( 'Hd1', ip='10.0.1.2/24', defaultRoute='via 10.0.1.1/24' )
	hostDireita2 = self.addHost( 'Hd2', ip='10.0.1.3/24', defaultRoute='via 10.0.1.1/24' )
    	hostDireita3 = self.addHost( 'Hd3', ip='10.0.1.4/24', defaultRoute='via 10.0.1.1/24' )


        #hostEsquerda1 = self.addHost( 'He1' )
        #hostEsquerda2 = self.addHost( 'He2' )
        #hostEsquerda3 = self.addHost( 'He3' )
	
	hostEsquerda1 = self.addHost( 'He1', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1/24' )
	hostEsquerda2 = self.addHost( 'He2', ip='10.0.2.3/24', defaultRoute='via 10.0.2.1/24' )
	hostEsquerda3 = self.addHost( 'He3', ip='10.0.2.4/24', defaultRoute='via 10.0.2.1/24' )         

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

	
	# adicao do link entre os switches e o roteador
	self.addLink( switchEsquerda, roteador, intfName2='r0-eth1', params2={ 'ip' : '10.0.2.1/24' } )
	self.addLink( switchDireita, roteador, intfName2='r0-eth2', params2={ 'ip' : '10.0.1.1/24' } )        

        # Adicao do link entre os switches
        #self.addLink( switchEsquerda, switchDireita )
       	#self.addLink( switchEsquerda, switchDireita, bw=0.2, delay='50ms' )
	
def criaTeste():
	"Cria a rede de testes"
	topo = MyTopo()
	rede = Mininet(topo)
	#rede = Mininet(topo, link=TCLink)
	#rede = Mininet( topo, link=TCLink, autoStaticArp=True )
	rede.start()

	#print "Testando as conexoes dos hosts com os switches"
	#dumpNodeConnections(rede.hosts)

	#h1, h4 = rede.getNodeByName('Hd1', 'He1')	
	#rede.iperf( ( h1, h4 ), l4Type='UDP' )
	#rede.pingAll()
	
	info( 'Tabela de roteamento no roteador\n' )
	print rede[ 'r0' ].cmd( 'route' )
	
	rede.pingAll()

	info( 'Tabela de rotemento no roteador\n' )
	print rede[ 'r0' ].cmd( 'route' )
	#CLI( rede )
	
	rede.stop()
	
if __name__ == '__main__':
	setLogLevel('info')
	criaTeste()
#topos = { 'mytopo': ( lambda: MyTopo() ) }

# iperf
# http://mininet.org/api/classmininet_1_1net_1_1Mininet.html
