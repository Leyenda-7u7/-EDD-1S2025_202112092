UNIVESIDAD DE SAN CARLOS DE GUATEMALA

FACULTAD DE INGENIERIA

ESCUELA DE CIENCAS Y SISTEMAS

ESTRUCTURAS DE DATOS 

SECCIÓN C

SEGUNDO SEMESTRE 2025

AUX. MARCOS ARNOLDO ITZEP IXMAY




<p align="center"> MANUAL TECNICO </p>



BRANDON EDUARDO PABLO GARCIA

202112092

Guatemala, octubre del 2025









# Introduccion

Este manual describe los pasos necesarios para cualquier persona que tenga ciertas bases de sistemas pueda realizar el código implementado en Object Pascal donde se crea un código que simula un sistema de envios de correos usando listas, listas doblemente enlazadas, circulares y pilas, usando punteros como bases. El siguiente código se explicó de la manera más detalla posible para la mejor compresión de la persona.



# Objetivos

* Brindar la información necesaria para poder  representar la funcionalidad técnica de la estructura, diseño y definición del aplicativo.

* Describir las herramientas utilizadas para el diseño y desarrollo del prototipo


# Requerimientos de funcion


|          Requerimientos      |     Descripcion |                                      
|----------------|-------------------------------|
|Lazarus          |Se recomienda el uso del IDE Lazarus (versión 2.0.12 o superior) que fue la versión donde se programó el sistema de información |       
|Graphviz        |Conocimiento sobre el uso de las librerias Graphviz para el uso de las representaciones graficas |            |            |


##	Desarrollo

