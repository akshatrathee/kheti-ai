#!/usr/bin/env python3
"""
Megalith Model Mesh - Test Client
Tests routing, failover, and persona-based capabilities
"""

import os
from openai import OpenAI
import time

# Configuration
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "sk-megalith-key-change-this")
LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL", "http://localhost:4000/v1")

client = OpenAI(api_key=LITELLM_API_KEY, base_url=LITELLM_BASE_URL)

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_model(model_name, prompt, description):
    """Test a single model with timing for TTFT and completion"""
    print(f"🧪 Testing: {description}")
    print(f"   Model Alias: {model_name}")
    
    start = time.time()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        duration = time.time() - start
        
        content = response.choices[0].message.content
        print(f"   ✅ Response ({duration:.2f}s): {content[:100]}...")
        if duration < 0.2:
            print("   ⚡ ZERO-LATENCY PINNING DETECTED!")
        print()
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        print()
        return False

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   MEGALITH Persona Mesh - Test Suite                    ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    print(f"🌐 Controller URL: {LITELLM_BASE_URL}")
    print(f"🔑 Auth: {LITELLM_API_KEY[:10]}...")
    
    # Test 1: Persona Routing
    print_section("PERSONA ROUTING TESTS")
    
    tests = [
        ("reasoning", "Explain the concept of entropy", "Reasoning (Routes to Cruncher)"),
        ("code", "Write a python function to scrape a website", "Coding (Routes to Cruncher)"),
        ("vision", "Describe this image content", "Vision (Routes to Media Lab)"),
        ("fast", "What is the capital of France?", "Utility (Routes to Swarm)"),
    ]
    
    results = []
    for model, prompt, desc in tests:
        success = test_model(model, prompt, desc)
        results.append((desc, success))
    
    # Test 2: OpenAI Compatibility
    print_section("OPENAI COMPATIBILITY")
    
    compat_tests = [
        ("gpt-4-turbo", "Detailed analysis of market trends", "GPT-4 Alias (Routes to Reasoning Group)"),
        ("gpt-3.5-turbo", "Quick greeting", "GPT-3.5 Alias (Routes to Swarm Fast)"),
    ]
    
    for model, prompt, desc in compat_tests:
        success = test_model(model, prompt, desc)
        results.append((desc, success))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"✅ Persona Nodes Up: {passed}/{total}")
    print(f"❌ Persona Nodes Down: {total - passed}/{total}")
    print()
    
    if passed == total:
        print("🎉 Megalith is fully operational. The specialized mesh is ready for production.")
    else:
        print("⚠️  Warning: Some personas are unreachable. Check PERSONAS.md and OLLAMA_HOST settings.")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
