import openai

# Инициализация клиента OpenAI с вашим API-ключом
api_key = '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'  # Замените на ваш реальный API-ключ
client = openai.OpenAI(api_key=api_key)

def generate_tier2_keywords(product_name, user_keywords, model="gpt-4-turbo"):
    """
    Генерирует список из 10 ключевых слов второго уровня (т.н. тир 2) для товара, основываясь на первичных ключевых словах (т.н. тир 1).

    Параметры:
    :param product_name: Название товара.
    :param user_keywords: Ключевые слова, введенные пользователем (ключевики тир 1).
    :param model: Используемая модель GPT для генерации.
    :return: Список ключевых слов тир 2.
    """
    # Строим запрос для генерации ключевых слов тир 2
    prompt_tier2_keywords = (
        f"Для товара '{product_name}', исходя из ключевых слов {user_keywords}, "
        "сгенерируйте список из 10 дополнительных ключевых слов (ключевики тир 2), "
        "релевантных для российских маркетплейсов, таких как Яндекс Маркет, OZON и Wildberries."
    )

    # Выполняем запрос к модели OpenAI
    response_tier2 = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt_tier2_keywords}]
    )

    # Обрабатываем и возвращаем полученный список ключевых слов
    tier2_keywords = response_tier2.choices[0].message.content.strip().split(", ")
    return tier2_keywords

def generate_product_description_V2(product_name, product_features, tier1_keywords, tier2_keywords, model="gpt-4-turbo-2024-04-09"):
    """
    Генерирует описание товара для российских маркетплейсов, используя ключевые слова тир 1 и тир 2.

    Параметры:
    :param product_name: Название товара.
    :param product_features: Характеристики товара.
    :param tier1_keywords: Ключевые слова первого уровня.
    :param tier2_keywords: Ключевые слова второго уровня.
    :param model: Используемая модель GPT.
    :return: Сгенерированное описание товара.
    """
    # Формируем запрос для генерации описания
    prompt_final_description = (
        f"Создайте продажное описание для товара '{product_name}', учитывая следующие условия:\n"
        f"- Используйте обязательно ВСЕ ключевые слова тир 1 (введенне): {', '.join(tier1_keywords)}.\n"
        f"- Можете также использовать ключевые слова тир 2 (менее предпочтительные, но только релевантные): {', '.join(tier2_keywords)}.\n"
        f"Характеристики товара(должны быть в описание обязательно все): {product_features}.\n"
        "Главные правила: описание должно быть написано сплошным текстом, без абзацев, без повторов одного слова более 4 раз, и не превышать 3000 символов, текст должен быть без смайликов."
    )

    # Выполняем запрос к модели OpenAI
    response_final = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt_final_description}]
    )

    # Возвращаем текст без переносов строк
    return response_final.choices[0].message.content.replace("\n", " ")



