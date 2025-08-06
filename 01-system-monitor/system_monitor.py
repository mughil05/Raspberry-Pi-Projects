#!/usr/bin/env python3
import psutil
import time
from datetime import datetime

def get_pi_stats():
    """Get Pi System Stats"""
    # CPU TEMP
    try: 
        temps = psutil.sensors_temperatures()
        if 'cpu_thermal' in temps and len(temps['cpu_thermal']) > 0:
            cpu_temp = temps['cpu_thermal'][0].current
        else:
            cpu_temp = "No CPU sensor"
    except Exception as e:
        cpu_temp = f"Error: {e}"
        

    #CPU Usage over 1 second
    cpu_percent = psutil.cpu_percent(interval=1)

    #Memory Info
    memory = psutil.virtual_memory()

    #Disk Usage
    disk = psutil.disk_usage('/')

    return cpu_temp, cpu_percent, memory, disk

def display_stats():
    """Display formatted system stats"""
    print("\n" + "="*50)
    print("RASPBERRY PI HEALTH MONITOR")
    print("="*50)

    temp, cpu, memory, disk = get_pi_stats()

    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"🌡️  CPU Temperature: {temp}°C")
    print(f"⚡ CPU Usage: {cpu}%")
    print(f"🧠 Memory Usage: {memory.percent}% ({memory.used // (1024**2)}MB used)")
    print(f"💾 Disk Usage: {disk.percent}% ({disk.used // (1024**3)}GB used)")

    #Health Warnings
    if isinstance(temp, float) and temp > 70:
        print("CPU running hot")
    if cpu > 80:
        print("High CPU usage")
    if memory.percent > 80:
        print("Low memory")

def main():
    print("Starting Pi Health Monitor")
    print("Press Ctrl + C to stop")

    try: 
        while True:
            display_stats()
            time.sleep(5)
    except KeyboardInterrupt:
        print("Health monitor stopped")
if __name__ == "__main__":
    main()