from OpenGL.GL import GL_DYNAMIC_DRAW

from graphics import Program, Window, VertexArray
from simulation import Space
from nptypes import Vertex


if __name__ == '__main__':
    window = Window()
    vertex_array = VertexArray()
    plane: Vertex = Space().plane
    vertex_array.create_buffer(plane, 3, GL_DYNAMIC_DRAW)
    vertex_array.create_array()
    program = Program()
    while window.is_open():
        window.refresh()
