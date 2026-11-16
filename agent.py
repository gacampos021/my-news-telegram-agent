import time
import calendar
import feedparser
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.genai import types

FEEDS = [
    "https://www.bleepingcomputer.com/feed/",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://therecord.media/feed",
    "https://feeds.feedburner.com/securityweek",
    "https://krebsonsecurity.com/feed/",
    "https://www.cisa.gov/cybersecurity-advisories/all.xml",
    "https://www.cert.br/rss/certbr-rss.xml",
]


def buscar_noticias() -> dict:
    """Lê feeds RSS de cibersegurança e devolve as notícias das últimas 30 horas, com título e link."""
    limite = time.time() - 30 * 3600
    linhas = []
    for url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:8]:
                t = e.get("published_parsed") or e.get("updated_parsed")
                if t and calendar.timegm(t) >= limite:
                    linhas.append(f"- {e.title[:120]} | {e.link}")
        except Exception:
            pass
    return {"noticias": "\n".join(linhas[:30]) or "Nenhuma notícia encontrada."}


agent = Agent(
    model=LiteLlm(
        model="ollama_chat/qwen3.5:4b",
        api_base="http://localhost:11434",
        num_ctx=8192,
        timeout=18000,
    ),
    name="agente_noticias",
    instruction=(
        "Responda em português do Brasil. Chame buscar_noticias uma única vez, "
        "escolha as 7 notícias mais relevantes e entregue como lista numerada, "
        "com título, link e um breve comentario do porque voce selecionou aquela noticia. responda somente a lista sem o processo ate chegar nela."
    ),
    tools=[buscar_noticias],
)

runner = InMemoryRunner(agent=agent, app_name="noticias")
sessao = runner.session_service.create_session_sync(app_name="noticias", user_id="u")
msg = types.Content(role="user", parts=[types.Part(text="Quais são as 7 notícias de cibersegurança mais relevantes de hoje?")])

texto = ""
for ev in runner.run(user_id="u", session_id=sessao.id, new_message=msg):
    if ev.is_final_response() and ev.content and ev.content.parts:
        texto = "".join(p.text or "" for p in ev.content.parts)

open("news.txt", "w", encoding="utf-8").write(texto)
