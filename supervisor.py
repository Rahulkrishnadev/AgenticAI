from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
api_key=""
llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=api_key,
    max_tokens=None,
)



@tool
def web_search(query:str):
    """search the web for information"""
    search=DuckDuckGoSearchResults()
    return search.invoke(query)


@tool
def Add(a:int,b:int):
    """Function to add two numbers"""
    sum= a+b
    return sum

@tool
def even(num):
    """function to find even/odd numbers"""
    if num%2==0:
        return "It is a even numbers"
    else:
        return "It is  odd one" 
    
math_agent=create_react_agent(
    model=llm,
    tools=[Add,even],
    name="math_expert",
    prompt="You are a math expert.Always use one tool at a time"


)

research_agent=create_react_agent(
    model=llm,
    tools=[web_search],
    name="research_expert",
    prompt=(
        "you are a world class reasercher with access to web search.Do not do any math"
    )
)


workflow=create_supervisor(
    [math_agent,research_agent],
    model=llm,
    prompt="""Your are a supervisor managing a research expert and a math expert.For current events use research_agent and for math problems use math_agent ."""
)

app=workflow.compile()
result=app.invoke(
    {
        # "messages":[HumanMessage(content="Who is known as the chase master in the cricket world")]
        "messages":[
            {
                'role':"user",
                "content":"is 21 an even or odd number?"
            }
        ]
    }
)
print(result)