#/usr/bin/env python
#coding:utf-8
import numpy as np
import math

class Model(object):
    '''community model,which is described in the paper Probabilistic Routing
       in Intermittently Connected Networks.
       area_length,area_width,radio_radius unit is meter. area is splited to 
       12subarea: 11 communities and 1 gathering place.
    '''
    area_x_len = 3000 #(meter)
    area_y_len = 1500  #(meter)
    subarea_x_len = 750
    subarea_y_len  = 500
    x_num = int(area_x_len/subarea_x_len)
    y_num = int(area_y_len/subarea_y_len)
    community_mobile_num = 4 
    community_nomobile_num = 1
    min_speed = 10  #(m/s)
    max_speed = 30  #(m/s)
    elsewhere2home = 0.9 #(probabilities)
    elsewhere2elsewhere = 0.1
    home2gathering = 0.8
    home2elsewhere = 0.2


    def __init__(self, radio_r=50, i_time=500, g_time=3000, 
                 p_time=8000):
        self.radio_radius = radio_r
        self.initial_time = i_time
        self.generating_time = g_time
        self.propagating_time = p_time
    
    def get_gateway_coordinates(self):
        coordinates = {}
        zero_cummunity_seq = self.x_num*(self.y_num-1) + 1
        for i in range(0, self.y_num):
            for j in range(zero_cummunity_seq, self.x_num+zero_cummunity_seq):
                
                community_seq = j-i*self.x_num
                community_name = 'c' + str(community_seq)
                x = (j-zero_cummunity_seq)*self.subarea_x_len
                y = i*self.subarea_y_len
                coordinates[community_name] = [x, y] 
        return coordinates
    

    def get_home_coordinates(self):
        coordinates = {}
        zero_cummunity_seq = self.x_num*(self.y_num - 1) + 1
        for i in range(0, self.y_num):
            for j in range(zero_cummunity_seq, self.x_num + zero_cummunity_seq):
                
                community_seq = j-i*self.x_num
                community_name = 'c' + str(community_seq)
                x = (j-zero_cummunity_seq)*self.subarea_x_len + \
                                         int(self.subarea_x_len/2)
                y = i*self.subarea_y_len + int(self.subarea_y_len/2)
                coordinates[community_name] = [x, y] 
        return coordinates

    def init_node_coordinates(self, gateway, mobile_nodes_num):
        coordinates = []
        x_coordinates = np.random.uniform(gateway[0],
                                          gateway[0] + self.subarea_x_len,
                                          self.community_mobile_num)
        y_coordinates = np.random.uniform(gateway[1],
                                          gateway[1] + self.subarea_y_len,
                                          self.community_mobile_num)
        for i in range(self.community_mobile_num):
            coordinates.append([x_coordinates[i], y_coordinates[i]])
        return coordinates   


    def is_home(self, gateway, node):
        if node[0] >gateway[0] and  node[0] < (gateway[0] + self.subarea_x_len):
            if node[1] >gateway[1] and node[1] < (gateway[1] + self.subarea_y_len):
                return True
        return False

    def _next_coordiante(self, src, dst, speed):
        node = [0,0]
        x = src[0] - dst[0]    
        y = src[1] - src[1]
        src2dst_len = float(math.sqrt(x*x + y*y))
        if src2dst_len < speed :
            return dst

        x_offset = speed*x/src2dst_len
        y_offset = speed*y/src2dst_len
        node[0] = src[0] - x_offset
        node[1] = src[1] - y_offset
        return node
    
        
    #from home to elsewhere,except gathering place
    def select_node1(self,community_name, node_index):
        #selected one([1-12]) communicat
        dst_community_seq = int(np.random.uniform(1,13))
        if dst_community_seq != int(community_name[1:]):
            dst_community_name = 'c' + str(dst_community_seq)
            dst_node_index  = int(np.random.uniform(0,4))
        else:
            dst_community_name = community_name
            dst_node_index  = int(np.random.uniform(0,4))
            while dst_node_index == node_index:
                dst_node_index  = int(np.random.uniform(0,4))
        return (dst_community_name, dst_node_index)

    #from eslewhere to elsewhere
    def select_node2(self, community_name, node_index):
        #selected one([1-12]) communicat ,expcept himself home
        dst_community_seq = int(np.random.uniform(1,13))
        while dst_community_seq == int(community_name[1:]):
            dst_community_seq = int(np.random.uniform(1,13))
        dst_community_name = 'c' + str(dst_community_seq)
        dst_node_index  = int(np.random.uniform(0,4))
        return (dst_community_name, dst_node_index)

    def _next_coordiantes(self, gateways, homes, nodes):
        for name,home_nodes in nodes.iteritems():
            if int(name[1:]) == len(nodes):continue
            for index,node in enumerate(home_nodes):
                speed = np.random.uniform(self.min_speed, self.max_speed)
                probability_number = np.random.uniform(0,1)
                # node is in home community
                if self.is_home(gateways[name], node):
                   #move to home gathering place
                    if probability_number > self.home2elsewhere:
                        nodes[name][index] =  self._next_coordiante(node,
                                                   gateways[name], speed)
                   #home move to elsewhere 
                    else:
                        dst_community_name, dst_node_index = self.select_node1(
                                                                   name, index)
                        if int(dst_community_name[1:]) == len(gateways):
                            nodes[name][index] = self._next_coordiante(node,
                                          gateways[dst_community_name], speed)
                        else:
                            nodes[name][index] = self._next_coordiante(node,
                                  nodes[dst_community_name][dst_node_index],
                                                                      speed)   
                           
                #node is not at home community(is at eslewhere)
                else:
                    #from eslewhere  to home 
                    if probability_number > self.elsewhere2elsewhere:
                        nodes[name][index] =  self._next_coordiante(node,
                                                   homes[name], speed)
                    #from eslewhere to elsewhere
                    else:
                        dst_community_name, dst_node_index = self.select_node2(
                                                                   name, index)
                        if int(dst_community_name[1:]) == len(gateways):
                            nodes[name][index] = self._next_coordiante(node,
                                          gateways[dst_community_name], speed)
                        else:
                            nodes[name][index] = self._next_coordiante(node,
                                  nodes[dst_community_name][dst_node_index],
                                                                      speed)   
                        
                              

    def create_coordiantes(self):
        time = 0
        nodes = {}
        #inital coordiates
        gateways = self.get_gateway_coordinates()
        homes  = self.get_home_coordinates()
        for name, gateway in gateways.iteritems():
            if int(name[1:]) == len(gateways): 
                #nodes[name] = [gateways['c12']]*4
                nodes[name] = []
            else:
                nodes[name] = self.init_node_coordinates(gateway,
                                            self.community_mobile_num)    
        
        while time <=  (self.generating_time + self.propagating_time):
            time = time + 1
            coordiantes = []
            self._next_coordiantes(gateways, homes, nodes) 

            for i in range(len(gateways)):
                name = 'c' + str(i + 1)
                coordiantes.extend([gateways[name]] + nodes[name])     
            yield coordiantes

    def get_topology(self):
        pass
    

    def get_senders(self):
        pass

     

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from pprint import pprint
    model = Model()
    coordiantes = model.create_coordiantes().next()
    x = []
    y = []
    for coordiante in coordiantes:
        x.append(coordiante[0])
        y.append(coordiante[1])
    plt.scatter(x, y, s=np.pi*100, alpha=0.5)
    plt.show()
