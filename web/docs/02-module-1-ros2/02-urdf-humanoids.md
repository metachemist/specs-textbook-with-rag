---
sidebar_position: 2
title: URDF for Humanoid Robots
---

# URDF for Humanoid Robots

## Introduction to URDF

URDF (Unified Robot Description Format) is an XML format used in ROS to describe robot models. It defines the physical and visual properties of a robot, including its links, joints, and other components.

## Basic URDF Structure

A URDF file typically includes:
- **Links**: Rigid parts of the robot (e.g., arms, legs, torso)
- **Joints**: Connections between links (e.g., revolute, prismatic, fixed)
- **Visual**: How the robot appears in simulation
- **Collision**: How the robot interacts physically with the environment
- **Inertial**: Mass properties for physics simulation

### Example URDF Structure

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.083" ixy="0.0" ixz="0.0" iyy="0.083" iyz="0.0" izz="0.083"/>
    </inertial>
  </link>
</robot>
```

## Links

Links represent rigid bodies in the robot. Each link can have:
- Visual properties (shape, color, material)
- Collision properties (shape for physics simulation)
- Inertial properties (mass, center of mass, inertia tensor)

## Joints

Joints connect links and define how they can move relative to each other. Common joint types:
- **Fixed**: No movement between links
- **Revolute**: Rotational movement around an axis
- **Prismatic**: Linear movement along an axis
- **Continuous**: Continuous rotation (like a revolute joint without limits)
- **Floating**: 6-DOF movement
- **Planar**: Movement on a plane

### Joint Example

```xml
<joint name="joint_name" type="revolute">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="0.0 0.0 0.0" rpy="0.0 0.0 0.0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
</joint>
```

## URDF for Humanoid Robots

Humanoid robots have special requirements in their URDF:

### Kinematic Chain Structure
- Multiple limbs (arms, legs) with appropriate joint limits
- Torso and head for upper body movement
- Specialized hands for manipulation

### Example Humanoid Joint Structure
```
base_link
├── torso
│   ├── head
│   ├── left_arm
│   │   ├── left_forearm
│   │   └── left_hand
│   ├── right_arm
│   │   ├── right_forearm
│   │   └── right_hand
│   ├── left_leg
│   │   └── left_foot
│   └── right_leg
│       └── right_foot
```

## Advanced URDF Features

### Materials
```xml
<material name="blue">
  <color rgba="0.0 0.0 0.8 1.0"/>
</material>
```

### Transmission Elements
For controlling joints with actuators:
```xml
<transmission name="tran1">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="joint1">
    <hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
  </joint>
  <actuator name="motor1">
    <hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

### Gazebo-Specific Elements
URDF can include Gazebo-specific elements:
```xml
<gazebo reference="link_name">
  <material>Gazebo/Blue</material>
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
</gazebo>
```

## Best Practices for Humanoid URDF

1. **Use consistent naming**: Follow a clear convention for links and joints
2. **Set appropriate joint limits**: Ensure they reflect the physical capabilities of the robot
3. **Include proper inertial properties**: Critical for stable simulation
4. **Use separate files**: Break complex robots into multiple files using `<xacro>` or `<include>`
5. **Validate URDF**: Use tools like `check_urdf` to verify correctness

## Summary

URDF is fundamental for representing humanoid robots in ROS. Properly designed URDF files enable accurate simulation, visualization, and control of complex humanoid systems. When designing URDF for humanoid robots, special attention must be paid to the kinematic structure, joint limits, and physical properties to ensure realistic behavior in simulation and proper control in the real world.