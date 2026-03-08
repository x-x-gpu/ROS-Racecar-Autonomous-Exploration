#!/usr/bin/env python3
import rospy
import csv
import os
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose, Point, Quaternion
from datetime import datetime

class CsvLoopNavigator:
    def __init__(self):
        # 初始化节点
        rospy.init_node("csv_loop_navigator", anonymous=True)
        
        # 配置参数（通过参数服务器指定，支持启动时修改）
        self.csv_file = rospy.get_param(
            "~_csv_file",
            "/home/admin/catkin_ws/src/explore_lite/doc/move_base_data.csv"
        )
        self.wait_timeout = rospy.get_param("~_timeout", 60.0)  # 单个目标超时时间（秒）(0=持续阻塞)
        self.loop_count = rospy.get_param("~_loop_count", 1)  # 循环次数（0=无限循环）
        
        # 存储导航点和当前循环索引
        self.goals = []
        self.current_loop = 0
        
        # 连接 move_base action 服务器
        rospy.loginfo("正在连接 move_base 服务器...")
        self.move_base_client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        if not self.move_base_client.wait_for_server(rospy.Duration(10.0)):
            rospy.logerr("错误：无法连接 move_base 服务器！")
            rospy.signal_shutdown("连接服务器失败")
            exit(1)
        rospy.loginfo("move_base 服务器连接成功！")
        
        # 检查文件并解析导航点
        self.check_file()
        self.parse_csv()
        
        # 打印启动信息
        rospy.loginfo("="*60)
        rospy.loginfo("CSV循环导航器（send_goal版）已启动！")
        rospy.loginfo(f"CSV文件路径：{self.csv_file}")
        rospy.loginfo(f"导航点总数：{len(self.goals)}")
        rospy.loginfo(f"单个目标超时：{self.wait_timeout}秒")
        rospy.loginfo(f"循环次数：{'无限循环' if self.loop_count == 0 else str(self.loop_count) + ' 次'}")
        rospy.loginfo("="*60)
        
        # 开始导航
        self.start_navigation()

    def check_file(self):
        """检查CSV文件是否存在"""
        if not os.path.exists(self.csv_file):
            rospy.logerr(f"错误：CSV文件不存在 -> {self.csv_file}")
            rospy.signal_shutdown("文件不存在")
            exit(1)

    def parse_csv(self):
        """解析CSV文件，提取导航点数据"""
        try:
            with open(self.csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.goals.append({
                        "position": Point(
                            x=float(row["位置_x(m)"]),
                            y=float(row["位置_y(m)"]),
                            z=float(row["位置_z(m)"])
                        ),
                        "orientation": Quaternion(
                            x=float(row["姿态_x"]),
                            y=float(row["姿态_y"]),
                            z=float(row["姿态_z"]),
                            w=float(row["姿态_w"])
                        ),
                        "frame_id": row["坐标系_frame_id"]
                    })
            if not self.goals:
                rospy.logerr("错误：CSV文件中无有效导航点！")
                rospy.signal_shutdown("无导航点数据")
                exit(1)
        except Exception as e:
            rospy.logerr(f"解析CSV失败：{str(e)}")
            rospy.signal_shutdown("解析失败")
            exit(1)

    def send_nav_goal(self, goal_data):
        """使用 send_goal 发送导航目标，等待执行结果"""
        # 创建 MoveBaseGoal 消息
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = goal_data["frame_id"]
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(
            position=goal_data["position"],
            orientation=goal_data["orientation"]
        )
        
        # 发送目标并等待结果
        rospy.loginfo(f"\n发送导航目标：")
        rospy.loginfo(f"  位置：({goal_data['position'].x:.3f}, {goal_data['position'].y:.3f})")
        rospy.loginfo(f"  坐标系：{goal_data['frame_id']}")
        rospy.loginfo(f"  超时时间：{self.wait_timeout}秒")
        
        self.move_base_client.send_goal(goal)
        success = self.move_base_client.wait_for_result(rospy.Duration(self.wait_timeout))
        
        # 处理结果
        if success:
            rospy.loginfo("✅ 导航目标达成！")
            return True
        else:
            rospy.logerr("❌ 导航失败（超时或被取消）")
            self.move_base_client.cancel_goal()
            return False

    def start_navigation(self):
        """按指定循环次数执行导航"""
        # 无限循环模式（loop_count=0）
        if self.loop_count == 0:
            rospy.loginfo("\n开始无限循环导航... 按 Ctrl+C 退出")
            while not rospy.is_shutdown():
                self.execute_one_loop()
                if rospy.is_shutdown():
                    break
                rospy.loginfo(f"\n--- 无限循环：完成一轮，2秒后开始下一轮 ---")
                rospy.sleep(2.0)
        
        # 有限循环模式（loop_count>0）
        else:
            rospy.loginfo(f"\n开始有限循环导航（共 {self.loop_count} 次）...")
            while not rospy.is_shutdown() and self.current_loop < self.loop_count:
                self.current_loop += 1
                rospy.loginfo(f"\n" + "="*40)
                rospy.loginfo(f"  执行第 {self.current_loop}/{self.loop_count} 轮循环")
                rospy.loginfo("="*40)
                
                self.execute_one_loop()
                
                # 检查是否完成所有循环
                if self.current_loop >= self.loop_count:
                    rospy.loginfo(f"\n🎉 所有 {self.loop_count} 轮循环已完成！")
                    break
                
                rospy.loginfo(f"\n--- 第 {self.current_loop} 轮完成，2秒后开始第 {self.current_loop+1} 轮 ---")
                rospy.sleep(2.0)
        
        # 导航结束，关闭节点
        rospy.loginfo("\n导航任务结束，正在退出...")
        rospy.signal_shutdown("导航完成")

    def execute_one_loop(self):
        """执行一轮完整的导航（所有导航点按顺序执行）"""
        for idx, goal in enumerate(self.goals, 1):
            if rospy.is_shutdown():
                break
            rospy.loginfo(f"\n--- 第 {idx}/{len(self.goals)} 个导航点 ---")
            # 发送目标并等待完成（失败不中断，继续下一个点）
            self.send_nav_goal(goal)

if __name__ == "__main__":
    try:
        navigator = CsvLoopNavigator()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("导航器被用户中断，已退出")
    except Exception as e:
        rospy.logerr(f"导航器异常：{str(e)}")