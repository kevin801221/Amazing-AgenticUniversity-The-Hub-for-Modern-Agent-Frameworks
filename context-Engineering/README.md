# Context Engineering for AI Agents

![Context Engineering Overview](image/pic1.png)

## 📖 TL;DR

Agents need context to perform tasks. Context engineering is the art and science of filling the context window with just the right information at each step of an agent's trajectory. In this post, we break down some common strategies — **write, select, compress, and isolate** — for context engineering by reviewing various popular agents and papers. We then explain how LangGraph is designed to support them!

## 🎯 What is Context Engineering?

As Andrej Karpathy puts it, LLMs are like a [new kind of operating system](https://www.youtube.com/watch?si=-aKY-x57ILAmWTdw&t=620&v=LCEmiRjPEtQ&feature=youtu.be). The LLM is like the CPU and its context window is like the RAM, serving as the model's working memory. Just like RAM, the LLM context window has limited capacity to handle various sources of context.

![LLM as Operating System Analogy](image/pic2.png)

Karpathy summarizes this well:
> [Context engineering is the] "…delicate art and science of filling the context window with just the right information for the next step."

### Context Types in LLM Applications

Context engineering applies across different context types:
- **Instructions** – prompts, memories, few-shot examples, tool descriptions, etc
- **Knowledge** – facts, memories, etc
- **Tools** – feedback from tool calls

![Context Types](image/pic3.png)

## 🤖 Context Engineering for Agents

This year, interest in agents has grown tremendously as LLMs get better at reasoning and tool calling. Agents interleave LLM invocations and tool calls, often for long-running tasks.

![Agent Workflow](image/pic4.png)

However, long-running tasks and accumulating feedback from tool calls mean that agents often utilize a large number of tokens. This can cause numerous problems:

- **Context Poisoning**: When a hallucination makes it into the context
- **Context Distraction**: When the context overwhelms the training  
- **Context Confusion**: When superfluous context influences the response
- **Context Clash**: When parts of the context disagree

![Context Problems](image/pic5.png)

As **Cognition** noted:
> "Context engineering" … is effectively the #1 job of engineers building AI agents.

**Anthropic** also emphasized:
> Agents often engage in conversations spanning hundreds of turns, requiring careful context management strategies.

## 🏗️ The Four Pillars of Context Engineering

![Four Pillars Framework](image/pic6.png)

### 1. Write Context 📝
**Writing context means saving it outside the context window to help an agent perform a task.**

#### Scratchpads
When humans solve tasks, we take notes and remember things for future, related tasks. Agents are also gaining these capabilities! Note-taking via a "scratchpad" is one approach to persist information while an agent is performing a task.

**Example**: Anthropic's multi-agent researcher illustrates this clearly:
> The LeadResearcher begins by thinking through the approach and saving its plan to Memory to persist the context, since if the context window exceeds 200,000 tokens it will be truncated and it is important to retain the plan.

**Implementation approaches**:
- Tool call that writes to a file
- Field in a runtime state object that persists during the session

#### Memories
Scratchpads help agents solve a task within a given session, but sometimes agents benefit from remembering things across many sessions!

![Memory Types and Flow](image/pic7.png)

**Memory research foundations**:
- **Reflexion**: Introduced reflection following each agent turn
- **Generative Agents**: Created memories synthesized periodically from past feedback

**Real-world implementations**:
- ChatGPT's auto-generated long-term memories
- Cursor's memory features
- Windsurf's persistent context

### 2. Select Context 🎯
**Selecting context means pulling it into the context window to help an agent perform a task.**

#### From Scratchpads
- **Tool-based**: Agent reads via tool calls
- **State-based**: Developer controls what state to expose at each step

#### From Memories
Agents need to select memories relevant to their current task:

![Memory Selection Process](image/pic8.png)

**Memory types for selection**:
- **Episodic memories**: Few-shot examples for desired behavior
- **Procedural memories**: Instructions to steer behavior  
- **Semantic memories**: Facts for task-relevant context

**Selection challenges**:
- Ensuring relevant memories are selected
- Managing large collections of facts/relationships
- Avoiding unexpected memory retrieval

**Real examples**:
- Claude Code uses `CLAUDE.md`
- Cursor and Windsurf use rules files
- ChatGPT stores and selects from large user-specific memory collections

#### Tools
Agents can become overloaded with too many tools. RAG applied to tool descriptions can improve tool selection accuracy by **3-fold**.

#### Knowledge
RAG is central to context engineering. Code agents exemplify this challenge well. As Varun from Windsurf captures:

> Indexing code ≠ context retrieval … embedding search becomes unreliable as a retrieval heuristic as the size of the codebase grows … we must rely on a combination of techniques like grep/file search, knowledge graph based retrieval, and … a re-ranking step.

### 3. Compress Context 🗜️
**Compressing context involves retaining only the tokens required to perform a task.**

#### Context Summarization
Agent interactions can span hundreds of turns and use token-heavy tool calls. 

**Example**: Claude Code's "auto-compact" feature runs after exceeding 95% of context window, summarizing the full trajectory of user-agent interactions.

![Summarization Applications](image/pic9.png)

**Summarization strategies**:
- **Recursive**: Summarizing summaries for deep compression
- **Hierarchical**: Multi-level summarization
- **Targeted**: Focus on specific events or decisions

**Applications**:
- Post-processing token-heavy tool calls
- Agent-to-agent knowledge hand-offs
- Periodic conversation compression

#### Context Trimming
While summarization uses LLMs to distill context, trimming can filter or "prune" context using:
- Hard-coded heuristics (removing older messages)
- Trained context pruners (like Provence for Q&A)

### 4. Isolate Context 🏗️
**Isolating context involves splitting it up to help an agent perform a task.**

#### Multi-agent Isolation
Split context across sub-agents for separation of concerns.

![Multi-agent Context Isolation](image/pic10.png)

**Benefits**:
- Each agent has specific tools, instructions, and context window
- Subagents operate in parallel, exploring different aspects simultaneously
- Better performance through focused sub-tasks

**Challenges**:
- Up to **15× more tokens** than single-agent chat
- Careful prompt engineering required
- Complex sub-agent coordination

#### Environment Isolation
**Example**: HuggingFace's CodeAgent approach

![Environment Isolation with Sandboxes](image/pic11.png)

Instead of JSON tool calls, the agent outputs code that runs in a sandbox. Selected context from tool calls is passed back to the LLM.

**Benefits**:
- Better state handling
- Isolate token-heavy objects (images, audio, data)
- Clean separation between LLM and environment

#### State-based Isolation
An agent's runtime state object can isolate context. Design state schema with specific fields - expose only relevant fields to LLM at each turn while isolating other information for selective use.

## 🛠️ Implementation with LangGraph & LangSmith

Before starting, ensure you have:
1. **Observability**: Track token usage across your agent (LangSmith)
2. **Testing**: Simple way to test if context engineering improves performance

### Write Context

**Short-term memory** (thread-scoped):
```python
# Checkpointing persists agent state across all steps
# Useful as "scratchpad" - write to state, fetch at any step
```

**Long-term memory**:
```python
# Persist context across many sessions
# Save small files (user profiles, rules) or large memory collections
# LangMem provides memory management abstractions
```

### Select Context

```python
# Fine-grained control within each node
def agent_node(state):
    # Fetch specific state parts
    # Control what context to present to LLM
    pass
```

**Memory retrieval options**:
- File fetching
- Embedding-based retrieval on memory collections
- Semantic search over tool descriptions (LangGraph Bigtool)

![Email Agent with Memory](image/pic12.png)

### Compress Context

**LangGraph's low-level control**:
- Lay out agent as nodes with defined logic
- State object passed between nodes
- Built-in utilities for summarization/trimming
- Add summarization nodes at specific points
- Compress specific tool call outputs

### Isolate Context

**State object design**:
```python
# Specify state schema with fields for different context
# Store tool call context in specific fields
# Isolate from LLM until required
```

**Sandbox support**:
- E2B sandbox integration
- Pyodide sandboxing with state persistence

**Multi-agent libraries**:
- Supervisor pattern
- Swarm architecture

## 📚 Learning Resources

### Courses
- [DeepLearning.ai: Long-term Agentic Memory with LangGraph](https://www.deeplearning.ai/short-courses/long-term-agentic-memory-with-langgraph/)
- [Ambient Agents Course](https://academy.langchain.com/courses/ambient-agents)

### Documentation & Tutorials
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Observability](https://docs.smith.langchain.com/observability)
- [RAG Tutorials with LangGraph](https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/)

### Video Resources
- [Context Engineering Video](https://youtu.be/4GiqzUHD5AA)
- [Multi-agent Architecture Videos](https://www.youtube.com/watch?v=4nZl32FwU-o)

## 🎯 Key Takeaways

Context engineering is becoming a craft that agent builders should master. The four key patterns are:

1. **Writing context** - saving it outside the context window
2. **Selecting context** - pulling relevant information into context  
3. **Compressing context** - retaining only required tokens
4. **Isolating context** - splitting context strategically

**LangGraph** makes it easy to implement each pattern, while **LangSmith** provides observability and testing capabilities. Together, they enable a virtuous feedback loop for context engineering optimization.

## 📁 Repository Structure

```
context-engineering/
├── README.md
├── image/
│   ├── pic1.png    # Context engineering overview
│   ├── pic2.png    # LLM as OS analogy  
│   ├── pic3.png    # Context types
│   ├── pic4.png    # Agent workflow
│   ├── pic5.png    # Context problems
│   ├── pic6.png    # Four pillars framework
│   ├── pic7.png    # Memory types and flow
│   ├── pic8.png    # Memory selection process
│   ├── pic9.png    # Summarization applications
│   ├── pic10.png   # Multi-agent isolation
│   ├── pic11.png   # Environment isolation
│   └── pic12.png   # Email agent example
├── examples/
│   ├── scratchpad_example.py
│   ├── memory_selection.py
│   ├── context_compression.py
│   └── multi_agent_isolation.py
├── notebooks/
│   ├── context_engineering_walkthrough.ipynb
│   └── performance_benchmarks.ipynb
└── tutorials/
    ├── 01_write_context.md
    ├── 02_select_context.md  
    ├── 03_compress_context.md
    └── 04_isolate_context.md
```

---

*This module is part of AgenticU - The Modular Teaching Hub for Modern LLM Agent Frameworks*