Este archivo ayuda a:
(0) Obtener una recomendacion general. 
(i) Navegar a traves del archivo Lulo_Bank_Prueba_VF.ipynb, y 
(ii) Ejecuetar el archivo tv_series_db.py
(iii) Reconocer la lista de carpetas y archivos entregados.
(iv) Informacion de contacto del autor

(0) Se recomienda descargar todas los carpetas asociadas a este proyecto y ejecutar exclusivamente los archivos 
    Lulo_Bank_Prueba_VF.ipynb y tv_series_db.py en Visual Studio Code. Los archivos (.csv) que se generen durante la 
    ejecucion de Lulo_Bank_Prueba_VF.ipynb y tv_series_db.py se guardan en la carpeta donde se encuentren 
    (src/ y model/ respectivamente; revisar seccion (iii) del presente archivo README).

(i) Lulo_Bank_PRueba_VF.ipynb: Tiene 6 secciones
    (0) Importe de librerias
    (1) Extracción de datos desde una API
    (2) Revisión general de los datos extraidos
    (3) Creación y revisión de DataFrames
    (4) DFs Celaning y Profiling
    (5) DFs a SQLite
    (6) ETL

    A continuacion se profundiza un poco en cada sección. 
    Se recomienda usar VisualStudio Code para abrir el archivo Lulo_Bank_Prueba_VF.ipynb

    (0) Importe de librerias: 
        Aquí se importaron las librerías necesarias para extraer, transformar,
        analizar y cargar los datos de salida. 
        Entre las librerías más importantes están: pandas, numpy, matplotlib, requests, json, seaborn y sqlite3.
    
    (1) Extracción de datos desde API: 
        La extracción de los datos de la API se realizó por medio de 3 for loops, que ayudaron a transformar los datos
        desde una API (url) a dataframe (pasando por text, json y list).

    (2) Revisión general de los datos extraidos:
        Aquí se revisó si los datos eran homogéneos es decir que cada día se registraban la misma cantidad de variables (columnas),
        y la misma cantidad de registros (filas). 
        Se identificó que no todos los días se registran la misma cantidad de datos y no todos los días se ingresan la misma cantidad de variables. 
        Los datos siguen un comportamiento periódico (semanal), empezando en los valores mas bajos los dias Sabados y Domingos. Luego se aumenta el numero
        de registros durante la semana y finalmente el valor mas alto de registros se obtienen los días Viernes.
        
        Tambien se reviso de manera general que tipos de variables existian y si cauntos registros no nulos tenian. 
        Se identificaron 12 variables principales (id, url, name, season, number, type, airdate, airtime, airstamp, runtime, image y summary) y 
        50 variables complementarias (en su gran mayoria embedded o incorporadas en el data set).

        Se identifico que en las variables incorporadas como 'ratings' es donde están la gran mayoría de datos faltantes en el data set. 
        Las 12 variables principales tienen baja cantidad de nulo oscilando entre un 2% y 15% (en el peor de los casos).  

        Con base en la información entregada sobre el ouput de interes, se definieron los DFs a formar y extraer. 
       
    
    (3) Creación y revisión de DataFrames
        Con base en como están los datos obtenidos de la API (filas y columnas), el número de datos faltantes por cada variable 
        registrada durante el periodo analizado (Diciembre 2020), y las variables de interés por parte del cliente se definió crear
        5 diferentes Dataframes que contienen la información más relevante para el cliente:
        
        (3.1) Air Basic DF: Variables de interes ['id','type','airdate','url']
        
        (3.2) Genre-Status DF: Variables de interes ['id','_embedded.show.genres','_embedded.show.status','_embedded.show.premiered']
        
        (3.3) Country DF: Variables de interes ['id','_embedded.show.webChannel.country.name', '_embedded.show.webChannel.country.code']

        (3.4) Runtime DF: Variables de interes ['id','runtime','_embedded.show.averageRuntime']
        
        (3.5) Ratings DF: ['id','rating.average','_embedded.show.rating.average']

        Cada uno de estas secciones esta compuesta por 4 subsecciones:
        (3.x.0) Compilacion del DF: Aqui se seleccionaron las variables de interes y se concateno la lista para obtener un dataframe usando pd.concat().
        
        (3.x.1) Revision basica del DF: Aqui se utilizo .info() para darle una vista rapida a los componentes del nuevo DF formado,
                al igual que .value_counts() para revisar que tipo de respuesta se tenian por variable y que tanto se repetian.
        
        (3.x.2) Mejoras del DF: Aqui se agregaron (.insert()) nuevas columnas al DF para identificar a que serie de tv pertenecia exactamente el episodio que se describia 
                utilizando un for loop y funciones como count() y find(), utiles para ayer caracteres de interes dentro de un string. Adicionalmente se organizo 
                el formato de cada una las variables de interes utilizando funciones como astype() de pandas cat.codes. 
        
        (3.x.3) Profiling antes de cleaning: Aqui se desea obtener un reporte preliminar del perfil de los datos antes de realizar su limpieza. 
    
    (4) Dfs Cleaning y Profiling:
        En esta seccion primero se seleccionaron las variables que aportaban el grueso de la informacion en cada DF y se le dieron nombres memotecnicos facil de reconocer en español.
        Segundo se definieron los DFs que se iban a guardar en la base de datos de SQLite. Y tercero se borraron los posibles duplicados en los data set y los datos nulos.
        Aqui se saco un reporte de profiling despues de hacer limpieza y se analizo en un archivo llamado 'Profiling_Analisis.pdf'

    (5) DFs a SQLite:
        Se llevaron los diferentes DFs a SQLite y se corrieron diferente queries para validar que si funcionara la base de datos.
    
    (6) ETL:
        En esta seccion se trabajaron con dos archivos externos config.py y tv_series_db.py. Este ultimo se corre desde TERMINAL en 
        VISUAL STUDIO CODE (o desde command prompt de Windows). En este caso el archivo tv_series ayuda extraer los datos de la API de interes, 
        transforma los datos en dataframes, cambia los formatos de ciertas variables de interes y finalmente carga los datos transformados a archivos en formato (.csv).
        Los archivos .csv pueden ser posteriormente utlizados en plataformas como PowerBI, Tableau y MS SQL.
        Nota: El archivo config.py ayuda a proteger si se desea activar con una clave la extraccion de los datos de la API.   

