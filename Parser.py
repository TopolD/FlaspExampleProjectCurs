import json

from playwright.sync_api import sync_playwright, Playwright

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://quotes.toscrape.com")
    # author = page.locator("div.quote small.author").first.text_content() это правильно получить 1 автора
    link = page.locator("div.quote a").first.get_attribute('href')
    page.click(f'a[href="{link}"]')
    page.wait_for_load_state('load')
    biograph = page.locator("div.author-details div.author-description").all_text_contents()
    print(biograph)

    # quotes = page.locator("div.quote span.text") получение цитат
    # authors = page.locator("div.quote small.author").first это не правильно
    # tags = page.locator(".tags a.tag").all_text_contents() получение тегов
    # for tag in tags:
    #     print(tag) распаковка ибо в list
    #
    # texts = quotes.all_text_contents()
    # for text in texts:
    #     print(text) распаковка ибо в list
    #
    # переход на вторую страницу
    # page.click('li.next a') переход
    # page.wait_for_load_state('load') ожидание загрузки стр
    # quotes_2 = page.locator("div.quote span.text")
    # texts_2 = quotes_2.all_text_contents()
    # for text_2 in texts_2:
    #     print(text_2)
    #
    # all_text = texts + texts_2+tags
    # with open('parses.json', 'w', encoding='utf-8') as f:
    #     json.dump(all_text, f, ensure_ascii=False, indent=4)

    # логин
    # page.click('a[href="/login"]')
    # page.fill("input#username", "admin")
    # page.fill("input#password", "<PASSWORD>")
    #
    # page.click('input[type="submit"]')
    # print("Логин успешен?", page.url != "https://quotes.toscrape.com/login")
    browser.close()
