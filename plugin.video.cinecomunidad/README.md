# Cine Comunidad

Complemento experimental para Kodi que permite buscar fichas de películas en [Internet Archive](https://archive.org/).

## Estado del prototipo

- Busca títulos y temas en el catálogo público de Internet Archive.
- Muestra título, año y creador cuando esos datos están disponibles.
- Permite consultar la dirección de la ficha original.
- **No aloja ni reproduce películas.** La disponibilidad, la legalidad y las condiciones de uso varían por elemento; verificá la ficha y los derechos antes de acceder o reutilizar contenido.

## Estructura

```
plugin.video.cinecomunidad/
  addon.xml
  addon.py
```

## Instalación para desarrollo

1. Copiá la carpeta `plugin.video.cinecomunidad` a la carpeta de addons de Kodi.
2. Reiniciá Kodi y buscá **Cine Comunidad** en Complementos de video.
3. El dispositivo necesita conexión a Internet para consultar la API pública de Internet Archive.

Este prototipo usa solamente Python y las API integradas de Kodi. Todavía no incluye un instalador ZIP ni una prueba en un televisor/dispositivo Kodi real.

## Licencia

MIT para el código de este repositorio. Esto no concede derechos sobre los archivos o metadatos de terceros que aparecen en Internet Archive.
