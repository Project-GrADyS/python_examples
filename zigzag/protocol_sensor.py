import logging
import os
from gradysim.protocol.plugin.statistics import create_statistics, finish_statistics
from gradysim.protocol.messages.communication import (
    SendMessageCommand,
)
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.protocol.interface import IProtocol
from message import ZigZagMessage, ZigZagMessageType, ZigZagNodeType
from utils import CommunicationStatus


class ZigZagProtocolSensor(IProtocol):
    def __init__(self):
        self.communication_status: CommunicationStatus = CommunicationStatus.FREE
        self.tentative_target: int = -1

        self._logger = logging.getLogger()

        self.folder_prefix = "/home/lac/Documents/Gradys/examples/results/cpp/15/"
        folder_count = 10

        def is_folder_empty(folder_path):
            return len(os.listdir(folder_path)) == 0

        for i in range(1, folder_count + 1):
            folder_path = f"{self.folder_prefix}{i}"

            if is_folder_empty(folder_path):
                self.current_run_id = i
                break



    def initialize(self):
        self._logger.debug("Initializing sensor/ground protocol")

        create_statistics(self, file_name_part="")

        self.provider.tracked_variables["communication_status"] = self.communication_status.name

    def handle_timer(self, timer: str):
        pass
    
    def handle_packet(self, message: str):
        message: ZigZagMessage = ZigZagMessage.from_json(message)

        if message.message_type == ZigZagMessageType.HEARTBEAT:
            self._logger.debug("Exchanging data in sensor/ground protocol")
            self.tentative_target = message.source_id

            message = ZigZagMessage(
                message_type=ZigZagMessageType.BEARER,
                source_id=self.provider.get_id(),
                destination_id=self.tentative_target,
                source_node_type=ZigZagNodeType.SENSOR
            )
            
            self.provider.send_communication_command(
                SendMessageCommand(
                    message=message.to_json(),
                    destination=self.tentative_target,
                )
            )

            self.provider.tracked_variables["communication_status"] = self.communication_status.name

    def handle_telemetry(self, telemetry: Telemetry):
        pass

    def finish(self):
        finish_statistics(self, f'{self.folder_prefix}{self.current_run_id}')