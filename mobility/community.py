#/usr/bin/env python
#coding:utf-8
import numpy as np
import math
    
import matplotlib.pyplot as plt
from copy import deepcopy


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


    def __init__(self, radio_radius=50, 
                 initial_time=500, 
                 generating_time=3000, 
                 propagating_time=8000,
                 sending_time=2):
        '''self.cgr and self.coordiantes list order format:
           [gateway1 community_mobile1 community_mobile2 community_mobile3 community_mobile4
           g2 c1 c2 c3 c4 ... gathering place]
        '''
        self.radio_r = radio_radius 
        self.i_time = initial_time
        self.g_time = generating_time 
        self.p_time = propagating_time
        # reached the dst, stop, and wait  for finishing to send messages
        self.s_time = sending_time
        self.nodes_num = (self.x_num*self.y_num - 1)*\
                         (self.community_mobile_num + self.community_nomobile_num) + 1
        self.cgr = []
        self.coordiantes = []
    
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
        '''mobile node: {'new':[x, y], 
                         'old':[old_x, old_y], 
                         'func':[x_f, y_f],
                         'src2dst_len':value, 
                         'wait_time':value
                         'speed': 0
                         } 
        '''
        coordinates = []
        x_coordinates = np.random.uniform(gateway[0],
                                          gateway[0] + self.subarea_x_len,
                                          self.community_mobile_num)
        y_coordinates = np.random.uniform(gateway[1],
                                          gateway[1] + self.subarea_y_len,
                                          self.community_mobile_num)
        for i in range(self.community_mobile_num):
            coordinates.append({
                                'new':[x_coordinates[i], y_coordinates[i]],
                                'old':[0, 0],
                                'func':[0, 0],
                                'src2dst_len':0,
                                'wait_time':0,
                                'speed':0
                                })
        return coordinates   


    def is_home(self, gateway, node):
        if node['new'][0] >gateway[0] and \
                node['new'][0] < (gateway[0] + self.subarea_x_len):
            if node['new'][1] >gateway[1] and \
                     node['new'][1] < (gateway[1] + self.subarea_y_len):
                return True
        return False

    
    def _next_coordiante(self, src, dst, speed):

        dst_tmp = {}
        if type(dst) == list: 
            dst_tmp['new'] = dst
        else:
            dst_tmp = dst
          
#         pprint(dst_tmp)  
        #start to new dst
        if  not src['wait_time']:
            x = src['new'][0] - src['old'][0]    
            y = src['new'][1] - src['old'][1] 
            new2old_len = float(math.sqrt(x*x + y*y))
            reached_flag = new2old_len - src['src2dst_len']
            #inital state
            if reached_flag>=0 and not src['src2dst_len']: 
#                 pprint(src)  
                x = src['new'][0] - dst_tmp['new'][0]    
                y = src['new'][1] - dst_tmp['new'][1] 
                src['src2dst_len'] = float(math.sqrt(x*x + y*y)) 
                src['func'][0] = x/src['src2dst_len']         
                src['func'][1] = y/src['src2dst_len']
                src['old'][0] = src['new'][0]
                src['old'][1] = src['new'][1]
                if src['speed'] == 0: src['speed'] = speed
                src['new'][0] = src['new'][0] - src['speed']*src['func'][0]
                src['new'][1] = src['new'][1] - src['speed']*src['func'][1]
#                 pprint(src)
                return src
            #continue to move as before
            elif reached_flag <0:
                src['new'][0] = src['new'][0] - src['speed']*src['func'][0]
                src['new'][1] = src['new'][1] - src['speed']*src['func'][1]
                return src
            #reach dst and new dst
            elif reached_flag >=0 and src['src2dst_len']:
                src['wait_time'] = self.s_time
                #update coordinate and other param
                x = src['new'][0] - dst_tmp['new'][0]    
                y = src['new'][1] - dst_tmp['new'][1] 
                src['src2dst_len'] = float(math.sqrt(x*x + y*y)) 
                src['func'][0] = x/src['src2dst_len']         
                src['func'][1] = y/src['src2dst_len']
                src['old'][0] = src['new'][0]
                src['old'][1] = src['new'][1]
                src['speed'] = speed
                return src
        #wait to send message
        else:
            src['wait_time'] = src['wait_time'] - 1
            return src      
