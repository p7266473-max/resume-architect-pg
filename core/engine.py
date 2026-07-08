import json
import logging
import time
from typing import Any, Optional
from pydantic import BaseModel

from google import genai
from google.genai import types
from smolagents import OpenAIModel, ToolCallingAgent, DuckDuckGoSearchTool

from core.prompts import (
    GEMINI_MODEL,
    MAX_RETRIES,
    RETRY_DELAY_SECONDS,
    RESUME_SCHEMA,
    PASS1_SYSTEM_PROMPT,
    PASS1_USER_TEMPLATE,
    PASS2_SYSTEM_PROMPT,
    PASS2_USER_TEMPLATE,
)

logger = logging.getLogger("resume_architect")

class ClientWrapper:
    """Wrapper to hold both the raw GenAI client and the API key for smolagents."""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.genai_client = genai.Client(api_key=api_key)

def get_gemini_client(api_key: str) -> ClientWrapper:
    """Initialise and return the wrapped GenAI client."""
    return ClientWrapper(api_key=api_key)

def call_gemini_with_retry(
    client: genai.Client,
    prompt: str,
    system_instruction: str,
    tools: Optional[list] = None,
    response_schema: Optional[Any] = None,
    status_ph: Any = None,
) -> Optional[str]:
    """Execute a Gemini API call with exponential backoff and structured output support."""
    config_kwargs = {
        "system_instruction": system_instruction,
        "temperature": 0.3,
    }
    if tools:
        config_kwargs["tools"] = tools
    if response_schema:
        config_kwargs["response_mime_type"] = "application/json"
        config_kwargs["response_schema"] = response_schema

    config = types.GenerateContentConfig(**config_kwargs)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("Calling Gemini API (Attempt %d/%d)...", attempt, MAX_RETRIES)
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=config,
            )
            return response.text
        except Exception as exc:
            logger.warning("Attempt %d failed: %s", attempt, exc)
            if status_ph:
                status_ph.warning(f"API attempt {attempt} failed. Retrying...")
            if attempt == MAX_RETRIES:
                logger.error("All Gemini API attempts failed.")
                if status_ph:
                    status_ph.error(f"❌ API Error: {exc}")
                return None
            time.sleep(RETRY_DELAY_SECONDS ** attempt)
    return None

def run_research_pass(
    client_wrapper: ClientWrapper,
    target_roles: list[str],
    status_ph: Any,
    selected_stream: str = "BSc Computer Science / IT",
) -> str:
    """Pass 0: Use smolagents ToolCallingAgent and DuckDuckGoSearchTool with Iterative Retrieval logic."""
    logger.info("Starting smolagents research pass...")
    if status_ph:
        status_ph.info("🕵️ Smolagents is launching search tools to research top PG certifications...")

    try:
        model = OpenAIModel(
            model_id="gemini-2.5-flash",
            api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=client_wrapper.api_key
        )
        
        search_tool = DuckDuckGoSearchTool()
        agent = ToolCallingAgent(
            tools=[search_tool],
            model=model,
            max_steps=6
        )
        
        roles_str = ", ".join(target_roles)
        prompt = (
            f"The user is a postgraduate/MBA student studying {selected_stream} who wants to obtain these target roles: {roles_str}.\n\n"
            "INSTRUCTIONS FOR ITERATIVE RETRIEVAL:\n"
            "1. Search the web for top FREE or open-source certifications suited for these roles.\n"
            "2. Read the search results critically.\n"
            "3. Evaluate: 'Are these certifications highly relevant, free, and fitting for a postgraduate/MBA level?'\n"
            "4. If not, refine your search terms and perform a follow-up query to find higher quality options.\n"
            "5. Present a final summary of the best 3-5 free certifications."
        )
        
        result = agent.run(prompt)
        return str(result)
    except Exception as exc:
        logger.warning("Smolagents research failed: %s. Falling back to native search pass...", exc)
        # Fallback to native GenAI search tool
        roles_str = ", ".join(target_roles)
        contents = (
            f"The user is a postgraduate student in {selected_stream} aiming to become one of the following: {roles_str}.\n\n"
            "Search the web for the absolute best, highly-recognized FREE or open-source online courses, bootcamps, and certifications "
            "that are highly recommended for these specific roles. Summarize the best 3-5 free courses."
        )
        tools = [types.Tool(google_search=types.GoogleSearch())]
        result = call_gemini_with_retry(
            client=client_wrapper.genai_client,
            prompt=contents,
            system_instruction="You are a career research assistant using Google Search to find high-value free courses.",
            tools=tools,
            status_ph=status_ph
        )
        return result or "No research data found."

