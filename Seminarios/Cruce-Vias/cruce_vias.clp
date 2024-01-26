
; Plantillas

(deftemplate Via
    (slot idVia)
    (slot nombreVia)
    (slot numVehiculos (default 0))
)

(deftemplate Semaforo
    (slot idSemaforo)
    (slot idVia)
    (slot estado (allowed-values Rojo Verde))
    (slot numVehiculos (default 0))
)

(deftemplate Sensor
    (slot idCelula (allowed-values 1 2 3))
    (slot idSemaforo)
    (slot estado (allowed-values activado desactivado)(default desactivado))
    (slot matricula)
)

(deftemplate Vehiculo
    (slot matricula)
    (slot tipo (allowed-values automovil motocicleta bicicleta))
    (slot idSemaforo)
    (slot accion (allowed-values llegando esperando cruzando realizando nada) (default nada))
)

; Hechos iniciales

(deffacts hechos-iniciales
    ; Vias
    (Via (idVia V1) (nombreVia "Avenida Constitución"))
    (Via (idVia V2) (nombreVia "Avenida Falla"))
    ; Semáforos
    (Semaforo (idSemaforo A)(idVia V2)(estado Verde))
    (Semaforo (idSemaforo B)(idVia V2)(estado Rojo))
    (Semaforo (idSemaforo C)(idVia V1)(estado Rojo))
    (Semaforo (idSemaforo D)(idVia V2)(estado Verde))
    ; Sensores del semaforo A
    (Sensor (idCelula 1)(idSemaforo A))
    (Sensor (idCelula 2)(idSemaforo A))
    (Sensor (idCelula 3)(idSemaforo A))
)

; Reglas

(defrule llegando-vehiculo ; Activar sensor del tipo 1
    ; Un vehiculo entra en la via
    ?f <- (activar_sensor ?idC ?idS ?matricula ?tipo)
    ; Datos 
    ?sensor <- (Sensor (idCelula ?idC)(idSemaforo ?idS))
    (test (eq ?idC 1))
    ?sem <- (Semaforo (idSemaforo ?idS)(idVia ?idV)(numVehiculos ?num))
    (Via (idVia ?idV)(nombreVia ?nombreVia))
    
    =>
    ; Crear un hecho del vehiculo que nos hemos encontrado
    (assert (Vehiculo (matricula ?matricula)(idSemaforo ?idS)(tipo ?tipo)(accion llegando)))
    (println "El vehículo está llegando al semáforo" )
    (modify ?sensor (estado activado) (matricula ?matricula))
    ;(modify ?sem (numVehiculos (+ 1 ?num)))
    (println "El sensor 1 acaba de ser activado por el/la " ?tipo " con matricula " ?matricula " en la via " ?nombreVia)
    (retract ?f)
)

; activar con (assert (activar_sensor 1 A 1234ABC automovil))

(defrule cambio-Rojo
    ; Lo activa el hecho
    ?f <- (cambia-color ?sem ?color)
    (test (eq ?color Rojo))
    ; Datos
    ?semaforo <- (Semaforo (idSemaforo ?sem)(numVehiculos ?num)(idVia ?idV))
    ?via <- (Via (idVia ?idV)(numVehiculos ?numV))

    => 
    (modify ?via (numVehiculos (+ ?numV ?num))) ; se le suma lo del semaforo
    (modify ?semaforo (estado Rojo)(numVehiculos 0)) ; se pone a 0
)

; activar con (assert (cambia-color A Rojo))

(defrule cruzando
    ?sem <- (Semaforo (idSemaforo ?idS)(estado Verde)(idVia ?v)(numVehiculos ?num))
    ?via1 <- (Via (idVia ?v)(nombreVia ?nombreVia))
    ?via2 <- (Via (idVia ?v2)(nombreVia ?nombreVia2))
    ?vehiculo <- (Vehiculo (idSemaforo ?idS)(accion ?accion)(tipo ?tipo)(matricula ?matricula))
    (test (or (eq ?accion llegando) (eq ?accion esperando)))
    (test (neq ?v ?v2))
    =>
    (modify ?vehiculo (accion cruzando))
    (modify ?sem (numVehiculos (+ ?num 1)))
    (println "El/la " ?tipo " con matricula " ?matricula " está cruzando la vía " ?nombreVia " con la vía " ?nombreVia2)
)

(defrule situacion
    (situacion semaforos) ; hecho que activa la regla
    ?semA <- (Semaforo (idSemaforo A)(estado ?estadoA))
    ?semB <- (Semaforo (idSemaforo B)(estado ?estadoB))
    ?semC <- (Semaforo (idSemaforo C)(estado ?estadoC))
    ?semD <- (Semaforo (idSemaforo D)(estado ?estadoD))
    ?via1 <- (Via (idVia V1)(nombreVia ?nombreVia1)(numVehiculos ?numV1))
    ?via2 <- (Via (idVia V2)(nombreVia ?nombreVia2)(numVehiculos ?numV2))
    =>
    (println "Semaforos A y B ( estados " ?estadoA " y " ?estadoB ") han pasado " ?numV2 " vehiculos por la via " ?nombreVia1)
    (println "Semaforos C y D ( estados " ?estadoC " y " ?estadoD ") han pasado " ?numV1 " vehiculos por la via " ?nombreVia2)
)
