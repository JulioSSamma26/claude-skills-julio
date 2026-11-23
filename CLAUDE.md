# Instrucciones para Claude

## Zona horaria
- Julio está en America/Bogota (UTC−5, sin horario de verano). El contenedor en la nube y la fecha de "hoy" que recibe Claude pueden venir en UTC.
- Antes de programar, fechar o decir "hoy", "mañana" u otra hora, convierte a America/Bogota (por ejemplo, `TZ=America/Bogota date`). Entre las 7:00 p. m. y la medianoche de Colombia, UTC ya va un día adelante.
- En recordatorios y tareas programadas, escribe la hora local con la zona: `2026-11-23T10:00:00[America/Bogota]`.
