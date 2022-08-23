from __future__ import annotations
import math
from typing import Optional, TYPE_CHECKING

from simple_playgrounds.agent.part.controller import (
    CenteredContinuousController,
    BoolController,
)
from tests.test_view.conftest import shape

if TYPE_CHECKING:
    from simple_playgrounds.agent.part.part import Part

import pymunk
import numpy as np

from simple_playgrounds.common.position_utils import Coordinate

from simple_playgrounds.common.definitions import (
    ANGULAR_VELOCITY,
    CollisionTypes,
    LINEAR_FORCE,
)
from simple_playgrounds.agent.agent import Agent
from simple_playgrounds.agent.part.part import (
    AnchoredPart,
    PhysicalPart,
    Platform,
    InteractivePart,
)


class MockBase(Platform):
    def __init__(self, agent: Agent, **kwargs):

        super().__init__(
            agent,
            mass=10,
            filename=":resources:images/topdown_tanks/tankBody_blue_outline.png",
            sprite_front_is_up=True,
            shape_approximation="decomposition",
            **kwargs,
        )

        self.forward_controller, self.angular_vel_controller = self._controllers

    def _set_controllers(self, **kwargs):

        control_forward = CenteredContinuousController(part=self)
        control_rotate = CenteredContinuousController(part=self)
        return control_forward, control_rotate

    def apply_commands(self, **kwargs):

        command_value = self.forward_controller.command_value

        self._pm_body.apply_force_at_local_point(
            pymunk.Vec2d(command_value, 0) * LINEAR_FORCE, (0, 0)
        )

        command_value = self.angular_vel_controller.command_value
        self._pm_body.angular_velocity = command_value * ANGULAR_VELOCITY


class MockAnchoredPart(AnchoredPart):
    def __init__(self, anchor: PhysicalPart, **kwargs):
        super().__init__(
            anchor,
            mass=10,
            filename=":resources:images/topdown_tanks/tankBlue_barrel3_outline.png",
            sprite_front_is_up=True,
            **kwargs,
        )
        self.joint_controller = self._controllers[0]

    # def post_step(self, **_):
    #     return super().post_step(**_)

    def _set_controllers(self, **kwargs):
        return [CenteredContinuousController(part=self)]

    def apply_commands(self, **kwargs):

        value = self.joint_controller.command_value

        theta_part = self.angle
        theta_anchor = self._anchor.angle

        angle_centered = theta_part - (theta_anchor + self._angle_offset)
        angle_centered = angle_centered % (2 * np.pi)
        angle_centered = (
            angle_centered - 2 * np.pi if angle_centered > np.pi else angle_centered
        )

        # Do not set the motor if the limb is close to limit
        if (angle_centered < -self._rotation_range / 2 + np.pi / 20) and value < 0:
            self._motor.rate = 0

        elif (angle_centered > self._rotation_range / 2 - np.pi / 20) and value > 0:
            self._motor.rate = 0

        else:
            self._motor.rate = -value * ANGULAR_VELOCITY

    @property
    def default_position_on_part(self):
        return (-self.radius, 0)


class MockHaloPart(InteractivePart):
    def __init__(self, anchor: Part, **kwargs):
        super().__init__(anchor, **kwargs)
        self._activated = False

    @property
    def _collision_type(self):
        return CollisionTypes.PASSIVE_INTERACTOR

    def _set_controllers(self, **_):
        return []

    def apply_commands(self, **_):
        pass

    def pre_step(self):
        self._activated = False

    def activate(self):
        self._activated = True

    @property
    def activated(self):
        return self._activated


class MockTriggerPart(InteractivePart):
    def __init__(self, anchor: Part, **kwargs):
        super().__init__(anchor, **kwargs)

        self.trigger = self._set_controllers()[0]
        self._activated = False

    @property
    def _collision_type(self):
        return CollisionTypes.ACTIVE_INTERACTOR

    def _set_controllers(self, **_):
        return [BoolController(part=self)]

    def apply_commands(self, **_):
        value = self.trigger.command_value
        if value:
            self.activate()

    def pre_step(self):
        self._activated = False

    def activate(self):
        self._activated = True

    @property
    def activated(self):
        return self._activated


class MockAgent(Agent):
    def _add_base(self, **kwargs) -> Part:
        base = MockBase(self, **kwargs)
        return base


class MockAgentWithArm(MockAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.left_arm = MockAnchoredPart(
            self.base,
            position_on_anchor=(15, 15),
            relative_angle=math.pi / 3,
            rotation_range=math.pi / 4,
        )

        self.right_arm = MockAnchoredPart(
            self.base,
            position_on_anchor=(15, -15),
            relative_angle=-math.pi / 3,
            rotation_range=math.pi / 4,
        )
