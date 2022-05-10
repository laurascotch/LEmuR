import math

class Router:

    #basic_router_energy = 69.1 # Watt - valid for most cisco's
    basic_router_energy = 55 # Watt

    def __init__(self, port_labels = ["eth1", "eth2", "eth3", "eth4", "eth5", "eth6", "s01", "s02"],\
                    port_speed = ["100", "100", "100", "100", "100", "100", "1000", "1000"],\
                    port_ip = ["10.1.0.1", "10.1.0.2", "10.1.0.3", "10.1.0.4", "10.1.0.5", "10.1.0.6", "10.1.10.1", "10.1.10.2"]):
        self.ports_bw = {}
        self.ports = port_labels
        self.port_speed = port_speed
        self.ports_bw = self.set_ports_bw(port_speed)
        self.ports_ip = self.set_ports_ip(port_ip)
        self.power_per_intf = {"10":0.4, "100":0.4, "1000":1.8} # native link rate : power per interface
        self.energy_consumption_rate = self.set_energy_consumption_rate() # W/Gbps
        self.port_usage = self.init_port_usage() # energy consumption of every port
        self.port_status = {}   # dictionary. Indicates for how many seconds the interface is still busy (e.g. "eth1": 0 means that it's free)
        self.init_port_status()
        self.energy_in_time = {}    # energy needed every tick with truly idle interfaces
        self.energy_in_time_no_optimization = {}    # energy needed every tick if all interfaces are always up (no power saving)
        self.buffer = []    # if an interface is already occupied, add the traffic to the buffer

    def set_energy_consumption_rate(self):
        ecr = {}
        for rate, power in self.power_per_intf.items():
            ecr[rate] = power / int(rate)
        return ecr
    
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

    def init_port_usage(self):
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

    def get_port_usage(self):
        return self.port_usage

    # defines how many ticks the router need to let a data stream pass through its interfaces
    def traffic_time(self, ingress, egress, data_size):
        in_speed = int(self.ports_bw[ingress])
        out_speed = int(self.ports_bw[egress])
        speed = min(in_speed, out_speed)
        ticks = int(math.ceil(data_size / speed))   # always round up, so to more or less take into account the computational time... it balances through the whole simulation
        return ticks

    def intf_time(self, interface, data_size):
        intf_speed = self.ports_bw[interface]
        ticks = int(math.ceil(data_size/int(intf_speed)))
        return ticks

    def compute_energy(self,active_ports,time):
        t = str(time)
        energy = self.basic_router_energy
        for port in active_ports:
            port_rate = self.ports_bw[port]
            energy += self.power_per_intf[str(port_rate)]
        self.energy_in_time[t] = round(energy, 2)
        energy_waste = self.basic_router_energy
        for port in self.ports:
            port_rate = self.ports_bw[port]
            energy_waste += self.power_per_intf[str(port_rate)]
        self.energy_in_time_no_optimization[t] = round(energy_waste, 2)