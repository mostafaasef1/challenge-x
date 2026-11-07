#!/usr/bin/env python3
import time
import struct
import json
import serial
import cv2

# --- Configuration Constants ---
LORA_PORT = "/dev/ttyUSB0"  # Serial interface for the 915 MHz transceiver module
BAUD_RATE = 9600
VIDEO_SOURCE = 0
TARGET_WIDTH = 320         # Optimized low resolution for high-attenuation waveguide pipes
TARGET_HEIGHT = 240
JPEG_QUALITY = 30           # Heavy compression to minimize byte packet length over LoRa

class CrawlerPilot:
    def __init__(self):
        # Initialize hardware connections
        try:
            self.lora_serial = serial.Serial(LORA_PORT, BAUD_RATE, timeout=0.1)
        except Exception as e:
            print(f"[WARN] LoRa module serial port not found: {e}. Simulating stream...")
            self.lora_serial = None

        self.cap = cv2.VideoCapture(VIDEO_SOURCE)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, TARGET_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, TARGET_HEIGHT)
        
        # Telemetry State Tracking
        self.segment_id = 0x01
        self.battery_v = 14.8
        self.pitch = 0.0
        self.roll = 0.0

    def read_operator_commands(self):
        """Checks the LoRa serial buffer for manual remote control commands."""
        if not self.lora_serial or not self.lora_serial.in_waiting:
            return None
        
        raw_data = self.lora_serial.readline()
        try:
            command = json.loads(raw_data.decode('utf-8').strip())
            print(f"[CMD] Incoming Operator Instruction: {command}")
            return command
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

    def pack_and_transmit(self):
        """Captures video, compresses to JPEG, appends telemetry headers, and transmits."""
        ret, frame = self.cap.read()
        if not ret:
            print("[ERROR] Camera frame capture failed.")
            return

        # Compress frame heavily to fit within the waveguide propagation bandwidth limits
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
        result, encimg = cv2.imencode('.jpg', frame, encode_param)
        if not result:
            return
            
        byte_data = encimg.tobytes()
        payload_size = len(byte_data)

        # Telemetry structural frame header: [SegmentID (1B)][PayloadSize (4B)][Pitch (4f)][Roll (4f)][Battery (4f)]
        header = struct.pack("!B I f f f", self.segment_id, payload_size, self.pitch, self.roll, self.battery_v)
        full_packet = header + byte_data

        if self.lora_serial:
            # Broadcast multi-hop packet frame
            self.lora_serial.write(full_packet)
            # Add small delay to prevent buffer saturation on intermediate relay pods
            time.sleep(0.05) 
        else:
            print(f"[SIM] Broadcast packet size: {len(full_packet)} bytes (Header: {len(header)}, Image: {payload_size})")

    def run_loop(self):
        print("[INFO] TurTech Multi-Segment Crawler Pilot Loop Active. Press Ctrl+C to terminate.")
        try:
            while True:
                # 1. Look for human-operated steering commands
                cmd = self.read_operator_commands()
                if cmd:
                    pass
                
                # 2. Transmit compressed video diagnostics and pipe health data
                self.pack_and_transmit()
                time.sleep(0.1)  # Target ~10 FPS transmission loop
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down crawler sub-systems safely.")
        finally:
            self.cap.release()

if __name__ == "__main__":
    pilot = CrawlerPilot()
    pilot.run_loop()
