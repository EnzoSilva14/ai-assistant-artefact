import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.tools import calculator, unit_converter, fx_converter
from src.prompts import SYSTEM_PROMPT


def create_math_agent(
    model_name: str = "gpt-4o-mini",
    temperature: float = 0.0,
    verbose: bool = True
) -> AgentExecutor:
    """
    Cria e configura o agente para resolução de problemas matemáticos.
    
    Args:
        model_name: Nome do modelo OpenAI a ser usado
        temperature: Temperatura do modelo (0 para máxima precisão)
        verbose: Se True, exibe logs detalhados do processo de raciocínio
        
    Returns:
        AgentExecutor configurado e pronto para uso
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY não encontrada. "
            "Configure a variável de ambiente ou crie um arquivo .env"
        )
    
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=api_key
    )
    
    tools = [calculator, unit_converter, fx_converter]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        handle_parsing_errors=True,
        max_iterations=10,
        max_execution_time=30
    )
    
    return agent_executor
