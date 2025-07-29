---
name: "Gemini PydanticAI Agent PRP Template"
description: "Template for generating comprehensive PRPs for PydanticAI agent development projects, optimized for Gemini and uv."
---

## Purpose

[Brief description of the PydanticAI agent to be built and its main purpose]

## Core Principles

1.  **Gemini Optimized**: Designed to leverage the strengths of Google's Gemini models.
2.  **`uv` for Environments**: All Python environments and dependencies are managed exclusively by `uv`.
3.  **PydanticAI Best Practices**: Deep integration with PydanticAI patterns for agents, tools, and structured outputs.
4.  **Production Ready**: Includes security, testing, and monitoring for production deployments.
5.  **Type Safety First**: Leverages Pydantic's validation throughout the entire agent.
6.  **Comprehensive Testing**: Uses `TestModel` and `FunctionModel` for thorough agent validation.

## ❗ MANDATORY: Python Environment Management with `uv`

**All Python development for this project MUST use `uv` for environment and package management.** It is significantly faster and more efficient than traditional tools.

-   **To Create a Virtual Environment:**
    ```bash
    uv venv
    ```
    *(This creates a `.venv` directory in your project root.)*

-   **To Activate the Environment:**
    ```bash
    source .venv/bin/activate
    ```

-   **To Install a Package:**
    ```bash
    uv pip install <package-name>
    ```

-   **To Install from a requirements file:**
    ```bash
    uv pip install -r requirements.txt
    ```

-   **To Generate a requirements.txt:**
    ```bash
    uv pip freeze > requirements.txt
    ```

**Do NOT use `python -m venv`, `virtualenv`, or `pip` directly without `uv`.**

---

## ⚠️ Implementation Guidelines: Don't Over-Engineer

**IMPORTANT**: Keep your agent implementation focused and practical. Don't build unnecessary complexity.

### What NOT to do:
- ❌ **Don't create dozens of tools** - Build only the tools your agent actually needs.
- ❌ **Don't over-complicate dependencies** - Keep dependency injection simple.
- ❌ **Don't add unnecessary abstractions** - Follow established patterns directly.
- ❌ **Don't build complex workflows** unless specifically required.
- ❌ **Don't add structured output** unless validation is specifically needed (default to string).

### What TO do:
- ✅ **Start simple** - Build the minimum viable agent.
- ✅ **Add tools incrementally** - Implement only what the agent needs.
- ✅ **Follow reference examples** - Use proven patterns, don't reinvent.
- ✅ **Use string output by default** - Only add `result_type` when validation is required.
- ✅ **Test early and often** - Use `TestModel` to validate as you build.

### Key Question:
**"Does this agent really need this feature to accomplish its core purpose?"**

If the answer is no, don't build it. Keep it simple, focused, and functional.

---

## Goal

[Detailed description of what the agent should accomplish]

## Why

[Explanation of why this agent is needed and what problem it solves]

## What

### Agent Type Classification
- [ ] **Chat Agent**: Conversational interface with memory and context.
- [ ] **Tool-Enabled Agent**: Agent with external tool integration capabilities.
- [ ] **Workflow Agent**: Multi-step task processing and orchestration.
- [ ] **Structured Output Agent**: Complex data validation and formatting.

### Model Provider Requirements
- [ ] **Google**: `gemini-1.5-pro` (default) or `gemini-1.5-flash`.
- [ ] **OpenAI**: `openai:gpt-4o` or `openai:gpt-4o-mini`.
- [ ] **Anthropic**: `anthropic:claude-3-sonnet-20240229`.
- [ ] **Fallback Strategy**: Multiple provider support with automatic failover.

### External Integrations
- [ ] Database connections (specify type: PostgreSQL, MongoDB, etc.)
- [ ] REST API integrations (list required services)
- [ ] File system operations
- [ ] Web scraping or search capabilities

