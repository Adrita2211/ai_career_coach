import os
import logging
from typing import List, Optional, Dict, Any, TypedDict, Annotated
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import asyncio
from dotenv import load_dotenv
from datetime import datetime
import uuid
import re
import json
from operator import add
import time
from fastapi.responses import JSONResponse

# LangGraph and LangChain imports with error handling
try:
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    LANGGRAPH_AVAILABLE = True
except ImportError as e:
    LANGGRAPH_AVAILABLE = False
    logging.warning(f"LangGraph dependencies not available: {e}")

# Load environment variables
load_dotenv()

# Get API keys from environment with better validation
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyAlM84sFx5DK0dpArY9bChvGOACqAu5h58")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","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")

# Validate API keys
if OPENAI_API_KEY:
    if not OPENAI_API_KEY.startswith('sk-'):
        logging.warning("OpenAI API key format appears invalid")
        OPENAI_API_KEY = None

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Pydantic models for API request bodies
class UserProfile(BaseModel):
    skills: List[str]
    career_goals: List[str]
    experience_level: str
    industry: str

class CareerAnalysisRequest(BaseModel):
    user_profile: UserProfile
    market_focus: str = "global"

class LearningPathRequest(BaseModel):
    skills: List[str]
    career_goals: List[str]
    experience_level: str
    industry: str
    topic: str
    preferred_learning_style: str
    time_commitment: str

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    target_role: str
    experience_years: int
    existing_projects: List[str]
    target_companies: List[str]
    salary_expectations: str

class InterviewPrepRequest(BaseModel):
    target_role: str
    company_name: str
    interview_type: str
    experience_level: str
    key_skills: List[str]

class SkillAssessmentRequest(BaseModel):
    skills_to_assess: List[str]
    experience_level: str
    target_role: str

class AgentState(TypedDict):
    """
    State for the multi-agent workflow.
    """
    input: str
    user_profile: Optional[Dict[str, Any]]
    result: Optional[str]
    agent_outcome: Optional[str]

# Define the FastAPI application
app = FastAPI(
    title="AI Career Coaching System",
    description="A multi-agent system for career advice, powered by LangGraph.",
    version="1.0.0",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handler
@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    logging.error(f"An unexpected error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred."}
    )

