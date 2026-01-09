import os
from dotenv import load_dotenv
from src.agent import create_math_agent


def main():
    """Função principal para execução interativa do agente."""
    load_dotenv()
    
    print("=" * 60)
    print("🤖 AI Math Agent - Agente ReAct com LangChain")
    print("=" * 60)
    print("\nConfigurando agente...")
    
    try:
        agent = create_math_agent(
            model_name=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0")),
            verbose=True
        )
        
        print("✅ Agente configurado com sucesso!\n")
        print("Digite suas perguntas (matemáticas ou gerais).")
        print("Digite 'sair' ou 'quit' para encerrar.\n")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n👤 Você: ").strip()
                
                if user_input.lower() in ['sair', 'quit', 'exit', 'q']:
                    print("\n👋 Encerrando agente. Até logo!")
                    break
                
                if not user_input:
                    continue
                
                print("\n🤖 Agente:")
                response = agent.invoke({"input": user_input})
                
                if "output" in response:
                    print(response["output"])
                
                print("-" * 60)
                
            except KeyboardInterrupt:
                print("\n\n👋 Encerrando agente. Até logo!")
                break
            except Exception as e:
                print(f"\n❌ Erro: {str(e)}")
                print("-" * 60)
                
    except ValueError as e:
        print(f"\n❌ Erro de configuração: {str(e)}")
        print("\nCertifique-se de que:")
        print("1. O arquivo .env existe e contém OPENAI_API_KEY")
        print("2. A API key é válida")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")


if __name__ == "__main__":
    main()
