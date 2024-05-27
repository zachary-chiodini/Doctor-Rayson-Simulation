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

    def __init__(self):
        self._glfw_init = glfw.init()
        if not self._glfw_init:
            raise RuntimeError('GLFW could not be initialized.')
        monitor = self.Monitor()
        self._glfw_window = glfw.create_window(
            *monitor.resolution, monitor.name, monitor.object, None)
        if not self._glfw_window:
            self._close()
            raise RuntimeError('GLFW window could not be created')
        glfw.set_key_callback(self._glfw_window, self._key_callback)
        glfw.make_context_current(self._glfw_window)

    def is_open(self) -> int:
        return self._glfw_init & (1 - glfw.window_should_close(self._glfw_window)) or self._close()

    def refresh(self) -> None:
        glfw.swap_buffers(self._glfw_window)
        glfw.poll_events()
        return None

    def _close(self) -> int:
        if self._glfw_init:
            glfw.terminate()
            self._glfw_init = 0
        return 0

    @staticmethod
    def _key_callback(glfw_window, key, scancode, action, mods) -> None:
        if (key == glfw.KEY_ESCAPE) & (action == glfw.PRESS):
            glfw.set_window_should_close(glfw_window, glfw.TRUE)
