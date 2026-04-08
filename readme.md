hacer demonios, y validar para que pase lo que pase, el demonio exista 
que aguante , reinicios, que forme parte de sistema 


Hacer la migracion de la db (acoplar a la tabla original)

esperar la reunion para restructurar el codigo y adaptarlo



Para acceder al entorno virtual del flask


````

source .venv/bin/activate


````


Para salir del env del flask


````

deactivate

````


Luego levantar el listener y esperar la llegada de valores 


#### Detalle de lo enviado
Te lo estoy enviando en formato float32 (IEEE754) en 2 registros Modbus.
El orden es normal, sin word swap: primero high word y luego low word.
No estoy aplicando byte swap.



#### Pruebas locales 
Por el momento se estan realizando pruebas locales controladas en una red interna de la empresa dcs 

##### Prueba desde el postgresql 

Primero accedo a la terminal con los acceso de la db local
La db es: webhook_db , el password es el de mi local

```

 psql -U postgres -d webhook_db

```

y luego ejecuto el script, 
a considerar que , la db ya tiene la funcion que manda toda la info 

y a la par debe estar ejecutando el codigo del listener, que lo que hace es escuchar y mandar por el protocolo modbus 

```

 psql -U postgres -d webhook_db

```

Para ingresa valores a la db y que el listener los encuentre

```

INSERT INTO items (name, value)
VALUES ('prueba', 12.34);

```