### Success Criteria
- [ ] Agent successfully handles specified use cases.
- [ ] All tools work correctly with proper error handling.
- [ ] Structured outputs validate according to Pydantic models.
- [ ] Comprehensive test coverage with `TestModel` and `FunctionModel`.
- [ ] Security measures implemented (API keys, input validation, rate limiting).
- [ ] Performance meets requirements (response time, throughput).

## All Needed Context

### PydanticAI Documentation & Research

```yaml
# ESSENTIAL PYDANTIC AI DOCUMENTATION - Must be researched
- url: https://ai.pydantic.dev/
  why: Official PydanticAI documentation with getting started guide.
  content: Agent creation, model providers, dependency injection patterns.

- url: https://ai.pydantic.dev/agents/
  why: Comprehensive agent architecture and configuration patterns.
  content: System prompts, output types, execution methods, agent composition.

- url: https://ai.pydantic.dev/tools/
  why: Tool integration patterns and function registration.
  content: "@agent.tool decorators, RunContext usage, parameter validation."

- url: https://ai.pydantic.dev/testing/
  why: Testing strategies specific to PydanticAI agents.
  content: TestModel, FunctionModel, Agent.override(), pytest patterns.

- url: https://ai.pydantic.dev/models/
  why: Model provider configuration and authentication.
  content: OpenAI, Anthropic, Gemini setup, API key management, fallback models.

# Prebuilt examples
- path: examples/
  why: Reference implementations for Pydantic AI agents.
  content: A bunch of already built simple Pydantic AI examples to reference.

- path: examples/main_agent_reference/
  why: Shows a robust, real-world structure for Pydantic AI agents.
  content: Demonstrates best practices for settings, providers, tools, and agent definition. This should be your primary reference.
```

### Agent Architecture Research

```yaml
# PydanticAI Architecture Patterns (follow main_agent_reference)
agent_structure:
  configuration:
    - settings.py: Environment-based configuration with pydantic-settings.
    - providers.py: Model provider abstraction with get_llm_model().
    - Environment variables for API keys and model selection.
    - Never hardcode model strings like "openai:gpt-4o".
  
  agent_definition:
    - Default to string output (no result_type unless structured output needed).
    - Use get_llm_model() from providers.py for model configuration.
    - System prompts as string constants or functions.
    - Dataclass dependencies for external services.
  
  tool_integration:
    - "@agent.tool" for context-aware tools with RunContext[DepsType].
    - Tool functions as pure functions that can be called independently.
    - Proper error handling and logging in tool implementations.
    - Dependency injection through RunContext.deps.
  
  testing_strategy:
    - TestModel for rapid development validation.
    - FunctionModel for custom behavior testing.
    - Agent.override() for test isolation.
    - Comprehensive tool testing with mocks.
```

### Security and Production Considerations

```yaml
# PydanticAI Security Patterns (research required)
security_requirements:
  api_management:
    environment_variables: ["GOOGLE_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    secure_storage: "Never commit API keys to version control."
    rotation_strategy: "Plan for key rotation and management."
  
  input_validation:
    sanitization: "Validate all user inputs with Pydantic models."
    prompt_injection: "Implement prompt injection prevention strategies."
    rate_limiting: "Prevent abuse with proper throttling."
  
  output_security:
    data_filtering: "Ensure no sensitive data in agent responses."
    content_validation: "Validate output structure and content."
    logging_safety: "Safe logging without exposing secrets."
```

### Implementation Blueprint

#### Technology Research Phase

**RESEARCH REQUIRED - Complete before implementation:**

✅ **PydanticAI Framework Deep Dive:**
- [ ] Agent creation patterns and best practices.
- [ ] Model provider configuration (especially for Gemini) and fallback strategies.
- [ ] Tool integration patterns (`@agent.tool` vs `@agent.tool_plain`).
- [ ] Dependency injection system and type safety.
- [ ] Testing strategies with `TestModel` and `FunctionModel`.

