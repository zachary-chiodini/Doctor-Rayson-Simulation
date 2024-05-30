from OpenGL.GL import GL_DYNAMIC_DRAW

from graphics import Program, Window, VertexArray
from simulation import Space
from nptypes import Vertex


if __name__ == '__main__':
    window = Window()
    vertex_array = VertexArray()
    stream: Vertex = Space().plane
    vertex_array.create_buffer(stream, 3, GL_DYNAMIC_DRAW)
    vertex_array.create_array()
    program = Program()
    while window.is_open():
        program.use_program()
        vertex_array.draw_triangles(stream.size // 3)
        window.refresh()
