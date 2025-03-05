#include <ros/ros.h>
#include <geometry_msgs/Point.h>
#include <angles/angles.h>
#include <iostream>
#include <bits/stdc++.h>
#include <cmath>
#include <fstream>
#include <vector>
#include<sstream>
#include <cstdlib>


class Dijsktra{
    
    public:
        std::vector<std::vector<geometry_msgs::Point>> dijsktra(geometry_msgs::Point Start, geometry_msgs::Point Goal);
    
    private:
        struct Line{ int a,b;};
        int V, L;
        double getDistance(geometry_msgs::Point pt1, geometry_msgs::Point pt2);
        double getAngle(geometry_msgs::Point pt1, geometry_msgs::Point pt2);
        double line_dist(geometry_msgs::Point l_start, geometry_msgs::Point l_end, geometry_msgs::Point pt);
        geometry_msgs::Point find_intersection(geometry_msgs::Point pt1, geometry_msgs::Point pt2, geometry_msgs::Point pt3,bool &in_line);
        int minDistance(double dist[], bool sptSet[]);
        std::vector<int> dijkstra_index(std::vector<std::vector<double>> graph, int src, int dest);
        void read_points(std::vector<geometry_msgs::Point> &pts, std::vector<Line> &lns);
        void NearestLine(std::vector<geometry_msgs::Point> &pts, std::vector<Line> &lns);
        std::vector<std::vector<double>> generateGraph(std::vector<geometry_msgs::Point> &pts, std::vector<Line> &lns);


};