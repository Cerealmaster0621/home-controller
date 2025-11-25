## iot

## After connecting with GPIO port

`sudo nano /boot/firmware/config.txt`
`dtoverlay=gpio-ir-tx,gpio_pin={PORT NUMBER}`
`sudo reboot`


## how to record with IR receiver 
`ir-ctl -r -d /dev/lirc0 --mode2 --one-shot > 파일이름.txt`

