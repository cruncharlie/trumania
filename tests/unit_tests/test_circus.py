from __future__ import division

from datetime import datetime

from datagenerator.action import *
from datagenerator.actor import *

from datagenerator.circus import *
from datagenerator.clock import *
from datagenerator.random_generators import *
from datagenerator.relationship import *
import pytest

def test_create_action_get_action_should_work_as_expected():

    customers = Actor(100)

    the_clock = Clock(datetime(year=2016, month=6, day=8), 60,
                      "%d%m%Y %H:%M:%S", 1)

    flying = Circus(the_clock)

    mov_prof = pd.Series(
        [1., 1., 1., 1., 1., 1., 1., 1., 5., 10., 5., 1., 1., 1., 1., 1., 1.,
         5., 10., 5., 1., 1., 1., 1.],
        index=[timedelta(hours=h, minutes=59, seconds=59) for h in range(24)])
    mobility_time_gen = DayProfiler(the_clock, mov_prof, seed=1)

    mobility_action = flying.create_action(
        name="mobility",

        initiating_actor=customers,
        actorid_field="A_ID",

        timer_gen=mobility_time_gen,
    )

    # add and get action by name should work as expected
    result = flying.get_action("mobility")

    assert result.name == "mobility"
    assert result.actorid_field_name == mobility_action.actorid_field_name


def test_get_non_existing_action_should_return_None():

    the_clock = Clock(datetime(year=2016, month=6, day=8), 60,
                      "%d%m%Y %H:%M:%S", 1)

    flying = Circus(the_clock)

    assert flying.get_action("non_existing_name") is None


def test_adding_a_second_action_with_same_name_should_be_refused():

    the_clock = Clock(datetime(year=2016, month=6, day=8), 60,
                      "%d%m%Y %H:%M:%S", 1)

    flying = Circus(the_clock)

    ac1 = flying.create_action(name="the_action",
                               initiating_actor=Actor(100),
                               actorid_field="actor_id")

    with pytest.raises(ValueError):
        ac2 = flying.create_action(name="the_action",
                               initiating_actor=Actor(100),
                               actorid_field="actor_id")



