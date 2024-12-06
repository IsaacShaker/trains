from Green_line_SW_PLC_0 import main
import unittest
from threading import Event

class TestPLCMachine(unittest.TestCase):
    def setUp(self):
        # Initialize input and output lists
        self.block_occupancies = [False] * 151
        self.switch_suggestions = [False] * 6 
        self.switches = [False] * 6
        self.traffic_lights = [False] * 10
        self.crossings = [False] * 2
        self.speed_hazard = [False] * 151

        # Create a stop_event for testing
        self.stop_event = Event()

    def test_default_behavior(self):
        """Test that the default state is maintained when no blocks are occupied."""
        self.stop_event.set()  # Immediately stop after one loop iteration
        main(
            self.stop_event,
            self.block_occupancies,
            self.switch_suggestions,
            self.switches,
            self.traffic_lights,
            self.crossings,
            self.speed_hazard,
        )
        # Default state checks
        self.assertFalse(any(self.speed_hazard))
        self.assertEqual(self.switches[4], False)
        self.assertEqual(self.switches[5], True)
        self.assertTrue(self.traffic_lights[6])
        self.assertFalse(self.crossings[1])  # Crossing should remain up

    def test_block_occupancy_effects(self):
        """Test that occupying specific blocks updates the speed hazards correctly."""
        self.block_occupancies[50] = True  # Simulate a train occupying block 50
        self.stop_event.set()  # Stop after one loop
        main(
            self.stop_event,
            self.block_occupancies,
            self.switch_suggestions,
            self.switches,
            self.traffic_lights,
            self.crossings,
            self.speed_hazard,
        )
        # Check speed hazard for trailing 4 blocks
        for i in range(46, 50):  # Blocks trailing 50
            self.assertTrue(self.speed_hazard[i])

    def test_crossing_down_when_occupied(self):
        """Test that the crossing goes down when blocks around it are occupied."""
        self.block_occupancies[108] = True  # Block 108 is the crossing block
        self.stop_event.set()  # Stop after one loop
        main(
            self.stop_event,
            self.block_occupancies,
            self.switch_suggestions,
            self.switches,
            self.traffic_lights,
            self.crossings,
            self.speed_hazard,
        )
        self.assertTrue(self.crossings[1])  # Crossing should be down

    def test_switch_and_light_logic(self):
        """Test switch and traffic light logic when section N is occupied."""
        self.block_occupancies[77] = True  # Section N occupied
        self.stop_event.set()  # Stop after one loop
        main(
            self.stop_event,
            self.block_occupancies,
            self.switch_suggestions,
            self.switches,
            self.traffic_lights,
            self.crossings,
            self.speed_hazard,
        )
        self.assertTrue(self.switches[4])
        self.assertFalse(self.switches[5])
        self.assertFalse(self.traffic_lights[6])
        self.assertTrue(self.traffic_lights[7])

    def test_hazards_prioritize_q_over_m(self):
        """Test that Q is prioritized over M when both are occupied."""
        self.block_occupancies[98] = True  # Q occupied
        self.block_occupancies[74] = True  # M occupied
        self.stop_event.set()  # Stop after one loop
        main(
            self.stop_event,
            self.block_occupancies,
            self.switch_suggestions,
            self.switches,
            self.traffic_lights,
            self.crossings,
            self.speed_hazard,
        )
        # M should be clear, Q should have hazards
        for i in range(74, 77):
            self.assertFalse(self.speed_hazard[i])
        for i in range(98, 101):
            self.assertTrue(self.speed_hazard[i])

    def tearDown(self):
        self.stop_event.clear()  # Ensure the stop_event is cleared for the next test

if __name__ == "__main__":
    unittest.main()
