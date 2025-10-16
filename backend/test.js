import OpenAI from "openai";
import dotenv from "dotenv";

dotenv.config();

const client = new OpenAI({
  apiKey: process.env.GROQ_API_KEY,
  baseURL: "https://api.groq.com/openai/v1", // ✅ Groq endpoint
});

async function runGroqResponse() {
  try {
    const response = await client.responses.create({
      model: "openai/gpt-oss-20b", // ✅ Groq-supported model
      input: "Explain the importance of fast language models",
    });

    console.log("Groq Response:\n", response.output_text);
  } catch (error) {
    console.error("Groq API Error:", error);
  }
}

runGroqResponse();