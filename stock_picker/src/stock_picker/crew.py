from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field

# Configuration files are automatically loaded by CrewBase

class TrendingCompany(BaseModel):
    name: str =Field(description="The name of the company")
    ticker: str =Field(description="The ticker symbol of the company")
    reason: str =Field(description="The reason for the company to be trending")

class TrendingCompanies(BaseModel):
    companies: List[TrendingCompany] =Field(description="The list of trending companies")

class TrendingCompanyResearch(BaseModel):
    name: str =Field(description="The name of the company")
    market_cap: str =Field(description="The market cap of the company")
    market_position: str =Field(description="The market position of the company")
    future_potential: str =Field(description="The future potential of the company")
    investment_potential:str=Field(description="The investment potential of the company")

class TrendingCompanyResearchList(BaseModel):
    companies: List[TrendingCompanyResearch] =Field(description="The list of trending companies research")


@CrewBase
class StockPicker():
    """StockPicker crew"""
    
    agents_config = 'config/agents.yaml'

    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent: 
        return Agent(config=self.agents_config['trending_company_finder'],verbose=True,tools=[SerperDevTool()])
    
    @agent
    def financial_researcher(self) -> Agent: 
        return Agent(config=self.agents_config['financial_researcher'],verbose=True,tools=[SerperDevTool()])
    
    @agent
    def stock_picker(self) -> Agent: 
        return Agent(config=self.agents_config['stock_picker'],verbose=True)

    
    @task
    def find_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['find_trending_companies'],agent=self.trending_company_finder(),output_pydantic=TrendingCompanies)
    
    @task
    def research_trending_companies(self) -> Task:
        return Task(config=self.tasks_config['research_trending_companies'],agent=self.financial_researcher(),output_pydantic=TrendingCompanyResearchList)

    @task
    def pick_best_company(self) -> Task:
        return Task(config=self.tasks_config['pick_best_company'],agent=self.stock_picker())

    @crew
    def crew(self) -> Crew:

        
        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=manager,
            verbose=True
        )
