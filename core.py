
# coding: utf-8

# In[6]:


import psutil
from cpuinfo import get_cpu_info


# In[7]:


cpuCountLogical = psutil.cpu_count(logical=True)
cpuCount =  psutil.cpu_count(logical=False)
print("CPU %d/%d" % (cpuCount,cpuCountLogical))


# In[8]:


print(get_cpu_info()['brand'])


# In[15]:


psutil.cpu_freq(percpu=False)


# In[22]:


psutil.cpu_percent(interval = None,percpu = False)


# In[23]:


psutil.virtual_memory()

