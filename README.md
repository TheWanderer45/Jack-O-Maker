# Jack-O-Maker
A simple drawing app that helps people create jack-o-lantern stencils.

Why is it a bad idea to carve the Target logo in a pumpkin?

The Target logo consists of several circles inside each other.
As soon as you carve the outermost circle, everything inside becomes detached from the pumpkin.
That leaves you with just a large circle instead of the Target logo.

The inner parts of the larger circle that are part of the logo but get carved out are what I call "islands."
Just as islands are surrounded by water in real life, islands in pumpkin carving are surrounded by parts that are meant to be carved out.
By nature, these islands cannot stay part of the pumpkin.

This app comes with an island detection feature to help you find these and get rid of them before you accidentally carve them out.
When activated, any islands detected on the canvas will be filled with red.
You can resolve islands by connecting these red parts to another white part or manually filling them in with grey.
You may then use the feature again to see if the islands still exist.
The feature can be found in the toolbar or with the shortcut Ctrl+I or Cmd+I.
Ideally, you should use this feature at the end of your jack-o-lantern stencil design process and there should be no red marks when you do.

This app comes with save and load features, a clear canvas feature, several brush size options, and only two colors: white and grey.
The grey parts are intended to be carved out completely.
When your design is done, you can save it as a PNG or JPEG, print it out, and use it as an actual jack-o-lantern stencil.

I used a drawing app tutorial from [geeksforgeeks](https://www.geeksforgeeks.org/python/pyqt5-create-paint-application/) and a flood fill algorithm from [mfitzp](https://stackoverflow.com/questions/52460040/implementing-flood-fill-in-pyqt5) on StackOverflow with my own modifications.


