"""
Unitree Robot Configurations

Configuration definitions for all Unitree robots supported by unitree_sdk2:
- G1: Humanoid (23/43 DOF)
- Go2: Quadruped (12 DOF)
- Go2w: Quadruped with wheels (12 DOF)
- H1: Humanoid (20 DOF)
- H2: Humanoid (variable DOF)
- B2: Quadruped (12 DOF)
- B2w: Quadruped with wheels (12 DOF)
- A2: Quadruped (12 DOF)
- R1: Wheeled robot
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


@dataclass
class RobotConfig:
    """Configuration for a Unitree robot"""
    name: str
    robot_id: str
    robot_type: str  # humanoid, quadruped, wheeled
    dof: int
    joint_names: List[str] = field(default_factory=list)
    joint_limits: Dict[str, Tuple[float, float]] = field(default_factory=dict)
    velocity_limits: Dict[str, float] = field(default_factory=dict)
    default_standing_positions: Dict[str, float] = field(default_factory=dict)
    support_walking: bool = False
    support_arm_control: bool = False
    # DDS topics
    lowstate_topic: str = "/lowstate"
    lowcmd_topic: str = "/lowcmd"
    sportstate_topic: str = "/sportmodestate"


# ============ G1 Humanoid ============
G1_CONFIG = RobotConfig(
    name="Unitree G1 Humanoid",
    robot_id="g1",
    robot_type="humanoid",
    dof=23,
    joint_names=[
        # Left leg (5)
        "left_hip_yaw", "left_hip_roll", "left_hip_pitch",
        "left_knee", "left_ankle",
        # Right leg (5)
        "right_hip_yaw", "right_hip_roll", "right_hip_pitch",
        "right_knee", "right_ankle",
        # Waist (3)
        "waist_yaw", "waist_roll", "waist_pitch",
        # Left arm (4)
        "left_shoulder_pitch", "left_shoulder_roll", "left_shoulder_yaw",
        "left_elbow",
        # Right arm (4)
        "right_shoulder_pitch", "right_shoulder_roll", "right_shoulder_yaw",
        "right_elbow",
    ],
    joint_limits={
        # Left leg
        "left_hip_yaw": (-2.35, 2.35),
        "left_hip_roll": (-0.78, 0.78),
        "left_hip_pitch": (-2.5, 2.5),
        "left_knee": (-0.5, 2.5),
        "left_ankle": (-1.0, 1.0),
        # Right leg
        "right_hip_yaw": (-2.35, 2.35),
        "right_hip_roll": (-0.78, 0.78),
        "right_hip_pitch": (-2.5, 2.5),
        "right_knee": (-0.5, 2.5),
        "right_ankle": (-1.0, 1.0),
        # Waist
        "waist_yaw": (-2.5, 2.5),
        "waist_roll": (-0.5, 0.5),
        "waist_pitch": (-1.0, 1.0),
        # Left arm
        "left_shoulder_pitch": (-3.14, 3.14),
        "left_shoulder_roll": (-0.5, 3.5),
        "left_shoulder_yaw": (-2.0, 2.0),
        "left_elbow": (-1.5, 2.0),
        # Right arm
        "right_shoulder_pitch": (-3.14, 3.14),
        "right_shoulder_roll": (-3.5, 0.5),
        "right_shoulder_yaw": (-2.0, 2.0),
        "right_elbow": (-1.5, 2.0),
    },
    velocity_limits={
        "leg": 10.0,
        "waist": 5.0,
        "arm": 10.0,
    },
    default_standing_positions={
        "left_hip_yaw": 0.0,
        "left_hip_roll": 0.0,
        "left_hip_pitch": -0.3,
        "left_knee": 0.6,
        "left_ankle": -0.3,
        "right_hip_yaw": 0.0,
        "right_hip_roll": 0.0,
        "right_hip_pitch": -0.3,
        "right_knee": 0.6,
        "right_ankle": -0.3,
        "waist_yaw": 0.0,
        "waist_roll": 0.0,
        "waist_pitch": 0.0,
        "left_shoulder_pitch": 0.0,
        "left_shoulder_roll": 0.0,
        "left_shoulder_yaw": 0.0,
        "left_elbow": 0.0,
        "right_shoulder_pitch": 0.0,
        "right_shoulder_roll": 0.0,
        "right_shoulder_yaw": 0.0,
        "right_elbow": 0.0,
    },
    support_walking=True,
    support_arm_control=True,
)


# ============ Go2 Quadruped ============
GO2_CONFIG = RobotConfig(
    name="Unitree Go2 Quadruped",
    robot_id="go2",
    robot_type="quadruped",
    dof=12,
    joint_names=[
        # Front left leg (3)
        "front_left_hip", "front_left_thigh", "front_left_calf",
        # Front right leg (3)
        "front_right_hip", "front_right_thigh", "front_right_calf",
        # Rear left leg (3)
        "rear_left_hip", "rear_left_thigh", "rear_left_calf",
        # Rear right leg (3)
        "rear_right_hip", "rear_right_thigh", "rear_right_calf",
    ],
    joint_limits={
        # All legs similar ranges
        "front_left_hip": (-0.87, 0.87),
        "front_left_thigh": (-0.52, 2.97),
        "front_left_calf": (-2.76, -0.52),
        "front_right_hip": (-0.87, 0.87),
        "front_right_thigh": (-0.52, 2.97),
        "front_right_calf": (-2.76, -0.52),
        "rear_left_hip": (-0.87, 0.87),
        "rear_left_thigh": (-0.52, 2.97),
        "rear_left_calf": (-2.76, -0.52),
        "rear_right_hip": (-0.87, 0.87),
        "rear_right_thigh": (-0.52, 2.97),
        "rear_right_calf": (-2.76, -0.52),
    },
    velocity_limits={
        "leg": 15.0,
    },
    default_standing_positions={
        "front_left_hip": 0.0,
        "front_left_thigh": 0.8,
        "front_left_calf": -1.5,
        "front_right_hip": 0.0,
        "front_right_thigh": 0.8,
        "front_right_calf": -1.5,
        "rear_left_hip": 0.0,
        "rear_left_thigh": 0.8,
        "rear_left_calf": -1.5,
        "rear_right_hip": 0.0,
        "rear_right_thigh": 0.8,
        "rear_right_calf": -1.5,
    },
    support_walking=True,
    support_arm_control=False,
)


# ============ Go2w (Quadruped with wheels) ============
GO2W_CONFIG = RobotConfig(
    name="Unitree Go2w Quadruped with Wheels",
    robot_id="go2w",
    robot_type="quadruped",
    dof=12,  # Same joint structure but with wheel actuators
    joint_names=GO2_CONFIG.joint_names,
    joint_limits=GO2_CONFIG.joint_limits,
    velocity_limits={
        "leg": 15.0,
        "wheel": 20.0,  # Wheels can rotate faster
    },
    default_standing_positions=GO2_CONFIG.default_standing_positions,
    support_walking=True,
    support_arm_control=False,
)


# ============ H1 Humanoid ============
H1_CONFIG = RobotConfig(
    name="Unitree H1 Humanoid",
    robot_id="h1",
    robot_type="humanoid",
    dof=20,
    joint_names=[
        # Left leg (5)
        "left_hip_yaw", "left_hip_roll", "left_hip_pitch",
        "left_knee", "left_ankle",
        # Right leg (5)
        "right_hip_yaw", "right_hip_roll", "right_hip_pitch",
        "right_knee", "right_ankle",
        # Waist (1)
        "waist_yaw",
        # Left arm (4)
        "left_shoulder_pitch", "left_shoulder_roll", "left_shoulder_yaw",
        "left_elbow",
        # Right arm (4)
        "right_shoulder_pitch", "right_shoulder_roll", "right_shoulder_yaw",
        "right_elbow",
    ],
    joint_limits={
        # Legs (similar to G1 but may vary)
        "left_hip_yaw": (-2.35, 2.35),
        "left_hip_roll": (-0.78, 0.78),
        "left_hip_pitch": (-2.5, 2.5),
        "left_knee": (-0.5, 2.5),
        "left_ankle": (-1.0, 1.0),
        "right_hip_yaw": (-2.35, 2.35),
        "right_hip_roll": (-0.78, 0.78),
        "right_hip_pitch": (-2.5, 2.5),
        "right_knee": (-0.5, 2.5),
        "right_ankle": (-1.0, 1.0),
        # Waist (simpler than G1)
        "waist_yaw": (-2.5, 2.5),
        # Arms
        "left_shoulder_pitch": (-3.14, 3.14),
        "left_shoulder_roll": (-0.5, 3.5),
        "left_shoulder_yaw": (-2.0, 2.0),
        "left_elbow": (-1.5, 2.0),
        "right_shoulder_pitch": (-3.14, 3.14),
        "right_shoulder_roll": (-3.5, 0.5),
        "right_shoulder_yaw": (-2.0, 2.0),
        "right_elbow": (-1.5, 2.0),
    },
    velocity_limits={
        "leg": 10.0,
        "waist": 5.0,
        "arm": 10.0,
    },
    default_standing_positions=G1_CONFIG.default_standing_positions,
    support_walking=True,
    support_arm_control=True,
)


# ============ H2 Humanoid ============
H2_CONFIG = RobotConfig(
    name="Unitree H2 Humanoid",
    robot_id="h2",
    robot_type="humanoid",
    dof=20,  # Similar to H1
    joint_names=H1_CONFIG.joint_names,
    joint_limits=H1_CONFIG.joint_limits,
    velocity_limits=H1_CONFIG.velocity_limits,
    default_standing_positions=H1_CONFIG.default_standing_positions,
    support_walking=True,
    support_arm_control=True,
)


# ============ B2 Quadruped ============
B2_CONFIG = RobotConfig(
    name="Unitree B2 Quadruped",
    robot_id="b2",
    robot_type="quadruped",
    dof=12,
    joint_names=GO2_CONFIG.joint_names,  # Same structure as Go2
    joint_limits={
        # B2 typically has larger ranges (bigger robot)
        "front_left_hip": (-1.0, 1.0),
        "front_left_thigh": (-0.6, 3.1),
        "front_left_calf": (-2.9, -0.4),
        "front_right_hip": (-1.0, 1.0),
        "front_right_thigh": (-0.6, 3.1),
        "front_right_calf": (-2.9, -0.4),
        "rear_left_hip": (-1.0, 1.0),
        "rear_left_thigh": (-0.6, 3.1),
        "rear_left_calf": (-2.9, -0.4),
        "rear_right_hip": (-1.0, 1.0),
        "rear_right_thigh": (-0.6, 3.1),
        "rear_right_calf": (-2.9, -0.4),
    },
    velocity_limits={
        "leg": 12.0,  # Slightly slower than Go2 due to size
    },
    default_standing_positions=GO2_CONFIG.default_standing_positions,
    support_walking=True,
    support_arm_control=False,
)


# ============ B2w (Quadruped with wheels) ============
B2W_CONFIG = RobotConfig(
    name="Unitree B2w Quadruped with Wheels",
    robot_id="b2w",
    robot_type="quadruped",
    dof=12,
    joint_names=B2_CONFIG.joint_names,
    joint_limits=B2_CONFIG.joint_limits,
    velocity_limits={
        "leg": 12.0,
        "wheel": 15.0,
    },
    default_standing_positions=B2_CONFIG.default_standing_positions,
    support_walking=True,
    support_arm_control=False,
)


# ============ A2 Quadruped ============
A2_CONFIG = RobotConfig(
    name="Unitree A2 Quadruped",
    robot_id="a2",
    robot_type="quadruped",
    dof=12,
    joint_names=GO2_CONFIG.joint_names,
    joint_limits={
        # A2 typically has more compact ranges
        "front_left_hip": (-0.8, 0.8),
        "front_left_thigh": (-0.5, 2.8),
        "front_left_calf": (-2.6, -0.5),
        "front_right_hip": (-0.8, 0.8),
        "front_right_thigh": (-0.5, 2.8),
        "front_right_calf": (-2.6, -0.5),
        "rear_left_hip": (-0.8, 0.8),
        "rear_left_thigh": (-0.5, 2.8),
        "rear_left_calf": (-2.6, -0.5),
        "rear_right_hip": (-0.8, 0.8),
        "rear_right_thigh": (-0.5, 2.8),
        "rear_right_calf": (-2.6, -0.5),
    },
    velocity_limits={
        "leg": 18.0,  # A2 is known for agility
    },
    default_standing_positions=GO2_CONFIG.default_standing_positions,
    support_walking=True,
    support_arm_control=False,
)


# ============ R1 Wheeled Robot ============
R1_CONFIG = RobotConfig(
    name="Unitree R1 Wheeled Robot",
    robot_id="r1",
    robot_type="wheeled",
    dof=4,  # 2 wheels + steering (simplified)
    joint_names=[
        "left_wheel",
        "right_wheel",
        "steering",
        "caster",
    ],
    joint_limits={
        "left_wheel": (-100.0, 100.0),  # Wheel rotation (unbounded in practice)
        "right_wheel": (-100.0, 100.0),
        "steering": (-0.785, 0.785),  # ±45 degrees
        "caster": (-3.14, 3.14),
    },
    velocity_limits={
        "wheel": 10.0,  # m/s
        "steering": 2.0,  # rad/s
    },
    default_standing_positions={
        "left_wheel": 0.0,
        "right_wheel": 0.0,
        "steering": 0.0,
        "caster": 0.0,
    },
    support_walking=False,
    support_arm_control=False,
)


# Registry of all supported robots
ROBOT_CONFIGS: Dict[str, RobotConfig] = {
    "g1": G1_CONFIG,
    "go2": GO2_CONFIG,
    "go2w": GO2W_CONFIG,
    "h1": H1_CONFIG,
    "h2": H2_CONFIG,
    "b2": B2_CONFIG,
    "b2w": B2W_CONFIG,
    "a2": A2_CONFIG,
    "r1": R1_CONFIG,
}


def get_robot_config(robot_id: str) -> Optional[RobotConfig]:
    """Get configuration for a specific robot"""
    return ROBOT_CONFIGS.get(robot_id.lower())


def list_supported_robots() -> List[str]:
    """List all supported robot IDs"""
    return list(ROBOT_CONFIGS.keys())


def list_robots_by_type(robot_type: str) -> List[RobotConfig]:
    """List robots filtered by type (humanoid, quadruped, wheeled)"""
    return [config for config in ROBOT_CONFIGS.values() if config.robot_type == robot_type]
