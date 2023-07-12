<p align="center"><img src="assets/icon.png" alt="" /></p>
<h1 align="center">Booru Tagger</h1>

Simple application made in Python for tagging datasets using Booru-style tags.

## Features

* Image Preview
* Tag Frequency
* Hotkeys
* Template

## Main Window

<img src="assets/readme-images/main.png" align="right"/>

- Thumbnail preview 
- <span style="color: #D3FFC0">Image Tags</span>
- <span style="color: #D2D5FF">Used Tags</span>
- Add tag to all images
- Remove individual tag from all files
- Remove from all tags from images above or below 

## Image Preview

<img src="assets/readme-images/image-preview.png" align="right"/>

- Image resized to 512 for preview
- Real dimensions displayed below image

## Tag Frequency

<img src="assets/readme-images/tags.png" align="right"/>

- Shows tag frequency
- Tags saved to "exported tags.txt"

## Hotkeys

<img src="assets/readme-images/hotkeys.png" align="right"/>

- Currently you can only add, delete and save tags using hotkeys
- "Add Tag to Table" add a selected tag from the <span style="color: #D2D5FF">Used Tags</span> panel to the <span style="color: #D3FFC0">Image Tags</span> panel
- "Add New Row" adds a new empty row to the selected panel
- "Add New Row Below" adds a new empty row below the selected tag

## Template

- Open/Save tags from the <span style="color: #D2D5FF">Used Tags</span> panel to a .tagger file.

## Default Hotkeys

- **Page Up:** Select image above
- **Page Down:** Select image below
- **Ctrl+S:** Save <span style="color: #D3FFC0">Image Tags</span>
- **Ctrl+D:** Add tag from <span style="color: #D2D5FF">Used Tags</span> to <span style="color: #D3FFC0">Image Tags</span>
- **Delete:** Delete selected row
- **Insert:** Add new empty row to selected panel
- **Ctrl+Insert:** Add new empty row below the selected row

## Todo

- [ ] Add buttons to handle tags add/remove/save functions
- [ ] Add tag filters
- [ ] Add in-app image crop