from simple_playgrounds.playground.playground import EmptyPlayground
from tests.mock_entities import MockPhysical, MockHaloTrigger, MockZoneTriggered
from simple_playgrounds.entity.embodied.contour import Contour


def test_mappings(radius, interaction_radius):

    playground = EmptyPlayground()

    contour = Contour(shape='circle', radius=radius)
    ent_1 = MockPhysical(playground, ((0, 0), 0), **contour.dict_attributes, 
                         movable=True, mass=5)
    halo = MockHaloTrigger(ent_1, interaction_range=interaction_radius)

    contour = Contour(shape='square', radius=radius)
    pos = ((0, 2*radius + interaction_radius - 1), 0)
    zone = MockZoneTriggered(playground, pos, **contour.dict_attributes)

    assert ent_1 in playground._entities
    assert halo not in playground._entities
    assert zone in playground._entities


def test_traversable_traversable(custom_contour, custom_contour_2):

    playground = EmptyPlayground()

    # Two traversable shouldn't collide with either traversables or non-traversables

    ent_1 = MockPhysical(playground, ((0, 0), 0), contour=custom_contour, traversable=True, movable=True, mass=5)
    ent_2 = MockPhysical(playground, ((0, 1), 0), contour=custom_contour_2, 
                         traversable=True, movable=True, mass=5)

    playground.step()

    assert ent_1.coordinates == ((0, 0), 0)
    assert ent_2.coordinates == ((0, 1), 0)


def test_traversable_basic(custom_contour, custom_contour_2):

    playground = EmptyPlayground()

    ent_1 = MockPhysical(playground, ((0, 0), 0), contour=custom_contour, traversable=True, movable=True, mass=5)
    ent_2 = MockPhysical(playground, ((0, 1), 0), contour=custom_contour_2, traversable=False, movable=True, mass=5)
    playground.step()

    assert ent_1.coordinates == ((0, 0), 0)
    assert ent_2.coordinates == ((0, 1), 0)


def test_basic_basic(custom_contour, custom_contour_2):

    playground = EmptyPlayground()

    ent_1 = MockPhysical(playground, ((0, 0), 0), contour=custom_contour, traversable=False, movable=True, mass=5)

    ent_2 = MockPhysical(playground, ((0, 1), 0), contour=custom_contour_2, traversable=False, movable=False)

    playground.step()

    assert ent_1.coordinates != ((0, 0), 0)
    assert ent_2.coordinates == ((0, 1), 0)


