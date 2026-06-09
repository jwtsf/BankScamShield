from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from .tools.custom_tool import SGSSIRChecker, URLTechnicalAnalyser

@CrewBase
class BankScamShieldCrew():
    """BankScamShield crew for detecting financial fraud"""
    
    # These point to your YAML files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def forensic_linguist(self) -> Agent:
        return Agent(
            config=self.agents_config['forensic_linguist'],
            verbose=True
        )

    @agent
    def technical_security_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_security_auditor'],
            tools=[SGSSIRChecker(), URLTechnicalAnalyser()],
            verbose=True
        )

    @task
    def linguistic_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['linguistic_analysis_task']
        )

    @task
    def technical_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['technical_audit_task']
        )

    @task
    def final_recommendation_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_security_recommendation_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BankScamShield crew"""
        return Crew(
            agents=self.agents, # Automatically collects all @agent methods
            tasks=self.tasks,   # Automatically collects all @task methods
            process=Process.sequential,
            verbose=True,
        )
