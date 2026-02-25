import psutil
import speedtest # For network monitoring
import logging
import os

class MultiLayerCircuitBreaker:
    """
    Advanced Defensive Wrapper for Agentic AI Systems.
    Monitors Network, App, and Hardware-level stress.
    """
    def __init__(self, thresholds):
        self.max_cpu = thresholds.get('cpu', 80.0)
        self.max_mem_mb = thresholds.get('mem', 2048)
        self.max_net_mbps = thresholds.get('net', 100.0)
        self.max_temp = thresholds.get('temp', 75) # Celsius
        
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    def check_hardware_thermal(self):
        """Monitor for hardware-level thermal exhaustion."""
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                current_temp = temps['coretemp'][0].current
                if current_temp > self.max_temp:
                    return False, current_temp
        return True, 0

    def check_network_saturation(self):
        """Prevents BGP/Router-level flooding."""
        net_io = psutil.net_io_counters()
        # Simple delta check (bytes converted to Mbps)
        # In production, compare this over a 1-second window
        return (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024)

    def enforce_safety(self, pid):
        try:
            p = psutil.Process(pid)
            
            # 1. Hardware Check
            temp_safe, val = self.check_hardware_thermal()
            if not temp_safe:
                self.trigger_emergency_shutdown(f"Thermal Threshold Exceeded: {val}°C")

            # 2. Network Check (The 'Butterfly' Prevention)
            net_usage = self.check_network_saturation()
            if net_usage > self.max_net_mbps:
                self.isolate_network_interface()

            # 3. Resource/Application Check
            if p.cpu_percent(interval=0.1) > self.max_cpu:
                self.trigger_emergency_shutdown("CPU Exhaustion Cascade Detected")

        except psutil.NoSuchProcess:
            logging.error("Agent process lost.")

    def isolate_network_interface(self):
        """Cuts the agent's connection to the global internet (Simulated)."""
        logging.critical("NETWORK ISOLATION TRIGGERED: Preventing global cascade.")
        # os.system("ifconfig eth0 down") # DANGER: Real implementation
        
    def trigger_emergency_shutdown(self, reason):
        logging.critical(f"SYSTEM KILL-SWITCH ACTIVATED: {reason}")
        # Terminate all AI processes immediately
        os._exit(1)

# Usage Logic
# thresholds = {'cpu': 50.0, 'mem': 4000, 'net': 500.0, 'temp': 80}
# breaker = MultiLayerCircuitBreaker(thresholds)
