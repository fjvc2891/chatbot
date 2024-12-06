from faker import Faker
import random
import pandas as pd

# Inicializar Faker
fake = Faker()

# Configurar categorías y opciones
categories = ['Zapatos', 'Ropa']
sizes_shoes = ['38', '39', '40', '41', '42', '43']
sizes_clothes = ['S', 'M', 'L', 'XL']
colors = ['negro', 'blanco', 'rojo', 'azul', 'verde', 'amarillo', 'gris']
brands = ['Nike', 'Adidas', 'Puma', 'Reebok', 'Levis', 'Zara', 'H&M']

# Generar datos
data = []
for _ in range(100):  # Cambia el número para generar más datos
    category = random.choice(categories)
    sizes = sizes_shoes if category == 'Zapatos' else sizes_clothes
    product = {
        'name': f"{fake.word().capitalize()} {random.choice(brands)}",
        'category': category,
        'price': round(random.uniform(20, 200), 2),
        'sizes': ', '.join(random.sample(sizes, random.randint(1, 4))),
        'colors': ', '.join(random.sample(colors, random.randint(1, 3))),
        'description': fake.sentence(),
        'stock': random.randint(5, 50)
    }
    data.append(product)

# Guardar los datos en un DataFrame
df = pd.DataFrame(data)

# Exportar a un archivo CSV
df.to_csv('productos_fake.csv', index=False)

print("Datos generados y guardados en 'productos_fake.csv'")
