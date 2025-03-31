import bisect
import threading
import time 
from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from sortedcontainers import SortedList

from models import LogResponse

class LogStorage:

    """Thread-safe storage for log entries with time-based expiration"""
    def __init__(self, retention_period: timedelta = timedelta(hours=1)):
        self.wlock = threading.Lock()
        self.rlock = threading.RLock() 
        self.logs = defaultdict(list)
        self.last_cleanup = datetime.utcnow()
        self.retention_period = retention_period
        self.start_cleanup_thread()
    

    """Add a log entry to storage, maintaining chronological order"""
    def add_log(self, service_name: str, timestamp: datetime, message: str) -> None:
        with self.wlock:
            if service_name not in self.logs:
                self.logs[service_name] = SortedList()
            self.logs[service_name].add((timestamp, message))
    

    """Retrieve logs for a service within a time range"""
    def get_logs(self, service_name: str, start_time: datetime, end_time: datetime) -> List[LogResponse]:
        with self.rlock:
            if service_name not in self.logs:
                return []
            start_index = self.logs[service_name].bisect_left((start_time, ""))
            end_index = self.logs[service_name].bisect_right((end_time, ""))
            result = [
                {"timestamp": log[0], "message": log[1]}
                for log in self.logs[service_name][start_index:end_index]
            ]
            return result 
    

    """Clean up old logs if enough time has passed since last cleanup"""
    def cleanup_old_logs(self):
        while True:
            time.sleep(60)
            with self.wlock:
                print(f"cleanup_old_logs")
                for service in list(self.logs.keys()):
                    while self.logs[service] and (time.now() - self.logs[service][0][0]).total_seconds() > self.retention_period:
                        self.logs[service].pop(0)
                    if not self.logs[service]:
                        del self.logs[service]


    """Starting a thread to clean up old logs"""
    def start_cleanup_thread(self):
        cleanup_thread = threading.Thread(target=self.cleanup_old_logs, daemon=True)
        cleanup_thread.start()
