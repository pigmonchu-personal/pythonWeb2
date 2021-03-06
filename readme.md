# Puesta en marcha del sistema

## Creación de al menos una categoría

Debe crearse al menos una categoría para los posts con el administrador de django. En otro caso será imposible dar de alta un post, puesto que el campo categoría es obligado.

La validación de tipos de ficheros para subir implica utilizar la librería `python-magic` y esta tiene ciertas dependencias en función del sistema operativo en que se instale, ver [https://github.com/ahupp/python-magic#dependencies](https://github.com/ahupp/python-magic#dependencies). En mi caso he instalado libmagic con homebrew

## Gestión de colas y worker

Como worker la aplicación utiliza `celery`. Para arrancarlo ejecutar desde una terminal.

```

celery -A dTBackend worker


```

Previamente ha de haberse levantado un gestor de colas. En mi caso he usado `Rabbit MQ`. **No figura en el repositorio**.


## Tipos de attachment admitidos para un post

La api de upload de imágenes y videos sólo admitirá este tipo de ficheros. Se admitirán **videos** de tipo  

	- WebM, 
	- Ogg, 
	- MP4, 

Las **imágenes** admitidas serán

	- JPEG, 
	- GIF, 
	- PNG, 
	- APNG, 
	- SVG, 
	- BMP, 

La relación de extensiones con formato de fichero la he tomado de [https://www.sitepoint.com/web-foundations/mime-types-complete-list/](https://www.sitepoint.com/web-foundations/mime-types-complete-list/)



# Notas para el profesor - 

## Internacionalización - [Backend avanzado]
Se ha internacionalizado la web de forma que puede utilizar ingles y español. Por defecto es inglés.

La traducción de las etiquetas de los campos de los formularios se ha complicado un poco. Si la hago directamente al definir el formulario queda siempre en inglés, ya que la definición de los formularios se realiza al lanzar la aplicación y no existe un request con una cabecera `Accept-Language` para extraer el idioma de la petición.

He creado una clase `TranslateView(View)` en la aplicación `ui`. En ella he definido un método `translate` que recorre todas las labels del formulario en el momento de la petición y las traduce.

**El problema viene** a la hora de generar los ficheros .po, las claves hay que ponerlas a mano o forzando una primera traducción al declarar el objeto labels de cada vista. Además quedan comentadas en cada nueva generación de cadenas a traducir. Es incómodo pero no tengo tiempo, por ahora, para desarrollar una solución más elegante.

## API subida imágenes y procesado responsive

Lo he hecho de manera sencilla y sin microservicios. Usando Rabbit MQ y Celery. La idea es hacerlo así.

1.	Subir un post en el que se indica el texto alternativo de la imagen (no necesario en el caso de un video). Si todo va bien se obtiene el id del post
2. Subir via [nueva api](#media-upload) el fichero. Importante informar los parámetros correctamente en la url, el body (binary) y la cabecera. 

[Soy capaz de hacerlo vía postman... estoy pendiente de hacerlo vía javascript.]

## Notas a los requisitos - [Fundamentos de Python]

1. Al hacer signup, el usuario no queda logueado al sistema porque creo que es mejor  montar el ciclo de validación de correo. No lo construyo, pero obligo al usuario a loguearse manualmente al sistema como recordatorio/simulación de que queda pendiente la validación del correo.
2. Al comenzar me pareció una buena idea montar el sistema de forma que un usuario pueda tener más de un blog (si yo fuera un usuario me gustaría tener dos distintos). Me ha ido dando problemas pero los he ido solventado. Sin embargo he tenido que tomar ciertas decisiones que no sé si van en contra de los requisitos.
	- **API de posts**: _"Un endpoint para crear posts en el cual el usuario deberá estar autenticado. En este endpoint el post quedará **publicado** automáticamente en el blog del usuario autenticado"_
		- Puesto que un usuario puede tener más de un blog. El blog al que va el post debe informarse como parámetro de entrada. La asignación no puede ser automática, pero si que se valida. Un usuario, incluso el adm, sólo puede asignar post a sus propios blogs, lo que obliga a matizar el endpoint de actualización de post (ver más abajo).
		- Este requisito queda entonces como que la publicación será automática si no se informa date_pub y que el post será no público mientras `date_pub > ahora`.
	- **API de posts**: _"Un endpoint de actualización de un post. Sólo podrá acceder al mismo el dueño del post o un administrador."_ **Le añado lo siguiente por compatibilidad con varios blogs:** _El usuario **dueño podrá modificar todo el post**, incluso asignar el post a cualquiera de sus blogs. El usuario **administrador podrá solamente modificar la fecha de publicación y las categorías**. Así podrá vetar su publicación (mientras pide al usuario que lo corrija), e incluso borrarlo (imaginemos que se ha saltado repetidamente la política del sitio). También podrá cambiar su clasificación por categorías, pero nunca podrá censurarlo o modificar su contenido."_
		
3. El usuario administrador, si quiere publicar, tiene que dar de alta su propio blog en el administrador de django. Se ha habilidado una direccion en el sitio web para ello `/new-blog`.

4. La api de blogs tiene dos variantes. v0.1 que es la primera que hice para entender como iba el tema de los serializers y las apis y v1.0 basada en ModelViewSet. Son ligeramente diferentes. 

# Uso de la API

## API de usuarios

### POST /api/1.0/users/

**Requisito**: _"Endpoint que permita a cualquier usuario registrarse indicando su nombre, apellidos, nombre de usuario, e-mail y contraseña."_

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **username** | body | identificador del usuario (debe ser único) | Si | string 
 **email** | body | correo electrónico del usuario | Si | string 
 **password** | body | Contraseña del usuario.| Si | string 
 **first_name** | body | Nombre del usuario.| No | string
 **last_name** | body | Apellidos del usuario| No | string
 
### GET /api/1.0/users/{id}/

**Requisito**: _"Endpoint que permita ver el detalle de un usuario. Sólo podrán ver el endpoint de detalle de un usuario el propio usuario o un administrador."_

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **id** | url | identificador único de usuario | Si | number 
 
### PUT /api/1.0/users/{id}/

**Requisito**: _"Endpoint que permita actualizar los datos de un usuario. Sólo podrán usar el endpoint de un usuario el propio usuario o un administrador."_

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **username** | body | identificador del usuario (debe ser único) | Si | string 
 **email** | body | correo electrónico del usuario | Si | string 
 **password** | body | Contraseña del usuario.| Si | string 
 **first_name** | body | Nombre del usuario.| No | string
 **last_name** | body | Apellidos del usuario| No | string
 
### DELETE /api/1.0/users/{id}/

**Requisito**: _"Endpoint que permita eliminar un usuario (para darse de baja). Sólo podrán usar el endpoint de un usuario el propio usuario o un administrador."_

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **id** | url | identificador único de usuario | Si | number 
 
### GET /api/1.0/blogs/

**Requisito**: _"Un endpoint que no requiera autenticación y devuelva el listado de blogs que hay en la plataforma con la URL de cada uno. Este endpoint debe permitir buscar blogs por el nombre del usuario y ordenarlos por nombre."_

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **search** | query | Permite buscar los blogs de un usuario determinado. Busca la cadena en el nombre del usuario propietario del blog | No | string
 **ordering** | query | ordenación por los siguientes campos `name, description, owner, id`. Se pueden utilizar varios de ellos separándolos por un espacio en blanco. Si el orden es decreciente se pone el signo - delante del campo a ordenar.  | No | string 
 
## API de posts

### GET /api/1.0/posts/

**Requisito**: _"Un endpoint para poder leer los artículos de un blog de manera que, si el usuario no está autenticado, mostrará sólo los artículos publicados. Si el usuario está autenticado y es el propietario del blog o un administrador, podrá ver todos los artículos (publicados o no). En este endpoint se deberá mostrar únicamente el título del post, la imagen, el resumen y la fecha de publicación. Este endpoint debe permitir buscar posts por título o contenido y ordenarlos por título o fecha de publicación. Por defecto los posts deberán venir ordenados por fecha de publicación descendente."_

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **search** | query | Permite buscar los post que contengan el texto en los campos `title, body, abstract`. | No | string
 **ordering** | query | ordenación por los siguientes campos `title, date_pub`. Se pueden utilizar varios de ellos separándolos por un espacio en blanco. Si el orden es decreciente se pone el signo - delante del campo a ordenar. | No | string

### POST /api/1.0/posts/

**Requisito**: _"Un endpoint para crear posts en el cual el usuario deberá estar autenticado. En este endpoint el post quedará publicado automáticamente en el blog del usuario autenticado."_

Se ha modificado la API para poder subir ficheros. Se impide que se informe el attachment aquí, sin embargo si que se informa la descripción de la imagen (opcional)

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **title** | body | Título del post | Si | string
 **abstract** | body | Resumen del post. | Si | string
 **body** | body | Texto del post. | Si | string
 **categories** | body | Array de identificadores de las categorías del post. | Si | string
 ~~**attachment**~~ | ~~body~~ | ~~Url del foto o video principal del post~~ | ~~No~~ | ~~string (url)~~
 **attachment_description** | body | Descripción de la imagen para el campo alt | No | string 
 **blog** | body | identificador del blog al que pertenece el post. | Si | number
 **date_pub** | body | Fecha y hora de publicación | Si | string (date 'YYYY-MM-DDTHH:MM:SSZ')
 
 
<a name="media-upload"> ### PUT /api/1.0/media/{id_post}</a>

**Requisito**: _"...se desea habilitar la posibilidad de subir imágenes a través de un endpoint del API y que, automáticamente el sistema se encargue de generar las versiones responsive de las imágenes así como un thumbnail de la imagen como tamaño máximo. Sólo podrá hacerlo el dueño del post"_

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **Content-Disposition** | Header | Indica que se va a subir un fichero | Si | attachment; filename=...
 **file** | body | Fichero de los tipos indicados más arriga | Si | File
 **id_post** | url | Identificador del post. | Si | number
 
El nombre con el que se guardará el documento en el servidor será el que se le indique en Content-Disposition. El campo file del body de la petición sólo contiene la información binaria del fichero, no su nombre.


### GET /api/1.0/posts/{id}

**Requisito**: _"Un endpoint de detalle de un post, en el cual se mostrará toda la información del POST. Si el post no es público, sólo podrá acceder al mismo el dueño del post o un administrador."_

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **id** | url | Identificador del post. | Si | number
 

### PUT /api/1.0/posts/{id}/

**Requisito**: _"Un endpoint de actualización de un post. Sólo podrá acceder al mismo el dueño del post o un administrador."_

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **id** | url | Identificador del post. | Si | number
 **title** | body | Título del post | Si | string
 **abstract** | body | Resumen del post. | Si | string
 **body** | body | Texto del post. | Si | string
 **categories** | body | Array de identificadores de las categorías del post. | Si | string
 ~~**attachment**~~ | ~~body~~ | ~~Url del foto o video principal del post~~ | ~~No~~ | ~~string (url)~~
 **attachment_description** | body | Descripción de la imagen para el campo alt | No | string (url)
 **blog** | body | identificador del blog al que pertenece el post. | Si | number
 **date_pub** | body | Fecha y hora de publicación | Si | string (date 'YYYY-MM-DDTHH:MM:SSZ')
 

### DELETE /api/1.0/posts/{id}

**Requisito**: _"Un endpoint de borrado de un post. Sólo podrá acceder al mismo el dueño del post o un administrador."_

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **id** | url | Identificador del post. | Si | number
 
 
# Pruebas API anteriores
 
## API de blogs

### GET /api/0.1/blogs/

**Requisito**: _"Un endpoint que no requiera autenticación y devuelva el listado de blogs que hay en la plataforma con la URL de cada uno. Este endpoint debe permitir buscar blogs por el nombre del usuario y ordenarlos por nombre."_

**Nota**: Este end-point se hizo antes de aprender a manejar ModelViewSets

### Parámetros

 *Parámetro* | *En* | *Descripción* | *Obligatorio* | *Schema* 
 :------ | :---------- | :----------- | :----------- | :------ 
 **owner** | query | nombre de usuario. Permite buscar los blogs de un usuario determinado  | No | string
 **ordering** | query | ordenación por los siguientes campos `name, description, owner, id`. Se pueden utilizar varios de ellos separándolos por un espacio en blanco. Si el orden es decreciente se pone el signo - delante del campo a ordenar.  | No | string 
 

