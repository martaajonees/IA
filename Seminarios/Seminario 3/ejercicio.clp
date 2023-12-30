; Plantillas

; Plantilla de Personal

(deftemplate Personal
    (slot Nombre)
    (slot DNI)
    (slot Turno (allowed-values Mañana Tarde Ambas))
    (slot Total_ventas)
    (slot Encargado (allowed-values Si No))
)

; Plantilla de Producto
(deftemplate Producto
    (slot Identificador)
    (slot Nombre)
    (slot StockCafeteria )
    (slot StockAlmacen)
    (slot Precio)
    (slot MaximoStock (default 30))
)

; Plantilla de Venta
(deftemplate Venta 
    (slot DNI) ; que camarero ha realizado la venta
    (slot Identificador) ; que producto se ha vendido
    (slot Unidades) ; cuantas unidades se han vendido por producto
    (slot Metodo_pago (allowed-values Efectivo Tarjeta Bono))
)

; Reglas
; Asignamos pedido de un cliente a un camarero
(defrule AsignarVenta (declare (salience 10))
    ?v <- (Venta (DNI ?dni) (Identificador ?id)(Unidades ?unidades)(Metodo_pago ?metodo))
    ?pers <- (Personal (DNI ?dni) (Total_ventas ?ventas)(Nombre ?nombre))
    ?prod <- (Producto (Identificador ?id)(Nombre ?nombre2) (Precio ?precio) (StockCafeteria ?stockcafeteria))
    ; Que haya stock suficiente en la cafeteria
    (test (<= ?unidades ?stockcafeteria))
    =>
    ; Precio total de la venta
    (bind ?precio_total (* ?precio ?unidades))
    ; Incrementar acumulador de ventas
    (modify ?pers (Total_ventas (+ ?precio_total ?ventas)))
    ; Decremento stock de la cafeteria
    (modify ?prod (StockCafeteria (- ?stockcafeteria ?unidades)))
    
    ; Imprimo
    (println ?nombre ": " ?unidades" de " ?nombre2 ", " ?precio_total "€ pagados con " ?metodo)
    (println ?nombre " acumula un total de " ?ventas "€ en la jornada de hoy")
    (retract ?v)
)
; funcion Reponer
(deffunction Reposicion (?almacen ?maximo)
    (if (> ?maximo ?almacen)
        then
            (return (- ?maximo ?almacen))
        else
            (return ?maximo)
    )
)
; Regla ReponerStock

(defrule ReponerStock (declare (salience 1))
    ?prod <- (Producto (StockCafeteria ?stockcafeteria) (StockAlmacen ?stockalmacen)(MaximoStock ?max))
    (test (< ?stockcafeteria 10))
    =>
    (modify ?prod (StockCafeteria (Reposicion ?stockalmacen ?max)))
) 

; Hechos iniciales

(deffacts hechos-iniciales
    (Producto (Identificador cafe) (Nombre "Café") (StockCafeteria 32) (StockAlmacen 400) (Precio 0.95) (MaximoStock 60))
    (Personal (Nombre "María") (DNI 11) (Turno Mañana) (Total_ventas 45) (Encargado Si))
    (Venta (DNI 11) (Identificador cafe) (Unidades 5) (Metodo_pago Efectivo))
)