def run_judge_pass(
    client: genai.Client,
    resume_data: dict,
    target_roles: list[str],
) -> tuple[bool, str]:
    """Pass 1.5: Judge Agent to evaluate if the resume contains corporate hallucinations or invalid structures."""
    prompt = (
        "You are an elite Resume Auditor.\n"
        f"Analyze this candidate's future resume JSON targeting these roles: {', '.join(target_roles)}.\n\n"
        f"RESUME JSON:\n{json.dumps(resume_data, indent=2)}\n\n"
        "Evaluate the resume based on the following criteria:\n"
        "1. Faithfulness: Does it contain hallucinated corporate jobs? (Check if experience contains projects/case studies instead of fake jobs at top tech firms).\n"
        "2. Relevance: Are the projects and skills highly relevant to the target roles?\n"
        "3. Dates: Are there US seasonal dates (e.g. Spring, Summer, Fall) instead of months or years?\n\n"
        "Respond strictly in JSON format matching the schema."
    )
    
    class JudgeResponse(BaseModel):
        Approved: bool
        Reason: str
        
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=JudgeResponse,
                temperature=0.1
            )
        )
        judge_res = json.loads(response.text)
        return judge_res.get("Approved", True), judge_res.get("Reason", "")
    except Exception as exc:
        logger.warning("Judge agent failed: %s. Defaulting to approved.", exc)
        return True, "Judge evaluation skipped due to API error."

def run_extraction_pass(
    client_wrapper: ClientWrapper,
    target_roles: list[str],
    research_summary: str,
    status_ph: Any,
    selected_stream: str = "BSc Computer Science / IT",
    degree_placeholder: str = "Bachelor of Science in Computer Science",
) -> Optional[dict]:
    """Pass 1: Generate the Future Resume JSON based on selected roles and free course research with Judge validation."""
    prompt = PASS1_USER_TEMPLATE.format(
        research_summary=research_summary,
        target_roles=", ".join(target_roles)
    )

    system_instruction = PASS1_SYSTEM_PROMPT.replace(
        "BSc Computer Science", selected_stream
    ).replace(
        "Bachelor of Science in Computer Science", degree_placeholder
    )

    # Core generation loop with Judge agent critique (Output Guardrails)
    for attempt in range(1, 3):
        if status_ph and attempt > 1:
            status_ph.warning("⚠️ Judge rejected the first draft. Regenerating resume with critique feedback...")

        result_text = call_gemini_with_retry(
            client=client_wrapper.genai_client,
            prompt=prompt if attempt == 1 else f"{prompt}\n\nRETRY INSTRUCTION: Correct the previous failures highlighted by the auditor.",
            system_instruction=system_instruction,
            response_schema=RESUME_SCHEMA,
            status_ph=status_ph
        )
        
        if not result_text:
            return None
            
        try:
            resume_data = json.loads(result_text)
            
            # Run output guardrail Judge check
            approved, reason = run_judge_pass(client_wrapper.genai_client, resume_data, target_roles)
            if approved:
                logger.info("Resume successfully approved by the Judge Agent.")
                return resume_data
            else:
                logger.warning("Judge rejected resume draft (Attempt %d): %s", attempt, reason)
                
        except json.JSONDecodeError as exc:
            logger.error("Pass 1 JSON parse failed: %s", exc)
            if status_ph:
                status_ph.error("❌ Failed to parse AI output (Pass 1).")
            return None
            
    # Fallback to last generated output if both attempts fail approval
    return resume_data

def run_enhancement_pass(
    client_wrapper: ClientWrapper,
    extracted_data: dict,
    status_ph: Any,
) -> dict:
    """Pass 2: Elevate the generated future resume to an elite standard."""
    input_json = json.dumps(extracted_data, indent=2)
    prompt = PASS2_USER_TEMPLATE.format(input_json=input_json)
    
    result_text = call_gemini_with_retry(
        client=client_wrapper.genai_client,
        prompt=prompt,
        system_instruction=PASS2_SYSTEM_PROMPT,
        response_schema=RESUME_SCHEMA,
        status_ph=status_ph
    )
    
    if not result_text:
        logger.warning("Pass 2 failed, falling back to Pass 1 data.")
        return extracted_data
        
    try:
        return json.loads(result_text)
    except json.JSONDecodeError as exc:
        logger.error("Pass 2 JSON parse failed: %s", exc)
        return extracted_data
