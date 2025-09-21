# EDD 1S2025 202112092
## PROYECTO F2
### DESCRIPCION

El proyecto consiste en la evolución de un sistema de simulación de correos electrónicos implementado en
Object Pascal utilizando la librería GTK. Este sistema permitirá a los usuarios registrarse, iniciar sesión,
enviar y recibir correos, gestionar contactos, programar envíos automáticos, organizar comunidades
jerárquicas y administrar correos favoritos, todo a través de una interfaz gráfica intuitiva. 

La aplicación está
diseñada para simular un entorno de correo electrónico real, con funcionalidades avanzadas como bandeja
de entrada, correos eliminados, favoritos, borradores, reportes gráficos y gestión de comunidades,
enfocándose en el uso eficiente de estructuras de datos dinámicas, incluyendo árboles para optimizar
búsquedas, inserciones y organización jerárquica.

El sistema incluirá un usuario administrador (root) con privilegios especiales, como la carga masiva de
usuarios desde un archivo JSON y la generación de reportes específicos para estructuras como árboles y
matrices. 

Los usuarios estándar podrán interactuar con una bandeja de entrada, (ordenada por árboles
AVL), gestionar contactos (usando BST), enviar correos a contactos registrados, programar envíos
automáticos, administrar correos favoritos (indexados en un árbol B de orden 5), guardar correos como
borradores (ordenada en árboles AVL) actualizar su perfil y participar en comunidades jerárquicas
(organizadas en un árbol n-ario). 

La visualización de relaciones entre emisores y receptores se realizará
mediante una matriz dispersa, y todas las funcionalidades estarán soportadas por estructuras de datos
optimizadas para garantizar un manejo eficiente y escalable de la información.
