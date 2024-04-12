# example_usage.py

from product_description_generator import generate_product_description


product_name = "Смарт-часы XYZ"
product_features = "водонепроницаемые, с шагомером, мониторинг сна"
keywords = "умные часы, фитнес браслет, трекер активности, члены, носки"

description = generate_product_description(api_key, product_name, product_features, keywords)
print(description)
