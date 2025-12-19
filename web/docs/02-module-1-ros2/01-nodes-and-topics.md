---
sidebar_position: 1
title: Nodes and Topics
---

# Nodes and Topics in ROS 2

## Introduction to ROS 2

ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

## Nodes

A node is a process that performs computation. ROS 2 is designed with a distributed architecture where nodes can be grouped in different processes or even run on different machines. Nodes communicate with each other through:

- Messages (passed via topics)
- Services
- Actions

### Creating a Node

In ROS 2, nodes are implemented using client libraries such as `rclpy` for Python or `rclcpp` for C++. Here's a basic example of a node in Python:

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1
```

## Topics

Topics are named buses over which nodes exchange messages. They enable asynchronous many-to-many communication between nodes using a publish/subscribe pattern.

### Publishers and Subscribers

- **Publishers**: Send messages to a topic
- **Subscribers**: Receive messages from a topic

### Quality of Service (QoS)

ROS 2 introduces Quality of Service settings that allow you to configure how messages are delivered, including:
- Reliability (reliable vs. best effort)
- Durability (transient local vs. volatile)
- History (keep last vs. keep all)

## Services

Services provide a request/reply communication pattern. A service client sends a request message and waits for a reply message from a service server.

## Actions

Actions are like services, but they are designed for long-running tasks. They provide feedback during execution and can be canceled.

## Practical Example: Humanoid Robot Control

In a humanoid robot system, nodes might include:
- Sensor processing nodes (processing data from cameras, IMUs, etc.)
- Motion planning nodes (determining how to move the robot)
- Motor control nodes (sending commands to actuators)
- Perception nodes (understanding the environment)

These nodes communicate through topics carrying sensor data, motor commands, and other information needed for coordinated robot behavior.

## Summary

Nodes and topics form the foundation of communication in ROS 2. Understanding these concepts is crucial for developing robotic systems, especially complex ones like humanoid robots where multiple subsystems need to coordinate seamlessly.