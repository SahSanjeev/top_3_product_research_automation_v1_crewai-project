import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool
)






@CrewBase
class Top3ProductResearchAutomationCrew:
    """Top3ProductResearchAutomation crew"""

    
    @agent
    def market_research_analyst(self) -> Agent:

        
        return Agent(
            config=self.agents_config["market_research_analyst"],
            
            
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4.1",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def product_evaluation_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["product_evaluation_specialist"],
            
            
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4.1",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def research_report_writer(self) -> Agent:

        
        return Agent(
            config=self.agents_config["research_report_writer"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4.1",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def identify_leading_companies_and_products(self) -> Task:
        return Task(
            config=self.tasks_config["identify_leading_companies_and_products"],
            markdown=False,
            
            
        )
    
    @task
    def evaluate_and_rank_products(self) -> Task:
        return Task(
            config=self.tasks_config["evaluate_and_rank_products"],
            markdown=False,
            
            
        )
    
    @task
    def create_top_products_report(self) -> Task:
        return Task(
            config=self.tasks_config["create_top_products_report"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the Top3ProductResearchAutomation crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
