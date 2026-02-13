#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False)

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    C1 = net.addHost('C1', cls=Node, ip=None)
    C1.cmd('sysctl -w net.ipv4.ip_forward=0')
    D1 = net.addHost('D1', cls=Node, ip=None)
    D1.cmd('sysctl -w net.ipv4.ip_forward=0')
    D2 = net.addHost('D2', cls=Node, ip=None)
    D2.cmd('sysctl -w net.ipv4.ip_forward=0')
    A1 = net.addHost('A1', cls=Node, ip=None)
    A1.cmd('sysctl -w net.ipv4.ip_forward=0')
    A2 = net.addHost('A2', cls=Node, ip=None)
    A2.cmd('sysctl -w net.ipv4.ip_forward=0')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='192.168.0.1/24', defaultRoute='via 192.168.0.254')
    h2 = net.addHost('h2', cls=Host, ip='192.168.1.1/24', defaultRoute='via 192.168.1.254')

    info( '*** Add links\n')
    net.addLink(C1, D1)
    net.addLink(C1, D2)
    net.addLink(D1, A1)
    net.addLink(D2, A2)
    net.addLink(D1, A2)
    net.addLink(D2, A1)
    net.addLink(A1, h1)
    net.addLink(A2, h2)

    A1.setIP('192.168.0.254/24', intf='A1-eth2')
    A2.setIP('192.168.1.254/24', intf='A2-eth2')

    C1.cmd('ip link set C1-eth0 netns C1')
    C1.cmd('ip link set C1-eth1 netns C1')
    C1.cmd('ip link set C1-eth0 name eth0')
    C1.cmd('ip link set C1-eth1 name eth1')

    D1.cmd('ip link set D1-eth0 netns D1')
    D1.cmd('ip link set D1-eth1 netns D1')
    D1.cmd('ip link set D1-eth2 netns D1')
    D1.cmd('ip link set D1-eth0 name eth0')
    D1.cmd('ip link set D1-eth1 name eth1')
    D1.cmd('ip link set D1-eth2 name eth2')

    D2.cmd('ip link set D2-eth0 netns D2')
    D2.cmd('ip link set D2-eth1 netns D2')
    D2.cmd('ip link set D2-eth2 netns D2')
    D2.cmd('ip link set D2-eth0 name eth0')
    D2.cmd('ip link set D2-eth1 name eth1')
    D2.cmd('ip link set D2-eth2 name eth2')

    A1.cmd('ip link set A1-eth0 netns A1')
    A1.cmd('ip link set A1-eth1 netns A1')
    A1.cmd('ip link set A1-eth2 netns A1')
    A1.cmd('ip link set A1-eth0 name eth0')
    A1.cmd('ip link set A1-eth1 name eth1')
    A1.cmd('ip link set A1-eth2 name eth2')

    A2.cmd('ip link set A2-eth0 netns A2')
    A2.cmd('ip link set A2-eth1 netns A2')
    A2.cmd('ip link set A2-eth2 netns A2')
    A2.cmd('ip link set A2-eth0 name eth0')
    A2.cmd('ip link set A2-eth1 name eth1')
    A2.cmd('ip link set A2-eth2 name eth2')

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

