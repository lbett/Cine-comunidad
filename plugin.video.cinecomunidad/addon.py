# -*- coding: utf-8 -*-
"""Cine Comunidad: buscador de fichas de películas en Internet Archive.

Este complemento muestra resultados y enlaces a las páginas originales.
No reproduce ni aloja contenido, y no certifica los derechos de cada archivo.
"""
import json
import sys
import urllib.parse
import urllib.request

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]


def notify(message):
    xbmcgui.Dialog().notification("Cine Comunidad", message, xbmcgui.NOTIFICATION_INFO, 4500)


def make_url(query="", page=1, action="search"):
    params = {"action": action, "query": query, "page": page}
    return BASE_URL + "?" + urllib.parse.urlencode(params)


def get_json(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "CineComunidadKodi/0.1.0 (community public-archive search)"}
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def add_folder(label, url, art=None):
    item = xbmcgui.ListItem(label=label)
    if art:
        item.setArt(art)
    xbmcplugin.addDirectoryItem(HANDLE, url, item, isFolder=True)


def show_home():
    xbmcplugin.setPluginCategory(HANDLE, "Cine Comunidad")
    add_folder("Buscar películas…", make_url(action="search_prompt"))
    add_folder("Películas destacadas del archivo", make_url(query="classic film", page=1))
    add_folder("Cine de animación", make_url(query="animation film", page=1))
    add_folder("Cine documental", make_url(query="documentary film", page=1))
    xbmcplugin.endOfDirectory(HANDLE)


def search_prompt():
    query = xbmcgui.Dialog().input("¿Qué película querés buscar?")
    if query and query.strip():
        xbmc.executebuiltin("Container.Update(" + make_url(query=query.strip(), page=1) + ")")


def search_results(query, page=1):
    xbmcplugin.setPluginCategory(HANDLE, "Resultados: " + query)
    encoded_query = urllib.parse.quote(query)
    api_url = (
        "https://archive.org/advancedsearch.php?q="
        + urllib.parse.quote('mediatype:movies AND (title:"' + query + '" OR subject:"' + query + '")')
        + "&fl[]=identifier&fl[]=title&fl[]=year&fl[]=creator&rows=25&page="
        + str(max(1, int(page)))
        + "&output=json"
    )
    try:
        data = get_json(api_url)
        docs = data.get("response", {}).get("docs", [])
    except Exception as exc:
        xbmc.log("Cine Comunidad search error: " + repr(exc), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            "Cine Comunidad",
            "No se pudo consultar Internet Archive. Revisá la conexión e intentá de nuevo."
        )
        xbmcplugin.endOfDirectory(HANDLE, succeeded=False)
        return

    if not docs:
        notify("No encontré resultados para esa búsqueda.")
    for doc in docs:
        identifier = doc.get("identifier", "")
        title = doc.get("title") or identifier or "Sin título"
        year = doc.get("year")
        creator = doc.get("creator")
        if isinstance(creator, list):
            creator = ", ".join(str(x) for x in creator[:2])
        details = []
        if year:
            details.append(str(year))
        if creator:
            details.append(str(creator))
        label = title + (("  (" + " · ".join(details) + ")") if details else "")
        page_url = "https://archive.org/details/" + urllib.parse.quote(identifier, safe="")
        item = xbmcgui.ListItem(label=label)
        item.setInfo("video", {"title": str(title), "year": int(year) if str(year).isdigit() else 0, "plot": "Ficha original en Internet Archive. La disponibilidad y los derechos varían según el elemento."})
        item.setProperty("IsPlayable", "false")
        item.setArt({"icon": "DefaultVideo.png", "thumb": "DefaultVideo.png"})
        # Abrir la ficha como acción informativa; no intentar reproducir una página web.
        url = make_url(query=page_url, action="show_link")
        xbmcplugin.addDirectoryItem(HANDLE, url, item, isFolder=False)

    next_url = make_url(query=query, page=int(page) + 1, action="search")
    add_folder("Siguiente página", next_url)
    xbmcplugin.endOfDirectory(HANDLE)


def show_link(url):
    xbmcgui.Dialog().ok(
        "Ficha en Internet Archive",
        "Abrí esta dirección en un navegador para consultar la ficha y sus opciones:\n\n" + url
    )


def main():
    params = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(sys.argv[2]).query))
    action = params.get("action", "")
    query = params.get("query", "")
    page = int(params.get("page", "1") or "1")
    if action == "search_prompt":
        search_prompt()
    elif action == "search":
        search_results(query, page)
    elif action == "show_link":
        show_link(query)
    else:
        show_home()


if __name__ == "__main__":
    main()
