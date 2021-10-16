from fastapi import FastAPI, HTTPException, Depends
import json
from .authentication import AuthHandler
from .schemas import Item, User

def IsFound(id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == id:
            bool = True
            break
        else:
            bool = False
    return bool

with open("src/menu.json", "r") as read_file:
    data = json.load(read_file)

with open("src/user.json", "r") as read_file:
    users = json.load(read_file)
    
app = FastAPI()

auth_handler = AuthHandler()

@app.get("/", tags=['Home'])
def home():
    nama = "M Ichsandro D Noor"
    nim = "18219094"
    return({"Nama": nama, "NIM": nim})

@app.post('/register', status_code=201, tags=['User'])
def register(user: User):
    if any(x['username'] == user.username for x in users["user"]):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(user.password)
    users["user"].append({
        'username': user.username,
        'password': hashed_password    
    })
    with open("src/user.json", "w") as write_file:
            json.dump(users, write_file, indent = 3)
    return {"username": user.username, "password": user.password}

@app.post('/login', tags=['User'])
def login(user: User):
    current_user = None
    for x in users["user"]:
        if x['username'] == user.username:
            current_user = x
            break
    
    if (current_user is None) or (not auth_handler.verify_password(user.password, current_user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(current_user['username'])
    return { 'token': token }

@app.get('/menu', tags=['Menu'])
def read_all_menu(current_user: users = Depends(auth_handler.auth_wrapper)):
    return (data['menu'])

@app.get('/menu/{item_id}', tags=['Menu'])
def read_menu(item_id: int, current_user: users = Depends(auth_handler.auth_wrapper)):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(status_code=404, detail="Item not found")
    
@app.post('/menu', tags=['Menu'])
def add_menu(item: Item, current_user: users = Depends(auth_handler.auth_wrapper)):
    if (IsFound(id = item.id)):
        raise HTTPException(status_code=404, detail="Item id is Used!")
    else:
        item = {"id": item.id, "name": item.name}
        data["menu"].append(item)
        with open("src/menu.json", "w") as write_file:
            json.dump(data, write_file, indent = 3)
        return (item)

@app.patch('/menu', tags=['Menu'])
def update_menu(item : Item, current_user: users = Depends(auth_handler.auth_wrapper)):
    if (IsFound(id = item.id)):
        x = {"id": item.id, "name": item.name}
        for menu_item in data['menu']:
                if menu_item['id'] == item.id:
                    menu_item['name'] = item.name
                    with open("src/menu.json", "w") as update_file:
                        json.dump(data, update_file, indent = 3)
                    return (x)   
    else:
        raise HTTPException(status_code=404, detail="Item not found!")

@app.delete('/menu/{item_id}', tags=['Menu'])
def delete_menu(item_id: int, current_user: users = Depends(auth_handler.auth_wrapper)):
    if (IsFound(id = item_id)):
        for i in range(len(data['menu'])):
                if data['menu'][i]['id'] == item_id:
                    x = {"id": item_id, "name": data['menu'][i]['name']}
                    del data['menu'][i]
                    break
        with open("src/menu.json", "w") as delete_file:
            json.dump(data, delete_file, indent = 3)
        return (x)
    else:
        raise HTTPException(status_code=404, detail="Item not found!")