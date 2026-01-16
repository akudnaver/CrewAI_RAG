from crewai.tools import BaseTool
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException
from typing import Type
from pydantic import BaseModel, Field


class MarkdownValidationInput(BaseModel):
    filename: str = Field(..., description="Path to the markdown file")


class MarkdownValidationTool(BaseTool):
    name: str = "markdown_validation_tool"
    description: str = (
        "Validate a markdown file and return linting issues. "
        "Input must be a file path."
    )
    args_schema: Type[BaseModel] = MarkdownValidationInput

    def _run(self, filename: str) -> str:
        api = PyMarkdownApi()

        try:
            results = api.scan_path(filename)
            if not results:
                return "Markdown is valid. No issues found."
            return "\n".join(results)
        except PyMarkdownApiException as e:
            return f"Markdown validation failed: {str(e)}"
