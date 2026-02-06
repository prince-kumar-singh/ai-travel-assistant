import sys
import json
import argparse
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent

def main():
    parser = argparse.ArgumentParser(description="AI Smart Travel Ops Assistant")
    parser.add_argument("query", nargs="?", type=str, help="The travel query (e.g., 'Is it safe to travel to Delhi tomorrow?')")
    args = parser.parse_args()

    user_query = args.query
    if not user_query:
        print("Please provide a query.")
        print("Usage: python main.py \"Your query here\"")
        return

    print(f"✈️  AI Smart Travel Ops Assistant")
    print(f"Query: {user_query}\n")

    # 1. Planner Agent
    print("🧠 Planner Agent: Analyzing query...")
    planner = PlannerAgent()
    plan = planner.plan(user_query)
    
    if "error" in plan:
        print(f"❌ Planning failed: {plan['error']}")
        return
        
    print(f"📋 Plan generated: {json.dumps(plan, indent=2)}\n")

    # 2. Executor Agent
    print("⚙️  Executor Agent: Running tools...")
    executor = ExecutorAgent()
    context = executor.execute_plan(plan)
    
    if "error" in context:
        print(f"❌ Execution failed: {context['error']}")
        return

    # 3. Verifier Agent
    print("✅ Verifier Agent: Validating and summarizing...")
    verifier = VerifierAgent()
    final_response = verifier.verify_and_respond(context)

    print("\n" + "="*40)
    print("       FINAL RECOMMENDATION       ")
    print("="*40)
    print(json.dumps(final_response, indent=2))

if __name__ == "__main__":
    main()
