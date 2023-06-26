from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, cast
from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.sensor import Sensor
from viam.logging import getLogger

import time
import asyncio
import subprocess

LOGGER = getLogger(__name__)

class OSSTATS(Sensor, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("biotinker", "sensor"), "osstats")
    
    

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sensor = cls(config.name)
        sensor.reconfigure(config, dependencies)
        return sensor

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        return

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):

        return

    """ Implement the methods the Viam RDK defines for the sensor API (rdk:component:sensor) """

    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        return
