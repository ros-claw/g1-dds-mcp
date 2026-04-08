# Tools Usage Guide: Unitree G1

## Essential Tools

### Movement Control

#### `stand_up()`
Transition robot from sitting/lying to standing position.

**When to use**: Before any walking or manipulation task.

**Safety**: Ensure adequate clearance above (2m) and around (1m radius).

---

#### `sit_down()`
Safely lower robot to sitting position.

**When to use**: End of session, low battery, or emergency shutdown.

**Safety**: Robot will freeze until fully seated.

---

#### `walk_forward(speed: float, duration: float)`
Walk forward at specified speed for duration.

**Parameters**:
- `speed`: 0.0 to 1.5 m/s (start with 0.1 for testing)
- `duration`: Seconds to walk

**When to use**: Locomotion tasks.

**Safety**:
- Verify ground is flat and clear
- Start with slow speed (0.1)
- Monitor IMU for stability

---

### Joint Control

#### `move_joint(joint_id: int, position: float, velocity: float)`
Move a specific joint to target position.

**Parameters**:
- `joint_id`: Joint name or index (0-22 for 23-DOF)
- `position`: Target angle in radians
- `velocity`: Max velocity in rad/s (0.1 to 5.0)

**Joint Names**:
- Legs: `left_hip_pitch`, `left_knee`, `right_ankle_roll`, etc.
- Arms: `right_shoulder_pitch`, `left_elbow`, etc.
- Torso: `waist_yaw`, `waist_pitch`, `waist_roll`
- Head: `head_yaw`, `head_pitch`

**When to use**: Precise manipulation or pose adjustment.

**Safety**: Check joint limits in e_urdf.json before commanding.

---

#### `get_joint_states()`
Get current positions, velocities, and torques of all joints.

**Returns**: Dictionary with joint states.

**When to use**: Before/after movement to verify state.

---

### State Monitoring

#### `get_battery_level()`
Get current battery percentage.

**Returns**: 0-100%

**When to use**:
- At start of session (must be > 20%)
- During long operations
- Before walking commands

**Safety**: Below 10% robot will auto-sit.

---

#### `get_imu_data()`
Get IMU orientation and motion data.

**Returns**:
- Quaternion (x, y, z, w)
- Gyroscope (rad/s)
- Accelerometer (m/s²)

**When to use**: Monitor stability during walking.

---

## Common Workflows

### Safe Walking Sequence
```python
# 1. Check prerequisites
battery = get_battery_level()
if battery < 20:
    return "Battery too low for walking"

# 2. Stand up
stand_up()

# 3. Verify standing
imu = get_imu_data()
if abs(imu.pitch) > 0.1 or abs(imu.roll) > 0.1:
    return "Robot not stable, aborting"

# 4. Walk slowly
walk_forward(speed=0.1, duration=5.0)

# 5. Stop
stop_movement()
```

### Arm Manipulation Sequence
```python
# 1. Get current state
joints = get_joint_states()

# 2. Move shoulder (slowly)
move_joint("right_shoulder_pitch", -1.57, velocity=0.5)

# 3. Move elbow
move_joint("right_elbow", -1.0, velocity=0.5)

# 4. Verify final pose
joints = get_joint_states()
```

## Error Codes

- `JOINT_LIMIT_ERROR`: Target exceeds joint limits
- `VELOCITY_LIMIT_ERROR`: Velocity too high
- `STABILITY_ERROR`: Robot would become unstable
- `LOW_BATTERY`: Battery below safe threshold
- `DDS_TIMEOUT`: Communication error

## Best Practices

1. **Always check battery** before movement
2. **Start slow** - Use low velocities for testing
3. **Verify state** after each command
4. **Plan paths** - Avoid rapid direction changes
5. **Emergency stop** - `stop_movement()` is always available
