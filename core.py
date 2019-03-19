import psutil
from cpuinfo import get_cpu_info

# In[]:
    # psutil.cpu_freq(percpu=False)
    # psutil.cpu_percent(interval = None,percpu = False)
    # psutil.virtual_memory()

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
    return basicMsg

