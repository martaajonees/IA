
; Relaciones Norte-Sur 
(deffacts hechos-iniciales
    ; Norte
    (Ubicacion A Norte D)
    (Ubicacion B Norte E)
    (Ubicacion C Norte F)
    (Ubicacion D Norte G)
    (Ubicacion E Norte H)
    (Ubicacion F Norte I)
    ; Oeste
    (Ubicacion A Oeste B)
    (Ubicacion D Oeste E)
    (Ubicacion G Oeste H)
    (Ubicacion B Oeste C)
    (Ubicacion E Oeste F)
    (Ubicacion H Oeste I)
)

; Relaciones sur-este
(defrule sur
    (Ubicacion ?a Norte ?b)
    =>
    (assert(Ubicacion ?b Sur ?a))
)

(defrule este
    (Ubicacion ?a Este ?b)
    =>
    (assert(Ubicacion ?b Oeste ?a))
)

; Relaciones Transistivas
(defrule transistiva
    (Ubicacion ?a ?ubi ?c)
    (Ubicacion ?c ?ubi ?e)
    =>
    (assert(Ubicacion ?a ?ubi ?e))
)

; Relacion noroeste
(defrule noroeste
    (Ubicacion ?a Norte ?b)
    (Ubicacion ?b Oeste ?c)
    =>
    (assert(Ubicacion ?a Noroeste ?c))
)

; Relacion suroeste
(defrule suroeste
    (Ubicacion ?a Sur ?b)
    (Ubicacion ?b Oeste ?c)
    =>
    (assert(Ubicacion ?a Suroeste ?c))
)

; Relacion noreste
(defrule noreste
    (Ubicacion ?a Norte ?b)
    (Ubicacion ?b Este ?c)
    =>
    (assert(Ubicacion ?a Noreste ?c))
)

; Relacion sureste
(defrule sureste
    (Ubicacion ?a Sur ?b)
    (Ubicacion ?b Este ?c)
    =>
    (assert(Ubicacion ?a Sureste ?c))
)

(defrule inicio
    ?f1 <-(situacion ?x ?y)
    (Ubicacion ?x ?u ?y) =>
    (println ?x" esta al " ?u " de " ?y )
    (retract ?f1) 
);; inicio