[![Rojo-Negro-Moderno-Cronograma-Agenda-de-Proyecto-Planificador.jpg](https://i.postimg.cc/LX6pcTk8/Rojo-Negro-Moderno-Cronograma-Agenda-de-Proyecto-Planificador.jpg)](https://postimg.cc/94SKTyN6)

 



#	Contenido tecnico

Este proyecto fue desarrollado bajo una arquitectura modular y orientada a objetos, utilizando Free Pascal y el IDE Lazarus. Para su compilación y ejecución, se requieren las siguientes herramientas y bibliotecas, fundamentales para la manipulación de datos, la interacción con el sistema de archivos y la visualización de la información.

Para comenzar, se utilizo las bibliotecas de la Free Pascal Component Library (FCL). Estoy nos ayudo a poder utilizar fpjson y jsonparser que son unidades estándar para la lectura, análisis y manipulación de datos en formato JSON. Se utilizan para la carga masiva de usuarios desde archivos externos.

Entre las librerias usadas tambien se encuentra Graphviz (DOT Language), es un software de código abierto para la visualización de gráficos y diagramas. Es indispensable para generar los reportes gráficos de las estructuras de datos (listas de usuarios, comunidades, etc.). Todo esto se puede visualizar a travez del ejecutable dot, el cual, es el motor de renderizado de Graphviz, utilizado para convertir archivos .dot (código de descripción del gráfico) a archivos de imagen (.png).

		
    digraph G {
    // Definición de Nodos en Graphviz
    nodo_A;
    nodo_B;
    nodo_C;
    
    // Conexiones
    nodo_A -> nodo_B;
    nodo_A -> nodo_C;
    }

## Sistema Operativo

El Sistema Operativo usado fue Linux (Ubunto). La implementación específica para la apertura de reportes gráficos utiliza comandos nativos de Linux (xdg-open), lo que requiere que el entorno de ejecución sea compatible con estos comandos.

## Estructuras de Datos y Modelado

El sistema se basa en el uso intensivo de punteros para construir listas enlazadas dinámicas, lo que permite una gestión eficiente de la memoria y una manipulación flexible de los datos.

#### Lista Simple Enlazada de Usuarios
La estructura principal del sistema es una lista enlazada doblemente ligada de usuarios.

- TUsuario: Es el registro (o nodo) que almacena la información de cada usuario. Sus campos incluyen Id, Nombre, Usuario, Password, Email y Telefono.
- PUsuario: Es el puntero que referencia a un registro TUsuario.
- Next: PUsuario y Prev: PUsuario: Punteros que permiten la navegación bidireccional a través de la lista. ListaUsuarios: PUsuario es la cabeza global de esta lista.
```
type
  PUsuario = ^TUsuario;
  TUsuario = record
    Id: Integer;
    Usuario: string;
    // ... otros campos
    Next: PUsuario;
    Prev: PUsuario; // Puntero al nodo anterior
  end;

var
  ListaUsuarios: PUsuario;
```
#### Lista Doblemente Enlazada de Correo Electrónico

Cada nodo (TUsuario) contiene una referencia a una lista enlazada doblemente ligada de correos electrónicos.

- TCorreo: Registro para almacenar detalles de un correo, como Asunto, Mensaje, Remitente, Destinatario, Fecha y Estado (leido o no leido).
- PCorreo: Puntero a un registro TCorreo.

```
type
  PCorreo = ^TCorreo;
  TCorreo = record
    Asunto: string;
    // ... otros campos
    Next: PCorreo;
    Prev: PCorreo; // Puntero al nodo anterior
  end;

  TUsuario = record
    // ... campos del usuario
    Correos: PCorreo; // Puntero a la cabecera de la lista de correos
    // ...
  end;
```
 
### Lista de Listas (Comunidades y Usuarios)
Para modelar la relación de "uno a muchos" (una comunidad tiene muchos usuarios), se implementó una lista anidada o lista de listas.

- Lista Principal (TComunidad): Una lista enlazada simple de comunidades, donde cada nodo representa una comunidad.
- Listas Secundarias (TUsuarioComunidad): Cada nodo TComunidad tiene un puntero a la cabeza de su propia lista enlazada simple de usuarios, que pertenecen a esa comunidad.

```
type
  PUsuarioComunidad = ^TUsuarioComunidad;
  TUsuarioComunidad = record
    CorreoUsuario: string;
    Next: PUsuarioComunidad;
  end;

  PComunidad = ^TComunidad;
  TComunidad = record
    NombreComunidad: string;
    Usuarios: PUsuarioComunidad; // Puntero a la lista de usuarios
    Next: PComunidad;
  end;
  
  var
  ListaComunidades: PComunidad;
  ```
  
### La Pila para la Papelera
La papelera de correos se implementó usando una pila (stack), una estructura de datos LIFO (Last-In, First-Out). Los correos eliminados se "apilan" uno encima del otro. El último correo que se elimina es el primero que se puede restaurar. Se utiliza una variable global (Papelera) que actúa como el puntero superior de la pila. Las operaciones principales son Push (agregar a la pila) y Pop (quitar de la pila).

  ```
type
  PNodoPila = ^TNodoPila;
  TNodoPila = record
    Correo: TCorreo; // O un puntero a un correo
    Next: PNodoPila;
  end;

var
  Papelera: PNodoPila; // Puntero a la cima de la pila

// Pseudo-código para la operación PUSH
procedure Push(P_Correo: TCorreo);
begin
  New(NuevoNodo);
  NuevoNodo^.Correo := P_Correo;
  NuevoNodo^.Next := Papelera;
  Papelera := NuevoNodo;
end;
  ```
  
### La Cola para Correos Programados
La gestión de los correos programados se realiza a través de una cola (queue), una estructura de datos FIFO (First-In, First-Out). Los correos se añaden al final de la cola y se procesan en el mismo orden en que fueron agregados, lo que garantiza que se envíen en el momento y la secuencia correctos. Se utilizan dos punteros para controlar la estructura: Frente para el primer correo en la cola y Final para el último.

  ```
  type
  PNodoCola = ^TNodoCola;
  TNodoCola = record
    Correo: TCorreo;
    Next: PNodoCola;
  end;

var
  ColaCorreosProgramados: record
    Frente: PNodoCola;
    Final: PNodoCola;
  end;

// Pseudo-código para la operación ENQUEUE
procedure Enqueue(P_Correo: TCorreo);
begin
  New(NuevoNodo);
  NuevoNodo^.Correo := P_Correo;
  NuevoNodo^.Next := nil;
  if Cola.Final = nil then
    Cola.Frente := NuevoNodo
  else
    Cola.Final^.Next := NuevoNodo;
  Cola.Final := NuevoNodo;
end;
  ```
    
### La Lista Circular para Contactos
Para los contactos, se implementó una lista enlazada circular. Esta estructura es ideal para una gestión de contactos, ya que permite navegar de manera continua a través de la lista sin un punto final. El último nodo de la lista apunta de nuevo al primer nodo, formando un círculo. Solo se necesita un único puntero de cabecera que apunte a cualquier nodo, ya que se puede acceder a toda la lista desde ese punto.

  ```
  type
  PNodoContacto = ^TNodoContacto;
  TNodoContacto = record
    Email: string;
    // ... otros campos
    Next: PNodoContacto;
  end;

var
  ListaContactos: PNodoContacto; // Puntero a un nodo de la lista circular 
  ```

### El Árbol B para Correos Favoritos
La gestión de los correos favoritos se realiza a través de un árbol B de orden 5. Esta estructura de datos es ideal para bases de datos y sistemas de archivos, ya que mantiene los datos ordenados y optimiza las operaciones de búsqueda, inserción y eliminación. A diferencia de un árbol binario, el árbol B puede tener múltiples claves y ramas por nodo, lo que reduce su altura y minimiza el tiempo de acceso.

Cada nodo del árbol B puede contener hasta 4 correos (claves) y 5 punteros a sus hijos. Esto permite que el árbol se mantenga balanceado automáticamente. El nodo raíz del árbol nunca está vacío.

```
type
  TCorreoFavorito = class;
  TBNodo = class
    NumClaves: Integer;
    Claves: array[0..ORDEN - 2] of TCorreoFavorito;
    Hijos: array[0..ORDEN - 1] of TBNodo;
    EsHoja: Boolean;
    constructor Create;
  end;

// Pseudo-código para la operación de INSERCIÓN
procedure Insertar(aCorreo: TCorreoFavorito);
var
  r: TBNodo;
begin
  r := Raiz;
  if r.NumClaves = (ORDEN - 1) then
  begin
    // Si la raíz está llena, se divide
    New(s);
    Raiz := s;
    s.EsHoja := False;
    s.NumClaves := 0;
    s.Hijos[0] := r;
    // se llama a la función para dividir el nodo lleno
    s.DividirHijo(0, r);
    s.InsertarNoLleno(aCorreo);
  end
  else
    r.InsertarNoLleno(aCorreo);
end;
```

### El Árbol AVL para Borradores de Correo
Los borradores se gestionan con un árbol AVL, una variante del árbol binario de búsqueda que se mantiene auto-balanceado. La clave aquí es el factor de equilibrio, que es la diferencia de altura entre el subárbol izquierdo y el derecho de cada nodo. Si este factor se desequilibra (es mayor a 1 o menor a -1), el árbol realiza rotaciones (izquierda o derecha) para reequilibrarse, garantizando que el acceso a los datos sea siempre eficiente.

Cada nodo del árbol AVL almacena un borrador, junto con referencias a sus hijos y su altura. Esto permite búsquedas, inserciones y eliminaciones muy rápidas, lo que es ideal para acceder rápidamente a los borradores.

```
type
  TCorreoBorrador = class;
  TAVLNodo = class
    Correo: TCorreoBorrador;
    Izquierdo: TAVLNodo;
    Derecho: TAVLNodo;
    Altura: Integer;
  end;

// Pseudo-código para la operación de INSERCIÓN
function InsertarEnArbol(aNodo: TAVLNodo; aCorreo: TCorreoBorrador): TAVLNodo;
begin
  if aNodo = nil then
  begin
    Result := TAVLNodo.Create(aCorreo);
    Exit;
  end;
  // ... lógica de inserción
  if aCorreo.Id < aNodo.Correo.Id then
    aNodo.Izquierdo := InsertarEnArbol(aNodo.Izquierdo, aCorreo)
  else
    aNodo.Derecho := InsertarEnArbol(aNodo.Derecho, aCorreo);

  aNodo.Altura := 1 + Max(ObtenerAltura(aNodo.Izquierdo), ObtenerAltura(aNodo.Derecho));
  Factor := ObtenerFactorEquilibrio(aNodo);

  // ... lógica de rotaciones para equilibrar el árbol
  if (Factor > 1) and (aCorreo.Id < aNodo.Izquierdo.Correo.Id) then
    Result := RotarDerecha(aNodo);
  // ... resto de las rotaciones
end;
```

 # Interfaz
 
En la interfaz se le muestra a contunuacion 

#### Login
La interfaz seria la siguiente:

[![Captura-desde-2025-09-02-16-54-42.png](https://i.postimg.cc/rpWrhpDm/Captura-desde-2025-09-02-16-54-42.png)](https://postimg.cc/GBLttdJw)


### Ingreso del Usuario ROOT

El usuario ROOT es el administrador y podra realizar lo que se muestra a continuacion

[![Captura-desde-2025-09-02-17-00-39.png](https://i.postimg.cc/cCvPPmsX/Captura-desde-2025-09-02-17-00-39.png)](https://postimg.cc/hQqCdVQd)

##### Carga Masiva
 
De esta manera se ve la carga masvia 

[![Captura-desde-2025-09-30-15-43-21.png](https://i.postimg.cc/Y0kPGprs/Captura-desde-2025-09-30-15-43-21.png)](https://postimg.cc/R6sd2xn7)

En esta parte realizara dicha carga 

[![Captura-desde-2025-09-30-15-44-29.png](https://i.postimg.cc/zfKpn9c5/Captura-desde-2025-09-30-15-44-29.png)](https://postimg.cc/Z9YrmDmD)


##### Menu de Usuario

El usuario podra realizar todo esto que se le indica 

[![Captura-desde-2025-09-30-15-54-46.png](https://i.postimg.cc/gJDJQHJF/Captura-desde-2025-09-30-15-54-46.png)](https://postimg.cc/sQMsZS7w)



