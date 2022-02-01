
import math
import pymunk
import random

import pytest
from simple_playgrounds.agent.part.part import AnchoredPart
from simple_playgrounds.entity.embodied.contour import Contour
from tests.mock_agents import MockAgent, MockAnchoredPart
from simple_playgrounds.playground.playground import EmptyPlayground


@pytest.fixture(scope='module', params=[(20, 20), (-20, -20), (0, 0)])
def pos(request):
    return request.param


@pytest.fixture(scope='module', params=[-1,  0, 1])
def angle(request):
    return request.param


@pytest.fixture(scope='module', params=[-4, -1, 0, 1, 4])
def offset_angle(request):
    return request.param


@pytest.fixture(scope='module', params=[(10, 10), (-10, -10), (0, 0)])
def pos_on_part(request):
    return request.param


@pytest.fixture(scope='module', params=[(10, 10), (-10, -10), (0, 0)])
def pos_on_anchor(request):
    return request.param


def test_move(pos, angle, pos_on_part, pos_on_anchor, offset_angle):

    angle = angle % (2*math.pi)
    playground = EmptyPlayground()
    agent = MockAgent(playground, coordinates=(pos, angle))

    contour = Contour(shape='rectangle', size=(50, 30))
    part = MockAnchoredPart(agent._base,
                            pivot_position_on_part=pos_on_part,
                            pivot_position_on_anchor=pos_on_anchor,
                            relative_angle=offset_angle,
                            rotation_range=math.pi,
                            contour=contour,
                            )

    # Check that joints are correct. Agent shouldn't move
    # for _ in range(100):
    #     playground.step()

    assert math.isclose(agent.position.x, pos[0], abs_tol=1e-10)
    assert math.isclose(agent.position.y, pos[1], abs_tol=1e-10)

    part_pos = (pymunk.Vec2d(*pos)
                + pymunk.Vec2d(*pos_on_anchor).rotated(angle)
                - pymunk.Vec2d(*pos_on_part).rotated(angle+offset_angle))

    assert math.isclose(part.position.x, part_pos.x)
    assert math.isclose(part.position.y, part_pos.y)

    random_pos = (random.uniform(-10, 10), random.uniform(-10, 10))
    random_angle = random.randint(-10, 10)
    agent.move_to((random_pos, random_angle))

    # for _ in range(100):
    #     playground.step()

    part_pos_after_move = (pymunk.Vec2d(*random_pos)
                + pymunk.Vec2d(*pos_on_anchor).rotated(random_angle)
                - pymunk.Vec2d(*pos_on_part).rotated(random_angle+offset_angle))

    assert math.isclose(part.position.x, part_pos_after_move.x)
    assert math.isclose(part.position.y, part_pos_after_move.y)

def test_reset_position(pos, angle, pos_on_part, pos_on_anchor, offset_angle):
    pass
