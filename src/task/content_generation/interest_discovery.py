"""
Interest Discovery component for AI-driven content generation.

This component discovers eye-catching, controversial questions based on given keywords
within a specific field of topic that will attract maximum audience attention.
"""

import asyncio
from typing import Optional

from pydantic import Field

from src import log
from src.core import DataCore
from src.lib.model.txt.lm_basis import LmBasis
from src.lib.model.txt.lm_gentxt_params import LmGentxtParams
from src.lib.model.txt.lm_gentxt_result import LmGentxtResult

from .prompts import (
    INTEREST_DISCOVERY_PROMPT_TEMPLATE,
    INTEREST_DISCOVERY_SYSTEM_PROMPT,
)


class InterestDiscoveryParams(DataCore):
    """Parameters for interest discovery."""

    field_of_topic: str = Field(
        description="The specific field or domain for interest discovery"
    )

    keywords: str = Field(
        description="Keywords or sentence related to the field of topic"
    )

    max_tokens: Optional[int] = Field(
        default=4000, description="Maximum tokens for the LLM response"
    )

    temperature: float = Field(
        default=0.7,
        description="Temperature for LLM generation (higher for more creative questions)",
    )


class InterestDiscoveryResult(DataCore):
    """Result from interest discovery."""

    field_of_topic: str = Field(description="The original field of topic")

    keywords: str = Field(description="The original keywords used")

    interest_analysis: str = Field(
        description="Comprehensive analysis of eye-catching questions and engagement strategies"
    )

    input_tokens: int = Field(description="Number of input tokens used by the LLM")

    output_tokens: int = Field(
        description="Number of output tokens generated by the LLM"
    )


class InterestDiscovery:
    """
    Interest Discovery Component.

    Discovers eye-catching, controversial questions based on keywords within a specific
    field of topic that will attract maximum audience attention.
    """

    def __init__(self, model: LmBasis, log_name: str = "interest_discovery"):
        """
        Initialize the interest discovery component.

        Args:
            model: Language model to use for interest discovery
            log_name: Name for logging purposes
        """
        self.model = model
        self.logger = log.bind(component=log_name)

    def discover(self, params: InterestDiscoveryParams) -> InterestDiscoveryResult:
        """
        Conduct synchronous interest discovery for keywords in a field.

        Args:
            params: Parameters for interest discovery

        Returns:
            InterestDiscoveryResult containing eye-catching questions and analysis
        """
        self.logger.info(
            f"Starting interest discovery for field: {params.field_of_topic}, keywords: {params.keywords}"
        )

        # Prepare the prompt
        prompt = INTEREST_DISCOVERY_PROMPT_TEMPLATE.format(
            field_of_topic=params.field_of_topic, keywords=params.keywords
        )

        # Create LLM parameters
        llm_params = LmGentxtParams(
            system_prompt=INTEREST_DISCOVERY_SYSTEM_PROMPT,
            prompt=prompt,
            max_new_tokens=params.max_tokens,
            temperature=params.temperature,
        )

        # Call the LLM
        llm_result: LmGentxtResult = self.model.gentxt(llm_params)

        # Create and return result
        result = InterestDiscoveryResult(
            field_of_topic=params.field_of_topic,
            keywords=params.keywords,
            interest_analysis=llm_result.output,
            input_tokens=llm_result.input_tokens,
            output_tokens=llm_result.output_tokens,
        )

        self.logger.success(
            f"Interest discovery completed for: {params.field_of_topic}"
        )
        self.logger.info(f"Generated {result.output_tokens} tokens of analysis")

        return result

    async def adiscover(
        self, params: InterestDiscoveryParams
    ) -> InterestDiscoveryResult:
        """
        Conduct asynchronous interest discovery for keywords in a field.

        Args:
            params: Parameters for interest discovery

        Returns:
            InterestDiscoveryResult containing eye-catching questions and analysis
        """
        self.logger.info(
            f"Starting async interest discovery for field: {params.field_of_topic}, keywords: {params.keywords}"
        )

        # Prepare the prompt
        prompt = INTEREST_DISCOVERY_PROMPT_TEMPLATE.format(
            field_of_topic=params.field_of_topic, keywords=params.keywords
        )

        # Create LLM parameters
        llm_params = LmGentxtParams(
            system_prompt=INTEREST_DISCOVERY_SYSTEM_PROMPT,
            prompt=prompt,
            max_new_tokens=params.max_tokens,
            temperature=params.temperature,
        )

        # Call the LLM asynchronously
        llm_result: LmGentxtResult = await self.model.agentxt(llm_params)

        # Create and return result
        result = InterestDiscoveryResult(
            field_of_topic=params.field_of_topic,
            keywords=params.keywords,
            interest_analysis=llm_result.output,
            input_tokens=llm_result.input_tokens,
            output_tokens=llm_result.output_tokens,
        )

        self.logger.success(
            f"Async interest discovery completed for: {params.field_of_topic}"
        )
        self.logger.info(f"Generated {result.output_tokens} tokens of analysis")

        return result
