from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.http import JsonResponse

def getOneCharacter(request, character_id):
    response = requests.get(
        f"https://api.disneyapi.dev/characters/{character_id}",
        timeout=10
    )

    if response.status_code != 200:
        return HttpResponse(
            f"<h1>Xatolik</h1><p>API {response.status_code} status qaytardi.</p>",
            status=response.status_code
        )

    character = response.json()
    data = character["data"]

    def render_list(title, items):
        if not items:
            items_html = "<li>Ma'lumot yo'q</li>"
        else:
            items_html = "".join(f"<li>{item}</li>" for item in items)

        return f"""
        <div class="section">
            <h3>{title}</h3>
            <ul>
                {items_html}
            </ul>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{data["name"]}</title>
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}

            body {{
                background: linear-gradient(135deg, #f6d365, #fda085);
                padding: 40px 20px;
            }}

            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            }}

            .header {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                padding: 30px;
                align-items: center;
                background: #fff8f0;
                border-bottom: 1px solid #eee;
            }}

            .header img {{
                width: 250px;
                max-width: 100%;
                border-radius: 16px;
                object-fit: cover;
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
            }}

            .header-content {{
                flex: 1;
            }}

            .header-content h1 {{
                font-size: 36px;
                color: #333;
                margin-bottom: 12px;
            }}

            .header-content p {{
                font-size: 17px;
                color: #666;
                margin-bottom: 10px;
            }}

            .header-content a {{
                display: inline-block;
                margin-top: 10px;
                text-decoration: none;
                background: #ff7a59;
                color: white;
                padding: 10px 18px;
                border-radius: 10px;
                transition: 0.3s;
            }}

            .header-content a:hover {{
                background: #e86545;
            }}

            .content {{
                padding: 30px;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
            }}

            .section {{
                background: #fafafa;
                border: 1px solid #eee;
                border-radius: 16px;
                padding: 20px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
            }}

            .section h3 {{
                margin-bottom: 15px;
                color: #222;
                font-size: 20px;
            }}

            .section ul {{
                padding-left: 20px;
            }}

            .section li {{
                margin-bottom: 8px;
                color: #444;
            }}

            .footer {{
                padding: 20px 30px;
                background: #fff8f0;
                border-top: 1px solid #eee;
                color: #666;
                font-size: 14px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="{data["imageUrl"]}" alt="{data["name"]}">
                <div class="header-content">
                    <h1>{data["name"]}</h1>
                    <p><strong>ID:</strong> {data["_id"]}</p>
                    <p><strong>Character URL:</strong></p>
                    <a href="{data["url"]}" target="_blank">API linkni ochish</a>
                </div>
            </div>

            <div class="content">
                {render_list("Films", data["films"])}
                {render_list("Short Films", data["shortFilms"])}
                {render_list("TV Shows", data["tvShows"])}
                {render_list("Video Games", data["videoGames"])}
                {render_list("Park Attractions", data["parkAttractions"])}
                {render_list("Allies", data["allies"])}
                {render_list("Enemies", data["enemies"])}
            </div>

            <div class="footer">
                Disney character ma'lumotlari asosida yaratildi
            </div>
        </div>
    </body>
    </html>
    """

    return HttpResponse(html)

def getAllCharacters(request):
    pass



def search_movies(request):
    print(request.method)
    query = request.GET.get("q")

    if not query:
        return JsonResponse(
            {
                "ok": False,
                "message": "Qidiruv so'zi yuborilmadi. Masalan: /movies/search/?q=hulk"
            },
            status=400
        )

    url = "https://imdb.iamidiotareyoutoo.com/search"
    params = {
        "q": query
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return JsonResponse(data, safe=False, json_dumps_params={"ensure_ascii": False})

    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {
                "ok": False,
                "message": "Tashqi API bilan bog'lanishda xatolik yuz berdi.",
                "error": str(e)
            },
            status=500
        )
    except ValueError:
        return JsonResponse(
            {
                "ok": False,
                "message": "API JSON formatda javob qaytarmadi."
            },
            status=500
        )

def search_movies_html(request):
    query = request.GET.get("q")

    if not query:
        return HttpResponse("<h1>Qidiruv so'zi kerak</h1><p>Masalan: ?q=hulk</p>", status=400)

    try:
        response = requests.get(
            "https://imdb.iamidiotareyoutoo.com/search",
            params={"q": query},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"<h1>API xatoligi</h1><p>{e}</p>", status=500)

    movies = data.get("description", [])

    cards = ""
    for movie in movies:
        cards += f"""
        <div style="width:300px;border:1px solid #ddd;border-radius:12px;padding:16px;background:#fff;box-shadow:0 4px 12px rgba(0,0,0,0.08);">
            <img src="{movie.get('#IMG_POSTER', '')}" alt="{movie.get('#TITLE', '')}" style="width:100%;height:420px;object-fit:cover;border-radius:8px;">
            <h2 style="font-size:20px;margin:12px 0 8px;">{movie.get('#TITLE', 'Noma’lum')}</h2>
            <p><strong>Yili:</strong> {movie.get('#YEAR', '—')}</p>
            <p><strong>Actorlar:</strong> {movie.get('#ACTORS', '—')}</p>
            <p><strong>IMDB ID:</strong> {movie.get('#IMDB_ID', '—')}</p>
            <a href="{movie.get('#IMDB_URL', '#')}" target="_blank" style="display:inline-block;margin-top:10px;padding:10px 14px;background:#111;color:#fff;text-decoration:none;border-radius:8px;">
                IMDB ko‘rish
            </a>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Search: {query}</title>
    </head>
    <body style="font-family:Arial,sans-serif;background:#f5f5f5;padding:30px;">
        <h1>"{query}" bo‘yicha natijalar</h1>
        <div style="display:flex;flex-wrap:wrap;gap:20px;margin-top:20px;">
            {cards if cards else "<p>Hech narsa topilmadi.</p>"}
        </div>
    </body>
    </html>
    """

    return HttpResponse(html)