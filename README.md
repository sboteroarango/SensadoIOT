# SensadoIOT
Este proyecto usa un Lilygo modelo Lora 32, un sensor HDC1080 de temperatura y humedad, y un CJMCU-3216 para medir la luz de una planta. 
El modo de ejecución es, en una instancia t3.large de EC2, una vez creada las instancias y subscripciones para cada sensor en el puerto 1026, tener el  archivo app.py y el docker-compose.yml. Después de debe ejecutar:

sudo apt install python3.10 -y
sudo apt install python3-pip -y
sudo sysctl -w vm.max_map_count=262144
sudo docker-compose up -d
usando pip3.10 instalar las librerías necesarias (flask,crate,matplotlib,pandas,requests,io,datetime,os)
sudo python3.10 app.py

Este video muestra el funcionamiento del programa:
https://www.youtube.com/watch?v=Gxqfh-1gEJQ
