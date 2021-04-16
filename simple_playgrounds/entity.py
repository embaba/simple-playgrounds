""" Contains the base class for entities.

Entity class should be used to create body parts of
an agent, or scene entities.
Entity is the generic building block of physical and interactive
objects in simple-playgrounds.

Examples can be found in :
    - simple_playgrounds/agents/parts
    - simple_playgrounds/playgrounds/scene_elements
"""
from typing import Union, Tuple, Dict

import math
from abc import ABC, abstractmethod

import pymunk
import pygame

from simple_playgrounds.utils.position_utils import CoordinateSampler, Trajectory
from simple_playgrounds.utils.texture import Texture, TextureGenerator
from simple_playgrounds.utils.definitions import CollisionTypes, PhysicalShapes

# pylint: disable=line-too-long
# pylint: disable=too-many-instance-attributes

FRICTION_ENTITY = 0.8
ELASTICITY_ENTITY = 0.5


class Entity(ABC):
    """
    Entity creates a physical object, and deals with interactive properties and visual appearance
    """

    index_entity = 0
    # TODO: remove entity type

    def __init__(self,
                 visible_shape: bool,
                 invisible_shape: bool,
                 texture: Union[Texture, Dict],
                 physical_shape: str,
                 size: Union[None, Tuple[int, int]] = None,
                 radius: Union[None, int] = None,
                 invisible_range: int = 5,
                 graspable: bool = False,
                 traversable: bool = False,
                 movable: bool = False,
                 temporary: bool = False,
                 name: Union[str, None] = None,
                 mass: Union[float, None] = None,
                 **pymunk_attributes,
                 ):

        # Internal counter to assign identity number and name to each entity
        self.name = name
        if not name:
            self.name = self.__class__.__name__ + '_' + str(Entity.index_entity)
        Entity.index_entity += 1

        # Physical properties of the entity
        if graspable:
            movable = True

        self.mass = mass
        self.physical_shape = PhysicalShapes[physical_shape.upper()]

        # Dimensions of the entity
        self.invisible_range = invisible_range

        assert (radius or size)

        if radius and not size:
            assert isinstance(radius, int)
            self._radius_visible = radius
            self._size_visible = (radius, radius)
            self._radius_invisible = radius + self.invisible_range
            self._size_invisible = (self._radius_invisible, self._radius_invisible)

        else:
            assert isinstance(size, tuple)
            assert len(size)==2 and isinstance(size[0], int) and isinstance(size[1], int)

            width, length = size
            self._size_visible = size
            self._radius_visible = int(((width/2)**2 + (length/2)**2)**(1/2))
            self._size_invisible = width+self.invisible_range, length+self.invisible_range
            self._radius_invisible = self._radius_visible + self.invisible_range

        self.pm_body = self._create_pm_body(movable)
        self.pm_elements = [self.pm_body]

        self.pm_visible_shape = None
        self.pm_invisible_shape = None
        self.pm_grasp_shape = None

        if visible_shape:
            self.pm_visible_shape = self._create_pm_shape()
            self._set_visible_shape_collision()
            self.pm_elements.append(self.pm_visible_shape)

            if traversable:
                self.pm_visible_shape.filter = pymunk.ShapeFilter(categories=1)
            else:
                self.pm_visible_shape.filter = pymunk.ShapeFilter(categories=2, mask=pymunk.ShapeFilter.ALL_MASKS() ^ 1)

        # Interactive properties of the entity
        
        if invisible_shape:
            self.pm_invisible_shape = self._create_pm_shape(invisible=True)
            self._set_invisible_shape_collision()
            self.pm_elements.append(self.pm_invisible_shape)

        if graspable:
            self.pm_grasp_shape = self._create_pm_shape(invisible=True)
            self.pm_grasp_shape.collision_type = CollisionTypes.GRASPABLE
            self.pm_elements.append(self.pm_grasp_shape)

        # To be set when entity is added to playground.
        self._initial_coordinates = None
        self.trajectory = None

        # Texture random generator can be set
        if isinstance(texture, Dict):
            texture['size'] = self._size_visible
            texture = TextureGenerator.create(**texture)
        self.texture_surface = texture.generate()

        # Used to set an element which is not supposed to overlap
        self._allow_overlapping = False
        self._overlapping_strategy_set = False
        self._max_attempts = 100

        self._set_pm_attr(pymunk_attributes)

        background = True
        if invisible_shape or movable:
            background = False

        self.background = background
        self.drawn = False

        self.temporary = temporary

    @abstractmethod
    def _set_visible_shape_collision(self):
        pass

    @abstractmethod
    def _set_invisible_shape_collision(self):
        pass

    def assign_shape_filter(self, category_index):
        """
        Used to define collisions between entities.
        Used for sensors.

        Returns:

        """
        if self.pm_visible_shape is not None:
            mask_filter = self.pm_visible_shape.filter.mask ^ 2**category_index
            self.pm_visible_shape.filter = pymunk.ShapeFilter(categories=self.pm_visible_shape.filter.categories,
                                                              mask=mask_filter)

    def _set_pm_attr(self, attr):

        for prop, value in attr.items():
            for pm_elem in self.pm_elements:
                setattr(pm_elem, prop, value)

    # BODY AND SHAPE

    def _create_pm_body(self, movable):

        if not movable:
            return pymunk.Body(body_type=pymunk.Body.STATIC)

        if self.physical_shape == PhysicalShapes.CIRCLE:
            moment = pymunk.moment_for_circle(self.mass, 0, self._radius_visible)

        elif self.physical_shape in [PhysicalShapes.TRIANGLE,
                                     PhysicalShapes.SQUARE,
                                     PhysicalShapes.PENTAGON,
                                     PhysicalShapes.HEXAGON]:

            vertices = self._compute_vertices()
            moment = pymunk.moment_for_poly(self.mass, vertices)

        elif self.physical_shape == PhysicalShapes.RECTANGLE:
            moment = pymunk.moment_for_box(self.mass, self._size_visible)

        else:
            raise ValueError

        return pymunk.Body(self.mass, moment)

    def _compute_vertices(self, offset_angle=0., invisible=False):

        vertices = []

        if self.physical_shape == PhysicalShapes.RECTANGLE:

            width, length = self._size_visible
            if invisible:
                width, length = self._size_invisible

            points = [(width / 2., length / 2.), (width / 2., -length / 2.),
                      (-width / 2., -length / 2.), (-width / 2., length / 2.)]

            for coord in points:
                pos_x = coord[0] * math.cos(offset_angle) - coord[1] * math.sin(offset_angle)
                pos_y = coord[0] * math.sin(offset_angle) + coord[1] * math.cos(offset_angle)

                vertices.append((pos_x, pos_y))

            return vertices

        else:

            radius = self._radius_visible
            if invisible:
                radius = self._radius_invisible

            number_sides = PhysicalShapes[self.physical_shape].value

            for n_sides in range(number_sides):
                vertices.append((radius * math.cos(n_sides * 2 * math.pi / number_sides + offset_angle),
                                 radius * math.sin(n_sides * 2 * math.pi / number_sides + offset_angle)))

        return vertices

    def _create_pm_shape(self, invisible=False):

        if self.physical_shape == PhysicalShapes.CIRCLE:

            if invisible:
                pm_shape = pymunk.Circle(self.pm_body, self._radius_invisible)
            else:
                pm_shape = pymunk.Circle(self.pm_body, self._radius_visible)

        elif self.physical_shape in [PhysicalShapes.TRIANGLE,
                                     PhysicalShapes.SQUARE,
                                     PhysicalShapes.PENTAGON,
                                     PhysicalShapes.HEXAGON]:

            vertices = self._compute_vertices(invisible=invisible)
            pm_shape = pymunk.Poly(self.pm_body, vertices)

        elif self.physical_shape == PhysicalShapes.RECTANGLE:

            if invisible:
                pm_shape = pymunk.Poly.create_box(self.pm_body, self._size_invisible)
            else:
                pm_shape = pymunk.Poly.create_box(self.pm_body, self._size_visible)
        else:
            raise ValueError

        if invisible:
            pm_shape.sensor = True
        else:
            pm_shape.friction = FRICTION_ENTITY
            pm_shape.elasticity = ELASTICITY_ENTITY

        return pm_shape

    # VISUAL APPEARANCE

    def _create_mask(self, invisible=False):

        # pylint: disable-all

        alpha = 255
        mask_size = self._size_visible

        if invisible:
            alpha = 75
            mask_size = self._size_invisible

        if self.physical_shape == PhysicalShapes.RECTANGLE:
            assert isinstance(mask_size, tuple)
            center = mask_size[0]/2., mask_size[1]/2.

        else:
            assert isinstance(mask_size, int)
            center = mask_size, mask_size
            mask_size = (2 * mask_size + 1, 2 * mask_size + 1)

        mask = pygame.Surface(mask_size, pygame.SRCALPHA)
        mask.fill((0, 0, 0, 0))

        if self.physical_shape == PhysicalShapes.CIRCLE:
            radius = center[0]
            pygame.draw.circle(mask, (255, 255, 255, alpha), center, radius)

        else:
            vert = self._compute_vertices(offset_angle=self.angle, invisible=invisible)
            vertices = [[x[0] + center[0], x[1] + center[1]] for x in vert]
            pygame.draw.polygon(mask, (255, 255, 255, alpha), vertices)

        if invisible:
            texture_surface = pygame.transform.scale(self.texture_surface,
                                                     mask_size)
        else:
            texture_surface = self.texture_surface.copy()

        # Pygame / numpy conversion
        mask_angle = math.pi/2 - self.angle
        texture_surface = pygame.transform.rotate(texture_surface, mask_angle * 180 / math.pi)
        mask_rect = texture_surface.get_rect()
        mask_rect.center = center
        mask.blit(texture_surface, mask_rect, None, pygame.BLEND_MULT)

        return mask

    # OVERLAPPING STRATEGY
    @property
    def overlapping_strategy(self):
        if self._overlapping_strategy_set:
            return self._allow_overlapping, self._max_attempts

        else:
            return None

    @overlapping_strategy.setter
    def overlapping_strategy(self, strategy):
        self._allow_overlapping, self._max_attempts = strategy
        self._overlapping_strategy_set = True

    # POSITION AND VELOCITY

    @property
    def initial_coordinates(self):
        """
        Initial coordinates of the Entity.
        Can be tuple of (x,y), angle, or PositionAreaSampler object
        """

        if isinstance(self._initial_coordinates, (tuple, list)):
            return self._initial_coordinates

        elif isinstance(self._initial_coordinates, CoordinateSampler):
            return self._initial_coordinates.sample()

        raise ValueError

    @initial_coordinates.setter
    def initial_coordinates(self, init_coordinates):

        if isinstance(init_coordinates, Trajectory):
            self.trajectory = init_coordinates
            self._initial_coordinates = next(self.trajectory)

        elif isinstance(init_coordinates, (tuple, list, CoordinateSampler)):
            self._initial_coordinates = init_coordinates

        else:
            raise ValueError('Initial position not valid')

    @property
    def coordinates(self):
        return self.position, self.angle

    @coordinates.setter
    def coordinates(self, coord):
        self.position, self.angle = coord

    @property
    def position(self):
        return self.pm_body.position

    @position.setter
    def position(self, pos):
        self.pm_body.position = pos

    @property
    def angle(self):
        return self.pm_body.angle

    @angle.setter
    def angle(self, phi):
        self.pm_body.angle = phi

    @property
    def velocity(self):
        return self.pm_body.velocity

    @velocity.setter
    def velocity(self, vel):
        self.pm_body.velocity = vel

    @property
    def angular_velocity(self):
        return self.pm_body.angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, v_phi):
        self.pm_body.angular_velocity = v_phi

    # INTERFACE

    def pre_step(self):
        """
        Performs calculation before the physical environment steps.
        """

        if self.trajectory:
            self.position, self.angle = next(self.trajectory)

        if not self.background:
            self.drawn = False

    def reset(self):
        """
        Reset the trajectory and initial position
        """

        if self.trajectory:
            self.trajectory.reset()

        self.velocity = (0, 0)
        self.angular_velocity = 0

        self.position, self.angle = self.initial_coordinates

        self.drawn = False

    def draw(self, surface, draw_invisible=False, force_recompute_mask=False):
        """
        Draw the entity on the surface.

        Args:
            surface: Pygame Surface.
            draw_invisible: If True, draws invisible shape
            force_recompute_mask: If True, the visual appearance is re-calculated.
        """

        if not self.drawn or force_recompute_mask:

            if draw_invisible and (self.pm_invisible_shape or self.pm_grasp_shape):
                invisible_mask = self._create_mask(invisible=True)
                mask_rect = invisible_mask.get_rect()
                mask_rect.center = self.position
                surface.blit(invisible_mask, mask_rect, None)

            if self.pm_visible_shape:
                visible_mask = self._create_mask()
                mask_rect = visible_mask.get_rect()
                mask_rect.center = self.position
                surface.blit(visible_mask, mask_rect, None)

        self.drawn = True
