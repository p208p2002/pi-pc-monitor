import psutil
from cpuinfo import get_cpu_info
import json

# In[]:
    # psutil.cpu_freq(percpu=False)
    # psutil.cpu_percent(interval = None,percpu = False)
    # psutil.virtual_memory()

def getUsageMsg():
    cpuPercent = psutil.cpu_percent(interval = None,percpu = False)
    virtualMem = psutil.virtual_memory()[2]

    usageMsg = {
        "Type":"USAGE_MSG",
        "Data":{
            "CPU_PERCENT":cpuPercent,
            "MEM_USED":virtualMem
        },
    }
    return json.dumps(usageMsg)

def getBasicMsg():
    cpuModel = get_cpu_info()['brand']
    cpuCountLogical = psutil.cpu_count(logical=True)
    cpuCount =  psutil.cpu_count(logical=False)
    ramTotalSize = round(psutil.virtual_memory()[0]/1024/1024)

    basicMsg = {
        "Type":"BASIC_MSG",
        "Data":{
            "CPU_Model":cpuModel,
            "CPU_Count":cpuCount,
            "CPU_Count_Logical":cpuCountLogical,
            "RAM_Total_Size":ramTotalSize
        },
    }
    return json.dumps(basicMsg)

