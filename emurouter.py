import math

class Router:

    def __init__(self, port_labels = ["eth1", "eth2", "eth3", "s01"], port_speed = ["100", "100", "100", "1000"], port_ip = ["10.1.0.1", "10.1.0.2", "10.1.0.3", "10.1.0.4"]):
        self.ports_bw = {}
        self.ports = port_labels
        self.port_speed = port_speed
        self.ports_bw = set_ports_bw(port_speed)
        self.ports_ip = set_ports_ip(port_ip)
        self.port_energy = init_port_energy()
        self.routes = {}

    
    def set_ports_bw(self, port_speed):
        ports_bw = {}
        for i in range(len(self.ports)):
            ports_bw[self.ports[i]] = port_speed[i]
        return ports_bw

    def set_ports_ip(self, port_ip):
        ports_ip = {}
        for i in range(len(self.ports)):
            ports_ip[self.ports[i]] = port_ip[i]
        return ports_ip

    def init_port_energy(self):
        port_energy = {}
        for i in range(len(self.ports)):
            port_energy[self.ports[i]] = 0
        return port_energy

    def get_ports(self):
        return self.ports

    def get_portspeed(self):
        return self.port_speed

    def add_route(self, interface, ip):
        self.routes[ip] = interface

    # defines how many ticks the router need to let a data stream pass through its interfaces
    def traffic_time(self, ingress, egress, data_size):
        in_speed = self.ports_bw[ingress]
        out_speed = self.ports_bw[egress]
        speed = min(in_speed, out_speed)
        ticks = int(math.ceil(data_size / speed))   # always round up, so to more or less take into account the computational time... it balances through the whole simulation
        return ticks

    def compute_energy(self, interface, time, speed):
        # TO DO: compute a value for the energy based on the time traffic need to go through the interface(s) and the speed/bandwidth provided by the interface(s)
        pass