# pylint: disable=no-self-argument
import logging
import logging.config
from typing import Any, Literal, Type

import ant31box.config
from ant31box.config import BaseConfig, FastAPIConfigSchema, GConfig
from pydantic import Field
from pydantic_settings import SettingsConfigDict

LOGGING_CONFIG: dict[str, Any] = ant31box.config.LOGGING_CONFIG
LOGGING_CONFIG["loggers"].update(
    {"opticr": {"handlers": ["default"], "level": "INFO", "propagate": True}}
)

logger: logging.Logger = logging.getLogger("opticr")


class LoggingConfigSchema(BaseConfig):
    use_colors: bool = Field(default=True)
    log_config: dict[str, Any] | str | None = Field(
        default_factory=lambda: LOGGING_CONFIG
    )
    level: str = Field(default="info")


ENVPREFIX = "OPTICR"


class FastAPIConfigCustomSchema(FastAPIConfigSchema):
    server: str = Field(default="opticr.server.server:serve")


class TesseractConfigSchema(BaseConfig):
    pass


class GoogleVisionConfigSchema(BaseConfig):
    service_account_json: str = Field(default="service-account.json")


class OCREngineConfigSchema(BaseConfig):
    default: Literal["tesseract", "google-vision"] = Field(default="tesseract")
    google_vision: GoogleVisionConfigSchema = Field(
        default_factory=GoogleVisionConfigSchema
    )
    tesseract: TesseractConfigSchema = Field(default_factory=TesseractConfigSchema)


# Main configuration schema
class ConfigSchema(ant31box.config.ConfigSchema):
    model_config = SettingsConfigDict(
        env_prefix=f"{ENVPREFIX}_",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="allow",
    )
    name: str = Field(default="opticr")
    server: FastAPIConfigCustomSchema = Field(default_factory=FastAPIConfigCustomSchema)
    ocr: OCREngineConfigSchema = Field(default_factory=OCREngineConfigSchema)


class Config(ant31box.config.Config[ConfigSchema]):
    _env_prefix: str = ENVPREFIX
    __config_class__: Type[ConfigSchema] = ConfigSchema

    @property
    def ocr(self) -> OCREngineConfigSchema:
        return self.conf.ocr


def config(path: str | None = None, reload: bool = False) -> Config:
    GConfig[Config].set_conf_class(Config)
    if reload:
        GConfig[Config].reinit()
    # load the configuration
    GConfig[Config](path)
    # Return the instance of the configuration
    return GConfig[Config].instance()
