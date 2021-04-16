"""
Teleport can be used to teleport an agent.
"""
from simple_playgrounds.scene_elements.element import SceneElement
from simple_playgrounds.utils.definitions import CollisionTypes, ElementTypes

# pylint: disable=line-too-long



class TeleportElement(SceneElement, ABC):

    def __init__(self, texture=(0, 100, 100), **kwargs):
        super().__init__(texture=texture, **kwargs)
        self.pm_invisible_shape.collision_type = CollisionTypes.TELEPORT

        self.reward = 0
        self.reward_provided = False

        self.target = None

    def add_target(self, target):
        self.target = target
