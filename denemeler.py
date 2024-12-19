# Jupyter Notebook içinde
import json
from datetime import datetime

# data.json dosyasını oku
with open('data.json', 'r') as f:
    data = json.load(f)

# JSON verisini Pydantic sınıfına dönüştür
user = User(**data)

# Kullanıcı verisini inceleyelim
print(user)
print(f"User email: {user.email}")
print(f"Last sign-in at: {user.last_sign_in_at}")
