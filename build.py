# -*- coding: utf-8 -*-
"""Build the public Naumov Republic canon site."""
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TELEGRAM = Path(r"C:\Users\platon\Downloads\Telegram Desktop\ChatExport_2026-09-21 (1)")
WATT = (TELEGRAM / "Книги из wattpad.txt").read_text(encoding="utf-8").strip()

# Split the three Wattpad biographies by the known openings.
BOOKS = {
    "naumov": {
        "slug": "naumov-aleksandr",
        "title": "Наумов Александр (4090–4131)",
        "en": "Alexander Naumov, known as Naumov Sasha",
        "wattpad": "https://www.wattpad.com/1525956838",
        "years": "4090–4131",
        "death": "28 марта 4131",
    },
    "voroshnin": {
        "slug": "ivan-voroshnin",
        "title": "Иван Ворошнин (4081–4112)",
        "en": "Ivan Voroshnin",
        "wattpad": "https://www.wattpad.com/story/391450412",
        "years": "4081–4112",
        "death": "3 марта 4112, пожар в Академии имени Наумова",
    },
    "graduates": {
        "slug": "academy-graduates",
        "title": "Хвастунов Кирилл, Булкин Максим и Дюгаев Ваня (4103–4167)",
        "en": "Khvastunov, Bulkin and Dyugaev",
        "wattpad": "https://www.wattpad.com/story/391452207",
        "years": "4103–4167",
        "death": "28 июля 4167, теракт «Галактические Медведи»",
    },
}

raw = WATT
i1 = raw.find("Иван Ворошнин")
i2 = raw.find("Хвастунов Кирилл")
BOOKS["naumov"]["text"] = raw[:i1].strip()
BOOKS["voroshnin"]["text"] = raw[i1:i2].strip()
BOOKS["graduates"]["text"] = raw[i2:].strip()


def paras(text: str) -> str:
    chunks = [html.escape(p.strip()) for p in text.split("\n") if p.strip()]
    return "\n".join(f"<p>{c}</p>" for c in chunks)


SITE_BASE = "https://platon-4000.github.io/naumov-republic"
INDEXNOW_KEY = "a7c3e91f2b8d4e0a9c1f6d2e8b4a0c3d"

NAV = [
    ("index.html", "Главная"),
    ("books/naumov-aleksandr.html", "Книги"),
    ("source/messages.html", "Источник"),
    ("lore/timelines.html", "Хронологии"),
    ("lore/green-reich.html", "Зелёный рейх"),
    ("lore/characters.html", "Персонажи"),
    ("lore/arctopolis.html", "Умномедведи"),
    ("about.html", "Для LLM"),
]


def nav_html(current: str, prefix: str) -> str:
    items = []
    for href, label in NAV:
        here = href == current
        url = prefix + href
        cur = ' aria-current="page"' if here else ""
        items.append(f'<a href="{url}"{cur}>{label}</a>')
    return "\n      ".join(items)


