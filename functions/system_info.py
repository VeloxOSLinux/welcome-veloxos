import psutil
import platform
import GPUtil

def get_sys_info():
    try:
        # CPU
        cpu_name = platform.processor()
        if not cpu_name or platform.system() == "Linux":
            try:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            cpu_name = line.split(":")[1].strip().split("@")[0]
                            break
            except:
                cpu_name = platform.machine()

        # GPU Erkennung
        gpu_name = "Internal Graphics"
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu_name = gpus[0].name
        except:
            # Fallback falls GPUtil fehlschlägt (z.B. keine NVIDIA Karte)
            gpu_name = "Generic GPU"

        info = {
            "os": "VeloxOS" if platform.system() == "Linux" else "Windows Dev",
            "cpu": cpu_name[:22] + ".." if len(cpu_name) > 22 else cpu_name,
            "gpu": gpu_name[:22] + ".." if len(gpu_name) > 22 else gpu_name,
            "ram": f"{round(psutil.virtual_memory().total / (1024**3), 1)} GB",
            "kernel": platform.release()
        }
        return info
    except:
        return {"os": "Unknown", "cpu": "Unknown", "gpu": "Unknown", "ram": "Unknown", "kernel": "Unknown"}