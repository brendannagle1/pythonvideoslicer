# pythonvideoslicer

This program was designed to easily parse 60 second (@ ~60fps) video clips of relatively static action and generate mp4 and gif video outputs without audio

The program currently uses the opencv and imageio libraries

  -- WARNING -- : All Video frames will be loaded into memory if the n-th frame selected is 1.

- The nth frame variable is set to discard frames if a smaller FPS is necessary for larger files.
- Left and Right keys can be used quickly toggle between images as well as moving the slider with the mouse at the top of the screen.
- Press the spacebar to select 2 images for the beggining and end frames. Selecting a later frame, then an earlier one will create the output in reverse.
- Tkinter is used to provide an intial interface for selecting the nth fram variable and the type of output (.gif/.mp4)