class CareerCoachingSystem:
    def __init__(self):
        if not LANGGRAPH_AVAILABLE:
            raise ImportError("LangGraph dependencies are not installed. Please install them to run this application.")
           
        self.llm_gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY, temperature=0.7)
        self.memory = MemorySaver()
        self.workflows = {}
       
        self._initialize_workflows()

    def _initialize_workflows(self):
        """Initializes and builds all agent workflows."""
        try:
            self.workflows['learning_path'] = self._create_learning_path_workflow()
            self.workflows['resume_analysis'] = self._create_resume_analysis_workflow()
            self.workflows['interview_prep'] = self._create_interview_prep_workflow()
            self.workflows['career_analysis'] = self._create_career_analysis_workflow()
            self.workflows['skill_assessment'] = self._create_skill_assessment_workflow()
            logging.info("All workflows initialized successfully.")
        except Exception as e:
            logging.error(f"Error initializing workflows: {e}")
            raise e

    def _create_learning_path_workflow(self):
        # A simple linear workflow for learning path
        workflow = StateGraph(AgentState)
        workflow.add_node("learning_path_agent", self._learning_path_node)
        workflow.add_edge("learning_path_agent", END)
        workflow.set_entry_point("learning_path_agent")
        return workflow.compile(checkpointer=self.memory)
   
    def _create_resume_analysis_workflow(self):
        # A simple linear workflow for resume analysis
        workflow = StateGraph(AgentState)
        workflow.add_node("resume_analyst_agent", self._resume_analyst_node)
        workflow.add_edge("resume_analyst_agent", END)
        workflow.set_entry_point("resume_analyst_agent")
        return workflow.compile(checkpointer=self.memory)
   
    def _create_interview_prep_workflow(self):
        # A simple linear workflow for interview prep
        workflow = StateGraph(AgentState)
        workflow.add_node("interview_prep_agent", self._interview_prep_node)
        workflow.add_edge("interview_prep_agent", END)
        workflow.set_entry_point("interview_prep_agent")
        return workflow.compile(checkpointer=self.memory)

    def _create_career_analysis_workflow(self):
        # A simple linear workflow for career analysis
        workflow = StateGraph(AgentState)
        workflow.add_node("career_analyst_agent", self._career_analyst_node)
        workflow.add_edge("career_analyst_agent", END)
        workflow.set_entry_point("career_analyst_agent")
        return workflow.compile(checkpointer=self.memory)

    def _create_skill_assessment_workflow(self):
        # This is where the error was occurring
        workflow = StateGraph(AgentState)
        workflow.add_node("skill_assessor", self._skill_assessor_node)
        workflow.add_edge("skill_assessor", END)
        workflow.set_entry_point("skill_assessor")
        return workflow.compile(checkpointer=self.memory)

    # --- Agent Nodes ---
    def _learning_path_node(self, state: AgentState) -> Dict[str, str]:
        # This is a placeholder for the actual LLM logic
        logging.info("Generating learning path...")
        prompt = f"""
        You are an expert career coach and learning path designer.
        Based on the user's profile and goals, create a detailed and actionable learning path.
       
        User Profile:
        - Current Skills: {state['user_profile']['skills']}
        - Career Goals: {state['user_profile']['career_goals']}
        - Experience Level: {state['user_profile']['experience_level']}
        - Industry: {state['user_profile']['industry']}
        - Specific Topic: {state['user_profile']['topic']}
        - Learning Style: {state['user_profile']['preferred_learning_style']}
        - Time Commitment: {state['user_profile']['time_commitment']}

        Provide the output in a well-structured markdown format. Include sections for:
        1. Roadmap (e.g., Phase 1, Phase 2)
        2. Key Skills to Master
        3. Recommended Resources (courses, books, projects)
        4. Milestones and Projects
        5. A final summary with encouragement.
        """
        response = self.llm_gemini.invoke(prompt)
        return {"result": response.content, "agent_outcome": "learning_path_complete"}

    def _resume_analyst_node(self, state: AgentState) -> Dict[str, str]:
        # Placeholder for the resume analysis LLM logic
        logging.info("Analyzing resume...")
        prompt = f"""
        You are a senior recruiter and resume expert.
        Analyze the provided resume text and provide actionable feedback for the target role.

        Resume Text:
        {state['user_profile']['resume_text']}
       
        Target Role: {state['user_profile']['target_role']}
        Years of Experience: {state['user_profile']['experience_years']}
        Existing Projects: {state['user_profile']['existing_projects']}
        Target Companies: {state['user_profile']['target_companies']}
        Salary Expectations: {state['user_profile']['salary_expectations']}

        Provide the output in a well-structured markdown format with sections for:
        1. Executive Summary: Overall feedback on the resume's strengths and weaknesses.
        2. Keyword Optimization: Suggestions for keywords to add/remove based on the target role.
        3. Project Recommendations: Ideas for projects to strengthen the resume.
        4. Formatting and Clarity: Tips for improving readability and professional appearance.
        """
        response = self.llm_gemini.invoke(prompt)
        return {"result": response.content, "agent_outcome": "resume_analysis_complete"}

    def _interview_prep_node(self, state: AgentState) -> Dict[str, str]:
        # Placeholder for the interview prep LLM logic
        logging.info("Preparing interview guide...")
        prompt = f"""
        You are a seasoned interview coach. Create a comprehensive interview preparation guide for the user.
       
        Target Role: {state['user_profile']['target_role']}
        Company Name: {state['user_profile']['company_name']}
        Interview Type: {state['user_profile']['interview_type']}
        Experience Level: {state['user_profile']['experience_level']}
        Key Skills: {state['user_profile']['key_skills']}
       
        Provide a detailed plan in markdown with sections for:
        1. Company Research: Key information to know about the company.
        2. Question Bank: Common and role-specific questions (technical, behavioral).
        3. Strategic Tips: Advice on how to approach the interview, answer questions, and follow up.
        4. Mock Interview Scenario: A brief scenario or challenge to practice.
        """
        response = self.llm_gemini.invoke(prompt)
        return {"result": response.content, "agent_outcome": "interview_prep_complete"}

    def _career_analyst_node(self, state: AgentState) -> Dict[str, str]:
    # Placeholder for the career analysis LLM logic
       logging.info("Performing career analysis...")
   
    # Handle nested user_profile structure for career analysis
       user_profile_data = state['user_profile']
       if 'user_profile' in user_profile_data:
        # If it's nested (from CareerAnalysisRequest)
        profile = user_profile_data['user_profile']
        market_focus = user_profile_data.get('market_focus', 'global')
       else:
        # If it's direct (from other request types)
        profile = user_profile_data
        market_focus = user_profile_data.get('market_focus', 'global')
   
       prompt = f"""
       You are a career market analyst. Provide a detailed analysis of the job market based on the user's profile.
   
       User Profile:
      - Skills: {profile.get('skills', [])}
      - Goals: {profile.get('career_goals', [])}
      - Experience: {profile.get('experience_level', 'intermediate')}
      - Industry: {profile.get('industry', 'Technology')}
    
        Market Focus: {market_focus}
    
        Provide the output in markdown with sections for:
        1. Market Trends: Key trends and a forecast for the next 1-3 years.
        2. Salary Insights: Typical salary ranges for the specified roles and market.
        3. Growth Opportunities: Potential career paths and specialization areas.
        4. Competitor Analysis: What other professionals are doing in this space.
        """
   
       response = self.llm_gemini.invoke(prompt)
       return {"result": response.content, "agent_outcome": "career_analysis_complete"}

    def _skill_assessor_node(self, state: AgentState) -> Dict[str, str]:
        # Placeholder for the skill assessment LLM logic
        logging.info("Performing skill assessment...")
        prompt = f"""
        You are an expert skill assessment agent. Analyze the user's provided skills in the context of their target role and provide a comprehensive skill gap analysis.

        Skills to Assess: {state['user_profile']['skills_to_assess']}
        Experience Level: {state['user_profile']['experience_level']}
        Target Role Context: {state['user_profile']['target_role']}

        Provide a well-structured markdown output with sections for:
        1. Skill Proficiency Breakdown: A rating and brief comment on each of the provided skills in relation to the target role.
        2. Identified Gaps: List essential skills for the target role that are missing or weak.
        3. Action Plan: A concrete, step-by-step plan to bridge the identified skill gaps.
        4. Suggested Projects: One or two project ideas to help the user practice and demonstrate mastery of the required skills.
        """
        response = self.llm_gemini.invoke(prompt)
        return {"result": response.content, "agent_outcome": "skill_assessment_complete"}


