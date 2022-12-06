# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as rspec
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Only Ubuntu images supported.
imageList = [
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD', 'UBUNTU 20.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD', 'UBUNTU 18.04'),
]

pc.defineParameter("clientNodes", "Number of Client Nodes",
                   portal.ParameterType.INTEGER, 1)

# Variable number of edge nodes.
pc.defineParameter("edgeNodes", "Number of Edge Nodes", portal.ParameterType.INTEGER, 1,
                   longDescription="Number of edge serverledge nodes")

# Variable number of cloud nodes.
pc.defineParameter("cloudNodes", "Number of Cloud Nodes", portal.ParameterType.INTEGER, 1,
                   longDescription="If you specify more then one node, " +
                                   "we will create a lan for you.")

pc.defineParameter("latency", "Latency of the edge-cloud link", portal.ParameterType.LATENCY, 100)

pc.defineParameter("osImage", "Select OS image",
                   portal.ParameterType.IMAGE,
                   imageList[0], imageList)

pc.defineParameter("phystype", "Optional cloud physical node type",
                   portal.ParameterType.STRING, "c6320",
                   longDescription="Specify a physical node type (pc3000,d710,etc) " +
                                   "instead of letting the resource mapper choose for you.")

# Always need this when using parameters
params = pc.bindParameters()

# The NFS network. All these options are required.
nfsLan = request.LAN("edgeLAN")
nfsLan.best_effort = True
nfsLan.vlan_tagging = True
nfsLan.link_multiplexing = True

cloudLan = request.LAN("cloudLAN")
cloudLan.best_effort = True
cloudLan.vlan_tagging = True
cloudLan.link_multiplexing = True

router = request.XenVM("router")
int1 = router.addInterface()
int1.addAddress(rspec.IPv4Address("10.10.1.1", "255.255.255.0"))
nfsLan.addInterface(int1)

int2 = router.addInterface()
int2.addAddress(rspec.IPv4Address("10.10.2.1", "255.255.255.0"))

cmd = "sudo tc qdisc add dev eth2 root netem delay %sms 20ms distribution normal" % str(params.latency)
router.addService(rspec.Execute(shell="bash", command=cmd))

cloudLan.addInterface(int2)

router.disk_image = params.osImage

for i in range(1, params.edgeNodes + 1):
    name = "edge" + str(i)
    node = request.XenVM(name)
    node.disk_image = params.osImage

    node.addService(rspec.Execute(shell="bash", command="wget https://bootstrap.pypa.io/get-pip.py; python3 "
                                                        "get-pip.py; python3 -m pip install --user ansible"))
    node.addService(rspec.Install(url="https://go.dev/dl/go1.19.3.linux-amd64.tar.gz", path="/usr/local"))
    node.addService(rspec.Execute(shell="bash", command="sudo apt-get update; sudo apt-get install -y ca-certificates "
                                                        'curl gnupg lsb-release; echo "export '
                                                        'PATH=$PATH:/usr/local/go/bin" >> $HOME/.profile'))
    node.addService(rspec.Execute(shell="bash", command="curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh "
                                                        "get-docker.sh; sudo usermod -aG docker $USER; newgrp docker"))

    node.addService(rspec.Execute(shell="bash", command="ip route add 10.10.2.0/24 via 10.10.1.1 dev eth1"))
    ip = "10.10.1." + str(i + 1)
    interface = node.addInterface()
    interface.addAddress(rspec.IPv4Address(ip, "255.255.255.0"))
    nfsLan.addInterface(interface)

for i in range(1, params.clientNodes + 1):
    name = "client" + str(i)
    node = request.XenVM(name)
    node.disk_image = params.osImage
    node.addService(rspec.Execute(shell="bash", command="wget https://bootstrap.pypa.io/get-pip.py; python3 "
                                                        "get-pip.py; python3 -m pip install --user ansible"))
    node.addService(rspec.Install(url="https://go.dev/dl/go1.19.3.linux-amd64.tar.gz", path="/usr/local"))
    node.addService(rspec.Execute(shell="bash", command="sudo apt-get update; sudo apt-get install -y ca-certificates "
                                                        'curl gnupg lsb-release; echo "export '
                                                        'PATH=$PATH:/usr/local/go/bin" >> $HOME/.profile'))
    node.addService(rspec.Execute(shell="bash", command="curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh "
                                                        "get-docker.sh; sudo usermod -aG docker $USER; newgrp docker"))

    ip = "10.10.1." + str(100 + i)
    interface = node.addInterface()
    interface.addAddress(rspec.IPv4Address(ip, "255.255.255.0"))
    nfsLan.addInterface(interface)

for i in range(1, params.cloudNodes + 1):
    name = "cloud" + str(i)

    # TODO change
    # node = request.RawPC(name)
    # node.hardware_type = params.phystype
    node = request.XenVM(name)

    node.disk_image = params.osImage

    node.addService(rspec.Execute(shell="bash", command="wget https://bootstrap.pypa.io/get-pip.py; python3 "
                                                        "get-pip.py; python3 -m pip install --user ansible"))
    node.addService(rspec.Install(url="https://go.dev/dl/go1.19.3.linux-amd64.tar.gz", path="/usr/local"))

    node.addService(rspec.Execute(shell="bash", command="ip route add 10.10.1.0/24 via 10.10.2.1 dev eth1"))
    node.addService(rspec.Execute(shell="bash", command="sudo apt-get update; sudo apt-get install -y ca-certificates "
                                                        'curl gnupg lsb-release; echo "export '
                                                        'PATH=$PATH:/usr/local/go/bin" >> $HOME/.profile'))
    node.addService(rspec.Execute(shell="bash", command="curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh "
                                                        "get-docker.sh; sudo usermod -aG docker $USER; newgrp docker"))

    ip = "10.10.2." + str(i + 1)
    interface = node.addInterface()
    interface.addAddress(rspec.IPv4Address(ip, "255.255.255.0"))
    cloudLan.addInterface(interface)

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
