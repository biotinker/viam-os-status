from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, cast
from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.sensor import Sensor
from viam.components.generic import Generic
from viam.logging import getLogger
from viam.utils import struct_to_dict, dict_to_struct, ValueTypes

import time
import asyncio
import subprocess

LOGGER = getLogger(__name__)

default_cmds = [
    ["uptime"],
    ["iwconfig"],
    ["df", "-h"]
]

class OSSTATS(Generic, Sensor, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("biotinker", "sensor"), "osstats")
    
    ext_cmds_allowed = False
    user_cmds = []

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
        self.user_cmds = []
        conf = struct_to_dict(config.attributes)
        
        if "ext_cmds_allowed" in conf.keys():
            if conf["ext_cmds_allowed"] == "true":
                self.ext_cmds_allowed = True
        if "commands" in conf.keys():
            for command_set in conf["commands"]:
                self.user_cmds.append(command_set)
        
        return

    """ Implement the methods the Viam RDK defines for the sensor API (rdk:component:sensor) """
    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        all_results = {}
        for cmd_list in default_cmds + self.user_cmds:
            try:
                result = subprocess.run(cmd_list, capture_output=True)
                cmd_result = {
                        "stdout": result.stdout.decode("utf-8") ,
                        "stderr": result.stderr.decode("utf-8")
                }
                all_results[" ".join(cmd_list)] = cmd_result
            except Exception as e:
                all_results[" ".join(cmd_list)] = {"error": str(e)}
        return all_results

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        all_results = {}
        if self.ext_cmds_allowed:
            for (name, args) in command.items():
                if name == 'run':
                    try:
                        result = subprocess.run(args, capture_output=True)
                        cmd_result = {
                            "stdout": result.stdout.decode("utf-8") ,
                            "stderr": result.stderr.decode("utf-8")
                        }
                        all_results[" ".join(args)] = cmd_result
                    except Exception as e:
                        all_results[" ".join(cmd_list)] = {"error": str(e)}
        else:
            all_results = {"error": "user commands not allowed unless 'ext_cmds_allowed' set to 'true' in module config"}
        return all_results
