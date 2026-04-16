"""
Unitree SDK2 MCP Server

Multi-robot MCP Server for Unitree robots using DDS protocol.
Supports: G1, Go2, Go2w, H1, H2, B2, B2w, A2, R1

Part of the ROSClaw Embodied Intelligence Operating System.

SDK Information:
    Name: unitree_sdk2
    Version: 2.1.0+
    Protocol: DDS (Data Distribution Service)
    Source: https://github.com/unitreerobotics/unitree_sdk2
    Documentation: https://support.unitree.com/home/zh/developer
    License: BSD-3-Clause

Supported Robots:
    - G1: Humanoid (23/43 DOF)
    - Go2/Go2w: Quadruped (12 DOF)
    - H1/H2: Humanoid (20 DOF)
    - B2/B2w: Quadruped (12 DOF)
    - A2: Quadruped (12 DOF)
    - R1: Wheeled robot

Generated: 2026-04-15
"""

import asyncio
import threading
import time
import json
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from collections import deque
from mcp.server.fastmcp import FastMCP

from robot_configs import (
    RobotConfig,
    get_robot_config,
    list_supported_robots,
    ROBOT_CONFIGS,
)

# SDK Metadata
SDK_METADATA = {
    "name": "unitree_sdk2",
    "version": "2.1.0+",
    "protocol": "DDS",
    "source_url": "https://github.com/unitreerobotics/unitree_sdk2",
    "doc_url": "https://support.unitree.com/home/zh/developer",
    "license": "BSD-3-Clause",
    "supported_robots": list(ROBOT_CONFIGS.keys()),
    "generated_at": "2026-04-15",
}

# Initialize MCP Server
mcp = FastMCP("unitree-sdk2")


@dataclass
class RobotState:
    """Generic robot state data"""
    timestamp: float
    robot_id: str
    battery_level: int  # 0-100%
    robot_mode: int  # 0: idle, 1: standing, 2: walking, etc.

    # Joint states (radians)
    joint_positions: Dict[str, float] = field(default_factory=dict)
    joint_velocities: Dict[str, float] = field(default_factory=dict)
    joint_torques: Dict[str, float] = field(default_factory=dict)

    # IMU data
    imu_quaternion: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)
    imu_gyroscope: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    imu_accelerometer: Tuple[float, float, float] = (0.0, 0.0, 0.0)

    # Body state (humanoid specific)
    body_height: float = 0.0
    body_pitch: float = 0.0
    body_roll: float = 0.0
    body_yaw: float = 0.0


@dataclass
class StateBuffer:
    """Thread-safe state buffer for DDS data"""
    max_size: int = 100
    _buffer: deque = field(default_factory=lambda: deque(maxlen=100))
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def append(self, state: RobotState):
        with self._lock:
            self._buffer.append(state)

    def get_latest(self) -> Optional[RobotState]:
        with self._lock:
            return self._buffer[-1] if self._buffer else None

    def get_history(self, n: int = 10) -> List[RobotState]:
        with self._lock:
            return list(self._buffer)[-n:]


