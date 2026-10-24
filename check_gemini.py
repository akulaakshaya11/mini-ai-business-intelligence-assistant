
from app.interpreter import interpret_question

try:
    result = interpret_question(
        "Which product makes the most money?"
    )
    print("SUCCESS! Gemini interpreted the question:")
    print(result)

except Exception as error:
    print("Gemini test failed.")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))
