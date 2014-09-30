#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_demos/license/LICENSE
#

import os
import subprocess

import rospy
import map_store.srv as map_store_srvs

def process_save_map(req):
    map_path = os.path.expanduser(rospy.get_param('map_path'))
    filename = map_path+rospy.get_param('filename', req.map_name)
    map_topic = rospy.get_param('map_topic', '/map')
    tmp_name = filename + '_ori'
    tmp_output = subprocess.check_output(['rosrun','map_server','map_saver','-f',tmp_name, 'map:=%s'%map_topic])
    rospy.sleep(2.0)
    tmp_name = tmp_name + '.yaml'
    crop_output = subprocess.check_output(['rosrun','map_server','crop_map',tmp_name,filename])
    rospy.loginfo('Map Saved into %s'%str(filename))
    return map_store_srvs.SaveMapResponse()

if __name__ == '__main__':
    rospy.init_node('map_saver_with_crop',anonymous=True)
    srv_saver = rospy.Service('save_map', map_store_srvs.SaveMap, process_save_map)
    rospy.spin()