#         pprint(src)
   
    def select_home_pos(self, gateway):
        x = range(gateway[0] + self.radio_r/2, 
                  gateway[0] + self.subarea_x_len,
                  self.radio_r/2)
        y = range(gateway[1] + self.radio_r/2, 
                  gateway[1] + self.subarea_y_len,
                  self.radio_r/2)
        x_index = int(np.random.uniform(len(x)))
        y_index = int(np.random.uniform(len(y)))
        return [x[x_index], y[y_index]]
    
    def select_node1(self,community_name, node_index):
        ''' from home to elsewhere,except gathering place.
        selected one([1-12]) communicat'''
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

    
    def select_node2(self, community_name, node_index):
        '''from eslewhere to elsewhere'''
        #selected one([1-12]) communicat ,expcept himself home
        dst_community_seq = int(np.random.uniform(1,13))
        while dst_community_seq == int(community_name[1:]):
            dst_community_seq = int(np.random.uniform(1,13))
        dst_community_name = 'c' + str(dst_community_seq)
        dst_node_index  = int(np.random.uniform(0,4))
        return (dst_community_name, dst_node_index)
    
    
    def select_node1_1(self, gateway, node):
        '''from home to elsewhere, except gathering place,1_1'''
        x = range(self.radio_r/2, self.area_x_len, self.radio_r/2)
        y = range(self.radio_r/2, self.area_y_len, self.radio_r/2)
        x_index = int(np.random.uniform(len(x)))
        y_index = int(np.random.uniform(len(y)))
        while ((x[x_index]-node[0])**2 + (y[y_index] -node[1])**2) < self.radio_r**2\
            or ((x[x_index]-gateway[0])**2 + (y[y_index] - gateway[1])**2) < self.radio_r**2:
            x_index = int(np.random.uniform(len(x)))
            y_index = int(np.random.uniform(len(y)))
        return [x[x_index], y[y_index]]
    
    def select_node1_2(self, gateway, node):
        '''from eslewhere to elsewhere 1_2'''
        x = range(self.radio_r/2, self.area_x_len, self.radio_r/2)
        y = range(self.radio_r/2, self.area_y_len, self.radio_r/2)
        x_index = int(np.random.uniform(len(x)))
        y_index = int(np.random.uniform(len(y)))
        while x[x_index] > gateway[0] and x[x_index] < (gateway[0] + self.subarea_x_len)\
               and y[y_index] > gateway[1] and y[y_index] < (gateway[1] + self.subarea_y_len):
                x_index = int(np.random.uniform(len(x)))
                y_index = int(np.random.uniform(len(y)))
        return [x[x_index], y[y_index]]
    
    def _next_coordiantes(self, gateways, homes, nodes):
        '''elsewhere means other "nodes" coordinates'''
        for name,home_nodes in nodes.iteritems():
            if int(name[1:]) == len(nodes): continue
            for index,node in enumerate(home_nodes):
                speed = np.random.uniform(self.min_speed, self.max_speed)
#                 if int(name[1:]) == 1: print(speed),
                probability_number = np.random.uniform(0,1)
#                 probability_number = np.random.random(1)
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
                        dst = self.select_home_pos(gateways[name])
                        nodes[name][index] =  self._next_coordiante(node,
                                                              dst, speed)
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
  
#                 pprint(nodes[name][index])        
#             print '\n'              
    
    def _next_coordiantes1(self, gateways, homes, nodes):
        '''elsewhere means all other  coordinates,  
          space between these coordinates is self.readio_r/2'''
        for name,home_nodes in nodes.iteritems():
            if int(name[1:]) == len(nodes): continue
            for index,node in enumerate(home_nodes):
                speed = np.random.uniform(self.min_speed, self.max_speed)
#                 if int(name[1:]) == 1: print(speed),
                probability_number = np.random.uniform(0,1)
