import psutil
import platform
from datetime import datetime

def get_system_summary():
    return {
        "timestamp": datetime.now().isoformat(),
        "platform": platform.platform(),
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "memory": {
            "total_gb": round(psutil.virtual_memory().total / 1e9, 2),
            "available_gb": round(psutil.virtual_memory().available / 1e9, 2),
            "used_percent": psutil.virtual_memory().percent,
        },
        "disk": {
            "total_gb": round(psutil.disk_usage('/').total / 1e9, 2),
            "used_gb": round(psutil.disk_usage('/').used / 1e9, 2),
            "free_gb": round(psutil.disk_usage('/').free / 1e9, 2),
            "used_percent": psutil.disk_usage('/').percent,
        },
        "network": {
            "bytes_sent_mb": round(psutil.net_io_counters().bytes_sent / 1e6, 2),
            "bytes_recv_mb": round(psutil.net_io_counters().bytes_recv / 1e6, 2),
        },
        "uptime_seconds": int((datetime.now() - datetime.fromtimestamp(psutil.boot_time())).total_seconds()),
    }