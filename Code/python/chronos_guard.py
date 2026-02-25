import time
import collections
import logging

class ChronosGuard:
    """
    Temporal Throttle for Agentic AI. 
    Prevents 'Flash Crashes' by limiting the rate of global state changes.
    """
    def __init__(self, max_actions=5, window_seconds=60):
        # Sliding window to track action timestamps
        self.action_history = collections.deque()
        self.max_actions = max_actions
        self.window_seconds = window_seconds
        
    def request_action(self, action_type="Global_Config_Change"):
        """
        Validates if the agent is allowed to perform an impactful action.
        """
        current_time = time.time()
        
        # Clean up timestamps outside the current window
        while self.action_history and self.action_history[0] < current_time - self.window_seconds:
            self.action_history.popleft()
            
        if len(self.action_history) >= self.max_actions:
            return self.deny_action(action_type)
            
        self.action_history.append(current_time)
        logging.info(f"Action Permitted: {action_type}. ({len(self.action_history)}/{self.max_actions} in window)")
        return True

    def deny_action(self, action_type):
        logging.warning(f"TEMPORAL BLOCK: Agent attempting too many changes: {action_type}")
        logging.warning("Cool-down period enforced to prevent cascading failure.")
        # Logic to force the agent into a 'sleep' state or wait
        return False

# Integrated Usage Example:
# guard = ChronosGuard(max_actions=3, window_seconds=300) # Only 3 big moves every 5 mins
# if guard.request_action("BGP_ROUTE_UPDATE"):
#    execute_agent_logic()
# else:
#    trigger_human_review()
