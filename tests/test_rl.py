from simple_playgrounds import SPGEngine


def test_all_test_playgrounds_interactive(base_forward_agent, pg_rl_cls):

    agent = base_forward_agent

    playground = pg_rl_cls()

    playground.add_agent(agent, allow_overlapping=False)

    print('Starting testing of ', pg_rl_cls.__name__)

    engine = SPGEngine(playground, time_limit=1000)
    engine.run()
    assert 0 < agent.position[0] < playground._size[0]
    assert 0 < agent.position[1] < playground._size[1]

    engine.terminate()
    playground.remove_agent(agent)
