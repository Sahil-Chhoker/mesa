"""
The agent class for Mesa framework.

Core Objects: Agent
"""
# Mypy; for the `|` operator purpose
# Remove this __future__ import once the oldest supported Python is 3.10
from __future__ import annotations

import weakref
from random import Random

# mypy
from typing import TYPE_CHECKING, Any, Callable, Iterator, Iterable

if TYPE_CHECKING:
    # We ensure that these are not imported during runtime to prevent cyclic
    # dependency.
    from mesa.model import Model
    from mesa.space import Position


class Agent:
    """
    Base class for a model agent in Mesa.

    Attributes:
        unique_id (int): A unique identifier for this agent.
        model (Model): A reference to the model instance.
        self.pos: Position | None = None
    """

    def __init__(self, unique_id: int, model: Model) -> None:
        """
        Create a new agent.

        Args:
            unique_id (int): A unique identifier for this agent.
            model (Model): The model instance in which the agent exists.
        """
        self.unique_id = unique_id
        self.model = model
        self.pos: Position | None = None

        # Directly register the agent with the model
        if type(self) not in self.model._agents:
            self.model._agents[type(self)] = set()
        self.model._agents[type(self)].add(self)

    def remove(self) -> None:
        """Remove and delete the agent from the model."""
        if type(self) in self.model._agents:
            self.model._agents[type(self)].discard(self)

    def step(self) -> None:
        """A single step of the agent."""

    def advance(self) -> None:
        pass

    @property
    def random(self) -> Random:
        return self.model.random


class AgentSet:
    def __init__(self, agents: Iterable[Agent], model: Model):
        self._agents = weakref.WeakKeyDictionary()

        for agent in agents:
            self._agents[agent] = None

        self.model = model

    def __len__(self) -> int:
        return len(self._agents)

    def __iter__(self) -> Iterator[Agent]:
        return iter(self._agents.keys())

    def __contains__(self, agent: Agent) -> bool:
        """Check if an agent is in the AgentSet."""
        return agent in self._agents

    def select(self, filter_func: Callable[[Agent], bool] | None = None, inplace: bool = False) -> AgentSet:
        if filter_func is None:
            if inplace:
                return self
            else:
                return AgentSet(list(self._agents.keys()), self.model)
        else:
            agents = [agent for agent in self._agents.keys() if filter_func(agent)]

            if inplace:
                self._reorder(agents)
                return self
            else:
                return AgentSet(
                    agents,
                    self.model
                )

    def shuffle(self, inplace: bool = False) -> AgentSet:
        shuffled_agents = list(self._agents.keys())
        self.model.random.shuffle(shuffled_agents)

        if inplace:
            self._reorder(shuffled_agents)
            return self
        else:
            return AgentSet(shuffled_agents, self.model)

    def sort(self, key: Callable[[Agent], Any], reverse: bool = False, inplace: bool = False) -> AgentSet:
        sorted_agents = sorted(list(self._agents.keys()), key=key, reverse=reverse)

        if inplace:
            self._reorder(sorted_agents)
            return self
        else:
            return AgentSet(sorted_agents, self.model)

    def _reorder(self, agents: Iterable[Agent]):
        _agents = weakref.WeakKeyDictionary()
        for agent in agents:
            _agents[agent] = None
        self._agents = _agents

    def do_each(self, method_name: str, *args, **kwargs) -> list[Any]:
        return [getattr(agent, method_name)(*args, **kwargs) for agent in self._agents]



    # Additional methods like union, intersection, difference, etc., can be added as needed.
