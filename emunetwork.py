from emurouter import Router
import random
import time

# TO DO HERE
# while(duration) --> emulate traffic flows going through the router.
# traffic is defined as a "tuple": < router_ingress_intf ; router_egress_intf ; data_size >
# what we want to achieve is that given the bandwidth provided by the router (which mainly depends on the slowest interface used by the traffic) and given the size of the data,
# we are able to compute the time needed by the router to "process" that data, and therefore the interface utilization in terms of electric energy


if __name__ == "__main__":
    #duration = input("Choose the duration of the simulation (in seconds): ")
    duration = 120

    router = Router()

    router_ports_bandwidth = router.get_ports_bw()
    router_ports_ip = router.get_ports_ip()

    # =======
    # Print summary of router interfaces
    # =======
    print("Interface\tIP\t\t\tSpeed (Mb/s)")
    for k in router_ports_bandwidth.keys():
        if k in router_ports_ip.keys():
            print(f"{k}\t\t{router_ports_ip[k]}\t\t{router_ports_bandwidth[k]}")
    # =======

    traffic_flows = {}

    for i in range(10):
        start_time = random.randint(0,duration)
        while start_time in traffic_flows.keys():
            start_time = random.randint(0,duration)
        in_intf = "s01"
        e_intf = "eth1"
        data_size = random.randint(1,1200)
        traffic_flows[str(start_time)] = [in_intf, e_intf, data_size]

    print("Traffic flows summary\nTime\t\tIngress intf\tEgress intf\tSize (MB)")
    for k,v in traffic_flows.items():
        print(f"{k}\t\t{v[0]}\t\t{v[1]}\t\t{v[2]}")

    # =======
    # Basic simulation run
    # =======
    seconds = 0
    while seconds<duration:
        print(f"Time {seconds}")
        s = str(seconds)
        if len(router.buffer) != 0:
            traffic = router.buffer.pop(0)
            ingress_interface = traffic[0]
            egress_interface = traffic[1]
            traffic_size = traffic[2]
            # fai tutto quello che fa sotto
        if s in traffic_flows.keys():
            ingress_interface = traffic_flows[s][0]
            egress_interface = traffic_flows[s][1]
            traffic_size = traffic_flows[s][2]
            #required_time = router.traffic_time(ingress=ingress_interface, egress=egress_interface, data_size=traffic_size)
            ingress_ticks = router.intf_time(interface=ingress_interface, data_size=traffic_size)
            egress_ticks = router.intf_time(interface=egress_interface, data_size=traffic_size)
            if router.port_status[ingress_interface] == 0:
                router.set_port_status(interface=ingress_interface, status=ingress_ticks)
                print(f"Router interface {ingress_interface} will now be busy for {ingress_ticks} seconds")
                if router.port_status[egress_interface] == 0:
                    router.set_port_status(interface=egress_interface, status=egress_ticks)
                    print(f"Router interface {egress_interface} will now be busy for {egress_ticks} seconds")
                else:
                    traffic_flows[s][0] = 0 # il traffico è già NEL router, deve solo uscire... ma forse non è corretto ed è troppo complicato... mica il router si tiene dentro 1 GB di pacchetti!!
                    (router.buffer).append(traffic_flows[s])
            else:
                (router.buffer).append(traffic_flows[s])
                print(f"Traffic flow {traffic_flows[s]} has been added to the buffer")
            print(f"Time required for traffic at time {seconds}: {required_time} seconds")
        for k,v in router.port_status.items():
            if v>0:
                router.port_status[k] = v-1
                
        seconds += 1
        time.sleep(0.5)
    # =======