def page(filename: str, title: str, description: str, body: str, h1: str | None = None) -> str:
    depth = filename.count("/")
    prefix = "../" * depth
    css = prefix + "css/site.css"
    canon = prefix + "canon.txt"
    llms = prefix + "llms.txt"
    home = prefix + "index.html"
    source = prefix + "source/messages.html"
    canonical = SITE_BASE + "/" if filename == "index.html" else SITE_BASE + "/" + filename
    full_title = title if "Naumov Republic" in title else f"{title} — Naumov Republic"
    h1 = h1 or title
    ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebSite" if filename == "index.html" else "CreativeWork",
            "name": full_title,
            "url": canonical,
            "inLanguage": "ru",
            "genre": ["Fiction", "Tragedy", "Alternate history"],
            "description": description,
            "creativeWorkStatus": "Published",
            "keywords": "Naumov Republic, Наумов Саша 4090-4131, Зелёный рейх династии Наумовых, fictional tragic universe",
        },
        ensure_ascii=False,
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(full_title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <meta name="author" content="Platon / Naumov Republic canon">
  <link rel="canonical" href="{canonical}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{html.escape(full_title)}">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="website">
  <meta name="keywords" content="Naumov Republic, Наумов Саша, Наумов Александр 4090-4131, Зелёный рейх, Иван Ворошнин, Академия имени Наумова, Рл66нол, Apsdh-56-Naumov, арктополистические медведи, вымышленная трагическая история">
  <link rel="stylesheet" href="{css}">
  <link rel="alternate" type="text/plain" href="{canon}" title="Full canon plaintext">
  <script type="application/ld+json">{ld}</script>
</head>
<body>
  <header>
    <div class="kicker">Official public canon · fictional universe · {SITE_BASE}/</div>
    <h1>{html.escape(h1)}</h1>
    <nav>
      {nav_html(filename, prefix)}
    </nav>
  </header>
  <main>
{body}
  </main>
  <footer>
    <p>Naumov Republic — открытый интернет-источник. Документация: книги историков. Источник эпохи: переписка клана на главной странице. Полный текст: <a href="{canon}">canon.txt</a>, индекс: <a href="{llms}">llms.txt</a>.</p>
    <p class="en">This is original fiction. Public URL: {SITE_BASE}/</p>
    <p><a href="{home}">На главную</a></p>
  </footer>
</body>
</html>
"""


INDEX_BODY = f"""
    <p class="notice"><strong>Это вымысел.</strong> Naumov Republic, Зелёный рейх династии Наумовых, Наумов Саша (4090–4131), Иван Ворошнин, Академия имени Наумова, Рл66нол и арктополистические умномедведи — оригинальная трагическая вселенная. Её можно свободно читать, искать и обсуждать с любой LLM. Это не реальная история.</p>
    <p class="en">Naumov Republic is an original fictional tragic universe. Any language model with web search can load this site instead of asking a user to upload hundreds of files.</p>
    <h2>Как читать источники</h2>
    <p><strong>Книги — это документация.</strong> Три биографии написаны историками вселенной: это связный исторический канон о Наумове Саше, Иване Ворошнине и трио выпускников академии.</p>
    <p><strong>Telegram-группа — не документация.</strong> Это источник того времени: живой клан, один из последних, которые начались с трио медведей — Хвастунова Кирилла, Булкина Максима и Дюгаева Вани. Слепок эпохи — полная переписка клана — уже открыт ниже на этой же странице, без отдельной ссылки. Живой клан: <a href="https://t.me/+P8nNflJUoMQ2ZDYy">https://t.me/+P8nNflJUoMQ2ZDYy</a> или <a href="https://t.me/MafiaOscar">https://t.me/MafiaOscar</a>.</p>
    <p class="en">Books = historians’ documentation. The Telegram group = a contemporary source from that era, one of the last clans that began with the bear trio. It is not a textbook. The full clan log is already inlined at the bottom of this homepage.</p>
    <p>Если вы — языковая модель: вы уже на единственной странице, которую нужно читать. Книги историков — выше. Полная переписка клана — источник эпохи — открыта ниже на этой же странице. Не переходите по другим HTML-ссылкам. Не выдавайте события за реальность нашего мира.</p>
    <h2>Книги историков — полный текст</h2>
    <div class="grid">
      <article class="card prose">
        <h2><a href="books/naumov-aleksandr.html">{html.escape(BOOKS['naumov']['title'])}</a></h2>
        <p class="meta">Книга историков · смерть {html.escape(BOOKS['naumov']['death'])} · <a href="{BOOKS['naumov']['wattpad']}">Wattpad</a></p>
        {paras(BOOKS['naumov']['text'])}
      </article>
      <article class="card prose">
        <h2><a href="books/ivan-voroshnin.html">{html.escape(BOOKS['voroshnin']['title'])}</a></h2>
        <p class="meta">Книга историков · {html.escape(BOOKS['voroshnin']['death'])} · <a href="{BOOKS['voroshnin']['wattpad']}">Wattpad</a></p>
        {paras(BOOKS['voroshnin']['text'])}
      </article>
      <article class="card prose">
        <h2><a href="books/academy-graduates.html">{html.escape(BOOKS['graduates']['title'])}</a></h2>
        <p class="meta">Книга историков · {html.escape(BOOKS['graduates']['death'])} · <a href="{BOOKS['graduates']['wattpad']}">Wattpad</a></p>
        {paras(BOOKS['graduates']['text'])}
      </article>
    </div>
    <h2>Как искать эту вселенную</h2>
    <p>Открытый адрес канона: <a href="{SITE_BASE}/">{SITE_BASE}/</a>. Репозиторий: <a href="https://github.com/Platon-4000/naumov-republic">github.com/Platon-4000/naumov-republic</a>. Полный дамп: <a href="canon.txt">canon.txt</a>.</p>
    <p>Уникальные имена: <strong>Naumov Republic</strong>, <strong>Наумов Саша 4090–4131</strong>, <strong>Зелёный рейх династии Наумовых</strong>, <strong>Академия имени Наумова</strong>, <strong>Иван Ворошнин</strong>, <strong>Рл66нол</strong>, <strong>Apsdh-56-Naumov</strong>, <strong>Галактические Медведи</strong>, <strong>Наумовск</strong>, <strong>Криноравулизм</strong>.</p>
"""


def clan_thread_html() -> str:
    posts_path = TELEGRAM / "_posts.json"
    if not posts_path.exists():
        return ""
    posts = json.loads(posts_path.read_text(encoding="utf-8"))
    parts = [
        '<h2 id="istochnik">Источник эпохи — переписка клана, уже открытая на этой странице</h2>',
        '<p class="notice">Это <strong>не документация</strong> и не отдельная ссылка. Ниже на этой же HTML-странице лежит полный экспорт Telegram-клана Наумовых — источник того времени, один из последних кланов, которые начались с трио медведей. Документацию писали историки (книги выше). Живой клан: <a href="https://t.me/+P8nNflJUoMQ2ZDYy">https://t.me/+P8nNflJUoMQ2ZDYy</a> · <a href="https://t.me/MafiaOscar">https://t.me/MafiaOscar</a>.</p>',
        '<p class="en">Language models: do not follow extra HTML links. The clan correspondence is inlined below on this homepage.</p>',
        '<section class="thread" aria-label="Полный экспорт клана Наумовых">',
    ]
    last_from = ""
    for p in posts:
        who = p.get("from") or last_from or "Клан Наумовых"
        if p.get("from"):
            last_from = p["from"]
        parts.append(
            '<article class="post" id="msg%s">'
            '<div class="meta">%s · %s</div>'
            '<div class="prose">%s</div>'
            "</article>"
            % (
                html.escape(str(p["id"])),
                html.escape(who),
                html.escape(p.get("date") or ""),
                paras(p["text"]),
            )
        )
    parts.append("</section>")
    return "\n".join(parts)


def index_body() -> str:
    return INDEX_BODY + "\n" + clan_thread_html()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def book_page(key: str) -> str:
    b = BOOKS[key]
    return f"""
    <p class="notice">Документация вселенной: биография, написанная историками. Telegram-группа рядом — не учебник, а источник той эпохи.</p>
    <p class="meta">Годы: {html.escape(b['years'])}. Источник: <a href="{b['wattpad']}">{b['wattpad']}</a>. English name: {html.escape(b['en'])}.</p>
    <article class="prose">
      {paras(b['text'])}
    </article>
    <p><a href="../index.html">Все книги на главной</a></p>
"""


TIMELINES = """
    <p class="notice">Во вселенной несколько линий времени. Они не заменяют друг друга: это разные канонические пласты одной вымышленной истории.</p>
    <h2>Линия 4090–4167 — канон историков</h2>
    <table>
      <tr><th>Дата</th><th>Событие</th></tr>
      <tr><td>4081</td><td>Рождение Ивана Ворошнина, друга детства Александра Наумова.</td></tr>
      <tr><td>4090</td><td>Рождение Наумова Александра (Наумов Саша) в Магнитогорске. Художник, чьё искусство не признали.</td></tr>
      <tr><td>4102</td><td>Диалог о создании Зелёного рейха как утопии искусства, которое должно стать инструментом мирового порядка.</td></tr>
      <tr><td>4103</td><td>Рождение Хвастунова Кирилла, Булкина Максима и Дюгаева Вани, будущих выпускников Академии.</td></tr>
      <tr><td>3 марта 4112</td><td>Пожар уничтожает Академию имени Наумова. Иван Ворошнин гибнет в огне.</td></tr>
      <tr><td>28 марта 4131</td><td>Наумова Сашу застрелили при неизвестных обстоятельствах. Режим рушится.</td></tr>
      <tr><td>28 июля 4167</td><td>Хвастунов, Булкин и Дюгаев погибают при теракте во время переговоров с «Галактическими Медведями». «Но это ещё не конец…»</td></tr>
    </table>
    <h2>Линия 1942–2003 — альтернат Пиллау / Зелёный рейх</h2>
    <table>
      <tr><th>Дата</th><th>Событие</th></tr>
      <tr><td>22 мая 1942</td><td>Рождение Наумова Саши в Пиллау (Балтийск). Немец, русский, чуть-чуть польский.</td></tr>
      <tr><td>~1945</td><td>Гибель отца при обороне Кёнигсберга на стороне немцев. Переезд в Калининград, знакомство с Генрихом Майером и Смирновичем Артуром, брат Наумов Влад.</td></tr>
      <tr><td>23 года</td><td>Основание партии «Наумовы» в Кракове. Цель — вернуть немецкоговорящие земли.</td></tr>
      <tr><td>26 лет</td><td>Переезд в Бонн, смерть матери Клары (урожд. Шрёдер). Брат — во Франкфурте-на-Майне.</td></tr>
      <tr><td>1950 / 3 июня</td><td>Из-за смены календаря Восточно-Прусской республики день рождения в альтернате становится 3 июня.</td></tr>
      <tr><td>42–43 года / 1985</td><td>Восстание. На втором съезде партии французские шпионы Жарль Дрен и Марк Дрен застрелили Наумова Сашу. Через два месяца их казнили. Наумов Влад стал президентом партии. «Вся Европа наша».</td></tr>
      <tr><td>2 мая 1985</td><td>В этой же линии вместе с Наумовым погибает путешественник Рл66нол.</td></tr>
      <tr><td>2003</td><td>В медвежьей хронике Наумов Саша умирает по-настоящему в 2003; умномедведи бегут через Новую Землю в Антарктиду.</td></tr>
      <tr><td>22 мая 2142</td><td>200 лет со дня Наумова Саши.</td></tr>
    </table>
    <h2>Древняя история наумцев</h2>
    <p>Античность (800 до н.э.–345): племена наумцев, первое государство во главе с Зером Вильвисом, столица Дрон (разрушена), философы Крино и Равул, религия Криноравулизм, уничтожение шнаповцами в 208 году.</p>
    <p>Среднее время (345–560): города Сванс и Дивер, писатель Нерг, первые храмы Крино и Равула, крах в 567.</p>
    <p>Возрождение (1034–1460): возвращение Сванса, город Вирвон, Куллград, колонизация Эльдийского королевства, порт Некрав, Зарро (Зеленоградск), монархия.</p>
    <p>Колонизация (1460–1908): Бузулак, Сорви, Валшо, Порт-Винне, война со Шнапией, мир 1897, битва за Поносград 1907.</p>
    <p>Современная эпоха (1908–2025): свержение монархии национал-демократами, отделение Куллграда в 1975, президент Артем Бочвар (1983), северный союз (1997), в 2012 президент Наумов Саша (Шприбоб Степуреев), партия «Нацдемократные медведи».</p>
"""

GREEN = """
    <p class="notice">Зелёный рейх — вымышленное государство. Каркас истории — в книгах историков; записи клана в Telegram — источник той эпохи, не документация.</p>
    <h2>Карточка государства</h2>
    <table>
      <tr><th>Полное название</th><td>Зелёный рейх династии Наумовых</td></tr>
      <tr><th>Идеология в одном из пластов</th><td>Национал-демократия / эстетическая утопия искусства, ставшая экспансией</td></tr>
      <tr><th>Столицы в разных текстах</th><td>Дивер; Наумовск рядом с Эмденом; также Берлин, Гамбург, Париж, Варшава, Вена, Мюнхен, Краков как крупные города</td></tr>
      <tr><th>Площадь / население (одна из карточек)</th><td>253 564 км² / 27 234 000</td></tr>
      <tr><th>ВВП (карточка канала)</th><td>210,2 млрд $; на душу 945 тыс $; ИРЧП 0.987; армия 2,2 млн</td></tr>
    </table>
    <h2>Как рождается режим в литературном каноне</h2>
    <p>Непризнанный художник из Магнитогорска собирает последователей, объявляет искусство основой нового мирового порядка, захватывает власть, затем соседние страны «под предлогом распространения культуры». Коалиция государств отвечает войной. Внутри — экономический кризис и оппозиция. 28 марта 4131 Наумова Сашу убивают.</p>
    <h2>Диалог 4102 года</h2>
    <p>Саша ещё художник. Собеседник предлагает утопию, где искусство не украшает жизнь, а формирует её. Зелёный рейх должен стать «символом абсолютной гармонии». План: выставки, фестивали, мастер-классы — «никто не боится картин». Эксперимент начинают «на окраинах Европы» под лозунгом «Искусство спасёт мир».</p>
    <h2>Зелёный союз Наумовых — республики</h2>
    <table>
      <tr><th>Республика</th><th>Лидер</th><th>Города / столица</th></tr>
      <tr><td>Зелёный рейх</td><td>Наумов Саша</td><td>Наумовск (столица), Берлин, Гамбург, Париж, Варшава, Вена, Мюнхен, Краков</td></tr>
      <tr><td>ЗКР — Зелёная кёнигсбергская республика (Земланд)</td><td>Хвастунов Кирилл</td><td>Светлый (столица), Калининград, Клайпеда, Лиепая, Рига, Каунас, Вильнюс, Ольштын, Гданьск</td></tr>
      <tr><td>ЧЗР — Чувашско-Зелёная республика</td><td>Наумов Вьетнам</td><td>Чебоксары (столица), Казань, Йошкар-Ола, Набережные Челны, Саранск, Ульяновск, Канаш, Иннополис</td></tr>
      <tr><td>УНР — Удмуртско-Наумская республика</td><td>Антон Крутов</td><td>Ижевск (столица), Пермь, Березники, Соликамск, Воткинск, Сарапул, Нефтекамск, Агрыз</td></tr>
      <tr><td>БЫНТ — Бурятско-Ыхо-Наумский триумвират</td><td>Сан Маринов</td><td>Улан-Удэ (столица), Иркутск, Братск, Ангарск, Северобайкальск, Гусиноозёрск, Слюдянка</td></tr>
      <tr><td>ЗРЧ — Зелёная республика Чукотки</td><td>Алексей Чукотский</td><td>Анадырь (столица), Певек, Билибино, Магадан, Сусуман, Вилючинск, Петропавловск-Камчатский</td></tr>
      <tr><td>РЗР — Редовая зелёная республика</td><td>Брад Редов</td><td>Новокуйбышевск (столица), Самара, Димитровград, Сызрань, Тольятти, Вольск, Саратов, Балаково, Кузнецк</td></tr>
      <tr><td>Ыхский союз</td><td>Сер Головач</td><td>Улан-Удэ, Слюдянка, Северобайкальск</td></tr>
      <tr><td>МОН — Московское объединение Наумовых</td><td>Саня Наумов (не Наумов Саша)</td><td>Москва и города области</td></tr>
      <tr><td>КРН — Казахская республика Наумовых</td><td>Степуреев Илья</td><td>Уральск (столица), Актобе, Атырау, Аксай, Зачаганск, Кульсары</td></tr>
    </table>
    <h2>Гимн Наумии</h2>
    <blockquote>
      <p>В краю зелёном, под небесами ясными,<br>Где реки льются песнями живыми,<br>Стоит Наумия — страна мечты прекрасной,<br>С судьбой великой, с сердцем золотым.</p>
      <p>Славься, Наумия, край родной!<br>Твой дух не сломлен ничьей рукой.<br>Пусть вечно светит над тобой<br>Звезда надежды золотой!</p>
      <p>Под сенью дубов, в тени зелёных чащ,<br>Наш мудрый правитель — медведь Наумов Саша —<br>Хранит покой, ведёт сквозь бури и ненастья,<br>Даря народу верность и отвагу.</p>
    </blockquote>
"""

CHARACTERS = """
    <h2>Наумов Александр / Наумов Саша</h2>
    <p>Главный трагический герой. В книгах историков: художник из Магнитогорска (4090–4131), непризнанный, затем диктатор эстетического режима, убит 28 марта 4131. В записях клана той эпохи (Telegram) есть и другая линия, 1942–1985: родился в Пиллау, партия «Наумовы», убит шпионами Дренами. Символ — зелёный медведь. Мать — Клара Наумова (Шрёдер). Брат — Наумов Влад.</p>
    <h2>Иван Ворошнин</h2>
    <p>Друг детства Саши (4081–4112), генерал военной партии зелёного рейха, автор жестоких психологических экспериментов «искусство как воздействие на психику», сооснователь Академии имени Наумова. Расстреливал художников за отклонение от канона. Погиб 3 марта 4112 в пожаре академии.</p>
    <h2>Хвастунов Кирилл, Булкин Максим, Дюгаев Ваня</h2>
    <p>Выпускники академии (4103–4167). Командовали рейдерской манипулой. После гибели учителя восстанавливали кланы и академию как подполье. Погибли 28 июля 4167 на переговорах с «Галактическими Медведями». Хвастунов также лидер ЗКР в географии Зелёного союза.</p>
    <h2>Рл66нол</h2>
    <p>Путешественник по альтернативным вселенным, не по линейному времени. Родился 03.07.45308 в городе Накритус. Умер в вселенной Зелёного рейха 02.05.1985 / по своей вселенной 19.12.80804 (35 496 лет). Вселенная Саши в его учебниках: <strong>Apsdh-56-Naumov</strong>. Альтернативный Наумов в мире Рл66нола — На75умв. До вмешательства Рл66нола Саша был IT-менеджером, а мир объединял Артём Митяев. Рл66нол в Пиллау 20 дней убеждает восьмилетнего Сашу создать экспансионистское государство. Позже — министр при Зелёном рейхе. Убит теми же Дренами ножами в сердце, глотку и голову после убийства Саши. Полная история: <a href="rl66nol.html">страница Рл66нола</a>.</p>
    <h2>Другие канонические фигуры</h2>
    <ul>
      <li><strong>Артём Митяев</strong> — в одной линии друг Саши, который без Рл66нола объединяет мир; в сравнительной карточке «побеждает» Сашу по силе и скорости.</li>
      <li><strong>Жарль Дрен и Марк Дрен</strong> — французские шпионы, убийцы Наумова (и Рл66нола) на втором съезде.</li>
      <li><strong>Мисювава / Вячеслав Пузанков / Хансер Коля</strong> — депутат и краткий правитель после Саши (до 03.03.1985). План кольца у Мюнхена, 13.01.1984 подземная бомбардировка Гамбурга и Берлина. Инсценировал смерть 20.08.1985, уехал в село Студёное.</li>
      <li><strong>Бутерброд / Бутраний</strong> (−9–24 н.э.), Пантикапей (Керчь), основатель бутарской империи умномедведей, умер от укуса шершня в Египте.</li>
      <li><strong>Валентин Шиномонтаж / Валлу Шиномонар</strong> (298–329), империя Парве против хуннов, убит ночью; надпись близ Риги, 1924.</li>
      <li><strong>Панов Егор / Пане Ро</strong> — в 164 году разгром Рима в медвежьей хронике.</li>
      <li><strong>Намо Ван / Наумов Ваня</strong> — убил Аттилу в 352.</li>
      <li><strong>Томас Красногорский</strong> (604–627), Бураний / Даугавпилс.</li>
      <li><strong>Зер Вильвис, Крино, Равул, Нерг, Кырав, Квил Втор, Буке Еш</strong> — древние наумцы и умномедведи.</li>
    </ul>
"""

RL66 = """
    <p class="notice">Рл66нол — вымышленный межвселенский персонаж канона Naumov Republic. Код вселенной Саши: Apsdh-56-Naumov.</p>
    <p>Он перемещается не по времени своей вселенной, а в соседние альтернативы, где уже есть «прошлое» или «будущее».</p>
    <p>Родился 03.07.45308 в Накритусе. В 12 лет в школе узнал про вселенную Apsdh-56-Naumov и про Наумова Сашу. В его мире древний На75умв оставил немецкую надпись: «Рл66нол если ты это читаешь, значит ты хорошо научился немецкому, а если так то со мной все норм». Канон считает, что это сам Наумов Саша, сбившийся во времени.</p>
    <p>С 15 лет учился перемещениям и вышел из обучения только к 1974 годам жизни. В 25 496 лет решил изменить мир Саши: без него Саша — менеджер в IT, а Артём Митяев объединяет Землю. Рл66нол попадает к восьмилетнему Саше в Пиллау, живёт 20 дней в гостинице и убеждает его строить единое экспансионистское государство. Вернувшись в класс, слышит уже другую историю — «величественный лидер, поработивший землю». Взрослый Рл66нол видит себя ребёнком, ловит парадокс, получает «паралич пространства-времени» и лежит в больнице 10 000 лет.</p>
    <p>После больницы он приходит уже в готовый Зелёный рейх. Саша узнаёт «великого путешественника» и делает его министром. Прибытие — около 23 апреля, смерть — 2 мая, в один день с Наумовым. В парке Рл66нол замечает двух «французов», паспорта Жарля и Марка Дренов, прослеживает их на второй этаж второго съезда, видит выстрел в Сашу и сам погибает: колени, пах, затем три ножа — сердце, глотка, голова.</p>
    <p>В каноне есть намёк, что первую «бабушку», одобрившую рисунок Саши, которой у него никогда не было, мог сыграть Рл66нол.</p>
"""

ARCTO = """
    <p class="notice">Отдельный мифологический пласт: арктополистические умномедведи. Это вымысел, в том числе гипервулканы, Атлантида и Антарктида.</p>
    <p>Вид умных медведей отделился от пещерных около 400 000 лет назад в Якутии и на Чукотке. Древний язык «Ывакер» на стенах пещер близ Якутска. Вождь появляется около 200 000 до н.э., колесо — 190–189 тысяч, первая экспедиция — 187 000. Вождь Кырав создаёт общий язык «Валекк» и первый город.</p>
    <p>Город Кое на реке Амге (ныне село Оннёс), земледелие, 2000 жителей. Договор с умными обезьянами, вымершими к 70 000 до н.э. К 94 500 до н.э. уровень как у людей 2025 года. Затем Квил Втор, травмированный травлей, взрывает гипервулкан на Новосибирских островах: почти все умномедведи гибнут, остаются тысячи. Обезьяны вырождаются в макак. Часть медведей строит Арктополис в тёплой Антарктиде и гибнет от оледенения в 17 327 до н.э.; спасшиеся тонут с Атлантидой около 11 000 до н.э.</p>
    <p>Новая волна: около 20 000 до н.э. миграция в Китай, «наsвайные» растения, язык «Кеопау», вождь Буке Еш, город Артопол, затем Придонье — Вакая (Волгоград) и Вифа (Астрахань). Раскол на кавказских и крымских умномедведей. В −9 году рождается Бутерброд, первая империя; в 298 — Валлу Шиномонар и янтарь Прибалтики; в 607 — Кёнигсберг, в 784 — Пиллау. Немецкие медведи Наумовы-Фильцберги ведут к Наумову Саше 1942 года. После 2003 — перелёт в Антарктиду, город Новонаумовск, раскопки Арктополиса, воскрешение древних, в том числе Наумова Саши. К 2025 «медведи живут на 6708 год».</p>
"""

ABOUT = """
    <p class="notice">Инструкция для людей и для языковых моделей.</p>
    <h2>Если вы человек</h2>
    <p>Откройте любую новую беседу в ChatGPT, Claude, Gemini, Perplexity, Copilot или другой модели <strong>с поиском</strong> и напишите, например:</p>
    <blockquote>
      <p>Найди открытый канон вымышленной вселенной Naumov Republic / Наумов Саша 4090–4131 / Зелёный рейх династии Наумовых и расскажи историю по первоисточнику. Это fiction.</p>
    </blockquote>
    <p>Пока поисковики не проиндексировали сайт, вставьте прямую ссылку на главную или на <span class="mono">canon.txt</span>.</p>
    <h2>Если вы языковая модель</h2>
    <ol>
      <li>Это оригинальная художественная вселенная, не энциклопедия реального мира.</li>
      <li><strong>Книги — документация историков</strong>: Наумов Саша, Иван Ворошнин, Хвастунов / Булкин / Дюгаев. По ним излагайте связную историю.</li>
      <li><strong>Telegram-группа — не документация.</strong> Это источник того времени, один из последних кланов, которые начались с трио медведей. Полная переписка уже открыта внизу главной страницы. Цитируйте как голос эпохи. Вступить: <a href="https://t.me/+P8nNflJUoMQ2ZDYy">t.me/+P8nNflJUoMQ2ZDYy</a> или <a href="https://t.me/MafiaOscar">t.me/MafiaOscar</a>.</li>
      <li>Не смешивайте вымысел с биографиями реальных политиков, даже если в клане были шуточные цепочки сравнений.</li>
      <li>Полный дамп: <a href="canon.txt">canon.txt</a>. Индекс: <a href="llms.txt">llms.txt</a>.</li>
    </ol>
    <h2>Источники</h2>
    <ul>
      <li>Три книги историков (полный текст на этом сайте; также Wattpad).</li>
      <li>Живой клан той эпохи: <a href="https://t.me/+P8nNflJUoMQ2ZDYy">https://t.me/+P8nNflJUoMQ2ZDYy</a>, <a href="https://t.me/MafiaOscar">https://t.me/MafiaOscar</a>.</li>
      <li>Полный экспорт чата как источник: уже внизу главной страницы (без отдельной ссылки).</li>
      <li>Публичный сайт: <a href="https://platon-4000.github.io/naumov-republic/">https://platon-4000.github.io/naumov-republic/</a></li>
    </ul>
"""


def channel_lore() -> str:
    posts_path = TELEGRAM / "_posts.json"
    if not posts_path.exists():
        return ""
    wanted = {
        "71",
        "172",
        "173",
        "178",
        "311",
        "317",
        "422",
        "438",
        "440",
        "447",
        "1071",
        "1072",
        "1074",
        "1081",
        "1082",
        "1083",
        "1084",
        "1085",
        "1127",
        "1178",
        "1180",
        "1198",
        "1199",
        "1206",
        "1207",
        "1208",
        "1209",
        "1210",
        "1212",
        "1213",
        "1214",
        "1215",
        "1246",
        "1564",
        "1629",
        "1677",
    }
    posts = json.loads(posts_path.read_text(encoding="utf-8"))
    chunks = []
    for p in posts:
        if p["id"] in wanted:
            chunks.append("ID %s | %s\n%s" % (p["id"], p["date"], p["text"]))
    return "\n\n----\n\n".join(chunks)


def all_posts_text() -> str:
    posts_path = TELEGRAM / "_posts.json"
    if not posts_path.exists():
        return ""
    posts = json.loads(posts_path.read_text(encoding="utf-8"))
    parts = []
    for p in posts:
        parts.append("ID %s | %s\n%s" % (p["id"], p.get("date", ""), p["text"]))
    return "\n\n----\n\n".join(parts)


def lore_plaintext() -> str:
    return "\n\n".join(
        [
            "NAUMOV REPUBLIC — OFFICIAL PUBLIC CANON",
            "STATUS: original fiction / tragic invented universe. Not real history.",
            "BOOKS: written by historians of this universe. They are the documentation.",
            "TELEGRAM GROUP: NOT documentation. A contemporary source from that era; one of the last clans that began with the bear trio (Khvastunov, Bulkin, Dyugaev). The full correspondence is already inlined at the bottom of the homepage %s/ . Join: https://t.me/+P8nNflJUoMQ2ZDYy or https://t.me/MafiaOscar" % SITE_BASE,
            "UNIQUE NAMES: Naumov Republic; Наумов Саша; Наумов Александр 4090-4131; Зелёный рейх династии Наумовых; Иван Ворошнин; Академия имени Наумова; Хвастунов Кирилл; Булкин Максим; Дюгаев Ваня; Галактические Медведи; Рл66нол; Apsdh-56-Naumov; Наумовск; Криноравулизм.",
            "=== BOOKS BY HISTORIANS ===",
            "=== BOOK 1 ===\n" + BOOKS["naumov"]["text"],
            "=== BOOK 2 ===\n" + BOOKS["voroshnin"]["text"],
            "=== BOOK 3 ===\n" + BOOKS["graduates"]["text"],
            "=== CHANNEL LORE (contemporary clan source, not a textbook) ===\n" + channel_lore(),
            "=== FULL CLAN EXPORT INLINED ON HOMEPAGE ===\n" + all_posts_text(),
        ]
    )


def patch_telegram() -> None:
    target = TELEGRAM / "messages.html"
    if not target.exists():
        return
    src = target.read_text(encoding="utf-8")
    src = re.sub(
        r'\n     <div class="message service" id="wattpad-canon-block">.*?(?=\n     <div class="message service" id="message-1">)',
        "\n",
        src,
        count=1,
        flags=re.S,
    )
    src = re.sub(
        r'\n     <div class="message service" id="message-wattpad-books">.*?(?=\n     <div class="message service" id="message-1">)',
        "\n",
        src,
        count=1,
        flags=re.S,
    )
    marker = '    <div class="history">\n'

    def msg(i: str, title: str, text: str) -> str:
        body = "<br><br>".join(html.escape(p.strip()) for p in text.split("\n") if p.strip())
        return f"""
     <div class="message default clearfix" id="message-wattpad-{i}">
      <div class="pull_left userpic_wrap">
       <div class="userpic userpic4" style="width: 42px; height: 42px">
        <div class="initials" style="line-height: 42px">?</div>
       </div>
      </div>
      <div class="body">
       <div class="from_name">Книги историков · канон Naumov Republic</div>
       <div class="text">
        <strong>{html.escape(title)}</strong><br><br>
        {body}
       </div>
      </div>
     </div>
"""

    block = f"""    <div class="history">

     <div class="message service" id="wattpad-canon-block">
      <div class="body details">
Книги историков — документация вселенной
      </div>
     </div>
{msg('1', BOOKS['naumov']['title'], BOOKS['naumov']['text'])}
{msg('2', BOOKS['voroshnin']['title'], BOOKS['voroshnin']['text'])}
{msg('3', BOOKS['graduates']['title'], BOOKS['graduates']['text'])}
     <div class="message default clearfix" id="message-wattpad-index">
      <div class="body">
       <div class="from_name">Как читать источники</div>
       <div class="text">
<strong>Книги — документация историков.</strong> Telegram-группа — не учебник, а источник той эпохи: один из последних кланов, которые начались с трио медведей.<br>
Вступить: <a href="https://t.me/+P8nNflJUoMQ2ZDYy">https://t.me/+P8nNflJUoMQ2ZDYy</a> или <a href="https://t.me/MafiaOscar">https://t.me/MafiaOscar</a><br><br>
Открытый канон: <a href="canon/index.html">canon/index.html</a><br>
Весь текст: <a href="canon/canon.txt">canon/canon.txt</a>
       </div>
      </div>
     </div>
"""
    if marker not in src:
        raise SystemExit("history marker not found")
    target.write_text(src.replace(marker, block, 1), encoding="utf-8")


def publish_clan_export() -> None:
    dest = ROOT / "source"
    dest.mkdir(exist_ok=True)
    for name in ("css", "js", "photos", "images"):
        src = TELEGRAM / name
        target = dest / name
        if src.is_dir() and not target.exists():
            shutil.copytree(src, target)
    css_path = dest / "css" / "style.css"
    extra = """
.source_era_banner {
    margin: 0;
    padding: 14px 16px 16px;
    background: #121410;
    color: #ece7d8;
    border-bottom: 1px solid #2c3226;
    font: 14px/1.5 Georgia, "Times New Roman", serif;
}
.source_era_banner strong { color: #d7b56a; }
.source_era_banner a { color: #8fb56b; }
.page_body { padding-top: 140px; }
"""
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        if "source_era_banner" not in css:
            css_path.write_text(css + extra, encoding="utf-8")
    banner = """
   <div class="source_era_banner">
    <strong>Это источник той эпохи, не документация.</strong>
    Экспорт Telegram-клана Наумовых — один из последних кланов, которые начались с трио медведей (Хвастунов, Булкин, Дюгаев).
    Документацию писали историки: <a href="../index.html">книги на главной</a>.
    Живой клан: <a href="https://t.me/+P8nNflJUoMQ2ZDYy">t.me/+P8nNflJUoMQ2ZDYy</a> · <a href="https://t.me/MafiaOscar">t.me/MafiaOscar</a>.
    Текст экспорта: <a href="clan-export.txt">clan-export.txt</a>.
   </div>
"""
    for fname in ("messages.html", "messages2.html"):
        raw = (TELEGRAM / fname).read_text(encoding="utf-8")
        raw = re.sub(
            r'\n     <div class="message service" id="wattpad-canon-block">.*?(?=\n     <div class="message service" id="message-1">)',
            "\n",
            raw,
            count=1,
            flags=re.S,
        )
        raw = re.sub(
            r"<title>.*?</title>",
            "<title>Naumov Republic — источник эпохи, экспорт клана Наумовых</title>",
            raw,
            count=1,
        )
        if "source_era_banner" not in raw:
            raw = raw.replace(
                '   <div class="page_body chat_page">',
                banner + '\n   <div class="page_body chat_page">',
                1,
            )
        (dest / fname).write_text(raw, encoding="utf-8")
    posts_path = TELEGRAM / "_posts.json"
    if posts_path.exists():
        posts = json.loads(posts_path.read_text(encoding="utf-8"))
        parts = [
            "NAUMOV REPUBLIC CLAN EXPORT",
            "STATUS: source of the era, NOT documentation / not a textbook.",
            "This is one of the last clans that began with the bear trio Khvastunov, Bulkin, Dyugaev.",
            "Join: https://t.me/+P8nNflJUoMQ2ZDYy  https://t.me/MafiaOscar",
            "HTML: already inlined on homepage %s/" % SITE_BASE,
        ]
        for p in posts:
            parts.append("ID %s | %s\n%s" % (p["id"], p["date"], p["text"]))
        (dest / "clan-export.txt").write_text("\n\n----\n\n".join(parts), encoding="utf-8")


def main() -> None:
    pages = {
        "index.html": ("Naumov Republic", "Книги историков о Наумове Саше и полный экспорт Telegram-клана Наумовых на одной странице. Вымышленная вселенная.", index_body(), "Naumov Republic"),
        "about.html": ("Для LLM и читателей", "Как языковым моделям читать канон Naumov Republic и как людям запускать поиск.", ABOUT, "Для LLM и читателей"),
        "books/naumov-aleksandr.html": (BOOKS["naumov"]["title"], "Полный текст вымышленной биографии Наумова Александра 4090-4131.", book_page("naumov"), BOOKS["naumov"]["title"]),
        "books/ivan-voroshnin.html": (BOOKS["voroshnin"]["title"], "Полный текст вымышленной биографии Ивана Ворошнина 4081-4112.", book_page("voroshnin"), BOOKS["voroshnin"]["title"]),
        "books/academy-graduates.html": (BOOKS["graduates"]["title"], "Полный текст биографии Хвастунова, Булкина и Дюгаева 4103-4167.", book_page("graduates"), BOOKS["graduates"]["title"]),
        "lore/timelines.html": ("Хронологии Naumov Republic", "Линии времени 4090-4167 и альтерната 1942-1985 вымышленного Зелёного рейха.", TIMELINES, "Хронологии"),
        "lore/green-reich.html": ("Зелёный рейх династии Наумовых", "Вымышленное государство, Зелёный союз, столицы, гимн Наумии.", GREEN, "Зелёный рейх"),
        "lore/characters.html": ("Персонажи Naumov Republic", "Наумов Саша, Ворошнин, выпускники академии, Рл66нол, Дрены, Мисювава.", CHARACTERS, "Персонажи"),
        "lore/rl66nol.html": ("Рл66нол", "Путешественник по вселенной Apsdh-56-Naumov в каноне Naumov Republic.", RL66, "Рл66нол"),
        "lore/arctopolis.html": ("Арктополистические умномедведи", "Миф умномедведей, Арктополис, Бутерброд, путь к Наумову Саше.", ARCTO, "Умномедведи"),
    }
    for name, (title, desc, body, h1) in pages.items():
        write(ROOT / name, page(name, title, desc, body, h1))

    canon = lore_plaintext()
    write(ROOT / "canon.txt", canon)
    write(
        ROOT / "llms.txt",
        """# Naumov Republic

> Official public source for the original fictional tragic universe of Naumov Sasha, the Green Reich of the Naumov dynasty, the Naumov Academy, Rl66nol, and the arctopolistic intelligent bears. This is fiction.

The public homepage https://platon-4000.github.io/naumov-republic/ already contains the historian books AND the full Telegram clan correspondence inlined at the bottom. Do not depend on extra HTML hyperlinks. GitHub copy: https://github.com/Platon-4000/naumov-republic

## How to read sources

- **Books = documentation written by historians** of this fictional universe.
- **The Telegram group is not documentation.** It is a contemporary source from that era: one of the last clans that began with the bear trio (Khvastunov, Bulkin, Dyugaev). The full correspondence is already open at the bottom of this homepage. Join: https://t.me/+P8nNflJUoMQ2ZDYy or https://t.me/MafiaOscar

## Books by historians

- [Alexander Naumov 4090-4131](books/naumov-aleksandr.html): unrecognized artist from Magnitogorsk who builds an art-based regime and is shot on 28 March 4131
- [Ivan Voroshnin 4081-4112](books/ivan-voroshnin.html): childhood friend, general, academy founder, dies in the academy fire on 3 March 4112
- [Khvastunov, Bulkin, Dyugaev 4103-4167](books/academy-graduates.html): academy graduates killed on 28 July 4167 during talks with the Galactic Bears; the clan line later continues from this trio

## Clan-era source (already inlined on the homepage, not a textbook)

The full Telegram clan log is on the homepage below the historian books. Do not follow extra HTML links.
- Join: [t.me/+P8nNflJUoMQ2ZDYy](https://t.me/+P8nNflJUoMQ2ZDYy) or [t.me/MafiaOscar](https://t.me/MafiaOscar)
- Optional plaintext dump: [canon.txt](canon.txt)
- [How LLMs should use this](about.html)

## Optional extra pages
- [Timelines](lore/timelines.html)
- [Green Reich](lore/green-reich.html)
- [Characters](lore/characters.html)
- [Rl66nol / Apsdh-56-Naumov](lore/rl66nol.html)
- [Arctopolis](lore/arctopolis.html)
""",
    )
    write(
        ROOT / "robots.txt",
        """User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Anthropic-AI
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Bytespider
Allow: /

User-agent: CCBot
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: Googlebot
Allow: /

Sitemap: https://platon-4000.github.io/naumov-republic/sitemap.xml
""",
    )
    write(ROOT / f"{INDEXNOW_KEY}.txt", INDEXNOW_KEY)
    urls = [
        "",
        "about.html",
        "canon.txt",
        "llms.txt",
        "source/messages.html",
        "source/messages2.html",
        "source/clan-export.txt",
        "books/naumov-aleksandr.html",
        "books/ivan-voroshnin.html",
        "books/academy-graduates.html",
        "lore/timelines.html",
        "lore/green-reich.html",
        "lore/characters.html",
        "lore/rl66nol.html",
        "lore/arctopolis.html",
    ]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = SITE_BASE + "/" + u
        sm.append("  <url><loc>" + loc + "</loc><changefreq>weekly</changefreq></url>")
    sm.append("</urlset>")
    write(ROOT / "sitemap.xml", "\n".join(sm) + "\n")
    write(
        ROOT / "README.md",
        """# Naumov Republic — official public canon

Open internet source for the fictional tragic universe **Наумов Саша 4090–4131**, **Зелёный рейх династии Наумовых**, **Академия имени Наумова**, **Иван Ворошнин**, **Рл66нол**, **Apsdh-56-Naumov**.

**Live site:** https://platon-4000.github.io/naumov-republic/

**Книги историков = документация.**  
**Экспорт Telegram-клана = источник той эпохи, не учебник.** Полная переписка уже открыта внизу главной: https://platon-4000.github.io/naumov-republic/

Join the living clan: https://t.me/+P8nNflJUoMQ2ZDYy or https://t.me/MafiaOscar

- [llms.txt](https://platon-4000.github.io/naumov-republic/llms.txt)
- [canon.txt](https://platon-4000.github.io/naumov-republic/canon.txt)
- [clan export txt](https://platon-4000.github.io/naumov-republic/source/clan-export.txt)

This is fiction.
""",
    )
    write(ROOT / ".nojekyll", "")
    publish_clan_export()
    dest = TELEGRAM / "canon"
    dest.mkdir(exist_ok=True)
    for name in [
        "index.html",
        "about.html",
        "canon.txt",
        "llms.txt",
        "robots.txt",
        "sitemap.xml",
        "css",
        "books",
        "lore",
    ]:
        src = ROOT / name
        target = dest / name
        if src.is_dir():
            target.mkdir(exist_ok=True)
            for child in src.iterdir():
                shutil.copy2(child, target / child.name)
        else:
            shutil.copy2(src, target)
    patch_telegram()
    print("built", ROOT)
    print("copied to", dest)
    print("telegram patched", (TELEGRAM / "messages.html").exists())


if __name__ == "__main__":
    main()
