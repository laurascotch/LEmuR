# TO DO HERE
# while(duration) --> emulate traffic flows going through the router.
# traffic is defined as a "tuple": < router_ingress_intf ; router_egress_intf ; data_size >
# what we want to achieve is that given the bandwidth provided by the router (which mainly depends on the slowest interface used by the traffic) and given the size of the data,
# we are able to compute the time needed by the router to "process" that data, and therefore the interface utilization in terms of electric energy