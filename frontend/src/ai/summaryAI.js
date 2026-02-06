export const generateSummary = async (company, text) => {
    const prompt = `
  You are an ESG intelligence analyst.
  
  Summarize in 2 short sentences:
  1. What happened
  2. ESG risk or opportunity impact on ${company}
  
  News:
  ${text}
  `;
  
    const res = await fetch("http://localhost:11434/api/generate", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ model:"mistral", prompt, stream:false })
    });
  
    const data = await res.json();
    return data.response;
  };
  