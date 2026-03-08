# 智能车自主探索项目

本项目是一个基于 ROS1 `catkin` 工作空间的自主探索与导航方案，核心入口为 `explore_lite/launch/epl_auto.launch`。整体流程围绕仿真场景、车辆模型、SLAM 建图、`move_base` 导航和前沿点探索展开，并叠加了队伍自己的顶点约束、任务切换和巡航收尾逻辑。

项目适合以下场景：

- 在 Gazebo 中加载赛道或场馆模型并生成仿真环境
- 通过 Cartographer 建图并实时输出 `map`
- 使用 `move_base` 完成路径规划与底盘控制
- 使用 `explore_lite` 自动探索未知区域
- 在探索后切换到预设巡航路线或收尾任务

## 1. 核心入口

主入口文件：`src/explore_lite/launch/epl_auto.launch`

建议直接通过下面的命令启动完整流程：

```bash
cd /home/admin/catkin_ws
catkin_make
source devel/setup.bash
roslaunch explore_lite epl_auto.launch
```

如果只想切换世界模型或显示 Gazebo GUI，可以覆盖启动参数：

```bash
roslaunch explore_lite epl_auto.launch world_name:=venue gui:=true
```

默认参数：

- `world_name:=venue`
- `gui:=false`
- `run_camera:=false`
- `use_sim_time:=true`
- `robot_name:=racecar`

## 2. 启动链路说明

`epl_auto.launch` 会按如下顺序组织系统：

1. 启动 Gazebo 空世界，并加载 `bringup/worlds/venue.world`
2. 启动 `racecar_control/nav_sim.py`
3. 通过 `racecar_description` 生成车辆 URDF，并在 Gazebo 中生成 `racecar` 模型
4. 启动 `racecar_control.launch`，加载控制器、底盘控制和里程计发布
5. 启动 `cartographer_ros/demo_revo_lds.launch` 进行建图
6. 启动 `navi.launch`，拉起 `move_base`
7. 启动 RViz，加载 `explore_lite/include/simple.rviz`
8. 启动 `send_4.py`，向 `/clicked_point` 注入 4 个预设顶点
9. 启动 `vertex_building`，把顶点转发到 `/vertex` 并发布可视化 Marker
10. 启动 `explore.launch`，运行 `explore` 前沿探索节点
11. 启动 `end_handle.py`，根据识别结果切换到巡航或收尾任务

从系统功能上看，这个入口把“仿真、建图、导航、探索、任务收尾”一次性串了起来，是整个项目最关键的启动文件。

## 3. 主要模块职责

### 3.1 explore_lite 包

`src/explore_lite` 是本项目的主控包，除开上游 `explore_lite` 的前沿探索逻辑外，还加入了多份比赛自定义脚本。

关键文件：

- `launch/epl_auto.launch`：总入口
- `launch/navi.launch`：启动 `move_base` 并加载导航参数
- `launch/explore.launch`：启动 `explore` 自动探索节点
- `src/explore.cpp`：前沿探索主逻辑
- `src/frontier_search.cpp`：前沿搜索逻辑
- `src/vertex_building.cpp`：顶点采集与可视化
- `scripts/send_4.py`：自动发送 4 个顶点到 `/clicked_point`
- `scripts/navigator.py`：从 CSV 读取导航点并顺序发送给 `move_base`
- `scripts/end_handle.py`：监听 `/goal_if_find`，在探索结束后切换巡航/收尾任务
- `scripts/recorder.py`：记录 `move_base` 目标到 CSV

### 3.2 场景与车辆相关包

- `src/carlike_robot_sim/calf_carlike_robot/bringup`：世界文件、导航参数、启动辅助配置
- `src/carlike_robot_sim/calf_carlike_robot/car_sim/racecar_control`：底盘控制、控制器配置、仿真接口
- `src/venue_gazebo`：场景模型与 Gazebo world 资源

### 3.3 其他包

- `src/rrt_exploration`、`src/rrt_exploration_tutorials`：另一套基于 RRT 的探索方案，当前主入口未直接使用
- `src/stepback_recovery`：恢复行为插件

## 4. 工作流程

一次完整运行通常如下：

1. Gazebo 载入 `venue` 世界与赛车模型
2. Cartographer 使用激光数据持续建图，发布 `/map`
3. `move_base` 基于 `bringup/param` 中的参数完成全局与局部规划
4. `send_4.py` 自动向地图里投放 4 个顶点
5. `vertex_building` 将顶点发布到 `/vertex`，供探索逻辑使用
6. `explore` 在 `/map` 上搜索前沿点并持续下发目标
7. 当外部节点向 `/goal_if_find` 发布结果时，`end_handle.py` 触发巡航或收尾路线
8. `navigator.py` 读取 CSV 中记录的目标点，依次发送给 `move_base`

