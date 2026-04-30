"""
This profile allows for flexible instantiation of LoRa experiments on the POWDER platform. Combinations of rooftop, dense deployment, fixed endpoint, and mobile endpoint resources can be composed together.

*Note:* Not all radios are within range of one another. Please see the table below for a table showing working pairs of fixed location devices. Shuttle (mobile endpoint) connectivity will vary depending on proximity of the vehicle to other radios.

**TODO: Insert Table Here**

Instructions:
TODO.
<https://gitlab.flux.utah.edu/Jie_Wang/gr_lora_sdr_powder>
"""

import geni.portal as portal
import geni.urn as urn
import geni.rspec.pg as pg
import geni.rspec.emulab as elab
import geni.rspec.emulab.spectrum as spectrum

# Resource strings
DISK_IMAGE = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-GR310"
STARTUP_SCRIPT = "/local/repository/bin/startup.sh"

# List of CBRS rooftop X310 radios.
cbrs_radios = [
    ("cbrssdr1-bes",
     "Behavioral"),
    ("cbrssdr1-browning",
     "Browning"),
    ("cbrssdr1-dentistry",
     "Dentistry"),
    ("cbrssdr1-fm",
     "Friendship Manor"),
    ("cbrssdr1-hospital",
     "Hospital"),
    ("cbrssdr1-honors",
     "Honors"),
    ("cbrssdr1-meb",
     "MEB"),
    ("cbrssdr1-smt",
     "SMT"),
    ("cbrssdr1-ustar",
     "USTAR"),
]

# A list of fixed endpoint sites.
fe_sites = [
    ('urn:publicid:IDN+bookstore.powderwireless.net+authority+cm',
     "Bookstore"),
    ('urn:publicid:IDN+cpg.powderwireless.net+authority+cm',
     "Garage"),
    ('urn:publicid:IDN+ebc.powderwireless.net+authority+cm',
     "EBC"),
    ('urn:publicid:IDN+guesthouse.powderwireless.net+authority+cm',
     "GuestHouse"),
    ('urn:publicid:IDN+humanities.powderwireless.net+authority+cm',
     "Humanities"),
    ('urn:publicid:IDN+law73.powderwireless.net+authority+cm',
     "Law73"),
    ('urn:publicid:IDN+madsen.powderwireless.net+authority+cm',
     "Madsen"),
    ('urn:publicid:IDN+moran.powderwireless.net+authority+cm',
     "Moran"),
    ('urn:publicid:IDN+sagepoint.powderwireless.net+authority+cm',
     "SagePoint"),
    ('urn:publicid:IDN+web.powderwireless.net+authority+cm',
     "WEB"),
]

# List of CBRS rooftop X310 radios.
dense_radios = [
    ("cnode-wasatch",
     "Wasatch"),
    ("cnode-mario",
     "Mario"),
    ("cnode-moran",
     "Moran"),
    ("cnode-guesthouse",
     "Guesthouse"),
    ("cnode-ebc",
     "EBC"),
    ("cnode-ustar",
     "USTAR"),
]

#
# Profile parameters.
#
pc = portal.Context()

# Node type parameter for PCs to be paired with X310 radios.
# Restricted to those that are known to work well with them.
portal.context.defineParameter(
    "nodetype",
    "Compute node type",
    portal.ParameterType.STRING, "d740",
    ["d740","d430"],
    "Type of compute node to be paired with the X310 Radios",
)

# Set of CBRS X310 radios to allocate
# portal.context.defineStructParameter(
#     "cbrs_radio_sites", "CBRS Radio Sites", [],
#     multiValue=True,
#     min=0,
#     multiValueTitle="CBRS roofotp X310 radios to allocate.",
#     members=[
#         portal.Parameter(
#             "radio",
#             "CBRS Radio Site",
#             portal.ParameterType.STRING,
#             cbrs_radios[0], cbrs_radios,
#             longDescription="CBRS X310 radio will be allocated from selected site."
#         ),
#     ])

# Set of OTA Lab NUC+B210 devices to allocate
# portal.context.defineStructParameter(
#     "dense_radios", "Dense Site Radios", [],
#     multiValue=True,
#     min=0,
#     multiValueTitle="Dense Site SFF+B210 radios to allocate.",
#     members=[
#         portal.Parameter(
#             "device",
#             "SFF Compute + NI B210 device",
#             portal.ParameterType.STRING,
#             dense_radios[0], dense_radios,
#             longDescription="A Small Form Factor compute with attached NI B210 device at the given Dense Deployment site will be allocated."
#         ),
#     ])

# Set of Fixed Endpoint devices to allocate
portal.context.defineStructParameter(
    "fe_radio_sites", "Fixed Endpoint Sites", [],
    multiValue=True,
    min=0,
    multiValueTitle="Fixed Endpoint NUC+B210 radios to allocate.",
    members=[
        portal.Parameter(
            "site",
            "FE Site",
            portal.ParameterType.STRING,
            fe_sites[0], fe_sites,
            longDescription="A `nuc2` device will be selected at the site."
        ),
        portal.Parameter(
            "device",
            "NUC Device",
            portal.ParameterType.STRING,
            "nuc2", ("nuc1", "nuc2"),
            longDescription="Select which NUC device+radio to use at the site."
        )
    ])

