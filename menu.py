# M Ichsandro D Noor 18219094

from fastapi import FastAPI, HTTPException
import json

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

app = FastAPI()

@app.get('/menu')
async def read_all_menu():
	return data['menu'] 

@app.get('/menu/{item_id}')
async def read_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(status_code=404, detail="Item not found")
    
@app.post('/menu')
async def add_menu(item_id: int, name: str):
    if (IsFound(id = item_id)):
        raise HTTPException(status_code=404, detail="Item id is Used!")
    else:
        item = {"id": item_id, "name": name}
        data["menu"].append(item)
        with open("menu.json", "w") as write_file:
            json.dump(data, write_file, indent = 3)
        return (item)

@app.patch('/menu')
async def update_menu(item_id: int, name: str):
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

@app.delete('/menu/{item_id}')
async def delete_menu(item_id: int):
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