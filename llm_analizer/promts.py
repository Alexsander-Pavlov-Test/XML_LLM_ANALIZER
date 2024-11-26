def analysys_prompt(
    date: str,
    revenue: str,
    products: str,
    categories: str,
    ) -> dict[str, str]:
    """
    Составление запроса для LLM

    Args:
        date (str): Дата выборки для анализа
        revenue (str): Выручка
        products (str): Топ продуктов
        category (str): Категории

    Returns:
        dict[str, str]: Prompt
    """
    analysys_prompt_test = dict(
    system='You are the best data analyst.',
    user=f"""Analyze sales data for {date}:
1. Total revenue: {revenue}.
2. Top 3 products by sales: {products}. 
3. Distribution by categories: {categories}.

Write a short analytical report with conclusions and recommendations.
This is very important for my career""",
)
    return analysys_prompt_test
