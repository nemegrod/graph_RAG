from agents import Agent, Runner, ModelSettings, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from openai.types.shared import Reasoning


from lib.tools import get_tool_definition, get_data

from pydantic import BaseModel

class GuardrailAgentOutput(BaseModel):
  is_not_allowed: bool
  reason: str | None


guardrail_agent = Agent(
    name="Guardrail agent",
    instructions="""
        You are a guardrail agent. 
          -- checking that the user input is related to jaguars.
          -- checking that the user input is not too long.
          -- checking that the user input is not too short.
          -- checking that the user input is not too vague.
          -- checking that the user input is not too specific.
          -- checking that the user input is not too general.
          -- checking that the user input is not too complex.
          -- checking that the user input is not too simple.
          -- checking that the user input is not too profane
          -- checking that the user input is not too sexual
          -- checking that the user input is not too violent
          -- checking that the user input is not too racist
          -- checking that the user input is not too sexist
          -- checking that the user input is not too ageist
          -- checking that the user input is not too religious
          -- checking that the user input is not too political
          -- checking that the user input is not too spammy


        You are responsible for checking if the user's input is allowed.
        If the user's input is not allowed, you should return the reason.

    """,
    tools=[],

    # här kan man sätta en mer naiv modell för att få ner kostnaderna
    output_type=GuardrailAgentOutput
    )

@input_guardrail
async def guardrail_function(context, agent, input_data)-> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input_data)
    return GuardrailFunctionOutput(
        output_info=result.final_output.reason,
        tripwire_triggered=result.final_output.is_not_allowed
    )



my_general_agent = Agent(
    name="Grapth agent",
    instructions="""
        You are a helpful assistant. 
        use the get_tool_definition function tool to formulate a valid SPARQL query.
        use get_data tool to retrive the information from the database. Use the valid SPARQL query as input to get the data.
            
        When responding:
        - answer the question based on the data retrieved from the database.
    """,
    tools=[get_tool_definition,
    get_data],
    model_settings=ModelSettings(reasoning=Reasoning(effort="minimal"), verbosity="low"),
    model="gpt-5",
    input_guardrails=[guardrail_function],
    output_guardrails=[]
    )

async def run_agent(user_input: str):
    try:
        result = await Runner.run(my_general_agent, user_input)
        return result.final_output
    except InputGuardrailTripwireTriggered as e:
        print("input guardrail tripwire triggered", e)