# Frequency/spectrum parameters
# portal.context.defineStructParameter(
#     "cbrs_freq_ranges", "CBRS Frequency Ranges", [],
#     multiValue=True,
#     min=1,
#     multiValueTitle="Frequency ranges for CBRS operation.",
#     members=[
#         portal.Parameter(
#             "freq_min",
#             "Frequency Min",
#             portal.ParameterType.BANDWIDTH,
#             3550.0,
#             longDescription="Values are rounded to the nearest kilohertz."
#         ),
#         portal.Parameter(
#             "freq_max",
#             "Frequency Max",
#             portal.ParameterType.BANDWIDTH,
#             3560.0,
#             longDescription="Values are rounded to the nearest kilohertz."
#         ),
#     ])

portal.context.defineStructParameter(
    "ISM_range", "ISM Frequency Ranges", [],
    multiValue=True,
    min=1,
    multiValueTitle="Frequency ranges for ISM operation.",
    members=[
        portal.Parameter(
            "freq_min",
            "Frequency Min",
            portal.ParameterType.BANDWIDTH,
            902.0,
            longDescription="Values are rounded to the nearest kilohertz."
        ),
        portal.Parameter(
            "freq_max",
            "Frequency Max",
            portal.ParameterType.BANDWIDTH,
            928.0,
            longDescription="Values are rounded to the nearest kilohertz."
        ),
    ])

portal.context.defineParameter(
    "alloc_shuttles", 
    "Allocate all routes (mobile endpoints)",
    portal.ParameterType.BOOLEAN, False)

# Bind and verify parameters
params = portal.context.bindParameters()

# TODO: Check to ensure devices and frequencies were selected.

for i, frange in enumerate(params.ISM_range):
    if frange.freq_min < 902 or frange.freq_min > 928 \
       or frange.freq_max < 902 or frange.freq_max > 928:
        perr = portal.ParameterError("CBAND/CBRS frequencies must be between 3400 and 3800 MHz", ["cbrs_freq_ranges[%d].freq_min" % i, "cbrs_freq_ranges[%d].freq_max" % i])
        portal.context.reportError(perr)
    if frange.freq_max - frange.freq_min < 1:
        perr = portal.ParameterError("Minimum and maximum frequencies must be separated by at least 1 MHz", ["cbrs_freq_ranges[%d].freq_min" % i, "cbrs_freq_ranges[%d].freq_max" % i])
        portal.context.reportError(perr)
        
pc.verifyParameters()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Helper function that allocates a PC + X310 radio pair, with Ethernet
# link between them.
# def x310_node_pair(x310_radio_name, node_type):
#     radio_link = request.Link("%s-link" % x310_radio_name)

#     node = request.RawPC("%s-comp" % x310_radio_name)
#     node.hardware_type = node_type
#     node.disk_image = DISK_IMAGE

#     node.addService(pg.Execute(shell="bash",
#                                command=STARTUP_SCRIPT))

#     node_radio_if = node.addInterface("usrp_if")
#     node_radio_if.addAddress(pg.IPv4Address("192.168.40.1",
#                                             "255.255.255.0"))
#     radio_link.addInterface(node_radio_if)

#     radio = request.RawPC("%s-radio" % x310_radio_name)
#     radio.component_id = x310_radio_name
#     radio_link.addNode(radio)

# # Request PC + CBRS X310 resource pairs.
# for rsite in params.cbrs_radio_sites:
#     x310_node_pair(rsite.radio, params.nodetype)

# Request NUC+B210 radio resources at the requested Dense Deployment sites.
for ddsite in params.dense_radios:
    node = request.RawPC("%s-dd-b210" % ddsite.device)
    node.component_id = ddsite.device
    node.disk_image = DISK_IMAGE
    node.addService(pg.Execute(shell="bash",
                              command=STARTUP_SCRIPT))

# Request nuc2+B210 radio resources at FE sites.
for fesite in params.fe_radio_sites:
    nuc = ""
    for urn,sname in fe_sites:
        if urn == fesite.site:
            nuc = request.RawPC("%s-b210" % sname)
            break
    nuc.component_manager_id = fesite.site
    nuc.component_id = fesite.device
    nuc.disk_image = DISK_IMAGE
    nuc.addService(pg.Execute(shell="bash",
                              command=STARTUP_SCRIPT))

# Request ed1+B210 radio resources on all ME units (shuttles).
if params.alloc_shuttles:
    allroutes = request.requestAllRoutes()
    allroutes.disk_image = DISK_IMAGE
    allroutes.addService(pg.Execute(shell="bash",
                                    command=STARTUP_SCRIPT))

# Request frequency range(s)
for frange in params.ISM_range:
    request.requestSpectrum(frange.freq_min, frange.freq_max, 0)

# Print the RSpec to the enclosing page.
pc.printRequestRSpec()
