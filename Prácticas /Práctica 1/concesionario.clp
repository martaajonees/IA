
; Plantilla de modelos de coches
(deftemplate modelos
    (slot nombre (type STRING))
    (slot precio (type INTEGER) (default 13000))
    (slot maletero (allowed-values grande mediano pequeño) (default grande))
    (slot caballos (type INTEGER) (default 80))
    (slot ABS (allowed-values si no) (default si))
    (slot consumo (default 8))
)

; Plantilla de cuentionario clientes
(deftemplate clientes
    (slot precio (type INTEGER))
    (slot maletero (allowed-values grande mediano pequeño))
    (slot caballos (type INTEGER))
    (slot ABS (allowed-values si no))
    (slot consumo )
)

; Hechos iniciales de los modelos

(deffacts iniciales
    (modelos (nombre "modelo 1")(precio 12000)(maletero pequeño)(caballos 65)(ABS no)(consumo 4,7))
    (modelos (nombre "modelo 2")(precio 12500)(maletero pequeño)(caballos 80)(ABS si)(consumo 4,9))
    (modelos (nombre "modelo 3")(precio 13000)(maletero mediano)(caballos 100)(ABS si)(consumo 7,8))
    (modelos (nombre "modelo 4")(precio 14000)(maletero grande)(caballos 125)(ABS si)(consumo 6,0))
    (modelos (nombre "modelo 5")(precio 15000)(maletero pequeño)(caballos 147)(ABS si)(consumo 8,5))
)

; funcion recomendacion

(defrule recomendacion
    (clientes (precio ?precio1)(maletero ?maletero)(caballos ?caballos1)(ABS ?ABS)(consumo ?consumo1))
    (modelos (nombre ?nombre)(precio ?precio2)(maletero ?maletero)(caballos ?caballos2)(ABS ?ABS)(consumo ?consumo2))
    (test (>= ?precio1 ?precio2))
    (test (>= ?caballos1 ?caballos2))
    (test (>= ?consumo1 ?consumo2))
    =>
    (printout t "El modelo recomendado es: " ?nombre crlf)
)

(defrule norecomendar
    (not (recomendacion))
    =>
    (printout t "No hay recomendación " crlf)
)
