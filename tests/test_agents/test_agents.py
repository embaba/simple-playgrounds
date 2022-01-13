import pytest

from simple_playgrounds.playground.playground import EmptyPlayground
from tests.mock_agents import MockAgent
from tests.mock_entities import MockBarrier, MockPhysical
from simple_playgrounds.entity.embodied.contour import Contour

def test_agent_in_playground():

    agent = MockAgent()
    playground = EmptyPlayground()
    
    playground.add(agent)
    assert agent in playground.agents

    playground.remove(agent)
    assert agent not in playground.agents
    assert not playground.space.shapes
    assert playground._shapes_to_entities == {}


def test_agent_initial_position():

    agent = MockAgent()
    playground = EmptyPlayground()
    
    playground.add(agent)

    assert agent.position == (0, 0)
    assert agent.angle == 0


def test_agent_forward_movable():
 
    agent = MockAgent()
    playground = EmptyPlayground()
    
    playground.add(agent)

    contour = Contour(shape='circle', radius=10)
    obstacle = MockPhysical(**contour.dict_attributes, movable=True, mass=5, initial_coordinates=((0,0), 0)
    playground.add(obstacle, ((50, 0), 0))

    actions = {}
    for command in agent.commands:
        actions[command] = command.max


def test_agent_forward_obstacle():
    pass


def test_agent_control():
    pass


def test_seed():
    pass


# def run_engine(base_agent, pg_class, **pg_params):
#     playground = pg_class(**pg_params)
#     playground.add_agent(base_agent, allow_overlapping=False)

#     engine = Engine(playground, time_limit=1000)
#     engine.run()

#     assert 0 < base_agent.position[0] < playground.size[0]
#     assert 0 < base_agent.position[1] < playground.size[1]

#     playground.remove_agent(base_agent)


# def test_agents_in_empty_room(is_interactive, going_backward, moving_laterally,
#                               all_agent_cls, random_controller):

#     agent = all_agent_cls(
#         controller=random_controller(),
#         interactive=is_interactive,
#         backward=going_backward,
#         lateral=moving_laterally,
#     )

#     run_engine(agent, SingleRoom, size=(300, 300))


# @pytest.mark.parametrize(
#     "pg,limits",
#     [(SingleRoom((300, 300)), (300, 300)),
#      (GridRooms((400, 400), (2, 2), doorstep_size=60), (200, 200))],
# )
# def test_agent_initial_position(base_forward_agent_random, pg, limits):

#     # When position is not set
#     agent = base_forward_agent_random
#     pg.add_agent(agent)
#     assert 0 < agent.position[0] < limits[0]
#     assert 0 < agent.position[1] < limits[1]
#     pg.remove_agent(agent)

#     # When position is fixed
#     pg.add_agent(agent, ((50, 50), 0))
#     assert agent.position == (50, 50)
#     pg.remove_agent(agent)

#     # When position is from area of room
#     position_sampler = pg.grid_rooms[0][0].get_area_sampler()
#     pg.add_agent(agent, position_sampler)
#     assert 0 < agent.position[0] < limits[0]
#     assert 0 < agent.position[1] < limits[1]


# def test_agent_overlapping(base_forward_agent_random, empty_playground):

#     elem = Physical(config_key='square')
#     empty_playground.add_element(elem, ((50, 50), 0))
#     empty_playground.add_agent(base_forward_agent_random, ((50, 50), 0))

#     assert empty_playground._overlaps(base_forward_agent_random)
#     assert empty_playground._overlaps(base_forward_agent_random, elem)

#     empty_playground.remove_agent(base_forward_agent_random)

#     with pytest.raises(ValueError):
#         empty_playground.add_agent(base_forward_agent_random, ((50, 50), 0),
#                                    allow_overlapping=False)

#     with pytest.raises(ValueError):
#         empty_playground.add_agent(base_forward_agent_random)
#         empty_playground.add_agent(base_forward_agent_random)
