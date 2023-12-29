; Template de usuario
(deftemplate Usuario
    (slot DNI)
    (slot Pin)
    (slot Dinero_extraer)
)
; Template de cuenta
(deftemplate Cuenta
    (slot DNI)
    (slot Saldo)
    (slot estado (allowed-values enPantalla dineroEntregado Inicial SuperaLimite SinSaldo)
        (default Inicial)
    )
)

; Template de tarjeta
(deftemplate Tarjeta
    (slot DNI)
    (slot Pin)
    (slot Num_intentos (default 0))
    (slot Limite_por_dia (default 500))
    (slot estado (allowed-values bloqueada desbloqueada)
        (default desbloqueada)
    )
    (slot Año_expiracion (default 2000))
    (slot Es_Validada (allowed-values si no)
        (default no)
    )
)

; Funciones
; Decrementar un valor en 1
(deffunction decrementar (?valor)
    (- ?valor 1)
)
; Calcular la diferencia entre dos valores
(deffunction diferencia (?valor1 ?valor2)
     (return (- ?valor1 ?valor2))
)

; Paso 1: Validación de la tarjeta

; Regla Supera_Intentos
(defrule Supera_Intentos (declare (salience 100))
    ?tarjeta <- (Tarjeta (Num_intentos ?num_intentos&:(> ?num_intentos 3)))
    =>
    (modify ?tarjeta (estado bloqueada))
    (printout t "La tarjeta ha sido bloqueada por superar el número de intentos" crlf)
)

; Regla Pin_Invalido
(defrule Pin_Invalido (declare (salience 99))
    ?tarjeta <- (Tarjeta (estado desbloqueada) (Es_Validada no)(Pin ?pin1)(DNI ?dni)(Num_intentos ?intentos))
    (Usuario (DNI ?dni) (Pin ?pin2))
    (Cuenta (DNI ?dni))
    (test (neq ?pin1 ?pin2)) ; El pin no coincide
    ; El Pin de la tarjeta debe ser igual a la del usuario
    ; Debe tener una cuenta, tarjeta e usuario con el mismo dni
    =>
    ; Añadimos un intento
    (modify ?tarjeta (Num_intentos (+ 1 ?intentos)))
    (printout t "El pin introducido es incorrecto" crlf)
)

;  Regla Valida_Tarjeta
(defrule Valida_Tarjeta (declare (salience 98))
    ; Validamos pin. El dni y pin debe ser el mismo en tarjeta y usuario
    ?tarjeta <- (Tarjeta (Num_intentos ?intentos) (Año_expiracion ?anno) (Pin ?pin)(DNI ?dni))
    (Usuario (DNI ?dni) (Pin ?pin))
    (Cuenta (DNI ?dni))
    (test (<= ?intentos 3)) ; Validamos intentos
    ; Validamos fecha de expiración
    (test (<= ?anno 2023))
    =>
    (printout t "Tarjeta validada" crlf)
    (modify ?tarjeta (Es_Validada si))
)

; Paso 2: Comprobación de Saldo y Entrega del dinero

; Regla Muestra_Saldo
(defrule Muestra_Saldo (declare (salience 97))
    ; La tarjeta se ha validado
    (Tarjeta (Es_Validada si) (estado desbloqueada) (DNI ?dni))
    ?cuenta <- (Cuenta (DNI ?dni) (Saldo ?saldo) (estado ?estado))
    =>
    ; Se muestra el saldo por pantalla 
    (printout t "El saldo es: " ?saldo crlf)
    ; Se modifica la cuenta a en Pantalla
    (modify ?cuenta (estado enPantalla))
)

; Regla Saldo_NoSuficiente: Si no tiene saldo muestra mensaje en pantalla.
(defrule Saldo_NoSuficiente (declare (salience 96))
    (Tarjeta (Es_Validada si) (estado desbloqueada) (DNI ?dni))
    ?cuenta <- (Cuenta (DNI ?dni) (Saldo ?saldo) (estado ?estado))
    ?user <- (Usuario (DNI ?dni) (Dinero_extraer ?dinero))
    (test (< ?saldo ?dinero))
    =>
    (printout t "No tiene saldo suficiente" crlf)
    (modify ?cuenta (estado SinSaldo))
    (retract ?user)
)

;Regla Comprueba_Limite1: Si supera el límite establecido por el banco muestra mensaje en pantalla.
(defrule Comprueba_Limite1 (declare (salience 95))
    (Tarjeta (Es_Validada si) (DNI ?dni))
    ?cuenta <- (Cuenta (DNI ?dni) (Saldo ?saldo) (estado ?estado))
    ?user <- (Usuario (DNI ?dni) (Dinero_extraer ?dinero))
    (test (> ?dinero 900)) ; El limite de dinero a extraer es de 900 euros
    =>
    (printout t "El límite de extracción por el banco es de 900 euros" crlf)
    (modify ?cuenta (estado SuperaLimite))
    (retract ?user)
)

; Regla Comprueba_Limite2: Si supera el límite establecido por la tarjeta muestra mensaje en pantalla
(defrule Comprueba_Limite2 (declare (salience 94))
    (Tarjeta (Es_Validada si) (DNI ?dni) (Limite_por_dia ?limite))
    ?cuenta <- (Cuenta (DNI ?dni) (Saldo ?saldo) (estado ?estado))
    ?user <- (Usuario (DNI ?dni) (Dinero_extraer ?dinero))
    (test (> ?dinero ?limite))
    =>
    (printout t "El límite de extracción por la tarjeta es de " ?limite " euros" crlf)
    (modify ?cuenta (estado SuperaLimite))
    (retract ?user)
)

; Regla Entrega_Dinero: Muestra mensaje con el nuevo saldo y la cuenta pasa al estado
; DineroEntregado. Si el cajero da el dinero al usuario se almacenará internamente este nuevo saldo.

(defrule Entrega_Dinero (declare (salience 93))
    (Tarjeta (Es_Validada si) (DNI ?dni) (estado desbloqueada))
    ?cuenta <- (Cuenta (DNI ?dni) (Saldo ?saldo) (estado enPantalla))
    ?user <- (Usuario (DNI ?dni) (Dinero_extraer ?dinero))
    (test (>= ?saldo ?dinero))
    => 
    (bind ?nuevo_saldo (diferencia ?saldo ?dinero))
    (modify ?cuenta (estado dineroEntregado) (Saldo ?nuevo_saldo))
    (printout t "El nuevo saldo de la cuenta es de " ?nuevo_saldo " euros" crlf)
    (retract ?user)
)

; Hechos iniciales
(deffacts hechos-iniciales
    (Tarjeta (DNI 123456) (Pin 1212) (Num_intentos 3) (Limite_por_dia 500) (Año_expiracion 2015)) 
    (Tarjeta (DNI 456456) (Pin 4545) (Num_intentos 3) (Limite_por_dia 500) (Año_expiracion 2015))
    (Tarjeta (DNI 000111) (Pin 0011) (Num_intentos 0) (Limite_por_dia 500) (Año_expiracion 2015))
    (Cuenta (DNI 123456) (Saldo 5000)) 
    (Cuenta (DNI 456456) (Saldo 33)) 
    (Cuenta (DNI 000111) (Saldo 30000))
)
