# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
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

pc.defineParameter("phystype",  "Optional cloud physical node type",
                   portal.ParameterType.STRING, "c6320",
                   longDescription="Specify a physical node type (pc3000,d710,etc) " +
                   "instead of letting the resource mapper choose for you.")




# Always need this when using parameters
params = pc.bindParameters()

# The NFS network. All these options are required.
nfsLan = request.LAN("edgeLAN")
nfsLan.best_effort       = True
nfsLan.vlan_tagging      = True
nfsLan.link_multiplexing = True

cloudLan = request.LAN("cloudLAN")
cloudLan.best_effort       = True
cloudLan.vlan_tagging      = True
cloudLan.link_multiplexing = True

"""
for i in range(1, params.clientCount+1):
    node = request.RawPC("node%d" % i)
    node.disk_image = params.osImage
    # Initialization script for the clients
    nfsLan.addInterface(node.addInterface())
    if params.phystype != "":
        node.hardware_type = params.phystype
    if params.localStorage != 0:
        bsName="bs"+str(i)
        bs = node.Blockstore(bsName, "/var/lib/libvirt/images")
        bs.size=str(params.localStorage)+"GB"
"""

for i in range(1, params.edgeNodes+1):
    name = "client" + str(i)
    node = request.XenVM(name)
    node.disk_image = params.osImage
    nfsLan.addInterface(node.addInterface())

for i in range(1, params.clientNodes+1):
    name = "edge" + str(i)
    node = request.XenVM(name)
    node.disk_image = params.osImage
    # Initialization script for the clients
    nfsLan.addInterface(node.addInterface())

for i in range(1, params.cloudNodes + 1):
    name = "cloud" + str(i)
    node = request.RawPC("node%d" % i)
    node.disk_image = params.osImage
    node.hardware_type = params.phystype
    # Initialization script for the clients
    cloudLan.addInterface(node.addInterface())

link = request.BridgedLink("link")
link.bridge.hardware_type = "d430"
# Add the interfaces we created above.
link.addInterface(nfsLan)
link.addInterface(cloudLan)
link.latency = params.latency

"""
# Create link/lan.
if params.nodeCount > 1:
    if params.nodeCount == 2:
        lan = request.Link()
    else:
        lan = request.LAN()
        pass
    if params.bestEffort:
        lan.best_effort = True
    elif params.linkSpeed > 0:
        lan.bandwidth = params.linkSpeed
    if params.sameSwitch:
        lan.setNoInterSwitchLinks()
    pass

# Process nodes, adding to link or lan.
for i in range(params.nodeCount):
    # Create a node and add it to the request
    if params.useVMs:
        name = "vm" + str(i)
        node = request.XenVM(name)
    else:
        name = "node" + str(i)
        node = request.RawPC(name)
        pass
    if params.osImage and params.osImage != "default":
        node.disk_image = params.osImage
        pass
    # Add to lan
    if params.nodeCount > 1:
        iface = node.addInterface("eth1")
        lan.addInterface(iface)
        pass
    # Optional hardware type.
    if params.phystype != "":
        node.hardware_type = params.phystype
        pass
    # Optional Blockstore
    if params.tempFileSystemSize > 0 or params.tempFileSystemMax:
        bs = node.Blockstore(name + "-bs", params.tempFileSystemMount)
        if params.tempFileSystemMax:
            bs.size = "0GB"
        else:
            bs.size = str(params.tempFileSystemSize) + "GB"
            pass
        bs.placement = "any"
        pass
    #
    # Install and start X11 VNC. Calling this informs the Portal that you want a VNC
    # option in the node context menu to create a browser VNC client.
    #
    # If you prefer to start the VNC server yourself (on port 5901) then add nostart=True.
    #
    if params.startVNC:
        node.startVNC()
        pass
    pass
"""

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)