(ii) Ejecuetar el archivo tv_series_db.py:
     Doble click ar archivo tv_series_db.py inmediatamente abre Visual Studio code. 
     Alli vaya a la TERMINAL que se encuentra en la parte inferior de la pantalla y seleccione la opcion de interes (recomendado Git Bash).
     Alli utilice los comando de Git Bash ($pwd, $cd, $ls y otros) para llegar a la carpeta que contiene el archivo. 
     Escriba el nombre del archivo y ejecutelo. El resultado seran archivos .csv donde estaran los datos transformados por la ETL.
     Este es el link en Tableau para ver las graficas resultantes: 
     https://public.tableau.com/app/profile/luis.m.caicedo/viz/TV_Series_Dec_2020/Dashboard1
          


(iii) Lista de carpetas y archivos:
● Carpeta src/ con el proyecto Lulo_Bank_Prueba_VF.ipynb.
● Carpeta json/, con todos los archivos json obtenidos ('dateX.json', 31 archivos 
  en total siendo X el dia al que pertenecen los datos en Diciembre del 2020).
● Carpeta profiling/, todos los archivos profiling en HtML de los DFs extraidos (5 archivos
  df_air_basic_db_VF.html, df_country_db_VF.html, DF_genre_status_db_VF.html, df_ratings_db_VF.html, df_runtime_db_VF.html) y
  un archivo donde se encuentra el analisis 'Profiling_Analisis.pdf'.
● Carpeta db/ con el archivo de la base de datos (tvseries_2020-12.sqlite).
● Carpeta model/, con los archivos config.py y tv_series_db.py que ayudan a obtener los datos en archivos  en formato (.csv).

(iv) Información de Contacto:
Nombre: Luis Miguel Caicedo 
email: lmcaiced@gmail.com
Celular N°: 3174154741
