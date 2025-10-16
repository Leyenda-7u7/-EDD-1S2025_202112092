import graphviz
import os

class GrafoCiudades:
    """Representa un grafo no dirigido donde los nodos son ciudades."""

    def __init__(self):
        self.adj = {}

    def agregar_nodo(self, ciudad):
        """Agrega un nodo (ciudad) al grafo si no existe."""
        ciudad = ciudad.strip().upper()
        if not ciudad:
            print("El nombre de la ciudad no puede estar vacío.")
            return False
            
        if ciudad not in self.adj:
            self.adj[ciudad] = []
            print(f"Ciudad '{ciudad}' agregada.")
            return True
        else:
            print(f"Ciudad '{ciudad}' ya existe.")
            return False

    def agregar_conexion(self, ciudad1, ciudad2, peso=None):
        """
        Agrega una arista bidireccional entre dos ciudades.
        """
        ciudad1 = ciudad1.strip().upper()
        ciudad2 = ciudad2.strip().upper()

        if ciudad1 == ciudad2:
            print("No se permite la conexión de una ciudad consigo misma.")
            return False

        # Asegurar que ambos nodos existan antes de la conexión
        if ciudad1 not in self.adj:
            self.agregar_nodo(ciudad1)
        if ciudad2 not in self.adj:
            self.agregar_nodo(ciudad2)

        # Conexión bidireccional
        agregada1 = self._agregar_arista_simple(ciudad1, ciudad2, peso)
        agregada2 = self._agregar_arista_simple(ciudad2, ciudad1, peso)
        
        if agregada1 or agregada2:
            print(f"Conexión agregada: {ciudad1} -- {ciudad2} (Peso: {peso if peso is not None else 'N/A'})")
            return True
        else:
            print(f"Conexión entre {ciudad1} y {ciudad2} ya existe. No se hicieron cambios.")
            return False

    def _agregar_arista_simple(self, origen, destino, peso):
        """Función auxiliar para agregar una arista en una sola dirección, evitando duplicados."""
        for vecino, p in self.adj[origen]:
            if vecino == destino:
                return False # La arista ya existe

        self.adj[origen].append((destino, peso))
        return True

    def visualizar_lista_adyacencia(self):
        """Imprime la lista de adyacencia del grafo."""
        print("\n--- Lista de Adyacencia ---")
        if not self.adj:
            print("El grafo está vacío. Agrega ciudades y conexiones primero.")
            return

        for ciudad, conexiones in self.adj.items():
            linea = f"[{ciudad}]: "
            con_str = []
            for vecino, peso in conexiones:
                if peso is not None:
                    con_str.append(f"{vecino} ({peso})")
                else:
                    con_str.append(vecino)
            linea += ", ".join(con_str)
            print(linea)
        print("----------------------------")

    def visualizar_grafo_graphviz(self, nombre_archivo="grafo_ciudades"):
        """Genera y visualiza el grafo usando Graphviz."""
        if not self.adj:
            print("El grafo está vacío. No se puede generar la gráfica.")
            return

        dot = graphviz.Graph(
            'GrafoCiudades',
            comment='Grafo de Conexiones de Ciudades',
            engine='dot',
            graph_attr={'rankdir': 'LR', 'bgcolor': "#BDD2E8"},
            node_attr={'shape': 'circle', 'style': 'filled', 'fillcolor': "#22015a"}
        )
        
        # 1. Agregar nodos
        for ciudad in self.adj.keys():
            dot.node(ciudad)

        # 2. Agregar las aristas
        aristas_agregadas = set()
        for ciudad, conexiones in self.adj.items():
            for vecino, peso in conexiones:
                # Usamos una tupla ordenada para representar la arista no dirigida (A, B) es igual a (B, A)
                arista = tuple(sorted((ciudad, vecino)))
                
                if arista not in aristas_agregadas:
                    label = str(peso) if peso is not None else None
                    # dir='none' indica que es no dirigido
                    dot.edge(ciudad, vecino, label=label, dir='none', color="#101010")
                    aristas_agregadas.add(arista)
        
        # Guardar y renderizar
        output_folder = "graphviz_output"
        os.makedirs(output_folder, exist_ok=True)
        dot_path = os.path.join(output_folder, nombre_archivo)
        
        try:
            # view=True genera el archivo y lo abre automáticamente
            dot.render(dot_path, view=True, format='png')
            print(f"\nGrafo generado con éxito en '{dot_path}.png' y abierto automáticamente.")
        except graphviz.backend.ExecutableNotFound:
            print("\n ERROR: Graphviz no está instalado o no está en el PATH.")
            print("Asegúrate de ejecutar: 'sudo apt install graphviz' y 'pip install graphviz'")
        except Exception as e:
            print(f"\nERROR al generar el grafo: {e}")

# --- FUNCIÓN PRINCIPAL CON MENÚ INTERACTIVO ---

def mostrar_menu():
    """Muestra el menú de opciones."""
    print("\n==================================")
    print("    GESTOR DE GRAFOS - CIUDADES  ")
    print("==================================")
    print("1. Agregar Ciudad (Nodo)")
    print("2. Agregar Conexión (Arista)")
    print("3. Visualizar Lista de Adyacencia")
    print("4. Generar y Visualizar Grafo (Graphviz)")
    print("5. Salir")
    print("==================================")

def main():
    """Lógica principal del menú interactivo."""
    grafo = GrafoCiudades()
    opcion = ''
    
    # ¡SE ELIMINA LA PRECARGA! El grafo comienza vacío.

    while opcion != '5':
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == '1':
            ciudad = input("Ingrese el nombre de la ciudad a agregar: ")
            grafo.agregar_nodo(ciudad)

        elif opcion == '2':
            ciudad1 = input("Ingrese la Ciudad Origen: ")
            ciudad2 = input("Ingrese la Ciudad Destino: ")
            
            peso_str = input("Ingrese el peso (distancia) o déjelo vacío: ").strip()
            peso = None
            if peso_str:
                try:
                    peso = float(peso_str)
                except ValueError:
                    print("Peso inválido. Se usará sin peso.")

            grafo.agregar_conexion(ciudad1, ciudad2, peso)

        elif opcion == '3':
            grafo.visualizar_lista_adyacencia()

        elif opcion == '4':
            nombre = input("Ingrese el nombre para el archivo de reporte (ej: REPORTE): ")
            grafo.visualizar_grafo_graphviz(nombre if nombre else "grafo_ciudades")

        elif opcion == '5':
            print("Saliendo del programa...")

        else:
            print("Opción no válida. Por favor, intente de nuevo.")

# Ejecutar el programa
if __name__ == "__main__":
    main()