from nptyping import Float, NDArray, Shape


Matrix = NDArray[Shape['*, 3'], Float]
Vector = NDArray[Shape['3'], Float]
Vertex = NDArray[Shape['*'], Float]
