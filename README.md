# Raccoons8741-code2026
Codigo de Raccoons 8741 para el First Robotics competition 2026

Main code desarrollado por Dabit, diferentes branches seran para los diferentes proyectos y ramificaciones


# Instrucciones
--------------------------
# Instalacion del Software

1- Instalar WPILIB desde la documentacion oficial de FRC, link aca abajo, solo instala y ejecuta
https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/wpilib-setup.html

2- Instalar REVLIB
Esta parte es un poco mas compleja, tienes dos opciones
- Online instalation: Mas simple, simplemente en tu vscode de wpilib busca la seccion de vendor dependencies, las cuales estan con el logo de wpilib en la izquierda al fondo, y busca revlib

- Ofline instalation: Mas complicado, ya esta adjunto la dependencia en la carpeta de dependencias, solo se tiene que seguir las instrucciones proporcionadas por la documentacion de first
https://docs.wpilib.org/en/latest/docs/software/vscode-overview/3rd-party-libraries.html#adding-offline-libraries

# Carpetas

La carpeta unica que esta es la del codigo del robot, si te da errores al copiarlo en tu computadora haz un nuevo file de wpilib y copia el codigo ahi, recuerda volver a hacer lo de la instalacion de REVlib si es necesario

# Broad documentation step by step
Puede tener errores en primeras versiones, por mejorar
### Import's
La primera parte son varias importacion, todas deberian checar que hace cada una, pero en lo personal las mas importantes son SparkMax y XboxController

### TimedRobot
Este codigo es usado cuando el robot enciende por primera vez y se deberia usar para inicializar variables
- Establecemos los sparks de los motores
- Establecemos los sparks de el lanzador y direccionador
- Establecemos el control
- Establecemos el robot container y autonomous commands

OJO, en los motores solo establecemos dos motores porque los otros dos estan como followers, esto lo configuramos en la aplicacion de rev

### Robot
Esta parte es llamada cada 20ms sin importar el modo del robot, se deberia usar para cosas como diagnosticos, etc.




