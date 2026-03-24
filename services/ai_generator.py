import openai, json, os

def generate_exam_content(subject_name, topic_title):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Generate 10 JAMB-style MCQs for {subject_name}: {topic_title}. Return JSON list: [{{question, a, b, c, d, answer, explanation}}]"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content).get('questions', [])