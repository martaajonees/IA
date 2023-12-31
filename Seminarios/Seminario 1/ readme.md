# Mamíferos y Aves
## Clasificación de Animales
Supóngase la siguiente Base de Reglas:

- R1: Si un animal tiene pelo, entonces es mamífero
- R2: Si un animal da leche, entonces es mamífero
- R3: Si un animal tiene plumas es un ave
- R4: Si un animal vuela y pone huevos, es ave
- R5: Si un animal come carne, es carnívoro
- R6: Si un animal tiene dientes puntiagudos, tiene garras, tiene ojos al frente es carnívoro
- R7: Si un animal mamífero tiene pezuñas es una ungulado
- R8: Si un animal mamífero rumia es un ungulado
- R9: Si un animal mamífero y carnívoro tiene color leonado con manchas oscuras se trata de un leopardo
- R10: Si un animal mamífero y carnívoro tiene color leonado con rayas negras es un tigre
- R11: Si un animal ungulado con cuello largo y piernas largas tienen manchas oscuras es una jirafa
- R12: Si un animal es un ungulado con rayas negras es una cebra
- R13: Si un animal es ave y no vuela y tiene el cuello largo y piernas largas de color blanco y negro es un avestruz
- R14: Si un animal es ave, no vuela, nada, de color blanco y negro, se trata de un pingüino
- R15: Si es un ave que vuela bien y come pescado, es un albatros
- R16: Si un animal es de una especie y ese animal es padre de otro, entonces el hijo es de la misma especie.

Y la siguiente base de hechos:

Robi y Susi son dos animales. Robi con pelo y color leonado y rayas negras, mientras que Susi tiene plumas y es de color blanco. A diferencia de Robi que no vuela, Susi vuela bien. 
Además Robi come carne y Susi pescado.

1. ¿Qué hechos pueden deducirse? Realiza una traza de la ejecución de este sistema con los hechos dados usando Encadenamiento hacia delante. Indica en cada paso cómo se va actualizando la base de hechos y la agenda.
2. Implementa en CLIPS este sistema y comprueba los resultados de la traza realizada en el apartado anterior.
3. Inventa nuevos hechos para probar el sistema, por ejemplo Fifi tiene el cuello largo y manchas oscuras y es la madre de Fofo.
