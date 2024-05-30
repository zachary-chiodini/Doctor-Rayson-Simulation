from typing import List

import glfw
from numpy import uintc
from OpenGL import GL

from nptypes import Matrix, Vector, Vertex


class VertexArray:

    def __init__(self) -> None:
        self._vba = uintc()
        self.vba_comps: List[int] = []
        self.vbo_list: List[uintc] = []

    def create_array(self) -> None:
        if not self.vbo_list:
            raise AttributeError('A Vertex Buffer Object must be created.')
        self._vba = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vba)
        for i, (vbo, comps) in enumerate(zip(self.vbo_list, self.vba_comps)):
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
            GL.glVertexAttribPointer(i, comps, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
            GL.glEnableVertexAttribArray(i)
        return None

    def create_buffer(self, vertex_stream: Vertex, components: int, usage: str) -> None:
        map_ = {'dynamic': GL.GL_DYNAMIC_DRAW}
        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertex_stream.size * vertex_stream.itemsize, vertex_stream, map_[usage])
        self.vbo_list.append(vbo)
        self.vba_comps.append(components)
        return None

    @staticmethod
    def draw_triangles(vector_count: int) -> None:
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, vector_count)
        return None


class Monitor:
    """Defaults to primary monitor."""

    def __init__(self):
        self.name = 'Doctor Rayson Simulation'
        self.object = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(self.object)
        self.resolution = video_mode.size
        self.refresh_rate = video_mode.refresh_rate


class Program:

    default_fragment_shader_src = '''
        // OpenGL Shader Language:
        void main() {
            // Elements are R, G, B and alpha.
            gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
        }
        '''
    default_vertex_shader_src = '''
        // OpenGL Shader Language:
        in vec3 xyzPosition;
        void main() {
            // 4D vector uses homogeneous coordinates.
            gl_Position = vec4(xyzPosition, 1.0);
        }
        '''

    def __init__(
            self, fragment_shader_src: str = default_fragment_shader_src,
            vertex_shader_src: str = default_vertex_shader_src):
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
        GL.glDeleteProgram(self._program)
        return None

    def use_program(self) -> None:
        GL.glUseProgram(self._program)
        return None


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
