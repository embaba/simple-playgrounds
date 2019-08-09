import pymunk, pygame
import math
from .forward import ForwardAgent
from ..common import texture


# move physical body to utils
from .agent import PhysicalBody

from ..utils.config import *

from pygame.locals import *


default_head_texture =  {
        'type': 'uniform',
        'a': (120, 5, 150),
        'b': (200, 34, 200)
    }

class ForwardHeadAgent(ForwardAgent):

    def __init__(self, agent_params):

        super(ForwardHeadAgent, self).__init__(agent_params)

        self.head_range = agent_params.get('head_range', 0)
        self.head_speed = agent_params.get('head_speed', 10)
        self.head_radius = agent_params.get("head_radius", 10)

        head = PhysicalBody()

        base = self.anatomy["base"]

        inertia = pymunk.moment_for_circle(1, 0, self.radius, (0, 0))

        body = pymunk.Body(1, inertia)
        body.position = agent_params['position'][:2]
        body.angle = agent_params['position'][2]

        head.body = body

        shape = pymunk.Circle(body, self.radius-5, (0, 0))
        shape.sensor = True

        head.shape = shape


        head.joint = [ pymunk.PinJoint(head.body, base.body, (0, 0), (0, 0)),
                       pymunk.SimpleMotor(head.body, base.body, 0)
                       ]


        self.anatomy["head"] = head


        text = agent_params.get('head_texture', default_head_texture)
        self.head_texture = texture.Texture.create(text)
        self.head_texture_surface = None

        list_sensors = agent_params.get("sensors", None)

        for sens in list_sensors:
            self.add_sensor(sens)


    def get_head_angle(self):

        a_head = self.anatomy["head"].body.angle
        a_base = self.anatomy["base"].body.angle

        rel_head = (a_base - a_head) % (2*math.pi)
        rel_head = rel_head - 2*math.pi if rel_head > math.pi else rel_head

        return rel_head

    def apply_action(self, actions):
        super().apply_action(actions)

        head_velocity = actions.get('head_velocity', 0)

        self.anatomy['head'].body.angle +=  self.head_speed * head_velocity

        if self.get_head_angle() < -self.head_range:
            self.anatomy['head'].body.angle = self.anatomy['base'].body.angle + self.head_range
        elif self.get_head_angle() > self.head_range:
            self.anatomy['head'].body.angle = self.anatomy['base'].body.angle - self.head_range




        #self.anatomy["head"].joint

    def getStandardKeyMapping(self):

        mapping = super().getStandardKeyMapping()

        mapping[K_z] = ['press_hold', 'head_velocity', 1]
        mapping[K_x] = ['press_hold', 'head_velocity', -1]

        return mapping

    def getAvailableActions(self):
        actions = super().getAvailableActions()

        actions['head_velocity'] = [-1, 1, 'continuous']

        return actions

    def draw(self, surface):
        super().draw(surface)

        # Body
        radius = int(self.head_radius)

        # Create a texture surface with the right dimensions
        if self.head_texture_surface is None:
            self.head_texture_surface = self.head_texture.generate(radius * 2, radius * 2)

            # Create the mask
            self.mask_head = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            self.mask_head.fill((0, 0, 0, 0))
            pygame.draw.circle(self.mask_head, (255, 255, 255, 255), (radius, radius), radius)

            # Apply texture on mask
            self.mask_head.blit(self.head_texture_surface, (0, 0), None, pygame.BLEND_MULT)
            pygame.draw.line(self.mask_head,  pygame.color.THECOLORS["blue"] , (radius,radius), (radius, 2*radius), 2)


        mask = pygame.transform.rotate(self.mask_head, self.anatomy['head'].body.angle * 180 / math.pi)

        mask_rect = mask.get_rect()
        mask_rect.center = self.anatomy['base'].body.position[1], self.anatomy['base'].body.position[0]

        # Blit the masked texture on the screen
        surface.blit(mask, mask_rect, None)