✅ **Agent Architecture Investigation:**
- [ ] Project structure conventions (`agent.py`, `tools.py`, `models.py`, `providers.py`).
- [ ] System prompt design for Gemini.
- [ ] Structured output validation with Pydantic models.
- [ ] Async/sync patterns and streaming support.
- [ ] Error handling and retry mechanisms.

✅ **Security and Production Patterns:**
- [ ] API key management and secure configuration.
- [ ] Input validation and prompt injection prevention.
- [ ] Rate limiting and monitoring strategies.
- [ ] Logging and observability patterns.

#### Agent Implementation Plan

```yaml
Implementation Task 1 - Agent Architecture Setup (Follow main_agent_reference):
  CREATE agent project structure:
    - settings.py: Environment-based configuration.
    - providers.py: Model provider abstraction.
    - agent.py: Main agent definition.
    - tools.py: Tool functions.
    - models.py: Pydantic models for data structures.
    - tests/: Comprehensive test suite.
  INITIALIZE environment with `uv venv`.

Implementation Task 2 - Core Agent Development:
  IMPLEMENT agent.py following main_agent_reference patterns:
    - Use get_llm_model() from providers.py.
    - Design a clear system prompt for Gemini.
    - NO `result_type` unless structured output is specifically needed.

Implementation Task 3 - Tool Integration:
  DEVELOP tools.py:
    - Use `@agent.tool` decorators.
    - Use `RunContext[DepsType]` for dependency access.
    - Implement robust error handling.

Implementation Task 4 - Data Models:
  CREATE models.py:
    - Pydantic models for any structured inputs or outputs.
    - Custom validators where necessary.

Implementation Task 5 - Comprehensive Testing:
  IMPLEMENT testing suite:
    - Use `TestModel` for rapid development.
    - Use `FunctionModel` for custom behavior.
    - Use `Agent.override()` for isolation.
    - Write integration tests with real providers.

Implementation Task 6 - Security and Configuration:
  SETUP security patterns:
    - Manage API keys via environment variables (`.env`).
    - Implement input sanitization.
```

### Validation Loop

```bash
# Level 1: Environment and Structure Validation
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
test -d .venv && echo "✅ uv environment created"
test -f agent_project/agent.py && echo "✅ Agent definition present"
test -f agent_project/tools.py && echo "✅ Tools module present"

# Level 2: Agent Functionality Validation
python -c "from agent_project.agent import agent; print('✅ Agent created successfully')"

# Level 3: Comprehensive Testing Validation
uv pip install pytest
pytest tests/ -v

# Level 4: Production Readiness Validation
grep -r "API_KEY" agent_project/ | grep -v ".py:" # Should not expose keys
test -f agent_project/.env.example && echo "✅ Environment template present"
```

## Final Validation Checklist

### Agent Implementation Completeness
- [ ] `uv` environment is set up and used correctly.
- [ ] Complete agent project structure is in place.
- [ ] Agent instantiates with Gemini model configuration.
- [ ] Tools are registered and tested.
- [ ] Dependency injection is properly configured.
- [ ] Comprehensive test suite passes.

### PydanticAI Best Practices
- [ ] Type safety is enforced everywhere.
- [ ] Security patterns are implemented.
- [ ] Error handling is robust.
- [ ] Code is well-documented.

### Production Readiness
- [ ] Configuration is managed via environment variables.
- [ ] Logging and monitoring are in place.
- [ ] Deployment process is defined.

---

## Anti-Patterns to Avoid

- ❌ **Don't use `pip` or `venv` without `uv`**. Stick to the mandated tool.
- ❌ **Don't hardcode API keys**. Use environment variables for all credentials.
- ❌ **Don't skip `TestModel` validation**. Test continuously during development.
- ❌ **Don't create monolithic tools**. Keep tools focused and composable.
- ❌ **Don't forget error handling**. Implement comprehensive retry and fallback mechanisms.
- ❌ **Don't ignore dependency injection**. Use proper type-safe dependency management.
- ❌ **Don't forget security**. Validate all inputs and outputs.
