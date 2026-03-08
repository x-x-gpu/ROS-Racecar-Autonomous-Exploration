#include <ros/ros.h>
#include <geometry_msgs/PointStamped.h>
#include <geometry_msgs/Point.h>
#include <visualization_msgs/Marker.h>
#include <std_msgs/ColorRGBA.h>
#include <vector>

using namespace std;

vector<geometry_msgs::Point> blacklist_points;  
ros::Publisher blacklist_pub;
ros::Publisher marker_pub;
visualization_msgs::Marker marker;

void callback(const geometry_msgs::PointStamped::ConstPtr& msg)
{
    ROS_INFO("Add prepared blacklist point:(%.2f, %.2f)", msg->point.x, msg->point.y);
    blacklist_points.push_back(msg->point);
    blacklist_pub.publish(msg->point);
    marker.header.stamp = ros::Time::now();
    marker.points.clear(); 
    marker.points = blacklist_points; 
    marker_pub.publish(marker);
}

int main(int argc, char** argv) {
    ros::init(argc, argv, "vertex_building");
    ros::NodeHandle nh;
    ros::NodeHandle pnh ("~");

    blacklist_pub = nh.advertise<geometry_msgs::Point>("/vertex", 10);
    marker_pub = pnh.advertise<visualization_msgs::Marker>("/vertex_marker", 10, true);  // latch=true

    std_msgs::ColorRGBA yellow;
    yellow.r = 1.0;
    yellow.g = 1.0;
    yellow.b = 0.0;
    yellow.a = 1.0; 

    marker.header.frame_id = "map";       
    marker.header.stamp = ros::Time::now();
    marker.action = visualization_msgs::Marker::ADD; 
    marker.type = visualization_msgs::Marker::POINTS;
    marker.scale.x = 0.2;  
    marker.scale.y = 0.2;
    marker.color = yellow; 
    marker.lifetime = ros::Duration(0); 

    ros::Subscriber sub = nh.subscribe("/clicked_point", 10, callback);

    ROS_INFO("Simple Blacklist Publisher Started!");
    ROS_INFO("RViz Fixed Frame must be 'map', click map to add purple blacklist points");
    ros::spin();
    return 0;
}