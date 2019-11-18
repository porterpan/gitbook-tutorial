---
title: gym 运行常见错误及解决办法
localimage: image4
urlname: gym_run_error
categories:      
    gym    
tags: [gym,Deep Learning,Algorithm]
date: 2019-4-4 22:55:03
---

# 摘要



- [x] Edit By Porter, 积水成渊,蛟龙生焉。 

<!-- more -->

## 1. env.close()问题

### 1.1 问题1描述(TypeError: 'NoneType' object is not iterable)

> 当我们在pycharm或者其他IDE运行一段gym例子,程序结束时都会弹出这个错误提示

```shell
OK
Exception ignored in: <bound method Viewer.__del__ of <gym.envs.classic_control.rendering.Viewer object at 0x7f8758e0a4a8>>
Traceback (most recent call last):
  File "/home/porter/gym/gym/envs/classic_control/rendering.py", line 152, in __del__
  File "/home/porter/gym/gym/envs/classic_control/rendering.py", line 71, in close
  File "/home/porter/anaconda3/lib/python3.5/site-packages/pyglet/window/xlib/__init__.py", line 480, in close
  File "/home/porter/anaconda3/lib/python3.5/site-packages/pyglet/gl/xlib.py", line 345, in destroy
  File "/home/porter/anaconda3/lib/python3.5/site-packages/pyglet/gl/base.py", line 334, in destroy
  File "/home/porter/anaconda3/lib/python3.5/site-packages/pyglet/gl/xlib.py", line 335, in detach
  File "/home/porter/anaconda3/lib/python3.5/site-packages/pyglet/gl/lib.py", line 97, in errcheck
  File "<frozen importlib._bootstrap>", line 968, in _find_and_load
  File "<frozen importlib._bootstrap>", line 953, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 887, in _find_spec
TypeError: 'NoneType' object is not iterable

Process finished with exit code 0

```
### 1.2 解决

- 原因是，我们没在迭代结束后加上这句话

在代码迭代结束后加上这句代码

```python
env.close()
```

### 1.3 测试代码如下：

```python 
import gym
from time import sleep
env = gym.make('CartPole-v0')
i = 0
for i_episode in range(20):
    observation = env.reset()

    for step in range(100):
        env.render()
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(step+1))
            break
    i += 1
    print("i=", i, )
print("OK")
sleep(3)
env.close()
```

## 2. [在运行 ‘python circuit2_turtlebot_lidar_qlearn.py ’ 报错](https://blog.csdn.net/zhangdadadawei/article/details/78906103?utm_source=blogxgwz6)

### 2.1 错误提示

```shell
while processing /home/harish/gym-gazebo/gym_gazebo/envs/installation/catkin_ws/src/turtlebot_simulator/turtlebot_gazebo/launch/includes/kobuki.launch.xml:
Invalid tag: Cannot load command parameter [robot_description]: command [/opt/ros/kinetic/lib/xacro/xacro --inorder '/home/harish/gym-gazebo/gym_gazebo/envs/installation/catkin_ws/src/turtlebot/turtlebot_description/robots/kobuki_hexagons_asus_xtion_pro.urdf.xacro'] returned with code [2].
Param xml is 
The traceback for the exception was written to the log file
```

- PyCharm 中的错误提示

```shell
GAZEBO_MASTER_URI=http://localhost:10039

Traceback (most recent call last):
  File "/home/porter/gym-gazebo/examples/turtlebot/circuit_turtlebot_lidar_qlearn.py", line 24, in <module>
    env = gym.make('GazeboCircuitTurtlebotLidar-v0')
  File "/home/porter/gym/gym/envs/registration.py", line 155, in make
    return registry.make(id, **kwargs)
  File "/home/porter/gym/gym/envs/registration.py", line 100, in make
    env = spec.make(**kwargs)
  File "/home/porter/gym/gym/envs/registration.py", line 72, in make
    env = cls(**_kwargs)
  File "/home/porter/gym-gazebo/gym_gazebo/envs/turtlebot/gazebo_circuit_turtlebot_lidar.py", line 20, in __init__
    gazebo_env.GazeboEnv.__init__(self, "GazeboCircuitTurtlebotLidar_v0.launch")
  File "/home/porter/gym-gazebo/gym_gazebo/envs/gazebo_env.py", line 36, in __init__
    ros_path = os.path.dirname(subprocess.check_output(["which", "roscore"]))
  File "/home/porter/anaconda3/lib/python3.5/subprocess.py", line 316, in check_output
    **kwargs).stdout
  File "/home/porter/anaconda3/lib/python3.5/subprocess.py", line 398, in run
    output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['which', 'roscore']' returned non-zero exit status 1

Process finished with exit code 1
```

### 2.2 解决方法

使用gedit打开kobuki.launch.xml文件

```shell
gedit /home/zhw/gym-gazebo/gym_gazebo/envs/installation/catkin_ws/src/turtlebot_simulator/turtlebot_gazebo/launch/includes/kobuki.launch.xml
```
然后，将第六行替换成：
```shell
<arg name="urdf_file" default="$(find xacro)/xacro.py '$(find turtlebot_description)/robots/$(arg base)_$(arg stacks)_$(arg 3d_sensor).urdf.xacro'"/>
```

## 3. 

### 错误提示

```shell
Multiple packages found with the same name "ecl_mobile_robot":
- ecl_core/ecl_mobile_robot
- ecl_navigation/ecl_mobile_robot
setup_kinetic.bash: 行 80: devel/setup.bash: 没有那个文件或目录
```

### [解决方法](https://blog.csdn.net/qq_20989743/article/details/79936639)

- 打开gazebo.repos,修改如下部分：
改写,原来的内容为：
```shell
ecl_core:
    type: git
    url: https://github.com/stonier/ecl_core
    version: devel
  ecl_lite:
    type: git
    url: https://github.com/stonier/ecl_lite
    version: devel
  ecl_navigation:
    type: git
    url: https://github.com/stonier/ecl_navigation
    version: devel
  ecl_tools:
    type: git
    url: https://github.com/stonier/ecl_tools
    version: devel
```

改写为(将ecl_core、 ecl_lite 和ecl_tools 的版本号（version）改成： release/0.61-indigo-kinetic）

```shell
  ecl_core:
    type: git
    url: https://github.com/stonier/ecl_core
    version: release/0.61-indigo-kinetic
  ecl_lite:
    type: git
    url: https://github.com/stonier/ecl_lite
    version: release/0.61-indigo-kinetic
  ecl_navigation:
    type: git
    url: https://github.com/stonier/ecl_navigation
    version: release/0.61-indigo-kinetic
  ecl_tools:
    type: git
    url: https://github.com/stonier/ecl_tools
    version: release/0.61-indigo-kinetic
```
