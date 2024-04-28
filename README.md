[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-718a45dd9cf7e7f842a935f5ebbe5719a5e09af4491e668f4dbf3b35d5cca122.svg)](https://classroom.github.com/online_ide?assignment_repo_id=13804652&assignment_repo_type=AssignmentRepo)

# Vision Board Maker
## CS110 Final Project Spring, 2024

## Team Members

Matt-Joshua Tan

***

## Project Description

Create your own vision board in Pygame! Use your imagination and Stable Diffusion to create a motivational poster for yourself, just like you did when you were young.

***    

## GUI Design

### Initial Design

![initial gui](assets/guidraft.jpg)

### Final Design

TBD
![final gui](assets/finalgui.jpg)

## Program Design

### Features

1. Add text with customizable color, size, and font
2. Add images from various sources
3. Change the background color
4. Remove text and images if you change your mind
5. Save your vision board as an image!

### Classes

Expected classes:
1. Text class (as sprite) holds text in vision board as objects
2. Image class (as sprite) holds images in vision board as objects

## ATP

| Step                 |Procedure             |Expected Results                   |
|----------------------|:--------------------:|----------------------------------:|
|  1: Menu and Board                  | Run program and click screen  |Start menu appears; after clicking, black screen appears with GUI and "Save" button. |
|  2: Adding Text                   | Click 'Add Text' | Add Text" GUI appears. After entering text and choosing settings, 'Choose Location' prompt appears; after clicking location, given text is added. |
| 3: Adding Images | Click 'Add Image' | "Add Image" GUI appears. After finding image and choosing settings, 'Choose Location' prompt appears; after clicking location, given image is added. |
| 4: Removing Text and Images | RIGHT click on text or image | Text or image is deleted |
| 5: Saving and Loading Board States | Press "Z" to save board state | "Board saved." appears; after pressing "X", the board will be cleared and the saved board state will appear. |
| 6: Saving Board as Image | Press "Save Button" in bottom right corner. | File dialog appears; after saving location, the board will be saved as an image and the end menu will appear. | 
etc...