# API Endpoints
@app.post("/learning_path")
async def get_learning_path(request: LearningPathRequest, background_tasks: BackgroundTasks):
    try:
        user_profile = request.model_dump()
        initial_state = {"input": "generate learning path", "user_profile": user_profile}
        thread_id = str(uuid.uuid4())
       
        # Fixed configuration - include required configurable keys
        config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": ""
            }
        }
       
        result = await coaching_system.workflows['learning_path'].ainvoke(initial_state, config=config)
        return {"result": result['result']}
    except Exception as e:
        logging.error(f"Error in learning_path endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate learning path.")

@app.post("/resume_analysis")
async def get_resume_analysis(request: ResumeAnalysisRequest, background_tasks: BackgroundTasks):
    try:
        user_profile = request.model_dump()
        initial_state = {"input": "analyze resume", "user_profile": user_profile}
        thread_id = str(uuid.uuid4())
       
        # Fixed configuration
        config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": ""
            }
        }
       
        result = await coaching_system.workflows['resume_analysis'].ainvoke(initial_state, config=config)
        return {"result": result['result']}
    except Exception as e:
        logging.error(f"Error in resume_analysis endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate resume analysis.")

@app.post("/interview_prep")
async def get_interview_prep(request: InterviewPrepRequest, background_tasks: BackgroundTasks):
    try:
        user_profile = request.model_dump()
        initial_state = {"input": "prepare for interview", "user_profile": user_profile}
        thread_id = str(uuid.uuid4())
       
        # Fixed configuration
        config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": ""
            }
        }
       
        result = await coaching_system.workflows['interview_prep'].ainvoke(initial_state, config=config)
        return {"result": result['result']}
    except Exception as e:
        logging.error(f"Error in interview_prep endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate interview prep.")

@app.post("/career_analysis")
async def get_career_analysis(request: CareerAnalysisRequest, background_tasks: BackgroundTasks):
    try:
        user_profile = request.model_dump()
        initial_state = {"input": "conduct career analysis", "user_profile": user_profile}
        thread_id = str(uuid.uuid4())
       
        # Fixed configuration
        config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": ""
            }
        }
       
        result = await coaching_system.workflows['career_analysis'].ainvoke(initial_state, config=config)
        return {"result": result['result']}
    except Exception as e:
        logging.error(f"Error in career_analysis endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate career analysis.")

@app.post("/skill_assessment")
async def get_skill_assessment(request: SkillAssessmentRequest, background_tasks: BackgroundTasks):
    try:
        user_profile = request.model_dump()
        initial_state = {"input": "perform skill assessment", "user_profile": user_profile}
        thread_id = str(uuid.uuid4())
       
        # Fixed configuration
        config = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_ns": ""
            }
        }
       
        result = await coaching_system.workflows['skill_assessment'].ainvoke(initial_state, config=config)
        return {"result": result['result']}
    except Exception as e:
        logging.error(f"Error in skill_assessment endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform skill assessment.")

@app.get("/")
def read_root():
    """
    Default route to check if the API is running.
    """
    return {"message": "AI Career Coaching API is running. Use /docs for documentation."}

# Initialize the coaching system
coaching_system = CareerCoachingSystem()

# Run the application (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )
