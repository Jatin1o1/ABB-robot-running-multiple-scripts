#!/usr/bin/env python

import socket         
import argparse
#import rospy
#from std_msgs.msg import Float64
#from geometry_msgs.msg import PoseStamped, PoseArray
import time

#def have_points_callback(msg):
#       global is_having_points
#       is_having_points = msg.data
#       time.sleep(0.2)

cmd_array=[]
def openfile(filename):
    f = open(filename, "r")
    for x in f:
        #print(x)
        jatin= x.split()
        for y in range(0,len(jatin)):
            try:
                jatin[y]=float(jatin[y])
            except:
                print "string found in file"
        #print jatin
        cmd_array.append(jatin)
    #print cmd_array
    #return cmd_array
    
    

def send_cordinate_to_robo(msg):
        global s, is_success
        try:
                print("Sending point to the robo")
                #s.send(str(msg.pose.position.x)+','+str(msg.pose.position.y)+','+str(msg.pose.position.z)+
                #       ','+str(msg.pose.orientation.x)+','+str(msg.pose.orientation.y)+','+str(msg.pose.orientation.z))
                s.send(str(msg[0]))  
                fed_value = s.recv(4096)
                if(fed_value =='next_point'):
                        s.send(str(msg[1]))
                        print(fed_value)# + "2")
                        fed_value = ""
                fed_value= s.recv(1024)
                if(fed_value =='next_point'):
                        s.send(str(msg[2]))
                        print(fed_value)# + "2")
                fed_value = s.recv(1024)
                if(fed_value =='next_point'):
                        s.send(str(msg[3]))
                        print(fed_value)# + "2")
                fed_value = s.recv(1024)
                if(fed_value =='next_point'):
                        s.send(str(msg[4]))
                        print(fed_value )#+ "2")
                fed_value=s.recv(1024)
                if(fed_value =='next_point'):
                        s.send(str(msg[5]))
                        print(fed_value )#+ "2")
                #s.send(str(msg.pose.orientation.w))
                print("Sent point to the robo")
                is_success=True                 
        except:
                print('Error')

if __name__ == '__main__':

        parser = argparse.ArgumentParser()
        parser.add_argument("-ip","--robot_ip_address", default = '192.168.98.94', help = "Specify the robot IP")
        parser.add_argument("-p","--robot_port", default = '1025', help = "specify the port")
        args = parser.parse_args()
        CONS_ROBOT_IP = args.robot_ip_address
        CONS_ROBOT_PORT = int(args.robot_port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #rospy.init_node('robot_socket_comm',anonymous=True)
        #rate = rospy.Rate(10)
        is_estabilished = False
        #pick_ready_pub = rospy.Publisher("/plc_modbus_control/robo_pick_ready", Float64 ,queue_size = 1)          
        #rospy.Subscriber("/plc_modbus_control/moveit_data", PoseStamped, send_cordinate_to_robo)
        #rospy.Subscriber("/have_points_for_robot", Float64 ,have_points_callback)
        is_success = True
        is_having_points = 0.0
        while True:
                try:
                        if not (is_estabilished):
                                print("Trying to establish connection with robot")
                                s.connect((CONS_ROBOT_IP,CONS_ROBOT_PORT))
                                is_estabilished = True
                                print('Connection Established')
                        if is_estabilished and is_success:      
                                print("Waiting for feedback")
                                feedback = s.recv(4096)
                                print(feedback )#+ "1")
                                if feedback == "success":
                                        openfile("demofile.txt")
                                        print"opening file"
                                        #print len(cmd_array)
                                        for a in range(0,len(cmd_array)):
                                            #print a
                                            print(cmd_array[a])
                                            send_cordinate_to_robo(cmd_array[a])
                                            is_success=False
                                            feedback = ""
                                            
                except socket.error as e:
                        print(e)
                        break
                except:
                        print ("Retrying Socket communication")
                        is_estabilished = False
                #'rate.sleep()
        s.close()