#                 probability_number = np.random.random(1)
                # node is in home community
                if self.is_home(gateways[name], node):
                    #move to home gathering place
                    if probability_number > self.home2elsewhere:
                        nodes[name][index] =  self._next_coordiante(node,
                                                   gateways[name], speed)
                   #home move to elsewhere 
                    else:
                        dst = self.select_node1_1(gateways[name], node['new'])
                        nodes[name][index] = self._next_coordiante(node, 
                                                                   dst, speed)
                 #node is not at home community(is at eslewhere)
                else:
                    #from eslewhere  to home 
                    if probability_number > self.elsewhere2elsewhere:
                        dst = self.select_home_pos(gateways[name])
                        nodes[name][index] =  self._next_coordiante(node,
                                                              dst, speed)
                    #from eslewhere to elsewhere
                    else:
                        dst = self.select_node1_2(gateways[name], node['new'])
                        nodes[name][index] = self._next_coordiante(node,
                                                                 dst, speed)
                           
    def create_coordiantes(self, elsewhere=True):
        '''param: elsewhere is True, elsewhere means all other  coordinates,  
                          space between these coordinates is self.readio_r/2;
                  elsewhere is False,elsewhere means other "nodes" coordinates
           return: coordiantes list, such as c1-c12
        '''
        time = 0
        nodes = {}
        community_nodes = []
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
#         pprint(len(nodes))
        while time <=  (self.g_time + self.p_time):
            self.coordiantes = []
            time = time + 1
            if elsewhere:
                self._next_coordiantes1(gateways, homes, nodes) 
            else:
                self._next_coordiantes(gateways, homes, nodes) 
#             pprint(nodes)
            for i in range(len(gateways)):
                name = 'c' + str(i + 1)
#                 print name
                community_nodes = [node['new'] for node in nodes[name]]
                self.coordiantes.extend([gateways[name]] +community_nodes)  
#             print coordiantes   
            yield self.coordiantes

    def refresh_topology(self):
        coordiantes_iter = self.create_coordiantes()
        while coordiantes_iter:
            self.cgr = []
            coordiantes_iter.next()
            for i in range(self.nodes_num):
                self.cgr.append([])
                for j in range(self.nodes_num):
                    if i == j: 
                        self.cgr[i].append(1)
                        continue
                    x = self.coordiantes[i][0] - self.coordiantes[j][0]
                    y = self.coordiantes[i][1] - self.coordiantes[j][1]
                    if np.sqrt(x**2 + y**2) <= self.radio_r*2:
                        self.cgr[i].append(1)
                    else:
                        self.cgr[i].append(0)
            yield self.cgr
    

    def create_senders(self, gateway=True):
        '''param:gateway True,return gateway src and dst;
                 gateway Flase,return community mobile src and dst
           func:create senders index on self.coordiantes,
                     
        '''
        if gateway:
            gateway_src_seq = int(np.random.uniform(0, self.x_num*self.y_num-1))
            gateway_dst_seq = int(np.random.uniform(0, self.x_num*self.y_num))
            while gateway_dst_seq == gateway_src_seq:
                gateway_dst_seq = int(np.random.uniform(0, self.x_num*self.y_num))
            src_index = gateway_src_seq*(self.community_mobile_num + \
                                         self.community_nomobile_num)
            dst_index = gateway_dst_seq*(self.community_mobile_num +\
                                         self.community_nomobile_num)
