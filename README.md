# LEmuR
LEmuR AKA **L**ittle **Emu**lated **R**outer is a simple simulator with the aim of studying the interface usage of a generic router.

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
 - We don't care about every single connection going through the router: we 