# torus-engine

## Description

Basic ASCII 3D rendering engine on the terminal.

## Install

### Download using pip

Open your terminal and type:

> `pip install torus-engine`

You can find more information on the package on PyPI by clicking [here](https://pypi.org/project/torus-engine/#description).

### Import to your Python project

In your Python project, add this line at the top of the file you wish to have access to the `torus-engine` package:

### Tutorial

Let's go through a simple tutorial that showcases the different essential functionalities of the `torus-engine` API.

#### Creating an object, `Torus`

You can choose which object you want to render. See `torusengine/objects` for the different objects available. Alternatively, you can create your own, as long as it satisfies the requirements.

```{.Python}
import torusengine.objects.orus import Torus

torus = Torus()
```

#### Adding a light source, `Light`

Then you can add a light source:

```{.Python}
import torusengine.light import Light

light_source_position = (2, 1, 0) # (x, y, z) coordinates
light_source = Light(position=light_source_position)
```

#### Placing a `Camera`

You also need a camera. To do that you can follow the code below:

```{.Python}
import torusengine.camera import Camera

camera_point = (1, 0, 0) # (x, y, z) coordinates
camera = Camera(camera_position=camera_point)
```

`Camera` takes as optional parameters `point_to_fix`, which is where the camera is pointing (`(0, 0, 0)` by default), and `horizontal_rotation` which determines the tilt of the camera.

#### Putting it altogether to create a `Scene`

You can now create a `Scene`, by passing the object, the light source and the camera:

```{.Python}
import torusengine.scene import Scene

scene = Scene(torus, light_source, camera)
```

`Scene` can also take the `fps` parameter (frames per second), which is set to 5 by default.

With the object `scene` instantiated, you can now call its `start()` method:

```{.Python}
scene.start()
```

It can take as parameter the boolean `static` (set to `False` by default), which determines whether to update the scene only once, or to update it conitnuously (according to its `fps` value).

Additional methods of the class `Scene` can be called, to change the camera (by moving it up, down, left or right), to increase or decrease the light source intensity, or even to change the object being rendered altogether.

## 🛠 Improvments
Feel free to create an issue or a pull request in case you find bugs or want to add a feature!