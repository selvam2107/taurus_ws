#!/usr/bin/env python3
import rospy
from hw_t.msg import LineSegmentList, LineSegment
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from std_msgs.msg import String
import math

marker_id = 0
# Distance threshold to consider lines as attached (in meters)
ATTACHMENT_THRESHOLD = 0.02  # 10 cm

# Callback function to process line segments
def line_segments_callback(msg):
    global marker_id
    attached_lines = []  # List to store the line segments that will be attached
    y="s"
    # Loop through each line segment
    for line in msg.line_segments:
        # Calculate the length of the line segment (Euclidean distance)
        x1, y1 = line.start[0], line.start[1]
        x2, y2 = line.end[0], line.end[1]
        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # Check if the length is 15 cm (0.15 meters)
        if abs(length - 0.15) < 0.01:  # Allowing a small tolerance
            rospy.loginfo("Found line of length 15 cm, checking for attached lines.")

            # Start by considering the current line as an attached line
            attached_lines.append([line])  # Each item is a list of lines attached together

    # Now, for each detected 15 cm line, check for attached lines
    for i in range(len(attached_lines)):
        current_group = attached_lines[i]  # Start with an empty group of lines

        # For each line in the group, check if it is attached to other lines
        for line in current_group:
            x1, y1 = line.start[0], line.start[1]
            x2, y2 = line.end[0], line.end[1]

            for other_line in msg.line_segments:
                if other_line not in current_group:  # Skip lines already in the group
                    # Calculate distance between the end of the current line and the start of another
                    dist_start = math.sqrt((other_line.start[0] - x2)**2 + (other_line.start[1] - y2)**2)
                    dist_end = math.sqrt((other_line.end[0] - x1)**2 + (other_line.end[1] - y1)**2)
                    
                    # Check if the distance is within the threshold (i.e., the lines are attached)
                    if dist_start < ATTACHMENT_THRESHOLD or dist_end < ATTACHMENT_THRESHOLD:
                        rospy.loginfo(f"Attached line found, distance: {dist_start} or {dist_end}")  # Add the attached line to the group
                        current_group.append(other_line)
                        length1 = math.sqrt((other_line.start[0] - other_line.end[0])**2 + (other_line.start[1] - other_line.end[1])**2)
                        # if abs(length1 - 0.15) < 0.03:
                        #     current_group.append(other_line)


        # Once all lines in the group are identified, create a marker to publish
        if len(current_group) > 3:  # Only publish if there are multiple lines attached
            rospy.loginfo(f"Publishing attached lines group {marker_id}")
            
            marker = Marker()
            marker.header.frame_id = "sick_link1"  # Adjust based on your frame
            marker.header.stamp = rospy.Time.now()
            marker.ns = "line_extractor"
            marker.id = marker_id
            marker.type = Marker.LINE_LIST  # Use LINE_LIST to connect all points at once
            marker.action = Marker.ADD

            # Set the line color (e.g., red)
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 1.0

            # Set the line width
            marker.scale.x = 0.05  # Line width (adjust as needed)

            # Add all points of the attached lines to the marker
            print("k",current_group,"h")
            # input()
            d={}
            l=[]
            d2={}
            l2=[]
            for line in current_group:
                start_point = Point(line.start[0], line.start[1], 0)
                end_point = Point(line.end[0], line.end[1], 0)
                mid=line.start[0]+line.end[0]/2
                mid1=line.start[1]+line.end[1]/2
                d[line.start[0]]=[mid,mid1]
                l.append([mid,mid1])
            print(l,"wdihbxjbi")
            print(len(l))
            for i in range(len(l)):
                print(l[i])
                # input()
                if i==3:
                    s=math.sqrt((l[i][0] - l[i][1])**2 + (l[0][0] - l[0][1])**2)
                else:
                    s=math.sqrt((l[i][0] - l[i][1])**2 + (l[i+1][0] - l[i+1][1])**2)
                d2[i]=s
                print(s)
            print(d2)
            for i in d2:
                l2.append(d2[i])
            maxi=max(l2)
            for i in d2:
                if d2[i]==maxi:
                    y=i
            print(y)
            current_group2=[]
            if y==0:
                current_group2.append(current_group[0])
                current_group2.append(current_group[1])
            if y==1:
                current_group2.append(current_group[1])
                current_group2.append(current_group[2])
            if y==2:
                current_group2.append(current_group[3])
                current_group2.append(current_group[4])
            if y==3:
                current_group2.append(current_group[4])
                current_group2.append(current_group[0])
            # input()
            for line in current_group2:
                # if current_group.index(line)==3:
                    start_point = Point(line.start[0], line.start[1], 0)
                    end_point = Point(line.end[0], line.end[1], 0)
                    y3=line.end[1]-line.start[1]
                    x3=line.end[0]-line.start[0]
                    m=y3/x3
                    m=str(m)
                   
                    print(d)
                    # input()
                    marker_pub1.publish(m)
                    # if slope
                    
                    marker.points.append(start_point)
                    marker.points.append(end_point)
            # for i in 
            # Publish the marker for the attached lines group
            marker_pub.publish(marker)
            marker_id += 1  # Increment marker ID for the next group
            print(d)
# Initialize ROS node and publisher
def listener():
    rospy.init_node('line_extractor', anonymous=True)
    
    # Publisher for the marker
    global marker_pub,marker_pub1
    marker_pub = rospy.Publisher('/line_markers2', Marker, queue_size=10)
    marker_pub1 = rospy.Publisher('/slope', String, queue_size=10)
    
    # Subscribe to the line segments topic
    rospy.Subscriber('/line_segments', LineSegmentList, line_segments_callback)
    
    rospy.spin()

if __name__ == '__main__':
    listener()
