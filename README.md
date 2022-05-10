# LEmuR
LEmuR AKA **L**ittle **Emu**lated **R**outer is a simple simulator with the aim of studying the power consumption due to the interface usage of a generic router.

### A bit of context - Energy consuption of a router
What follows is a summary of the main concepts expressed in [Analyzing Local Strategies for Energy-Efficient Networking](https://doi.org/10.1007/978-3-642-23041-7_28).

The tendency towards miniaturization and the ICT growing dynamic aren't effectively aiming at reducing power consumption. In particular, miniaturization has reduced the single unit power consumption, but it allows for more ports to be put into the same device, thus increasing performances and power utilization (rebound effect, Jevons paradox). The result is that the total power required per node in a network is growing.

Experimental measurements ([Ref1](https://ieeexplore.ieee.org/abstract/document/4509688)) from many different network devices show that half of the energy consumption is due to the base system, while the other half depends on the number of installed line interface cards (even if idle). Furthermore, the power consumption of routers and switches is, quite surprisingly, independent from the network load, resulting in a difference of just 3% more energy required by heavy loaded network devices, compared to idle ones. This is a clear suggestion that it is crucial to develop energy-efficient architectures able to temporarily switch off entire devices or at least some parts, so to minimize energy consumption as much as possible.

Putting in sleep mode entire nodes may be unpractical for various reasons, mainly: a) it is unconvenient, investment-wise, to switch off highly expensive transmission links; b) decreasing the meshing degree of a network leads to lesser reliability and difficulty in load balancing.

Putting in sleep mode only single interfaces of a device may be really effective in terms of energy saving, in particular when operating at high speed: in a common commercial Ethernet switch Catalyst 2970 24-ports LAN switch) a 1000baseT adds 1.8 W to the overall energy consumption. The following table gives an insight of interface power consumption of the vast majority of commercial off-the-shelf network devices.

| Active interfaces | 10BaseT | 100BaseT | 1000BaseT |
|---|---|---|---|
| 0 | 69.1 | 69.1 | 69.1 |
| 2 | 70.2 | 70.1 | 72.9 |
| 4 | 71.1 | 70.0 | 76.7 |
| 6 | 71.6 | 71.1 | 80.2 |
| 8 | 71.9 | 71.9 | 83.7 |

There are two main per-interface sleeping mechanisms, ALR and LPI. ALR is based on the ability of dinamically modifying the link rate according to the traffic needs: in fact, operating devices at lower frequency can enable energy consumption reduction. In LPI, transmission on a single interface is stopped when there's no data to send and quickly resumed when new packets arrive, instead of having the continuous IDLE signal typical of legacy systems. 

It is important to remember that in network environments where packet arrival rates can be highly non-uniform, allowing interface transitions between different operating rates or sleep/active modes can introduce additional delays or even losses.

In order to provide realistic values regarding the energy consuption during the simulation, the following table is considered. The table shows the energy/power consumption of interfaces working at their native link rates for most commercial off-the-shelf network devices.

| Native link rate | Power per interface | Energy Scaling Index | Energy Consumption Rate (power per Gbps) |
|---|---|---|---|
| 10 Mbps | 0.1 W | 10 nJ/bit | 10 W/Gbps |
| 100 Mbps | 0.2 W | 2 nJ/bit | 2 W/Gbps |
| 1000 Mbps | 0.5 W | 0.5 nJ/bit | 0.5 W/Gbps |
| 10000 Mbps | 5.0 W | 0.5 nJ/bit | 0.5 W/Gbps |

We can notice that the energy consumption for forwarding one bit isn't the same for every interface, but depends on its native link rate.

Observations confirm that an interface consumes the same power whatever its current throughput is: power consumption is throughput independent. It derives that the link rate can be adapted to the current throughput (by using ALR) with consequent energy savings.

### Simulation outline
The router is initialized by the default with the following interfaces:
 - `eth1` is a FastEthernet port (100 Mb/s)
 - `eth2` is a FastEthernet port (100 Mb/s)
 - `eth3` is a FastEthernet port (100 Mb/s)
 - `s01` is a Gigabit port (1000 Mb/s)

The router has a (yet) infinite buffer where traffic flows are stored waiting for needed interfaces to be available.

Traffic flows are represented by a triple: `[ingress_interface, egress_interface, data_size]`. The idea is that a traffic flow represents a rather big chunk of generic network traffic; in fact we are not interested in studying every single TCP flow from every client in a LAN attached to the router, but in general we want to understand how the router behaves in terms of energy consumption under different loads.

Given a duration (in seconds) of the simulation, time is discretized (1 tick = 1 second).

At every tick:
 - If there is a flow in the buffer, if the needed interfaces are free, manage it: set the interfaces to "busy" for the time needed to dispose of the total size of the traffic flow
 - If there is an incoming flow, if the needed interfaces are busy, enqueue it in the buffer, otherwise manage it: again set the interfaces to "busy" for the time needed
 - Decrease the timers indicating the "still-busy" time of the interfaces
 - Update the usage statistics of the router and its interfaces

### Needed assumptions
It would be a gigantic work to perfectly emulate a router and there are professional softwares that are much more suited for that objective. In order to just gather some statistics on the energy consumption of a router, we can make some simplifications thanks to the following assumptions:
 - All the routing mechanisms (ARP, BGP, OSPF, etc.) go under the computational effort of the router, which translates to a certain amount of energy consumption, that isn't strictly dependent on a regular traffic. We can consider this a priori.
 - We don't care about every single connection going through the router: since we already know (as already cited) that power consumption is throughput independent for each interface, we assume that for every traffic flow/burst arriving to the router, the ingress and egress interfaces are used to their maximum capacity and rate.
