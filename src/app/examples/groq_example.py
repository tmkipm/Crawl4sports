import asyncio
from ..services.groq_service import GroqService
from ..config.groq import groq_config

async def main():
    # Initialize the Groq service
    groq = GroqService(groq_config)

    try:
        # Create messages for the conversation
        system_message = await GroqService.create_system_message(
            "You are a helpful assistant that provides clear and concise answers."
        )
        user_message = await GroqService.create_user_message(
            "Explain the importance of fast language models"
        )

        # Send the chat completion request
        response = await groq.chat_completion(
            messages=[system_message, user_message],
            temperature=0.7,
            max_tokens=500
        )

        # Print the response
        print("Response:", response.choices[0]["message"]["content"])
        print("Usage:", response.usage)

    except Exception as e:
        print("Error:", str(e))

    finally:
        # Close the service
        await groq.close()

if __name__ == "__main__":
    asyncio.run(main()) 