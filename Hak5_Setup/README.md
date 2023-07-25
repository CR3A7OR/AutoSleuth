# Hak5 Rubber Ducky USB

The updated version of the **AutoSleuth** Project here is designed for users with a [Hak5 Rubber Ducky](https://shop.hak5.org/products/usb-rubber-ducky). The setup is much simpler and requires only a few steps to setup a functional payload. Useful resources for this project include: 
- [Payload Library](https://github.com/hak5/usbrubberducky-payloads/tree/master)
- [Documentation](https://docs.hak5.org/hak5-usb-rubber-ducky/)

## Setup 
1. Move the **ftkimager** and **exeFiles** into the payloads folder
2. Update the http:// links in `payload.txt` to point to correct ip (replace *localhost*)
3. Upload `payload.txt` to [Hak5 Studio](https://payloadstudio.hak5.org/community/) and generate a `inject.bin`
4. Select Keyboard Layout: `Settings -> Compiler Settings -> Language`
5. Copy `inject.bin` into the root directory of the USB

### » File Hierarchy
```
📂DUCKY
└📄inject.bin
└📁payloads
 └📁exeFiles
 └📁ftkimager
```

## Improvements 
Using the Rubber Ducky some significant improvments are visible when compared to my original Bachelor construct: \
✔ OS Detection means no running of redundant code \
✔ Faster operation \
✔ Single USB required \
✔ Less reliance on custom keyboard layout and delays for keystroke entry
