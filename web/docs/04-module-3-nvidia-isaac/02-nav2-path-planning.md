---
sidebar_position: 2
title: Nav2 Path Planning
---

# Nav2 Path Planning

## Introduction to Navigation 2 (Nav2)

Navigation 2 (Nav2) is the ROS 2 navigation framework designed for mobile robot navigation. It provides a complete stack for path planning, obstacle avoidance, and autonomous navigation. For humanoid robots, Nav2 can be adapted for whole-body navigation and path planning.

## Nav2 Architecture

### Core Components
- **Lifecycle Manager**: Manages the state of navigation components
- **Planner Server**: Global path planning
- **Controller Server**: Local path following and obstacle avoidance
- **Recovery Server**: Recovery behaviors for navigation failures
- **BT Navigator**: Behavior Tree-based navigation executive

### Behavior Trees in Nav2
Nav2 uses Behavior Trees (BT) to orchestrate navigation tasks:
- **Sequential execution**: Tasks execute in order
- **Fallback mechanisms**: Alternative behaviors when tasks fail
- **Reactive behaviors**: Respond to environment changes
- **Modular design**: Easy to customize and extend

## Global Path Planning

### A* and Dijkstra Algorithms
Nav2 includes multiple global planners:
- **NavFn**: Uses Dijkstra's algorithm for global planning
- **GlobalPlanner**: Implementation of A* algorithm
- **Theta* Planners**: Any-angle path planning for smoother paths

### Costmap-2D Integration
Global planners work with costmaps to account for obstacles:
- **Static Layer**: Static map of the environment
- **Obstacle Layer**: Dynamic obstacles from sensors
- **Inflation Layer**: Safety margins around obstacles

### Example Global Planner Configuration
```yaml
global_planner:
  ros__parameters:
    planner_frequency: 1.0
    use_rclcpp_node_options: true
    allow_unknown_grids: false
    expected_planner_frequency: 20.0
    type: "nav2_navfn_planner/NavfnPlanner"
    NavfnPlanner:
      tolerance: 0.5
      use_astar: false
      allow_unknown: true
```

## Local Path Planning and Control

### Trajectory Rollout
Local planners generate and evaluate multiple trajectories:
- **Dynamic Window Approach (DWA)**: Considers robot dynamics
- **Timed Elastic Band (TEB)**: Optimizes trajectories over time
- **MPC (Model Predictive Control)**: Predictive control approach

### Controller Server
The controller server executes local path following:
- **FollowPath Action**: Follows a given global path
- **Velocity Control**: Sends velocity commands to robot base
- **Obstacle Avoidance**: Adjusts path to avoid obstacles

### Example Controller Configuration
```yaml
local_planner:
  ros__parameters:
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.001
    min_theta_velocity_threshold: 0.001
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # Progress checker parameters
    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0

    # Goal checker parameters
    goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
      stateful: True

    # FollowPath controller parameters
    FollowPath:
      plugin: "nav2_rotation_shim_controller::RotationShimController"
      rotational_scaler: 1.5
      max_angular_accel: 3.2
      max_angular_vel: 1.5
      min_angular_vel: 0.4
```

## Nav2 for Humanoid Robots

### Challenges with Humanoid Navigation
Humanoid robots present unique challenges for navigation:
- **Stability**: Maintaining balance during navigation
- **Footstep Planning**: Planning stable footstep sequences
- **Upper Body Motion**: Coordinating arm and torso movements
- **Dynamic Center of Mass**: Changing during locomotion

### Footstep Planners
For humanoid robots, special footstep planners are needed:
- **Footstep Planner**: Plans stable footstep locations
- **ZMP-based Planning**: Zero Moment Point for balance
- **Capture Point Planning**: Dynamic balance consideration

### Whole-Body Navigation
- **Center of Mass Planning**: Plan CoM trajectory for stability
- **Multi-Contact Planning**: Consider multiple support contacts
- **Posture Planning**: Plan upper body posture during navigation

## Recovery Behaviors

### Built-in Recovery Actions
Nav2 includes several recovery behaviors:
- **Spin**: Rotate in place to clear local minima
- **Backup**: Move backward to escape obstacles
- **Wait**: Pause briefly to allow dynamic obstacles to clear

### Custom Recovery Behaviors
For humanoid robots, custom recovery behaviors may be needed:
- **Stance Adjustment**: Adjust foot positioning
- **Balance Recovery**: Regain balance if lost
- **Step Recovery**: Adjust footsteps to regain stability

### Recovery Configuration
```yaml
recovery_server:
  ros__parameters:
    costmap_topic: "local_costmap/costmap_raw"
    footprint_topic: "local_costmap/published_footprint"
    cycle_frequency: 10.0
    recovery_plugins: ["spin", "backup", "wait"]
    spin:
      plugin: "nav2_recoveries/Spin"
      spin_dist: 1.57
    backup:
      plugin: "nav2_recoveries/BackUp"
      backup_dist: 0.15
      backup_speed: 0.025
    wait:
      plugin: "nav2_recoveries/Wait"
      wait_duration: 1.0
```

## Navigation Safety

### Costmap Configuration
Proper costmap configuration is critical for safe navigation:
- **Inflation parameters**: Ensure adequate safety margins
- **Obstacle detection**: Proper sensor configuration
- **Dynamic obstacles**: Handle moving objects appropriately

### Velocity Limiting
- **Speed limits**: Set appropriate velocity limits for robot
- **Acceleration limits**: Smooth velocity changes
- **Emergency stops**: Implement safety stop mechanisms

## Performance Optimization

### Parameter Tuning
Key parameters for performance:
- **Frequency settings**: Balance update rates with performance
- **Costmap resolution**: Balance accuracy with computation
- **Path planning resolution**: Match to robot capabilities

### Multi-Threading
- **Thread configuration**: Optimize for available CPU cores
- **Resource management**: Prevent contention between components

## Integration with Perception Systems

### Sensor Fusion
Nav2 integrates with various perception systems:
- **LIDAR**: Primary obstacle detection
- **Cameras**: Visual obstacle detection and semantic mapping
- **IMU**: Motion and orientation data
- **Wheel encoders**: Odometry information

### SLAM Integration
- **Mapping**: Create maps for navigation
- **Localization**: Determine robot position in map
- **Dynamic updates**: Update maps with new information

## Debugging and Visualization

### RViz2 Integration
Nav2 provides extensive visualization in RViz2:
- **Path visualization**: Show planned and executed paths
- **Costmap visualization**: Display obstacle information
- **Robot state**: Show current robot status

### Logging and Monitoring
- **Navigation logs**: Detailed navigation execution logs
- **Performance metrics**: Track navigation success rates
- **Error analysis**: Identify navigation failures

## Best Practices

1. **Start with defaults**: Use default parameters initially, then tune
2. **Safety first**: Always configure safety margins appropriately
3. **Test incrementally**: Add features gradually and test each step
4. **Monitor performance**: Track navigation metrics during operation
5. **Regular validation**: Ensure navigation behavior matches expectations

## Summary

Nav2 provides a comprehensive navigation framework for mobile robots that can be adapted for humanoid robots. Understanding its architecture, components, and configuration options is essential for implementing safe and effective navigation. For humanoid robots, special consideration must be given to balance, footstep planning, and whole-body coordination during navigation tasks.