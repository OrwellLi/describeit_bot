import openai

def generate_product_description(api_key, product_name, product_features, keywords):
    """
    Генерирует описание товара для Wildberries c использованием модели GPT-3.5-turbo от OpenAI.
    
    :param api_key: API ключ от OpenAI.
    :param product_name: Название товара.
    :param product_features: Характеристики товара.
    :param keywords: Ключевые слова для SEO.
    :return: Сгенерированное описание товара.
    """
    client = openai.OpenAI(api_key=api_key)

    # master_prompt = (
    #     "Вы пишете крутое продажное описание карточки товара на Wildberries. "
    #     "Создайте описание, которое будет оптимизировано для поисковых систем, "
    #     "используя ключевые слова и подчеркнув преимущества товара."
    # )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # {"role": "system", "content": master_prompt},
            {"role": "user", "content": f"Напишите описание для товара '{product_name}'. Характеристики: {product_features}. Ключевые слова: {keywords}."}
        ]
    )

    return response.choices[0].message.content
