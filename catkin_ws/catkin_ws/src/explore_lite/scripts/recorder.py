#!/usr/bin/env python3
import rospy
import csv
import os
from datetime import datetime
from move_base_msgs.msg import MoveBaseActionGoal

class MoveBaseGoalRecorder:
    def __init__(self):
        # 初始化节点
        rospy.init_node("move_base_goal_recorder", anonymous=True)
        
        # 配置文件路径（默认存放在用户目录下，文件名含时间戳）
        self.log_file = rospy.get_param(
            "~csvfile",  # 允许通过参数服务器修改文件路径
            f"/home/admin/catkin_ws/src/explore_lite/doc/finish_task.csv"
        )
        
        # 初始化 CSV 文件（写入表头）
        self.init_csv_file()
        
        # 计数器：记录导航点序号
        self.goal_count = 0
        
        # 订阅 move_base 的目标话题（move_base 发布目标时会触发此话题）
        self.goal_sub = rospy.Subscriber(
            "/move_base/goal",  # move_base 目标话题（固定话题名）
            MoveBaseActionGoal,  # 目标消息类型
            self.goal_callback,  # 回调函数
            queue_size=10
        )
        
        rospy.loginfo(f"导航点记录器已启动！日志文件：{self.log_file}")
        rospy.loginfo("等待接收 move_base 导航目标...")

    def init_csv_file(self):
        """初始化 CSV 文件，写入表头"""
        try:
            with open(self.log_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # 表头：序号、时间戳、x、y、z（位置）、x、y、z、w（姿态四元数）、坐标系
                writer.writerow([
                    "序号", "记录时间", 
                    "位置_x(m)", "位置_y(m)", "位置_z(m)",
                    "姿态_x", "姿态_y", "姿态_z", "姿态_w",
                    "坐标系_frame_id"
                ])
            rospy.loginfo(f"CSV 文件初始化成功：{self.log_file}")
        except Exception as e:
            rospy.logerr(f"创建 CSV 文件失败：{str(e)}")
            rospy.signal_shutdown("文件创建失败")

    def goal_callback(self, msg):
        """接收 move_base 目标消息的回调函数"""
        self.goal_count += 1
        
        # 提取关键信息
        record_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 精确到毫秒
        pose = msg.goal.target_pose.pose
        frame_id = msg.goal.target_pose.header.frame_id
        
        # 位置信息
        x = pose.position.x
        y = pose.position.y
        z = pose.position.z
        
        # 姿态四元数信息
        orient_x = pose.orientation.x
        orient_y = pose.orientation.y
        orient_z = pose.orientation.z
        orient_w = pose.orientation.w
        
        # 打印日志（终端可视化）
        rospy.loginfo(f"\n===== 记录导航点 {self.goal_count} =====")
        rospy.loginfo(f"记录时间：{record_time}")
        rospy.loginfo(f"位置：({x:.3f}, {y:.3f}, {z:.3f})")
        rospy.loginfo(f"姿态：({orient_x:.4f}, {orient_y:.4f}, {orient_z:.4f}, {orient_w:.4f})")
        rospy.loginfo(f"坐标系：{frame_id}")
        
        # 写入 CSV 文件
        self.write_to_csv([
            self.goal_count, record_time,
            round(x, 3), round(y, 3), round(z, 3),
            round(orient_x, 4), round(orient_y, 4), round(orient_z, 4), round(orient_w, 4),
            frame_id
        ])

    def write_to_csv(self, data):
        """将数据追加写入 CSV 文件"""
        try:
            with open(self.log_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(data)
        except Exception as e:
            rospy.logerr(f"写入 CSV 文件失败：{str(e)}")

if __name__ == "__main__":
    try:
        # 创建实例并保持节点运行
        recorder = MoveBaseGoalRecorder()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("导航点记录器已退出")
    except Exception as e:
        rospy.logerr(f"记录器异常退出：{str(e)}")