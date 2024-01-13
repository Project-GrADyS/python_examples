from gradysim.simulator.handler.communication import CommunicationHandler, CommunicationMedium
from gradysim.simulator.handler.mobility import MobilityHandler
from gradysim.simulator.handler.timer import TimerHandler
from gradysim.simulator.simulation import SimulationBuilder, SimulationConfiguration

from protocol_mobile import ZigZagProtocolMobile
from protocol_sensor import ZigZagProtocolSensor
from protocol_ground import ZigZagProtocolGround


def run_simulation():
    builder = SimulationBuilder(SimulationConfiguration(duration=60000, real_time=False))
    builder.add_handler(CommunicationHandler(CommunicationMedium(transmission_range=50)))
    builder.add_handler(TimerHandler())
    builder.add_handler(MobilityHandler())

    # Drone locations 
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolMobile, (-600.0, -600.0, 0.0))

    # Ground location
    builder.add_node(ZigZagProtocolGround, (-600.0, -600.0, 0.0))

    # Sensor locations 
    builder.add_node(ZigZagProtocolSensor, (-600.0, -300.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (-600.0, 0.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (-600.0, 300.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (-600.0, 600.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (-300.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (-300.0, -300.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (-300.0, 0.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (-300.0, 300.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (-300.0, 600.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (0.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (0.0, -300.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (0.0, 0.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (0.0, 300.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (0.0, 600.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (300.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (300.0, -300.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (300.0, 0.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (300.0, 300.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (300.0, 600.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (600.0, -600.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (600.0, -300.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (600.0, 0.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (600.0, 300.0, 0.0))
    builder.add_node(ZigZagProtocolSensor, (600.0, 600.0, 0.0))

    # Simulation
    simulation = builder.build()
    simulation.start_simulation()


if __name__ == '__main__':
    run_simulation()
