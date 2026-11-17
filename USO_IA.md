Se usa IA para la creación de un archivo "validators.py" el cual valida el rut y luego lo importa hacia models. También se usa para importar uuid a models e incluirlo en el dato "codigo" dentro de el modelo "Reserva", para que dicho campo sea unico y se cree al generar una reserva sin tener que pedirselo al usuario.


Se usa IA para separar el stock del dato "disponibilidad" para que así se pueda quitar un comic si el admin lo ve conveniente sin tener que ajustar el stock en "0" para sacarlo de la pagina web. Ahora los que estan sin stock se muestran como "Agotado".


Se usa IA para generar una barra de busqueda que permita filtrar por titulo de cómic y editorial (o ambas a la vez).


Se usa IA para crear la validación de datos (Email, Rut y control de stock ) Los resultados se muestran desde "reserva.html", cuando el usuario registra sus datos.


Se usa IA para guardar los datos del proyecto en json y hacer un readme con instrucciones de ejecución.