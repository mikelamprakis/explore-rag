# Agentic Debate App

A CrewAI-powered application that orchestrates AI agents to conduct structured debates on any given topic. The app uses specialized AI agents to argue both sides of a motion and an impartial judge to evaluate and decide the winner.

## What This App Does

The Agentic Debate App simulates a formal debate process using autonomous AI agents:

1. **Debate Motion**: You provide a debate topic (motion) - for example, "The round pizza is better than square pizza"

2. **Proposing Arguments**: A specialized debater agent generates compelling arguments **in favor** of the motion, presenting the case for the affirmative side

3. **Opposing Arguments**: The same debater agent (or you can configure separate agents) generates strong arguments **against** the motion, presenting the case for the negative side

4. **Judgment**: An impartial judge agent reviews both sets of arguments, evaluates their merit, and makes an objective decision about which side presented a more convincing case

5. **Output**: All arguments and the final decision are saved to markdown files in the `src/output/` directory:
   - `propose.md`: Arguments in favor of the motion
   - `oppose.md`: Arguments against the motion
   - `decide.md`: Judge's evaluation and decision

The app uses **sequential processing** to ensure that arguments are generated before the judge evaluates them, creating a realistic debate flow where the judge has access to both sides before making a decision.

### Key Features

- 🤖 **AI-Powered Debating**: Uses advanced LLMs to generate nuanced arguments
- ⚖️ **Impartial Judging**: Judge agent evaluates based on argument quality, not personal bias
- 📝 **Structured Output**: Results saved in organized markdown files
- ⚙️ **Configurable**: Easy to modify agents, tasks, and debate topics via YAML configuration
- 🔄 **Sequential Workflow**: Ensures proper debate flow with dependencies between tasks

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up environment variables:**
   Create a `.env` file with your API keys: 
   ```
   OPENAI_API_KEY=your_key_here
   ```


## Running the App

**Option 1: Using uv run (recommended)**
   ```bash
   uv run python -m src.main
   ```

**Option 2: Activate virtual environment first**
   ```bash
   source .venv/bin/activate
   python -m src.main
   ```

**Option 3: Direct Python execution**
   ```bash
   uv run python src/main.py
   ```

## Project Structure

- `src/main.py`: Application entry point - defines the debate motion and runs the crew
- `src/crew.py`: Defines the DebateApp crew with agents and tasks
- `src/config/agents.yaml`: Configuration for debater and judge agents
- `src/config/tasks.yaml`: Configuration for propose, oppose, and decide tasks
- `src/output/`: Directory where debate results are saved
- `docs/`: Documentation including architecture and CrewAI framework details

## Customization

You can easily customize the debate by:

- **Changing the motion**: Edit the `motion` value in `src/main.py`
- **Modifying agents**: Update personalities, goals, or backstories in `src/config/agents.yaml`
- **Adjusting tasks**: Change task descriptions or expected outputs in `src/config/tasks.yaml`
- **Adding agents**: Create new agent types (e.g., moderator, fact-checker) for more complex debates

For more details, see the [Architecture Documentation](docs/ARCHITECTURE.md).

