#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import PointStamped   # 举例：你要发 clicked_point

def wait_for_node(node_name, timeout=0):
    """
    阻塞直到 graph 里出现指定节点名
    timeout=0 表示一直等
    """
    import rosnode
    import time
    start = time.time()
    while not rospy.is_shutdown():
        if node_name in rosnode.get_node_names():
            rospy.loginfo('[%s] is up → continue', node_name)
            return True
        if timeout and (time.time() - start > timeout):
            rospy.logerr('[%s] not found after %.1f s', node_name, timeout)
            return False
        rospy.sleep(0.2)
    return False

def main():
    rospy.init_node('send5')
    if not wait_for_node('/vertex_building'):    
        rospy.signal_shutdown('vertex_building fail to start')
        return
    pub = rospy.Publisher('/clicked_point', PointStamped, queue_size=10)
    rospy.sleep(3)
    coor = [[-5, -6.8], [4.33, -6.8], [4.33, 7], [-5, 7]]
    for i in range(4):
        p = PointStamped()
        p.header.stamp = rospy.Time.now()
        p.header.frame_id = 'map'
        p.point.x = coor[i][0]
        p.point.y = coor[i][1]
        p.point.z = 0
        pub.publish(p)
        rospy.loginfo('sent  %d  x=%.1f', i, p.point.x)
        rospy.sleep(0.2)         

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass