import json


with open('Car_Model_List.json', 'r') as f:
    lines = f.readlines()

lines = ''.join(lines)
x = json.loads(lines)
x = x['results']
types=[]
for car in x:
    categories = car['Category'].split(',')
    for category in categories:
        category = ''.join(i for i in category.strip().lower() if not i.isdigit())
        if category not in types:
            types.append(category)
print(types)
    