# inquire

**Intelligent inquiry with structured results**

Combine BAML's structured extraction with deep research capabilities.

## Installation

```bash
pip install inquire
```

## Quick Start

### 1. Define Schema in BAML

Create `baml_schemas/baml_src/company.baml`:

```baml
class CompanyInfo {
  name string @description("Company's legal name")
  description string @description("What the company does")
  founders string[] @description("List of founder names")
}

function ExtractCompanyInfo(research_output: string) -> CompanyInfo {
  client GPT4
  prompt #"
    Extract company information from the research:

    {{ research_output }}
    {{ ctx.output_format }}
  "#
}
```

### 2. Use in Python

```python
import asyncio
from inquire import research
from baml_client.types import CompanyInfo
from baml_client import b

async def main():
    result = await research(
        research_instructions="Research Stripe's founders",
        schema=CompanyInfo,
        baml_function=b.ExtractCompanyInfo
    )

    print(f"Company: {result.name}")
    print(f"Founders: {', '.join(result.founders)}")

asyncio.run(main())
```

## Features

- ✅ **BAML-first** - Single source of truth, no sync issues
- ✅ **Type-safe** - Full IDE autocomplete and validation
- ✅ **Extensible** - Multiple BAML functions per schema
- ✅ **Simple API** - One function call does everything

## Configuration

Set environment variables:

```bash
export OPENAI_API_KEY="your-key"
export TAVILY_API_KEY="your-key"  # For web search
```

Or pass config explicitly:

```python
from inquire import Researcher

researcher = Researcher(config={
    "openai_api_key": "your-key",
    "research_model": "gpt-4o",
})
```

## License

MIT