class UnitreeDDSBridge:
    """
    Unitree DDS Communication Bridge

    Protocol: DDS (Data Distribution Service)
    Domain: Default DDS domain
    Topics:
    - /lowstate: Robot state (joints, IMU, battery)
    - /lowcmd: Robot commands (joint targets, mode)
    - /sportmodestate: Sport mode state
    """

    def __init__(self, robot_id: str, domain_id: int = 0):
        self.robot_id = robot_id
        self.config = get_robot_config(robot_id)
        if self.config is None:
            raise ValueError(f"Unknown robot ID: {robot_id}")

        self.domain_id = domain_id
        self.connected = False
        self._stop_event = threading.Event()
        self._dds_thread: Optional[threading.Thread] = None

        # State buffer
        self.state_buffer = StateBuffer(max_size=100)

        # Current command
        self._current_mode = 0  # 0: idle
        self._target_positions: Dict[str, float] = {}
        self._cmd_lock = threading.Lock()

    def connect(self) -> bool:
        """
        Connect to robot DDS domain

        Returns:
            True if connected successfully
        """
        try:
            # TODO: Initialize DDS participant
            # This would use unitree_sdk2 or cyclonedds Python bindings

            self.connected = True
            self._stop_event.clear()

            # Start DDS listener thread
            self._dds_thread = threading.Thread(
                target=self._dds_listener,
                name=f"{self.robot_id.upper()}DDSListener",
                daemon=True
            )
            self._dds_thread.start()

            return True

        except Exception as e:
            print(f"DDS connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect from DDS domain"""
        self._stop_event.set()
        if self._dds_thread and self._dds_thread.is_alive():
            self._dds_thread.join(timeout=2.0)
        self.connected = False

    def _dds_listener(self):
        """
        DDS listener thread - receives state updates

        This runs in a separate thread to avoid blocking MCP
        """
        print(f"{self.config.name} DDS listener started")

        while not self._stop_event.is_set():
            try:
                # TODO: Implement actual DDS subscription
                # Subscribe to /lowstate topic

                # Simulate state update for now
                state = RobotState(
                    timestamp=time.time(),
                    robot_id=self.robot_id,
                    battery_level=85,
                    robot_mode=self._current_mode,
                    joint_positions={name: 0.0 for name in self.config.joint_names},
                )
                self.state_buffer.append(state)

                time.sleep(0.01)  # 100Hz update rate

            except Exception as e:
                print(f"DDS listener error: {e}")
                time.sleep(0.1)

        print(f"{self.config.name} DDS listener stopped")

    def publish_command(self, mode: int, positions: Optional[Dict[str, float]] = None):
        """
        Publish command to robot

        Args:
            mode: Robot mode (0: idle, 1: standing, 2: walking, etc.)
            positions: Target joint positions (optional)
        """
        with self._cmd_lock:
            self._current_mode = mode
            if positions:
                self._target_positions = positions.copy()

        # TODO: Publish to /lowcmd topic via DDS

    def _validate_joint_positions(self, positions: Dict[str, float]) -> Tuple[bool, str]:
        """
        Validate joint positions against safety limits

        Returns:
            (valid, error_message)
        """
        for joint, value in positions.items():
            if joint in self.config.joint_limits:
                min_val, max_val = self.config.joint_limits[joint]
                if not (min_val <= value <= max_val):
                    return False, f"Joint {joint} value {value} out of range [{min_val}, {max_val}]"
        return True, "OK"

    def get_latest_state(self) -> Optional[RobotState]:
        """Get latest robot state"""
        return self.state_buffer.get_latest()


# Global bridge instances (per robot)
_bridges: Dict[str, UnitreeDDSBridge] = {}


def get_bridge(robot_id: str) -> Optional[UnitreeDDSBridge]:
    """Get bridge for a specific robot"""
    return _bridges.get(robot_id)


def require_bridge(robot_id: str) -> UnitreeDDSBridge:
    """Get bridge or raise error if not connected"""
    bridge = get_bridge(robot_id)
    if bridge is None:
        raise RuntimeError(f"Not connected to {robot_id}. Call connect_robot first.")
    if not bridge.connected:
        raise RuntimeError(f"Connection to {robot_id} lost. Reconnect required.")
    return bridge


# ============ MCP Tools ============

@mcp.tool()
async def get_sdk_info() -> str:
    """
    Get SDK metadata and version information.

    Returns:
        JSON string with SDK metadata including version,
        source URL, documentation URL, and supported robots.
    """
    return json.dumps(SDK_METADATA, indent=2)


@mcp.tool()
async def list_robots() -> str:
    """
    List all supported Unitree robots.

    Returns:
        List of supported robot IDs and their details.
    """
    robots = []
    for robot_id, config in ROBOT_CONFIGS.items():
        robots.append({
            "id": robot_id,
            "name": config.name,
            "type": config.robot_type,
            "dof": config.dof,
        })
    return json.dumps({"supported_robots": robots}, indent=2)


@mcp.tool()
async def get_robot_info(robot_id: str) -> str:
    """
    Get detailed information about a specific robot.

    Args:
        robot_id: Robot identifier (e.g., 'g1', 'go2', 'h1')

    Returns:
        JSON with robot configuration including joint limits and capabilities.
    """
    config = get_robot_config(robot_id)
    if config is None:
        return json.dumps({"error": f"Unknown robot: {robot_id}"})

    return json.dumps({
        "id": config.robot_id,
        "name": config.name,
        "type": config.robot_type,
        "dof": config.dof,
        "joint_names": config.joint_names,
        "joint_limits": config.joint_limits,
        "velocity_limits": config.velocity_limits,
        "capabilities": {
            "walking": config.support_walking,
            "arm_control": config.support_arm_control,
        },
    }, indent=2)


@mcp.tool()
async def connect_robot(robot_id: str, domain_id: int = 0) -> str:
    """
    Connect to a Unitree robot via DDS.

    Args:
        robot_id: Robot identifier (e.g., 'g1', 'go2', 'h1', 'b2')
        domain_id: DDS domain ID (default: 0)

    Returns:
        Connection status message
    """
    global _bridges

    # Validate robot ID
    config = get_robot_config(robot_id)
    if config is None:
        supported = ", ".join(list_supported_robots())
        return f"Error: Unknown robot '{robot_id}'. Supported: {supported}"

    # Disconnect if already connected
    if robot_id in _bridges:
        _bridges[robot_id].disconnect()
        del _bridges[robot_id]

    # Create new bridge
    try:
        bridge = UnitreeDDSBridge(robot_id=robot_id, domain_id=domain_id)

        if bridge.connect():
            _bridges[robot_id] = bridge
            return f"✓ Connected to {config.name} on DDS domain {domain_id}"
        else:
            return f"✗ Failed to connect to {config.name}"
    except Exception as e:
        return f"✗ Connection error: {str(e)}"


@mcp.tool()
async def disconnect_robot(robot_id: str) -> str:
    """
    Disconnect from a robot.

    Args:
        robot_id: Robot identifier

    Returns:
        Disconnection status message
    """
    global _bridges

    if robot_id in _bridges:
        _bridges[robot_id].disconnect()
        del _bridges[robot_id]
        return f"✓ Disconnected from {robot_id}"

    return f"Not connected to {robot_id}"


@mcp.tool()
async def stand_up(robot_id: str) -> str:
    """
    Command robot to stand up.

    Args:
        robot_id: Robot identifier

    Returns:
        Command status message
    """
    try:
        bridge = require_bridge(robot_id)
        config = bridge.config

        if not config.support_walking:
            return f"⚠ {config.name} does not support standing/walking commands"

        # Set standing mode
        bridge.publish_command(mode=1)

        return f"✓ Stand up command sent to {config.name}"
    except RuntimeError as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def sit_down(robot_id: str) -> str:
    """
    Command robot to sit down / stop.

    Args:
        robot_id: Robot identifier

    Returns:
        Command status message
    """
    try:
        bridge = require_bridge(robot_id)
        config = bridge.config

        bridge.publish_command(mode=0)

        return f"✓ Sit down command sent to {config.name}"
    except RuntimeError as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def walk_with_velocity(
    robot_id: str,
    linear_x: float = 0.0,
    linear_y: float = 0.0,
    angular_z: float = 0.0,
    duration: float = 2.0
) -> str:
    """
    Command robot to walk with specified velocity.

    Args:
        robot_id: Robot identifier
        linear_x: Forward/backward velocity (m/s)
        linear_y: Left/right velocity (m/s)
        angular_z: Rotation velocity (rad/s)
        duration: Walking duration (seconds)

    Returns:
        Command status message
    """
    try:
        bridge = require_bridge(robot_id)
        config = bridge.config

        if not config.support_walking:
            return f"⚠ {config.name} does not support walking"

        # Safety limits
        if abs(linear_x) > 1.0:
            return "Error: linear_x exceeds safety limit of ±1.0 m/s"
        if abs(linear_y) > 0.5:
            return "Error: linear_y exceeds safety limit of ±0.5 m/s"
        if abs(angular_z) > 1.0:
            return "Error: angular_z exceeds safety limit of ±1.0 rad/s"

        # Set walking mode
        bridge.publish_command(mode=2)

        # Walk for specified duration
        await asyncio.sleep(duration)

        # Stop walking
        bridge.publish_command(mode=1)

        return f"✓ {config.name} walked with velocity ({linear_x}, {linear_y}, {angular_z}) for {duration}s"
    except RuntimeError as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def move_joint(
    robot_id: str,
    joint_name: str,
    target_position: float,
    duration: float = 2.0
) -> str:
    """
    Move a specific joint to target position.

    Args:
        robot_id: Robot identifier
        joint_name: Name of the joint
        target_position: Target angle in radians
        duration: Movement duration (seconds)

    Returns:
        Command status message
    """
    try:
        bridge = require_bridge(robot_id)
        config = bridge.config

        # Validate joint name
        if joint_name not in config.joint_names:
            return f"Error: Unknown joint '{joint_name}'. Valid joints: {config.joint_names}"

        # Validate position
        valid, msg = bridge._validate_joint_positions({joint_name: target_position})
        if not valid:
            return f"Safety check failed: {msg}"

        # Send command
        bridge.publish_command(mode=1, positions={joint_name: target_position})

        await asyncio.sleep(duration)

        return f"✓ Moved {joint_name} to {target_position:.3f} rad on {config.name}"
    except RuntimeError as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def move_joints(
    robot_id: str,
    positions: Dict[str, float],
    duration: float = 3.0
) -> str:
    """
    Move multiple joints simultaneously.

    Args:
        robot_id: Robot identifier
        positions: Dictionary of {joint_name: target_position}
        duration: Movement duration (seconds)

    Returns:
        Command status message
    """
    try:
        bridge = require_bridge(robot_id)
        config = bridge.config

        # Validate all positions
        valid, msg = bridge._validate_joint_positions(positions)
        if not valid:
            return f"Safety check failed: {msg}"

        # Send command
        bridge.publish_command(mode=1, positions=positions)

        await asyncio.sleep(duration)

        return f"✓ Moved {len(positions)} joints on {config.name}"
    except RuntimeError as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def stop_movement(robot_id: str) -> str:
    """
    Stop all movement and hold current position.

    Args:
        robot_id: Robot identifier

    Returns:
        Command status message
    """
    try:
        bridge = require_bridge(robot_id)
        bridge.publish_command(mode=1)
        return f"✓ Stopped and holding position"
    except RuntimeError as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def emergency_stop(robot_id: str) -> str:
    """
    Emergency stop - immediately halt all motion.

    Args:
        robot_id: Robot identifier

    Returns:
        Command status message
    """
    try:
        bridge = require_bridge(robot_id)
        bridge.publish_command(mode=0)
        return f"⚠ Emergency stop activated for {robot_id}!"
    except RuntimeError as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def wave_hand(robot_id: str, hand: str = "right", times: int = 3) -> str:
    """
    Perform a waving motion with the specified hand.
    Only works for humanoid robots with arms.

    Args:
        robot_id: Robot identifier
        hand: Which hand to wave ('left' or 'right')
        times: Number of waves

    Returns:
        Command status message
    """
    try:
        bridge = require_bridge(robot_id)
        config = bridge.config

        if not config.support_arm_control:
            return f"⚠ {config.name} does not support arm control"

        if hand not in ["left", "right"]:
            return "Error: hand must be 'left' or 'right'"

        # Wave motion
        shoulder_yaw = f"{hand}_shoulder_yaw"
        elbow = f"{hand}_elbow"

        for i in range(times):
            # Raise arm
            bridge.publish_command(mode=1, positions={
                shoulder_yaw: -1.5,
                elbow: -1.0
            })
            await asyncio.sleep(0.5)

            # Wave
            bridge.publish_command(mode=1, positions={
                elbow: 0.0
            })
            await asyncio.sleep(0.5)

        # Lower arm
        bridge.publish_command(mode=1, positions={
            shoulder_yaw: 0.0,
            elbow: 0.0
        })

        return f"✓ Waved {hand} hand {times} times on {config.name}"
    except RuntimeError as e:
        return f"Error: {str(e)}"


# ============ MCP Resources ============

@mcp.resource("unitree://{robot_id}/status")
async def get_robot_status(robot_id: str) -> str:
    """
    Get robot current status.

    Returns battery level, robot mode, and joint states.
    """
    bridge = get_bridge(robot_id)
    if bridge is None:
        return f"Not connected to {robot_id}"

    state = bridge.get_latest_state()
    if state is None:
        return "No state data available"

    mode_names = {
        0: "Idle/Sitting",
        1: "Standing",
        2: "Walking",
        3: "Running",
    }
    mode_str = mode_names.get(state.robot_mode, f"Unknown({state.robot_mode})")

    return f"""
{bridge.config.name} Status:
  Battery: {state.battery_level}%
  Mode: {mode_str}
  Timestamp: {state.timestamp:.3f}

  Joint Positions (sample):
    {state.joint_positions.get(bridge.config.joint_names[0], 0):.3f} rad ({bridge.config.joint_names[0]})
"""


@mcp.resource("unitree://{robot_id}/joints")
async def get_joint_info(robot_id: str) -> str:
    """Get information about all joints for a robot."""
    config = get_robot_config(robot_id)
    if config is None:
        return f"Unknown robot: {robot_id}"

    info = [f"{config.name} Joint Information:", "=" * 40]

    for joint, (min_val, max_val) in config.joint_limits.items():
        info.append(f"  {joint}: [{min_val:.2f}, {max_val:.2f}] rad")

    return "\n".join(info)


@mcp.resource("unitree://connections")
async def get_connection_status() -> str:
    """Get DDS connection status for all robots."""
    if not _bridges:
        return "No active connections"

    status = ["Active Connections:", "=" * 40]
    for robot_id, bridge in _bridges.items():
        conn_status = "Connected" if bridge.connected else "Disconnected"
        status.append(f"  {robot_id}: {conn_status} (domain {bridge.domain_id})")

    return "\n".join(status)


if __name__ == "__main__":
    mcp.run(transport="stdio")
