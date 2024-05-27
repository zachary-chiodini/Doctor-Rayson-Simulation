import glfw


class Window:

    class Monitor:
        """Defaults to primary monitor."""

        def __init__(self):
            self.name = 'Doctor Rayson Simulation'
            self.object = glfw.get_primary_monitor()
            video_mode = glfw.get_video_mode(self.object)
            self.resolution = video_mode.size
            self.refresh_rate = video_mode.refresh_rate

    instantiated = False

    def __init__(self):
        if not glfw.init():
            raise RuntimeError('GLFW could not be initialized.')
        self.instantiated = True
        monitor = self.Monitor()
        self._glfw_window = glfw.create_window(
            *monitor.resolution, monitor.name, monitor.object, None)
        if not self._glfw_window:
            self.close()
            raise RuntimeError('GLFW window could not be created')
        glfw.set_key_callback(self._glfw_window, self.key_callback)
        glfw.make_context_current(self._glfw_window)

    def close(self) -> None:
        if self.instantiated:
            glfw.terminate()
        return None

    def is_open(self) -> int:
        return 1 - glfw.window_should_close(self._glfw_window)

    @staticmethod
    def key_callback(glfw_window, key, scancode, action, mods) -> None:
        if (key == glfw.KEY_ESCAPE) and (action == glfw.PRESS):
            glfw.set_window_should_close(glfw_window, glfw.TRUE)

    def refresh(self) -> None:
        glfw.swap_buffers(self._glfw_window)
        glfw.poll_events()
        return None
