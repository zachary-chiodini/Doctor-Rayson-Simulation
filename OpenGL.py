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
        self.context = glfw.create_window(
            *monitor.resolution, monitor.name, monitor.object, None)
        if not self.context:
            self.close()
            raise RuntimeError('GLFW window could not be created')
        glfw.set_key_callback(self.context, self.key_callback)
        glfw.make_context_current(self.context)

    def close(self) -> None:
        if self.instantiated:
            glfw.terminate()
        return None

    def is_open(self) -> int:
        return 1 - glfw.window_should_close(self.context)

    @staticmethod
    def key_callback(window, key, scancode, action, mods) -> None:
        if (key == glfw.KEY_ESCAPE) and (action == glfw.PRESS):
            glfw.set_window_should_close(window, glfw.TRUE)

    def refresh(self) -> None:
        glfw.swap_buffers(self.context)
        glfw.poll_events()
        return None
