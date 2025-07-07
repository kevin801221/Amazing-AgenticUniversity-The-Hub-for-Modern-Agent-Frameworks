# 🎓 AgenticU: The Modular Teaching Hub for Modern LLM Agent Frameworks

Welcome to **AgenticU** — a curated, multi-project teaching repository focused on building modern Agentic AI systems with LLMs.

This project is built from my teaching journeys across Everywhere: in classrooms, workshops, and corporate trainings.  
Inside, you’ll find **hands-on tutorials, code examples, and full project demos** built with the latest frameworks in the LLM agent ecosystem, including:

- LangChain
- LangGraph
- AutoGen
- LlamaIndex
- RAG / CRAG
- OpenAI Function Calling
- More coming soon...

I'll update this repo every week, even every day maybe. If you have any questions, please feel free to ask. ""Your Stars are my motivation"" to continue updating this repo.🤩 
---

## 🧩 What's Inside?

Each folder in this repository is a standalone project or tutorial, covering a specific agentic technique, workflow, or framework.

Some are full applications, others are Jupyter notebook experiments.  
They’re all designed to help you **learn by building**.

Example folders might include:

```
agentic_u/
├── langgraph_agents/
├── autogen_planner/
├── rag_crag_search_demo/
├── openai_function_calling/
├── agentic_ui_streamlit/
├── notebook_demos/
├── Controllable-RAG-Agent/
├── business-intelligence-ai-SQL-dashboard/
```

---

## 📜 Archived History

Looking for the full archive from my previous teaching repo?  
You’ll find detailed update logs, course plans, and project notes in:

👉 [`README_old.md`](.Old_README.md)

This archive comes from my original repo —  
`AgenticAI_LLMs_Amazing_courses_Langchain_LlamaIndex` — which once had over 29stars before deletion.

---

## 📦 Projects Overview   
| Folder | Description |
|--------|-------------|
| `langgraph_agents/` | Stateful agents with LangGraph |
| `autogen_planner/` | Multi-agent coordination using AutoGen |
| `Agentic_Stock_Insight/` | An application for stock data insights, combining RAG workflows to extract insights from news and financial data. |
| `Short-Long_term_memory_simulation/` | An application for simulating short and long term memory |
| `ai-agent-papers/` | A curated collection of research papers on AI Agents, covering capabilities, architectures, and real-world applications, updated biweekly. |
| `context-Engineering/` | A complete tutorial on context engineering for AI agents. |
| `langgraph-bigtool/` | A library for creating LangGraph agents that can access a large number of tools. |
| `Controllable-RAG-Agent/` | A sophisticated RAG agent implementation with controllable parameters for Harry Potter knowledge base. |
| `business-intelligence-ai-SQL-dashboard/` | An AI-driven dashboard system that connects to SQL databases and creates visualizations without writing queries. |

<!-- Keep join -->

---

## 🆕 Update Log     

- **2025/07/07** — Added `business-intelligence-ai-SQL-dashboard/` with an AI-driven dashboard system for SQL databases.
- **2025/07/07** — Added `Controllable-RAG-Agent/` with a sophisticated RAG agent for Harry Potter knowledge base.
- **2025/07/03** — Added `langgraph-bigtool/` with a library for creating LangGraph agents that can access a large number of tools.
- **2025/07/03** — Added `context-Engineering/` with a complete tutorial on context engineering for AI agents.
- **2025/07/01** — Added `ai-agent-papers/` with a curated collection of research papers on AI Agents.
- **2025/06/29** — Added `Short-Long_term_memory_simulation/` with short and long term memory simulation, that uses LangGraph to simulate a conversation between human philosophers.     
- **2025/06/29** — Added `Agentic_Stock_Insight/` with stock data analysis and news RAG workflows      
- **2025/06/27** — Initial repo relaunch, added ``, ``
- **2025/06/29** — Added `notebook_demos/` with Streamlit + RAG examples

<!-- Keep join -->
---

## 🙌 A Note to My Previous Supporters

> This is the successor to my original Agentic AI teaching repo,  
> which once had over a thousand stars before it was accidentally deleted.

If you supported that work before — thank you.  
I’m rebuilding it here, even better, and would love your support again ⭐

---

## 🤝 Contribute / Collaborate

Educators, engineers, learners — all are welcome.

