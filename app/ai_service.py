import json
import re
from pathlib import Path
from PIL import Image
from .catalog import catalog_for
from .config import GEMINI_API_KEY, GEMINI_MODEL

def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text, flags=re.I).strip()
        text = re.sub(r"```$", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        a, b = text.find("{"), text.rfind("}")
        if a >= 0 and b > a:
            return json.loads(text[a:b+1])
        raise

def demo(planner, data):
    budget = float(data["budget"])
    items = catalog_for(planner)
    if planner == "home":
        allocation = [
            {"category":"Lighting","amount":round(budget*.20,2)},
            {"category":"Furniture","amount":round(budget*.55,2)},
            {"category":"Decor","amount":round(budget*.15,2)},
            {"category":"Reserve","amount":round(budget*.10,2)}]
        summary = f"Demo {data.get('style','Modern')} plan for {', '.join(data.get('rooms',[]))}."
    elif planner == "party":
        allocation = [
            {"category":"Food","amount":round(budget*.50,2)},
            {"category":"Decoration","amount":round(budget*.20,2)},
            {"category":"Venue","amount":round(budget*.20,2)},
            {"category":"Reserve","amount":round(budget*.10,2)}]
        summary = f"Demo plan for {data['event_type']} with {data['guests']} guests."
    else:
        allocation = [
            {"category":"Main jewelry","amount":round(budget*.55,2)},
            {"category":"Secondary piece","amount":round(budget*.25,2)},
            {"category":"Reserve","amount":round(budget*.20,2)}]
        summary = f"Demo {data['style']} jewelry plan for {data['occasion']}."
    return {
        "planner": planner, "summary": summary, "budget": budget,
        "allocation": allocation,
        "recommendations": [
            {"id":x["id"],"name":x["name"],"category":x["category"],
             "platform":x["platform"],"price":x["price"],
             "reason":f"Fits the {planner} planning context."}
            for x in items[:4]],
        "tips":[
            "Demo prices are not live prices; compare current seller prices before buying.",
            "Keep a reserve for delivery, taxes or unexpected costs.",
            "Prioritize essential items before optional upgrades."
        ],
        "source":"demo-fallback"
    }

def generate_recommendation(planner, data, image_path=None):
    if not GEMINI_API_KEY:
        return demo(planner, data)
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GEMINI_API_KEY)
        catalog = catalog_for(planner)
        prompt = f'''You are PocketSmart AI, a budget-aware recommendation assistant.
Respect the user's total budget. Use ONLY the catalog supplied below.
Never invent IDs, platforms, prices or URLs. Catalog prices are demo values.
Return valid JSON only.

Planner: {planner}
User request:
{json.dumps(data, indent=2)}

Catalog:
{json.dumps(catalog, indent=2)}

Return:
{{
 "planner":"{planner}",
 "summary":"short summary",
 "budget":{float(data["budget"])},
 "allocation":[{{"category":"name","amount":0}}],
 "recommendations":[{{"id":"catalog id","name":"catalog name","category":"category","platform":"platform","price":0,"reason":"why it fits"}}],
 "tips":["tip 1","tip 2"],
 "source":"gemini"
}}'''
        contents = [prompt]
        if image_path:
            contents += [Image.open(Path(image_path)),
                         "Use visible outfit colors/style only as a high-level coordination signal."]
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(temperature=.3, max_output_tokens=2500)
        )
        result = extract_json(response.text)
        result["planner"] = planner
        result["budget"] = float(data["budget"])
        result["source"] = f"gemini:{GEMINI_MODEL}"
        return result
    except Exception as exc:
        result = demo(planner, data)
        result["ai_error"] = str(exc)[:300]
        return result
