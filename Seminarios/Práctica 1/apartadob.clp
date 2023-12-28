(deftemplate animal
    (slot nombre)
    (slot especie)
    (slot tiene-pelo (default no))
    (slot da-leche (default no))
    (slot tiene-plumas (default no))
    (slot vuela (default no))
    (slot nada (default no))
    (slot come (default no))
    (slot es-carnivoro (default no))
    (slot dientes-puntiagudos (default no))
    (slot garras (default no))
    (slot ojos-al-frente (default no))
    (slot pone-huevos (default no))
    (slot tiene-pezuñas (default no))
    (slot es-ungulado (default no))
    (slot color (default no))
    (slot rumia (default no))
    (slot cuello-largo (default no))
    (slot rayas-negras (default no))
    (slot manchas-oscuras (default no))
    (slot piernas-largas (default no))
)

(deffacts hechos-iniciales
    (animal (nombre "Robi") (tiene-pelo si) (color leonado) (rayas-negras si) (vuela no) (come carne))
    (animal (nombre "Susi") (tiene-plumas si) (color blanco) (vuela bien) (come pescado))
)

(defrule regla1
    ?an <- (animal (nombre ?nombre) (tiene-pelo si))
    =>
    (modify ?an (especie mamifero))
)  

(defrule regla2
    ?an <- (animal (nombre ?nombre) (da-leche si))
    =>
    (modify ?an  (especie mamifero))
)

(defrule regla3
    ?an <- (animal (nombre ?nombre) (tiene-plumas si))
    =>
    (modify ?an (especie ave))
)

(defrule regla4
    ?an <- (animal (nombre ?nombre) (vuela si)(pone-huevos si))
    =>
    (modify ?an (especie ave))
)

(defrule regla5
    ?an <- (animal (nombre ?nombre)(come carne))
    =>
    (modify ?an (es-carnivoro si))
)

(defrule regla6
    ?an <- (animal (nombre ?nombre) (dientes-puntiagudos si) (garras si) (ojos-al-frente si))
    =>
    (modify ?an (es-carnivoro si))
)

(defrule regla7
    ?an <- (animal (nombre ?nombre) (especie mamifero) (tiene-pezuñas si))
    =>
    (modify ?an (es-ungulado si))
)

(defrule regla8
    ?an <- (animal (nombre ?nombre) (especie mamifero) (rumia si))
    =>
    (modify ?an (es-ungulado si))
)

(defrule regla9
    (animal (nombre ?nombre) (especie mamifero)(es-carnivoro si)(color leonado)(manchas-oscuras si))
    =>
    (printout t ?nombre " es un leopardo " crlf)
)

(defrule regla10
    (animal (nombre ?nombre) (especie mamifero)(es-carnivoro si)(color leonado)(rayas-negras si))
    =>
    (printout t ?nombre " es un tigre " crlf)
)

(defrule regla11
    (animal (nombre ?nombre) (es-ungulado si) (cuello-largo si) (piernas-largas si) (manchas-oscuras si))
    =>
    (printout t ?nombre " es una jirafa " crlf)
)

(defrule regla12
    (animal (nombre ?nombre) (es-ungulado si) (rayas-negras si))
    =>
    (printout t ?nombre " es una cebra " crlf)
)

(defrule regla13
    (animal (nombre ?nombre) (especie ave)(vuela no)(cuello-largo si)(piernas-largas si)(color blanco-negro))
    =>
    (printout t ?nombre " es una avestruz " crlf)
)

(defrule regla14
    (animal (nombre ?nombre) (especie ave)(vuela no)(nada si)(color blanco-negro))
    =>
   (printout t ?nombre " es un pingüino " crlf)
)

(defrule regla15
    (animal (nombre ?nombre) (vuela bien)(come pescado))
    =>
    (printout t ?nombre " es un albatros " crlf)
)

(defrule regla16
    (especie ?padre)
    (padre-de ?hijo)
    =>
    (assert (especie ?hijo ?padre))
)
