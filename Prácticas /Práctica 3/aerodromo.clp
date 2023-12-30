
; Plantillas

(deftemplate Aeronave
    (slot id)
    (slot compañia)
    (slot origen) ; aerodromo de origen
    (slot destino) ; aerodromo de destino
    (slot velocidad_actual)
    (slot peticion (allowed-values Ninguna Aterrizaje Despegue Emergencia Rumbo))
    (slot estado (allowed-values enTierra Ascenso Descenso Crucero) (default enTierra))
)

(deftemplate Aerodromo
    (slot id)
    (slot ciudad)
    (slot radar (allowed-values ON OFF))
    (slot radio_visibilidad)
    (slot velocidad_viento)
)

(deftemplate Piloto
    (slot aeronave)
    (slot vuelo) 
    (slot accion (allowed-values OK SOS Ejecutando Stand-by) (default Stand-by))
)

(deftemplate Vuelo
    (slot aerodromo1) ; id
    (slot aerodromo2) ; id
    (slot distancia)
    (slot velocidad_despegue (default 240))
    (slot velocidad_crucero (default 700))
)

; Reglas
(defrule Despegar
    ?avion <- (Aeronave (id ?id)(compañia ?comp)(origen ?or)(destino ?dest)(estado enTierra) (peticion Despegue))
    ?pil <- (Piloto (accion OK))
    (Aerodromo (id ?id1)(ciudad ?ciudad)(radar ON)(radio_visibilidad ?rv)(velocidad_viento ?vv))
    (test (> ?rv 5))
    (test (< ?vv 75))
    (Vuelo (aerodromo1 ?or)(aerodromo2 ?dest)(velocidad_despegue ?vd))
    =>
    (modify ?pil (accion Ejecutando))
    (modify ?avion (estado Ascenso)(velocidad_actual ?vd)(peticion Ninguna))
    (println "La aeronave " ?id " de la compañía " ?comp " va a realizar la acción despegue desde el aeródromo " ?id1 " de " ?ciudad " con destino " ?dest)
)

(defrule Excepcion
    ?avion <- (Aeronave (id ?id) (peticion Despegue)(compañia ?comp)(origen ?or)(destino ?dest))
    (Piloto (aeronave ?id)(accion ?estado))
    (test (neq ?estado OK))
    =>
    (modify ?avion (peticion Emergencia))
    (println "ATENCION El piloto de la aeronave " ?id " de la compañía " ?comp "no se encuentra disponible para iniciar el despegue desde el aerodromo "?or " con destino " ?dest)
)

(deffunction calcular-tiempo-horas (?distancia ?velocidad)
    (bind ?hora (div ?distancia ?velocidad))
    (return ?hora)
)

(deffunction calcular-tiempo-minutos (?distancia ?velocidad)
    (bind ?residuo (mod ?distancia ?velocidad))
    (bind ?horas (div  ?residuo ?velocidad))
    (bind ?minutos (* ?distancia 60))
    (return ?minutos)
)


(defrule Crucero 
    ?avion <- (Aeronave (id ?id)(estado Ascenso)(origen ?or)(destino ?dest)(velocidad_actual ?va))
    (Aerodromo (ciudad ?or) (id ?idor)) ; Aerodromo de origen
    (Aerodromo (ciudad ?dest) (id ?iddest)) ; Aerodromo de destino
    (Vuelo (velocidad_crucero ?vc)(aerodromo1 ?idor)(aerodromo2 ?iddest)(distancia ?dist))
    ?pil <- (Piloto (aeronave ?id)(accion Ejecutando))
    =>
    (modify ?avion (estado Crucero)(velocidad_actual ?vc))
    (println "El despegue ha sido correcto. El vuelo realizará desde " ?or " con destino " ?dest " con un tiempo estimado de " (calcular-tiempo-horas ?dist ?vc) " horas y "(calcular-tiempo-minutos ?dist ?vc)" minutos")
    (modify ?pil (accion Stand-by))
)
