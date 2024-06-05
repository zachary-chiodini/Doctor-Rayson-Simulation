import vulkan as v


class Vulkan:
    
    def __init__(self):
        info = v.VkInstanceCreateInfo()
        self._instance = v.vkCreateInstance(info)
