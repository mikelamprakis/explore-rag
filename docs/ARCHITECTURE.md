# Architecture Documentation

## Overview

The Agentic Debate App is built using CrewAI, a framework for orchestrating role-playing, autonomous AI agents. The application implements a structured debate system where AI agents argue for and against a given motion, with a judge agent evaluating the arguments.

## Project Structure

```
agentic-debate-app/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── crew.py              # CrewAI crew definition
│   ├── config/
│   │   ├── agents.yaml      # Agent configurations
│   │   └── tasks.yaml       # Task definitions
│   └── output/              # Generated debate outputs
│       ├── propose.md       # Arguments in favor
│       ├── oppose.md        # Arguments against
│       └── decide.md        # Judge's decision
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md      # This file
│   └── CrewAI.md           # CrewAI framework documentation
├── pyproject.toml          # Project dependencies and configuration
├── uv.lock                 # Dependency lock file
└── README.md               # Project overview and setup instructions
```

## Architecture Components

### 1. Main Entry Point (`src/main.py`)

The `main.py` file serves as the application entry point. It:
- Defines the debate motion (input)
- Initializes the `DebateApp` crew
- Executes the crew workflow
- Handles errors and displays results

**Key Function:**
- `run()`: Orchestrates the debate execution with a predefined motion

### 2. Crew Definition (`src/crew.py`)

The `crew.py` file defines the `DebateApp` class using CrewAI's `@CrewBase` decorator. This class:

- **Agents**: Defines two specialized agents:
  - `debater`: Handles both proposing and opposing arguments
  - `judge`: Evaluates arguments and makes a decision

- **Tasks**: Defines three sequential tasks:
  - `propose`: Generate arguments in favor of the motion
  - `oppose`: Generate arguments against the motion
  - `decide`: Judge evaluates and decides the winner

- **Crew Configuration**: Uses `Process.sequential` to ensure tasks execute in order, allowing the judge to review both arguments before making a decision.

### 3. Configuration Files

#### Agents Configuration (`src/config/agents.yaml`)

Defines the personality, goals, and behavior of each agent:

- **Debater Agent**:
  - Role: Compelling debater
  - Goal: Present clear arguments for or against the motion
  - Backstory: Experienced debater with concise, convincing argumentation skills
  - LLM: Uses OpenAI's GPT-4o-mini model

- **Judge Agent**:
  - Role: Fair debate judge
  - Goal: Evaluate arguments objectively based on merit
  - Backstory: Reputation for impartial evaluation
  - LLM: Uses OpenAI's GPT-4o-mini model

#### Tasks Configuration (`src/config/tasks.yaml`)

Defines the workflow tasks:

- **Propose Task**: 
  - Description: Generate convincing arguments in favor of the motion
  - Agent: debater
  - Output: Saved to `output/propose.md`

- **Oppose Task**:
  - Description: Generate convincing arguments against the motion
  - Agent: debater
  - Output: Saved to `output/oppose.md`

- **Decide Task**:
  - Description: Review both arguments and determine the winner
  - Agent: judge
  - Output: Saved to `output/decide.md`

## Workflow

The application follows a sequential process:

1. **Initialization**: The motion is defined in `main.py`
2. **Propose Phase**: The debater agent generates arguments in favor of the motion
3. **Oppose Phase**: The debater agent generates arguments against the motion
4. **Decision Phase**: The judge agent reviews both arguments and makes a decision
5. **Output**: All results are saved to markdown files in the `output/` directory

## Design Patterns

### Configuration-Driven Design

The application uses YAML configuration files to define agents and tasks, making it easy to:
- Modify agent personalities without changing code
- Adjust task descriptions and expected outputs
- Experiment with different debate formats

### Sequential Processing

The crew uses `Process.sequential` to ensure:
- Arguments are generated before the judge evaluates
- The judge has access to both sides of the debate
- Output files are created in the correct order

### Separation of Concerns

- **Configuration**: YAML files for easy modification
- **Logic**: Python classes for crew orchestration
- **Execution**: Main entry point for running debates
- **Output**: Structured markdown files for results

## Extensibility

The architecture supports easy extension:

1. **Additional Agents**: Add new agent types (e.g., moderator, fact-checker) in `agents.yaml` and `crew.py`
2. **New Tasks**: Define additional tasks in `tasks.yaml` (e.g., rebuttal, closing statements)
3. **Different Process Types**: Switch from sequential to hierarchical or consensual processing
4. **Custom Tools**: Integrate CrewAI tools for research, fact-checking, or data analysis
5. **Multiple Debates**: Modify `main.py` to handle multiple motions or batch processing

## Dependencies

- **CrewAI**: Core framework for agent orchestration
- **OpenAI API**: LLM provider for agent reasoning (configurable to Anthropic or others)
- **Python 3.13+**: Required Python version
- **uv**: Package manager for dependency management