#             print('gg', gateway_src_seq, gateway_dst_seq)
            return [src_index, dst_index]
        else:
            mobile_community_arr = np.random.uniform(0, self.x_num*self.y_num - 1, 2)
            mobile_community_arr = [int(elem) for elem in mobile_community_arr]
            if mobile_community_arr[0] == mobile_community_arr[1]:
                mobile_index_arr = np.random.uniform(0, self.community_mobile_num+1,2)
                mobile_index_arr = [int(elem) for elem in mobile_index_arr]
                while int(mobile_index_arr[0]) == int(mobile_index_arr[1]):
                    mobile_index_arr = np.random.uniform(0, self.community_mobile_num+1, 2)
                    mobile_index_arr = [int(elem) for elem in mobile_index_arr]

                src_index = (self.community_mobile_num + self.community_nomobile_num)*\
                            mobile_community_arr[0] + \
                            mobile_index_arr[0] + 1
                                                                  
                dst_index = (self.community_mobile_num + self.community_nomobile_num)*\
                            mobile_community_arr[1]  + \
                            mobile_index_arr[1] + 1
                return [src_index, dst_index]
            else:
                mobile_index_arr = np.random.uniform(0, self.community_mobile_num+1,2)
                mobile_index_arr = [int(elem) for elem in mobile_index_arr]
                src_index = (self.community_mobile_num + self.community_nomobile_num)*\
                            mobile_community_arr[0] + \
                            mobile_index_arr[0] + 1
                                                                  
                dst_index = (self.community_mobile_num + self.community_nomobile_num)*\
                            mobile_community_arr[1]  + \
                            mobile_index_arr[1] + 1
#                 print(mobile_community_arr, mobile_index_arr)
                return [src_index, dst_index]
            
    def run(self):
        time_count = 0
        flag = 0
        topology_iter = self.refresh_topology()
        while topology_iter:
            time_count = time_count + 1
            sender = []
            topology_iter.next()
            if time_count%10 == 0:
                flag = 1
                sender = self.create_senders()
            if (time_count-5)%10 == 0 and flag == 1:
                    flag = 0
                    time_count = 5 
                    sender = self.create_senders(False)
            yield [self.cgr, sender]

     


if __name__ == '__main__':
    colors = ['b', 'g', 'r', 'c', 'm' , 'y', 'k', 'slategrey', 'orange', 
              'mediumblue', 'brown', 'orchid']
#     print(len(colors))
    from pprint import pprint
    import matplotlib.animation as animation  
    model = Model()
    coordiantes_iter = model.create_coordiantes()
    topology_iter = model.refresh_topology()
    patchs = []
    fig = plt.figure()
    fig.set_dpi(100)
    fig.set_size_inches(7, 6.5)

    axes = plt.axes(xlim=(0, 3000), ylim=(0, 1500))
    axes.grid(True)
#     axes.set_xticks([0, 750, 1500, 2250, 3000])
    axes.set_xticks(range(0, 3750, 375))
    axes.set_yticks(range(0, 1750, 250))
    
    flag = 0
    def init():
        global flag 
        if flag == 0:
            flag = 1
        else:
            return tuple(patchs)
        coordiantes = coordiantes_iter.next()
        print "只执行一次"
        for index, coordiante in enumerate(coordiantes):
            i = index/5
#             if i >0: break
#             coordiante = [int(e) for e in coordiante]
            patch = plt.Circle(coordiante, radius=50, color=colors[i],alpha=0.5)
            patchs.append(patch)
            axes.add_patch(patch)
        axes.axis('equal')
        axes.margins(0)
        return tuple(patchs)
    
    def animate(i):
#         coordiantes = coordiantes_iter.next()
        topology_iter.next()
#         print(model.cgr[50].count(1)-1)
#         hh = [e.count(1) for e in model.cgr]
#         print(sum(hh))
#         print(len(coordiantes))
        for index,coordiante in enumerate(model.coordiantes):
#             print([int(e) for e in coordiante]),
#             if index/5 >0: break
            patchs[index].center = coordiante
#         print("\n")
        return tuple(patchs)
    
#     anim = animation.FuncAnimation(fig, animate, 
#                                init_func=init, 
#                                 frames=360, 
#                                interval=100,
#                                blit=True)
# #  
#     plt.show()

    n = 0
    gateways = []
    x_s = []
    y_s = []
    hh_iter =  model.run()
    while n < 20:
        hh = []
        hh = hh_iter.next()
        n = n + 1
       
#         print(len(hh[0]))
        print(hh[1])
        print ""
#         x_s.append(len(hh[0]))
#         y_s.append(hh[1])
# #         gateways.append(hh)
#         print hh
#     print('avg',sum(x_s)/len(gateways), sum(y_s)/len(gateways))
#     print('x_s max:%d', max(x_s))
#     print('y_s max:%d', max(y_s))


