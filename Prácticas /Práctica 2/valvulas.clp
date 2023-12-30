
; Plantilla de válvula
(deftemplate válvula
    (slot nombre)
    (slot estado (allowed-symbols abierto cerrado)(default cerrado))
    (slot presion (default 0))
    (slot T1 (default 0)) ; temperatura interna
    (slot T2 (default 0)) ; temperatura externa
)

; Hechos iniciales
( deffacts iniciales
    (válvula (nombre Entrada)(T1 101)(T2 35) (presion 1)) 
    (válvula (nombre Salida) (T1 101) (T2 155) (presion 5)) 
    (válvula (nombre Pasillo1)(T1 99) (T2 37) (estado cerrado))

)

; Reglas de las válvuulas

(defrule R1
    ?v <- (válvula (estado abierto) (presion 5))
    =>
    (modify ?v (estado cerrado)(presion 0))
)

(deffunction calcular_presion (?t1 ?presion)
    (bind ?p ?presion)
    (while (> ?t1 35)
        (bind ?p (+ ?p 1))
        (bind ?t1 (- ?t1 5))
    )
    (return ?p)
)

(defrule R2
    ?v <- (válvula (estado cerrado) (presion ?presion) (T1 ?t1))
    (test (< ?presion 10))
    (test (> ?t1 35))
    =>
    (bind ?p (calcular_presion ?t1 ?presion))
    (modify ?v (estado abierto)(presion ?p))
)

(deffunction decrementar_temp (?t1 ?t2)
    (if (> ?t2 ?t1) then
        (bind ?t2 (- ?t2 ?t1))
    )
)

(defrule R3
    ?v1 <- (válvula (T2 ?t2)(T1 ?t1))
    ?v2 <- (válvula (T2 ?t2)(T1 ?t1a))
    (test (< ?t1a ?t2))
    =>
    (modify ?v2 (T2 (decrementar_temp ?t1 ?t2))(estado abierto))
    (modify ?v1 (estado abierto))
)
