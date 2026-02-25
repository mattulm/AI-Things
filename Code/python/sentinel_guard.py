import psutil
import time
import os
import logging
from collections import deque

class SentinelGuard:
    """
    The Ultimate Safety Wrapper for Agentic AI.
    Monitors: Hardware (Thermal), Resource (CPU/MEM), 
    Network (Throughput), and Temporal (Action Rate).
    """
    def __init__(self, config):
        self.max_cpu = config.get('cpu_limit', 80.0)
        self.max_mem = config.get('mem_limit_mb', 1024)
        self.max_net = config.get('net_limit_mbps', 100.0)
        self.max_temp = config.get('temp_limit_c', 75)
        
        # Temporal Throttle: Max 3 global actions per 5 minutes
        self.action_window = deque()
        self.max_actions = config.get('max_actions', 3)
        self.window_size = config.get('window_seconds', 300)

        logging.basicConfig(level=logging.INFO, format='[SENTINEL] %(message)s')

    def check_temporal_throttle(self, action_name):
        """Prevents rapid-fire cascading changes (The Butterfly Filter)."""
        now = time.time()
        while self.action_window and self.action_window[0] < now - self.window_size:
            self.action_window.popleft()

        if len(self.action_window) >= self.max_actions:
            logging.critical(f"TEMPORAL BLOCK: Rate limit exceeded for {action_name}")
            return False
        
        self.action_window.append(now)
        return True

    def check_system_vitals(self, pid):
        """Multi-layer health check: Hardware, Resource, Network."""
        try:
            p = psutil.Process(pid)
            
            # 1. Resource Check
            if p.cpu_percent(interval=0.1) > self.max_cpu or \
               (p.memory_info().rss / 1e6) > self.max_mem:
                return False, "Resource Exhaustion"

            # 2. Hardware Thermal Check
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures().get('coretemp', [])
                if any(t.current > self.max_temp for t in temps):
                    return False, "Hardware Thermal Critical"

            # 3. Network Saturation (Butterfly Prevention)
            net_mbps = (psutil.net_io_counters().bytes_sent / 1e6)
            if net_mbps > self.max_net:
                return False, "Network Saturation"

            return True, "All Systems Nominal"
        except psutil.NoSuchProcess:
            return False, "Agent Process Lost"

    def run_sidecar(self, agent_pid):
        logging.info(f"Sentinel Guard active for PID: {agent_pid}")
        while True:
            safe, reason = self.check_system_vitals(agent_pid)
            if not safe:
                logging.critical(f"EMERGENCY SHUTDOWN: {reason}")
                os.kill(agent_pid, 9) # Hard Kill
                break
            time.sleep(1)

# Usage Logic
if __name__ == "__main__":
    # Example Config
    cfg = {'cpu_limit': 50, 'mem_limit_mb': 500, 'max_actions': 2}
    sentinel = SentinelGuard(cfg)
    # sentinel.run_sidecar(target_pid)
