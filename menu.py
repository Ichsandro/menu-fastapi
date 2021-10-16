# M Ichsandro D Noor 18219094

from fastapi import FastAPI, HTTPException, Depends
import json
from authentication import AuthHandler

def IsFound(id: int):
    with open("menu.json", "r") as read_file:
        data = json.load(read_file)
    for menu_item in data['menu']:
        if menu_item['id'] == id:
            bool = True
            break
        else:
            bool = False
    return bool

with open("menu.json", "r") as read_file:
    data = json.load(read_file)

with open("user.json", "r") as read_file:
    users = json.load(read_file)
    
app = FastAPI()

auth_handler = AuthHandler()

@app.post('/register', status_code=201, tags=['User'])
def register(username: str, password: str):
    if any(x['username'] == username for x in users["user"]):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(password)
    users["user"].append({
        'username': username,
        'password': hashed_password    
    })
    with open("user.json", "w") as write_file:
            json.dump(users, write_file, indent = 3)
    return {"username": username, "password": password}

@app.post('/login', tags=['User'])
def login(username: str, password: str):
    user = None
    for x in users["user"]:
        if x['username'] == username:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }

@app.get('/menu', tags=['Menu'])
async def read_all_menu(current_user: users = Depends(auth_handler.auth_wrapper)):
    return (data['menu'])

@app.get('/menu/{item_id}', tags=['Menu'])
async def read_menu(item_id: int, current_user: users = Depends(auth_handler.auth_wrapper)):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(status_code=404, detail="Item not found")
    
@app.post('/menu', tags=['Menu'])
async def add_menu(item_id: int, name: str, current_user: users = Depends(auth_handler.auth_wrapper)):
    if (IsFound(id = item_id)):
        raise HTTPException(status_code=404, detail="Item id is Used!")
    else:
        item = {"id": item_id, "name": name}
        data["menu"].append(item)
        with open("menu.json", "w") as write_file:
            json.dump(data, write_file, indent = 3)
        return (item)

@app.patch('/menu', tags=['Menu'])
async def update_menu(item_id: int, name: str,current_user: users = Depends(auth_handler.auth_wrapper)):
    if (IsFound(id = item_id)):
        x = {"id": item_id, "name": name}
        for menu_item in data['menu']:
                if menu_item['id'] == item_id:
                    menu_item['name'] = name
                    with open("menu.json", "w") as update_file:
                        json.dump(data, update_file, indent = 3)
                    return (x)   
    else:
        raise HTTPException(status_code=404, detail="Item not found!")

@app.delete('/menu/{item_id}', tags=['Menu'])
async def delete_menu(item_id: int, current_user: users = Depends(auth_handler.auth_wrapper)):
    if (IsFound(id = item_id)):
        for i in range(len(data['menu'])):
                if data['menu'][i]['id'] == item_id:
                    x = {"id": item_id, "name": data['menu'][i]['name']}
                    del data['menu'][i]
                    break
        with open("menu.json", "w") as delete_file:
            json.dump(data, delete_file, indent = 3)
        return (x)
    else:
        raise HTTPException(status_code=404, detail="Item not found!")