Feel free to explore, fork, submit PRs, or reach out to collaborate.

📫 kilong31442@gmail.com

---

> **Let’s teach the future of Agentic AI — together, one project at a time.**

---
# Context Engineering for AI Agents: A Complete Tutorial

## Table of Contents
1. [Introduction](#introduction)
2. [Understanding Context Types](#understanding-context-types)
3. [The Four Pillars of Context Engineering](#the-four-pillars-of-context-engineering)
4. [Implementation Strategies](#implementation-strategies)
5. [Best Practices](#best-practices)
6. [Conclusion](#conclusion)

## Introduction

As AI agents become more sophisticated, managing their context efficiently has become crucial. **Context engineering** is the art and science of filling an LLM's context window with precisely the right information at each step of an agent's execution.

### Why Context Engineering Matters

Think of LLMs as a new kind of operating system where:
- The **LLM** acts as the CPU
- The **context window** serves as RAM (working memory)
- **Context engineering** functions like an OS managing what fits into RAM

As Andrej Karpathy describes it: Context engineering is the *"delicate art and science of filling the context window with just the right information for the next step."*

### Common Context Challenges

Long-running agent tasks often lead to:
- **Context Poisoning**: Hallucinations entering the context
- **Context Distraction**: Context overwhelming the training
- **Context Confusion**: Superfluous context influencing responses
- **Context Clash**: Contradictory information in context

## Understanding Context Types

Before diving into strategies, let's identify the main types of context in LLM applications:

### 1. Instructions
- Prompts and system messages
- Few-shot examples
- Tool descriptions
- Behavioral guidelines

### 2. Knowledge
- Facts and information
- Domain-specific data
- Historical context

### 3. Tools
- Tool call feedback
- API responses
- Environment state

## The Four Pillars of Context Engineering

### 1. Write Context 📝

**Purpose**: Save information outside the context window for future use.

#### Scratchpads
Agents can take "notes" during task execution, similar to human problem-solving.

**Implementation approaches**:
- Tool calls that write to files
- Runtime state object fields
- Persistent session storage

**Example use case**: 
When Anthropic's multi-agent researcher exceeds 200,000 tokens, it saves its plan to memory to prevent truncation loss.

#### Memories
Persist information across multiple sessions for long-term learning.

**Types of memories**:
- **Episodic**: Specific experiences and examples
- **Procedural**: Instructions and behavioral patterns  
- **Semantic**: Facts and relationships

**Real-world examples**:
- ChatGPT's auto-generated user memories
- Cursor's rules files
- Windsurf's persistent context

### 2. Select Context 🎯

**Purpose**: Pull relevant information into the context window when needed.

#### From Scratchpads
- **Tool-based**: Agent reads via tool calls
- **State-based**: Developer controls what state to expose

#### From Memories
Select memories relevant to current tasks:
- Few-shot examples for desired behavior
- Instructions for behavioral steering
- Facts for task-relevant context

**Selection challenges**:
- Ensuring relevance (avoid unexpected injections)
- Managing large memory collections
- Maintaining user control over context

**Selection methods**:
- Embedding-based similarity search
- Knowledge graph traversal
- Rule-based filtering

#### Tool Selection
Use RAG on tool descriptions to avoid tool overload and confusion.

**Benefits**:
- 3x improvement in tool selection accuracy
- Reduced model confusion
- Better task performance

### 3. Compress Context 🗜️

**Purpose**: Retain only essential tokens for task completion.

#### Context Summarization
**When to use**:
- Multi-turn conversations spanning hundreds of interactions
- Token-heavy tool call results
- Agent-to-agent knowledge handoffs

**Summarization strategies**:
- **Recursive**: Summarize summaries for deep compression
- **Hierarchical**: Multi-level summarization
- **Targeted**: Focus on specific events or decisions

**Example**: Claude Code's auto-compact feature summarizes full interaction trajectories when approaching context limits.

#### Context Trimming
**Approaches**:
- **Hard-coded heuristics**: Remove older messages
- **Trained pruners**: ML models for intelligent filtering
- **Rule-based filtering**: Remove based on content type or relevance

### 4. Isolate Context 🏗️

**Purpose**: Split context across different spaces to manage complexity.

#### Multi-Agent Architecture
Distribute context across specialized sub-agents.

**Benefits**:
- Each agent focuses on narrow sub-tasks
- Parallel processing of different aspects
- Cleaner separation of concerns

**Challenges**:
- Increased token usage (up to 15x more)
- Complex coordination requirements
- Careful prompt engineering needed

#### Environment Isolation
Use sandboxes to isolate token-heavy objects from the LLM.

**Example**: HuggingFace's CodeAgent runs tool calls in sandboxes, passing only selected results back to the LLM.

**Advantages**:
- Better state management
- Isolation of large objects (images, audio, data)
- Reduced context pollution

#### State-Based Isolation  
Use structured state objects with selective field exposure.

**Implementation**:
- Design schema with specific fields for different context types
- Expose only relevant fields to LLM at each step
- Maintain isolated storage for later use

## Implementation Strategies

### Getting Started

#### 1. Observability First
- Track token usage across agent interactions
- Monitor context window utilization
- Identify bottlenecks and inefficiencies

#### 2. Establish Testing Framework
- Create evaluation metrics for agent performance
- Test context engineering changes systematically
- Measure impact on task success rates

### LangGraph Implementation Examples

#### Write Context
```python
# Short-term memory (scratchpad)
class AgentState(TypedDict):
    messages: List[BaseMessage]
    scratchpad: Dict[str, Any]
    
# Long-term memory
memory = LangGraphMemory()
memory.save("user_preferences", user_data)
```

#### Select Context
```python
# Fine-grained state control
def agent_node(state: AgentState):
    relevant_context = select_relevant_memories(state.current_task)
    # Only include what's needed for this step
    return {"context": relevant_context}
```

#### Compress Context
```python
# Periodic summarization
def summarize_if_needed(state: AgentState):
    if len(state.messages) > threshold:
        summary = summarize_conversation(state.messages)
        return {"messages": [summary] + state.messages[-5:]}
    return state
```

#### Isolate Context
```python
# Multi-agent isolation
supervisor = SupervisorAgent()
research_agent = ResearchAgent()
writing_agent = WritingAgent()

# Each agent maintains separate context
```

## Best Practices

### 1. Context Auditing
- Regularly review what's in your context
- Remove redundant or outdated information
- Monitor for context pollution

### 2. Selective Exposure
- Don't dump everything into context
- Use relevance scoring for memory selection
- Implement context freshness tracking

### 3. Hierarchical Organization
- Structure context in layers (immediate, session, long-term)
- Use different strategies for different context types
- Maintain clear separation between context categories

### 4. Performance Monitoring
- Track context-to-performance relationships
- A/B test different context strategies
- Monitor token costs and latency

### 5. User Control
- Allow users to influence context selection
- Provide transparency in what context is being used
- Enable users to correct or override context decisions

## Common Pitfalls to Avoid

### ❌ Context Overload
Don't include everything "just in case" - be selective and purposeful.

### ❌ Stale Context
Regularly refresh and validate context relevance.

### ❌ Ignoring User Intent
Ensure context selection aligns with user goals and expectations.

### ❌ Over-Compression
Don't lose critical information in pursuit of token efficiency.

### ❌ Poor Isolation
Maintain clear boundaries between different types of context.

## Conclusion

Context engineering is becoming an essential skill for AI agent developers. The four pillars - **Write**, **Select**, **Compress**, and **Isolate** - provide a comprehensive framework for managing context effectively.

### Key Takeaways

1. **Context is finite** - Treat it as a precious resource
2. **Strategy matters** - Different context types need different approaches  
3. **Observability is crucial** - You can't optimize what you can't measure
4. **Testing is essential** - Always validate that context changes improve performance
5. **User experience counts** - Context decisions should enhance, not surprise users

### Next Steps

1. Audit your current agent's context usage
2. Identify the biggest context inefficiencies
3. Implement one pillar at a time
4. Measure and iterate on improvements
5. Scale successful patterns across your agent architecture

Remember: Context engineering is both an art and a science. Start with solid observability, experiment systematically, and always keep the end-user experience in mind.

---

*For more advanced implementations and examples, explore LangGraph's documentation and consider the LangSmith platform for comprehensive agent observability and testing.*

---

*This tutorial was inspired by insights from Andrej Karpathy, Andrew Ng, and the LangChain team.*