#!/usr/bin/env python3
import rospy
import subprocess
import time
import signal
import os
from std_msgs.msg import Int32

class GoalOrderNavigator:
    def __init__(self):
        # 初始化节点
        rospy.init_node("goal_order_navigator", anonymous=True)
        
        # 配置参数
        self.navigator_node = "navigator.py"  # 导航节点文件名
        self.navigator_package = "explore_lite"   # 导航节点所属包名
        self.cruise_csv = "/home/admin/catkin_ws/src/explore_lite/doc/cruise.csv"
        self.finish_csv = "/home/admin/catkin_ws/src/explore_lite/doc/finish_task.csv"
        
        # 状态变量
        self.received_1 = False          # 是否收到过 1
        self.received_2 = False          # 是否收到过 2
        self.cruise_process = None       # cruise.csv 进程句柄（用于强制关闭）
        self.is_cruise_running = False   # cruise.csv 是否正在运行
        self.is_finish_executed = False  # finish_task.csv 是否已执行（确保只执行一次）
        
        # 订阅 /goal_if_find 话题
        self.sub = rospy.Subscriber(
            "/goal_if_find",
            Int32,
            self.goal_callback,
            queue_size=10
        )
        
        # 注册退出信号处理
        rospy.on_shutdown(self.shutdown_handler)
        
        rospy.loginfo("="*60)
        rospy.loginfo("目标顺序导航控制器已启动！")
        rospy.loginfo("核心逻辑：")
        rospy.loginfo("1. 收到 1 且未收 2 → 启动 cruise.csv")
        rospy.loginfo("2. cruise 自然结束 → 执行 finish_task.csv")
        rospy.loginfo("3. 收到 2 且 cruise 运行 → 关闭 cruise → 执行 finish_task.csv")
        rospy.loginfo("等待接收 /goal_if_find 话题消息（响应 1 和 2）...")
        rospy.loginfo(f"cruise.csv 路径：{self.cruise_csv}")
        rospy.loginfo(f"finish_task.csv 路径：{self.finish_csv}")
        rospy.loginfo("="*60)

    def goal_callback(self, msg):
        """接收 /goal_if_find 消息的回调函数"""
        data = msg.data
        
        # 只处理 1 和 2，忽略其他值
        if data not in [1, 2]:
            rospy.loginfo(f"收到无效消息：{data}，仅处理 1 和 2")
            return
        
        if data == 1:
            self.handle_msg_1()
        elif data == 2:
            self.handle_msg_2()

    def handle_msg_1(self):
        """处理收到消息 1 的逻辑"""
        if not self.received_1:
            self.received_1 = True
            rospy.loginfo(f"📌 收到目标消息：1")
            
            # 未收到过 2 且 cruise 未运行 → 启动 cruise.csv
            if not self.received_2 and not self.is_cruise_running and not self.is_finish_executed:
                rospy.loginfo("✅ 未收到过 2，启动 cruise.csv...")
                # 在新线程中运行 cruise（避免阻塞回调）
                import threading
                cruise_thread = threading.Thread(target=self.run_cruise)
                cruise_thread.daemon = True
                cruise_thread.start()
            else:
                rospy.loginfo("⚠️  不启动 cruise.csv（原因：已收到 2 / cruise 正在运行 / finish 已执行）")

    def handle_msg_2(self):
        """处理收到消息 2 的逻辑"""
        if not self.received_2:
            self.received_2 = True
            rospy.loginfo(f"📌 收到目标消息：2")
            
            # cruise 正在运行 → 强制关闭并执行 finish_task
            if self.is_cruise_running and not self.is_finish_executed:
                rospy.loginfo("🛑 cruise.csv 正在运行，强制关闭并启动 finish_task.csv...")
                self.stop_cruise()
                self.run_finish_task()
            else:
                rospy.loginfo("⚠️  不执行关闭操作（原因：cruise 未运行 / finish 已执行）")

    def run_cruise(self):
        """启动 cruise.csv 并监控进程状态"""
        if not os.path.exists(self.cruise_csv):
            rospy.logerr(f"❌ 错误：cruise.csv 不存在 -> {self.cruise_csv}")
            return
        
        # 构建 rosrun 命令
        cmd = (
            f"rosrun {self.navigator_package} {self.navigator_node} "
            f"_csv_file:={self.cruise_csv} "
            f"_loop_count:=1 "
            f"_timeout:=60"
        )
        
        rospy.loginfo(f"\n" + "="*50)
        rospy.loginfo(f"启动 cruise.csv：{cmd}")
        rospy.loginfo("="*50)
        
        self.is_cruise_running = True
        try:
            # 启动子进程（记录进程句柄，用于后续关闭）
            self.cruise_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid,  # 设置进程组，方便批量杀死
                text=True
            )
            
            # 实时打印输出
            while self.is_cruise_running and self.cruise_process.poll() is None:
                if stdout := self.cruise_process.stdout.readline():
                    rospy.loginfo(f"[cruise输出] {stdout.strip()}")
                if stderr := self.cruise_process.stderr.readline():
                    rospy.logerr(f"[cruise错误] {stderr.strip()}")
                time.sleep(0.1)
            
            # 进程自然退出后，执行 finish_task
            if not self.is_finish_executed:
                rospy.loginfo("\n✅ cruise.csv 自然结束，启动 finish_task.csv...")
                self.run_finish_task()
        
        except Exception as e:
            rospy.logerr(f"\n❌ 执行 cruise.csv 失败：{str(e)}")
            if not self.is_finish_executed:
                self.run_finish_task()
        finally:
            self.is_cruise_running = False
            self.cruise_process = None

    def stop_cruise(self):
        """强制关闭 cruise.csv 进程"""
        if self.cruise_process and self.is_cruise_running:
            try:
                # 杀死进程组（确保所有子进程都被关闭）
                os.killpg(os.getpgid(self.cruise_process.pid), signal.SIGINT)
                # 等待进程退出
                self.cruise_process.wait(timeout=5)
                rospy.loginfo(f"✅ cruise.csv 已强制关闭（PID：{self.cruise_process.pid}）")
            except Exception as e:
                rospy.logerr(f"❌ 关闭 cruise.csv 失败：{str(e)}")
            finally:
                self.is_cruise_running = False
                self.cruise_process = None

    def run_finish_task(self):
        """执行 finish_task.csv（确保只执行一次）"""
        if self.is_finish_executed:
            rospy.loginfo("⚠️ finish_task.csv 已执行过，跳过")
            return
        
        if not os.path.exists(self.finish_csv):
            rospy.logerr(f"❌ 错误：finish_task.csv 不存在 -> {self.finish_csv}")
            self.is_finish_executed = True
            return
        
        # 构建 rosrun 命令
        cmd = (
            f"rosrun {self.navigator_package} {self.navigator_node} "
            f"_csv_file:={self.finish_csv} "
            f"_loop_count:=1 "
            f"_timeout:=60"
        )
        
        rospy.loginfo(f"\n" + "="*50)
        rospy.loginfo(f"启动 finish_task.csv：{cmd}")
        rospy.loginfo("="*50)
        
        self.is_finish_executed = True
        try:
            # 启动进程并等待完成
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid,
                text=True
            )
            
            # 实时打印输出
            while process.poll() is None:
                if stdout := process.stdout.readline():
                    rospy.loginfo(f"[finish输出] {stdout.strip()}")
                if stderr := process.stderr.readline():
                    rospy.logerr(f"[finish错误] {stderr.strip()}")
                time.sleep(0.1)
            
            process.wait(timeout=10)
            if process.returncode == 0:
                rospy.loginfo(f"\n✅ finish_task.csv 执行成功！")
            else:
                rospy.logerr(f"\n❌ finish_task.csv 异常退出（返回码：{process.returncode}）")
        
        except Exception as e:
            rospy.logerr(f"\n❌ 执行 finish_task.csv 失败：{str(e)}")
        
        # 所有任务完成，退出节点
        rospy.loginfo("\n" + "="*60)
        rospy.loginfo("🎉 所有导航任务已完成，节点将退出")
        rospy.loginfo("="*60)
        rospy.signal_shutdown("所有任务完成")

    def shutdown_handler(self):
        """节点退出时的清理操作"""
        rospy.loginfo("\n正在清理资源...")
        if self.is_cruise_running and self.cruise_process:
            self.stop_cruise()
        rospy.loginfo("节点已退出")

if __name__ == "__main__":
    try:
        controller = GoalOrderNavigator()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("目标顺序导航控制器已退出")
    except Exception as e:
        rospy.logerr(f"控制器异常：{str(e)}")