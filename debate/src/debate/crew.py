from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Debate():

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def debater(self) -> Agent:
        return Agent(config=self.agents_config['debater'],verbose=True)

    @agent
    def judge(self) -> Agent:
        return Agent(config=self.agents_config['judge'],verbose=True)

   
    @task
    def propose_task(self) -> Task:
        return Task(config=self.tasks_config['propose_task'])

    @task
    def oppose_task(self) -> Task:
        return Task(config=self.tasks_config['oppose_task'])

    @task
    def judge_task(self) -> Task:
        return Task(config=self.tasks_config['judge_task'])

    @crew
    def crew(self) -> Crew:
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
