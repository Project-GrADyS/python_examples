import logging
import os
import random
from pathlib import Path
from gradysim.protocol.plugin.mission_mobility import (
    LoopMission,
    MissionMobilityPlugin,
    MissionMobilityConfiguration,
)
from gradysim.protocol.plugin.statistics import create_statistics, finish_statistics
from gradysim.protocol.messages.communication import BroadcastMessageCommand, SendMessageCommand
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.protocol.interface import IProtocol
from message import ZigZagMessage, ZigZagMessageType
from utils import CommunicationStatus


class ZigZagProtocolGround(IProtocol):
    def __init__(self):
        self.timeout_end: int = 0
        self.timeout_set: bool = False
        self.timeout_duration: int = 5

        self.communication_status: CommunicationStatus = CommunicationStatus.FREE

        self.tentative_target: int = -1

        self.current_data_load: int = 0
        self.stable_data_load: int = self.current_data_load

        # self.current_telemetry: Telemetry
        # self.last_stable_telemetry: Telemetry
       
        self._logger = logging.getLogger()
        self.old_mission_is_reversed: bool = False

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
        create_statistics(self, file_name_part="")

        self._logger.debug("initializing mobile protocol")

        # self.provider.tracked_variables["timeout_set"] = self.timeout_set
        # self.provider.tracked_variables["timeout_end"] = self.timeout_end
        self.provider.tracked_variables["current_data_load"] = self.current_data_load
        # self.provider.tracked_variables["stable_data_load"] = self.current_data_load
        # self.provider.tracked_variables["communication_status"] = self.communication_status.name

        self.provider.schedule_timer("", self.provider.current_time() + random.random())

    def handle_timer(self, timer: str):
        self._send_heartbeat()        
        self.provider.schedule_timer("", self.provider.current_time() + random.random())

    def handle_packet(self, message: str):
        self._logger.debug("Handling packet in mobile protocol")
        message: ZigZagMessage = ZigZagMessage.from_json(message)

        match message.message_type:
            case ZigZagMessageType.HEARTBEAT:
                if not self._is_timedout():
                    self.tentative_target = message.source_id
                    self._send_message()

            case ZigZagMessageType.PAIR_REQUEST:
                if self._is_timedout() or message.destination_id != self.provider.get_id():
                    return
                else: 
                    if self.communication_status != CommunicationStatus.PAIRED:
                        self.tentative_target = message.source_id
                        self.communication_status = CommunicationStatus.PAIRED
                        self._send_message()

            case ZigZagMessageType.PAIR_CONFIRM:
                if self._is_timedout() or message.destination_id != self.provider.get_id():
                    return 
                else:
                    if message.source_id == self.tentative_target:
                        if self.communication_status != CommunicationStatus.PAIRED_FINISHED:
                            self._initiate_timeout()

                            self.stable_data_load += message.data_length
                            self.current_data_load += message.data_length
                            self.provider.tracked_variables["current_data_load"] = self.current_data_load

                            self.communication_status = CommunicationStatus.PAIRED_FINISHED
                            self._send_message()

    def _send_message(self):
        message = ZigZagMessage(
            source_id=self.provider.get_id(),
            reversed_flag=self.old_mission_is_reversed,
        )

        if self.provider.get_id() == self.tentative_target:
            return
        
        match self.communication_status:
            case CommunicationStatus.FREE:
                message.message_type = ZigZagMessageType.PAIR_REQUEST
                message.destination_id = self.tentative_target

            case CommunicationStatus.PAIRED:
                message.message_type = ZigZagMessageType.PAIR_CONFIRM
                message.destination_id = self.tentative_target
                message.data_length = self.stable_data_load

            case CommunicationStatus.PAIRED_FINISHED:
                message.message_type = ZigZagMessageType.PAIR_FINISH
                message.destination_id = self.tentative_target
                message.data_length = self.stable_data_load

        self.provider.tracked_variables["communication_status"] = self.communication_status.name

        if self.tentative_target < 0:
            command = BroadcastMessageCommand(
                message=message.to_json()
            )

        else:
            command = SendMessageCommand(
                message=message.to_json(), destination=self.tentative_target
            )

        self.provider.send_communication_command(command)

    def handle_telemetry(self, telemetry: Telemetry):
        pass
    #     self.current_telemetry = telemetry

    #     if self._is_timedout():
    #         self.last_stable_telemetry = telemetry

    def finish(self):
        finish_statistics(self, f'{self.folder_prefix}{self.current_run_id}')


    def _send_heartbeat(self):
        message = ZigZagMessage(
            source_id=self.provider.get_id(),
            reversed_flag=False,
            message_type=ZigZagMessageType.HEARTBEAT
        )

        self.provider.tracked_variables["communication_status"] = self.communication_status.name

        command = BroadcastMessageCommand(
            message=message.to_json()
        )
        self.provider.send_communication_command(command)

    def _initiate_timeout(self):
        if self.timeout_duration > 0:
            self.timeout_end = self.provider.current_time() + self.timeout_duration
            self.timeout_set = True

    def _is_timedout(self):
        def __is_timedout():
            if self.timeout_set:
                if self.provider.current_time() < self.timeout_end:
                    return True
                else:
                    self.timeout_set = False
                    return False
            else:
                return False
    
        self.provider.tracked_variables["timeout_set"] = self.timeout_set
        self.provider.tracked_variables["timeout_end"] = self.timeout_end

        old_timeout_set = self.timeout_set
        is_timedout = __is_timedout()
        if not is_timedout and old_timeout_set:
            self._reset_parameters()
        return is_timedout

           
    def _reset_parameters(self):
        self.timeout_set = False
        self.tentative_target = -1
        self.communication_status = CommunicationStatus.FREE
        # self.last_stable_telemetry = self.current_telemetry
        self.stable_data_load = self.current_data_load
        self.provider.tracked_variables["stable_data_load"] = self.stable_data_load
