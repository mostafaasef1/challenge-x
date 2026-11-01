# Challenge X

Challenge+X is a hybrid, hackathon-style, eight-week innovation program that connects students with organizations to solve real-world problems across healthcare, finance, technology, engineering, and beyond.

# Autonomous FMCW GPR Wildlife Detection & Relocation Rover

An all-terrain autonomous sub-surface scanning rover developed for the Challenge X competition. The system is designed to locate buried wildlife—specifically native Virginia Eastern Woodland Box Turtles—on active construction sites without disrupting construction workflows. 

## Key Features
*   **FMCW Radar Architecture:** Custom RF sweep string (300 MHz to 1 GHz) using a JTOS-850VW+ Voltage Controlled Oscillator to spot shallow 5-inch targets.
*   **3D-Printed Vivaldi Antennas:** Antipodal Vivaldi antenna system lined with copper foil, engineered to skim 1-2 inches above the soil line.
*   **Fail-Safe Detection Engine:** Python-based processing unit (NumPy/SciPy) running continuous Fast Fourier Transforms (FFT) optimized to prioritize false positives over false negatives.
*   **Automated Telemetry:** Integrated SIM7600G-H 4G LTE HAT using the Twilio API to instantly relay GPS coordinates to site managers when a target is detected.
*   **Rugged Hardware:** 4WD aluminum chassis with 8-inch all-terrain puncture-resistant tires and an IP65 waterproof control enclosure.

# Untethered Wireless Video Communication for Long-Distance Pipe Inspection

A multi-segment, articulated robotic crawler developed for Garney during Challenge X to inspect deep underground municipal sewer systems. This project implements a novel tetherless communication strategy to map structural cracks, faults, and discolorations inside highly attenuating pipelines.

## Key Features
*   **Train-Bogie Articulation:** A 24-inch, 3-segment modular chassis connected by passive 2-axis spring universal joints to easily flex through tight pipe bends.
*   **Dropped Relay Mechanism:** A unique mechanical system that drops low-profile magnetic micro-RF relay pods at calculated physical intervals to maintain a multi-hop wireless link up to 2 miles.
*   **Waveguide Propagation Optimization:** Transceiver array tuned to 915 MHz LoRa to cleanly propagate above the calculated circular waveguide cut-off frequency of municipal sewer mains.
*   **Dual Processing Unit:** Raspberry Pi Zero 2 W handles lightweight H.264 video compression and OpenCV data pipelines, while an Arduino Nano handles direct PWM high-torque motor drive control.
*   **Intrinsically Safe Enclosure:** Sealed IP68 watertight acrylic/aluminum structural casings designed to operate safely near volatile sewer gases.
