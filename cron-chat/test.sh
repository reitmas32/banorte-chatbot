curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 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" \
  -d '{
     "model": "gpt-4o-mini",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
   }'