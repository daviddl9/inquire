"""Core research orchestration."""

from pathlib import Path
from typing import Any

from inquire.baml_manager import BamlManager
from inquire.config import ResearchConfig
from inquire.exceptions import ExtractionError
from inquire.types import ConfigDict


class Researcher:
    """Main research orchestrator using BAML-generated types."""

    def __init__(
        self, baml_dir: Path | None = None, config: ConfigDict | None = None
    ):
        """Initialize researcher.

        Args:
            baml_dir: Path to BAML project directory (default: cwd/baml_schemas)
            config: Optional configuration overrides
        """
        self.config = ResearchConfig.from_dict(config or {})

        # Override baml_dir if provided
        if baml_dir:
            self.config.baml_dir = baml_dir

        self.baml_manager = BamlManager(self.config.baml_dir)

        # Validate configuration
        self.config.validate_or_raise()

    async def research(
        self,
        research_instructions: str,
        schema: type,
        baml_function: Any,
    ) -> Any:
        """Execute research with BAML extraction.

        Args:
            research_instructions: What to research (can include context/focus)
            schema: BAML-generated type (from baml_client.types)
            baml_function: BAML function callable (from baml_client.b)

        Returns:
            Instance of schema with researched data

        Raises:
            ResearchError: If research execution fails
            ExtractionError: If BAML extraction fails
        """
        # Initialize BAML if needed
        await self.baml_manager.init()

        # Verify function is valid
        self.baml_manager.verify_function(baml_function)

        # Execute research (stub for now)
        research_output = await self._run_research(research_instructions)

        # Call BAML function for extraction
        try:
            result = await baml_function(research_output)
        except Exception as e:
            raise ExtractionError(f"BAML extraction failed: {e}") from e

        # Validate result matches schema
        if not isinstance(result, schema):
            raise ExtractionError(
                f"BAML function returned {type(result)}, expected {schema}"
            )

        return result

    async def _run_research(self, instructions: str) -> str:
        """Execute deep research and return text output.

        This is a stub implementation. Real implementation will integrate
        with open-deep-research library.

        Args:
            instructions: Research instructions

        Returns:
            Research output as text
        """
        # TODO: Integrate with open-deep-research
        # For now, return placeholder
        return f"[Research output for: {instructions}]"


async def research(
    research_instructions: str,
    schema: type,
    baml_function: Any,
    config: ConfigDict | None = None,
) -> Any:
    """Convenience function for one-off research calls.

    Args:
        research_instructions: What to research (can include context/focus)
        schema: BAML-generated type (from baml_client.types)
        baml_function: BAML function callable (from baml_client.b)
        config: Optional configuration overrides

    Returns:
        Instance of schema with researched data
    """
    researcher = Researcher(config=config)
    return await researcher.research(
        research_instructions=research_instructions,
        schema=schema,
        baml_function=baml_function,
    )
