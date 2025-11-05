# inquire-py

**Intelligent inquiry with structured results**

Combine BAML's structured extraction with deep research capabilities to get type-safe, structured data from research queries.

## Quick Start

### 1. Install Dependencies

```bash
# Install the package
pip install inquire-py

# Install BAML CLI for schema management
npm install -g @boundaryml/baml
```

> **Note**: The package is installed as `inquire-py` but imported as `inquire` in Python.

### 2. Set Up API Keys

Create a `.env` file or export environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export TAVILY_API_KEY="tvly-..."
```

Get API keys:
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://tavily.com/ (for web search)

### 3. Initialize BAML Project

Create your project directory and initialize BAML:

```bash
mkdir my_research_project
cd my_research_project

# Initialize BAML with Python/Pydantic support
baml-cli init --client-type python/pydantic
```

This creates:
```
baml_schemas/
├── baml_src/
│   ├── clients.baml      # LLM client configurations
│   └── generators.baml   # Code generation settings
└── baml_client/          # Generated Python client (auto-created)
```

### 4. Define Your Schema

Create `baml_schemas/baml_src/research.baml` with your data structure:

```baml
class CompanyInfo {
  name string @description("Company's legal name")
  description string @description("What the company does")
  founders string[] @description("List of founder names")
  funding string | null @description("Total funding raised")
}

function ExtractCompanyInfo(research_output: string) -> CompanyInfo {
  client CustomGPT4o
  prompt #"
    Extract company information from the research output below.

    Research Output:
    {{ research_output }}

    {{ ctx.output_format }}
  "#
}
```

**Important**: Make sure to use client names defined in `baml_schemas/baml_src/clients.baml` (like `CustomGPT4o`, `CustomGPT4oMini`, etc.)

### 5. Generate Python Types

```bash
# Generate Python client from BAML schemas
baml-cli generate
```

This creates type-safe Python classes in `baml_client/` that you can import.

### 6. Use in Your Python Code

Create `research_companies.py`:

```python
import asyncio
from inquire import research
from baml_client.types import CompanyInfo
from baml_client import b

async def main():
    # Run research with structured extraction
    result = await research(
        research_instructions="Research Stripe: founders, funding, and what they do",
        schema=CompanyInfo,
        baml_function=b.ExtractCompanyInfo
    )

    # Result is type-safe with full IDE autocomplete
    print(f"Company: {result.name}")
    print(f"Description: {result.description}")
    print(f"Founders: {', '.join(result.founders)}")
    print(f"Funding: {result.funding}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python research_companies.py
```

## How It Works

1. **Research Phase**: `inquire` uses Tavily to search the web and OpenAI to synthesize findings
2. **Extraction Phase**: Your BAML function extracts structured data from the research
3. **Type Safety**: Returns a Pydantic model with full validation and IDE support

## Automatic BAML Initialization

If you skip the manual BAML setup, `inquire` will automatically initialize BAML on first run:

```python
from inquire import Researcher

# This will auto-initialize baml_schemas/ if it doesn't exist
researcher = Researcher()
await researcher.research(...)
```

After auto-initialization, add your schemas to `baml_schemas/baml_src/` and run `baml-cli generate`.

## Features

- ✅ **BAML-first** - Single source of truth, no sync issues
- ✅ **Type-safe** - Full IDE autocomplete and validation
- ✅ **Extensible** - Multiple BAML functions per schema
- ✅ **Simple API** - One function call does everything
- ✅ **Async by default** - Built for modern Python async/await
- ✅ **Configurable** - Customize models, search depth, and more

## Advanced Usage

### Multiple BAML Functions

Create different extraction functions for different use cases:

```baml
// baml_schemas/baml_src/research.baml

function ExtractBasicInfo(research_output: string) -> CompanyInfo {
  client CustomGPT4oMini  // Faster, cheaper
  prompt #"Extract basic company info from: {{ research_output }}"#
}

function ExtractDetailedAnalysis(research_output: string) -> CompanyInfo {
  client CustomGPT4o  // More detailed
  prompt #"
    You are a business analyst. Provide detailed analysis.
    {{ research_output }}
    {{ ctx.output_format }}
  "#
}
```

Then use different functions based on your needs:

```python
# Quick extraction
basic = await research(
    "Research Stripe",
    schema=CompanyInfo,
    baml_function=b.ExtractBasicInfo
)

# Detailed analysis
detailed = await research(
    "Research Stripe",
    schema=CompanyInfo,
    baml_function=b.ExtractDetailedAnalysis
)
```

### Custom Configuration

```python
from inquire import Researcher, ResearchConfig

config = ResearchConfig(
    research_model="gpt-4o",           # Model for research synthesis
    extraction_model="gpt-4o-mini",    # Model for BAML extraction
    max_search_queries=10,             # Number of web searches
    max_iterations=5,                  # Research depth
    search_api="tavily",               # Search provider
)

researcher = Researcher(config=config)

result = await researcher.research(
    research_instructions="Research OpenAI's latest models",
    schema=ModelInfo,
    baml_function=b.ExtractModelInfo
)
```

### Reusing Researcher Instance

For multiple queries, reuse the `Researcher` instance:

```python
researcher = Researcher()

# First query
company1 = await researcher.research(
    "Research Stripe",
    schema=CompanyInfo,
    baml_function=b.ExtractCompanyInfo
)

# Second query (BAML already initialized)
company2 = await researcher.research(
    "Research Shopify",
    schema=CompanyInfo,
    baml_function=b.ExtractCompanyInfo
)
```

## Project Structure

A typical project using `inquire-py`:

```
my_research_project/
├── baml_schemas/
│   ├── baml_src/
│   │   ├── clients.baml       # LLM configurations
│   │   ├── generators.baml    # Code generation settings
│   │   └── research.baml      # Your schemas and functions
│   └── baml_client/           # Generated (don't edit manually)
│       ├── __init__.py
│       ├── types.py
│       └── ...
├── .env                       # API keys
├── research_companies.py      # Your Python code
└── requirements.txt
```

Add to `.gitignore`:
```
baml_schemas/baml_client/
.env
```

## Requirements

- Python 3.11+
- Node.js (for BAML CLI)
- OpenAI API key
- Tavily API key

## License

MIT
