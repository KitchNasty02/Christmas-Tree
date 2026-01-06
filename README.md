# Christmas Tree Project

The goal of this project is to have more complex LED patterns on a Christmas tree. I used an Arduino Uno and a custom-designed and built PCB to interface between the Uno and the Neopixel lights. The PCB allows the whole system to run off a 5V 10A power supply. The Python vision script maps the coordinates of the LEDs into a mapped range of -1 to 1 in the x/y, with the z scaled proportionally to them. The tree is scanned in 4 different directions, which can be converted into 3D coordinates for each LED. These coordinates are translated and manipulated to create different patterns.


## PCB Design in KiCad:

<div align="center">
  <img height="250" alt="PCB" src="https://github.com/user-attachments/assets/2a295851-252e-4809-bc63-9d9f43c390c6" />
  <img height="250" alt="3D_view_pcb" src="https://github.com/user-attachments/assets/1917db8c-b034-4167-b316-ffcf00c8510c" />
  <img height="250" alt="IMG_3037" src="https://github.com/user-attachments/assets/dad54a37-7cbf-4fad-90f8-d50af33efe3c" />
</div>


## Pattern Examples

Rainbow:
<video src="https://github.com/user-attachments/assets/0f6e10a9-0110-4c18-8e69-efe2349c4bbb" controls height="300"></video>

<br/>
Rainbow Theater Chase:
<video src="https://github.com/user-attachments/assets/7815d67a-6773-413e-9849-2f68e6898052" controls height="300"></video>

<br/>
Particle:
add particle video here


