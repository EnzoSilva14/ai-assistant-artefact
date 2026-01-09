# AI Math Agent

## Como executar
- Criar venv e ativar  
  - Windows: `python -m venv env && .\env\Scripts\activate`  
  - Linux/Mac: `python -m venv env && source env/bin/activate`
- Instalar: `pip install -r requirements.txt`
- Criar `.env` a partir de `env.example` e definir `OPENAI_API_KEY`
- Rodar CLI: `python main.py`  
  Ou API: `python api.py` (http://localhost:8000/docs)

## Lógica de implementação
- Agent com LangChain: o LLM roteia a intenção e chama tools.
- Tools: `calculator` (numexpr), `unit_converter` (comprimento/peso/temperatura/volume), `fx_converter` (câmbio via exchangerate.host com fallback).
- Prompt força: matemática → calculator; unidades físicas → unit_converter; moedas → fx_converter; geral → resposta direta. Cálculos/conversões sempre via tools.

## O que aprendi e o que faria diferente
- Aprendido: roteamento claro reduz alucinação; fallback de câmbio aumenta robustez.
- Com mais tempo: ampliar unidades/moedas, cache de taxas, testes automatizados e logs estruturados.

