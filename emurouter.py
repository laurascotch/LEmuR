import math

class Router:

    def __init__(self, port_labels = ["eth1", "eth2", "eth3", "s01"], port_speed = ["100", "100", "100", "1000"], port_ip = ["10.1.0.1", "10.1.0.2", "10.1.0.3", "10.1.0.4"]):
        self.ports_bw = {}
        self.ports = port_labels
        self.port_speed = port_speed
        self.ports_bw = self.set_ports_bw(port_speed)
        self.ports_ip = self.set_ports_ip(port_ip)
        self.port_energy = self.init_port_energy()
        self.routes = {}    # mi sa che non serve
        self.port_status = {}   # dictionary. Indicates for how many seconds the interface is still busy (e.g. "eth1": 0 means that it's free)
        init_port_status()
        self.buffer = []    # if an interface is already occupied, add the traffic to the buffer

    
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

    def init_port_status(self):
        for i in range(len(self.ports)):
            self.port_status[self.ports[i]] = 0
        

    def init_port_energy(self):
        port_energy = {}
        for i in range(len(self.ports)):
            port_energy[self.ports[i]] = 0
        return port_energy

    def get_ports(self):
        return self.ports

    def get_portspeed(self):
        return self.port_speed
    
    def get_ports_bw(self):
        return self.ports_bw

    def get_ports_ip(self):
        return self.ports_ip

    def set_port_status(self, interface, status):
        self.port_status[interface] = status

    def add_route(self, interface, ip):
        self.routes[ip] = interface

    # defines how many ticks the router need to let a data stream pass through its interfaces
    def traffic_time(self, ingress, egress, data_size):
        in_speed = int(self.ports_bw[ingress])
        out_speed = int(self.ports_bw[egress])
        speed = min(in_speed, out_speed)
        ticks = int(math.ceil(data_size / speed))   # always round up, so to more or less take into account the computational time... it balances through the whole simulation
        return ticks

    def intf_time(self, interface, data_size):
        intf_speed = int(self.ports_bw[interface])
        ticks = int(math.ceil(data_size/speed))
        return ticks

    def compute_energy(self, interface, time, speed):
        # TO DO: compute a value for the energy based on the time traffic need to go through the interface(s) and the speed/bandwidth provided by the interface(s)
        pass