## 5. 目录结构

建议重点关注下面这些目录：

```text
catkin_ws/
├─ src/
│  ├─ explore_lite/
│  │  ├─ launch/
│  │  ├─ scripts/
│  │  ├─ src/
│  │  └─ doc/
│  ├─ carlike_robot_sim/
│  │  └─ calf_carlike_robot/
│  │     ├─ bringup/
│  │     └─ car_sim/
│  ├─ venue_gazebo/
│  ├─ rrt_exploration/
│  └─ stepback_recovery/
├─ build/
└─ devel/
```

## 6. 依赖说明

从代码和 launch 文件来看，运行本项目至少需要以下 ROS 组件：

- ROS1 `catkin`
- `gazebo_ros`
- `rviz`
- `xacro`
- `move_base`
- `cartographer_ros`
- `controller_manager`
- `robot_state_publisher`
- `costmap_2d`
- `actionlib`
- `tf`
- `geometry_msgs`
- `nav_msgs`
- `map_msgs`
- `move_base_msgs`
- `visualization_msgs`

如果你的环境里没有这些包，`roslaunch explore_lite epl_auto.launch` 会在启动阶段报缺包错误。

## 7. 编译方式

在工作空间根目录执行：

```bash
cd /home/admin/catkin_ws
catkin_make
source devel/setup.bash
```

如果你只改了 `explore_lite` 包，也仍然建议在整个工作空间下统一编译，避免跨包依赖没有同步更新。

## 8. 常用调试方法

### 8.1 查看系统是否正常启动

```bash
rosnode list
rostopic list
```

重点检查这些节点或话题是否存在：

- `/move_base`
- `/explore`
- `/vertex_building`
- `/map`
- `/clicked_point`
- `/vertex`
- `/goal_if_find`

### 8.2 手动查看导航目标

`navigator.py` 和 `end_handle.py` 使用 CSV 文件记录或回放导航点。相关文件在：

- `src/explore_lite/doc/move_base_data.csv`
- `src/explore_lite/doc/cruise.csv`
- `src/explore_lite/doc/finish_task.csv`

### 8.3 检查参数来源

`move_base` 主要读取 `bringup/param` 下的导航参数，例如：

- `costmap_common_params.yaml`
- `global_costmap_params.yaml`
- `local_costmap_params.yaml`
- `base_local_planner_params.yaml`

如果导航效果异常，通常先从这些参数排查。

## 9. 已知注意事项

### 9.1 脚本里存在硬编码路径

以下脚本默认把 CSV 文件写死在 `/home/admin/catkin_ws/src/explore_lite/doc/` 下：

- `scripts/navigator.py`
- `scripts/end_handle.py`
- `scripts/recorder.py`

如果你的工作空间根目录不是 `/home/admin/catkin_ws`，需要至少做其中一种处理：

1. 把工作空间放到对应路径
2. 修改脚本中的默认路径
3. 通过 ROS 参数覆盖相关 CSV 文件路径

否则会出现“文件不存在”或“巡航任务不执行”的问题。

### 9.2 `bringup` 与 `racecar_control` 是跨包依赖

`epl_auto.launch` 同时依赖：

- `bringup` 提供世界文件和导航参数
- `racecar_control` 提供车辆控制与里程计
- `racecar_description` 提供车辆模型
- `cartographer_ros` 提供建图

因此不能只单独拷贝 `explore_lite` 包运行。

### 9.3 探索前提

`explore` 节点依赖可用的 `/map`、TF 关系和 `move_base` action 服务。也就是说，探索功能建立在“SLAM 正常、导航正常、底盘控制正常”这三个前提上。

## 10. 推荐阅读顺序

如果你是第一次接手这个项目，建议按这个顺序看代码：

1. `src/explore_lite/launch/epl_auto.launch`
2. `src/explore_lite/launch/navi.launch`
3. `src/explore_lite/launch/explore.launch`
4. `src/explore_lite/scripts/send_4.py`
5. `src/explore_lite/src/vertex_building.cpp`
6. `src/explore_lite/scripts/end_handle.py`
7. `src/explore_lite/scripts/navigator.py`

这样可以最快理解整个系统是如何从“探索”切到“巡航/收尾”的。

## 11. 后续可改进项

为了让项目更稳定、便于移植，建议后续优先处理以下问题：

1. 去掉 Python 脚本中的硬编码路径，统一改成 ROS 参数
2. 在 README 中补充一张节点关系图或话题流图
3. 给 `epl_auto.launch` 增加更完整的参数说明
4. 为 CSV 巡航任务补充示例生成流程
