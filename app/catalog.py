CATALOG = [
{"id":"H001","planner":"home","category":"lighting","name":"Warm LED Ceiling Light","platform":"IKEA","price":1299,"style":"Modern"},
{"id":"H002","planner":"home","category":"lighting","name":"Minimal Floor Lamp","platform":"Amazon","price":1899,"style":"Minimal"},
{"id":"H003","planner":"home","category":"seating","name":"Compact Accent Chair","platform":"Amazon","price":5499,"style":"Modern"},
{"id":"H004","planner":"home","category":"table","name":"4-Seater Dining Table","platform":"IKEA","price":8999,"style":"Modern"},
{"id":"H005","planner":"home","category":"decor","name":"Neutral Wall Art Set","platform":"Amazon","price":1499,"style":"Minimal"},
{"id":"H006","planner":"home","category":"storage","name":"Open Storage Shelf","platform":"IKEA","price":3999,"style":"Modern"},
{"id":"P001","planner":"party","category":"food","name":"Budget Party Catering Package","platform":"Swiggy","price":450,"unit":"per guest"},
{"id":"P002","planner":"party","category":"food","name":"Celebration Meal Package","platform":"Zomato","price":650,"unit":"per guest"},
{"id":"P003","planner":"party","category":"decoration","name":"Basic Balloon Decoration","platform":"Local Vendor","price":3500},
{"id":"P004","planner":"party","category":"decoration","name":"Premium Theme Decoration","platform":"Local Vendor","price":8500},
{"id":"P005","planner":"party","category":"venue","name":"Budget Venue Option","platform":"OYO","price":2500,"unit":"starting price"},
{"id":"P006","planner":"party","category":"entertainment","name":"Basic Music Setup","platform":"Local Vendor","price":3000},
{"id":"J001","planner":"jewelry","category":"earrings","name":"Gold-Tone Drop Earrings","platform":"Amazon","price":799,"style":"Elegant"},
{"id":"J002","planner":"jewelry","category":"necklace","name":"Minimal Pendant Necklace","platform":"Amazon","price":1299,"style":"Minimal"},
{"id":"J003","planner":"jewelry","category":"set","name":"Traditional Necklace Set","platform":"Flipkart","price":2499,"style":"Traditional"},
{"id":"J004","planner":"jewelry","category":"bracelet","name":"Classic Bracelet","platform":"Flipkart","price":999,"style":"Elegant"},
{"id":"J005","planner":"jewelry","category":"set","name":"Festive Jewelry Combo","platform":"Amazon","price":3299,"style":"Festive"},
]

def catalog_for(planner):
    return [x for x in CATALOG if x["planner"] == planner]
