from dataclasses import dataclass


@dataclass(frozen=True)
class CommandConfigurationDto:
    name: str
    text: str
    description: str