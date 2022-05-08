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

