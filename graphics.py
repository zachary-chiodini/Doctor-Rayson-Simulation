from typing import List, Optional

import glfw
from nptyping import Float, NDArray, Shape
from OpenGL import GL
from OpenGL.constant import IntConstant


Vector = NDArray[Shape['*'], Float]


class VertexArray:

    def __init__(self) -> None:
        self._vba = GL.c_int()
        self.vba_comps: List[int] = []
        self.vbo_list: List[GL.ctypes.c_long] = []

    def create_array(self) -> None:
        if not self.vbo_list:
            raise AttributeError('A Vertex Buffer Object must be created.')
        GL.glGenVertexArrays(1, self._vba)
        GL.glBindVertexArray(self._vba)
        for i, (vbo, comps) in enumerate(zip(self.vbo_list, self.vba_comps)):
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
            GL.glVertexAttribPointer(i, comps, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
            GL.glEnableVertexAttribArray(i)
        return None

    def create_buffer(self, vertex_stream: Vector, components: int, usage: IntConstant) -> None:
        vbo = GL.c_int()
        GL.glGenBuffers(1, vbo)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertex_stream.size * vertex_stream.itemsize, vertex_stream, usage)
        self.vbo_list.append(vbo)
        self.vba_comps.append(components)
        return None

    def delete(self) -> None:
        pass


class Monitor:
    """Defaults to primary monitor."""

    def __init__(self):
        self.name = 'Doctor Rayson Simulation'
        self.object = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(self.object)
        self.resolution = video_mode.size
        self.refresh_rate = video_mode.refresh_rate


class Program:

    def __init__(self):
        fragment_shader_src = '''
            // OpenGL Shader Language:
            void main() {
                // Elements are R, G, B and alpha.
                gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
            }
            '''
        vertex_shader_src = '''
            // OpenGL Shader Language:
            in vec3 xyzPosition;
            void main() {
                // 4D vector uses homogeneous coordinates.
                gl_Position = vec4(xyzPosition, 1);
            }
            '''
        self._vertex_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        self._fragment_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        GL.glShaderSource(self._vertex_shader, vertex_shader_src)
        GL.glShaderSource(self._fragment_shader, fragment_shader_src)
        GL.glCompileShader(self._vertex_shader)
        GL.glCompileShader(self._fragment_shader)
        self._program = GL.glCreateProgram()
        GL.glAttachShader(self._program, self._vertex_shader)
        GL.glAttachShader(self._program, self._fragment_shader)
        GL.glLinkProgram(self._program)
        GL.glDetachShader(self._program, self._vertex_shader)
        GL.glDetachShader(self._program, self._fragment_shader)

    def exit(self) -> None:
        GL.glDeleteShader(self._program, self._vertex_shader)
        GL.glDeleteShader(self._program, self._fragment_shader)


class Window:

    def __init__(self):
        self._glfw_init = glfw.init()
        if not self._glfw_init:
            raise RuntimeError('GLFW could not be initialized.')
        monitor = Monitor()
        self._glfw_window = glfw.create_window(
            *monitor.resolution, monitor.name, monitor.object, None)
        if not self._glfw_window:
            self.close()
            raise RuntimeError('GLFW window could not be created')
        glfw.set_key_callback(self._glfw_window, self._key_callback)
        glfw.make_context_current(self._glfw_window)

    def close(self) -> int:
        if self._glfw_init:
            glfw.terminate()
            self._glfw_init = 0
        return 0

    def is_open(self) -> int:
        """Checks to see if the GLFW window is open and closes it if it should be closed."""
        return self._glfw_init & (1 - glfw.window_should_close(self._glfw_window)) or self.close()

    def refresh(self) -> None:
        glfw.swap_buffers(self._glfw_window)
        glfw.poll_events()
        return None

    @staticmethod
    def _key_callback(glfw_window, key, scancode, action, mods) -> None:
        if (key == glfw.KEY_ESCAPE) & (action == glfw.PRESS):
            glfw.set_window_should_close(glfw_window, glfw.TRUE)
        return None
